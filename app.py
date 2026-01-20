import streamlit as st


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="News Authenticity Checker",
    page_icon="📰",
    layout="centered"
)

# ---------------- TITLE ----------------
st.title("📰 News Authenticity Checker")
st.caption("Advanced, explainable fake news analysis tool")

st.markdown("---")

# ---------------- USER STRICTNESS ----------------
strictness = st.slider(
    "🔧 Detection Strictness",
    min_value=1,
    max_value=5,
    value=3,
    help="Higher value = stricter fake detection"
)

# ---------------- INPUT ----------------
news_text = st.text_area(
    "📌 Paste news text here",
    height=220,
    placeholder="Paste full news article here..."
)

# ---------------- RULE SET ----------------
fake_keywords = [
    "shocking", "breaking", "exposed", "secret", "viral",
    "you won't believe", "must watch", "bloodbath",
    "conspiracy", "hoax", "rumor", "fake"
]

trusted_terms = [
    "according to", "reported by", "official", "statement",
    "confirmed", "data shows", "research", "source said"
]

# ---------------- ANALYSIS ----------------
if st.button("🔍 Analyze News"):
    if news_text.strip() == "":
        st.warning("⚠️ Please paste some news text first")
    else:
        text = news_text.lower()
        words = news_text.split()

        score = 0
        checks = {}

        # Rule 1: Length
        if len(words) < 80:
            score += 2
            checks["Sufficient Length"] = False
        else:
            checks["Sufficient Length"] = True

        # Rule 2: Sensational keywords
        fake_hit = any(w in text for w in fake_keywords)
        if fake_hit:
            score += 3
            checks["Sensational Language"] = False
        else:
            checks["Sensational Language"] = True

        # Rule 3: Trusted language
        real_hit = any(w in text for w in trusted_terms)
        if real_hit:
            score -= 2
            checks["Credible Language"] = True
        else:
            checks["Credible Language"] = False

        # Rule 4: Capital letters
        caps_ratio = sum(1 for c in news_text if c.isupper()) / max(len(news_text), 1)
        if caps_ratio > 0.08:
            score += 1
            checks["Neutral Tone"] = False
        else:
            checks["Neutral Tone"] = True

        # Rule 5: Emotional punctuation
        if "!" in news_text or "?" in news_text:
            score += 1
            checks["Emotional Punctuation"] = False
        else:
            checks["Emotional Punctuation"] = True

        # ---------------- STRICTNESS ADJUST ----------------
        score = score + (strictness - 3)

        # ---------------- FINAL DECISION ----------------
        st.markdown("---")

        if score >= 4:
            st.error("❌ HIGHLY LIKELY FAKE NEWS")
            confidence = 85
        elif score >= 2:
            st.warning("⚠️ SUSPICIOUS — Needs Verification")
            confidence = 60
        else:
            st.success("✅ LIKELY REAL NEWS")
            confidence = 80

        st.markdown(f"### 📊 Confidence Score: {confidence}%")
        st.progress(confidence)

        # ---------------- SCORE CARD ----------------
        st.markdown("---")
        st.markdown("### 🧾 Explainability Score Card")

        for check, status in checks.items():
            if status:
                st.write(f"✅ {check}")
            else:
                st.write(f"❌ {check}")

        st.markdown("---")
        st.info(
            "ℹ️ This system uses a conservative, explainable rule-based approach. "
            "Unverified or emotionally charged content is treated as suspicious by default."
        )


   










