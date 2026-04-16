# Video Script — Ask What Matters
**Target: 3.5–4 minutes | ~550 words spoken**

---

## 1. Problem & Context (~45 sec)

> Reviews are the single most trusted signal in travel booking — 81% of travelers say they rely on them. But there's a structural problem: reviewers write what they remember, not what future guests need to know.

> Take this hotel in Pompei, Italy — the Villa dei Misteri, steps from the archaeological ruins. It advertises a restaurant. Out of 146 reviews, nearly every single one says the same thing: great location, nice staff, very close to the ruins. Almost nothing about dinner. One reviewer buried near the bottom says: "describes itself as having a restaurant but it was never open after 6pm — the whole area shuts down when the crowds go home."

> There are also noise complaints — but they're in German and Dutch. An English-speaking traveler browsing this page has no idea.

> If you're arriving by train from Rome at 8pm expecting dinner, you're going in blind.

---

## 2. Our AI Solution (~45 sec)

> We built Ask What Matters — a two-sided information system that connects what travelers need to know with the people who can answer it.

> The key insight from the literature is that reviewers are already motivated by altruism — they write to help other travelers. They don't need to be pushed harder. They need to be shown what's missing.

> So instead of adding voice prompts or mandatory follow-up fields — both of which disrupt the writing experience reviewers value — we built two lightweight features that work with existing behavior, not against it.

---

## 3. Demo (~2 min)

**[Show browse page — Villa dei Misteri Hotel]**

> Here's the property page. A traveler is planning a late arrival from Rome. They scroll through the reviews. Location, location, location. Staff was nice. Close to the ruins. Nothing about whether dinner is actually available. They submit a question: *"Is the restaurant open for dinner, or is it breakfast only?"* Five seconds, no review required.

**[Show question submitted, gap panel updating]**

> That question hits our demand signal. On the back end, the gap scorer combines embedding-based coverage analysis of the review corpus with this demand signal from guest questions. Food & Dining just moved to the top of the gap rankings for this property.

**[Switch to reviewer view]**

> A guest checks out and opens the review form. Before they type a word, they see the gap panel — three topics this property is missing: Food & Dining, Noise Levels, and WiFi. Food & Dining is ranked first because someone just asked about it — and it's listed under "Travelers asking."

**[Show reviewer typing, topics crossing off]**

> They write their review. They mention the restaurant — breakfast only, closes at nine, nothing nearby after seven. *Food & Dining crosses off.* They mention the thin walls. *Noise Levels crosses off.* They note WiFi only reaches the corridor. *WiFi crosses off.*

**[Show traveler notification]**

> The traveler gets notified: a recent reviewer just wrote about dining at this property. They read it. They book the early check-in, plan dinner in Naples before arriving. A stay they were hesitant about — not because the hotel was bad, but because no one had written what they needed to know.

---

## 4. Feasibility & Scalability (~20 sec)

> The stack is OpenAI embeddings, VADER sentiment analysis, and GPT-4o-mini for discovering property-specific gaps outside our fixed taxonomy. The system improves automatically as review volume grows and self-corrects as gaps get filled — no manual curation required.

---

## 5. Wrap-Up (~15 sec)

> Reviews are only as useful as the questions they answer. Ask What Matters closes that gap — not by changing how people write, but by showing them what matters.
