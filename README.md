# 🎭 OpenPDB

<div align="center">

**Generate AI agents with real personalities using MBTI + Enneagram + Instincts from the Personality Database.**

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](https://opensource.org/licenses/MIT)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gitsual/creador-de-personajes/blob/main/demo.ipynb)

[**Try Demo →**](#-try-it-now) • [Quick Start](#-quick-start-30-seconds) • [How It Works](#-how-it-works) • [OpenGoat Integration](#-opengoat-multi-agent-collaboration)

</div>

---

## 🎮 Try It Now

**No installation required.** Click the button to run in your browser:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gitsual/creador-de-personajes/blob/main/demo.ipynb)

The notebook lets you:
1. Generate any character's personality
2. Chat with them using their unique voice

---

## 🤔 What's the Point?

**Generic AI gives you lists. Personality agents give you perspective.**

When you ask ChatGPT for advice, you get a neutral, comprehensive response. When you ask Batman, you get *Batman's* response — direct, strategic, with references to his world and values.

---

## 🧪 Real Results (Actual Outputs, Not Marketing)

These are **literal outputs** from `ollama run qwen3-coder`:

### "I'm creatively blocked on my project"

<details>
<summary>🤖 <b>Generic AI</b> — Click to expand</summary>

```
Creative block is a common experience. Here are some strategies:

1. **Change your environment** - A change of scenery can help.
2. **Take a break** - Stopping to force creativity might help.
3. **Establish a routine** - Even without ideas, write something.
4. **Seek inspiration** - Read a book, watch a movie.
5. **Break it into smaller pieces** - Divide into manageable tasks.
6. **Talk to someone** - [continues with more points...]
```

</details>

**🦇 Batman (INTJ 1w9):**
```
*You're not blocked. You're stuck in the same room, staring at the 
same wall, and you know it.*

Look, I've been there — more times than I care to count. When ideas 
die on the page, when expectations are crushing you... that's not 
failure. That's the moment before the breakthrough.

**Step one:** Stop trying to force it.
**Step two:** Go back to basics. What was your original spark?
**Step three:** Work in silence. Let your subconscious work.
```

### "Is it worth investing in cryptocurrency?"

**🃏 Joker (ENTP 7w8):**
```
**[Soft, slightly unhinged laughter]**

This is like playing with fire, but with a digital coin in your hand! 
Isn't that what makes it fun? You can't predict it, you can't control it!

Cryptocurrencies are like chaos in asset form! You can have all your 
money one night and then... boom! Gone!

**But remember... if you're not willing to lose it all, you're not 
playing big!**
```

---

## 🐐 OpenGoat Multi-Agent Collaboration

The real power comes when agents **work together**. Here's a real collaboration:

### Scenario: Startup Crisis

> "Our startup has 3 months of runway. Pivot or seek investment?"

**The Team:**
- **Ripley** (CEO) — Makes the final call
- **Batman** (CTO) — Technical assessment  
- **Katniss** (COO) — Operational reality
- **Wonder Woman** (CCO) — Team alignment

### How They Collaborate

**RIPLEY (CEO)** opens:
```
"We've got three months. That's not a luxury — that's a death sentence. 
Batman — can we pivot without betraying our vision?
Katniss — what are the real numbers?
Tell me the truth — not the one that sounds good."
```

**BATMAN (CTO)** responds:
```
"If we're going to pivot, it has to be strategic, not reactive. 
The problem isn't features — it's trust. We can pivot — but only 
from a place of clarity, not chaos."
```

**KATNISS (COO)** delivers numbers:
```
Burn rate: $2.3M runway at current pace
Timeline: Need $1.2M by Q2 or we're looking at hard stop
Tactical: Can cut overhead 15% if we streamline
```

**RIPLEY (CEO)** decides:
```
Decision: Pursue investment with clear pivot strategy.

Week 1-4: Batman refines positioning
Week 5-8: Katniss prepares investor materials  
Week 9-12: We pitch. No traction? Controlled pivot.

The ship doesn't go down on my watch.
```

👉 **[Full collaboration transcript](docs/COLLABORATION_DEMO.md)**

### Run OpenGoat Demo

```bash
./demo-opengoat.sh
# → Isolated instance at http://127.0.0.1:19124
# → Pre-configured: Ripley (CEO) → Batman/Katniss/Wonder Woman → ICs
```

---

## 📊 The Difference

| | Generic AI | Personality Agent |
|---|-----------|------------------|
| **Tone** | Neutral, hedging | Distinctive voice |
| **Length** | 10-point lists | Concise, opinionated |
| **References** | None | Their world (Gotham, Stark Industries...) |
| **Collaboration** | N/A | Natural conflict & resolution |
| **Decision-making** | "Consider factors..." | Takes a stance |

---

## 🚀 Quick Start (30 seconds)

```bash
# 1. Clone
git clone https://github.com/gitsual/creador-de-personajes.git && cd creador-de-personajes

# 2. Get character database (12,000+ characters)
mkdir -p data && curl -sL "https://raw.githubusercontent.com/AKAazure/character-personality-database/main/pdb_dataset.csv" -o data/pdb_raw.csv

# 3. Generate a character
python agent_generator.py -c "Batman" --lang en
```

**Output:**
```
🔍 Searching PDB for 'Batman'...
✅ Found: Bruce Wayne "Batman" → INTJ 1w9 so/sp
📚 Context: wikipedia (Batman)
✨ V8 'Bruce' ready → test_batman/
```

---

## 🧠 How It Works

1. **PDB Search** — Finds character in 12,000+ [personality database](https://www.personality-database.com/)
2. **Typology** — Gets MBTI + Enneagram + Instinctual variants
3. **Wikipedia** — Fetches character background for grounding
4. **Generation** — Creates SOUL.md with personality-specific voice, values, stories

**Use the output:**
```bash
cat test_batman/SOUL.md | ollama run qwen3-coder
```

---

## 🦸 Available Characters

```
examples/
├── batman/          # INTJ 1w9 - DC Comics
├── tony_stark/      # ENTP 7w8 - MCU
├── john_wick/       # ISTP 6w5 - Action
├── joker/           # ENTP 7w8 - DC Comics
├── daenerys/        # ENFJ 1w2 - Game of Thrones
├── ripley/          # INTJ 8w9 - Alien
├── katniss/         # ISTP 6w5 - Hunger Games
└── wonder_woman/    # ENFJ 2w1 - DC Comics
```

Or generate any of the 12,000+ characters in the database.

---

## ⚠️ Honest Limitations

- **Quality ceiling:** With qwen3-coder, expect ~7/10 quality. Larger models do better.
- **Well-known characters work better:** Batman > obscure anime characters.
- **Not magic:** They have the personality *style*, not actual memories.

---

## 🔧 Requirements

- Python 3.9+
- [Ollama](https://ollama.ai) with any model (qwen3-coder recommended)
- Internet for Wikipedia context (optional)

---

## 📖 More Examples

- [Real Test Results](docs/REAL_TEST_RESULTS.md) — Individual agent outputs
- [Collaboration Demo](docs/COLLABORATION_DEMO.md) — Full multi-agent transcript

---

**MIT License** | Real tests, not marketing 🎭
