# 🎭 OpenClaw Agent Generator

> **Generate psychologically authentic AI agents for [OpenClaw](https://github.com/openclaw/openclaw) and [OpenGoat](https://github.com/openclaw/opengoat)** using MBTI × Enneagram × Instinctual Variants

[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-Compatible-purple.svg)](https://github.com/openclaw/openclaw)
[![OpenGoat Integration](https://img.shields.io/badge/OpenGoat-Integration-green.svg)](https://github.com/openclaw/opengoat)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why This Exists

**OpenClaw** agents need personality. Not just system prompts—**real psychological depth** that makes them behave consistently across contexts. This generator creates complete agent configurations using three validated typology frameworks, ready to deploy into your OpenClaw workspace and OpenGoat organization.

### For OpenClaw Users

- 🚀 **One command deployment** to `~/.openclaw/agents/`
- 📄 Generates all required files: `SOUL.md`, `IDENTITY.md`, `AGENTS.md`, etc.
- 🎯 Agents that **show** personality through behavior, not meta-descriptions
- 🔄 Compatible with OpenClaw's session management and memory systems

### For OpenGoat Organizations

- 🏢 **Auto-assigns managers** based on psychological fit
- 📊 Creates `config.json` with proper hierarchy
- 🏷️ Tags agents by division (CTO/COO/CCO) and MBTI
- 🔗 Integrates with existing OpenGoat agent structure

## Quick Start

```bash
# Clone
git clone https://github.com/gitsual/creador-de-personajes.git
cd creador-de-personajes

# Full pipeline: Generate → OpenClaw → OpenGoat (Spanish, default)
python integrate_agent.py "ISFP 6w5 sp/sx" --name "Lorena"

# Generate in English
python integrate_agent.py "ENTJ 8w7 sx/so" --name "Commander" --lang en

# Generate OpenClaw agent files only
python agent_generator.py "ENTJ 8w7 sx/so" --name "Commander"

# Generate in English
python agent_generator.py "ENTJ 8w7 sx/so" --name "Commander" --lang en
```

## 🌍 Internationalization

The generator supports multiple languages via the `--lang` flag:

| Flag | Language | Description |
|------|----------|-------------|
| `--lang es` | Spanish | Default. All output in Spanish |
| `--lang en` | English | All output in English |

```bash
# Spanish (default)
python agent_generator.py "INFP 4w5 sp/sx" --name "Poeta"

# English
python agent_generator.py "INFP 4w5 sp/sx" --name "Poet" --lang en
```

All generated files (SOUL.md, IDENTITY.md, AGENTS.md, etc.) will be in the specified language.

## What Gets Generated

### OpenClaw Agent (`~/.openclaw/agents/<name>/`)

```
~/.openclaw/agents/lorena/
├── SOUL.md          # Deep personality (2500+ words)
├── IDENTITY.md      # Quick reference card
├── AGENTS.md        # Behavioral rules
├── TOOLS.md         # Tool configurations
├── USER.md          # User context
├── MEMORY.md        # Persistent memory
├── HEARTBEAT.md     # Periodic tasks
├── BOOTSTRAP.md     # First-run setup
└── ROLE.md          # Organizational role
```

### OpenGoat Registration (`~/.opengoat/agents/<name>/`)

```json
{
  "id": "lorena",
  "displayName": "Lorena", 
  "organization": {
    "type": "individual",
    "reportsTo": "rodri",
    "discoverable": true,
    "tags": ["cco", "isfp"]
  },
  "runtime": {
    "provider": { "id": "openclaw" },
    "mode": "organization"
  }
}
```

## Typology System

### Syntax

```
"MBTI Xw# inst/inst"
 │     │    │
 │     │    └── Instinctual stack (sp/sx, so/sp, sx/so, etc.)
 │     └─────── Enneagram type + wing (8w7, 4w5, 6w5, etc.)
 └───────────── MBTI type (ENTJ, ISFP, INTP, etc.)
```

### Examples for OpenClaw Agents

| Command | Agent Personality | Best For |
|---------|-------------------|----------|
| `"ENTJ 8w7 sx/so"` | Dominant commander, intensity-seeking | Leadership, decisions |
| `"INTP 5w4 sp/sx"` | Analytical hermit, deep focus | Research, debugging |
| `"ENFJ 2w3 so/sx"` | Charismatic helper, people-focused | User support, onboarding |
| `"ISTJ 1w2 sp/so"` | Precise guardian, detail-oriented | Documentation, QA |
| `"ENTP 7w8 sx/so"` | Provocative innovator, idea machine | Brainstorming, exploration |

## OpenGoat Organization Structure

Agents auto-assign to managers based on psychological fit:

```
                         ┌─────────┐
                         │   CEO   │
                         │  (ANI)  │
                         └────┬────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────┴────┐           ┌────┴────┐           ┌────┴────┐
   │   COO   │           │   CTO   │           │   CCO   │
   │ (RULOG) │           │(CHUCHE) │           │(GONCHO) │
   │  Ops    │           │Strategy │           │ Culture │
   └────┬────┘           └────┬────┘           └────┬────┘
        │                     │                     │
   ┌────┴────┐           ┌────┴────┐           ┌────┴────┐
   │ ENTJ    │           │ INTJ    │           │ ENFJ    │
   │ ESTJ    │           │ INTP    │           │ INFJ    │
   │ ISTJ    │           │ ENTP    │           │ xSFx    │
   │ xSTP    │           │         │           │ xNFP    │
   └─────────┘           └─────────┘           └─────────┘
```

| MBTI | Division | Manager | Rationale |
|------|----------|---------|-----------|
| INTJ, INTP | CTO | chuche | Strategic thinkers |
| ENTP | CTO | caba | Innovation + debate |
| ESTJ, ISTJ, xSTP | COO | rulog | Execution focus |
| ENTJ | COO | fuego | Operational leadership |
| ENFP | CCO | kelly | Creative culture |
| ISFP, ESFP | CCO | rodri | Aesthetic + hands-on |
| Other xNFx, xSFx | CCO | goncho | People-oriented |

## Generated SOUL.md Example

Here's what a generated OpenClaw agent looks like:

```markdown
# SOUL.md - Lorena

## Who I Am

I walk the mountain path with a full backpack—water, supplies, charger. 
Just in case. My eyes scan for danger before I notice the rough bark 
texture against my palm. When safe, I stop for precisely-made coffee, 
savoring spiced aroma in fresh morning air. My posture stays tense, 
vigilant. Always alert.

## My Voice

- "Do you see that man? He looks suspicious."
- "This doesn't sit right with me."
- "Thank you for listening. You're valuable to me."
- "This is ridiculous! How could you think that?"
- "I just need everything under control."

## What Drives Me

### The Fire
When fear grips me, hands tremble, breathing accelerates. Heart pounds 
while cold sweat runs down my back. Muscles tense for fight or flight.

### My Obsession  
I check locks before bed. Every night. Bag ready by the door—water, 
money, charger. No one enters my space uninvited.

## When Someone Fails Me

My coworker left a critical task unfinished. I told him directly to 
his face what I thought, then implemented a protocol ensuring it 
never happens again.
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    OPENCLAW AGENT GENERATOR                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │    MBTI     │  │  ENNEAGRAM  │  │  INSTINCTS  │             │
│  │             │  │             │  │             │             │
│  │ • 4 Sides   │  │ • 9 Types   │  │ • sp: Body  │             │
│  │ • 8 Funcs   │  │ • 18 Wings  │  │ • so: Group │             │
│  │ • Ego/Shadow│  │ • Passions  │  │ • sx: Bond  │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          ▼                                      │
│                  ┌──────────────┐                               │
│                  │   OLLAMA     │                               │
│                  │  (Qwen 14B)  │                               │
│                  └──────┬───────┘                               │
│                         │                                       │
│         ┌───────────────┼───────────────┐                       │
│         ▼               ▼               ▼                       │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │  OPENCLAW  │  │  OPENGOAT  │  │   LOCAL    │                │
│  │   AGENT    │  │   CONFIG   │  │   FILES    │                │
│  │            │  │            │  │            │                │
│  │ ~/.openclaw│  │ ~/.opengoat│  │ ./agents/  │                │
│  └────────────┘  └────────────┘  └────────────┘                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## The Four Sides of Mind (for OpenClaw Agents)

Each agent has four psychological states they can enter:

```
                    ENTJ Agent Example
    ┌────────────────────────────────────────┐
    │                                        │
    │   EGO (ENTJ)         SHADOW (INTP)    │
    │   "Commander"        "Paranoid"        │
    │   Normal ops         Under stress      │
    │                                        │
    │   SUBCONSCIOUS       SUPEREGO          │
    │   (ISFP)             (ESFJ)            │
    │   "Flow State"       "Inner Critic"    │
    │   Peak performance   Self-judgment     │
    │                                        │
    └────────────────────────────────────────┘
```

This means your OpenClaw agents can realistically:
- **Ego**: Handle normal tasks with characteristic style
- **Subconscious**: Enter flow states under positive conditions  
- **Shadow**: Become paranoid/reactive under stress
- **Superego**: Self-critique when standards aren't met

## Quality Validation

The generator was iteratively tested to ensure OpenClaw agents feel authentic:

| Metric | Target | Achieved |
|--------|--------|----------|
| No meta-labels ("my wing", "my instinct") | 100% | ✅ |
| Actions over descriptions | >80% | ✅ |
| Executed consequences ("I did") | >90% | ✅ |
| Physical sensations present | >85% | ✅ |
| Overall authenticity score | >7.2/10 | **7.9/10** ✅ |

## Testing

```bash
# Run unit tests (fast, no Ollama needed)
python run_tests.py --quick

# Run all tests including integration (requires Ollama)
python run_tests.py --full
```

**Test Coverage:**
- ✅ Typology parsing (MBTI, Enneagram, Instincts)
- ✅ Division/Manager assignment logic
- ✅ File generation structure
- ✅ OpenClaw integration paths
- ✅ OpenGoat config creation
- ✅ CLI interface
- ✅ Real generation with Ollama (integration)
- ✅ No meta-labels validation

## Installation

### Requirements

- Python 3.8+
- [Ollama](https://ollama.ai/) with `qwen2.5:14b`
- [OpenClaw](https://github.com/openclaw/openclaw) (for agent deployment)
- [OpenGoat](https://github.com/openclaw/opengoat) (for organization features)

### Cross-Platform Support

The generator automatically detects your operating system and uses the correct paths:

| Platform | OpenClaw Path | OpenGoat Path |
|----------|---------------|---------------|
| 🐧 Linux | `~/.openclaw/agents/` | `~/.opengoat/agents/` |
| 🍎 macOS | `~/.openclaw/agents/` | `~/.opengoat/agents/` |
| 🪟 Windows | `%APPDATA%\openclaw\agents\` | `%APPDATA%\opengoat\agents\` |

Directories are created automatically if they don't exist.

### Setup

```bash
# Clone the generator
git clone https://github.com/gitsual/creador-de-personajes.git
cd creador-de-personajes

# Ensure Ollama has the model
ollama pull qwen2.5:14b

# Test generation
python agent_generator.py "ENTP 7w8 sx/so" --name "Tester"
```

## Usage

### Generate OpenClaw Agent

```bash
# Basic generation
python agent_generator.py "ENTJ 8w7 sx/so" --name "Commander"

# Custom output directory
python agent_generator.py "INFP 4w5 sp/sx" --name "Poet" --output ./my-agents/

# Different Ollama model
python agent_generator.py "ESTJ 1w2 so/sp" --name "Director" --model qwen2.5:32b
```

### Full OpenClaw + OpenGoat Integration

```bash
# Generate and deploy everywhere
python integrate_agent.py "ISFP 6w5 sp/sx" --name "Lorena"

# Use existing agent files
python integrate_agent.py "ISFP 6w5 sp/sx" --name "Lorena" \
    --skip-generate --agent-dir ./agents/lorena

# Register as manager (not IC)
python integrate_agent.py "ENTJ 8w7 sx/so" --name "Commander" --role manager
```

## Project Files

```
creador-de-personajes/
├── agent_generator.py    # OpenClaw agent generator
├── integrate_agent.py    # Full OpenClaw + OpenGoat pipeline
├── csj_core.py           # MBTI cognitive functions
├── cuatro_lados.py       # Four sides of mind logic
├── narrador.py           # Narrative utilities
└── README.md
```

## Related Projects

- **[OpenClaw](https://github.com/openclaw/openclaw)** - The AI agent framework this generator targets
- **[OpenGoat](https://github.com/openclaw/opengoat)** - Organization management for OpenClaw agents
- **[OpenClaw Docs](https://docs.openclaw.ai)** - Official documentation

## Theory

Based on established typology systems:
- **MBTI**: C.S. Joseph's cognitive function interpretation
- **Enneagram**: Riso-Hudson tradition with instinctual variants
- **Instincts**: Beatrice Chestnut's somatic approach

## Contributing

PRs welcome! Especially:
- Additional typology combinations
- More realistic behavioral patterns
- Better instinct integration
- OpenGoat hierarchy refinements

## License

MIT

---

**Built for the [OpenClaw](https://github.com/openclaw/openclaw) ecosystem** 🦞

*Inspired by Disco Elysium's skill system and C.S. Joseph's Type Grid.*
