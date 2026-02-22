# 🎭 Creador de Personajes

Genera agentes IA con personalidad auténtica basada en tipología psicológica (MBTI + Eneagrama + Instintos) e intégralos automáticamente en [OpenClaw](https://github.com/openclaw/openclaw) y OpenGoat.

## ✨ Características

- **Personalidad profunda**: Combina MBTI (16 tipos), Eneagrama (9 tipos + alas), e Instintos (sp/so/sx)
- **Sin meta-etiquetas**: Los agentes MUESTRAN su personalidad en acciones, no la describen
- **Integración automática**: OpenClaw + OpenGoat con jerarquía organizacional
- **Calidad validada**: Evaluación >7.2/10 en pruebas de autenticidad

## 🚀 Uso Rápido

```bash
# Flujo completo: genera + integra en OpenClaw + OpenGoat
python integrate_agent.py "ISFP 6w5 sp/sx" --name "Lorena"

# Solo generar archivos (sin integrar)
python agent_generator.py "ENTJ 8w7 sx/so" --name "Comandante"
```

## 📝 Sintaxis de Tipología

```
"MBTI Xw# inst/inst"

MBTI:      INTJ, INTP, ENTJ, ENTP, INFJ, INFP, ENFJ, ENFP,
           ISTJ, ISFJ, ESTJ, ESFJ, ISTP, ISFP, ESTP, ESFP

Eneagrama: 1w2, 1w9, 2w1, 2w3, 3w2, 3w4, 4w3, 4w5,
           5w4, 5w6, 6w5, 6w7, 7w6, 7w8, 8w7, 8w9, 9w8, 9w1

Instintos: sp/so, sp/sx, so/sp, so/sx, sx/sp, sx/so
           (sp=supervivencia, so=social, sx=sexual/intensidad)
```

### Ejemplos

```bash
python integrate_agent.py "ENTJ 8w7 sx/so" --name "Comandante"  # Líder dominante
python integrate_agent.py "INFP 4w5 sp/sx" --name "Poeta"       # Artista introspectivo
python integrate_agent.py "ESTJ 1w2 so/sp" --name "Director"    # Organizador estricto
python integrate_agent.py "ENFP 7w6 so/sx" --name "Explorador"  # Aventurero social
```

## 🏢 Estructura Organizacional

Los agentes se asignan automáticamente a managers según su MBTI:

```
ANI (CEO)
├── RULOG (COO) ─ Operaciones
│   └── ENTJ, ESTJ, ISTJ, ESTP, ISTP
├── CHUCHE (CTO) ─ Estrategia
│   └── INTJ, INTP, ENTP
└── GONCHO (CCO) ─ Cultura
    └── ENFJ, INFJ, ESFJ, ISFJ, ENFP, INFP, ESFP, ISFP
```

| MBTI | División | Manager Directo |
|------|----------|-----------------|
| INTJ, INTP | CTO | chuche |
| ENTP | CTO | caba |
| ESTJ, ISTJ, ESTP, ISTP | COO | rulog |
| ENTJ | COO | fuego |
| ENFP | CCO | kelly |
| ISFP, ESFP | CCO | rodri |
| Resto | CCO | goncho |

## 📂 Archivos Generados

**OpenClaw** (`~/.openclaw/agents/<nombre>/`):
```
├── SOUL.md        # Personalidad completa
├── IDENTITY.md    # Resumen de identidad
├── AGENTS.md      # Reglas de comportamiento
├── TOOLS.md       # Configuraciones de herramientas
├── USER.md        # Info del usuario (vacío inicial)
├── MEMORY.md      # Memoria persistente
├── HEARTBEAT.md   # Tareas periódicas
├── BOOTSTRAP.md   # Instrucciones de inicio
└── ROLE.md        # Rol en la organización
```

**OpenGoat** (`~/.opengoat/agents/<nombre>/`):
```
└── config.json    # Jerarquía organizacional
```

## 🧠 Teoría

El generador combina tres sistemas de tipología:

### MBTI (Funciones Cognitivas)
- **Dominante + Auxiliar**: Cómo procesa información
- **4 Lados de la Mente**: Ego, Subconsciente, Shadow, Superego
- Basado en la teoría de C.S. Joseph

### Eneagrama
- **Pasión Core**: Motor emocional (ira, orgullo, envidia, etc.)
- **Ala**: Modulador de la pasión
- **Miedo/Deseo**: Motivaciones fundamentales

### Instintos
- **sp (Self-Preservation)**: Supervivencia, recursos, territorio
- **so (Social)**: Grupo, estatus, pertenencia
- **sx (Sexual/Intensidad)**: Fusión, magnetismo, química

## 🔧 Archivos del Proyecto

| Archivo | Descripción |
|---------|-------------|
| `agent_generator.py` | Generador principal de agentes |
| `integrate_agent.py` | Flujo completo con integración |
| `csj_core.py` | Funciones cognitivas MBTI |
| `cuatro_lados.py` | Lógica de los 4 lados de la mente |
| `narrador.py` | Utilidades de narración |

## 📊 Calidad

El generador ha sido iterado y evaluado para producir agentes que:

- ✅ **No usan meta-etiquetas** ("mi ala 5", "mi instinto sp")
- ✅ **Muestran en vez de describir** (acciones > adjetivos)
- ✅ **Tienen consecuencias ejecutadas** ("hice X", no "haría X")
- ✅ **Integran MBTI invisible** (comportamiento, no etiquetas)
- ✅ **Pasan umbral 7.2/10** en evaluación de autenticidad

## 🛠️ Requisitos

- Python 3.8+
- [Ollama](https://ollama.ai/) con modelo `qwen2.5:14b` (o especificar otro con `--model`)
- OpenClaw y OpenGoat instalados (para integración)

## 📜 Licencia

MIT

---

*Inspirado en Disco Elysium y la teoría de C.S. Joseph.*
