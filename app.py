"""
Ask What Matters — Adaptive AI for Smarter Travel Reviews
2026 Wharton Hack-AI-thon | Presented by Expedia Group
"""

import json
import pandas as pd
import streamlit as st

from utils import (
    load_data, load_questions, save_question, wipe_user_questions, get_demand_scores,
    covered_topics, analyze_property, nudge_intro, classify_question_topic,
    prop_info, prop_dropdown_label, logo_img_tag, property_summary, clean_question,
)

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Expedia",
    page_icon="✈️",
    layout="centered",
)

# ── CSS ───────────────────────────────────────────────────────────────────────

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
    padding: 0 2rem;
    z-index: 9999;
  }

  .block-container {
    padding-top: 5rem !important;
    padding-bottom: 4rem !important;
    max-width: 860px !important;
  }

  /* Nav buttons — small and muted */
  [data-testid="baseButton-secondary"] {
    background: transparent !important;
    color: #4A5270 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 6px !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    padding: 0.2rem 0.6rem !important;
    width: 100% !important;
    white-space: nowrap !important;
  }
  [data-testid="baseButton-secondary"]:hover {
    color: #C5CCDF !important;
    border-color: rgba(255,255,255,0.18) !important;
    background: rgba(255,255,255,0.04) !important;
  }
  /* Main action buttons — gold */
  [data-testid="baseButton-primary"] {
    background: #FFD700 !important;
    color: #0D1021 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    padding: 0.65rem 1.5rem !important;
    width: 100% !important;
  }
  [data-testid="baseButton-primary"]:hover { background: #f0ca00 !important; }

  /* Demo nav */
  .demo-nav .stButton button {
    background: transparent !important;
    color: #4A5270 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 6px !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    padding: 0.2rem 0.7rem !important;
    width: 100% !important;
  }
  .demo-nav .stButton button:hover {
    color: #C5CCDF !important;
    border-color: rgba(255,255,255,0.15) !important;
  }
  .demo-nav .active .stButton button {
    color: #EEF2FF !important;
    border-color: rgba(255,255,255,0.2) !important;
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
    margin: 1.5rem 0 0.3rem;
  }
  .section-hint {
    font-size: 0.82rem;
    color: #7B87AB;
    margin: 0 0 0.6rem;
    line-height: 1.5;
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
  .topic-row.covered { color: #4A5270; }
  .topic-row.covered .topic-name { text-decoration: line-through; }
  .topic-left { display: flex; align-items: center; gap: 0.5rem; }
  .topic-badge {
    font-size: 0.68rem;
    color: #7B87AB;
    background: rgba(255,255,255,0.06);
    border-radius: 999px;
    padding: 0.15rem 0.5rem;
    white-space: nowrap;
  }
  .topic-badge.done      { color: #34D399; background: rgba(52,211,153,0.12); }
  .topic-badge.contested { color: #F59E0B; background: rgba(245,158,11,0.12); }
  .topic-badge.demand    { color: #A78BFA; background: rgba(167,139,250,0.12); }
  .topic-questions {
    margin-top: 0.3rem;
    display: flex;
    flex-direction: column;
    gap: 0.18rem;
  }
  .topic-q {
    font-size: 0.75rem;
    color: #7B87AB;
    line-height: 1.4;
  }
  .topic-row.covered .topic-q { color: #3D4866; }
  .nudge-footer {
    font-size: 0.75rem;
    color: #4A5270;
    margin-top: 0.85rem;
    padding-top: 0.7rem;
    border-top: 1px solid rgba(255,255,255,0.06);
    line-height: 1.45;
  }
  .nudge-footer.all-done { color: #34D399; font-weight: 600; }

  /* Insight card */
  .insight-card {
    background: #161B33;
    border: 1px solid rgba(255,255,255,0.08);
    border-left: 3px solid #FFD700;
    border-radius: 12px;
    padding: 1.25rem 1.35rem;
    margin-top: 1.5rem;
  }
  .insight-card h4 { margin: 0 0 0.7rem; font-size: 0.9rem; font-weight: 700; color: #EEF2FF; }
  .insight-row {
    display: flex;
    align-items: flex-start;
    gap: 0.65rem;
    padding: 0.55rem 0;
    border-top: 1px solid rgba(255,255,255,0.06);
    font-size: 0.86rem;
    color: #C5CCDF;
    line-height: 1.55;
  }
  .insight-icon { flex-shrink: 0; margin-top: 0.1rem; }

  /* Review cards (browse page) */
  .review-card {
    background: #161B33;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 1rem 1.15rem;
    margin-bottom: 0.75rem;
  }
  .review-meta { font-size: 0.76rem; color: #7B87AB; margin-bottom: 0.4rem; }
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
  .review-text { font-size: 0.87rem; color: #C5CCDF; line-height: 1.6; }

  /* Questions panel (browse page) */
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
  .q-source { font-size: 0.7rem; color: #4A5270; margin-left: auto; white-space: nowrap; padding-left: 0.5rem; }

  /* Streamlit widget overrides */
  [data-testid="stTextArea"] textarea {
    background: #111627 !important;
    color: #EEF2FF !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    font-size: 0.93rem !important;
    line-height: 1.6 !important;
  }
  [data-testid="stTextArea"] textarea:focus {
    border-color: #FFD700 !important;
    box-shadow: 0 0 0 2px rgba(255,215,0,0.15) !important;
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

  [data-testid="stSlider"] { padding: 0.25rem 0 0.5rem; }
  [data-testid="stSlider"] [data-testid="stTickBarMin"],
  [data-testid="stSlider"] [data-testid="stTickBarMax"] { color: #7B87AB !important; }


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


# ── LLM helper (reviewer only) ────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def extract_insights(review_text: str, covered_labels: tuple, city: str) -> dict:
    from utils import get_client
    if not covered_labels:
        return {}
    r = get_client().chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content":
            f"Guest reviewed a hotel in {city}:\n\"{review_text}\"\n\n"
            f"For each topic mentioned, write one specific factual sentence (max 12 words).\n"
            f"Topics: {', '.join(covered_labels)}\n"
            f"Return JSON only: {{\"topic\": \"insight\"}}. Omit topics not clearly mentioned."}],
        temperature=0.2, max_tokens=250,
    )
    raw = r.choices[0].message.content.strip().replace("```json","").replace("```","").strip()
    try:
        return json.loads(raw)
    except Exception:
        return {}


# ── Session init ──────────────────────────────────────────────────────────────

desc_df, reviews_df = load_data()

for k, v in [("page", "form"), ("gaps", []), ("prop_id", None),
              ("covered", set()), ("review_text", ""), ("insights", {})]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Startup pre-warm ──────────────────────────────────────────────────────────

if not st.session_state.get("_warmed"):
    _prop_ids = desc_df["eg_property_id"].tolist()
    _bar = st.progress(0, text="Preparing review insights…")
    for _i, _pid in enumerate(_prop_ids):
        try:
            _gaps = analyze_property(_pid)
            if _gaps:
                _info = prop_info(_pid, desc_df)
                _city = _info.get("city", "this property") or "this property"
                nudge_intro(_city, tuple(g["label"] for g in _gaps))
            property_summary(_pid)
        except Exception:
            pass
        _bar.progress((_i + 1) / len(_prop_ids),
                      text=f"Preparing review insights… ({_i + 1}/{len(_prop_ids)})")
    _bar.empty()
    st.session_state["_warmed"] = True


# ── Fixed top bar ─────────────────────────────────────────────────────────────

# ── Topbar ────────────────────────────────────────────────────────────────────

st.markdown(f'<div class="topbar">{logo_img_tag(28)}</div>', unsafe_allow_html=True)

# ── Nav ───────────────────────────────────────────────────────────────────────

_c1, _c2, _ = st.columns([1.6, 1.6, 7])
with _c1:
    if st.button("Review (Feature 1)", use_container_width=True):
        st.session_state.page = "form"
        st.rerun()
with _c2:
    if st.button("Browse (Feature 2)", use_container_width=True):
        st.session_state.page = "browse"
        st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: THANK-YOU
# ═════════════════════════════════════════════════════════════════════════════

if st.session_state.page == "thanks":
    covered  = st.session_state.covered
    insights = st.session_state.insights
    gaps     = st.session_state.gaps

    st.markdown('<p class="page-title">Review submitted ✓</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Your review is now live on Expedia.</p>', unsafe_allow_html=True)

    if covered and insights:
        n = len(covered)
        st.markdown(
            f"You mentioned **{n} topic{'s' if n > 1 else ''}** that fellow travelers "
            f"have been looking for. Here's what your review contributed:"
        )
        icon_map  = {g["label"]: g["icon"] for g in gaps}
        rows_html = "".join(
            f'<div class="insight-row"><span class="insight-icon">{icon_map.get(lbl,"•")}</span>'
            f'<div><strong>{lbl}:</strong>&nbsp;{ins}</div></div>'
            for lbl, ins in insights.items()
        )
        st.markdown(
            f'<div class="insight-card"><h4>What your review added to the listing</h4>{rows_html}</div>',
            unsafe_allow_html=True,
        )
    elif covered:
        st.success(
            f"Your review covered **{', '.join(covered)}** — "
            f"{'a topic' if len(covered) == 1 else 'topics'} other travelers have been asking about."
        )
    else:
        st.info("Your review has been added. Every perspective helps future travelers.")

    st.write("")
    if st.button("Write another review"):
        for k in ["page", "gaps", "prop_id", "covered", "review_text", "insights"]:
            del st.session_state[k]
        st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: BROWSE PROPERTIES
# ═════════════════════════════════════════════════════════════════════════════

elif st.session_state.page == "browse":
    prop_ids = desc_df["eg_property_id"].tolist()

    st.markdown('<p class="page-title">Browse a property</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Read what guests have said — and flag anything you\'re still unsure about.</p>', unsafe_allow_html=True)

    browse_id = st.selectbox(
        "Property",
        prop_ids,
        format_func=lambda pid: prop_dropdown_label(pid, desc_df),
        label_visibility="collapsed",
        key="browse_prop",
    )

    b_info = prop_info(browse_id, desc_df)
    st.markdown(f"""
<div class="prop-banner">
  <div>
    <p class="prop-name">{b_info.get("name", "Selected property")}</p>
    <p class="prop-sub">{b_info.get("location", "")}</p>
  </div>
  <div class="prop-score">
    <strong>{b_info.get("rating", "—")}</strong>
    <small>/ 10</small>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Property summary ──────────────────────────────────────────────────────
    summary = property_summary(browse_id)
    if summary:
        st.markdown(
            f'<p style="font-size:0.86rem;color:#9BA7C5;line-height:1.6;margin:0.25rem 0 1.25rem;">{summary}</p>',
            unsafe_allow_html=True,
        )

    # ── Recent reviews (full width) ───────────────────────────────────────────
    st.markdown('<p class="section-label">Recent guest reviews</p>', unsafe_allow_html=True)

    prop_reviews = (
        reviews_df[reviews_df["eg_property_id"] == browse_id]
        .dropna(subset=["acquisition_date"])
        .sort_values("acquisition_date", ascending=False)
        .head(10)
    )

    if prop_reviews.empty:
        st.markdown('<p style="color:#7B87AB;font-size:0.88rem;">No reviews yet for this property.</p>', unsafe_allow_html=True)
    else:
        for idx, (_, rev) in enumerate(prop_reviews.iterrows()):
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

            is_long      = len(text) > 300
            expand_key   = f"rev_exp_{browse_id}_{idx}"
            is_expanded  = st.session_state.get(expand_key, False)
            display_text = text if (not is_long or is_expanded) else text[:297] + "…"
            rating_html  = f'<span class="review-rating">{rating_val} / 5</span>' if rating_val else ""

            st.markdown(f"""
<div class="review-card">
  <div class="review-meta">{rating_html}{date_str}</div>
  <div class="review-text">{display_text}</div>
</div>
""", unsafe_allow_html=True)

            if is_long:
                btn_label = "Show less ↑" if is_expanded else "Read more ↓"
                if st.button(btn_label, key=f"rev_btn_{browse_id}_{idx}"):
                    st.session_state[expand_key] = not is_expanded
                    st.rerun()

    # ── Submit a question (full width, bottom) ────────────────────────────────
    st.write("")
    st.markdown('<p class="section-label">Still not sure about something?</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-hint">What would you still want to know before booking? We\'ll make sure future guests are prompted to address it in their reviews.</p>', unsafe_allow_html=True)

    if "q_counter" not in st.session_state:
        st.session_state.q_counter = 0

    question_input = st.text_area(
        "",
        placeholder="e.g. Is it easy to get a taxi late at night from here?",
        height=90,
        label_visibility="collapsed",
        key=f"question_input_{st.session_state.q_counter}",
    )

    if st.button("Submit →", use_container_width=True):
        q = question_input.strip()
        if not q:
            st.warning("Please write a question first.")
        elif len(q) < 10:
            st.warning("Please write a more complete question.")
        else:
            with st.spinner("Filing your question…"):
                q = clean_question(q)
                if q is None:
                    st.warning("That question couldn't be saved — please keep it relevant to your hotel stay.")
                    st.stop()
                topic = classify_question_topic(q)
            save_question(browse_id, q, topic)
            st.session_state.q_counter += 1  # clears the text box
            st.success(f"Saved under **{topic}**. Future reviewers will be nudged to cover this.")
            st.rerun()

    # ── Demo wipe ─────────────────────────────────────────────────────────────
    st.write("")
    questions_df = load_questions()
    n_user_q = len(questions_df[questions_df["source"] == "user"])
    wipe_col, _ = st.columns([2, 5])
    with wipe_col:
        st.markdown(
            f'<p style="font-size:0.75rem;color:#4A5270;margin-bottom:0.3rem;">'
            f'{n_user_q} question{"s" if n_user_q != 1 else ""} on record</p>',
            unsafe_allow_html=True,
        )
        st.markdown('<style>.wipe-btn button{background:transparent!important;color:#4A5270!important;border:1px solid rgba(255,255,255,0.07)!important;font-size:0.75rem!important;font-weight:500!important;padding:0.25rem 0.75rem!important;}.wipe-btn button:hover{color:#FCA5A5!important;border-color:rgba(239,68,68,0.3)!important;}</style><div class="wipe-btn">', unsafe_allow_html=True)
        if st.button("Wipe questions", use_container_width=True):
            n = wipe_user_questions()
            st.success(f"Cleared {n} question{'s' if n != 1 else ''}.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: REVIEW FORM
# ═════════════════════════════════════════════════════════════════════════════

else:
    prop_ids = desc_df["eg_property_id"].tolist()

    st.markdown('<p class="page-title">Write a review</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Share your experience and help other travelers choose with confidence.</p>', unsafe_allow_html=True)

    col_form, col_nudge = st.columns([3, 2], gap="large")

    with col_form:
        selected_id = st.selectbox(
            "Property",
            prop_ids,
            format_func=lambda pid: prop_dropdown_label(pid, desc_df),
            label_visibility="collapsed",
        )

        questions_df  = load_questions()
        demand_scores = get_demand_scores(selected_id, questions_df)
        demand_tuple  = tuple(sorted(demand_scores.items()))

        if selected_id != st.session_state.prop_id or demand_tuple != st.session_state.get("_demand_tuple"):
            with st.spinner("Analysing reviews…"):
                st.session_state.gaps = analyze_property(selected_id, demand=demand_tuple)
            st.session_state.prop_id          = selected_id
            st.session_state.covered          = set()
            st.session_state["_demand_tuple"] = demand_tuple

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

        st.markdown('<p class="section-label">Overall rating</p>', unsafe_allow_html=True)
        overall = st.slider("", 1, 10, 8, label_visibility="collapsed")

        st.markdown('<p class="section-label">Your review</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-hint">What stood out about your stay? Specific, recent details are the most helpful to other travelers.</p>', unsafe_allow_html=True)

        review_text = st.text_area(
            "",
            placeholder="e.g. The room was spotless and the location was ideal for getting around the city. Breakfast had a great variety. One thing worth knowing: the rooftop bar closes at 10pm.",
            height=240,
            label_visibility="collapsed",
        )

        st.session_state.covered     = covered_topics(review_text, st.session_state.gaps)
        st.session_state.review_text = review_text

        st.write("")
        if st.button("Post review →", type="primary", use_container_width=True):
            if not review_text.strip():
                st.warning("Please write something before submitting.")
            else:
                covered = st.session_state.covered
                if covered:
                    with st.spinner("Processing your review…"):
                        st.session_state.insights = extract_insights(
                            review_text,
                            tuple(sorted(covered)),
                            info.get("city", "this property"),
                        )
                st.session_state.page = "thanks"
                st.rerun()

    with col_nudge:
        st.markdown("<div style='height:15rem'></div>", unsafe_allow_html=True)

        gaps    = st.session_state.gaps
        covered = st.session_state.covered

        if gaps:
            city       = prop_info(selected_id, desc_df).get("city", "this property") or "this property"
            gap_labels = tuple(g["label"] for g in gaps)
            intro      = nudge_intro(city, gap_labels)
            all_done   = covered >= set(gap_labels)

            rows_html = ""
            for gap in gaps:
                done    = gap["label"] in covered
                row_css = "topic-row covered" if done else "topic-row"
                icon    = "✅" if done else gap["icon"]

                if done:
                    badge_css, badge = "topic-badge done", "Covered"
                elif gap.get("type") == "contested":
                    badge_css, badge = "topic-badge contested", "Contrasting reviews"
                else:
                    badge_css, badge = "topic-badge", "Not documented"

                # Specific questions for this topic from traveler submissions
                prop_qs = questions_df[
                    (questions_df["eg_property_id"] == selected_id) &
                    (questions_df["topic"] == gap["label"])
                ]["question"].dropna().tolist()
                qs_html = ""
                if prop_qs:
                    qs_html = '<div class="topic-questions">' + "".join(
                        f'<span class="topic-q">· {q.strip().rstrip("??")}?</span>'
                        for q in prop_qs[:3]
                    ) + "</div>"

                rows_html += (
                    f'<div class="{row_css}">'
                    f'  <div class="topic-left"><span>{icon}</span>'
                    f'    <div><span class="topic-name">{gap["label"][0].upper() + gap["label"][1:]}</span>'
                    f'    {qs_html}</div></div>'
                    f'  <span class="{badge_css}">{badge}</span>'
                    f'</div>'
                )

            footer_css  = "nudge-footer all-done" if all_done else "nudge-footer"
            footer_text = ("✓ You've covered everything — thank you."
                           if all_done else
                           "No obligation — include whatever feels relevant.")

            st.markdown(f"""
<div class="nudge-panel">
  <h4>Travelers want to know</h4>
  <p class="nudge-intro">{intro}</p>
  {rows_html}
  <p class="{footer_css}">{footer_text}</p>
</div>
""", unsafe_allow_html=True)

            with st.expander("Why am I seeing this?"):
                st.markdown(
                    "These topics are where prospective guests tend to be most uncertain — either "
                    "because recent reviews haven't covered them or because experiences have been "
                    "mixed. Reviews that address these topics lead to more informative review content, helping travelers make "
                    "better choices and get more out of every trip!"
                )

        else:
            st.markdown("""
<div class="nudge-panel">
  <h4>Well covered</h4>
  <p class="nudge-intro">Recent guests have already shared a lot about this property. Just tell us what mattered most to you.</p>
</div>
""", unsafe_allow_html=True)
