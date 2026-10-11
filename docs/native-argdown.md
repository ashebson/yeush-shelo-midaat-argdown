# Native Argdown modeling notes

The thirteen views use official Argdown parsing, modeling, Graphviz rendering and source highlighting. The complete [syntax reference](https://argdown.org/syntax/) and guides to [selection](https://argdown.org/guide/creating-statement-and-argument-nodes.html), [edges](https://argdown.org/guide/creating-edges.html), [inference trees](https://argdown.org/guide/creating-oldschool-argument-maps-and-inference-trees.html), [groups](https://argdown.org/guide/creating-group-nodes.html) and [embedding](https://argdown.org/guide/embedding-your-maps-in-a-webpage.html) informed this upgrade.

## What the numbered structures mean

| Argument | Numbered dependency | Interpretation |
| --- | --- | --- |
| OA, Abaye | O4 (present unawareness) and supplied O9 jointly yield O5 | O9 explicitly supplies awareness as necessary within the ordinary unmarked dispute; it is not an independently proved or quoted premise. |
| OB, Rava | O6 (expected future despair) and supplied O10 jointly yield O7 | O10 explicitly supplies the anticipatory legal bridge within the same scope; this reconstructs the stated position, not a proof that it is correct. |
| C4, coins objection | C1, C2 and C3 jointly yield C8; `uses: [1,2,3]` | A conditional challenge. C2 is the disputed unawareness assumption; C6 attacks C2 directly. No undercut or established refutation of Abaye is asserted. |
| R5, final river comparison | R2 and R3 yield intermediate R9; R9 and R4 yield R6 | A supplied two-step reconstruction. The second step requires Rashi’s temporal qualification. River permission alone does not establish the ordinary-loss result. |
| KR6, Rashi/Tosafot synthesis | KR3 precedes KR4 in the condensed reading; KR4, KR1 and KR2 jointly yield KR5 | The first transition records Tosafot’s reading, not an entailment from nonredundancy alone; the separate objection views expose its missing warrants. The arrangement combines this reading with Rashi’s same-verse warrant and timing limit. It is explicitly editorial synthesis, not one commentator’s proof or a joint attributed ruling. |

The exact numbered statements, inference names, `uses`, source IDs and interpretive notes live in [reconstructions.json](../sources/reconstructions.json). Named statements reused across views retain identical wording and meaning. The extra C8 and R9 statements have new IDs and class R; they are not silently treated as Gemara quotations. KO7, KC2 and KB3 remain argument **sketches**, without numbered structures. Shape alone does not establish reconstruction status.

Inference rule names describe the editorial reading; Argdown does not verify them as a formal calculus. All views remain in **loose** mode. The Gemara’s refutation and ruling are recorded as source claims, not computed. No omitted episode or exhaustive commentary survey has been added.

## Native structure and selection

The overview uses three native episode groups and retains the original **22-node overview with cross-episode links**, 18 rendered relations, and isolated scope notes O1–O3. `excludeDisconnected: false` also preserves KR7 as an explanatory note. Compact views exclude only the additional C8/R9 statements from the map, while retaining them in the model and Code panel.

The three inference detail views use native tag selection, `statementSelectionMode: all` and `explodeArguments`. River commentary likewise displays both KR6 inference steps. Their arrows into a single inference node represent joint premises. The base river’s two generated nodes are R5 - 1 and R5 - 2; the corresponding commentary nodes are KR6 - 1 and KR6 - 2. The canonical source keeps each argument’s single ordered PCS.

Explicit supports replaced by PCS membership are no longer duplicated in the input. Argdown intentionally transfers the overview’s C4 attack to its C8 main conclusion in the model; because C8 is hidden in the compact map, the rendered attack remains C4 → O5. Tests distinguish model relations from rendered edges and check both exact sets. C6 → C2 remains the coins reply’s sole attack in the rendered views. Only the four source-grounded/editorial undercuts specified in the new objection layer are accepted; prior views retain no undercuts. Self-relations and extra propagated attacks remain rejected.

Each definition carries `sourceRef`, `sourceUrl`, `speaker`, `provenanceClass`, `hebrewAnchor`, `anchorScope`, `temporalScope`, `baseNodeIds`, `sourceIds` and `reconstructionStatus`. Hebrew anchors locate source context; they are not claims that editorial English is a literal quotation. Tags identify episode, provenance and commentator. Rashi’s explanations of Rava are not labeled Rashi’s own ruling; Ritva is explicitly attributed through **Shittah Mekubbetzet**.

## Exact Hebrew evidence

[anchors.json](../sources/anchors.json) assigns all 71 claim records 96 exact saved-source spans. Every span has a source ID, SHA-256 of the complete saved text, start/end code-point offsets, verbatim quotation and its evidentiary purpose. Offsets are zero-based, start inclusive and end exclusive, with no normalization. JavaScript validation uses `Array.from(text)` rather than UTF-16 string indexing. The full `hebrewAnchors` array is carried into authored Argdown and model JSON; `hebrewAnchor` retains the first span for compatibility. HTML cards render the same intervals, with isolated RTL Hebrew.

KR3, KR4 and KR5 select distinct successive portions of Tosafot’s argument. R4 includes the awareness-before-pickup clause. KO4 selects scope/custody; KO5 later despair and holding for the owner; KO6 non-theft and the owner’s continued domain. These are attributed English paraphrases supported by verbatim Hebrew. Class R claims, including O9/O10 and all synthesis nodes, explicitly use **editorial context**, never an attributed quotation of their English claim.

The opening detail preserves O1–O3 as isolated scope notes and O5 → O7 as the existing opposition. It replaces the two direct rationale-to-conclusion arrows only inside the detailed view. The original opening and 22-node overview retain their counts and wording.

## Review of remaining sketches

KO7 juxtaposes distinct timing, marked-loss and custody qualifications; treating them as joint premises of a single legal inference would overstate this selected reading. KC2 explains why Rashi’s awareness timing changes C2; the actual attack remains C6 → C2, and the coins objection already has its numbered reconstruction. KB3 compares Rashba’s recoverability boundaries; those examples do not independently establish the final ordinary-loss prohibition. These three remain explicitly labeled editorial argument sketches. No invented conclusion, undercut or strict-mode semantics was added to force a numbered structure.

## Editing and integrity

Edit the scholarly ledgers, then run:

```sh
python3 scripts/author-native.py
npm run build
npm run pdf
npm test
python3 scripts/visual-qa.py
```

The original base claim/relation ledger and Gemara excerpt files retain their existing SHA-256 checks. The prior byte locks on four presentation-source files were replaced by fresh-generation checks because this authorized upgrade changes their native syntax. Commentary excerpt hashes are unchanged. Do not edit generated SVG, JSON or highlighted source HTML manually.

Graph / Code switches between the SVG and **the exact corresponding authored `.argdown`**, including frontmatter. The official `highlight-source` process runs during the build; its escaped markup is embedded in the offline HTML. Copy uses the displayed code’s text, including whitespace and trailing newline. Arrow keys, Home and End operate the display tabs. Clipboard restrictions produce an honest selection/manual-copy fallback. No CDN, runtime parser or network fetch is required. Relative asset/source links work beneath the GitHub Pages project prefix.

Every build invocation deep-clones its configuration. Argdown’s plugins mutate request settings; shallow sharing would allow a preceding inference view’s tag selection or explosion setting to contaminate later maps. Exact overview counts and model tests protect against this regression.

## Native undercuts and repairs

The two [objection-and-repair views](objections.md) add six single-inference arguments: JA, JD, JB, LA, LB and LC. Four objections target specific inference markers, with exact `toType: inference` and `conclusionIndex` assertions. JB uses timing, comparative scope and separate permission jointly; LC uses both temporal and comparative premises. The 11 existing SVGs are hash-checked as unchanged. There are now 13 views, 11 numbered arguments, 71 evidence records and 96 exact Hebrew spans. The scholarly corpus comprises eight Gemara excerpts and fourteen commentary excerpts.
