# 🎭 AI Personality Generator

<div align="center">

**Why settle for "I am a helpful assistant" when you can have Batman, Ripley, or Daenerys?**

Generate AI agents that actually *behave* like their personality — not just describe it.

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/github/actions/workflow/status/gitsual/creador-de-personajes/test.yml?branch=main&style=flat-square&label=tests)](https://github.com/gitsual/creador-de-personajes/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](https://opensource.org/licenses/MIT)

</div>

---

## 🎯 The Problem With Generic Agents

Most AI agents sound the same. They're helpful, they're polite, and they're **forgettable**.

```
USER: "Should I take this risky business opportunity?"

GENERIC AGENT: "That's an interesting question. There are pros and cons to consider. 
               On one hand, risk can lead to reward. On the other hand, it could fail. 
               I recommend weighing your options carefully."
```

**Useful? Barely. Memorable? No. Actionable? Not really.**

---

## 💥 The Solution: Personality-Driven Responses

Same question. Different agents. **Real value.**

```
USER: "Should I take this risky business opportunity?"
```

### Batman (INTJ — Strategic Planner)
```
"What's your exit strategy? Before you commit, map every scenario where this fails. 
Who benefits if you lose? I've seen too many people walk into traps because they 
only looked at the upside. Show me your contingency plan first."
```
**Value:** Forces you to think about failure modes you hadn't considered.

### Tony Stark (ENTP — Innovator)
```
"Risky? That's where the fun is. But here's the real question — is it risky because 
it's actually dangerous, or risky because nobody's tried it yet? Those are very 
different things. If it's the second one, you might be looking at your biggest win."
```
**Value:** Reframes "risk" to distinguish real danger from unexplored opportunity.

### Ripley (INTJ — Crisis Survivor)
```
"I've walked into situations where everyone said it was fine. It wasn't. 
Trust your gut, but verify everything. Who gave you this opportunity? 
What do they gain? And what happens if you say no — do they pressure you?"
```
**Value:** Pattern recognition from someone who's survived actual disasters.

### Daenerys (ENFJ — Visionary Leader)
```
"Will this opportunity let you help the people who depend on you, or will it 
only serve yourself? I've taken risks that cost everything — but they were 
for something larger than me. What's yours for?"
```
**Value:** Connects the decision to purpose and impact on others.

---

## 🦸 The Full Team: 8 Iconic Personalities

<div align="center">

![Full Team](docs/full_team.png)

</div>

| Character | Type | Franchise | Strength | Best For |
|-----------|------|-----------|----------|----------|
| **Batman** | INTJ 1w9 | DC | Strategic planning | Risk assessment, contingencies |
| **Daenerys** | ENFJ 1w2 | GoT | Inspiring vision | Leadership, motivation |
| **Tony Stark** | ENTP 7w8 | MCU | Rapid innovation | Brainstorming, pivots |
| **Ripley** | INTJ 8w9 | Alien | Crisis management | Threat analysis, survival |
| **John Wick** | ISTP 6w5 | Action | Precise execution | Implementation, reliability |
| **Katniss** | ISTP 6w5 | Hunger Games | Resourceful survival | Constraints, adaptation |
| **Wonder Woman** | ENFJ 2w1 | DC | Diplomatic solutions | Conflict resolution |
| **Joker** | ENTP 7w8 | DC | Chaos & stress-testing | Finding vulnerabilities |

---

## 📊 Individual Use Cases: Generic vs. Personality

### Use Case 1: Code Review

**USER:** "Review this authentication code for security issues."

| Agent | Response Style | Unique Value |
|-------|---------------|--------------|
| **Generic** | "Here are some best practices to consider..." | Checklist approach |
| **Ripley** | "I've seen systems fail because people trusted the happy path. Where's your breach protocol? What happens when — not if — someone gets through?" | **Paranoid thoroughness from surviving the Nostromo** |
| **Joker** | "Oh, this is fun. You're assuming users will behave. Let me show you 12 ways I'd break this before lunch." | **Adversarial thinking that finds real exploits** |

---

### Use Case 2: Product Launch Decision

**USER:** "Should we launch next month or wait for more features?"

| Agent | Response | Unique Value |
|-------|----------|--------------|
| **Generic** | "Both options have merit. Consider your market timing." | Non-committal |
| **Tony Stark** | "Ship it. Perfect is the enemy of done. I launched the Mark I in a cave with scraps. You've got more than that. Ship, learn, iterate." | **Bias toward action from someone who built Iron Man under fire** |
| **Batman** | "What does your competition know that you don't? If they're moving, waiting costs you. If they're stalled, you have time. Don't launch blind." | **Competitive intelligence focus** |

---

### Use Case 3: Team Conflict Resolution

**USER:** "Two senior engineers are fighting over architecture decisions."

| Agent | Response | Unique Value |
|-------|----------|--------------|
| **Generic** | "Communication is key. Try facilitating a meeting." | Obvious advice |
| **Wonder Woman** | "Bring them together — but not to argue. Ask each to present the OTHER person's position fairly first. When they understand what they're actually fighting about, half the conflict dissolves." | **Diplomatic technique from an actual ambassador** |
| **Daenerys** | "Who do they serve? If this fight is about ego, remove both from the decision. If it's about genuinely different visions, make them choose: unity or exile." | **Leadership clarity that cuts through politics** |

---

### Use Case 4: Handling Burnout

**USER:** "I'm exhausted and losing motivation. What should I do?"

| Agent | Response | Unique Value |
|-------|----------|--------------|
| **Generic** | "Self-care is important. Consider taking breaks and maintaining work-life balance." | Platitudes |
| **Katniss** | "You don't have to save everyone. I learned that the hard way. Protect what you can carry. Drop everything else. The people who matter will still be there." | **Survival wisdom from someone who carried too much** |
| **John Wick** | "Focus on one thing. Complete it. Then the next. Don't think about the mountain — just the step in front of you. That's how I got through." | **Tactical focus from someone who literally fought his way out** |

---

## 🚀 Full Team Collaboration: Complex Problem

**SCENARIO:** Your startup just discovered a major security breach. Customer data may be compromised. You have 48 hours before it becomes public. What do you do?

### Generic Agent Response:
```
"This is a serious situation. I recommend:
1. Assess the damage
2. Notify relevant parties
3. Implement fixes
4. Communicate transparently

Would you like me to elaborate on any of these points?"
```

**Problem:** This is a checklist, not a strategy. It doesn't account for competing priorities, human factors, or the chaos of real crisis management.

---

### The Full Team Response:

#### **BATMAN** (Crisis Command)
```
"First: contain. No one outside this room knows anything until we control the 
narrative. Ripley — assess what they actually got. Tony — can we patch the 
vulnerability in 12 hours? Katniss — what's our absolute minimum viable response 
if everything else fails?"
```

#### **RIPLEY** (Threat Assessment)
```
"I've pulled the logs. They were in the system for 72 hours before we noticed. 
That's enough time for complete exfiltration. Assume they have everything. 
The question isn't what they took — it's what they'll do with it. And why 
they haven't moved yet."
```

#### **TONY STARK** (Technical Response)
```
"I can patch the entry point in 6 hours. But here's the thing — if they're still 
watching, they'll see us patching and know we're onto them. We could use that. 
Let them see us 'fix' a decoy while we actually rebuild the core system underneath."
```

#### **JOHN WICK** (Execution Planning)
```
"I'll handle the operational timeline. Every hour blocked out. Every person 
assigned. No gaps. When we move, we move together — no one goes solo, 
no one freelances. Clear?"
```

#### **DAENERYS** (Stakeholder Management)
```
"Our customers trusted us. That trust was broken. When we communicate, 
we don't hide behind legal language — we speak to them as people. I'll draft 
the message personally. They'll hear it from leadership, not PR."
```

#### **WONDER WOMAN** (External Relations)
```
"We have regulators, partners, and press to manage. I'll open direct lines 
before the story breaks — frame it as proactive disclosure, not damage control. 
We control the narrative by getting there first."
```

#### **KATNISS** (Worst-Case Preparation)
```
"If we can't contain this — if it all goes wrong — what do we need to survive? 
I'm preparing the fallback: reduced operations, skeleton crew, emergency funds 
accessible. Hope we don't need it, but it'll be ready."
```

#### **JOKER** (Red Team)
```
"You're all assuming they wanted data. What if that's not the point? What if 
they wanted you to FIND the breach? While you're all staring at this door, 
what's happening at the other ones? I'd check your supply chain partners. Today."
```

---

### Result: A Complete Crisis Response

| Phase | Owner | Action | Timeline |
|-------|-------|--------|----------|
| **Command** | Batman | Central coordination, information control | Immediate |
| **Assessment** | Ripley | Full threat analysis, assume worst case | 0-6 hours |
| **Technical** | Tony Stark | Decoy patch + real rebuild | 0-24 hours |
| **Operations** | John Wick | Hour-by-hour execution timeline | Continuous |
| **Communications** | Daenerys | Customer messaging, human tone | 12-24 hours |
| **External** | Wonder Woman | Regulator/partner/press management | 6-48 hours |
| **Contingency** | Katniss | Survival plan if containment fails | Parallel |
| **Red Team** | Joker | Adversarial analysis, find blind spots | Continuous |

**This isn't a checklist. It's a coordinated response leveraging 8 distinct perspectives.**

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/gitsual/creador-de-personajes.git
cd creador-de-personajes

# Get character database (12,000+ characters)
mkdir -p data && curl -sL "https://raw.githubusercontent.com/AKAazure/character-personality-database/main/pdb_dataset.csv" -o data/pdb_raw.csv

# Install Ollama (free local LLM) — https://ollama.ai
ollama pull qwen2.5:14b

# Generate any character!
python agent_generator.py -c "Batman" --lang en
python agent_generator.py -c "Ripley" --lang en
python agent_generator.py -c "Daenerys Targaryen" --lang en
```

---

## 📂 8 Pre-Generated Examples

```
examples/
├── batman/          # INTJ 1w9 - Strategic Commander
├── tony_stark/      # ENTP 7w8 - Innovative Disruptor
├── john_wick/       # ISTP 6w5 - Precise Executor
├── joker/           # ENTP 7w8 - Chaos Consultant
├── daenerys/        # ENFJ 1w2 - Visionary Leader
├── ripley/          # INTJ 8w9 - Crisis Survivor
├── katniss/         # ISTP 6w5 - Resourceful Adapter
└── wonder_woman/    # ENFJ 2w1 - Diplomatic Bridge
```

Each character generates 9 files with deep personality profiles, behavioral rules, and organizational integration.

---

## 🧠 How It Works

**Three psychology frameworks + Wikipedia context:**

| Layer | What It Provides |
|-------|-----------------|
| **MBTI** | Cognitive style (how they think) |
| **Enneagram** | Core motivation (what drives them) |
| **Instincts** | Focus area (what they prioritize) |
| **Wikipedia** | Real-world grounding (their actual story) |

**Result:** Ripley doesn't just "analyze threats" — she analyzes them like someone who survived the Nostromo. Batman doesn't just "plan" — he plans like someone who watched his parents die and vowed it would never happen again.

---

## 🔧 Requirements

- **Python 3.9+**
- **Ollama** with `qwen2.5:14b` — [Install Ollama](https://ollama.ai)
- **Internet** for Wikipedia context (optional)

---

## 🤝 Integration

Works standalone or with:
- [OpenClaw](https://github.com/openclaw/openclaw) — AI agent framework
- [OpenGoat](https://github.com/openclaw/opengoat) — Multi-agent organization

---

**MIT License** | Built for humans who want AI with soul 🎭

---

<div align="center">

*"Generic agents give you answers. Personality-driven agents give you perspectives."*

</div>
