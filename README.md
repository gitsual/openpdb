# 🎭 Character Creator

> Generate AI agents with authentic personalities based on psychological typology systems (MBTI × Enneagram × Instinctual Variants)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Character Creator generates AI agent configuration files with deep, psychologically-grounded personalities. Unlike surface-level persona prompts, this system combines three validated typology frameworks to create agents that **behave** authentically rather than just **describe** themselves.

### Key Features

- **Triple-layer personality**: MBTI cognitive functions + Enneagram motivations + Instinctual drives
- **Show, don't tell**: Generated agents demonstrate personality through actions, not meta-labels
- **Automatic integration**: Deploy directly to [OpenClaw](https://github.com/openclaw/openclaw) and OpenGoat
- **Organizational hierarchy**: Auto-assign managers based on psychological fit
- **Quality validated**: Iteratively tested to score >7.2/10 on authenticity metrics

## Quick Start

```bash
# Full pipeline: generate + integrate into OpenClaw + OpenGoat
python integrate_agent.py "ISFP 6w5 sp/sx" --name "Lorena"

# Generate files only (no integration)
python agent_generator.py "ENTJ 8w7 sx/so" --name "Commander"
```

## Typology Syntax

```
"MBTI Xw# inst/inst"
 │     │    │
 │     │    └── Instinctual stack (e.g., sp/sx, so/sp, sx/so)
 │     └─────── Enneagram type + wing (e.g., 8w7, 4w5, 6w5)
 └───────────── MBTI type (e.g., ENTJ, ISFP, INTP)
```

### Examples

| Command | Personality Profile |
|---------|---------------------|
| `"ENTJ 8w7 sx/so"` | Dominant leader, intensity-seeking, tribal protector |
| `"INFP 4w5 sp/sx"` | Introspective artist, self-preserving, deep connections |
| `"ESTJ 1w2 so/sp"` | Structured organizer, principled helper, status-aware |
| `"ENTP 7w8 sx/so"` | Provocative innovator, pleasure-seeking, magnetically social |

## Architecture

### Typology Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                      CHARACTER CREATOR                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │    MBTI     │  │  ENNEAGRAM  │  │  INSTINCTS  │             │
│  │             │  │             │  │             │             │
│  │ • 4 Sides   │  │ • Core Fear │  │ • sp: Body  │             │
│  │ • 8 Funcs   │  │ • Passion   │  │ • so: Group │             │
│  │ • Ego/Shadow│  │ • Wing mod  │  │ • sx: Bond  │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          ▼                                      │
│                   ┌─────────────┐                               │
│                   │  GENERATOR  │                               │
│                   │             │                               │
│                   │ • Ollama    │                               │
│                   │ • Qwen 14B  │                               │
│                   └──────┬──────┘                               │
│                          │                                      │
│         ┌────────────────┼────────────────┐                     │
│         ▼                ▼                ▼                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  SOUL.md    │  │ IDENTITY.md │  │  AGENTS.md  │             │
│  │             │  │             │  │             │             │
│  │ Full psyche │  │ Quick ref   │  │ Behavior    │             │
│  │ 2000+ words │  │ 100 words   │  │ rules       │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### The Four Sides of the Mind (C.S. Joseph)

Each MBTI type has four "sides" representing different states:

```
                    ENTJ Example
    ┌────────────────────────────────────────┐
    │                                        │
    │   EGO (ENTJ)         SHADOW (INTP)    │
    │   Te-Ni-Se-Fi        Ti-Ne-Si-Fe      │
    │   "Commander"        "Paranoid"        │
    │   Normal state       Under stress      │
    │                                        │
    │   SUBCONSCIOUS       SUPEREGO          │
    │   (ISFP)             (ESFJ)            │
    │   Fi-Se-Ni-Te        Fe-Si-Ne-Ti      │
    │   "Artist"           "Inner Critic"    │
    │   Aspirational       Self-judgment     │
    │                                        │
    └────────────────────────────────────────┘
```

### Enneagram Integration

The generator maps each type's core passion to **physical sensations** and **behavioral patterns**:

| Type | Passion | Physical Manifestation |
|------|---------|----------------------|
| 1 | Anger | Clenched jaw, shoulder tension, sighs of exasperation |
| 2 | Pride | Leans in, touches arm, studies your reaction |
| 3 | Vanity | Perfect posture, checks watch, always "on" |
| 4 | Envy | Distant gaze, deep sighs, dramatic gestures |
| 5 | Avarice | Steps back, crosses arms, wide personal space |
| 6 | Fear | Scans environment, vigilant tension, defensive posture |
| 7 | Gluttony | Restless, eyes the door, easy smile, can't sit still |
| 8 | Lust | Occupies space, unblinking gaze, leans into conflict |
| 9 | Sloth | Relaxed, slow movements, avoids direct eye contact |

### Instinctual Variants

```
┌─────────────────────────────────────────────────────────────┐
│                   INSTINCTUAL STACK                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SP (Self-Preservation)                                     │
│  ├── Focus: Body, resources, territory, survival            │
│  ├── Behavior: Checks locks, carries emergency kit          │
│  └── Speech: "Do we have enough?" "Is it safe?"            │
│                                                             │
│  SO (Social)                                                │
│  ├── Focus: Group, status, belonging, influence            │
│  ├── Behavior: Reads hierarchies, builds alliances          │
│  └── Speech: "Who knows whom?" "What's the consensus?"     │
│                                                             │
│  SX (Sexual/Intensity)                                      │
│  ├── Focus: Fusion, magnetism, chemistry, THE connection   │
│  ├── Behavior: Intense eye contact, rapid intimacy          │
│  └── Speech: "You're mine." "I need MORE."                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Output Example

### Generated SOUL.md (ISFP 6w5 sp/sx)

```markdown
# SOUL.md - Lorena

## Who I Am

I walk the mountain path with a full backpack—water, supplies, charger. 
Just in case. My eyes scan the environment for signs of danger before 
I notice the rough texture of tree bark against my palm. When I feel 
safe, I stop for coffee prepared with precision, savoring the spiced 
aroma in the fresh morning air while listening to birds and leaves 
rustling in the wind. My posture stays tense, vigilant. Always alert.

## My Voice

- "Do you see that man? He looks suspicious."
- "I can't believe you did that to my face... This doesn't sit right with me."
- "Thank you for listening. You're valuable to me."
- "This is ridiculous! How could you even think that?"
- "I just need to make sure everything is under control."

## What Drives Me

### The Fire
When fear grips my body, my hands tremble and breathing accelerates. 
My heart pounds while cold sweat runs down my back. When I'm about 
to lose something important, my muscles tense, preparing for fight 
or flight.

### My Obsession  
I check the locks before bed. Every night. I keep a bag ready by 
the door—water, money, charger. I don't let anyone enter my space 
without invitation. I'm always alert to the slightest environmental 
change.

## When Someone Fails Me

My former coworker left an important task unfinished. Furious at his 
lack of responsibility, I told him directly to his face what I thought, 
then implemented a protocol to ensure it never happened again.

## My Lines

- **Don't touch my personal belongings without permission**: When someone 
  violated this, I installed additional locks and restricted access to 
  my private spaces.
- **Don't enter without notice**: When someone tried to access my property 
  without permission, I called the police and reinforced security measures.
```

## Organizational Integration

When integrating agents, they're automatically assigned to managers based on MBTI:

```
                         ┌─────────┐
                         │   ANI   │
                         │  (CEO)  │
                         └────┬────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────┴────┐           ┌────┴────┐           ┌────┴────┐
   │  RULOG  │           │ CHUCHE  │           │ GONCHO  │
   │  (COO)  │           │  (CTO)  │           │  (CCO)  │
   │ Ops     │           │ Strategy│           │ Culture │
   └────┬────┘           └────┬────┘           └────┬────┘
        │                     │                     │
   ┌────┴────┐           ┌────┴────┐           ┌────┴────┐
   │ ENTJ    │           │ INTJ    │           │ ENFJ    │
   │ ESTJ    │           │ INTP    │           │ INFJ    │
   │ ISTJ    │           │ ENTP    │           │ xSFx    │
   │ xSTP    │           │         │           │ xNFP    │
   └─────────┘           └─────────┘           └─────────┘
```

### Assignment Logic

| MBTI Pattern | Division | Direct Manager |
|--------------|----------|----------------|
| INTJ, INTP | CTO | chuche |
| ENTP | CTO | caba |
| ESTJ, ISTJ, ESTP, ISTP | COO | rulog |
| ENTJ | COO | fuego |
| ENFP | CCO | kelly |
| ISFP, ESFP | CCO | rodri |
| Other xNFx, xSFx | CCO | goncho |

## Generated Files

### OpenClaw (`~/.openclaw/agents/<name>/`)

| File | Purpose | Size |
|------|---------|------|
| `SOUL.md` | Complete personality profile | ~2500 words |
| `IDENTITY.md` | Quick reference card | ~100 words |
| `AGENTS.md` | Behavioral rules | ~300 words |
| `TOOLS.md` | Tool configurations | Variable |
| `USER.md` | User context (initially empty) | Variable |
| `MEMORY.md` | Persistent memory | Variable |
| `HEARTBEAT.md` | Periodic task definitions | Variable |
| `BOOTSTRAP.md` | First-run instructions | ~50 words |
| `ROLE.md` | Organizational role | ~30 words |

### OpenGoat (`~/.opengoat/agents/<name>/`)

```json
{
  "id": "lorena",
  "displayName": "Lorena",
  "organization": {
    "type": "individual",
    "reportsTo": "rodri",
    "discoverable": true,
    "tags": ["cco", "isfp"],
    "priority": 50
  }
}
```

## Quality Metrics

The generator was iteratively refined through evaluation cycles:

| Version | Score | Key Issues |
|---------|-------|------------|
| V1-V3 | 4.0-5.5 | Meta-labels, generic descriptions |
| V4 | 7.3 | Better voice, missing body sensations |
| V5 | 7.6 | Wing present, weak consequences |
| V6 | 6.8 | Regression: placeholders, meta-comments |
| V7 | 8.1 | Clean output, executed consequences |
| **V8** | **7.9** | Generalized for all typologies |

### Quality Criteria

- ✅ **No meta-labels**: Never says "my wing 5" or "my sp instinct"
- ✅ **Show don't tell**: Actions and scenes, not adjectives
- ✅ **Executed consequences**: "I did X" not "I would do X"
- ✅ **Invisible MBTI**: Cognitive functions shown in behavior
- ✅ **Physical sensations**: Passion felt in the body
- ✅ **Concrete names**: "Carlos, my right hand" not "my allies"

## Requirements

- **Python 3.8+**
- **[Ollama](https://ollama.ai/)** with `qwen2.5:14b` model (or specify `--model`)
- **OpenClaw** and **OpenGoat** (for integration features)

### Installation

```bash
git clone https://github.com/gitsual/creador-de-personajes.git
cd creador-de-personajes

# Ensure Ollama is running with the model
ollama pull qwen2.5:14b
```

## Usage

### Basic Generation

```bash
# Generate agent files to ./agents/<name>/
python agent_generator.py "ENTJ 8w7 sx/so" --name "Commander"

# Specify output directory
python agent_generator.py "INFP 4w5 sp/sx" --name "Poet" --output ./my-agents/poet

# Use different model
python agent_generator.py "ESTJ 1w2 so/sp" --name "Director" --model qwen2.5:32b
```

### Full Integration

```bash
# Generate + deploy to OpenClaw + register in OpenGoat
python integrate_agent.py "ISFP 6w5 sp/sx" --name "Lorena"

# Skip generation (use existing agent)
python integrate_agent.py "ISFP 6w5 sp/sx" --name "Lorena" \
    --skip-generate --agent-dir ./agents/lorena

# Create as manager (not individual contributor)
python integrate_agent.py "ENTJ 8w7 sx/so" --name "Commander" --role manager
```

## Project Structure

```
creador-de-personajes/
├── agent_generator.py    # Main generator (V8)
├── integrate_agent.py    # Full pipeline with integration
├── csj_core.py           # MBTI cognitive functions & 4 sides
├── cuatro_lados.py       # Four sides of mind logic
├── narrador.py           # Narrative utilities
└── README.md
```

## Theory References

- **MBTI Cognitive Functions**: Based on C.S. Joseph's interpretation
- **Four Sides of the Mind**: Ego, Subconscious, Shadow, Superego states
- **Enneagram**: Riso-Hudson tradition with instinctual variants
- **Instinctual Variants**: Beatrice Chestnut's somatic approach

## License

MIT

---

*Inspired by Disco Elysium's skill system and C.S. Joseph's Type Grid.*
