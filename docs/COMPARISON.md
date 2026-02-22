# 🔬 Generic Agent vs Personality Agent

## The Task: Code Review

**User prompt:** "Review this function and tell me what's wrong"

```python
def get_user(id):
    user = db.query(f"SELECT * FROM users WHERE id = {id}")
    if user:
        return user
    return None
```

---

## ❌ Generic Agent Response

> "This function has a potential SQL injection vulnerability. The `id` parameter is directly interpolated into the SQL query string, which could allow malicious input. Consider using parameterized queries instead.
>
> Additionally, the function returns `None` when no user is found, which is acceptable but you might want to consider raising an exception for better error handling.
>
> Overall, the code is functional but could be improved for security and robustness."

**Problems:**
- ✓ Technically correct
- ✗ Forgettable
- ✗ No personality
- ✗ Won't change your behavior

---

## ✅ Dr. House (INTP 5w4 sp/sx) Response

> "Oh look, a SQL injection waiting to happen. Did you copy this from a 2003 tutorial?
>
> Let me diagnose this corpse:
>
> **Critical:** You're concatenating user input directly into SQL. Congratulations, you've just given every script kiddie on the internet the keys to your database. This isn't a bug—it's an invitation.
>
> **Secondary symptom:** That `if user` check. What happens when `user` is an empty list? Right. You return `None` when you should be returning an empty list. Inconsistent return types. Classic.
>
> **The cure:**
> ```python
> def get_user(id: int) -> Optional[User]:
>     return db.query("SELECT * FROM users WHERE id = ?", (id,)).first()
> ```
>
> Type hints. Parameterized query. Single line. It's not rocket surgery.
>
> *Next patient.*"

**Why it works:**
- ✓ Same technical content
- ✓ **Memorable** — you won't forget this review
- ✓ **Consistent voice** — House is House
- ✓ **Actually changes behavior** — shame is a powerful teacher

---

## The Difference

| Aspect | Generic | Dr. House |
|--------|---------|-----------|
| Accuracy | ✅ | ✅ |
| Engagement | 😐 | 🔥 |
| Memorability | Low | **High** |
| Behavior change | Unlikely | **Likely** |
| Personality | None | INTP 5w4 |
| Consistency | Random | **Predictable** |

---

## More Examples

### Gordon Ramsay (ENTJ 8w7) — Project Management

**Generic:** "The deadline was missed due to scope creep. Consider better planning."

**Ramsay:** "This project is RAWWW! Three weeks late and you're telling me about 'scope creep'? The scope didn't creep—your planning was DEAD ON ARRIVAL. Where's the accountability? WHO signed off on these changes? Get your mise en place together or GET OUT OF THE KITCHEN!"

---

### Sherlock Holmes (INTP 5w6) — Bug Investigation

**Generic:** "The bug appears to be related to a race condition in the async handler."

**Holmes:** "Observe the timestamps. 14:23:01.003 and 14:23:01.004. One millisecond. The handler fires before the lock is acquired—elementary, but the evidence was always there. You were looking at the wrong logs. The game, as they say, is afoot. Though in this case, it's already solved."

---

### The Joker (ENTP 7w8) — Creative Brainstorming

**Generic:** "Here are some ideas for the marketing campaign..."

**Joker:** "Why so SERIOUS? You want a marketing campaign? Let's put a SMILE on their faces. Burn the old playbook. What if—and hear me out—what if we make them *uncomfortable* first? Chaos is a ladder, and comfort is death. Give me something that makes the CEO sweat. THAT'S how you get attention."

---

## Try It Yourself

```bash
# Generate a Dr. House agent
python agent_generator.py "INTP 5w4 sp/sx" --name "House" --lang en

# Generate Gordon Ramsay
python agent_generator.py "ENTJ 8w7 so/sx" --name "Ramsay" --lang en

# Generate Sherlock
python agent_generator.py "INTP 5w6 sp/sx" --name "Sherlock" --lang en
```

**The difference isn't just style. It's consistency, memorability, and impact.**

---

*From robots to people. One command.*

🔗 [github.com/gitsual/creador-de-personajes](https://github.com/gitsual/creador-de-personajes)
