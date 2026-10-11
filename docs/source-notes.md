# Source notes and interpretive boundaries

Verified on 11 October 2026 against the unvocalized **Wikisource Talmud Bavli** edition through Sefaria and Hebrew Wikisource. English node text is original analytical paraphrase, not a published translation.

## Passage and source ledger

- [Bava Metzia 21b](https://www.sefaria.org/Bava_Metzia.21b?vhe=Wikisource_Talmud_Bavli), especially segments 1–4 and 7.
- [Bava Metzia 22b:5–7](https://www.sefaria.org/Bava_Metzia.22b.5-7?vhe=Wikisource_Talmud_Bavli).
- Hebrew Wikisource: [כא ב](https://he.wikisource.org/wiki/בבא_מציעא_כא_ב), [כב ב](https://he.wikisource.org/wiki/בבא_מציעא_כב_ב).
- [Rashi on Bava Metzia 22b:6:1–3](https://www.sefaria.org/Rashi_on_Bava_Metzia.22b.6.1-3), especially **אף איסורא**; on 21b, **עשוי למשמש**, visible on the Hebrew Wikisource 21b page.
- [Deuteronomy 22:3](https://www.sefaria.org/Deuteronomy.22.3), as cited and interpreted by the Gemara.

`sources/model.json` provides the complete node ledger and explicit edge list. `sources/hebrew-excerpts.json` preserves only the selected Hebrew/Aramaic segments with edition, license metadata, URL, retrieval date and SHA-256. No English API translation is included. Segment numbers are Sefaria references; daf references remain usable across editions.

## S, E and R are provenance classes

**S — Source:** an explicit claim or question in the Gemara, in our short paraphrase. An S label does not imply that a question's premise is accepted. C2 is the anonymous objection's assumption, later answered.

**E — Explanation:** explanatory wording added to make an elliptical passage accessible. C6 spells out awareness and despair before discovery, following Rashi's **עשוי למשמש** on 21b. R4 and R6 spell out the ordinary-loss prohibition's temporal qualification, following Rashi's **אף איסורא** on 22b. These are commentator-supported expansions; they must not be presented as verbatim Gemara or as a modern translator's independent evidence. No modern translator expansion is imported into this project.

**R — Reconstruction:** an analytical bridge, argument summary, or local assessment supplied by this demo. C3 is the explicit bridge from permission while unaware to a challenge to Abaye. C4 collects the objection; C7 records why that particular objection no longer decides the dispute. R5 makes the river comparison usable as an argument under the temporal qualification in R4.

All graph edges are editorial reconstruction, even between S nodes. The sources do not contain arrows or this taxonomy.

## Opening: scope matters

O1 confines the dispute to ordinary objects lacking a **סימן**, an identifying mark. O2 preserves the agreed marked-object case: when an object reaches the finder before legitimate acquisition is possible, later despair does not cure that pickup. The owner initially expects recovery using the mark. This is not a claim that marked objects can never be acquired after conscious despair.

O3 preserves the separate Torah-permitted sea/river category. The criterion is loss inaccessible to everyone, not simply contact with water. Its permission is not an instance proving Rava's unconscious-yeush rule. The three scope nodes are deliberately isolated; scope is not drawn as evidential support for a disputed conclusion.

O4 → O5 and O6 → O7 are compact source-level reason/conclusion summaries. The opposing conclusions remain attributed to Abaye and Rava. The overview is a dialectical record, not a set of jointly true propositions.

## Coins: attack the right target

C1 is the accepted Mishnah permission. C2 is the objection's assumed unawareness. C3 makes the bridge explicit. Together they support C4, whose attack targets Abaye's O5 in the overview.

The reply cites Rabbi Yitzhak's habitual purse checking (C5). Its application treats awareness and despair as preceding the find (C6; Rashi). The red relation **C6 → C2** attacks the factual premise. It does not attack C1, and it is not an undercut of C4's inference. Habitual checking is the sugya's factual generalization, not a modern measured probability or a universal empirical guarantee. C7 is a local result: this challenge does not decide between the positions. It is not an independent proof of Abaye.

The anonymous objection and answer belong to the Gemara's dialogue. We do not attribute them automatically to Abaye or Rava.

## River: permission alone is insufficient

R1–R2 state the verse-based distinction, transmitted by Rabbi Yohanan in the name of Rabbi Yishmael ben Yehotzadak in this edition. R3 is the Gemara's explicit comparison **ואיסורא דומיא דהיתירא**: the prohibition parallels the permission with respect to presence or absence of a mark.

R4, following Rashi, supplies the operative temporal qualification: the ordinary-loss case is one in which the owner has not learned of the loss before pickup. R5 reconstructs application of the comparison in that setting. R6 therefore includes unmarked, ordinarily recoverable loss within the prohibition. This conclusion conflicts with Rava's O7. It is not a universal prohibition on keeping any unmarked object, and it does not erase the role of prior conscious yeush.

R7 preserves the explicit **תיובתא דרבא תיובתא**. R8 preserves the ensuing ruling for Abaye, **והלכתא כוותיה דאביי ביע״ל קג״ם**. The arrow from refutation to ruling records the justificatory flow of this passage; it is not a rule for computing halakhah from graph acceptance.

This final river proof is **22b:5–7**, not the earlier river-loss discussion on 22a. The presentation makes no claim to encode all intervening lines or all later halakhic qualifications.

## Deliberate omissions

The optional figs/olives/carobs episode (21b:13–16) is omitted to keep 22 overview nodes. It would add another instructive premise dispute: appearance identifies the source tree, weakening the expectation of future despair; Rav Pappa distinguishes figs because they become disagreeable when they fall. Other omissions include scattered fruit, heavy/valuable objects, public-place coins, gleanings, the exchanges on 22a, dew/consent, and the post-ruling windfall dates discussion. No conclusions about these omitted arguments are inferred from their absence.
