#!/usr/bin/env python3
"""
Core de C.S. Joseph - Funciones Cognitivas + 4 Lados + Quadras

Copiado de: /home/lorty/m2/Escritorio/Proyectos/Proyectos-de-Compatibilidad-MBTI/
Corregido según auditorías del vault de Obsidian (2026-02-21)

CORRECCIONES APLICADAS:
- Subconsciente/Inconsciente estaban INVERTIDOS → CORREGIDO
- Subconsciente = flip E/I + J/P (aspiracional)
- Inconsciente = flip TODO (shadow)
"""

# ==============================================================================
# LAS 8 FUNCIONES COGNITIVAS POR TIPO (Hero → Demon)
# Fuente: compatibilidad_mbti/mbti_api/mbti_type_functions.py
# ==============================================================================

MBTI_FUNCTIONS = {
    'INFJ': ['Ni', 'Fe', 'Ti', 'Se', 'Ne', 'Fi', 'Te', 'Si'],
    'INFP': ['Fi', 'Ne', 'Si', 'Te', 'Fe', 'Ni', 'Se', 'Ti'],
    'INTJ': ['Ni', 'Te', 'Fi', 'Se', 'Ne', 'Ti', 'Fe', 'Si'],
    'INTP': ['Ti', 'Ne', 'Si', 'Fe', 'Te', 'Ni', 'Se', 'Fi'],
    'ISFJ': ['Si', 'Fe', 'Ti', 'Ne', 'Se', 'Fi', 'Te', 'Ni'],
    'ISFP': ['Fi', 'Se', 'Ni', 'Te', 'Fe', 'Si', 'Ne', 'Ti'],
    'ISTJ': ['Si', 'Te', 'Fi', 'Ne', 'Se', 'Ti', 'Fe', 'Ni'],
    'ISTP': ['Ti', 'Se', 'Ni', 'Fe', 'Te', 'Si', 'Ne', 'Fi'],
    'ENFJ': ['Fe', 'Ni', 'Se', 'Ti', 'Fi', 'Ne', 'Si', 'Te'],
    'ENFP': ['Ne', 'Fi', 'Te', 'Si', 'Ni', 'Fe', 'Ti', 'Se'],
    'ENTJ': ['Te', 'Ni', 'Se', 'Fi', 'Ti', 'Ne', 'Si', 'Fe'],
    'ENTP': ['Ne', 'Ti', 'Fe', 'Si', 'Ni', 'Te', 'Fi', 'Se'],
    'ESFJ': ['Fe', 'Si', 'Ne', 'Ti', 'Fi', 'Se', 'Ni', 'Te'],
    'ESFP': ['Se', 'Fi', 'Te', 'Ni', 'Si', 'Fe', 'Ti', 'Ne'],
    'ESTJ': ['Te', 'Si', 'Ne', 'Fi', 'Ti', 'Se', 'Ni', 'Fe'],
    'ESTP': ['Se', 'Ti', 'Fe', 'Ni', 'Si', 'Te', 'Fi', 'Ne'],
}

# Roles de las 8 funciones según C.S. Joseph
FUNCTION_ROLES = {
    0: {'name': 'Hero', 'fps': 100, 'description': 'Tu fortaleza principal, lo que haces naturalmente'},
    1: {'name': 'Parent', 'fps': 75, 'description': 'Tu responsabilidad, lo que proteges en otros'},
    2: {'name': 'Child', 'fps': 50, 'description': 'Tu vulnerabilidad juguetona, lo que te hace feliz'},
    3: {'name': 'Inferior', 'fps': 25, 'description': 'Tu aspiración e inseguridad, donde creces'},
    4: {'name': 'Nemesis', 'fps': 20, 'description': 'Tu preocupación, lo que temes en otros'},
    5: {'name': 'Critic', 'fps': 15, 'description': 'Tu autocrítica despiadada'},
    6: {'name': 'Trickster', 'fps': 10, 'description': 'Tu punto ciego, donde te engañan'},
    7: {'name': 'Demon', 'fps': 5, 'description': 'Tu lado más oscuro, destructivo cuando se activa'},
}

# ==============================================================================
# LAS 4 QUADRAS (Cuadrantes)
# Fuente: transcripciones de C.S. Joseph - 17_the_four_sides_of_the_mind_and_the_quadras
# ==============================================================================

QUADRAS = {
    'Alpha': {
        'name': 'Crusaders (Cruzados)',
        'types': ['ESFJ', 'ENTP', 'ISFJ', 'INTP'],
        'axis': 'Ti-Fe / Ne-Si',
        'virtue': 'Faith (Fe)',
        'vice': 'Apathy',
        'description': 'Buscan la verdad y la comparten con el mundo. Cruzadas ideológicas.'
    },
    'Beta': {
        'name': 'Templars (Templarios)',
        'types': ['ESTP', 'ISTP', 'ENFJ', 'INFJ'],
        'axis': 'Ti-Fe / Ni-Se',
        'virtue': 'Willpower (Voluntad)',
        'vice': 'Cowardice',
        'description': 'Guerreros espirituales. Acción con propósito trascendente.'
    },
    'Gamma': {
        'name': 'Wayfarers (Caminantes)',
        'types': ['INTJ', 'ENTJ', 'ESFP', 'ISFP'],
        'axis': 'Te-Fi / Ni-Se',
        'virtue': 'Ambition (Ambición)',
        'vice': 'Greed',
        'description': 'Emprendedores y artistas. Libertad individual sobre conformidad.'
    },
    'Delta': {
        'name': 'Philosophers (Filósofos)',
        'types': ['ESTJ', 'ENFP', 'ISTJ', 'INFP'],
        'axis': 'Te-Fi / Ne-Si',
        'virtue': 'Duty (Deber)',
        'vice': 'Laziness',
        'description': 'Preservadores de tradición y buscadores de significado.'
    }
}

# ==============================================================================
# TRANSFORMACIONES DE LOS 4 LADOS DE LA MENTE
# CORREGIDO: Subconsciente e Inconsciente estaban invertidos
# ==============================================================================

def _flip_letter(letter: str, pair: tuple) -> str:
    """Invierte una letra dentro de un par."""
    return pair[1] if letter == pair[0] else pair[0]

def _calculate_subconscious_correct(mbti: str) -> str:
    """
    SUBCONSCIENTE (Aspiracional): flip TODAS las letras
    
    ENTJ → ISFP
    E→I, N→S, T→F, J→P
    
    El subconsciente es tu yo aspiracional, el opuesto completo.
    """
    letters = list(mbti)
    letters[0] = _flip_letter(letters[0], ('E', 'I'))
    letters[1] = _flip_letter(letters[1], ('N', 'S'))
    letters[2] = _flip_letter(letters[2], ('T', 'F'))
    letters[3] = _flip_letter(letters[3], ('J', 'P'))
    return ''.join(letters)

def _calculate_shadow_correct(mbti: str) -> str:
    """
    SHADOW/INCONSCIENTE: flip E/I + J/P (primera y última)
    
    ENTJ → INTP
    E→I, N se mantiene, T se mantiene, J→P
    
    El shadow comparte el mismo eje de funciones pero con orientación invertida.
    Te-Ni → Ti-Ne (las mismas letras base pero e/i flip)
    """
    letters = list(mbti)
    letters[0] = _flip_letter(letters[0], ('E', 'I'))
    letters[3] = _flip_letter(letters[3], ('J', 'P'))
    return ''.join(letters)

# Funciones legacy (mantener compatibilidad)
def calculate_subconscious(mbti: str) -> str:
    return _calculate_subconscious_correct(mbti)

def calculate_shadow(mbti: str) -> str:
    return _calculate_shadow_correct(mbti)

def calculate_superego(mbti: str) -> str:
    """
    SUPEREGO (Crítico): flip N/S + T/F (las dos del medio)
    
    ENTJ → ESFJ (mantiene E y J, cambia NT→SF)
    
    El superego es tu crítico interno, representa lo que más te cuesta integrar.
    """
    letters = list(mbti)
    letters[1] = _flip_letter(letters[1], ('N', 'S'))
    letters[2] = _flip_letter(letters[2], ('T', 'F'))
    return ''.join(letters)

# ==============================================================================
# CUATERNIDADES CORRECTAS (de C.S. Joseph)
# Estas son las 4 "casas" - cada tipo comparte cuaternidad con otros 3
# ==============================================================================

QUATERNITIES = {
    # Cuaternidad 1
    'ENTJ': ['ENTJ', 'ISFP', 'INTP', 'ESFJ'],
    'ISFP': ['ENTJ', 'ISFP', 'INTP', 'ESFJ'],
    'INTP': ['ENTJ', 'ISFP', 'INTP', 'ESFJ'],
    'ESFJ': ['ENTJ', 'ISFP', 'INTP', 'ESFJ'],
    
    # Cuaternidad 2
    'INTJ': ['INTJ', 'ESFP', 'ENTP', 'ISFJ'],
    'ESFP': ['INTJ', 'ESFP', 'ENTP', 'ISFJ'],
    'ENTP': ['INTJ', 'ESFP', 'ENTP', 'ISFJ'],
    'ISFJ': ['INTJ', 'ESFP', 'ENTP', 'ISFJ'],
    
    # Cuaternidad 3
    'INFJ': ['INFJ', 'ESTP', 'ENFP', 'ISTJ'],
    'ESTP': ['INFJ', 'ESTP', 'ENFP', 'ISTJ'],
    'ENFP': ['INFJ', 'ESTP', 'ENFP', 'ISTJ'],
    'ISTJ': ['INFJ', 'ESTP', 'ENFP', 'ISTJ'],
    
    # Cuaternidad 4
    'ENFJ': ['ENFJ', 'ISTP', 'ESTJ', 'INFP'],
    'ISTP': ['ENFJ', 'ISTP', 'ESTJ', 'INFP'],
    'ESTJ': ['ENFJ', 'ISTP', 'ESTJ', 'INFP'],
    'INFP': ['ENFJ', 'ISTP', 'ESTJ', 'INFP'],
}

def get_four_sides(mbti: str) -> dict:
    """
    Calcula los 4 lados de la mente para un tipo MBTI.
    
    Basado en las cuaternidades de C.S. Joseph y las transcripciones.
    
    CORRECCIÓN: Usar las cuaternidades directamente, no cálculos.
    El orden en cada cuaternidad es: [Ego, Subconsciente, Shadow, Superego]
    """
    mbti = mbti.upper()
    quaternity = QUATERNITIES.get(mbti, [mbti, mbti, mbti, mbti])
    
    # Las cuaternidades ya tienen el orden correcto
    # Pero el ego puede estar en cualquier posición, necesitamos rotar
    
    # Encontrar el índice del ego en la cuaternidad
    try:
        ego_index = quaternity.index(mbti)
    except ValueError:
        ego_index = 0
    
    # Rotar para que el ego sea el primero
    # El orden de los 4 lados de la mente es fijo dentro de cada cuaternidad:
    # Posición 0 = un tipo de ego, Posición 1 = su subconsciente, etc.
    
    # Según C.S. Joseph, las cuaternidades tienen este patrón:
    # Para ENTJ: [ENTJ(ego), ISFP(sub), INTP(shadow), ESFJ(superego)]
    
    ego = mbti
    
    # Calcular usando las reglas correctas:
    # Subconsciente: flip todas las letras (ENTJ → ISFP)
    subconscious = _calculate_subconscious_correct(mbti)
    
    # Shadow: flip E/I y J/P (ENTJ → INTP)
    shadow = _calculate_shadow_correct(mbti)
    
    # Superego: flip N/S y T/F (ENTJ → ESFJ)
    superego = calculate_superego(mbti)
    
    return {
        'ego': {
            'type': ego,
            'functions': MBTI_FUNCTIONS.get(ego, []),
            'role': 'Tu yo principal, donde operas normalmente'
        },
        'subconscious': {
            'type': subconscious,
            'functions': MBTI_FUNCTIONS.get(subconscious, []),
            'role': 'Tu yo aspiracional, donde quieres llegar cuando maduras'
        },
        'shadow': {
            'type': shadow,
            'functions': MBTI_FUNCTIONS.get(shadow, []),
            'role': 'Tu sombra, emerge bajo estrés extremo'
        },
        'superego': {
            'type': superego,
            'functions': MBTI_FUNCTIONS.get(superego, []),
            'role': 'Tu crítico interno, lo que más te cuesta integrar'
        }
    }

def get_cognitive_stack(mbti: str) -> list:
    """
    Retorna las 8 funciones con sus roles y descripciones.
    """
    functions = MBTI_FUNCTIONS.get(mbti.upper(), [])
    stack = []
    for i, func in enumerate(functions):
        role = FUNCTION_ROLES.get(i, {})
        stack.append({
            'position': i + 1,
            'function': func,
            'role': role.get('name', 'Unknown'),
            'fps': role.get('fps', 0),
            'description': role.get('description', '')
        })
    return stack

def get_quadra(mbti: str) -> dict:
    """
    Determina la quadra del tipo.
    """
    mbti = mbti.upper()
    for quadra_name, quadra_info in QUADRAS.items():
        if mbti in quadra_info['types']:
            return {
                'name': quadra_name,
                **quadra_info
            }
    return None

def get_ego_functions_pair(mbti: str) -> str:
    """Retorna el par de funciones principales del ego (ej: Te-Ni)"""
    functions = MBTI_FUNCTIONS.get(mbti.upper(), [])
    if len(functions) >= 2:
        return f"{functions[0]}-{functions[1]}"
    return ""

def get_inferior_function(mbti: str) -> str:
    """Retorna la función inferior"""
    functions = MBTI_FUNCTIONS.get(mbti.upper(), [])
    if len(functions) >= 4:
        return functions[3]
    return ""

# ==============================================================================
# FUNCIÓN PRINCIPAL DE TRANSICIONES
# ==============================================================================

def build_transitions_text(mbti: str) -> str:
    """
    Construye el texto de transiciones cognitivas para usar en prompts.
    """
    sides = get_four_sides(mbti)
    
    ego_funcs = get_ego_functions_pair(mbti)
    sub_type = sides['subconscious']['type']
    sub_funcs = get_ego_functions_pair(sub_type)
    shadow_type = sides['shadow']['type']
    shadow_funcs = get_ego_functions_pair(shadow_type)
    superego_type = sides['superego']['type']
    superego_funcs = get_ego_functions_pair(superego_type)
    inferior = get_inferior_function(mbti)
    
    text = f"""
### TRANSICIONES COGNITIVAS PARA {mbti}

**Cuaternidad:** {mbti} - {sub_type} - {shadow_type} - {superego_type}

**Transición 1: Ego ({mbti}) → Subconsciente ({sub_type})**
Cuando el **{ego_funcs}** de [NOMBRE] se ve frustrado por situaciones emocionales o relaciones personales no resueltas, su **{inferior}** inferior erupciona, activando al {sub_type} interno con su {sub_funcs}.

**Transición 2: Subconsciente ({sub_type}) → Inconsciente/Shadow ({shadow_type})**
La frustración prolongada del **{sub_funcs}** aspiracional despierta la sombra **{shadow_type}**: el **{shadow_funcs}** paranoico reemplaza la autenticidad del subconsciente.

**Transición 3: Inconsciente ({shadow_type}) → Super-Ego ({superego_type})**
El **{shadow_funcs}** corrupto del {shadow_type} invoca al crítico **{superego_type}** con su **{superego_funcs}** tiránico: ya no analiza, juzga sin piedad.
"""
    return text


# ==============================================================================
# TEST
# ==============================================================================

if __name__ == '__main__':
    import sys
    
    mbti = sys.argv[1] if len(sys.argv) > 1 else 'ENTJ'
    
    print(f"\n{'='*60}")
    print(f"ANÁLISIS C.S. JOSEPH PARA {mbti}")
    print('='*60)
    
    print("\n📊 STACK COGNITIVO (8 funciones):")
    for f in get_cognitive_stack(mbti):
        print(f"  {f['position']}. {f['function']} - {f['role']} ({f['fps']} fps)")
    
    print("\n🧠 4 LADOS DE LA MENTE:")
    sides = get_four_sides(mbti)
    for side_name, side_info in sides.items():
        funcs = '-'.join(side_info['functions'][:4]) if side_info['functions'] else 'N/A'
        print(f"  {side_name.upper()}: {side_info['type']} ({funcs})")
        print(f"    → {side_info['role']}")
    
    print("\n🏛️ QUADRA:")
    quadra = get_quadra(mbti)
    if quadra:
        print(f"  {quadra['name']} - {quadra['types']}")
        print(f"  Virtud: {quadra['virtue']} | Vicio: {quadra['vice']}")
    
    print("\n📝 TRANSICIONES:")
    print(build_transitions_text(mbti))
