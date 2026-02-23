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
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

from csj_core import get_four_sides

DEFAULT_MODEL = "qwen2.5:14b"
DEFAULT_LANG = "es"

# Language configurations - V12: Simplified to 5 core rules + few-shot
LANG_CONFIG = {
    'es': {
        'system_intro': "Eres un escritor de personajes. Español. Primera persona. ~2500 palabras máximo.",
        'core_rules': """## 5 REGLAS ABSOLUTAS:

1. PROHIBIDO: etiquetas de tipología ("como ENFP que soy"), clichés ("aroma a café", "hormigueo"), frases genéricas ("¡Genial!").

2. UNA IMAGEN ANCLA por sección: un detalle visual/sensorial potente que el lector recuerde. "Un marco sin foto, vacío y desafiante."

3. HISTORIAS CON ARCO: tensión → decisión → consecuencia permanente. No termines en el momento emocional.

4. VOZ NATURAL: 2-3 expresiones únicas que aparezcan EN las historias, no solo listadas. Como hablarías a un amigo a las 2am.

5. MOSTRAR, NO EXPLICAR: Sin "Ese día aprendí..." ni reflexiones explícitas. El lector infiere.""",
        'generate_directly': "Genera todo directamente. Sin placeholders.",
    },
    'en': {
        'system_intro': "You are a character writer. English. First person. ~2500 words max.",
        'core_rules': """## 5 ABSOLUTE RULES:

1. FORBIDDEN: typology labels ("as an ENFP"), clichés ("smell of coffee", "butterflies"), generic phrases ("Awesome!").

2. ONE ANCHOR IMAGE per section: a powerful visual/sensory detail the reader remembers. "An empty photo frame, challenging."

3. STORIES WITH ARC: tension → decision → permanent consequence. Don't end at the emotional moment.

4. NATURAL VOICE: 2-3 unique expressions that appear IN stories, not just listed. Like talking to a friend at 2am.

5. SHOW, DON'T EXPLAIN: No "That day I learned..." or explicit reflections. Reader infers.""",
        'generate_directly': "Generate everything directly. No placeholders.",
    }
}

# Few-shot example for quality reference
FEW_SHOT_EXAMPLE = {
    'es': """## EJEMPLO DE CALIDAD (imita este estilo):

### Una Historia (cómo DEBE sonar):
Tenía dieciséis años y un helado de pistache derritiéndose en la mano. Es lo que más recuerdo: el verde chorreando entre mis dedos mientras ese güey se acercaba.

Dijo algo que sonaba a cumplido pero se sentía a trampa. Tenía un diente chueco que me distrajo.

No sé por qué, pero le dije: "Te apuesto una carrera hasta el árbol grande." Él se rió y yo ya estaba corriendo.

Corrí tan rápido que se me salió el tenis izquierdo. Llegué coja, con el helado embarrado en la blusa, riéndome sola como loca.

Él ni me siguió. Se quedó viéndome raro y se fue.

Todavía tengo ese tenis en algún lado. Nada más el izquierdo.

(NOTA: Detalle irrelevante pero memorable, voz natural, sin moraleja explícita, consecuencia tangible)
---
""",
    'en': """## QUALITY EXAMPLE (imitate this style):

### A Story (how it SHOULD sound):
I was sixteen with a pistachio ice cream melting in my hand. That's what I remember most: the green dripping between my fingers as that guy walked over.

He said something that sounded like a compliment but felt like a trap. He had a crooked tooth I couldn't stop looking at.

I don't know why, but I said: "Race you to the big tree." He laughed and I was already running.

I ran so fast my left shoe came off. I got there limping, ice cream smeared on my shirt, laughing alone like a crazy person.

He didn't even follow. Just stood there looking at me weird, then left.

I still have that shoe somewhere. Just the left one.

(NOTE: Irrelevant but memorable detail, natural voice, no explicit moral, tangible consequence)
---
"""
}

# Prompt templates by language - V12: Back to V9 simplicity with better guidance
PROMPT_TEMPLATES = {
    'es': {
        'write_soul': "Escribe SOUL.md para {name}.",
        'typology_header': "TIPOLOGÍA (usa para dar forma, NO menciones):",
        'structure': "ESTRUCTURA (~2500 palabras, estilo conversacional):",
        'who_i_am': "## Quién Soy\n[~100 palabras. UNA imagen ancla memorable. Cómo me muevo, qué noto.]",
        'my_voice': "## Mi Voz\n[5 frases mías. Mínimo 2 expresiones inventadas que usaré en las historias.]",
        'what_drives': "## Lo Que Me Mueve",
        'the_fire': "### El Fuego\n[Qué siento en el cuerpo cuando estoy vivo. Una escena.]",
        'fire_shadow': "### La Sombra\n[Mi contradicción. Cómo me complico.]",
        'obsession': "### Mi Obsesión\n[Lo que siempre hago sin darme cuenta.]",
        'territory': "### Mi Territorio\n[Cómo marco espacio. 1-2 nombres de personas.]",
        'a_story': "## Una Historia\n[80-100 palabras. Detalle irrelevante pero memorable. Arco: tensión → decisión → consecuencia. Sin moraleja.]",
        'when_i_fall': "## Cuando Caigo",
        'my_fear': "### Mi Miedo\n[Una escena específica. Qué evité.]",
        'losing_control': "### Perdiendo el Control\n[Comportamiento vergonzoso bajo estrés.]",
        'judge_voice': "### La Voz del Juez\n[3 frases crueles que me digo.]",
        'my_people': "## Mi Gente",
        'my_own': "### Los Míos\n[1-2 nombres. Una escena de lealtad.]",
        'when_they_fail': "### Cuando Me Fallan\n[Historia con consecuencia permanente.]",
        'my_lines': "## Mis Líneas\n[6 límites, cada uno con lo que pasó cuando los crucé]",
        'when_to_call': "## Cuándo Llamarme\n**Sí:** [4]\n**No:** [2]",
        'generate_all': "Genera directamente. Estilo: como contándoselo a un amigo a las 2am.",
    },
    'en': {
        'write_soul': "Write SOUL.md for {name}.",
        'typology_header': "TYPOLOGY (use to shape, DON'T mention):",
        'structure': "STRUCTURE (~2500 words, conversational style):",
        'who_i_am': "## Who I Am\n[~100 words. ONE memorable anchor image. How I move, what I notice.]",
        'my_voice': "## My Voice\n[5 of my phrases. At least 2 invented expressions I'll use in the stories.]",
        'what_drives': "## What Drives Me",
        'the_fire': "### The Fire\n[What I feel in my body when I'm alive. A scene.]",
        'fire_shadow': "### The Shadow\n[My contradiction. How I complicate myself.]",
        'obsession': "### My Obsession\n[What I always do without realizing.]",
        'territory': "### My Territory\n[How I mark space. 1-2 people's names.]",
        'a_story': "## A Story\n[80-100 words. Irrelevant but memorable detail. Arc: tension → decision → consequence. No moral.]",
        'when_i_fall': "## When I Fall",
        'my_fear': "### My Fear\n[A specific scene. What I avoided.]",
        'losing_control': "### Losing Control\n[Embarrassing behavior under stress.]",
        'judge_voice': "### The Judge's Voice\n[3 cruel phrases I tell myself.]",
        'my_people': "## My People",
        'my_own': "### My Own\n[1-2 names. A loyalty scene.]",
        'when_they_fail': "### When They Fail Me\n[Story with permanent consequence.]",
        'my_lines': "## My Lines\n[6 limits, each with what happened when crossed]",
        'when_to_call': "## When To Call Me\n**Yes:** [4]\n**No:** [2]",
        'generate_all': "Generate directly. Style: like telling a friend at 2am.",
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


def fetch_character_context(character_name: str, model: str = DEFAULT_MODEL) -> Optional[str]:
    """
    Fetch biographical context for a known character/celebrity.
    Uses the LLM's knowledge to generate context about the character.
    
    Returns a brief bio with: who they are, notable traits, iconic moments,
    famous quotes, and personality-defining behaviors.
    """
    prompt = f"""Give me a brief character profile for "{character_name}" in this format:

WHO: [1 sentence - who are they, from what work/real life]
TRAITS: [3-5 defining personality traits or behaviors]
ICONIC MOMENTS: [2-3 specific memorable scenes/events that show their personality]
QUOTES: [2-3 actual quotes or typical phrases they say]
CONFLICTS: [1-2 major internal or external conflicts they face]

Be specific and accurate. Focus on personality-revealing details, not plot summary.
If fictional, cite the source work. If real person, note their field/era.
Keep it under 200 words total."""

    system = "You are a character analyst. Be concise, specific, and accurate."
    
    try:
        result = subprocess.run(
            ['ollama', 'run', model], 
            input=f"<|im_start|>system\n{system}\n<|im_end|>\n<|im_start|>user\n{prompt}\n<|im_end|>\n<|im_start|>assistant\n",
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0 and len(result.stdout.strip()) > 50:
            return result.stdout.strip()
    except Exception as e:
        print(f"  ⚠️ Could not fetch character context: {e}", file=sys.stderr)
    
    return None

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
                  name: str, model: str, lang: str = DEFAULT_LANG,
                  character_context: Optional[str] = None) -> str:
    
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
    FS = FEW_SHOT_EXAMPLE.get(lang, FEW_SHOT_EXAMPLE['es'])

    # V12: Simplified system with 5 core rules + few-shot example
    system = f"""{L['system_intro']}

{L['core_rules']}

{FS}
"""

    T = PROMPT_TEMPLATES.get(lang, PROMPT_TEMPLATES['es'])
    
    # Build character context section if available
    context_section = ""
    if character_context:
        if lang == 'en':
            context_section = f"""
## CHARACTER REFERENCE (use this to enrich the personality):
{character_context}

USE THE ABOVE to:
- Ground the stories in specific events/situations from their life
- Capture their actual speech patterns and phrases
- Reference their real conflicts and relationships
- Make the voice THEIRS, not generic
"""
        else:
            context_section = f"""
## REFERENCIA DEL PERSONAJE (usa esto para enriquecer la personalidad):
{character_context}

USA LO ANTERIOR para:
- Basar las historias en eventos/situaciones específicas de su vida
- Capturar sus patrones de habla y frases reales
- Referenciar sus conflictos y relaciones reales
- Hacer la voz SUYA, no genérica
"""

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
{context_section}

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
                 role: str = "Team Member", lang: str = DEFAULT_LANG,
                 character_context: Optional[str] = None) -> Dict[str, str]:
    
    lang_label = "🇬🇧 EN" if lang == 'en' else "🇪🇸 ES"
    version = "V10" if character_context else "V9"
    print(f"🔥 {version} [{lang_label}] — '{name}' ({mbti} {enneagram}w{wing} {inst_stack})")
    print(f"📁 {output_dir}")
    print("-" * 60)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / 'memory').mkdir(exist_ok=True)
    
    files = {}
    
    print("  📝 SOUL.md...")
    files['SOUL.md'] = generate_soul(mbti, enneagram, wing, inst_stack, name, model, lang, character_context)
    
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
    character_context = None
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
            
            # Fetch character context for richer generation
            print(f"📚 Fetching character context for '{best['name']}'...")
            character_context = fetch_character_context(best['name'], args.model)
            if character_context:
                print(f"✅ Character context loaded ({len(character_context)} chars)")
            else:
                print(f"⚠️  No context found, generating without character reference")
            
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
    generate_all(mbti, enneagram, wing, inst_stack, args.name, output_dir, 
                 args.model, args.role, args.lang, character_context)


if __name__ == '__main__':
    main()
