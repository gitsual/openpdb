# 🎭 AI Personality Generator

<div align="center">

**Turn any fictional character into an AI agent with their real personality.**

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](https://opensource.org/licenses/MIT)

[Demo](#-real-results) • [Quick Start](#-quick-start-30-seconds) • [How It Works](#-how-it-works) • [OpenGoat Integration](#-opengoat-integration)

</div>

---

## 🤔 What's the Point?

**Generic AI gives you lists. Personality agents give you perspective.**

When you ask ChatGPT for advice, you get a neutral, comprehensive response. When you ask Batman, you get *Batman's* response — direct, strategic, with references to his world and values.

---

## 🧪 Real Results (Actual Outputs, Not Marketing)

We ran identical questions through generic AI and personality-generated agents. These are **literal outputs** from `ollama run qwen3-coder`:

### "I'm creatively blocked on my project, haven't made progress in weeks"

<details>
<summary>🤖 <b>Generic AI</b> — Click to expand</summary>

```
Creative block is a common experience and can be very frustrating, especially 
when you're working on a project you're passionate about. Here are some 
strategies you could try:

1. **Change your environment** - Sometimes, a change of scenery can help you 
   see things from a different perspective.

2. **Take a break** - Stopping to force creativity might be what you need.

3. **Establish a routine** - Even if you don't have clear ideas, write something.

4. **Seek inspiration** - Read a book, watch a movie, listen to music.

5. **Break your project into smaller pieces** - If it seems overwhelming, 
   divide it into manageable tasks.

6. **Talk to someone** - [continues with 4 more generic points...]
```

</details>

**🦇 Batman (INTJ 1w9):**
```
*You're not blocked. You're stuck in the same room, staring at the same wall, 
and you know it.*

Look, I've been there — more times than I care to count. When ideas die on the 
page, when expectations are crushing you... that's not failure. That's the moment 
before the breakthrough.

**Step one:** Stop trying to force it. You won't solve a creative problem with 
more pressure.

**Step two:** Go back to basics. What was your original spark? Reconnect with 
that fire.

**Step three:** Work in silence. Let your subconscious work. Sometimes the best 
ideas come when you're not looking for them.
```

### "My friend is going through depression, how can I help without being intrusive?"

**🔧 Tony Stark (ENTP 7w8):**
```
— Listen, don't get me wrong, but if your friend is dealing with depression, 
you can't "fix" them like it's a software bug that gets patched. It's deeper 
than that.

*Leans in, with that look of someone who's been through the same thing.*

— What you need is to be present. You don't need to tell them "everything will 
be fine" or "just be positive." You just need to be there.

— If they don't want to talk, don't push them. If they want to talk, listen. 
Don't try to fix it with quick solutions.

— I've had my own fall. And the only person who helped me... was someone who 
didn't try to "cure" me. They let me breathe.

— So don't be intrusive. Be a friend. Don't push them, but don't let them fall 
either.
```

### "Is it worth investing in cryptocurrency now?"

**🃏 Joker (ENTP 7w8):**
```
**[Soft, slightly unhinged laughter]**

This is like playing with fire, but with a digital coin in your hand! 
Isn't that exactly what makes it fun? You can't predict it, you can't 
control it!

Cryptocurrencies are like chaos in asset form! You can have all your 
money one night and then... boom! Gone!

**But remember... if you're not willing to lose it all, you're not 
playing big!**
```

---

## 📊 The Difference

| | Generic AI | Personality Agent |
|---|-----------|------------------|
| **Tone** | Neutral, hedging | Distinctive voice |
| **Length** | 10-point lists | Concise, opinionated |
| **References** | None | Their world (Gotham, Stark Industries...) |
| **Actionability** | "Consider these factors..." | Clear stance |
| **Emotional Connection** | None | High (speaks from experience) |

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
# The SOUL.md becomes your system prompt
cat test_batman/SOUL.md | ollama run qwen3-coder
```

---

## 🐐 OpenGoat Integration

Generated agents work with [OpenGoat](https://github.com/marian2js/opengoat) for multi-agent orchestration.

<!-- TODO: Replace with actual OpenGoat UI screenshot -->
![OpenGoat Hierarchy](docs/opengoat_hierarchy.png)

### Demo Mode (Isolated)

Run a complete OpenGoat instance with fictional characters **without touching your real setup**:

```bash
./demo-opengoat.sh
# → Creates isolated instance at .opengoat-demo/
# → Runs on port 19124
# → Pre-configured hierarchy: Ripley (CEO) → Batman/Katniss/Wonder Woman → ICs
```

Access at: `http://127.0.0.1:19124`

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

See [docs/REAL_TEST_RESULTS.md](docs/REAL_TEST_RESULTS.md) for more real outputs.

---

**MIT License** | Real tests, not marketing 🎭
