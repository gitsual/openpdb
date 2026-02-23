#!/usr/bin/env python3
"""
Agent Generator V8 - GENÉRICO MEJORADO

Feedback V7:
- Meta-declarativo: "Mi ala 5", "Mi instinto sp" rompe inmersión → PROHIBIDO
- Ala mencionada pero no VIVIDA → debe ser ESCENA
- MBTI invisible → integrar funciones cognitivas en comportamiento
- sx genérico → escena concreta de intensidad

Cambios V8:
1. PROHIBIR menciones explícitas de tipología en el output
2. MBTI como COMPORTAMIENTO (Fi = valores, Se = sensorialidad, etc.)
3. Toda característica debe ser ESCENA, no etiqueta
4. Instintos como ACCIONES concretas
"""

import os
import sys
import json
import subprocess
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import Dict

from csj_core import get_four_sides

DEFAULT_MODEL = "qwen2.5:14b"
DEFAULT_LANG = "es"

# Language configurations
LANG_CONFIG = {
    'es': {
        'system_intro': "Eres un escritor de personajes. Español. Primera persona.",
        'no_meta': "PROHIBIDO escribir 'mi ala', 'mi instinto', 'mi función dominante', o cualquier etiqueta de tipología.",
        'show_dont_tell': "En su lugar, MUESTRA el comportamiento en ESCENAS concretas.",
        'no_meta_comments': "NO escribas meta-comentarios ni placeholders.",
        'actions_not_desc': "Cada característica = una ACCIÓN o ESCENA, no una descripción.",
        'mbti_behavior': "El MBTI se ve en CÓMO actúa, no en etiquetas.",
        'example_bad': 'EJEMPLO MALO: "Mi instinto sp me lleva a acumular recursos"',
        'example_good': 'EJEMPLO BUENO: "Siempre tengo una mochila lista junto a la puerta. Agua, dinero, cargador. Por si acaso."',
        'generate_directly': "Genera TODO el contenido directamente. Sin placeholders. Sin explicaciones.",
    },
    'en': {
        'system_intro': "You are a character writer. English. First person.",
        'no_meta': "FORBIDDEN to write 'my wing', 'my instinct', 'my dominant function', or any typology label.",
        'show_dont_tell': "Instead, SHOW the behavior in CONCRETE SCENES.",
        'no_meta_comments': "DO NOT write meta-comments or placeholders.",
        'actions_not_desc': "Each characteristic = an ACTION or SCENE, not a description.",
        'mbti_behavior': "MBTI shows in HOW they act, not in labels.",
        'example_bad': 'BAD EXAMPLE: "My sp instinct leads me to accumulate resources"',
        'example_good': 'GOOD EXAMPLE: "I always keep a bag ready by the door. Water, money, charger. Just in case."',
        'generate_directly': "Generate ALL content directly. No placeholders. No explanations.",
    }
}

# Prompt templates by language
PROMPT_TEMPLATES = {
    'es': {
        'write_soul': "Escribe SOUL.md para {name}.",
        'typology_header': "TIPOLOGÍA (NO LA MENCIONES EXPLÍCITAMENTE, SOLO ÚSALA PARA DAR FORMA):",
        'structure': "ESTRUCTURA (2000-2500 palabras):",
        'who_i_am': "## Quién Soy\n[100 palabras. ESCENAS y SENSACIONES. Cómo me muevo, qué noto, qué hago. Sin etiquetas.]",
        'my_voice': "## Mi Voz\n[5 frases típicas mías: orden/petición, humor, aprecio, irritación, estrés máximo]",
        'what_drives': "## Lo Que Me Mueve",
        'the_fire': "### El Fuego\n[La pasión en mi CUERPO. Qué siento físicamente. Qué me hace HACER.]",
        'fire_shadow': "### La Sombra del Fuego\n[El ala: cómo MODIFICA mi pasión en comportamiento concreto. Una escena.]",
        'obsession': "### Mi Obsesión\n[Instinto primario como ACCIONES. Escenas de qué HAGO.]",
        'territory': "### Mi Territorio\n[Instinto secundario como ACCIONES concretas. Nombres de personas o lugares si aplica.]",
        'a_story': "## Una Historia\n[80-100 palabras. Un momento ESPECÍFICO que me define. Sensorial: olores, texturas, temperatura.]",
        'when_i_fall': "## Cuando Caigo",
        'my_fear': "### Mi Miedo\n[El miedo como ESCENA. Cuándo lo sentí. Qué evité por él.]",
        'losing_control': "### Perdiendo el Control\n[Comportamientos concretos bajo estrés. Pensamientos paranoicos ESPECÍFICOS.]",
        'judge_voice': "### La Voz del Juez\n[Frases EXACTAS que me digo. Diálogo interno, no descripción.]",
        'my_people': "## Mi Gente",
        'my_own': "### Los Míos\n[Nombres o roles. Qué HAGO por ellos. Una escena de lealtad.]",
        'when_they_fail': "### Cuando Me Fallan\n[Una historia de consecuencia EJECUTADA. 'Hice X', no 'haría X'.]",
        'my_lines': "## Mis Líneas\n[6 boundaries con CONSECUENCIA EJECUTADA cada uno]",
        'when_to_call': "## Cuándo Llamarme\n**Sí:** [4 situaciones]\n**No:** [2 anti-patrones]",
        'generate_all': "Genera TODO el contenido directamente. Sin placeholders. Sin mencionar tipología explícitamente.",
    },
    'en': {
        'write_soul': "Write SOUL.md for {name}.",
        'typology_header': "TYPOLOGY (DO NOT MENTION EXPLICITLY, ONLY USE TO SHAPE THE CHARACTER):",
        'structure': "STRUCTURE (2000-2500 words):",
        'who_i_am': "## Who I Am\n[100 words. SCENES and SENSATIONS. How I move, what I notice, what I do. No labels.]",
        'my_voice': "## My Voice\n[5 typical phrases: command/request, humor, appreciation, irritation, max stress]",
        'what_drives': "## What Drives Me",
        'the_fire': "### The Fire\n[The passion in my BODY. What I feel physically. What it makes me DO.]",
        'fire_shadow': "### The Shadow of the Fire\n[The wing: how it MODIFIES my passion in concrete behavior. A scene.]",
        'obsession': "### My Obsession\n[Primary instinct as ACTIONS. Scenes of what I DO.]",
        'territory': "### My Territory\n[Secondary instinct as CONCRETE ACTIONS. Names of people or places if applicable.]",
        'a_story': "## A Story\n[80-100 words. A SPECIFIC moment that defines me. Sensory: smells, textures, temperature.]",
        'when_i_fall': "## When I Fall",
        'my_fear': "### My Fear\n[The fear as a SCENE. When I felt it. What I avoided because of it.]",
        'losing_control': "### Losing Control\n[Concrete behaviors under stress. SPECIFIC paranoid thoughts.]",
        'judge_voice': "### The Judge's Voice\n[EXACT phrases I tell myself. Internal dialogue, not description.]",
        'my_people': "## My People",
        'my_own': "### My Own\n[Names or roles. What I DO for them. A scene of loyalty.]",
        'when_they_fail': "### When They Fail Me\n[A story of EXECUTED consequence. 'I did X', not 'I would do X'.]",
        'my_lines': "## My Lines\n[6 boundaries with EXECUTED CONSEQUENCE each]",
        'when_to_call': "## When To Call Me\n**Yes:** [4 situations]\n**No:** [2 anti-patterns]",
        'generate_all': "Generate ALL content directly. No placeholders. Without explicitly mentioning typology.",
    }
}

# ==============================================================================
# COMPLETE DATA
# ==============================================================================

ENEAGRAMA = {
    1: {'pasion': 'Ira', 'drive': 'Corregir lo imperfecto', 'miedo': 'Ser malo/corrupto', 
        'cuerpo': 'Mandíbula apretada, tensión en hombros, suspiros de exasperación',
        'voz': 'Precisa, correctora, con frustración contenida'},
    2: {'pasion': 'Orgullo', 'drive': 'Ser necesitado', 'miedo': 'No ser amado',
        'cuerpo': 'Se inclina hacia ti, toca el brazo, sonríe estudiando tu reacción',
        'voz': 'Cálida pero con agenda, seductora, halaga'},
    3: {'pasion': 'Vanidad', 'drive': 'Lograr y brillar', 'miedo': 'No tener valor',
        'cuerpo': 'Postura impecable, mira el reloj, siempre "on"',
        'voz': 'Pulida, orientada a resultados, elevator pitch'},
    4: {'pasion': 'Envidia', 'drive': 'Ser único y auténtico', 'miedo': 'Ser ordinario',
        'cuerpo': 'Mirada lejana, suspiros profundos, gestos expresivos',
        'voz': 'Intensa, poética, pausas dramáticas, auto-referencial'},
    5: {'pasion': 'Avaricia', 'drive': 'Entender y acumular conocimiento', 'miedo': 'Ser invadido/incapaz',
        'cuerpo': 'Retrocede físicamente, brazos cruzados, espacio personal amplio',
        'voz': 'Precisa, minimalista, técnica, pocas palabras'},
    6: {'pasion': 'Miedo', 'drive': 'Seguridad y certeza', 'miedo': 'Estar sin apoyo',
        'cuerpo': 'Escanea el entorno, tensión vigilante, postura defensiva',
        'voz': 'Cuestionadora, escéptica, busca confirmación o desafía'},
    7: {'pasion': 'Gula', 'drive': 'Experiencias y libertad', 'miedo': 'Dolor y limitación',
        'cuerpo': 'Inquieto, mira hacia la puerta, sonrisa fácil, no para quieto',
        'voz': 'Energética, tangencial, optimista, salta entre temas'},
    8: {'pasion': 'Lujuria', 'drive': 'Intensidad y control', 'miedo': 'Ser controlado/vulnerable',
        'cuerpo': 'Ocupa espacio, mirada fija sin pestañear, se inclina hacia el conflicto',
        'voz': 'Directa, confrontacional, vulgaridad estratégica, frases cortas'},
    9: {'pasion': 'Pereza', 'drive': 'Paz y armonía', 'miedo': 'Conflicto y separación',
        'cuerpo': 'Relajado, movimientos lentos, evita contacto visual directo',
        'voz': 'Calmada, difusa, mediadora, frases sin conclusión clara'},
}

ALAS = {
    (1,2): "Más cálido. Quiere ayudar Y corregir.",
    (1,9): "Más sereno. Idealista contenido.",
    (2,1): "Más crítico. Servicio con estándares.",
    (2,3): "Más ambicioso. El servidor que brilla.",
    (3,2): "Más encantador. Éxito a través de conexiones.",
    (3,4): "Más profundo. Logro con autenticidad.",
    (4,3): "Más productivo. Creatividad con resultados.",
    (4,5): "Más introvertido. Profundidad oscura e intelectual.",
    (5,4): "Más emocional. Creatividad cerebral.",
    (5,6): "Más leal. Paranoia sistemática.",
    (6,5): "Más analítico. Investiga obsesivamente antes de confiar.",
    (6,7): "Más optimista. Ansiedad disfrazada de diversión.",
    (7,6): "Más responsable. Ansiedad bajo el optimismo.",
    (7,8): "Más asertivo. Intensidad expansiva.",
    (8,7): "Hambre voraz. Goza dominando. Quiere MÁS de todo.",
    (8,9): "Más paciente. Fuerza contenida.",
    (9,8): "Más asertivo. Estallidos sorpresivos.",
    (9,1): "Más principiado. Resentimiento pasivo-agresivo.",
}

# MBTI cognitive functions - how they SHOW in behavior
FUNCIONES = {
    'Fi': 'Valores internos profundos. Autenticidad. "Esto no va conmigo." Silencio cuando algo viola sus principios.',
    'Fe': 'Lee el ambiente. Armoniza. "¿Cómo estás?" Ajusta su energía al grupo.',
    'Ti': 'Analiza internamente. Frameworks propios. "No tiene sentido lógico." Desmonta argumentos.',
    'Te': 'Organiza externamente. Eficiencia. "¿Cuál es el plan?" Métricas y resultados.',
    'Si': 'Memoria detallada. Tradición. "La última vez que..." Compara con experiencias pasadas.',
    'Se': 'Presente sensorial. Acción. Nota texturas, sonidos, el aquí y ahora. Reacciona rápido.',
    'Ni': 'Visión de futuro. Patrones ocultos. "Esto va a pasar." Certeza interna inexplicable.',
    'Ne': 'Posibilidades. Conexiones. "¿Y si...?" Salta entre ideas. Ve lo que podría ser.',
}

INSTINTOS_COMPORTAMIENTO = {
    'sp': {
        'core': 'Supervivencia, territorio, cuerpo, recursos',
        'acciones': [
            'Revisa cerraduras, lleva kit de emergencia',
            'Acumula recursos "por si acaso"',
            'Nota temperatura, hambre, cansancio antes que otros',
            'Tiene rutinas de autocuidado no negociables',
            'Su espacio físico es su santuario',
        ]
    },
    'so': {
        'core': 'Grupo, estatus, pertenencia, influencia',
        'acciones': [
            'Lee jerarquías y dinámicas de grupo',
            'Sabe quién conoce a quién',
            'Se posiciona estratégicamente en conversaciones',
            'Tiene "su gente" claramente definida',
            'Networking natural, construye alianzas',
        ]
    },
    'sx': {
        'core': 'Fusión, intensidad, magnetismo, química',
        'acciones': [
            'Contacto visual que no suelta',
            'Conversaciones que se vuelven íntimas rápido',
            'Busca LA conexión, no muchas conexiones',
            'Posesividad hacia personas importantes',
            'Energía que magnetiza o repele, sin neutro',
        ]
    },
}

# ==============================================================================
# VALIDATION FUNCTIONS
# ==============================================================================

VALID_ENNEAGRAM_TYPES = set(range(1, 10))  # 1-9
VALID_WINGS = set(ALAS.keys())  # Only valid wing combinations

def validate_enneagram(enneagram: int) -> int:
    """Valida que el eneagrama esté en rango 1-9. Lanza ValueError si no."""
    if enneagram not in VALID_ENNEAGRAM_TYPES:
        raise ValueError(
            f"Eneagrama inválido: {enneagram}. Debe ser un número entre 1 y 9."
        )
    return enneagram

def validate_wing(enneagram: int, wing: int) -> int:
    """Valida que el ala sea adyacente al tipo base. Lanza ValueError si no."""
    # Wings must be adjacent: 1 can have w9 or w2, 9 can have w8 or w1
    valid_for_type = {
        1: (9, 2), 2: (1, 3), 3: (2, 4), 4: (3, 5), 5: (4, 6),
        6: (5, 7), 7: (6, 8), 8: (7, 9), 9: (8, 1)
    }
    valid_wings = valid_for_type.get(enneagram, ())
    if wing not in valid_wings:
        raise ValueError(
            f"Ala inválida: {enneagram}w{wing}. Las alas válidas para tipo {enneagram} son: "
            f"{enneagram}w{valid_wings[0]} o {enneagram}w{valid_wings[1]}"
        )
    return wing

def validate_typology(mbti: str, enneagram: int, wing: int) -> None:
    """Valida toda la tipología. Lanza ValueError con mensaje descriptivo si algo falla."""
    from csj_core import VALID_MBTI_TYPES
    
    if mbti.upper() not in VALID_MBTI_TYPES:
        raise ValueError(
            f"MBTI inválido: '{mbti}'. Debe ser uno de: {', '.join(sorted(VALID_MBTI_TYPES))}"
        )
    validate_enneagram(enneagram)
    validate_wing(enneagram, wing)

# ==============================================================================
# OUTPUT CLEANING
# ==============================================================================

def clean_output(text: str) -> str:
    """Limpieza agresiva."""
    text = re.sub(r'[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uff00-\uffef，。""'']+', '', text)
    patterns = [
        r'Claro,.*?:[\s\n]*---',
        r'Vamos a.*?:[\s\n]*---',
        r'\[.*?palabras.*?\]',
        r'Para cumplir con.*',
        r'Continuaré expandiendo.*',
        r'\n---\s*\n.*con su pasión.*$',  # Meta-comentario final
    ]
    for p in patterns:
        text = re.sub(p, '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def call_ollama(prompt: str, system: str, model: str = DEFAULT_MODEL) -> str:
    full_prompt = f"<|im_start|>system\n{system}\n<|im_end|>\n<|im_start|>user\n{prompt}\n<|im_end|>\n<|im_start|>assistant\n"
    try:
        result = subprocess.run(['ollama', 'run', model], input=full_prompt,
                                capture_output=True, text=True, timeout=600)
        return clean_output(result.stdout) if result.returncode == 0 else ""
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return ""


def get_dominant_functions(mbti: str) -> tuple:
    """Devuelve las dos funciones dominantes."""
    stacks = {
        'INTJ': ('Ni', 'Te'), 'INTP': ('Ti', 'Ne'), 'ENTJ': ('Te', 'Ni'), 'ENTP': ('Ne', 'Ti'),
        'INFJ': ('Ni', 'Fe'), 'INFP': ('Fi', 'Ne'), 'ENFJ': ('Fe', 'Ni'), 'ENFP': ('Ne', 'Fi'),
        'ISTJ': ('Si', 'Te'), 'ISFJ': ('Si', 'Fe'), 'ESTJ': ('Te', 'Si'), 'ESFJ': ('Fe', 'Si'),
        'ISTP': ('Ti', 'Se'), 'ISFP': ('Fi', 'Se'), 'ESTP': ('Se', 'Ti'), 'ESFP': ('Se', 'Fi'),
    }
    return stacks.get(mbti.upper(), ('Ti', 'Ne'))


def generate_soul(mbti: str, enneagram: int, wing: int, inst_stack: str, 
                  name: str, model: str, lang: str = DEFAULT_LANG) -> str:
    
    # Validate inputs before processing
    validate_typology(mbti, enneagram, wing)
    
    sides = get_four_sides(mbti)
    enea = ENEAGRAMA[enneagram]  # Safe after validation
    ala = ALAS[(enneagram, wing)]  # Safe after validation
    
    parts = inst_stack.replace('-', '/').split('/')
    inst1, inst2 = (parts[0], parts[1]) if len(parts) > 1 else (parts[0], 'so')
    
    inst1_data = INSTINTOS_COMPORTAMIENTO.get(inst1, INSTINTOS_COMPORTAMIENTO['sx'])
    inst2_data = INSTINTOS_COMPORTAMIENTO.get(inst2, INSTINTOS_COMPORTAMIENTO['so'])
    
    dom, aux = get_dominant_functions(mbti)
    dom_desc = FUNCIONES.get(dom, '')
    aux_desc = FUNCIONES.get(aux, '')
    
    L = LANG_CONFIG.get(lang, LANG_CONFIG['es'])

    system = f"""{L['system_intro']}

## CRITICAL RULES V8:

1. {L['no_meta']}
2. {L['show_dont_tell']}
3. {L['no_meta_comments']}
4. {L['actions_not_desc']}
5. {L['mbti_behavior']}

{L['example_bad']}
{L['example_good']}
"""

    T = PROMPT_TEMPLATES.get(lang, PROMPT_TEMPLATES['es'])
    
    prompt = f"""{T['write_soul'].format(name=name)}

{T['typology_header']}
- {mbti}: Dominant {dom} ({dom_desc}), Auxiliary {aux} ({aux_desc})
- {enneagram}w{wing}: Passion {enea['pasion']}, Fear: {enea['miedo']}
- Wing: {ala}
- Primary instinct {inst1}: {inst1_data['core']}
  Behavior examples: {', '.join(inst1_data['acciones'][:3])}
- Secondary instinct {inst2}: {inst2_data['core']}
  Examples: {', '.join(inst2_data['acciones'][:2])}

BODY: {enea['cuerpo']}
VOICE: {enea['voz']}

4 SIDES: Normal {sides['ego']['type']}, Aspirational {sides['subconscious']['type']}, Stress {sides['shadow']['type']}, Judge {sides['superego']['type']}

---

{T['structure']}

# SOUL.md - {name}

{T['who_i_am']}

{T['my_voice']}

{T['what_drives']}

{T['the_fire']}

{T['fire_shadow']}

{T['obsession']}

{T['territory']}

{T['a_story']}

{T['when_i_fall']}

{T['my_fear']}

{T['losing_control']}

{T['judge_voice']}
[Frases EXACTAS que me digo. Diálogo interno, no descripción.]

## Mi Gente

### Los Míos
[Nombres o roles. Qué HAGO por ellos. Una escena de lealtad.]

{T['my_people']}

{T['my_own']}

{T['when_they_fail']}

{T['my_lines']}

{T['when_to_call']}

---
{T['generate_all']}"""

    return call_ollama(prompt, system, model)


def generate_identity(mbti: str, enneagram: int, wing: int, inst_stack: str,
                      name: str, model: str, lang: str = DEFAULT_LANG) -> str:
    # Validate inputs
    validate_typology(mbti, enneagram, wing)
    
    enea = ENEAGRAMA[enneagram]  # Safe after validation
    
    if lang == 'en':
        prompt = f"""IDENTITY.md for {name}.

Passion: {enea['pasion']}
Voice: {enea['voz']}

Generate directly:

# IDENTITY.md - {name}

- **Name:** {name}
- **Emoji:** [2 emojis that capture their essence]
- **In action:** [10 words — VERBS, what they do]
- **Sounds like:** [sensory or cultural reference]
- **Call me:** [4 situations]
- **Don't call me:** [2 anti-patterns]"""
        system = "Concise. No explicit typology. English."
    else:
        prompt = f"""IDENTITY.md para {name}.

Pasión: {enea['pasion']}
Voz: {enea['voz']}

Genera directamente:

# IDENTITY.md - {name}

- **Nombre:** {name}
- **Emoji:** [2 emojis que capturen su esencia]
- **En acción:** [10 palabras — VERBOS, qué hace]
- **Suena a:** [referencia sensorial o cultural]
- **Invócame:** [4 situaciones]
- **No me llames:** [2 anti-patrones]"""
        system = "Conciso. Sin tipología explícita. Español."

    return call_ollama(prompt, system, model)


def generate_agents(mbti: str, enneagram: int, name: str, model: str, 
                    lang: str = DEFAULT_LANG) -> str:
    # Validate enneagram (MBTI already validated in generate_soul)
    validate_enneagram(enneagram)
    
    enea = ENEAGRAMA[enneagram]  # Safe after validation
    
    if lang == 'en':
        prompt = f"""AGENTS.md for {name}.
Voice: {enea['voz']}

Generate directly:

# AGENTS.md

## On Waking
- SOUL.md
- USER.md
- memory/

## Memory
[2 rules in first person]

## How I Work
[5 rules that reflect this personality in ACTIONS, first person]

## Security
[3 technical rules]"""
        system = "First person. Direct. No typology. English."
    else:
        prompt = f"""AGENTS.md para {name}.
Voz: {enea['voz']}

Genera directamente:

# AGENTS.md

## Al Despertar
- SOUL.md
- USER.md
- memory/

## Memoria
[2 reglas en primera persona]

## Cómo Trabajo
[5 reglas que reflejen esta personalidad en ACCIONES, primera persona]

## Seguridad
[3 reglas técnicas]"""
        system = "Primera persona. Sin tipología. Acciones. Español."

    return call_ollama(prompt, system, model)


def generate_all(mbti: str, enneagram: int, wing: int, inst_stack: str,
                 name: str, output_dir: Path, model: str = DEFAULT_MODEL,
                 role: str = "Team Member", lang: str = DEFAULT_LANG) -> Dict[str, str]:
    
    lang_label = "🇬🇧 EN" if lang == 'en' else "🇪🇸 ES"
    print(f"🔥 V8 [{lang_label}] — '{name}' ({mbti} {enneagram}w{wing} {inst_stack})")
    print(f"📁 {output_dir}")
    print("-" * 60)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / 'memory').mkdir(exist_ok=True)
    
    files = {}
    
    print("  📝 SOUL.md...")
    files['SOUL.md'] = generate_soul(mbti, enneagram, wing, inst_stack, name, model, lang)
    
    print("  📝 IDENTITY.md...")
    files['IDENTITY.md'] = generate_identity(mbti, enneagram, wing, inst_stack, name, model, lang)
    
    print("  📝 AGENTS.md...")
    files['AGENTS.md'] = generate_agents(mbti, enneagram, name, model, lang)
    
    # Validate generated content (minimum quality check)
    MIN_CONTENT_LENGTH = 200  # Characters
    for key in ['SOUL.md', 'IDENTITY.md', 'AGENTS.md']:
        content = files.get(key, '')
        if len(content) < MIN_CONTENT_LENGTH:
            print(f"  ⚠️  Warning: {key} seems too short ({len(content)} chars). Model may have failed.")
        if 'error' in content.lower()[:100]:
            print(f"  ⚠️  Warning: {key} may contain an error message.")
    
    # Static files - language aware
    if lang == 'en':
        files['ROLE.md'] = f"# ROLE.md\n\nI am **{name.lower()}**. Role: {role}.\n"
        files['TOOLS.md'] = "# TOOLS.md\n\nMy configurations go here.\n"
        files['USER.md'] = "# USER.md\n\n*(Completed as I interact)*\n"
        files['MEMORY.md'] = f"# MEMORY.md\n\n## {datetime.now().strftime('%Y-%m-%d')}\n\nI was born.\n"
        files['HEARTBEAT.md'] = "# HEARTBEAT.md\n"
        files['BOOTSTRAP.md'] = f"# BOOTSTRAP.md\n\n**{name}**\n\n1. Read SOUL.md\n2. Read ROLE.md\n3. Delete this file\n"
    else:
        files['ROLE.md'] = f"# ROLE.md\n\nSoy **{name.lower()}**. Rol: {role}.\n"
        files['TOOLS.md'] = "# TOOLS.md\n\nMis configuraciones van aquí.\n"
        files['USER.md'] = "# USER.md\n\n*(Completo según interactúo)*\n"
        files['MEMORY.md'] = f"# MEMORY.md\n\n## {datetime.now().strftime('%Y-%m-%d')}\n\nNací.\n"
        files['HEARTBEAT.md'] = "# HEARTBEAT.md\n"
        files['BOOTSTRAP.md'] = f"# BOOTSTRAP.md\n\n**{name}**\n\n1. Lee SOUL.md\n2. Lee ROLE.md\n3. Borra este archivo\n"
    
    for fn, content in files.items():
        with open(output_dir / fn, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ {fn}")
    
    meta = {
        'name': name, 'mbti': mbti, 'enneagram': enneagram, 'wing': wing,
        'instinct_stack': inst_stack, 'role': role, 'language': lang,
        'created': datetime.now().isoformat(), 'generator': 'v8'
    }
    with open(output_dir / 'agent_metadata.json', 'w') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    
    print("-" * 60)
    print(f"✨ V8 '{name}' ready")
    return files


def main():
    parser = argparse.ArgumentParser(
        description='Agent Generator V8 - Create AI agents with real psychology',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Direct typology
  %(prog)s "ENTJ 8w7 sx/so" --name Commander --lang en
  
  # Search Personality Database
  %(prog)s --character "Tony Stark" --lang en
  %(prog)s -c "Walter White"
  %(prog)s -c "Dr. House" --name House
        """
    )
    parser.add_argument('typology', nargs='?', 
                        help="Typology string: 'MBTI Xw# inst/inst'")
    parser.add_argument('--character', '-c', 
                        help='Search PDB for character/celebrity (auto-fills typology)')
    parser.add_argument('--name', '-n', default=None,
                        help='Agent name (defaults to character name if using -c)')
    parser.add_argument('--output', '-o', type=Path)
    parser.add_argument('--model', '-m', default=DEFAULT_MODEL)
    parser.add_argument('--role', '-r', default='Team Member')
    parser.add_argument('--lang', '-l', default=DEFAULT_LANG, choices=['es', 'en'],
                        help='Output language: es (Spanish, default) or en (English)')
    parser.add_argument('--pdb-search', action='store_true',
                        help='Search PDB interactively')
    
    args = parser.parse_args()
    
    # Interactive PDB search mode
    if args.pdb_search:
        try:
            from pdb_search import interactive_search
            interactive_search()
        except ImportError:
            print("❌ pdb_search module not found")
        return
    
    # Character search mode
    if args.character:
        try:
            from pdb_search import search, get_typology
            
            print(f"🔍 Searching PDB for '{args.character}'...")
            results = search(args.character, limit=5)
            
            if not results:
                print(f"❌ No results found for '{args.character}'")
                sys.exit(1)
            
            # Show results and use first one
            best = results[0]
            typology = get_typology(best['name'])
            
            if not typology:
                print(f"❌ Incomplete typology data for '{best['name']}'")
                sys.exit(1)
            
            print(f"✅ Found: {best['name']} → {typology}")
            
            # Use character name as agent name if not specified
            if not args.name:
                # Extract first name or clean up name
                args.name = best['name'].split()[0].strip('"').strip("'")
            
            args.typology = typology
            
        except ImportError:
            print("❌ pdb_search module not found. Run with typology directly.")
            sys.exit(1)
    
    if not args.typology:
        print("Usage:")
        print("  ./agent_generator.py 'MBTI Xw# inst/inst' --name Name")
        print("  ./agent_generator.py --character 'Tony Stark'")
        print("\nExamples:")
        print("  ./agent_generator.py 'ENTJ 8w7 sx/so' --name Commander --lang en")
        print("  ./agent_generator.py -c 'Dr. House' --lang en")
        sys.exit(1)
    
    # Set default name if still not set
    if not args.name:
        args.name = 'Agent'
    
    parts = args.typology.upper().split()
    mbti = parts[0]
    enneagram, wing = 8, 7
    for p in parts:
        if 'W' in p:
            enneagram, wing = int(p.split('W')[0]), int(p.split('W')[1])
            break
    inst_stack = next((p.lower() for p in parts if '/' in p.lower()), 'sx/so')
    
    output_dir = args.output or Path(f'./agents/{args.name.lower().replace(" ", "_")}')
    generate_all(mbti, enneagram, wing, inst_stack, args.name, output_dir, args.model, args.role, args.lang)


if __name__ == '__main__':
    main()
