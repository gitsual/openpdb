# 🎭 AI Personality Generator

<div align="center">

**Generate AI agents with REAL personality** — not "I am analytical", but actual behavior patterns grounded in their fictional world.

```
Generic AI: "I am analytical and detail-oriented. I check locks before leaving."
Walter White: "The smell of ammonia from the reagent bottles, sharp but familiar. 
              I assess the room as if mapping out an enemy's lair."
```

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/github/actions/workflow/status/gitsual/creador-de-personajes/test.yml?branch=main&style=flat-square&label=tests)](https://github.com/gitsual/creador-de-personajes/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](https://opensource.org/licenses/MIT)

</div>

---

## 🎬 See It In Action

| What You Say | What You Get |
|--------------|--------------|
| `python agent_generator.py -c "Tony Stark"` | ENTP 7w8 — Stark Industries, Pepper, Rhodey, suits malfunctioning in deserts |
| `python agent_generator.py -c "Walter White"` | INTJ 5w6 — Heisenberg, Jesse, Tuco's compound, blue meth |
| `python agent_generator.py -c "Hermione Granger"` | ISTJ 1w2 — Hogwarts, Harry, Ron, Triwizard Tournament |
| `python agent_generator.py -c "Luna Lovegood"` | INFP 9w1 — Ravenclaw, Thestrals, The Quibbler |

**New in V10:** Automatically fetches character context from Wikipedia to ground personalities in their actual fictional universe — no more generic "coffee shops" for wizards!

---

## 📊 The Difference

| Aspect | Without Context | With Context (V10) |
|--------|-----------------|-------------------|
| **Places** | "Office", "coffee shop" | **Hogwarts**, **Stark Tower**, **Tuco's compound** |
| **People** | Generic names (Sarah, Alex) | **Jesse Pinkman**, **Pepper Potts**, **Ron Weasley** |
| **Objects** | "Flashlight, batteries" | **Wand**, **Iron Man suit**, **reagent bottles** |
| **Stories** | "Missed a phone call" | **Negotiation with Tuco**, **Triwizard Tournament** |
| **Voice** | "I am analytical" | *"Say my name"* / *"Honestly, Ron!"* |

**Same typology. World-specific soul.**

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/gitsual/creador-de-personajes.git
cd creador-de-personajes

# 2. Get character database (12,000+ characters)
mkdir -p data && curl -sL "https://raw.githubusercontent.com/AKAazure/character-personality-database/main/pdb_dataset.csv" -o data/pdb_raw.csv

# 3. Install Ollama (free local LLM)
# See: https://ollama.ai — then: ollama pull qwen2.5:14b

# 4. Generate!
python agent_generator.py -c "Walter White" --lang en
```

**Output:** 9 personality files ready to use (SOUL.md, IDENTITY.md, etc.)

---

## 🌟 Real Examples

### Walter White (INTJ 5w6 sp/so)

```markdown
## Who I Am
I notice the exact placement of every item in my lab, how each piece of 
equipment is perfectly calibrated. The smell of ammonia from the reagent 
bottles, sharp but familiar. My movements are calculated; when I enter a 
room, I assess it as if mapping out an enemy's lair.

## My Territory
In the drug trade, I know who has power over whom. The name Gus Fring 
looms large, a figure of both respect and caution.

## A Story
The moment I stepped into Tuco's compound, the smell of gunpowder lingered 
in the air. After a tense negotiation, he left me alone amidst chaos. What 
changed was my newfound knowledge of Tuco's instability; from then on, I 
planned for all contingencies.
```

### Hermione Granger (ISTJ 1w2 so/sp)

```markdown
## Who I Am
I move through the crowded halls of Hogwarts with a purposeful stride. 
The scent of ancient parchment and beeswax candles is ever-present. 
My mandibles tighten involuntarily whenever I encounter a messy desk.

## My Voice
1. "If you don't mind, could I see the list of ingredients?" (with impatience)
2. "Honestly, Ron, I just need five minutes to think!"
3. "This is absolutely unacceptable."

## When They Fail Me
When Ron turned his back on Harry during their fourth-year fight over the 
Yule Ball, my heart sank. The bond that once seemed unbreakable had been 
tested, and I couldn't help but feel responsible for its repair.
```

### Tony Stark (ENTP 7w8 sx/sp)

```markdown
## Who I Am
I stand by the window of my penthouse, looking out at the city skyline. 
My hand traces the ridges of the metal frame as my eyes dart from the 
latest Stark Industries project to the small, framed photo of my parents.

## My Obsession
I'm drawn to people who can light up my brain as brightly as an idea does. 
A glance at Pepper, and her eyes become windows to the soul; a conversation 
with Rhodey turns into a deep dive into our shared past.

## A Story
At my father's funeral, I was distracted by thoughts of new projects—until 
James Rhodes called me out for not being there emotionally. For the next 
three months, I focused solely on stabilizing Stark Industries.
```

### Luna Lovegood (INFP 9w1 sx/sp)

```markdown
## Who I Am
I notice the patterns in the sky, how the stars shift at different times. 
In Hogwarts' Great Hall, the chandeliers cast shadows that dance along the 
walls during feasts. The stone feels cool beneath my feet.

## A Story
During the Triwizard Tournament, when Harry was chosen as the fourth 
champion, my father and I were discussing it over tea. Later that night, 
when we heard about Barty Crouch Jr., I couldn't shake the feeling that 
I should have paid more attention.
```

---

## 🧠 How It Works

**Three psychology frameworks + Wikipedia context:**

| Layer | What It Does | Example |
|-------|--------------|---------|
| **MBTI** | How they think | INTJ = strategic, long-term planning |
| **Enneagram** | What drives them | 5w6 = knowledge-hoarding + loyalty concerns |
| **Instincts** | Where they focus | sp/so = self-preservation + group status |
| **Context** | Ground in reality | Breaking Bad universe, meth lab, Heisenberg |

**Result:** Walter White doesn't check "door locks" — he checks **Tuco's instability**.

---

## 📂 Generated Files

Each character generates 9 files:

| File | Purpose |
|------|---------|
| `SOUL.md` | Deep personality (2500+ words) — the core |
| `IDENTITY.md` | Quick reference card |
| `AGENTS.md` | Behavioral rules |
| `ROLE.md` | Organizational role |
| `TOOLS.md` | Tool configurations |
| `USER.md` | User context template |
| `MEMORY.md` | Persistent memory |
| `HEARTBEAT.md` | Periodic tasks |
| `BOOTSTRAP.md` | First-run setup |

---

## 🔧 Requirements

- **Python 3.9+** (uses modern type hints)
- **Ollama** with `qwen2.5:14b` — [Install Ollama](https://ollama.ai) (free, runs locally)
- **Internet** for Wikipedia context (optional — works without, just less specific)

```bash
# Verify Ollama is running
ollama list

# Get the model (~9GB)
ollama pull qwen2.5:14b
```

**System requirements:**
- **RAM:** 16GB+ recommended
- **VRAM:** 12GB+ for GPU acceleration
- **Disk:** ~10GB for model

---

## 🌍 Languages

```bash
# English
python agent_generator.py -c "Tony Stark" --lang en

# Spanish (default)
python agent_generator.py -c "Tony Stark" --lang es
```

---

## 📂 Project Structure

```
creador-de-personajes/
├── agent_generator.py   # Main generator
├── character_context.py # Wikipedia context fetcher (NEW)
├── pdb_search.py        # Character database search
├── integrate_agent.py   # OpenClaw + OpenGoat integration
├── data/                # PDB dataset (12,000+ characters)
├── examples/            # Pre-generated examples
│   ├── tony_stark/
│   ├── walter_white/
│   ├── hermione/
│   └── luna_lovegood/
└── tests/               # 29 tests passing
```

---

## ❓ FAQ

<details>
<summary><b>What if Wikipedia doesn't have my character?</b></summary>

The generator still works — it just uses typology alone (like V9). For best results, use well-known characters from movies, TV, books, or games.
</details>

<details>
<summary><b>Can I provide custom context?</b></summary>

Coming soon! For now, Wikipedia is the automatic source. Manual `--context` flag planned.
</details>

<details>
<summary><b>Can I use GPT-4/Claude instead of Ollama?</b></summary>

Modify `call_ollama()` in `agent_generator.py` to call your preferred API. The prompt structure remains the same.
</details>

<details>
<summary><b>Does it work offline?</b></summary>

**Partially.** Generation works offline once you have the model, but Wikipedia context requires internet. Without internet, you get typology-only generation (still good, just more generic).
</details>

---

## 🤝 Related Projects

- [OpenClaw](https://github.com/openclaw/openclaw) — AI agent framework
- [OpenGoat](https://github.com/openclaw/opengoat) — Agent organization management
- [Personality Database](https://www.personality-database.com) — Character typology source

---

## 📚 Theory

Based on established typology systems:
- **MBTI**: C.S. Joseph's cognitive function interpretation
- **Enneagram**: Riso-Hudson tradition with instinctual variants
- **Instincts**: Beatrice Chestnut's somatic approach

> **Note:** These are personality frameworks for creative characterization, not scientifically validated psychological assessments.

---

**MIT License** | Built for humans who want AI with soul 🎭
