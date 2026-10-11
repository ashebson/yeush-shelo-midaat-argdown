# Native Argdown modeling notes

The ten views use official Argdown parsing, modeling, Graphviz rendering and source highlighting. The complete [syntax reference](https://argdown.org/syntax/) and guides to [selection](https://argdown.org/guide/creating-statement-and-argument-nodes.html), [edges](https://argdown.org/guide/creating-edges.html), [inference trees](https://argdown.org/guide/creating-oldschool-argument-maps-and-inference-trees.html), [groups](https://argdown.org/guide/creating-group-nodes.html) and [embedding](https://argdown.org/guide/embedding-your-maps-in-a-webpage.html) informed this upgrade.

## What the numbered structures mean

| Argument | Numbered dependency | Interpretation |
| --- | --- | --- |
| C4, coins objection | C1, C2 and C3 jointly yield C8; `uses: [1,2,3]` | A conditional challenge. C2 is the disputed unawareness assumption; C6 attacks C2 directly. No undercut or established refutation of Abaye is asserted. |
| R5, final river comparison | R2 and R3 yield intermediate R9; R9 and R4 yield R6 | A supplied two-step reconstruction. The second step requires Rashi’s temporal qualification. River permission alone does not establish the ordinary-loss result. |
| KR6, Rashi/Tosafot synthesis | KR3 yields KR4; KR4, KR1 and KR2 jointly yield KR5 | The arrangement combines Tosafot’s redundancy reasoning with Rashi’s same-verse warrant and timing limit. It is explicitly editorial synthesis, not one commentator’s proof or a joint attributed ruling. |

The exact numbered statements, inference names, `uses`, source IDs and interpretive notes live in [reconstructions.json](../sources/reconstructions.json). Named statements reused across views retain identical wording and meaning. The extra C8 and R9 statements have new IDs and class R; they are not silently treated as Gemara quotations. KO7, KC2 and KB3 remain argument **sketches**, without numbered structures. Shape alone does not establish reconstruction status.

Inference rule names describe the editorial reading; Argdown does not verify them as a formal calculus. All views remain in **loose** mode. The Gemara’s refutation and ruling are recorded as source claims, not computed. No omitted episode or exhaustive commentary survey has been added.

## Native structure and selection

The overview uses three native episode groups and retains the original **22-node overview with cross-episode links**, 18 rendered relations, and isolated scope notes O1–O3. `excludeDisconnected: false` also preserves KR7 as an explanatory note. Compact views exclude only the additional C8/R9 statements from the map, while retaining them in the model and Code panel.

The two inference detail views use native tag selection, `statementSelectionMode: all` and `explodeArguments`. River commentary likewise displays both KR6 inference steps. Their arrows into a single inference node represent joint premises. The base river’s two generated nodes are R5 - 1 and R5 - 2; the corresponding commentary nodes are KR6 - 1 and KR6 - 2. The canonical source keeps each argument’s single ordered PCS.

Explicit supports replaced by PCS membership are no longer duplicated in the input. Argdown intentionally transfers the overview’s C4 attack to its C8 main conclusion in the model; because C8 is hidden in the compact map, the rendered attack remains C4 → O5. Tests distinguish model relations from rendered edges and check both exact sets. C6 → C2 remains the coins reply’s sole attack in the rendered views. No undercuts, self-relations or extra propagated attacks are accepted.

Each definition carries `sourceRef`, `sourceUrl`, `speaker`, `provenanceClass`, `hebrewAnchor`, `anchorScope`, `temporalScope`, `baseNodeIds`, `sourceIds` and `reconstructionStatus`. Hebrew anchors locate source context; they are not claims that editorial English is a literal quotation. Tags identify episode, provenance and commentator. Rashi’s explanations of Rava are not labeled Rashi’s own ruling; Ritva is explicitly attributed through **Shittah Mekubbetzet**.

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
