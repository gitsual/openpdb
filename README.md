# 🎭 AI Personality Generator

<div align="center">

**Generate AI agents with REAL personality** — not "I am analytical", but actual behavior patterns.

```
Generic AI: "I am analytical and detail-oriented."
Tony Stark: "The room spins around me, a carousel of ideas. My fingers drum against the table, restless."
```

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/github/actions/workflow/status/gitsual/creador-de-personajes/test.yml?branch=main&style=flat-square&label=tests)](https://github.com/gitsual/creador-de-personajes/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/gitsual/creador-de-personajes?style=social)](https://github.com/gitsual/creador-de-personajes/stargazers)

</div>

---

## 🎬 See It In Action

| What You Say | What You Get |
|--------------|--------------|
| `python agent_generator.py -c "Tony Stark"` | ENTP 7w8 — restless innovator, carousel of ideas |
| `python agent_generator.py -c "John Wick"` | ISTP 6w5 — silent, prepared, lethal precision |
| `python agent_generator.py -c "Joker"` | ENTP 7w8 — chaos incarnate, magnetic intensity |
| `python agent_generator.py -c "Hermione"` | ISTJ 1w2 — perfectionist, by-the-book, loyal |

![Demo](docs/demo.gif)

---

## 📊 The Difference

| Aspect | Generic Agent | Generated Personality |
|--------|--------------|----------------------|
| **Voice** | "I am analytical" | "That's not how it works" (House) |
| **Energy** | (none) | "body feels electrified" (Stark) |
| **Stress** | (generic) | "They know where I live" (House) |
| **Boundaries** | "I prefer not to..." | "If you cross me — consequences" |

**Same AI. Different soul.**

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/gitsual/creador-de-personajes.git
cd creador-de-personajes

# 2. Get character database (12,000+ characters)
mkdir -p data && curl -sL "https://raw.githubusercontent.com/AKAazure/character-personality-database/main/pdb_dataset.csv" -o data/pdb_raw.csv
# Verify download (should be ~2MB+)
ls -lh data/pdb_raw.csv

# 3. Install Ollama (free local LLM)
# See: https://ollama.ai — then: ollama pull qwen2.5:14b

# 4. Generate!
python agent_generator.py -c "Tony Stark" --name Stark --lang en
```

**Output:** 9 personality files ready to use (SOUL.md, IDENTITY.md, AGENTS.md, etc.)

---

## 🌟 12,000+ Characters Available

Search any character from movies, TV, anime, games, or real people:

| Character | Type | Personality | Best For |
|-----------|------|-------------|----------|
| **Tony Stark** | ENTP 7w8 | Restless innovator, intense connections | Brainstorming, rapid prototyping |
| **John Wick** | ISTP 6w5 | Silent precision, prepared for anything | Execution, tactical tasks |
| **Hermione Granger** | ISTJ 1w2 | Perfectionist, loyal, by-the-book | Documentation, QA, research |
| **Tyrion Lannister** | ENTP 7w6 | Witty strategist, sees all angles | Negotiation, problem-solving |
| **The Joker** | ENTP 7w8 | Chaos agent, magnetic intensity | Creative disruption, edge cases |
| **Naruto Uzumaki** | ENFP 3w2 | Relentless optimist, never gives up | Motivation, team morale |
| **Yoda** | INTP 5w6 | Wise observer, cryptic depth | Mentorship, long-term strategy |
| **Jack Sparrow** | ENTP 7w8 | Chaotic improviser, lucky survivor | Unconventional solutions |
| **James Bond** | ISTP 6w5 | Cool under pressure, resourceful | Crisis management |
| **Walter White** | INTJ 5w6 | Cold strategist, meticulous planner | Complex planning, contingencies |

```bash
# Search the database
python pdb_search.py "your favorite character"

# Get just the typology
python pdb_search.py -t "Gandalf"
# Output: INTJ 5w4 sp/sx
```

---

## ❓ Do I Need OpenClaw?

**No!** This generator works standalone:

| Use Case | What You Get |
|----------|--------------|
| **Standalone** | Markdown files with complete personality (SOUL.md, etc.) |
| **With OpenClaw** | Auto-deploys to `~/.openclaw/agents/` |
| **With OpenGoat** | Auto-assigns to organizational hierarchy |

The output is **plain Markdown** — use it with any AI system, chatbot, or agent framework.

---

## 🧠 How It Works

Three psychology frameworks combined:

| Framework | What It Does | Example |
|-----------|--------------|---------|
| **MBTI** | How they think | ENTP = ideas first, debate everything |
| **Enneagram** | What drives them | 7w8 = avoid pain through excitement + intensity |
| **Instincts** | Where they focus | sx/sp = deep bonds + self-preservation |

**Result:** Agents that don't just respond — they *behave consistently*.

```
Tony Stark (ENTP 7w8 sx/sp):
- Thinks in rapid connections
- Driven by avoiding boredom + need for intensity  
- Focuses on deep bonds but protects himself
```

---

## 📝 Generated Output Example

**Command:** `python agent_generator.py -c "Tony Stark" --name Stark --lang en`

```markdown
# SOUL.md - Stark (ENTP 7w8 sx/sp)

## Who I Am
The hum of the city buzzes in my ears as I walk, eyes darting between 
buildings and people, searching for patterns and possibilities. 
I move with purpose, each step calculated but never stagnant.

## My Voice
1. Let's do this!
2. You've got to be kidding me.
3. This is a stroke of genius!
4. Why are you holding back?
5. We can't afford to wait!

## What Drives Me
My body hums with anticipation and desire; I'm drawn to the intensity 
of connection, the rush that comes from forging deep bonds.

## When They Fail Me
"If you can't be reliable, then I need to find someone else who can."
No room for excuses. Consequence executed without hesitation.
```

<details>
<summary>📄 All 9 generated files (click to expand)</summary>

- `SOUL.md` — Deep personality (2500+ words)
- `IDENTITY.md` — Quick reference card
- `AGENTS.md` — Behavioral rules
- `ROLE.md` — Organizational role
- `TOOLS.md` — Tool configurations
- `USER.md` — User context template
- `MEMORY.md` — Persistent memory
- `HEARTBEAT.md` — Periodic tasks
- `BOOTSTRAP.md` — First-run setup

</details>

---

## 🤝 Team Chemistry (OpenGoat)

When agents work together, personality matters:

| Pair | Chemistry | Why It Works |
|------|-----------|--------------|
| ENTP + INTJ | Stark + Batman | Innovation meets strategy |
| ISTP + ESTJ | Wick + Hermione | Execution meets process |
| ENFP + INTJ | Naruto + Sasuke | Optimism meets realism |

**Auto-assignment:** Based on MBTI, agents get assigned to compatible managers:
- Analysts (INTJ, INTP, ENTP) → CTO division
- Executors (ISTJ, ESTJ, ISTP) → COO division  
- Harmonizers (ENFJ, ENFP, ISFP) → CCO division

---

## 🌍 Languages

```bash
# English (recommended for sharing)
python agent_generator.py -c "Tony Stark" --lang en

# Spanish (default)
python agent_generator.py -c "Tony Stark" --lang es
```

---

## 🔧 Requirements

- **Python 3.8+**
- **Ollama** with `qwen2.5:14b` — [Install Ollama](https://ollama.ai) (free, runs locally)
- **curl** in PATH (included in Linux/macOS; Windows: install via `winget install curl`)
- **No external Python packages required**

> ⚠️ **Windows users:** Run scripts with `python script.py` instead of `./script.py`. Ensure `curl` is in PATH.

```bash
# Verify Ollama is running
ollama list

# If not installed:
# Linux: curl -fsSL https://ollama.ai/install.sh | sh
# macOS: brew install ollama
# Windows: Download from ollama.ai

# Get the model
ollama pull qwen2.5:14b
```

---

## 📂 Project Structure

```
creador-de-personajes/
├── agent_generator.py   # Main generator
├── pdb_search.py        # Character database search
├── integrate_agent.py   # OpenClaw + OpenGoat integration
├── data/                # PDB dataset (downloaded)
├── docs/                # GIFs, comparisons
└── tests/               # 31 tests passing
```

---

## ⭐ Support

If this helps you build better AI agents:

- **⭐ Star** — Helps others find it
- **🍴 Fork** — Customize for your needs
- **🐛 Issues** — Report bugs or request features
- **🔀 PRs** — New characters, better patterns

---

## 📚 Theory

Based on established typology systems:
- **MBTI**: C.S. Joseph's cognitive function interpretation
- **Enneagram**: Riso-Hudson tradition with instinctual variants
- **Instincts**: Beatrice Chestnut's somatic approach

> **Note:** These are personality frameworks for creative characterization, not scientifically validated psychological assessments. Great for AI personas; not for clinical use.

---

## 🔗 Related

- [OpenClaw](https://github.com/openclaw/openclaw) — AI agent framework
- [OpenGoat](https://github.com/openclaw/opengoat) — Agent organization management
- [Personality Database](https://www.personality-database.com) — Character typology source

---

## ❓ FAQ

<details>
<summary><b>How do I update an agent without losing manual changes?</b></summary>

The generator creates backups automatically before overwriting. Find them in the agent directory with `_backup_YYYYMMDD_HHMMSS` suffix. To preserve changes:
1. Copy your customized files somewhere safe
2. Regenerate the agent
3. Merge your changes back manually
</details>

<details>
<summary><b>Can I use GPT-4/Claude instead of Ollama?</b></summary>

Currently hardcoded for Ollama. To use other providers, modify `call_ollama()` in `narrador.py` or `agent_generator.py` to call your preferred API. The prompt structure remains the same.
</details>

<details>
<summary><b>How do I verify generation was successful?</b></summary>

Check that `SOUL.md` has 200+ words of coherent content. The generator now shows warnings if output seems too short or contains error messages.
</details>

<details>
<summary><b>How do I delete/uninstall an agent?</b></summary>

```bash
python integrate_agent.py --delete "Agent Name"
```
This removes the agent from local, OpenClaw, and OpenGoat directories.
</details>

<details>
<summary><b>What are the system requirements?</b></summary>

- **RAM:** 16GB+ recommended (model loads into memory)
- **VRAM:** 12GB+ for `qwen2.5:14b` (GPU acceleration)
- **Disk:** ~10GB for model, ~5MB per generated agent
- **CPU-only:** Works but slow (~2-5 min per agent)
</details>

<details>
<summary><b>Does it work offline?</b></summary>

**Yes**, once you have:
1. Downloaded the model (`ollama pull qwen2.5:14b`)
2. Downloaded the PDB dataset (`data/pdb_raw.csv`)

No internet required for generation after that.
</details>

---

**MIT License** | Built for humans who want AI with soul 🎭
