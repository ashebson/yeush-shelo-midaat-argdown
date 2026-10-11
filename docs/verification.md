# Verification record · 11 October 2026

The cloud completion now includes ten native Argdown views, an offline Graph / Code toggle and a [20-page PDF](yeush-shelo-midaat.pdf). No Mac access was used for implementation or QA. These checks establish artifact integrity and presentation behavior, not formal validity or a complete encoding of the sugya.

## Reproduction and results

Node 24.19.0, npm 11.9.0, Chromium 154.0.8037.57. Pinned official Argdown packages remain node 2.0.3, core 2.0.1 and CLI 2.0.0; official highlight-source uses the installed Argdown highlighter. No dependencies were added or upgraded.

```sh
python3 scripts/author-native.py
npm run build
npm run pdf
npm test
npx argdown 'argdown/*.argdown'
python3 scripts/visual-qa.py
```

Build, artifact validation and browser QA pass. The official CLI reports **Successfully checked 10 files**. The existing pinned dependency installation was reused. Whitespace checks pass. Parser counts match fresh outputs:

| View | Leaf nodes | Rendered relations | Parser / lexer errors |
| --- | ---: | ---: | ---: |
| 01-opening | 7 | 3 | 0 / 0 |
| 02-coins | 7 | 6 | 0 / 0 |
| 03-river | 8 | 7 | 0 / 0 |
| 04-opening-commentary | 7 | 6 | 0 / 0 |
| 05-coins-commentary | 3 | 2 | 0 / 0 |
| 06-river-commentary | 8 | 6 | 0 / 0 |
| 07-river-boundary | 4 | 3 | 0 / 0 |
| 08-coins-inference | 8 | 7 | 0 / 0 |
| 09-river-inference | 10 | 9 | 0 / 0 |
| overview | 22 | 18 | 0 / 0 |

## Native model and source integrity

The original 22-node/18-edge base ledger and eight Hebrew excerpts retain their original hashes. The authorized upgrade intentionally changes the four base Argdown presentation files: real PCS, metadata and native grouping replace comment-only provenance. The [numbered reconstruction ledger](../sources/reconstructions.json) adds C8 and R9 as editorial statements. The [modeling notes](native-argdown.md) explain this migration and exact semantics.

Tests check every ordered PCS statement, premise/intermediate/main-conclusion role, inference rule, source IDs and uses dependencies. C4 jointly uses three premises. R5 has two stages. KR6 is explicitly editorial synthesis of Rashi and Tosafot. All reused named propositions retain their original wording. KO7, KC2 and KB3 are accurately described as argument sketches. Ritva’s attribution names Shittah Mekubbetzet.

Tests separately compare explicit model relations and exact rendered edges. Native premise/conclusion edges replace duplicate explicit arrows. The overview’s C4 attack is intentionally transferred to C8 in the model and rendered as C4 → O5 because compact selection hides C8. C6 → C2 remains the coins reply’s sole rendered attack. O1–O3 and KR7 remain visible isolated notes. No extra propagation, undercuts, self-relations or fabricated commentator disagreements are accepted. Loose mode is retained.

Every node carries reference URLs, speaker, provenance class, Hebrew context anchor, temporal scope and source/base IDs. All 11 commentary excerpt hashes, author/source consistency and reference coverage are checked. Tests also verify the package/lock metadata, exact source/claim parity, fresh SVG/DOT/JSON and official highlighted HTML, embedded unique IDs, RTL blocks, local links and no network-dependent runtime resources. Source and HTML regeneration in a temporary directory catches stale output. Saved hashes are integrity checks, not a new live-source review.

## Browser and visual inspection

[Browser QA](qa/browser-report.json) passes at **1440 × 1000, 390 × 844 and 320 × 740**. All ten view selectors, Graph/Code tabs, arrow/Home/End keys, exact code text including trailing newline, actual clipboard contents, denied-clipboard manual selection, Fit/Read/+/−, scroll reachability and source disclosures were exercised. The same HTML works with networking disabled and makes zero external requests. No JavaScript errors or page-level horizontal overflow occurred. All SVG label bounding boxes fit inside their node shapes.

All ten maps were visually inspected in the PDF, with representative desktop/mobile viewer and source-panel screenshots inspected separately. The dense overview has three native groups and cross-episode links. On phones, Fit shows structure; Read/+ and scrolling are required for dense labels. Code scrolls horizontally inside its frame. Hebrew source disclosures use isolated RTL blocks; authors and English explanations remain readable.

Evidence: [desktop](qa/desktop.png), [river synthesis](qa/desktop-06-river-commentary.png), [coins inference](qa/map-08-coins-inference.png), [river inference on a phone](qa/mobile-09-river-inference.png), [Code on a phone](qa/code-390-02-coins.png), [Ritva Hebrew](qa/mobile-commentary-ri-possession.png), [Tosafot Hebrew](qa/mobile-commentary-to-compare.png).

Testing caught and fixed configuration leakage between Argdown builds: deep-cloning each request prevents native detail-view settings from contaminating the later overview. It also caught a minimum-zoom problem when the grouped overview fit below 10% on narrow phones. Zoom now returns correctly after +/−. The clipboard fallback uses a selected textarea so manual copying preserves the exact source, including its trailing newline.

All **20 PDF pages** were rendered and visually inspected. Minimum map type is **10.05 pt**; all claims and labels extract. No overflow, text outside page bounds or rasterized maps were found. The PDF has 55 link annotations and bookmarks. See [PDF verification](pdf-export.md), [export report](pdf-export-report.json) and [object report](qa/pdf-object-report.json).

## Deployment and environment limits

The repository is public and Pages was configured separately by the authorized deployment task. The [presentation](https://ashebson.github.io/yeush-shelo-midaat-argdown/) uses main/root and relative project-prefix paths. The release check command is:

```sh
python3 scripts/pages-qa.py --url https://ashebson.github.io/yeush-shelo-midaat-argdown/
```

That check compares deployed HTML, all ten SVGs, all ten authored sources and the PDF with the local release, then exercises Graph/Code and clipboard controls at all three viewports. Its output is stored in ignored `output/pages-qa/`; local checks alone are not deployment evidence.

Direct file navigation in this managed browser returns **net::ERR_BLOCKED_BY_ADMINISTRATOR**. Therefore direct double-click opening is not claimed as tested here. Loopback HTTP and a separate network-disabled HTML context were tested. Safari, Firefox, assistive technology certification and the user’s Mac were not tested. The cloud proxy also blocks GitHub API CONNECT requests; git transport and anonymous Pages requests are separate paths. No Pages administration was duplicated in this implementation.

## Dependency audit limitation

The previously saved [npm audit](qa/npm-audit.json) reports **12 affected development packages: 8 high and 4 moderate**. This is not a clean security audit. It concerns lodash-es, file-type and fast-xml-parser paths within the pinned Argdown authoring tools; no forced incompatible upgrade was applied. Dependencies are not bundled as browser JavaScript. These checks do not establish safety for arbitrary untrusted Argdown/XML/media. The dependency set is unchanged by this upgrade.
