# Selected commentary · a separate layer

The original three-episode reconstruction remains **22 nodes / 18 relations**. Four additional maps contain **21 commentary nodes / 16 editorial support relations**: 15 attributed paraphrases (**C**) and six supplied mapping explanations or syntheses (**R**). They add no relations to the Gemara overview. This is selected commentary on the opening, scattered coins and final river comparison, not an exhaustive edition or formal proof.

## Coverage and sources

Checked against the classical Hebrew on [Wikisource 21b](https://he.wikisource.org/wiki/בבא_מציעא_כא_ב) and [22b](https://he.wikisource.org/wiki/בבא_מציעא_כב_ב), 11 October 2026. The [commentary ledger](../sources/commentary.json) preserves author, exact daf/dibbur, source URL, excerpt boundaries, context, edition attribution and SHA-256 for eleven Hebrew excerpts. English is our own paraphrase. The excerpts are reproduced in the offline HTML and PDF pages 12–15.

| Map | Commentary included | Interpretive contribution |
| --- | --- | --- |
| [Opening](../argdown/04-opening-commentary.argdown) | Rashi 21b, **יאוש שלא מדעת**, **מהשתא הוי יאוש**; Tosafot 21b, **דלכי נפל מיניה לא מיאש**; Ritva through Shittah Mekubbetzet 21b, paragraph beginning **ורבא אמר הוי יאוש כיון דלכי ידע לא סגי דלא מייאש** | Time of discovery; Rava’s anticipated response; contingent later despair over a marked object; possession for the owner and why later despair cannot cure pickup. |
| [Coins](../argdown/05-coins-commentary.argdown) | Rashi 21b, **עשוי למשמש** | Awareness and despair precede discovery. Two explicitly supplied nodes locate the effect on the base unawareness premise. |
| [Final river comparison](../argdown/06-river-commentary.argdown) | Rashi 22b, **ואיסורא דומיא דהיתירא**, **אף איסורא**; Tosafot 22b, **איסורא דומיא דהתירא**, **תיובתא דרבא** | Same-verse warrant and temporal limit; why the special verse must add permission without awareness; Rava knew the source but missed the comparison. |
| [River boundary](../argdown/07-river-boundary.argdown) | Rashba 21b, **זוטו של ים ושלוליתו של נהר … רחמנא אפקריה** | Scriptural ownerlessness even over the owner’s protest; genuinely recoverable loss differs from loss to everyone. |

## Qualifications preserved

Rashi’s **מהשתא** explains Rava’s position; it is not represented as Rashi ruling for Rava. Tosafot’s marked-object comment qualifies an overbroad extension of that position, without inventing a dispute with Rashi. Ritva’s explanation applies where unconscious despair is ineffective: unmarked loss for Abaye and marked loss for both. His account of **באיסורא** concerns the object remaining in the owner’s domain, not necessarily intentional theft. His marked-item duty to pick up is not generalized to every unmarked find. We attribute him through **Shittah Mekubbetzet**, which labels the passage הריטב״א; no standalone Ritva edition was verified.

The coins commentary concerns **21b:7**. Tosafot’s **ת״ש המוצא מעות כו׳** comments on the later synagogue/study-house baraita and is deliberately excluded. We retain the original C6 → C2 factual attack and the Mishnah’s claim; no undercut or new refutation of Abaye is added.

Tosafot’s final river explanation contains one connected argument: ordinary conscious despair already permits acquisition, so the special verse cannot be confined to that case; the exceptional permission therefore includes unawareness, and the ordinary prohibition is compared with it. Rashi supplies the same-verse warrant and awareness-before-pickup qualification. KR6 is our synthesis, not a quotation. KR7 is an isolated explanatory note about what Rava missed, not another proof. None of this makes river permission alone a refutation or forbids all unmarked finds.

Rashba’s complete ownerlessness concerns **true loss to everyone**. His Biran River and sand examples test recoverability; they do not license every river find. The saved closing excerpt concerns siftable sand. These later examples are commentary context, not new Gemara episodes. This selected reading does not purport to resolve all other commentators’ treatments of the exception or textual variants of the final comparison.

All arrows are our editorial support/explanation choices in Argdown’s loose mode. Selected passages mostly explain or qualify; no disagreement between these authors has been manufactured. Unselected commentators and intervening sugya challenges, including figs/olives, remain outside this demo.

## Editing and preservation

Edit `sources/commentary.json`, then run:

```sh
python3 scripts/author-native.py
npm run build
npm run pdf
npm test
python3 scripts/visual-qa.py
```

The native author script regenerates all ten views from the scholarly ledgers. Original base-ledger and Gemara-excerpt hashes remain protected; the four base presentation-source files intentionally gained metadata and numbered PCS in the authorized upgrade. KR6 is now an explicitly editorial two-step synthesis displayed through native inference expansion; KO7, KC2 and KB3 remain sketches. See [native modeling notes](native-argdown.md). The validator checks exact claim wording, attribution, citation coverage, numbered dependencies and model/rendered edges separately. Hashes protect saved-text integrity; source fidelity rests on the documented reading of the cited Hebrew.
