import streamlit as st
import numpy as np

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
# ARGUMENT TYPE
# -----------------------------
def argument_type(text):
    t = text.lower()

    if "?" in text:
        return "Rhetorical"

    if any(w in t for w in ["%", "study", "research", "data"]):
        return "Evidence-led"

    if any(w in t for w in ["right", "justice", "freedom", "compassion"]):
        return "Moral"

    return "General"

# -----------------------------
# FUNCTION (UPGRADED)
# -----------------------------
def message_function(text):
    t = text.lower()

    if "?" in text:
        return "Challenge to existing beliefs or norms"

    if any(w in t for w in ["right", "justice", "freedom", "compassion"]):
        return "Mobilisation of moral concern and public reaction"

    if any(w in t for w in ["data", "%", "study"]):
        return "Persuasion through evidence and reasoning"

    return "Informational awareness building"

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

    moral_terms = sum(w in t for w in ["right", "justice", "compassion", "should", "must"])

    score = min(100, moral_terms * 20)

    explanation = f"""
- Moral terms detected: {moral_terms}  
- Examples: right, justice, compassion, should, must  
- Scoring logic: (terms × 20)
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
# FINAL SCORE
# -----------------------------
def final_score(func, e, l, m):

    if "Mobilisation" in func:
        score = 0.6*m + 0.2*l + 0.2*e

    elif "Persuasion" in func:
        score = 0.4*e + 0.4*l + 0.2*m

    elif "Challenge" in func:
        score = 0.5*l + 0.3*m + 0.2*e

    else:
        score = (e + l + m) / 3

    return int(score)

# -----------------------------
# INTERPRETATION
# -----------------------------
def interpret(score):

    if score < 30:
        return "Weak — lacks structure, clarity, or persuasive depth."

    elif score < 60:
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
# STRATEGY MOVES
# -----------------------------
def strategy(func, e, l, m):

    moves = []

    if "Mobilisation" in func:
        if l < 30:
            moves.append("👉 Add reasoning: explain why the issue matters")
        if e < 20:
            moves.append("👉 Add legitimacy: reference law, authority, or facts")

    if "Persuasion" in func:
        if e < 40:
            moves.append("👉 Add data or research evidence")
        if l < 40:
            moves.append("👉 Improve cause-effect clarity")

    if "Challenge" in func:
        if l < 30:
            moves.append("👉 Add reasoning after the question")

    if not moves:
        moves.append("✅ Message is structurally strong")

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
    load, avg_len = cognitive_load(message)

    score = final_score(func, e, l, m)

    # -----------------------------
    # DISPLAY
    # -----------------------------
    st.subheader("🧠 Message Analysis")
    st.write(f"**Argument Type:** {arg}")
    st.write(f"**Function:** {func}")

    st.subheader("📊 Component Breakdown")

    with st.expander("Evidence Strength"):
        st.write(f"Score: {e}/100")
        st.markdown(e_exp)

    with st.expander("Logic Structure"):
        st.write(f"Score: {l}/100")
        st.markdown(l_exp)

    with st.expander("Moral Pressure"):
        st.write(f"Score: {m}/100")
        st.markdown(m_exp)

    st.write(f"**Cognitive Load:** {load} (avg sentence length: {round(avg_len,1)} words)")

    st.subheader("🔥 Final Strength Score")
    st.metric("Persuasion Strength", f"{score}/100")

    st.write(f"🧠 **Interpretation:** {interpret(score)}")

    st.subheader("🔍 Why this score?")
    st.write(explain_score(func, e, l, m))

    st.subheader("🧭 Strategic Moves")
    for move in strategy(func, e, l, m):
        st.write(move)

else:
    st.info("Enter a message to begin analysis")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Developed by Anusha Narain as part of the Ahimsa Fellowship")