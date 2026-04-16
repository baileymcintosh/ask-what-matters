# Research on Review Writers

## Why this exists in this repo

The app in [app.py](/c:/Users/baile/OneDrive%20-%20PennO365/Projects/GITHUB/expedia/app.py:1) is built around a specific product assumption:

- hotel reviewers are primarily motivated by helping other travelers
- reviewers do not want their normal writing flow disrupted
- the right intervention is a light nudge, not a new workflow

That framing is directionally supported by the literature I found. The strongest support is for altruism, reciprocity, and low-friction participation. The weaker part of the current repo narrative is the specific claim that Expedia review writers skew Baby Boomer / Gen X. I did not find strong Expedia-specific academic evidence for that exact statement during this pass, so treat it as a hypothesis unless you have a separate internal source.

## Short answer

### Who writes reviews

- People with stronger engagement, opinion leadership, platform involvement, or reviewer identity are more likely to write reviews.
- Reviewer behavior is explained more consistently by attitudes, motivations, expertise, personality, and platform design than by simple demographics alone.
- In hospitality, reviewer trustworthiness is associated with reviewer profile cues, accumulated expertise, emotional expression, and the perceived credibility of the source.

### Why people write reviews

- The most repeated finding is altruism: helping future consumers make better decisions.
- Other recurring motives are helping the firm, self-enhancement, enjoyment, reciprocity, social recognition, venting negative feelings, and occasionally incentives.
- In travel specifically, recent work still points to altruism as the strongest driver, with cognitive effort and workflow friction reducing participation.

### How people write reviews

- Helpful reviews tend to be concrete, detailed, recent, contextual, and balanced rather than purely emotional.
- Review text and star rating work together. Readers use both.
- Review helpfulness is affected by depth, length, identity cues, reputation cues, emotional arousal, and whether the review gives actionable specifics.

## Implications for this project

### What the research supports in the current app

- A subtle "help fellow travelers" framing is well aligned with the literature.
- Minimizing extra steps is important because executional and cognitive costs reduce review-posting intent.
- Prompting for concrete missing topics should help because readers value detail, factuality, and context.

### What to be careful about

- Do not overstate age or generation claims without a real source.
- Do not assume all review writers are equally altruistic; self-image, recognition, and frustration also matter.
- Prompts should feel optional, not mandatory. Several papers point to friction and motivation crowding as real risks.

## Annotated research notes

### Foundational motivation papers

1. Hennig-Thurau, Gwinner, Walsh, and Gremler (2004), *Electronic word-of-mouth via consumer-opinion platforms: What motivates consumers to articulate themselves on the Internet?*
   - Classic eWOM motivation paper.
   - Key takeaway: the biggest drivers are concern for other consumers, social interaction, economic incentives, and self-enhancement.
   - Link: https://doi.org/10.1002/dir.10073

2. Yoo and Gretzel (2008), *What Motivates Consumers to Write Online Travel Reviews?*
   - Travel-specific and directly relevant here.
   - Key takeaway: the strongest motives were helping the travel service provider, concern for other consumers, enjoyment, and positive self-enhancement.
   - Link: https://doi.org/10.3727/109830508788403114

3. Bakshi, Gupta, and Gupta (2021), *Online travel review posting intentions: a social exchange theory perspective*
   - Focuses on travel review posting, not just reading.
   - Key takeaway: altruism, reputation, economic rewards, and venting negative feelings increase posting intent, while cognitive and executional costs reduce it.
   - Link: https://doi.org/10.1080/14927713.2021.1924076

4. Dogra and colleagues (2019), *What motivates posting online travel reviews? Integrating gratifications with technological acceptance factors*
   - Useful for product design.
   - Key takeaway: altruism, reciprocity, habit, hedonic motivation, and ease of use matter; habit was especially strong.
   - Link: https://hrcak.srce.hr/en/227726

5. Yu and Hsu (2022), *Understanding Users' Urge to Post Online Reviews: A Study Based on Existence, Relatedness, and Growth Theory*
   - General online review behavior.
   - Key takeaway: intrinsic motives such as helping others and supporting the website are especially important; users post when motivated and when platform features support that urge.
   - Link: https://doi.org/10.1177/21582440221129851

6. Evans, Zhang, and Zhao (2019), *Motivation crowding in online product reviewing: A qualitative study of Amazon reviewers*
   - Important caution for nudges and incentives.
   - Key takeaway: status rewards and obligations can either strengthen or crowd out intrinsic motivation.
   - Link: https://doi.org/10.1016/j.im.2019.04.006

7. Sharma and Sharma (2025), *Identifying Factors Motivating Users to Post Reviews on Online Travel Review Platforms: A Factor Analysis Study*
   - Recent travel-specific evidence.
   - Key takeaway: personal reasoning, peer support, social connection, and social capital remain central drivers.
   - Link: https://doi.org/10.32870/myn.vi54.7765

8. Llorens-Marin, Hernandez, and Puelles-Gallo (2023), *Altruism in eWOM: Propensity to Write Reviews on Hotel Experience*
   - Closest match to this repo's current logic.
   - Key takeaway: among hotel customers, altruism is the most important underlying motivation to write a review; managers should encourage reviews on altruistic grounds.
   - Link: https://doi.org/10.3390/jtaer18040113

### Who writes reviews

9. Chua, Al-Ansi, Lee, and Han (2023), *Exploring the antecedents for hospitality reviewers' trustworthiness and its impact on business patronage*
   - Hospitality-specific source characteristics paper.
   - Key takeaway: reviewer trustworthiness depends on both reviewer-profile information and the qualitative properties of the review text.
   - Link: https://doi.org/10.1016/j.ijhm.2023.103448

10. Liang, Wang, and Benyoucef (2021), *Examining the effect of reviewer expertise and personality on reviewer satisfaction: An empirical study of TripAdvisor*
    - Relevant to the "who" question.
    - Key takeaway: reviewer expertise and personality significantly shape review ratings and text sentiment.
    - Link: https://doi.org/10.1016/j.chb.2020.106654

11. Kwok, Xie, and Richards (2018), *Hospitality and Tourism Online Review Research: A Systematic Analysis and Heuristic-Systematic Model*
    - Good meta-level orientation paper.
    - Key takeaway: source cues, review cues, context cues, and receiver cues all shape how reviews are produced and interpreted.
    - Link: https://doi.org/10.3390/su10041141

12. Kovacs and Horwitz (2018), *Conspicuous Reviewing: Affiliation with High-status Organizations as a Motivation for Writing Online Reviews*
    - Less travel-specific, but useful corrective to overly altruistic assumptions.
    - Key takeaway: some people write reviews to make their consumption visible and status-relevant.
    - Link: https://doi.org/10.1177/2378023118776848

### How people write helpful reviews

13. Tripadvisor (2015), *TripAdvisor Launches Guide for Writing Helpful Reviews Based on Survey of More Than 100,000*
    - Industry source, not a peer-reviewed paper, but directly useful.
    - Key takeaway: travelers prefer reviews that focus on facts, provide detail, are recent, offer context, and present a balanced view.
    - Link: https://tripadvisor.mediaroom.com/2015-03-18-TripAdvisor-Launches-Guide-for-Writing-Helpful-Reviews-Based-On-Survey-of-More-Than-100-000

14. Tripadvisor Insights (2015), *Research: What makes a helpful review*
    - Companion industry source.
    - Key takeaway: lack of detail is a major reason reviews are seen as unhelpful; personality and context improve usefulness.
    - Link: https://www.tripadvisor.com/TripAdvisorInsights/w753

15. Shin, Du, Ma, Fan, and Xiang (2021), *Moderating effects of rating on text and helpfulness in online hotel reviews: an analytical approach*
    - Strong fit for your UI logic.
    - Key takeaway: text and rating interact; helpfulness cannot be understood from stars or prose alone.
    - Link: https://doi.org/10.1080/19368623.2020.1778596

16. Zhao, Wang, Guo, and Law (2019), *Assessing the helpfulness of online hotel reviews: A classification-based approach*
    - Directly about hotel review helpfulness.
    - Key takeaway: review quality, sentiment, and reviewer characteristics jointly predict helpfulness.
    - Link: https://doi.org/10.1016/j.jbusres.2017.10.045

17. Kim, Kim, and Park (2022), *The Determinants of Helpful Hotel Reviews: A Social Influence Perspective*
    - Hotel-specific and practical.
    - Key takeaway: review length, ratings, and social influence factors affect helpfulness, with variation by hotel grade.
    - Link: https://doi.org/10.3390/su142214881

18. Filieri, Raguseo, and Vitari (2021), *What makes an online consumer review helpful? A diagnosticity-adoption framework to explain informational and normative influences in e-WOM*
   - General but highly relevant to review design.
   - Key takeaway: helpful reviews increase information diagnosticity; reviewer and message cues both matter.
   - Link: https://doi.org/10.1007/s11747-019-00695-1

19. de Langhe, Fernbach, and Lichtenstein (2016), *Navigating by the stars: Investigating the actual and perceived validity of online user ratings*
   - Useful caution on ratings versus text.
   - Key takeaway: aggregated star ratings can be biased or misunderstood, which increases the importance of richer review text.
   - Link: https://doi.org/10.1016/j.obhdp.2016.04.002

20. Mladenovic, Val, and colleagues (2024), *Rant or rave: variation over time in the language of online reviews*
   - Language-focused paper.
   - Key takeaway: review language and helpfulness are linked to text length and writing conditions; mobile-submitted reviews tend to be shorter and less helpful.
   - Link: https://doi.org/10.1007/s10579-023-09652-5

## What this means for a next iteration of the app

- Keep the current panel optional and non-blocking.
- Frame prompts as helping future travelers, not helping Expedia.
- Prefer 3 to 5 concrete missing topics over long questionnaires.
- Ask for specific, factual observations such as noise, Wi-Fi, parking, breakfast, and check-in details.
- Avoid adding required follow-up questions after submission unless there is evidence the added step will not suppress completion.
- If you want to retain the generation claim in the demo narrative, add a real source or rewrite it as a hypothesis.

## Source quality note

- I prioritized peer-reviewed articles and official industry material where possible.
- Some useful sources above are journal landing pages or DOI pages rather than open PDFs.
- I included industry sources only where they were directly relevant to review-writing behavior or helpful-review guidance.
