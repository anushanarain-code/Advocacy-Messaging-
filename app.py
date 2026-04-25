import streamlit as st
import numpy as np
import random

st.set_page_config(
    page_title="AMIS — Messaging Intelligence",
    layout="wide"
)

st.set_page_config(layout="wide")

# -----------------------------
# 🧠 HEADER
# -----------------------------
st.title("🧠 AMIS v10.2 — Advocacy Messaging Intelligence System")

st.markdown("""
### What this tool does:
- Analyzes advocacy messages using persuasion theory  
- Identifies argument type, function, and strength  
- Explains **how and why** a message is strong or weak  
- Suggests clear strategic improvements  

### Core idea:
This is **not a content generator**.  
It is a **decision intelligence tool for improving messaging**.
""")

# -----------------------------
# 📚 THEORY BLOCK
# -----------------------------
with st.expander("📚 Understanding Message Framing"):

    st.markdown("""
**Moral Framing**  
Uses ideas of right/wrong, justice, compassion.  
✔ Strong for mobilisation  
⚠ Can trigger resistance  

**Evidence Framing**  
Uses data, statistics, research.  
✔ Builds credibility  
✔ Strong for broad persuasion  

**Narrative Framing**  
Uses stories or lived experience  
✔ Reduces resistance  
✔ Improves relatability  
""")

# -----------------------------
# INPUT
# -----------------------------
message = st.text_area("✍️ Enter your message")

# -----------------------------
# OPTIONAL FUTURE LAYER
# -----------------------------
with st.expander("📊 Optional: Campaign Context (Future Layer)"):

    platform = st.selectbox("Platform", ["Twitter/X", "Instagram", "LinkedIn"])
    post_type = st.selectbox("Post Type", ["Text", "Thread", "Video"])
    engagement = st.number_input("Engagement", min_value=0, value=0)

    st.caption("Not used in scoring yet — future analytics layer")
# -----------------------------
# SIGNAL EXTRACTION (NEW CORE LAYER)
# -----------------------------
def extract_signals(text):
    t = text.lower()
    words = t.split()

    # LENGTH
    length = len(words)

    # INTENSITY (simple proxy)
    intensity = 0
    if "!" in text:
        intensity += 1
    if any(w.isupper() for w in text.split()):
        intensity += 1
    if length < 10:
        intensity += 1  # short = punchy/emotional

    # STRUCTURE SIGNALS
    has_numbers = any(c.isdigit() for c in text)
    has_reasoning = any(w in t for w in ["because", "therefore", "leads", "causes"])
    has_moral = any(w in t for w in ["should", "must"])

    # QUESTION
    is_question = "?" in text

    return {
        "length": length,
        "intensity": intensity,
        "has_numbers": has_numbers,
        "has_reasoning": has_reasoning,
        "has_moral": has_moral,
        "is_question": is_question
    }

# -----------------------------
# ARGUMENT TYPE
# -----------------------------
def argument_type(text):

    s = extract_signals(text)

    if s["is_question"]:
        return "Rhetorical"

    if s["has_numbers"]:
        return "Evidence-led"

    if s["has_moral"]:
        return "Moral"

    if s["intensity"] >= 2 and s["length"] < 12:
        return "High-intensity claim"

    if s["length"] > 15:
        return "Narrative / descriptive"

    return "Basic claim"

# -----------------------------
# FUNCTION (UPGRADED)
# -----------------------------
def message_function(text):

    s = extract_signals(text)

    # Emotional alarm (urgent, punchy, no reasoning)
    if s["intensity"] >= 2 and not s["has_reasoning"]:
        return "Emotional alarm / attention trigger"

    if s["is_question"]:
        return "Challenge to existing beliefs"

    if s["has_moral"]:
        return "Mobilisation of moral concern"

    if s["has_numbers"] or s["has_reasoning"]:
        return "Persuasion through reasoning"

    return "Basic awareness statement"

# -----------------------------
# COMPONENT SCORING + EXPLANATION
# -----------------------------
def evidence_score(text):
    numbers = sum(c.isdigit() for c in text)
    research = sum(w in text.lower() for w in ["study", "research", "analysis"])

    score = min(100, numbers * 5 + research * 20)

    explanation = f"""
- Numerical references found: {numbers}  
- Research signals found: {research}  
- Scoring logic: (numbers × 5) + (research × 20)
"""

    return score, explanation

def logic_score(text):
    t = text.lower()

    cause = sum(w in t for w in ["because", "therefore"])
    conditional = sum(w in t for w in ["if"])
    contrast = sum(w in t for w in ["but", "however"])

    score = min(100, (cause + conditional + contrast) * 25)

    explanation = f"""
- Cause-effect links: {cause}  
- Conditional reasoning: {conditional}  
- Contrast framing: {contrast}  
- Scoring logic: (total × 25)
"""

    return score, explanation

def moral_score(text):
    t = text.lower()

    moral_terms = sum(w in t for w in ["right", "justice", "compassion", "should", "must", "cruel", "suffer", "harm", "pain"])

    score = min(100, moral_terms * 20)

    explanation = f"""
- Moral terms detected: {moral_terms}  
- Examples: right, justice, compassion, should, must  
- Scoring logic: (terms × 20)
"""

    return score, explanation

# -----------------------------
# ACTION SCORE (NEW)
# -----------------------------
# -----------------------------
# ACTION SCORE (REFINED)
# -----------------------------
def action_score(text):
    t = text.lower()

    # Strong, specific actions
    strong_actions = ["sign", "join", "support", "boycott", "demand", "donate", "vote"]

    # Weak / vague actions
    weak_actions = ["stop", "act", "change", "help"]

    strong_count = sum(w in t for w in strong_actions)
    weak_count = sum(w in t for w in weak_actions)

    score = strong_count * 30 + weak_count * 10
    score = min(100, score)

    explanation = f"""
- Strong action cues: {strong_count} (e.g. sign, support, boycott)  
- Weak action cues: {weak_count} (e.g. stop, act, change)  
- Scoring logic: (strong × 30) + (weak × 10)
"""

    return score, explanation

def cognitive_load(text):
    sentences = text.split(".")
    lengths = [len(s.split()) for s in sentences if s.strip()]
    avg = np.mean(lengths) if lengths else 0

    if avg < 12:
        level = "LOW"
    elif avg < 20:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return level, avg
# -----------------------------
# STRUCTURE GAP DETECTION (NEW)
# -----------------------------
def missing_structure(e, l, m):
    missing = []

    if e < 20:
        missing.append("evidence")

    if l < 20:
        missing.append("reasoning")

    if m < 20:
        missing.append("moral")

    return missing
# -----------------------------
# FINAL SCORE
# -----------------------------
def final_score(func, e, l, m, a):

    if "Mobilisation" in func:
        score = 0.4*m + 0.2*l + 0.2*e + 0.2*a

    elif "Persuasion" in func:
        score = 0.35*e + 0.35*l + 0.15*m + 0.15*a

    elif "Challenge" in func:
        score = 0.4*l + 0.3*m + 0.2*e + 0.1*a

    else:
        score = (e + l + m + a) / 4

    return int(score)

# -----------------------------
# INTERPRETATION
# -----------------------------
def interpret(score):

    if score < 30:
        return "Weak — lacks structure, clarity, or persuasive depth."

    elif score < 50:
        return "Moderate — some persuasive elements present but incomplete."

    elif score < 80:
        return "Strong — likely effective with the intended audience."

    return "Very strong — high persuasion potential."

# -----------------------------
# WHY THIS SCORE (KEY FEATURE)
# -----------------------------
def explain_score(func, e, l, m):

    if "Mobilisation" in func:
        return "This score is driven primarily by moral pressure. Low logic and evidence reduce overall effectiveness."

    if "Persuasion" in func:
        return "This score depends on both evidence and logical structure. Weakness in either reduces impact."

    if "Challenge" in func:
        return "Challenge messages rely on reasoning and contrast. Lack of logic weakens persuasive force."

    return "This is an informational message with balanced but limited persuasive elements."

# -----------------------------
# GAP DETECTION (NEW)
# -----------------------------
def detect_gaps(e, l, m):
    gaps = []

    if e < 20:
        gaps.append("evidence")

    if l < 20:
        gaps.append("logic")

    if m < 20:
        gaps.append("moral")

    return gaps

# -----------------------------
# STRATEGY MOVES
# -----------------------------
def strategy(func, e, l, m, text):

    import random

    moves = []

    # -----------------------------
    # 1. MORAL-HEAVY BUT STRUCTURALLY WEAK
    # -----------------------------
    if m > 40 and e < 20 and l < 20:

        fact_prompts = [
            "👉 Add ONE concrete fact to support this claim",
            "👉 Anchor this with a statistic or real-world number",
            "👉 Add a verifiable data point to increase credibility"
        ]

        reason_prompts = [
            "👉 Explain WHY this is happening (cause or system)",
            "👉 Add cause-effect logic: what leads to this?",
            "👉 Clarify the mechanism behind this issue"
        ]

        action_prompts = [
            "👉 Add a clear next step: what should the audience do?",
            "👉 Tell the audience exactly what action to take",
            "👉 Convert this into a call to action"
        ]

        moves.append(random.choice(fact_prompts))
        moves.append(random.choice(reason_prompts))
        moves.append(random.choice(action_prompts))

    # -----------------------------
    # 2. PERSUASION MODE
    # -----------------------------
    elif "Persuasion" in func:

        if e < 40:
            moves.append("👉 Add a specific data point or study to strengthen credibility")

        if l < 40:
            moves.append("👉 Strengthen cause-effect reasoning (use 'because', 'this leads to')")

    # -----------------------------
    # 3. MOBILISATION MODE
    # -----------------------------
    elif "Mobilisation" in func:

        if l < 30:
            moves.append("👉 The message lacks reasoning after the moral claim, which may reduce persuasive impact")

        if e < 20:
            moves.append("👉 The message lacks external credibility (data, policy, expert reference)")

    # ✅ ADD ACTION GAP
            moves.append("👉 The message does not specify what the audience should do next (e.g. boycott, support policy, sign, share)")

    # -----------------------------
    # 4. CHALLENGE MODE
    # -----------------------------
    elif "Challenge" in func:

        if l < 30:
            moves.append("👉 The message lacks reasoning, which weakens persuasive impact")

    # -----------------------------
    # 5. FALLBACK — STRUCTURE-BASED
    # -----------------------------
    if not moves:

        if e < 20:
            moves.append("👉 Add a concrete fact or number to anchor the claim")

        if l < 20:
            moves.append("👉 Explain why this is happening or why it matters")

        if m < 20:
            moves.append("👉 Clarify why this is important or morally relevant")

        if not moves:
            moves.append("👉 Add a clear action: what should the audience do next?")

    return moves
# -----------------------------
# MAIN
# -----------------------------
if message:

    arg = argument_type(message)
    func = message_function(message)

    e, e_exp = evidence_score(message)
    l, l_exp = logic_score(message)
    m, m_exp = moral_score(message)
    a, a_exp = action_score(message)
    load, avg_len = cognitive_load(message)

    score = final_score(func, e, l, m,a)

    # -----------------------------
    # DISPLAY
    # -----------------------------
    st.subheader("🧠 Message Analysis")
    st.write(f"**Argument Type:** {arg}")
    st.write(f"**Function:** {func}")

    st.subheader("📊 Component Breakdown")
    st.caption("This tool evaluates message strength across four dimensions: evidence, logic, moral framing, and action clarity.")

    with st.expander("Evidence Strength"):
        st.write(f"Score: {e}/100")
        st.markdown(e_exp)

    with st.expander("Logic Structure"):
        st.write(f"Score: {l}/100")
        st.markdown(l_exp)

    with st.expander("Moral Pressure"):
        st.write(f"Score: {m}/100")
        st.markdown(m_exp)

    with st.expander("Action Clarity"):
        st.write(f"Score: {a}/100")
        st.markdown(a_exp)

    st.write(f"**Cognitive Load:** {load} (avg sentence length: {round(avg_len,1)} words)")

    st.subheader("🔥 Final Strength Score")
    st.metric("Persuasion Strength", f"{score}/100")

    st.write(f"🧠 **Interpretation:** {interpret(score)}")

    st.subheader("🔍 Why this score?")
    st.write(explain_score(func, e, l, m))

    st.subheader("🧭 Strategic Moves")
    for move in strategy(func, e, l, m, message):
        st.write(move)

else:
    st.info("Enter a message to begin analysis")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Developed by Anusha Narain as part of the Ahimsa Fellowship")
