# Research Supporting The Product Thesis

## Why this exists

This memo tests the specific product choices behind the current prototype:

- use AI to detect review information gaps, not to replace review writing
- surface prompts at the start of the writing flow, not as an end-of-flow interrogation
- preserve text review writing as the primary interaction mode
- keep the intervention subtle, optional, and low-friction

I prioritized primary research and official publisher or journal pages. The evidence is strongest for altruism, low-friction participation, habit, and the value of detailed review text. The evidence is more indirect for the claim that voice or conversational review collection is a bad fit for hotel reviews specifically.

## Bottom line

### Strongly supported

- Review writers are often motivated by helping other consumers, not just by rewards.
- Cognitive effort, executional cost, and platform friction reduce review-posting intent.
- Habit and ease of use matter in travel-review posting.
- Review usefulness depends heavily on the quality of the text, not just on star ratings.
- Readers value specificity, context, balance, and authentic personal detail.

### Supported, but more indirectly

- Reviews are not just data capture; they also function as self-expression and identity signaling.
- Because review usefulness depends on detailed, authentic, personal writing, product changes that disrupt composition should be treated carefully.
- A subtle in-context prompt is easier to defend than an extra step after the user already feels finished.

### Not directly proven by the literature I found

- I did not find a strong primary study showing that voice-first hotel review collection specifically reduces review quality.
- I also did not find direct Expedia-specific evidence that reviewers are unusually resistant to workflow change.

Those two claims are better presented as product hypotheses or design judgments supported by adjacent evidence, not as settled facts.

## Findings by core argument

### 1. "People write reviews largely to help other travelers"

This is well supported.

- Hennig-Thurau et al. (2004) found that concern for other consumers is one of the primary drivers of eWOM behavior, alongside social interaction, economic incentives, and self-enhancement.
- Yoo and Gretzel (2008) found that online travel review writers are mostly motivated by helping a travel service provider, concern for other consumers, and enjoyment/positive self-enhancement.
- Llorens-Marin, Hernandez, and Puelles-Gallo (2023) found that, among hotel customers, the most important underlying motivation to write a review is altruistic.
- Yu and Hsu (2022) similarly found that helping others and supporting websites are important intrinsic motivators behind the urge to post reviews.

What this supports for the product:

- Framing the panel around helping fellow travelers is aligned with the literature.
- The app should present the prompt as an opportunity to help others, not as a company demand.

### 2. "Extra effort and extra steps can suppress review contribution"

This is also well supported.

- Bakshi, Gupta, and Gupta (2021) found that cognitive and executional costs negatively influence travel-review posting intentions.
- Dogra, Bakshi, and Gupta (2019) found that effort expectancy, habit, altruism, reciprocity, and hedonic motivation positively influence travel-review posting intentions, and explicitly recommend simple, easy-to-use review sites.
- Evans, Zhang, and Zhao (2019) found that extrinsic structures such as status recognition and reciprocal obligation can crowd out intrinsic motivation in online reviewing.

What this supports for the product:

- The prototype should avoid adding a second task after the user has already written the review.
- Prompts should remain optional and lightweight.
- The system should be careful not to feel like a forced questionnaire.

### 3. "Review writing is not only fact capture; it is also expressive writing"

There is meaningful support here.

- Hennig-Thurau et al. (2004) includes self-enhancement and social benefits among primary eWOM motives.
- Kovacs and Horwitz (2018) show that some review writing behavior is status-relevant and identity-expressive, not purely altruistic.
- Hoyer and Kreis (2022) found experimentally that self-expression stimulates review publication for less-altruistic participants, and that suppressing self-expression through anonymity reduces ratings.
- Fourkan, Darani, and Wiggins (2026) argue that readers judge not only credibility but also "expressive authenticity," defined as whether a review represents the communicator's values, beliefs, and experiences. Their studies show that expressive authenticity has separate effects on review usefulness.

What this supports for the product:

- The review box should remain the center of the experience.
- AI should guide what to cover, but not take over how the person says it.
- Your thesis that reviews are deliberate communication, not just structured data entry, is defensible.

### 4. "Detailed written text matters; stars alone are not enough"

This is strongly supported.

- Shin et al. (2021) found that review text and ratings interact in shaping how hotel reviews are perceived.
- Zhao et al. (2018) found that review helpfulness depends on review quality, review sentiment, and reviewer characteristics.
- Chua et al. (2023) found that trustworthiness depends on both quantitative and qualitative review information, including sentiment content and emotional arousal in review text.
- Ziser, Webber, and Cohen (2023) found that reviews have become less comprehensive over time and note that helpful opinionated text is strongly related to text length and comprehensiveness.
- TripAdvisor's large-sample review guidance, while not peer-reviewed, is directionally consistent: travelers prefer factual, detailed, recent, contextual, and balanced reviews.

What this supports for the product:

- It makes sense to optimize for better review text, not just more structured ratings.
- Nudging writers toward missing topics should improve usefulness if it increases specificity and context.

### 5. "A subtle prompt at the start is better than a follow-up question at the end"

There is no single paper in this set that directly tests start-of-flow prompts versus end-of-flow follow-up questions in hotel reviews. But the combined evidence points in your direction.

Relevant evidence:

- Review-posting intent falls when cognitive and executional costs rise.
- Habit and ease-of-use matter in travel review posting.
- Review usefulness depends on the richness and authenticity of the written text.
- Motivation crowding research suggests that intrusive or obligation-feeling interventions can backfire.

Inference:

- If the user already feels finished after writing the review, adding another mandatory step is likely to feel like extra work.
- Showing the relevant gaps before or during composition is more consistent with the evidence on low friction and authentic text production.

This is an inference from the literature, not a directly tested finding in the sources above.

### 6. "Avoiding voice or conversational review collection is a reasonable design choice"

This claim has the weakest direct evidence in the review literature, so it should be framed carefully.

What the evidence does support:

- Rich, authentic, personal text is valuable.
- Self-expression is one motive for writing reviews.
- Review helpfulness is sensitive to textual quality and comprehensiveness.
- Mobile-originated reviews tend to be shorter, more intense, and less comprehensive in at least some studies, suggesting that lower-friction input modes do not automatically preserve review quality.

From Ziser et al. (2023):

- Reviews posted from mobile devices were shorter and showed lower language quality in the Booking.com analysis discussed in the paper.

From Xu, Zha, and colleagues (Information & Management, 2022):

- Mobile reviews on TripAdvisor received fewer helpful votes, and text length is one of the negative mediating paths between mobile device usage and review helpfulness.

Inference:

- Because the review task appears to benefit from deliberate composition, it is reasonable to treat voice-first or conversation-first capture as a risk rather than an automatic UX win.
- The literature supports caution here, but not a categorical claim that voice is always worse.

How to say this rigorously:

- "We intentionally did not center voice. The literature suggests review usefulness depends on rich, authentic text and that lower-friction capture modes can sometimes produce shorter, less helpful reviews. We therefore chose to preserve deliberate text composition and use AI as a subtle writing aid instead of a conversational replacement."

## Practical implications for the current prototype

The current app's strongest research-backed choices are:

- altruistic framing
- low-friction, optional intervention
- targeting missing/stale topics
- preserving the main review-writing box as the central experience

The parts that should be phrased as design judgment rather than proven fact are:

- avoiding voice because it undermines how people naturally write reviews
- claiming users are resistant to workflow change in this exact Expedia use case

## Suggested claims you can make safely

- "Hotel review writing is strongly motivated by helping other travelers."
- "Reducing cognitive and executional costs is important because friction suppresses review-posting intent."
- "Review usefulness depends on rich, specific text, not just star ratings."
- "Because reviews also communicate personal experience and expressive authenticity, AI should guide the writing process without replacing it."
- "Our design hypothesis is that subtle prompts at the start of writing are less disruptive than additional follow-up steps after the review feels complete."

## Sources

See [sources.csv](/c:/Users/baile/OneDrive%20-%20PennO365/Projects/GITHUB/expedia/research/product-thesis/sources.csv:1) for the structured source list.
