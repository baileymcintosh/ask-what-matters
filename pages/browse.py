"""
Browse Properties — Prospective Guest View
2026 Wharton Hack-AI-thon | Presented by Expedia Group

Lets prospective travelers browse recent reviews and submit questions/uncertainties
about a property. Their questions feed back as demand weights into the reviewer TWTK panel.
"""

import streamlit as st
import pandas as pd

from utils import (
    load_data, load_questions, save_question, wipe_user_questions,
    get_demand_scores, analyze_property, nudge_intro,
    classify_question_topic,
    prop_info, prop_dropdown_label, logo_img_tag,
    TOPICS, TOPIC_ICON_MAP,
)

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Browse Properties | Expedia",
    page_icon="🔍",
    layout="centered",
)

# ── CSS (matches reviewer page) ───────────────────────────────────────────────

st.markdown("""
<style>
  html, body, .stApp { background: #0D1021 !important; color: #EEF2FF; }

  .topbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 56px;
    background: #ffffff;
    border-bottom: 1px solid #e8e8e8;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 2rem;
    z-index: 9999;
  }
  .topbar-nav {
    display: flex;
    gap: 1.75rem;
    font-size: 0.84rem;
    color: #555;
  }
  .topbar-nav span { cursor: pointer; transition: color 0.15s; }
  .topbar-nav span:hover { color: #1B2259; }

  .block-container {
    padding-top: 5rem !important;
    padding-bottom: 4rem !important;
    max-width: 860px !important;
  }

  .page-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #EEF2FF;
    margin: 0 0 0.3rem;
    line-height: 1.2;
  }
  .page-subtitle {
    font-size: 0.92rem;
    color: #7B87AB;
    margin: 0 0 2rem;
  }
  .section-label {
    font-size: 0.88rem;
    font-weight: 600;
    color: #C5CCDF;
    margin: 1.5rem 0 0.5rem;
  }

  .prop-banner {
    background: #161B33;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin: 1.25rem 0 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .prop-name { font-size: 1.05rem; font-weight: 700; color: #EEF2FF; margin: 0 0 0.25rem; }
  .prop-sub  { font-size: 0.82rem; color: #7B87AB; }
  .prop-score {
    background: #FFD700;
    color: #0D1021;
    border-radius: 10px;
    padding: 0.55rem 0.9rem;
    text-align: center;
    min-width: 60px;
    flex-shrink: 0;
  }
  .prop-score strong { display: block; font-size: 1.2rem; font-weight: 800; }
  .prop-score small  { font-size: 0.68rem; font-weight: 600; opacity: 0.75; }

  /* Review cards */
  .review-card {
    background: #161B33;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 1rem 1.15rem;
    margin-bottom: 0.75rem;
  }
  .review-meta {
    font-size: 0.76rem;
    color: #7B87AB;
    margin-bottom: 0.4rem;
  }
  .review-rating {
    display: inline-block;
    background: #FFD700;
    color: #0D1021;
    font-weight: 700;
    font-size: 0.76rem;
    border-radius: 6px;
    padding: 0.1rem 0.45rem;
    margin-right: 0.5rem;
  }
  .review-text {
    font-size: 0.87rem;
    color: #C5CCDF;
    line-height: 1.6;
  }

  /* Nudge panel */
  .nudge-panel {
    background: #161B33;
    border: 1px solid rgba(255,255,255,0.08);
    border-top: 3px solid #FFD700;
    border-radius: 12px;
    padding: 1.15rem 1.25rem;
    margin-top: 0.5rem;
  }
  .nudge-panel h4 {
    margin: 0 0 0.3rem;
    font-size: 0.68rem;
    color: #FFD700;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    font-weight: 700;
  }
  .nudge-intro {
    font-size: 0.86rem;
    color: #9BA7C5;
    margin: 0 0 0.9rem;
    line-height: 1.5;
  }
  .topic-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.6rem 0;
    border-top: 1px solid rgba(255,255,255,0.06);
    font-size: 0.86rem;
    color: #C5CCDF;
  }
  .topic-left { display: flex; align-items: center; gap: 0.5rem; }
  .topic-badge {
    font-size: 0.68rem;
    color: #7B87AB;
    background: rgba(255,255,255,0.06);
    border-radius: 999px;
    padding: 0.15rem 0.5rem;
    white-space: nowrap;
  }
  .topic-badge.contested { color: #F59E0B; background: rgba(245,158,11,0.12); }
  .topic-badge.demand    { color: #A78BFA; background: rgba(167,139,250,0.12); }

  /* Questions panel */
  .q-panel {
    background: #161B33;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    margin-top: 1rem;
  }
  .q-panel h4 {
    margin: 0 0 0.75rem;
    font-size: 0.68rem;
    color: #A78BFA;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    font-weight: 700;
  }
  .q-row {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.45rem 0;
    border-top: 1px solid rgba(255,255,255,0.06);
    font-size: 0.84rem;
    color: #C5CCDF;
    line-height: 1.5;
  }
  .q-icon { flex-shrink: 0; font-size: 0.9rem; margin-top: 0.05rem; }
  .q-source {
    font-size: 0.7rem;
    color: #4A5270;
    margin-left: auto;
    white-space: nowrap;
    padding-left: 0.5rem;
  }

  /* Submission form */
  .submit-panel {
    background: #111627;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    margin-top: 1.5rem;
  }
  .submit-panel h4 {
    margin: 0 0 0.6rem;
    font-size: 0.92rem;
    font-weight: 700;
    color: #EEF2FF;
  }
  .submit-hint {
    font-size: 0.82rem;
    color: #7B87AB;
    margin: 0 0 0.8rem;
    line-height: 1.5;
  }

  [data-testid="stTextArea"] textarea {
    background: #161B33 !important;
    color: #EEF2FF !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
  }
  [data-testid="stTextArea"] textarea:focus {
    border-color: #A78BFA !important;
    box-shadow: 0 0 0 2px rgba(167,139,250,0.15) !important;
  }
  [data-testid="stTextArea"] textarea::placeholder { color: #3D4866 !important; }

  [data-baseweb="select"] > div {
    background: #111627 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #EEF2FF !important;
  }
  [data-baseweb="select"] * { color: #EEF2FF !important; }
  [data-baseweb="popover"] { background: #161B33 !important; }
  [role="option"] { background: #161B33 !important; }
  [role="option"]:hover { background: #1C2240 !important; }

  .stButton button {
    background: #FFD700 !important;
    color: #0D1021 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    padding: 0.65rem 1.5rem !important;
    width: 100% !important;
    transition: background 0.15s !important;
  }
  .stButton button:hover { background: #f0ca00 !important; }

  /* Danger/wipe button override */
  .wipe-btn button {
    background: rgba(255,255,255,0.04) !important;
    color: #7B87AB !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
  }
  .wipe-btn button:hover {
    background: rgba(239,68,68,0.12) !important;
    color: #FCA5A5 !important;
    border-color: rgba(239,68,68,0.3) !important;
  }

  label, .stMarkdown p { color: #C5CCDF !important; }
  [data-testid="stAlert"] {
    background: rgba(52,211,153,0.08) !important;
    border-color: rgba(52,211,153,0.25) !important;
    color: #C5CCDF !important;
    border-radius: 10px !important;
  }
  ul[data-testid="stSelectboxVirtualDropdown"] { background: #161B33 !important; }
  #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Data ──────────────────────────────────────────────────────────────────────

desc_df, reviews_df = load_data()
prop_ids = desc_df["eg_property_id"].tolist()

# ── Fixed top bar ─────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="topbar">
  {logo_img_tag(28)}
  <div class="topbar-nav">
    <span>Stays</span><span>Flights</span><span>Cars</span><span>My Trips</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────────────────────

st.markdown('<p class="page-title">Browse a property</p>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Read what guests have said — and flag anything you\'re still unsure about.</p>', unsafe_allow_html=True)

# ── Property selector ─────────────────────────────────────────────────────────

selected_id = st.selectbox(
    "Property",
    prop_ids,
    format_func=lambda pid: prop_dropdown_label(pid, desc_df),
    label_visibility="collapsed",
)

info = prop_info(selected_id, desc_df)

st.markdown(f"""
<div class="prop-banner">
  <div>
    <p class="prop-name">{info.get("name", "Selected property")}</p>
    <p class="prop-sub">{info.get("location", "")}</p>
  </div>
  <div class="prop-score">
    <strong>{info.get("rating", "—")}</strong>
    <small>/ 10</small>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Load demand data ──────────────────────────────────────────────────────────

questions_df  = load_questions()
demand_scores = get_demand_scores(selected_id, questions_df)
demand_tuple  = tuple(sorted(demand_scores.items()))

# ── Two-column layout ─────────────────────────────────────────────────────────

col_reviews, col_panel = st.columns([3, 2], gap="large")

# ── Left: Recent reviews ──────────────────────────────────────────────────────

with col_reviews:
    st.markdown('<p class="section-label">Recent guest reviews</p>', unsafe_allow_html=True)

    prop_reviews = (
        reviews_df[reviews_df["eg_property_id"] == selected_id]
        .dropna(subset=["acquisition_date"])
        .sort_values("acquisition_date", ascending=False)
        .head(10)
    )

    if prop_reviews.empty:
        st.markdown('<p style="color:#7B87AB;font-size:0.88rem;">No reviews yet for this property.</p>', unsafe_allow_html=True)
    else:
        for _, rev in prop_reviews.iterrows():
            # Extract numeric overall rating
            rating_val = ""
            try:
                rp = rev.get("rating_parsed", {})
                if isinstance(rp, dict):
                    overall = rp.get("overall", rp.get("Overall", ""))
                    if overall:
                        rating_val = f"{float(overall):.0f}"
            except Exception:
                pass

            date_str = ""
            try:
                date_str = pd.to_datetime(rev["acquisition_date"]).strftime("%b %Y")
            except Exception:
                pass

            text = str(rev.get("review_text", "")).strip()
            if not text or text.lower() in ("nan", "none"):
                continue

            # Truncate long reviews
            display_text = text if len(text) <= 300 else text[:297] + "…"

            meta_parts = []
            if rating_val:
                meta_parts.append(f'<span class="review-rating">{rating_val} / 10</span>')
            if date_str:
                meta_parts.append(date_str)
            meta_html = "".join(meta_parts)

            st.markdown(f"""
<div class="review-card">
  <div class="review-meta">{meta_html}</div>
  <div class="review-text">{display_text}</div>
</div>
""", unsafe_allow_html=True)

# ── Right: TWTK + Questions panel ────────────────────────────────────────────

with col_panel:
    # TWTK widget (demand-weighted)
    with st.spinner("Loading insights…"):
        gaps = analyze_property(selected_id, demand=demand_tuple)

    if gaps:
        city       = info.get("city", "this property") or "this property"
        gap_labels = tuple(g["label"] for g in gaps)
        intro      = nudge_intro(city, gap_labels)

        rows_html = ""
        for gap in gaps:
            has_demand = demand_scores.get(gap["label"], 0.0) > 0
            if gap.get("type") == "contested":
                badge_css, badge = "topic-badge contested", "Mixed reviews"
            elif has_demand:
                badge_css, badge = "topic-badge demand", "Travelers asking"
            else:
                badge_css, badge = "topic-badge", "Not documented"

            rows_html += (
                f'<div class="topic-row">'
                f'  <div class="topic-left"><span>{gap["icon"]}</span>'
                f'    <span>{gap["label"][0].upper() + gap["label"][1:]}</span></div>'
                f'  <span class="{badge_css}">{badge}</span>'
                f'</div>'
            )

        st.markdown(f"""
<div class="nudge-panel">
  <h4>Travelers want to know</h4>
  <p class="nudge-intro">{intro}</p>
  {rows_html}
</div>
""", unsafe_allow_html=True)

    # Questions already submitted for this property
    prop_questions = questions_df[questions_df["eg_property_id"] == selected_id]

    if not prop_questions.empty:
        q_rows_html = ""
        for _, q in prop_questions.iterrows():
            topic_icon = TOPIC_ICON_MAP.get(q.get("topic", ""), "❓")
            source_label = "your question" if q.get("source") == "user" else ""
            source_html  = f'<span class="q-source">{source_label}</span>' if source_label else ""
            q_rows_html += (
                f'<div class="q-row">'
                f'  <span class="q-icon">{topic_icon}</span>'
                f'  <span>{q["question"]}</span>'
                f'  {source_html}'
                f'</div>'
            )

        st.markdown(f"""
<div class="q-panel">
  <h4>Questions travelers have asked</h4>
  {q_rows_html}
</div>
""", unsafe_allow_html=True)

# ── Question submission ───────────────────────────────────────────────────────

st.markdown('<div class="submit-panel">', unsafe_allow_html=True)
st.markdown('<h4 style="color:#EEF2FF;font-size:0.92rem;font-weight:700;margin:0 0 0.4rem;">Something giving you pause?</h4>', unsafe_allow_html=True)
st.markdown('<p class="submit-hint">Ask anything you couldn\'t find in the reviews. Your question gets passed on anonymously to help future reviewers know what to address.</p>', unsafe_allow_html=True)

question_input = st.text_area(
    "",
    placeholder="e.g. Is it easy to get a taxi late at night from here?",
    height=90,
    label_visibility="collapsed",
    key="question_input",
)

if st.button("Submit question →", use_container_width=True):
    q = question_input.strip()
    if not q:
        st.warning("Please write a question first.")
    elif len(q) < 10:
        st.warning("Please write a more complete question.")
    else:
        with st.spinner("Filing your question…"):
            topic = classify_question_topic(q)
        save_question(selected_id, q, topic)
        st.success(f"Question saved under **{topic}**. It will help shape what reviewers are nudged to cover.")
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ── Demo controls ─────────────────────────────────────────────────────────────

st.write("")
st.markdown("---")
st.markdown('<p style="font-size:0.8rem;color:#4A5270;margin-bottom:0.5rem;">Demo controls</p>', unsafe_allow_html=True)

n_user_questions = len(questions_df[questions_df["source"] == "user"])
st.markdown(
    f'<p style="font-size:0.82rem;color:#7B87AB;">'
    f'{n_user_questions} user-submitted question{"s" if n_user_questions != 1 else ""} on record '
    f'(seed questions are preserved).</p>',
    unsafe_allow_html=True,
)

st.markdown('<div class="wipe-btn">', unsafe_allow_html=True)
if st.button("Wipe user questions", use_container_width=True):
    n = wipe_user_questions()
    st.success(f"Cleared {n} user-submitted question{'s' if n != 1 else ''}. Seed data is intact.")
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
