# Objections and repairs in the final 22b comparison

Two separate views add historically recorded objections and explicit interpretive repairs. The existing eleven SVG maps, base claims and source passages are preserved. These views distinguish a challenge to an inference from a denial of the verse, the Gemara’s recorded refutation or its ruling. All relations remain dialectical, in loose mode.

## Attribution and exact sources

[Ritva’s passage quoted in Shittah Mekubbetzet, 22b](https://he.wikisource.org/wiki/בבא_מציעא_כב_ב#שיטה_מקובצת) introduces the objections with **ובתוספות הקשו** and closes with **הריטב״א**. We therefore label J1/J2 “Ritva reports” and preserve that indirect attribution. We do not identify these reported objections with the printed Tosafot **איסורא דומיא דהתירא**. The passage discusses alternative textual versions and supplies an interpretation compatible with both; the saved excerpt retains that context.

[Rashba’s first comment on 22b](https://he.wikisource.org/wiki/בבא_מציעא_כב_ב#חידושי_הרשב"א) records his alternative and temporal repair after discussing textual versions. The complete first comment, including editorial brackets visible in the transcription, is saved. No critical-edition or variant-adjudication claim is made.

[Rashi 26b, נטלה לפני יאוש](https://he.wikisource.org/wiki/בבא_מציעא_כו_ב#רש"י), says the finder may act before there has been time for purse checking. Q1 preserves the exact gloss. Habitual checking remains a defeasible presumption in the coins reply; C6 → C2 remains its factual attack, with no new coins undercut.

The three new excerpts were checked in the browser on 11 October 2026 and saved in [objections.json](../sources/objections.json). Only paragraph whitespace was collapsed before freezing the source text. Exact Hebrew wording, punctuation and brackets are retained. [anchors.json](../sources/anchors.json) binds each displayed span to its source SHA-256 and zero-based, end-exclusive Unicode code-point interval. Offsets address the saved transcription without further normalization. English remains our own paraphrase; editorial nodes have context-only anchors.

## The four undercuts

| View | Objection | Native inference target | What is contested |
| --- | --- | --- | --- |
| [Ritva](../argdown/11-river-objections.argdown) | J1, reported objection | JA, conclusion index 2 | Whether the verse’s exclusion is an explicit juxtaposition warranting the proposed comparison. |
| Ritva | J2, reported objection | JD, conclusion index 2 | Unrestricted transfer would prohibit ordinary loss even after actual despair; J3 records why that overreaches. |
| [Rashba / countermodel](../argdown/12-river-alternative.argdown) | L1, Rashba’s alternative | LA, conclusion index 1 | Nonredundancy alone need not establish all of KR4: explicit refusal to despair could supply another purpose for the exceptional permission. |
| Rashba / countermodel | L2, editorial countermodel | LB, conclusion index 1 | Exceptional permission does not by itself establish the ordinary unawareness prohibition. |

Indices here are the parser’s zero-based PCS conclusion indices. Each undercut is authored as `<_ [objection]` immediately after the relevant inference marker. Model JSON must record `relationType: undercut` and `toType: inference`; the rendered map must show the same objection targeting that argument’s inference. A purple arrow to a statement is not accepted as a substitute.

JA/JD separate the comparison from the unrestricted extension. JD’s overextended consequence is a stress test from the reported objection, **not Rashi’s actual qualified conclusion**. LA/LB likewise name editorial shortcuts under examination; Rashba is not labeled as directly attacking printed Tosafot.

The installed renderer dropped undercuts when a multi-step target was exploded into separate inference nodes. The final authoring uses one native argument per contested step, which preserves the precise inference targets in both model and map. Tests check exact edge sets and conclusion indices, and reject undercuts in all prior views.

## Explicit repairs and the countermodel

JB reconstructs Ritva’s repair from three named premises: J6 reads finding immediately after loss and before awareness; J7 states the comparative scope and exclusive irrecoverable-loss exemption in that case; J8 preserves the separate permission after awareness derived from **שמלה**. All three are used jointly. The source’s comparison and timing commitments are represented as interpretive premises, not silently proved by redundancy.

LC reconstructs Rashba’s repair from L4’s instant-of-loss reading and L5’s explicit comparative scope. Both are required. The resulting L6 records his conclusion under that reading. These diagrams expose the commitments of the repairs; they do not independently prove them.

L2 is an editorial countermodel, with illustrative cases checked in the test suite:

| Case | Permission in the countermodel |
| --- | --- |
| Irrecoverable loss, owner unaware, even marked | Yes |
| Irrecoverable loss, owner aware and refusing despair | Yes |
| Ordinary unmarked loss before awareness | Yes, consistent with Rava’s position |
| Ordinary marked loss before actual despair | No |
| Ordinary marked loss after established prior despair | Yes |

This grants the exceptional permission while denying the shortcut’s ordinary-unawareness conclusion. It illustrates insufficiency of that shortcut, not a complete legal theory or a disproof of the sugya. The earlier KR6 view keeps its condensed presentation of printed Tosafot; its inference annotation now explicitly says redundancy alone does not establish every part of KR4 and points to these views.

## Bounded scope

[Tosafot 22a, שטף נהר](https://he.wikisource.org/wiki/בבא_מציעא_כב_א#תוספות), was also checked. It challenges the negative inference from Rashi’s wording and offers its own reading. That **earlier** river exchange remains unencoded here; it is not conflated with the final 22b comparison. No figs/olives, further episodes, or general commentary survey were added.
