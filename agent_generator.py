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

# ==============================================================================
# DATOS COMPLETOS
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

# Funciones cognitivas MBTI - cómo se VEN en comportamiento
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
                  name: str, model: str) -> str:
    
    sides = get_four_sides(mbti)
    enea = ENEAGRAMA.get(enneagram, ENEAGRAMA[8])
    ala = ALAS.get((enneagram, wing), f"Modulado por ala {wing}")
    
    parts = inst_stack.replace('-', '/').split('/')
    inst1, inst2 = (parts[0], parts[1]) if len(parts) > 1 else (parts[0], 'so')
    
    inst1_data = INSTINTOS_COMPORTAMIENTO.get(inst1, INSTINTOS_COMPORTAMIENTO['sx'])
    inst2_data = INSTINTOS_COMPORTAMIENTO.get(inst2, INSTINTOS_COMPORTAMIENTO['so'])
    
    dom, aux = get_dominant_functions(mbti)
    dom_desc = FUNCIONES.get(dom, '')
    aux_desc = FUNCIONES.get(aux, '')

    system = """Eres un escritor de personajes. Español. Primera persona.

## REGLAS CRÍTICAS V8:

1. PROHIBIDO escribir "mi ala", "mi instinto", "mi función dominante", o cualquier etiqueta de tipología.
2. En su lugar, MUESTRA el comportamiento en ESCENAS concretas.
3. NO escribas meta-comentarios ni placeholders.
4. Cada característica = una ACCIÓN o ESCENA, no una descripción.
5. El MBTI se ve en CÓMO actúa, no en etiquetas.

EJEMPLO MALO: "Mi instinto sp me lleva a acumular recursos"
EJEMPLO BUENO: "Siempre tengo una mochila lista junto a la puerta. Agua, dinero, cargador. Por si acaso."

EJEMPLO MALO: "Mi función Fi me hace valorar la autenticidad"  
EJEMPLO BUENO: "Cuando alguien miente, lo noto en el estómago antes de procesarlo. Me callo, pero algo se rompe."
"""

    prompt = f"""Escribe SOUL.md para {name}.

TIPOLOGÍA (NO LA MENCIONES EXPLÍCITAMENTE, SOLO ÚSALA PARA DAR FORMA):
- {mbti}: Dominante {dom} ({dom_desc}), Auxiliar {aux} ({aux_desc})
- {enneagram}w{wing}: Pasión {enea['pasion']}, Miedo: {enea['miedo']}
- Ala: {ala}
- Instinto primario {inst1}: {inst1_data['core']}
  Ejemplos de comportamiento: {', '.join(inst1_data['acciones'][:3])}
- Instinto secundario {inst2}: {inst2_data['core']}
  Ejemplos: {', '.join(inst2_data['acciones'][:2])}

CUERPO: {enea['cuerpo']}
VOZ: {enea['voz']}

4 LADOS: Normal {sides['ego']['type']}, Aspiracional {sides['subconscious']['type']}, Estrés {sides['shadow']['type']}, Juez {sides['superego']['type']}

---

ESTRUCTURA (2000-2500 palabras):

# SOUL.md - {name}

## Quién Soy
[100 palabras. ESCENAS y SENSACIONES. Cómo me muevo, qué noto, qué hago. Sin etiquetas.]

## Mi Voz
[5 frases típicas mías: orden/petición, humor, aprecio, irritación, estrés máximo]

## Lo Que Me Mueve

### El Fuego
[La pasión {enea['pasion']} en mi CUERPO. Qué siento físicamente. Qué me hace HACER.]

### La Sombra del Fuego  
[El ala {wing}: cómo MODIFICA mi pasión en comportamiento concreto. Una escena.]

### Mi Obsesión
[Instinto {inst1} como ACCIONES. No "mi instinto sp me lleva a..." sino escenas de qué HAGO.]

### Mi Territorio
[Instinto {inst2} como ACCIONES concretas. Nombres de personas o lugares si aplica.]

## Una Historia
[80-100 palabras. Un momento ESPECÍFICO que me define. Sensorial: olores, texturas, temperatura.]

## Cuando Caigo

### Mi Miedo
[El miedo {enea['miedo']} como ESCENA. Cuándo lo sentí. Qué evité por él.]

### Perdiendo el Control
[Comportamientos concretos bajo estrés. Pensamientos paranoicos ESPECÍFICOS. NO menciones tipos MBTI.]

### La Voz del Juez
[Frases EXACTAS que me digo. Diálogo interno, no descripción.]

## Mi Gente

### Los Míos
[Nombres o roles. Qué HAGO por ellos. Una escena de lealtad.]

### Cuando Me Fallan
[Una historia de consecuencia EJECUTADA. "Hice X", no "haría X".]

## Mis Líneas
[6 boundaries con CONSECUENCIA EJECUTADA cada uno]
- [Límite]: [Lo que HICE cuando alguien lo cruzó]

## Cuándo Llamarme
**Sí:** [4 situaciones]
**No:** [2 anti-patrones]

---
Genera TODO el contenido directamente. Sin placeholders. Sin mencionar tipología explícitamente."""

    return call_ollama(prompt, system, model)


def generate_identity(mbti: str, enneagram: int, wing: int, inst_stack: str,
                      name: str, model: str) -> str:
    enea = ENEAGRAMA.get(enneagram, ENEAGRAMA[8])
    
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

    return call_ollama(prompt, "Conciso. Sin tipología explícita. Español.", model)


def generate_agents(mbti: str, enneagram: int, name: str, model: str) -> str:
    enea = ENEAGRAMA.get(enneagram, ENEAGRAMA[8])
    
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

    return call_ollama(prompt, "Primera persona. Sin tipología. Acciones.", model)


def generate_all(mbti: str, enneagram: int, wing: int, inst_stack: str,
                 name: str, output_dir: Path, model: str = DEFAULT_MODEL,
                 role: str = "Team Member") -> Dict[str, str]:
    
    print(f"🔥 V8 — '{name}' ({mbti} {enneagram}w{wing} {inst_stack})")
    print(f"📁 {output_dir}")
    print("-" * 60)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / 'memory').mkdir(exist_ok=True)
    
    files = {}
    
    print("  📝 SOUL.md...")
    files['SOUL.md'] = generate_soul(mbti, enneagram, wing, inst_stack, name, model)
    
    print("  📝 IDENTITY.md...")
    files['IDENTITY.md'] = generate_identity(mbti, enneagram, wing, inst_stack, name, model)
    
    print("  📝 AGENTS.md...")
    files['AGENTS.md'] = generate_agents(mbti, enneagram, name, model)
    
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
        'instinct_stack': inst_stack, 'role': role,
        'created': datetime.now().isoformat(), 'generator': 'v8'
    }
    with open(output_dir / 'agent_metadata.json', 'w') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    
    print("-" * 60)
    print(f"✨ V8 '{name}' listo")
    return files


def main():
    parser = argparse.ArgumentParser(description='Agent Generator V8')
    parser.add_argument('typology', nargs='?')
    parser.add_argument('--name', '-n', default='Agente')
    parser.add_argument('--output', '-o', type=Path)
    parser.add_argument('--model', '-m', default=DEFAULT_MODEL)
    parser.add_argument('--role', '-r', default='Team Member')
    
    args = parser.parse_args()
    if not args.typology:
        print("Uso: ./agent_generator_v8.py 'MBTI Xw# inst/inst' --name Nombre")
        sys.exit(1)
    
    parts = args.typology.upper().split()
    mbti = parts[0]
    enneagram, wing = 8, 7
    for p in parts:
        if 'W' in p:
            enneagram, wing = int(p.split('W')[0]), int(p.split('W')[1])
            break
    inst_stack = next((p.lower() for p in parts if '/' in p.lower()), 'sx/so')
    
    output_dir = args.output or Path(f'./agents/{args.name.lower().replace(" ", "_")}')
    generate_all(mbti, enneagram, wing, inst_stack, args.name, output_dir, args.model, args.role)


if __name__ == '__main__':
    main()
