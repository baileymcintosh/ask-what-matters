# Video Script — Ask What Matters
**Target: 3.5–4 minutes | ~550 words spoken**

---

## 1. Problem & Context (~45 sec)

> Reviews are the single most trusted signal in travel booking — 81% of travelers say they rely on them. But there's a structural problem: reviewers write what they remember, not what future guests need to know.

> Take this resort in Broomfield, Colorado. It advertises a full-service spa with six treatment rooms, a 27-hole golf course, and rooms renovated last October. I scrolled through over a thousand reviews. Staff is mentioned everywhere. Pools — everywhere. The spa? Forty-five reviews out of a thousand. The golf course? Seventeen. No one has written about what the rooms actually feel like post-renovation.

> If I'm planning a golf trip with a spa day, I'm going in blind. The hotel isn't bad — the review corpus just hasn't caught up to it.

---

## 2. Our AI Solution (~45 sec)

> We built Ask What Matters — a two-sided information system that connects what travelers need to know with the people who can answer it.

> The key insight from the literature is that reviewers are already motivated by altruism — they write to help other travelers. They don't need to be pushed harder. They need to be shown what's missing.

> So instead of adding voice prompts or mandatory follow-up fields — both of which disrupt the writing experience reviewers value — we built two lightweight features that work with existing behavior, not against it.

---

## 3. Demo (~2 min)

**[Show browse page]**

> Here's the property page. A prospective traveler is planning a spa-and-golf trip. They read the reviews. Nothing useful about the spa. Nothing about the golf course. They submit a quick question: *"Is the spa worth booking in advance? How far ahead?"* That takes five seconds and requires no review.

**[Show question submitted, gap panel updating]**

> That question hits our demand signal. On the back end, the gap scorer combines two streams: embedding-based coverage analysis of the review corpus, and this demand signal from guest questions. Spa just moved to the top of the gap rankings for this property.

**[Switch to reviewer view]**

> Now a guest checks out and opens the review form. Before they type a word, they see the gap panel — three topics the property is missing: Spa, Golf, and Room Condition post-renovation. The spa is ranked first because someone just asked about it.

**[Show reviewer typing, topics crossing off]**

> They write their review. The moment they mention the spa — it crosses off the list in real time. They write about the golf course — crosses off. They mention the renovated rooms — crosses off. The list empties. They submit.

**[Show traveler notification]**

> The traveler gets notified: a recent reviewer just wrote about the spa. They read it. They book. A stay they were hesitant about — not because the hotel was bad, but because no one had written what they needed to know.

---

## 4. Feasibility & Scalability (~20 sec)

> The stack is OpenAI embeddings, VADER sentiment analysis, and GPT-4o-mini for discovering property-specific gaps outside our fixed taxonomy. The system improves automatically as review volume grows and self-corrects as gaps get filled — no manual curation required.

---

## 5. Wrap-Up (~15 sec)

> Reviews are only as useful as the questions they answer. Ask What Matters closes that gap — not by changing how people write, but by showing them what matters.
