"""
Shared utilities for Ask What Matters — Expedia Hack-AI-thon 2026.
Imported by both app.py (reviewer) and pages/browse.py (prospective guest).
"""

import json, os, ast, base64, math, re
from pathlib import Path

import pandas as pd
import numpy as np
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

load_dotenv()

# ── Constants ─────────────────────────────────────────────────────────────────

DECAY_HALFLIFE_DAYS  = 180   # recency half-life for review weighting
MAX_EMBED_REVIEWS    = 40    # reviews to embed per property (cost control)
RELEVANCE_THRESHOLD  = 0.40  # cosine similarity for a review to "count" as on-topic
COVERAGE_THRESHOLD   = 0.15  # flag as gap if < this fraction of weighted reviews discuss it
CONTESTED_STD        = 0.38  # flag as contested if VADER sentiment std dev exceeds this
CONTESTED_MIN        = 4     # need at least this many on-topic reviews to call contested
DEMAND_BETA          = 0.5   # demand multiplier strength

TOPICS = [
    # ── Always relevant: experiential categories reviewers write about in depth ──
    ("Location & Neighborhood", ["location", "area", "neighborhood", "walk", "nearby", "central",
                                  "transport", "metro", "surroundings", "distance"],              "📍"),
    ("Room Quality",            ["room", "space", "decor", "furnish", "interior", "layout",
                                  "size", "small", "spacious", "design", "view"],                 "🛏️"),
    ("Service & Staff",         ["staff", "service", "helpful", "friendly", "reception",
                                  "concierge", "attentive", "rude", "host"],                      "👋"),
    ("Atmosphere & Vibe",       ["atmosphere", "vibe", "ambiance", "feel", "character",
                                  "cozy", "romantic", "lively", "charm", "quiet retreat"],        "✨"),
    ("Bathroom",                ["bathroom", "shower", "bath", "water pressure", "bathtub",
                                  "toilet", "toiletries", "hot water"],                           "🚿"),
    ("Sleep Quality",           ["sleep", "slept", "rest", "bed", "mattress", "pillow",
                                  "comfortable", "night", "woke"],                                "😴"),
    ("Noise Levels",            ["noise", "noisy", "quiet", "loud", "soundproof",
                                  "disturb", "traffic", "street", "thin walls"],                  "🔇"),
    ("Value for Money",         ["value", "worth", "price", "expensive", "affordable",
                                  "cost", "overpriced", "money", "pricey"],                       "💰"),
    ("Cleanliness",             ["clean", "dirty", "spotless", "hygiene", "dust",
                                  "housekeeping", "tidy", "stain"],                               "🧹"),
    ("Check-in Experience",     ["check-in", "checkin", "check out", "checkout",
                                  "arrival", "front desk", "reception", "waited"],                "🔑"),
    # ── Conditional: only surfaced when property amenity data confirms relevance ──
    ("Food & Dining",           ["food", "restaurant", "meal", "dining", "eat",
                                  "menu", "dinner", "lunch", "bar", "drink"],                     "🍽️"),
    ("Breakfast",               ["breakfast", "brunch", "morning meal", "buffet"],                "🍳"),
    ("Pool & Facilities",       ["pool", "gym", "fitness", "spa", "swimming",
                                  "workout", "sauna", "hot tub"],                                 "🏊"),
    ("WiFi / Connectivity",     ["wifi", "internet", "connection", "signal",
                                  "bandwidth", "online", "speed"],                                "📶"),
    ("Parking",                 ["parking", "valet", "garage", "car park"],                       "🅿️"),
]

TOPIC_ANCHORS = {
    "Location & Neighborhood": "hotel location neighborhood area walkable surroundings convenient central transport proximity attractions",
    "Room Quality":            "hotel room size space furnishings decor layout interior quality design appointed view",
    "Service & Staff":         "hotel staff service helpful friendly attentive responsive front desk concierge host",
    "Atmosphere & Vibe":       "hotel atmosphere vibe ambiance character feel cozy romantic lively charm relaxed peaceful",
    "Bathroom":                "hotel bathroom shower water pressure hot water bathtub toiletries quality maintained",
    "Sleep Quality":           "hotel sleep quality rest comfortable bed mattress pillow night disturbed woke rested",
    "Noise Levels":            "hotel noise levels quiet loud soundproofing street traffic walls rooms disturb sleep",
    "Value for Money":         "hotel value money price worth cost expensive affordable overpriced rate",
    "Cleanliness":             "hotel room cleanliness hygiene dirty spotless housekeeping maintained tidy stain",
    "Check-in Experience":     "hotel check-in check-out arrival process wait time front desk efficiency smooth",
    "Food & Dining":           "hotel restaurant food quality meal dining worth eating menu dinner lunch bar",
    "Breakfast":               "hotel breakfast buffet morning meal food quality variety included spread",
    "Pool & Facilities":       "hotel swimming pool gym fitness spa facilities sauna hot tub condition",
    "WiFi / Connectivity":     "hotel wifi internet connection speed reliable signal bandwidth online work",
    "Parking":                 "hotel parking availability garage valet car ease convenient",
}

HOTEL_NAMES = {
    "ba8ce0b0": "Villa dei Misteri Hotel",
    "a9b17723": "Omni Interlocken Resort",
    "2c101a12": "Waldhotel Zollernblick",
    "c83a2820": "Hotel Jardín Quetzal",
    "f59be65f": "Cortina Stadthotel Bochum",
    "c9cd4676": "Silom Garden Hotel",
    "1343f838": "The Lodge at Frisco",
    "c68c3caa": "Old Fisherman's Inn",
    "179206df": "Hotel Medici Roma",
    "6c499052": "Kruger View Safari Lodge",
    "f76a1941": "Garden Inn Bell Gardens",
    "74a2a2b9": "Oceanview Suites NSB",
    "c32a5b06": "Silver Springs Inn",
}

TOPIC_ICON_MAP = {label: icon for label, _, icon in TOPICS}


# ── OpenAI client ─────────────────────────────────────────────────────────────

@st.cache_resource
def get_client():
    key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")
    if not key:
        st.error("OPENAI_API_KEY not set.")
        st.stop()
    return OpenAI(api_key=key)


# ── Data loaders ──────────────────────────────────────────────────────────────

@st.cache_data
def load_data():
    root = Path(__file__).parent / "data"
    desc    = pd.read_csv(root / "Description_PROC.csv")
    reviews = pd.read_csv(root / "Reviews_PROC.csv")

    def safe_parse(raw):
        try:
            return json.loads(str(raw))
        except Exception:
            try:
                return ast.literal_eval(str(raw))
            except Exception:
                return {}

    reviews["rating_parsed"]    = reviews["rating"].apply(safe_parse)
    reviews["acquisition_date"] = pd.to_datetime(reviews["acquisition_date"], errors="coerce")
    return desc, reviews


def load_questions() -> pd.DataFrame:
    """Load traveler questions. Never cached — always reads fresh from disk."""
    p = Path(__file__).parent / "data" / "traveler_questions.csv"
    if p.exists():
        return pd.read_csv(p)
    return pd.DataFrame(columns=["eg_property_id", "question", "topic", "timestamp", "source"])


def save_question(property_id: str, question: str, topic: str) -> None:
    """Append a user-submitted question to the CSV."""
    p = Path(__file__).parent / "data" / "traveler_questions.csv"
    df = load_questions()
    new_row = pd.DataFrame([{
        "eg_property_id": property_id,
        "question": question.strip(),
        "topic": topic,
        "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d"),
        "source": "user",
    }])
    pd.concat([df, new_row], ignore_index=True).to_csv(p, index=False)


def wipe_user_questions() -> int:
    """Delete all user-submitted questions, keep seed data. Returns count deleted."""
    p = Path(__file__).parent / "data" / "traveler_questions.csv"
    df = load_questions()
    n_before = len(df)
    df = df[df["source"] != "user"]
    df.to_csv(p, index=False)
    return n_before - len(df)


def get_demand_scores(property_id: str, questions_df: pd.DataFrame) -> dict:
    """
    Returns {topic_label: demand_signal ∈ [0,1]}.
    Demand signal = question count for topic / max count across topics (normalised).
    """
    prop_q = questions_df[questions_df["eg_property_id"] == property_id]
    if prop_q.empty:
        return {}
    counts = prop_q["topic"].value_counts().to_dict()
    max_count = max(counts.values()) if counts else 1
    return {label: count / max_count for label, count in counts.items()}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _clean(val) -> str:
    if val is None:
        return ""
    try:
        if pd.isna(val):
            return ""
    except Exception:
        pass
    s = str(val).strip()
    return "" if s.lower() in ("nan", "none", "") else s


def _amenity_text(row, col: str) -> str:
    """Parse a JSON-list amenity column into a single lowercase string."""
    val = row.get(col, "")
    try:
        if pd.isna(val):
            return ""
    except Exception:
        pass
    s = str(val).strip()
    if not s or s.lower() in ("nan", "none", "[]"):
        return ""
    try:
        items = json.loads(s)
        return " ".join(str(i) for i in items).lower()
    except Exception:
        return s.lower()


def _topic_is_relevant(row, label: str) -> bool:
    """Return True if this topic is relevant for this property."""
    if label == "WiFi / Connectivity":
        return bool(_amenity_text(row, "property_amenity_internet"))
    if label == "Parking":
        return bool(_amenity_text(row, "property_amenity_parking"))
    if label == "Breakfast":
        food = _amenity_text(row, "property_amenity_food_and_drink")
        return any(kw in food for kw in ["breakfast", "buffet"])
    if label == "Food & Dining":
        food = _amenity_text(row, "property_amenity_food_and_drink")
        return any(kw in food for kw in ["restaurant", "bar", "dining", "cafe", "bistro"])
    if label == "Pool & Facilities":
        todo    = _amenity_text(row, "property_amenity_things_to_do")
        outdoor = _amenity_text(row, "property_amenity_outdoor")
        return any(kw in todo + " " + outdoor for kw in ["pool", "fitness", "gym", "spa", "hot tub"])
    return True


def prop_info(pid: str, desc_df: pd.DataFrame) -> dict:
    row = desc_df[desc_df["eg_property_id"] == pid]
    if row.empty:
        return {}
    r        = row.iloc[0]
    city     = _clean(r.get("city"))
    province = _clean(r.get("province"))
    country  = _clean(r.get("country"))
    location = ", ".join(x for x in [city, province, country] if x)
    name     = HOTEL_NAMES.get(pid[-8:], f"{city} Hotel" if city else "Hotel")
    try:
        rating_str = f"{float(_clean(r.get('guestrating_avg_expedia'))):.1f}"
    except Exception:
        rating_str = "—"
    return {"name": name, "city": city, "location": location, "rating": rating_str}


def prop_dropdown_label(pid: str, desc_df: pd.DataFrame) -> str:
    info = prop_info(pid, desc_df)
    if not info:
        return f"Property …{pid[-6:]}"
    name     = info.get("name", "")
    location = info.get("location", "")
    return f"{name}  —  {location}" if location else name


def logo_img_tag(height: int = 28) -> str:
    assets = Path(__file__).parent / "assets"
    for name, mime in [("expedia-logo.svg", "image/svg+xml"),
                        ("expedia-logo.png", "image/png")]:
        p = assets / name
        if p.exists():
            data = base64.b64encode(p.read_bytes()).decode()
            return (f'<img src="data:{mime};base64,{data}" '
                    f'style="height:{height}px;width:auto;display:block;" alt="Expedia">')
    return '<span style="font-size:1.25rem;font-weight:800;color:#fff;letter-spacing:-0.01em;">Expedia</span>'


# ── Embedding ─────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def embed(texts: tuple) -> list:
    """Batch embed texts via OpenAI. Input is a tuple (hashable for st.cache_data)."""
    safe = [t if t.strip() else "." for t in texts]
    resp = get_client().embeddings.create(model="text-embedding-3-small", input=safe)
    return [e.embedding for e in resp.data]


@st.cache_data(show_spinner=False)
def anchor_embeddings() -> dict:
    """Embed all topic anchor phrases once; reused across all properties."""
    labels = list(TOPIC_ANCHORS.keys())
    vecs   = embed(tuple(TOPIC_ANCHORS[l] for l in labels))
    return dict(zip(labels, vecs))


@st.cache_resource
def get_vader() -> SentimentIntensityAnalyzer:
    return SentimentIntensityAnalyzer()


@st.cache_data(show_spinner=False)
def embed_sentence(sentence: str) -> list:
    """Embed a single sentence, cached by content."""
    return embed((sentence,))[0]


def covered_topics(text: str, gaps: list) -> set:
    """
    Semantic coverage: embed each completed sentence in the review and compare
    against topic anchor embeddings. A sentence is 'on-topic' if cosine similarity
    to the anchor exceeds the relevance threshold.
    """
    if not text or len(text.strip()) < 10:
        return set()
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if len(s.strip()) > 8]
    if not sentences:
        return set()
    anchors = anchor_embeddings()
    covered = set()
    for sentence in sentences:
        try:
            s_vec = np.array(embed_sentence(sentence))
        except Exception:
            continue
        s_norm = np.linalg.norm(s_vec)
        if s_norm == 0:
            continue
        s_unit = s_vec / s_norm
        for g in gaps:
            if g["label"] in covered:
                continue
            label = g["label"]
            if label in anchors:
                a_vec  = np.array(anchors[label])
                a_norm = np.linalg.norm(a_vec)
                if a_norm == 0:
                    continue
                if float(s_unit @ (a_vec / a_norm)) >= RELEVANCE_THRESHOLD:
                    covered.add(label)
            else:
                words = [w for w in label.lower().split() if len(w) > 3]
                if words and any(w in sentence.lower() for w in words):
                    covered.add(label)
    return covered


@st.cache_data(show_spinner=False)
def classify_question_topic(question: str) -> str:
    """Find the best-matching TOPICS label for a question using embedding similarity."""
    q_vec  = np.array(embed((question,))[0])
    q_norm = np.linalg.norm(q_vec)
    if q_norm == 0:
        return TOPICS[0][0]
    q_unit  = q_vec / q_norm
    anchors = anchor_embeddings()
    best_label, best_sim = TOPICS[0][0], -1.0
    for label, _, _ in TOPICS:
        if label not in anchors:
            continue
        a = np.array(anchors[label])
        a_n = np.linalg.norm(a)
        if a_n == 0:
            continue
        sim = float(q_unit @ (a / a_n))
        if sim > best_sim:
            best_sim, best_label = sim, label
    return best_label


# ── Gap analysis ──────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def discover_unique_topics(property_id: str) -> list:
    """One gpt-4o-mini call: find property-specific gaps the fixed categories can't capture."""
    desc_df, reviews_df = load_data()
    prop_row = desc_df[desc_df["eg_property_id"] == property_id]
    if prop_row.empty:
        return []
    row  = prop_row.iloc[0]
    name = HOTEL_NAMES.get(property_id[-8:], "this hotel")
    city = _clean(row.get("city"))
    desc = _clean(row.get("property_description"))[:600]
    amen = _clean(row.get("popular_amenities_list"))[:300]
    sample = (reviews_df[reviews_df["eg_property_id"] == property_id]
              .dropna(subset=["acquisition_date"])
              .sort_values("acquisition_date", ascending=False)["review_text"]
              .dropna().head(12).tolist())
    reviews_block = "\n---\n".join(sample)
    prompt = (
        f"Hotel: {name}, {city}\nDescription: {desc}\nAmenities: {amen}\n\n"
        f"Recent reviews:\n{reviews_block}\n\n"
        f"A traveler is about to book this hotel. What would they be genuinely UNCERTAIN about "
        f"that the reviews above fail to answer? Focus on things a guest would only know from "
        f"staying there — operational details, experiential qualities, or aspects specific to "
        f"this property's type or setting that the reviews leave unclear.\n"
        f"Do NOT suggest: generic topics (WiFi, cleanliness, bed comfort), things already "
        f"well-covered in the reviews, or obvious facts from the description.\n"
        f"Return up to 2 items as JSON array only: [{{\"label\": \"short topic name\", \"icon\": \"one emoji\"}}]\n"
        f"Return [] if no genuine uncertainty gaps exist."
    )
    r = get_client().chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3, max_tokens=150,
    )
    raw = r.choices[0].message.content.strip().replace("```json", "").replace("```", "").strip()
    try:
        items = json.loads(raw)
        return [
            {"label": i["label"][0].upper() + i["label"][1:], "icon": i.get("icon", "✨"),
             "keywords": [], "type": "unique", "score": 0.2}
            for i in items if isinstance(i, dict) and "label" in i
        ][:2]
    except Exception:
        return []


@st.cache_data(show_spinner=False)
def analyze_property(property_id: str, demand: tuple = ()) -> list:
    """
    Three-signal gap analysis with optional demand weighting.

    demand: tuple of (topic_label, demand_signal) pairs — hashable for caching.
            Pass tuple(sorted(get_demand_scores(...).items())) from the caller.
    """
    demand_scores = dict(demand)

    desc_df, reviews_df = load_data()
    prop_row     = desc_df[desc_df["eg_property_id"] == property_id]
    prop_reviews = reviews_df[reviews_df["eg_property_id"] == property_id].copy()

    if prop_row.empty or prop_reviews.empty:
        return []

    row = prop_row.iloc[0]
    now = pd.Timestamp.now()

    prop_reviews = prop_reviews.dropna(subset=["acquisition_date"]).copy()
    prop_reviews["days_ago"] = (now - prop_reviews["acquisition_date"]).dt.days.clip(lower=0)
    prop_reviews["weight"]   = prop_reviews["days_ago"].apply(
        lambda d: math.exp(-math.log(2) * d / DECAY_HALFLIFE_DAYS)
    )
    prop_reviews = prop_reviews[prop_reviews["review_text"].fillna("").str.strip().str.len() > 0]
    top          = prop_reviews.nlargest(MAX_EMBED_REVIEWS, "weight").reset_index(drop=True)
    total_weight = top["weight"].sum()
    if total_weight == 0:
        return []

    review_vecs  = np.array(embed(tuple(top["review_text"].fillna("").tolist())))
    anchors      = anchor_embeddings()
    vader        = get_vader()

    review_norms = np.linalg.norm(review_vecs, axis=1, keepdims=True)
    review_norms[review_norms == 0] = 1
    R = review_vecs / review_norms

    results = []
    for label, keywords, icon in TOPICS:
        if not _topic_is_relevant(row, label) or label not in anchors:
            continue

        # Signal 1: embedding coverage
        a_vec  = np.array(anchors[label])
        a_norm = np.linalg.norm(a_vec)
        if a_norm == 0:
            continue
        sims       = R @ (a_vec / a_norm)
        on_topic   = sims >= RELEVANCE_THRESHOLD
        coverage   = float(top.loc[on_topic, "weight"].sum()) / total_weight

        # Signal 2: VADER consensus
        is_contested   = False
        on_topic_texts = top.loc[on_topic, "review_text"].dropna().tolist()
        if len(on_topic_texts) >= CONTESTED_MIN:
            sentiments = [vader.polarity_scores(t)["compound"] for t in on_topic_texts]
            if float(np.std(sentiments)) >= CONTESTED_STD:
                is_contested = True

        is_gap = coverage < COVERAGE_THRESHOLD
        if not is_gap and not is_contested:
            continue

        # Demand multiplier
        d            = demand_scores.get(label, 0.0)
        multiplier   = 1.0 + DEMAND_BETA * d
        base_score   = (1.0 - coverage) if not is_contested else (0.5 * (1.0 - coverage))
        sort_score   = base_score * multiplier
        gap_type     = "contested" if is_contested else "gap"

        results.append({"label": label, "icon": icon, "keywords": keywords,
                         "type": gap_type, "score": sort_score})

    # Signal 3: LLM unique topics (no demand boost — they're already rare)
    results.extend(discover_unique_topics(property_id))
    results.sort(key=lambda g: -g["score"])
    return results[:3]


@st.cache_data(show_spinner=False)
def nudge_intro(city: str, gap_labels: tuple) -> str:
    r = get_client().chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content":
            f"Write ONE warm sentence (max 18 words) for a hotel review form in {city}. "
            f"Tell the reviewer other travelers are curious about: {', '.join(gap_labels)}. "
            f"Frame it as a chance to help others. Don't use 'we'. No colon at end."}],
        temperature=0.6, max_tokens=60,
    )
    return r.choices[0].message.content.strip().strip('"')
