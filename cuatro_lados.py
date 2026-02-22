#!/usr/bin/env python3
"""
Four Sides of Mind Generator
Based on C.S. Joseph's theory + Enneagram

Generates 7 variants:
1. EGO (base)
2. SUBCONSCIOUS healthy (integration)
3. SUBCONSCIOUS unhealthy (disintegration)
4. UNCONSCIOUS healthy (integration)
5. UNCONSCIOUS unhealthy (disintegration)
6. SUPEREGO healthy (integration)
7. SUPEREGO unhealthy (disintegration)
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Import base narrator functions
from narrador import parse_typology, build_prompt, call_ollama, DEFAULT_MODEL

# Enneagram integration/disintegration map
INTEGRACION = {
    '1': '7', '2': '4', '3': '6', '4': '1', '5': '8',
    '6': '9', '7': '5', '8': '2', '9': '3'
}

DESINTEGRACION = {
    '1': '4', '2': '8', '3': '9', '4': '2', '5': '7',
    '6': '3', '7': '1', '8': '5', '9': '6'
}

# Alas naturales para cada tipo (cuando cambia el tipo base)
ALAS_DEFAULT = {
    '1': '9', '2': '1', '3': '2', '4': '3', '5': '4',
    '6': '5', '7': '6', '8': '7', '9': '8'
}


def flip_letter(letter: str, position: int) -> str:
    """Cambia una letra MBTI por su opuesta"""
    flips = {
        0: {'E': 'I', 'I': 'E'},  # Extraversion/Introversion
        1: {'N': 'S', 'S': 'N'},  # Intuition/Sensing
        2: {'T': 'F', 'F': 'T'},  # Pensamiento/Sentimiento
        3: {'J': 'P', 'P': 'J'},  # Judging/Perceiving
    }
    return flips[position].get(letter, letter)


def calculate_sides(mbti: str) -> dict:
    """
    Calcula los 4 lados de la mente según C.S. Joseph
    
    EGO: tipo base
    SUBCONSCIENTE: todas las letras cambiadas (E↔I, N↔S, T↔F, J↔P)
    INCONSCIENTE: primera y última cambiadas (E↔I, J↔P)
    SUPEREGO: medio cambiado (N↔S, T↔F)
    """
    if not mbti or len(mbti) != 4:
        return None
    
    mbti = mbti.upper()
    
    # EGO = base
    ego = mbti
    
    # SUBCONSCIENTE = todo cambiado
    subconsciente = ''.join([
        flip_letter(mbti[0], 0),
        flip_letter(mbti[1], 1),
        flip_letter(mbti[2], 2),
        flip_letter(mbti[3], 3)
    ])
    
    # SUBCONSCIOUS = first and last changed, middle same
    inconsciente = ''.join([
        flip_letter(mbti[0], 0),
        mbti[1],
        mbti[2],
        flip_letter(mbti[3], 3)
    ])
    
    # SUPEREGO = middle changed, first and last same
    superego = ''.join([
        mbti[0],
        flip_letter(mbti[1], 1),
        flip_letter(mbti[2], 2),
        mbti[3]
    ])
    
    return {
        'ego': ego,
        'subconsciente': subconsciente,
        'inconsciente': inconsciente,
        'superego': superego
    }


def calculate_enneagram_variant(base_type: str, variant: str) -> tuple:
    """
    Calcula el tipo de eneagrama para integración o desintegración
    Retorna (nuevo_tipo, nueva_ala)
    """
    if variant == 'integracion':
        new_type = INTEGRACION.get(base_type, base_type)
    elif variant == 'desintegracion':
        new_type = DESINTEGRACION.get(base_type, base_type)
    else:
        return (base_type, None)
    
    # Ala por defecto para el nuevo tipo
    new_wing = ALAS_DEFAULT.get(new_type, str((int(new_type) % 9) + 1))
    
    return (new_type, new_wing)


def generate_all_variants(typology: dict) -> list:
    """
    Genera las 7 variantes del perfil:
    1. EGO (base)
    2-3. SUBCONSCIENTE sano/insano
    4-5. INCONSCIENTE sano/insano
    6-7. SUPEREGO sano/insano
    """
    if not typology.get('mbti'):
        raise ValueError("Se requiere MBTI para calcular los 4 lados")
    
    sides = calculate_sides(typology['mbti'])
    base_ennea = typology.get('enneagram', '5')  # Default tipo 5 si no hay
    
    variants = []
    
    # 1. EGO (base)
    variants.append({
        'nombre': 'EGO',
        'lado': 'ego',
        'estado': 'base',
        'mbti': sides['ego'],
        'enneagram': base_ennea,
        'wing': typology.get('wing'),
        'instincts': typology.get('instincts'),
        'gender': typology.get('gender'),
        'descripcion': f"El tipo base, la personalidad consciente y desarrollada."
    })
    
    # For each side (except ego), healthy and unhealthy version
    for lado in ['subconsciente', 'inconsciente', 'superego']:
        lado_mbti = sides[lado]
        
        # HEALTHY version (integration)
        int_type, int_wing = calculate_enneagram_variant(base_ennea, 'integracion')
        variants.append({
            'nombre': f'{lado.upper()}_SANO',
            'lado': lado,
            'estado': 'sano',
            'mbti': lado_mbti,
            'enneagram': int_type,
            'wing': int_wing,
            'instincts': typology.get('instincts'),
            'gender': typology.get('gender'),
            'descripcion': f"El {lado} en estado de integración/crecimiento."
        })
        
        # UNHEALTHY version (disintegration)
        des_type, des_wing = calculate_enneagram_variant(base_ennea, 'desintegracion')
        variants.append({
            'nombre': f'{lado.upper()}_INSANO',
            'lado': lado,
            'estado': 'insano',
            'mbti': lado_mbti,
            'enneagram': des_type,
            'wing': des_wing,
            'instincts': typology.get('instincts'),
            'gender': typology.get('gender'),
            'descripcion': f"El {lado} en estado de desintegración/estrés."
        })
    
    return variants


# Cognitive functions by MBTI type
FUNCIONES_COGNITIVAS = {
    'ENTJ': {'dom': 'Te', 'aux': 'Ni', 'ter': 'Se', 'inf': 'Fi'},
    'INTJ': {'dom': 'Ni', 'aux': 'Te', 'ter': 'Fi', 'inf': 'Se'},
    'ENTP': {'dom': 'Ne', 'aux': 'Ti', 'ter': 'Fe', 'inf': 'Si'},
    'INTP': {'dom': 'Ti', 'aux': 'Ne', 'ter': 'Si', 'inf': 'Fe'},
    'ENFJ': {'dom': 'Fe', 'aux': 'Ni', 'ter': 'Se', 'inf': 'Ti'},
    'INFJ': {'dom': 'Ni', 'aux': 'Fe', 'ter': 'Ti', 'inf': 'Se'},
    'ENFP': {'dom': 'Ne', 'aux': 'Fi', 'ter': 'Te', 'inf': 'Si'},
    'INFP': {'dom': 'Fi', 'aux': 'Ne', 'ter': 'Si', 'inf': 'Te'},
    'ESTJ': {'dom': 'Te', 'aux': 'Si', 'ter': 'Ne', 'inf': 'Fi'},
    'ISTJ': {'dom': 'Si', 'aux': 'Te', 'ter': 'Fi', 'inf': 'Ne'},
    'ESFJ': {'dom': 'Fe', 'aux': 'Si', 'ter': 'Ne', 'inf': 'Ti'},
    'ISFJ': {'dom': 'Si', 'aux': 'Fe', 'ter': 'Ti', 'inf': 'Ne'},
    'ESTP': {'dom': 'Se', 'aux': 'Ti', 'ter': 'Fe', 'inf': 'Ni'},
    'ISTP': {'dom': 'Ti', 'aux': 'Se', 'ter': 'Ni', 'inf': 'Fe'},
    'ESFP': {'dom': 'Se', 'aux': 'Fi', 'ter': 'Te', 'inf': 'Ni'},
    'ISFP': {'dom': 'Fi', 'aux': 'Se', 'ter': 'Ni', 'inf': 'Te'},
}

# Disintegration guides by type - how each type behaves at their worst state
DESINTEGRACION_GUIAS = {
    'ISFP': {
        'patron': 'Fi-Se loop autodestructivo',
        'comportamiento': '''El ISFP desintegrado es REACTIVO, IMPULSIVO y AUTODESTRUCTIVO - NO calculador ni maquiavélico.
- Explosiones emocionales repentinas (Fi corrupto)
- Búsqueda de gratificación sensorial destructiva: adicciones, autolesión, conductas de riesgo (Se descontrolado)
- Aislamiento obstinado en valores rígidos que ya no sirven
- Incapacidad de articular el dolor, actuándolo físicamente
- ARQUETIPO: Van Gogh cortándose la oreja, no Hannibal Lecter
- NO manipula estratégicamente (eso es Ni-Te de INTJ). El ISFP actúa impulsivamente sin plan.''',
    },
    'ESFJ': {
        'patron': 'Fe-Si corrupto, control tiránico',
        'comportamiento': '''El ESFJ desintegrado es TIRÁNICO, CONTROLADOR y OBSESIVO con formas sociales - NO existencialista ni filosófico.
- Manipulación emocional abierta: culpa, victimismo, chantaje afectivo (Fe corrupto)
- Obsesión enfermiza con "cómo deben ser las cosas" (Si rígido)
- Control totalitario del entorno familiar/social
- Juzga constantemente a otros por no cumplir sus estándares
- ARQUETIPO: La madre de Carrie, no un filósofo atormentado
- NO tiene "dudas existenciales" profundas (eso es Ni). El ESFJ insano IMPONE su visión, no la cuestiona.''',
    },
    'INTP': {
        'patron': 'Ti-Si loop paranoico',
        'comportamiento': '''El INTP desintegrado se retrae en análisis obsesivo y paranoia.
- Rumia interminable sobre problemas sin actuar (Ti loop)
- Paranoia y desconfianza extrema
- Cinismo corrosivo que destruye relaciones
- Se aferra a viejos sistemas de pensamiento (Si)
- ARQUETIPO: El científico loco aislado, Dr. House en su peor momento''',
    },
    'ENTJ': {
        'patron': 'Te-Se corrupto, tiranía',
        'comportamiento': '''El ENTJ desintegrado se vuelve un tirano despiadado.
- Control obsesivo sobre todo y todos (Te corrupto)
        - Explotación de otros como recursos
- Búsqueda de placer como escape (Se inferior)
- Incapacidad de vulnerabilidad, armadura impenetrable
- ARQUETIPO: El CEO psicópata, el dictador corporativo''',
    },
    'INFP': {
        'patron': 'Fi-Si loop melancólico',
        'comportamiento': '''El INFP desintegrado se hunde en melancolía y victimismo.
- Rumiación nostálgica sobre heridas pasadas (Si grip)
- Victimismo y pasividad extrema
- Idealización rígida que rechaza toda realidad
- Aislamiento total del mundo
- ARQUETIPO: El poeta que se deja morir, pasividad autodestructiva''',
    },
    'ENFJ': {
        'patron': 'Fe-Se corrupto, mesianismo',
        'comportamiento': '''El ENFJ desintegrado se vuelve un manipulador mesiánico.
- Manipulación emocional para "el bien de todos" (Fe corrupto)
- Comportamiento dramático y escenas (Se)
- Necesidad enfermiza de ser necesitado
- Sacrificio compulsivo que genera deuda emocional
- ARQUETIPO: El líder de culto carismático, el mártir manipulador''',
    },
    'INTJ': {
        'patron': 'Ni-Fi loop paranoico',
        'comportamiento': '''El INTJ desintegrado cae en paranoia y aislamiento.
- Visiones paranoicas de conspiración contra ellos (Ni corrupto)
- Sentido mesiánico de ser el único que "ve la verdad"
- Aislamiento total, desconexión de la realidad
- Frialdad emocional completa
- ARQUETIPO: El genio incomprendido que odia a la humanidad''',
    },
    'ENTP': {
        'patron': 'Ne-Fe loop manipulador',
        'comportamiento': '''El ENTP desintegrado manipula con ingenio para evitar compromiso.
- Argumentación sofística sin fin para evitar responsabilidad
- Manipulación carismática que encanta mientras destruye
- Incapacidad de profundidad, todo es juego
- Sadismo intelectual
- ARQUETIPO: El estafador carismático, el abogado del diablo''',
    },
    'ESTJ': {
        'patron': 'Te-Ne corrupto',
        'comportamiento': '''El ESTJ desintegrado se vuelve un autoritario inflexible.
- Imposición brutal de reglas sin sentido
- "Las cosas se hacen como yo digo" sin espacio para matices
- Explosiones de ira cuando las cosas no siguen el plan
- Paranoia sobre pérdida de control
- ARQUETIPO: El jefe tiránico, el padre autoritario''',
    },
    'ISTJ': {
        'patron': 'Si-Fi loop rígido',
        'comportamiento': '''El ISTJ desintegrado se aferra obstinadamente al pasado.
- Rigidez total: "siempre se ha hecho así"
- Resentimiento callado que explota eventualmente
- Pesimismo extremo sobre el futuro
- Incapacidad de adaptarse a cualquier cambio
- ARQUETIPO: El funcionario que prefiere que todo se derrumbe antes que cambiar''',
    },
    'ISFJ': {
        'patron': 'Si-Ti corrupto',
        'comportamiento': '''El ISFJ desintegrado se convierte en mártir resentido.
- Sacrificio compulsivo que genera deuda emocional
- Resentimiento pasivo-agresivo
- "Yo lo hago todo y nadie aprecia"
- Catastrofismo y preocupación obsesiva
- ARQUETIPO: El mártir que recuerda cada sacrificio no reconocido''',
    },
    'ESTP': {
        'patron': 'Se-Fe loop impulsivo',
        'comportamiento': '''El ESTP desintegrado busca estimulación sin límites.
- Impulsividad extrema, conductas de alto riesgo
- Manipulación social para obtener lo que quiere YA
- Incapacidad total de considerar consecuencias
- Hedonismo destructivo
- ARQUETIPO: El adicto a la adrenalina que arrastra a otros consigo''',
    },
    'ISTP': {
        'patron': 'Ti-Ni loop frío',
        'comportamiento': '''El ISTP desintegrado se desconecta completamente.
- Frialdad emocional total, desapego de consecuencias humanas
- Puede volverse peligrosamente eficiente sin empatía
- Paranoia silenciosa
- Aislamiento que puede derivar en actos impulsivos violentos
- ARQUETIPO: El francotirador frío, competencia sin compasión''',
    },
    'ESFP': {
        'patron': 'Se-Te loop',
        'comportamiento': '''El ESFP desintegrado busca atención a cualquier costo.
- Drama constante para ser el centro de atención
- Impulsividad que destruye relaciones
- Hedonismo que ignora todas las responsabilidades
- Ira explosiva cuando no recibe la atención deseada
- ARQUETIPO: La estrella en caída libre, autodestrucción pública''',
    },
    'ENFP': {
        'patron': 'Ne-Te loop',
        'comportamiento': '''El ENFP desintegrado se dispersa en mil proyectos para evitar el vacío.
- Hiperactividad que esconde depresión profunda
- Incapacidad de compromiso con nada ni nadie
- Manipulación carismática para evitar consecuencias
- Abandono de proyectos y personas cuando se ponen "difíciles"
- ARQUETIPO: El eterno Peter Pan que deja devastación a su paso''',
    },
    'INFJ': {
        'patron': 'Ni-Ti loop apocalíptico',
        'comportamiento': '''El INFJ desintegrado cae en visiones apocalípticas.
- Profecías de doom y desastre constantes (Ni corrupto)
- "Door slam" - corte total y repentino de relaciones
- Sentido mesiánico de misión imposible
- Puede justificar acciones cuestionables "por el bien mayor"
- ARQUETIPO: El profeta del apocalipsis, el manipulador "por tu bien"''',
    },
}


def build_variant_prompt(variant: dict) -> str:
    """Construye el prompt específico para una variante"""
    
    mbti = variant['mbti']
    funciones = FUNCIONES_COGNITIVAS.get(mbti, {})
    
    # Additional context depending on the side
    contextos = {
        'ego': "Este es el EGO, la personalidad consciente y principal. El tipo que la persona muestra al mundo y con el que se identifica.",
        'subconsciente': "Este es el SUBCONSCIENTE, el lado aspiracional. Representa quién quiere llegar a ser la persona, sus metas idealizadas.",
        'inconsciente': "Este es el INCONSCIENTE, la sombra. Representa los patrones automáticos, lo que la persona hace sin darse cuenta, especialmente bajo estrés.",
        'superego': "Este es el SUPEREGO, el crítico interno. Representa las expectativas que la persona siente que otros tienen de ella."
    }
    
    estados = {
        'base': "",
        'sano': "En estado SANO/INTEGRADO: la persona accede a las mejores cualidades de este lado, mostrando crecimiento y madurez.",
        'insano': "En estado INSANO/DESINTEGRADO: la persona cae en los peores patrones de este lado, mostrando estrés y comportamientos destructivos."
    }
    
    # Construir perfil
    parts = []
    if variant['mbti']:
        parts.append(f"MBTI: {variant['mbti']}")
    if variant['enneagram']:
        ennea_str = variant['enneagram']
        if variant['wing']:
            ennea_str += f"w{variant['wing']}"
        parts.append(f"Eneagrama: {ennea_str}")
    if variant['instincts']:
        parts.append(f"Instintos: {variant['instincts']}")
    if variant['gender']:
        parts.append(f"Género: {variant['gender']}")
    
    profile = " | ".join(parts)
    contexto = contextos.get(variant['lado'], "")
    estado = estados.get(variant['estado'], "")
    
    # Cognitive functions info
    funciones_info = ""
    if funciones:
        funciones_info = f"""
FUNCIONES COGNITIVAS de {mbti}:
- Dominante: {funciones['dom']} (función principal)
- Auxiliar: {funciones['aux']} (soporte)
- Terciaria: {funciones['ter']} (en desarrollo)
- Inferior: {funciones['inf']} (punto ciego/grip)
"""
    
    # Type-specific disintegration guide
    guia_desintegracion = ""
    if variant['estado'] == 'insano' and mbti in DESINTEGRACION_GUIAS:
        guia = DESINTEGRACION_GUIAS[mbti]
        guia_desintegracion = f"""
⚠️ GUÍA CRÍTICA PARA {mbti} DESINTEGRADO:
Patrón: {guia['patron']}

{guia['comportamiento']}

DEBES seguir estas pautas exactamente. NO inventes comportamientos que contradigan la estructura cognitiva del tipo.
"""
    
    return f"""Genera la descripción del narrador arquetípico para este perfil:

{profile}
{funciones_info}
CONTEXTO: {contexto}
{estado}
{guia_desintegracion}
IMPORTANTE: Esta descripción es para el {variant['nombre']}. Captura tanto las fortalezas como las sombras de este lado de la mente. {"Enfatiza los aspectos positivos y de crecimiento." if variant['estado'] == 'sano' else "Enfatiza los aspectos oscuros y destructivos, siguiendo EXACTAMENTE la guía de desintegración proporcionada." if variant['estado'] == 'insano' else ""}

Genera un párrafo denso (150-250 palabras) que empiece con "Debe ser un narrador como..." """


def generate_and_save(input_str: str, output_dir: str = None, model: str = DEFAULT_MODEL, verbose: bool = True):
    """
    Genera las 7 variantes y las guarda en una carpeta
    """
    # Parsear input
    typology = parse_typology(input_str)
    
    if not typology.get('mbti'):
        print("Error: Se requiere al menos el MBTI")
        return None
    
    # Generar variantes
    variants = generate_all_variants(typology)
    
    # Crear nombre de carpeta base
    base_name = f"{typology['mbti']}"
    if typology.get('enneagram'):
        base_name += f"_{typology['enneagram']}"
        if typology.get('wing'):
            base_name += f"w{typology['wing']}"
    if typology.get('instincts'):
        base_name += f"_{typology['instincts'].replace('/', '-')}"
    if typology.get('gender'):
        base_name += f"_{typology['gender']}"
    
    # Directorio de output
    if output_dir:
        out_path = Path(output_dir) / base_name
    else:
        out_path = Path("output") / base_name
    
    out_path.mkdir(parents=True, exist_ok=True)
    
    if verbose:
        print(f"=" * 60)
        print(f"🎭 Generating 4 Sides of Mind for: {input_str}")
        print(f"=" * 60)
        print(f"📁 Output: {out_path}")
        print()
    
    results = []
    
    for i, variant in enumerate(variants, 1):
        if verbose:
            print(f"[{i}/7] Generating {variant['nombre']}...")
        
        # Construir prompt y generar
        prompt = build_variant_prompt(variant)
        response = call_ollama(prompt, model)
        
        # Save result
        variant['output'] = response
        results.append(variant)
        
        # Save individual file
        filename = f"{i:02d}_{variant['nombre']}.md"
        filepath = out_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {variant['nombre']}\n\n")
            f.write(f"**Lado:** {variant['lado'].title()}\n")
            f.write(f"**Estado:** {variant['estado'].title()}\n")
            f.write(f"**MBTI:** {variant['mbti']}\n")
            if variant['enneagram']:
                ennea = variant['enneagram']
                if variant['wing']:
                    ennea += f"w{variant['wing']}"
                f.write(f"**Enneagram:** {ennea}\n")
            if variant['instincts']:
                f.write(f"**Instincts:** {variant['instincts']}\n")
            if variant['gender']:
                f.write(f"**Gender:** {variant['gender']}\n")
            f.write(f"\n---\n\n")
            f.write(f"## Description\n\n{response}\n")
        
        if verbose:
            print(f"    ✓ Saved: {filename}")
    
    # Save index/summary
    index_path = out_path / "00_INDEX.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(f"# 4 Sides of Mind: {input_str}\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"## Structure\n\n")
        
        sides = calculate_sides(typology['mbti'])
        f.write(f"| Side | MBTI | Description |\n")
        f.write(f"|------|------|-------------|\n")
        f.write(f"| EGO | {sides['ego']} | Conscious personality |\n")
        f.write(f"| SUBCONSCIOUS | {sides['subconsciente']} | Aspirational side |\n")
        f.write(f"| UNCONSCIOUS | {sides['inconsciente']} | The shadow |\n")
        f.write(f"| SUPEREGO | {sides['superego']} | The inner critic |\n")
        f.write(f"\n## Enneagram\n\n")
        f.write(f"- **Base:** {typology.get('enneagram', '?')}w{typology.get('wing', '?')}\n")
        f.write(f"- **Integration (healthy):** {INTEGRACION.get(typology.get('enneagram', '5'), '?')}\n")
        f.write(f"- **Disintegration (unhealthy):** {DESINTEGRACION.get(typology.get('enneagram', '5'), '?')}\n")
        f.write(f"\n## Files\n\n")
        for i, v in enumerate(results, 1):
            f.write(f"{i}. [{v['nombre']}]({i:02d}_{v['nombre']}.md)\n")
    
    # Save JSON with everything
    json_path = out_path / "data.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'input': input_str,
            'typology': typology,
            'sides': sides,
            'variants': results,
            'generated': datetime.now().isoformat()
        }, f, indent=2, ensure_ascii=False)
    
    if verbose:
        print()
        print(f"✅ Complete! 7 variants generated in: {out_path}")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Generate the 4 Sides of Mind with healthy/unhealthy variants",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  ./cuatro_lados.py "ENTJ 8w7 sx/so male"
  ./cuatro_lados.py "INFP 4w5 sp/sx female" -o ~/characters
  ./cuatro_lados.py "ENTP 7w8 sx/so" --model qwen2.5:14b
        """
    )
    
    parser.add_argument('profile', help='Base typological profile (MBTI Enneagram Instincts...)')
    parser.add_argument('-o', '--output', help='Directorio de output (default: ./output)')
    parser.add_argument('-m', '--model', default=DEFAULT_MODEL, help=f'Modelo de Ollama')
    parser.add_argument('-q', '--quiet', action='store_true', help='Modo silencioso')
    parser.add_argument('--dry-run', action='store_true', help='Solo mostrar variantes, no generar')
    
    args = parser.parse_args()
    
    if args.dry_run:
        typology = parse_typology(args.perfil)
        variants = generate_all_variants(typology)
        print(json.dumps(variants, indent=2, ensure_ascii=False))
        return
    
    generate_and_save(
        args.perfil,
        output_dir=args.output,
        model=args.model,
        verbose=not args.quiet
    )


if __name__ == "__main__":
    main()
