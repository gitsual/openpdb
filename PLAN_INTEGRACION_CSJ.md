# Plan de Integración: C.S. Joseph + Naranjo → Creador de Personajes 10/10

> **Fecha:** 2026-02-21
> **Objetivo:** Integrar el modelo completo de C.S. Joseph y Claudio Naranjo para que el creador de personajes sea un 10/10

---

## 📦 Fuentes de Datos Disponibles

### 1. Código Existente (Listo para usar)
```
/home/lorty/m2/Escritorio/Proyectos/Proyectos-de-Compatibilidad-MBTI/
├── compatibilidad_mbti/
│   ├── mbti_api/mbti_type_functions.py  # Las 8 funciones por tipo
│   └── c/mbti_api/include/
│       ├── cognitive_functions.h         # Hero → Demon
│       ├── four_sides_of_the_mind.h      # Ego, Shadow, Subconscious, Superego
│       └── type_compability.h            # Compatibilidad 16×16
```

### 2. Transcripciones C.S. Joseph (80+ videos)
```
/home/lorty/m2/Documentos/whisper/
├── 17_the_four_sides_of_the_mind_and_the_quadras/  # Quadras + 4 Lados
├── 16_attitudes_of_cognitive_functions/             # 8 actitudes
├── 22_cognitive_transitions/                        # Transiciones por tipo
├── 12_social_compatibility/                         # Compatibilidad social
└── socionics/                                       # Relaciones intertipo
```

### 3. Proyecto Eneagrama (Completo)
```
/home/lorty/m2/programas/carta-no-astral/
└── src/data/tritipos.json  # 27 tritipos de Katherine Fauvre
```

---

## 🔧 Correcciones Pendientes (de la auditoría)

### Prioridad ALTA
- [ ] **Invertir Subconsciente/Inconsciente en cuatro_lados.py**
  - Actual: Subconsciente = flip TODO → INCORRECTO
  - Correcto: Subconsciente = flip E/I + J/P (aspiracional)
  - Correcto: Inconsciente = flip TODO (shadow)

### Prioridad MEDIA
- [ ] **Añadir las 8 funciones completas** (incluir Shadow)
  - Hero, Parent, Child, Inferior (Ego)
  - Nemesis, Critic, Trickster, Demon (Shadow)
  
- [ ] **Añadir roles psicológicos** de cada función

- [ ] **Añadir INSTINCTS_DATA** con subtipos del Eneagrama
  - 27 combinaciones (9 eneatipos × 3 instintos)
  - Contratipos marcados (E6 sx, E2 so, E4 so, E1 so)

---

## 🏗️ Estructura Propuesta

### csj_core.py (NUEVO)
```python
"""
Core de C.S. Joseph - Funciones Cognitivas + 4 Lados + Quadras
"""

# Las 8 funciones por tipo (copiado del proyecto existente)
MBTI_FUNCTIONS = {
    'ENTJ': ['Te', 'Ni', 'Se', 'Fi', 'Ti', 'Ne', 'Si', 'Fe'],
    'INTP': ['Ti', 'Ne', 'Si', 'Fe', 'Te', 'Ni', 'Se', 'Fi'],
    # ... los 16 tipos
}

# Roles de las funciones
FUNCTION_ROLES = {
    0: 'Hero',      # 100 fps - Fortaleza principal
    1: 'Parent',    # 75 fps - Responsabilidad
    2: 'Child',     # 50 fps - Juego/vulnerabilidad
    3: 'Inferior',  # 25 fps - Aspiración/inseguridad
    4: 'Nemesis',   # 20 fps - Preocupación
    5: 'Critic',    # 15 fps - Autocrítica
    6: 'Trickster', # 10 fps - Punto ciego
    7: 'Demon',     # 5 fps - Lado oscuro
}

# Las 4 Quadras
QUADRAS = {
    'Alpha': {
        'name': 'Crusaders',
        'types': ['ESFJ', 'ENTP', 'ISFJ', 'INTP'],
        'axis': 'Ti-Fe / Ne-Si'
    },
    'Beta': {
        'name': 'Templars',
        'types': ['ESTP', 'ISTP', 'ENFJ', 'INFJ'],
        'axis': 'Ti-Fe / Ni-Se'
    },
    'Gamma': {
        'name': 'Wayfarers',
        'types': ['INTJ', 'ENTJ', 'ESFP', 'ISFP'],
        'axis': 'Te-Fi / Ni-Se'
    },
    'Delta': {
        'name': 'Philosophers',
        'types': ['ESTJ', 'ENFP', 'ISTJ', 'INFP'],
        'axis': 'Te-Fi / Ne-Si'
    }
}

def get_four_sides(mbti: str) -> dict:
    """Calcula los 4 lados de la mente."""
    # Ego = tipo base
    # Subconsciente = flip E/I + J/P (aspiracional)
    # Inconsciente/Shadow = flip TODO
    # Superego = flip N/S + T/F
    ...

def get_cognitive_stack(mbti: str) -> list:
    """Retorna las 8 funciones con sus roles."""
    ...

def get_quadra(mbti: str) -> str:
    """Determina la quadra del tipo."""
    ...
```

### naranjo_core.py (NUEVO)
```python
"""
Core de Claudio Naranjo - Eneagrama completo
"""

# 9 eneatipos con pasión, fijación, virtud
ENEATIPOS = {
    1: {'pasion': 'Ira', 'fijacion': 'Resentimiento', 'virtud': 'Serenidad'},
    2: {'pasion': 'Orgullo', 'fijacion': 'Halagos', 'virtud': 'Humildad'},
    # ... los 9
}

# Direcciones de integración/desintegración
INTEGRACION = {1: 7, 2: 4, 3: 6, 4: 1, 5: 8, 6: 9, 7: 5, 8: 2, 9: 3}
DESINTEGRACION = {1: 4, 2: 8, 3: 9, 4: 2, 5: 7, 6: 3, 7: 1, 8: 5, 9: 6}

# 27 subtipos (9 × 3 instintos)
SUBTIPOS = {
    '6_sx': {
        'nombre': 'E6 Sexual (Contrafóbico)',
        'contratipo': True,
        'pasion_especifica': 'Fuerza',
        'caracteristicas': [...]
    },
    # ... los 27
}

# Tritipos (importar de carta-no-astral)
```

---

## 📋 Tareas de Implementación

### Fase 1: Core (Hoy)
- [ ] Crear `csj_core.py` con funciones cognitivas + 4 lados + quadras
- [ ] Crear `naranjo_core.py` con eneagrama completo
- [ ] Corregir `cuatro_lados.py` (invertir subconsciente/inconsciente)
- [ ] Tests unitarios para validar

### Fase 2: Integración (Mañana)
- [ ] Integrar cores en `narrador.py`
- [ ] Integrar cores en `crear_personaje.py`
- [ ] Añadir transiciones cognitivas automáticas
- [ ] Añadir compatibilidad entre tipos

### Fase 3: Validación
- [ ] Comparar outputs con transcripciones de C.S. Joseph
- [ ] Validar contra vault de Obsidian
- [ ] Ejecutar suite de 85 tests
- [ ] Evaluación con agentes críticos (Caba, José, Sanz)

---

## 📊 Métricas de Éxito

| Métrica | Actual | Objetivo |
|---------|--------|----------|
| Funciones cognitivas | 4 (solo ego) | 8 (ego + shadow) |
| Lados de la mente | 4 (mal calculados) | 4 (correctos) |
| Quadras | 0 | 4 |
| Subtipos eneagrama | 3 genéricos | 27 específicos |
| Contratipos | 0 | 4+ |
| Score evaluación | 5.5/10 | 9+/10 |

---

## 🔗 Referencias

- Proyecto existente: `/home/lorty/m2/Escritorio/Proyectos/Proyectos-de-Compatibilidad-MBTI/`
- Transcripciones CSJ: `/home/lorty/m2/Documentos/whisper/`
- Tritipos: `/home/lorty/m2/programas/carta-no-astral/src/data/tritipos.json`
- TODO Vault: `CONOCIMIENTO/Psicología/MBTI y Funciones Cognitivas/TODO - CS Joseph Pendiente.md`
