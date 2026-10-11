# Verification record · 11 October 2026

The selected three-episode demo was completed in the saved Linux cloud environment, continuing checkpoint `f016978348aa8b6facf225dc15c072441cec5065`. No Mac access was used. These checks establish artifact integrity and presentation behavior, not a formal proof or a complete encoding of the sugya.

The subsequently requested [15-page PDF with selected commentary](yeush-shelo-midaat.pdf) is also complete. See the [PDF export and inspection record](pdf-export.md) for page sizes, legibility checks, Hebrew inspection and reproduction instructions.

## Reproduction and results

Node **24.19.0**, npm **11.9.0**, Chromium **154.0.8037.57**. The pinned official Argdown packages remain unchanged: node 2.0.3, core 2.0.1, CLI 2.0.0.

```sh
npm ci
npm run build
npm run pdf
npm test
npx --no-install argdown 'argdown/*.argdown'
python3 scripts/visual-qa.py --browser /usr/bin/chromium
git diff --check
```

- The original clean dependency installation succeeded; the unchanged dependency set renders all eight current maps.
- `npm test` independently parses/renders the sources and compares them with the checked-in outputs. All checks passed.
- The official CLI reported: `Successfully checked 8 files.`
- Browser QA passed at 1440 × 1000, 390 × 844 and 320 × 740, with no page errors or external resource requests. See the [browser report](qa/browser-report.json).
- Whitespace/error checking with `git diff --check` passed.

| Map | Nodes | Relations | Parser / lexer errors |
| --- | ---: | ---: | ---: |
| Opening | 7 | 3 | 0 / 0 |
| Coins | 7 | 6 | 0 / 0 |
| River | 8 | 7 | 0 / 0 |
| Overview | 22 | 18 | 0 / 0 |
| Opening commentary | 7 | 6 | 0 / 0 |
| Coins commentary | 3 | 2 | 0 / 0 |
| River commentary | 7 | 5 | 0 / 0 |
| River boundary | 4 | 3 | 0 / 0 |

The [build report](build-report.json) matches a fresh parse. Fresh SVG, DOT and JSON outputs are byte-for-byte identical to the checked-in maps; the commentary extension did not alter the original four authored arguments, base ledger, Gemara excerpts or their generated maps.

## What the validator checks

[`scripts/validate.cjs`](../scripts/validate.cjs) checks exact node IDs, labels, kinds, text and provenance against the ledger; exact model and rendered relation sets; the expected counts above; and absence of extra relations or undercuts. It explicitly protects the coins attack **C6 → C2**, the cross-episode attacks **C4 → O5** and **R6 → O7**, and the direction of the Abaye/Rava relations. O1–O3 remain isolated scope notes. It does not require graph connectivity.

It also checks all eight excerpt SHA-256 values, Hebrew anchors against their cited saved excerpts, edition/license metadata, Argdown provenance comments, Rashi-expansion and supplied-bridge classes, SVG node/edge counts, build-report accuracy, package/lockfile root metadata, local document links, unique HTML/SVG IDs, RTL block markup, and absence of external runtime resources. The page is regenerated in a temporary directory and compared with `index.html` to catch stale presentation output. Hash checks establish that saved excerpts have not drifted; they are not a fresh live-source verification.

The previous source review is retained: Abaye rejects unconscious yeush; Rava accepts it in the disputed case. The coins reply attacks the unawareness premise. The final comparison is 22b:5–7, with R4/R6 attributed to Rashi and R5 marked as a supplied bridge. This completion preserves that content and adds no omitted episodes or formal-proof claims.

## Commentary extension

The user-requested layer adds Rashi, three Tosafot comments, Rashba and Ritva as quoted in Shittah Mekubbetzet. [Commentary notes](commentary-notes.md) list exact dibburim, excerpt boundaries and interpretation limits. Eleven classical Hebrew excerpts were independently inspected against the cited Wikisource daf pages. There are 21 new nodes (15 attributed C claims and six supplied R explanations) and 16 editorial support relations in four separate maps. No disagreement was invented and no new base episode was added.

The validator additionally checks the original six source-file hashes, unique commentary IDs, author/source consistency, visible attribution, complete per-view source appendices, valid base-node references, exact rendered commentary relations and all eleven excerpt hashes. Semantic guardrails retain Ritva’s possession/intent distinction, Rashi’s coins timing, Tosafot’s isolated explanation that Rava knew the baraita, and Rashba’s recoverability limit. These checks protect the authored interpretation; they do not independently adjudicate scholarship.

Every new standalone map, desktop view and phone view was opened for visual inspection. Node labels fit their shapes, arrows avoid labels and authors remain visible. Evidence: [opening](qa/map-04-opening-commentary.png), [coins](qa/map-05-coins-commentary.png), [river](qa/map-06-river-commentary.png), [boundary](qa/map-07-river-boundary.png). The phone Fit view shows overall structure; Read/+ is necessary for dense-map text. All eleven commentary source disclosures passed RTL, attribution and overflow checks at 320 px. Representative inspected excerpts: [Ritva](qa/mobile-commentary-ri-possession.png), [Tosafot](qa/mobile-commentary-to-compare.png), [Rashba](qa/mobile-commentary-rb-boundary.png). Mixed Hebrew was removed from the letter-spaced map eyebrow; exact Hebrew dibburim remain in the source ledger.

All 15 PDF pages were rendered and visually inspected, with eight vector maps and complete base/commentary claim extraction. The new river page was changed to portrait after the font-size check rejected the first export. See [PDF verification](pdf-export.md). No Node dependency versions or audit findings were changed by this addition.

## Visual inspection and fixes

The screenshots were opened and visually inspected, in addition to automated DOM/geometry checks. Standalone exports were inspected in full; enlarged embedded maps intentionally scroll within their frame.

| Inspected view | Result and evidence |
| --- | --- |
| Desktop presentation | Header, Hebrew title, navigation and zoom controls render clearly: [desktop](qa/desktop.png). |
| Opening | All seven nodes and three relations visible, O1–O3 isolated; no label clipping: [presentation](qa/desktop-01-opening.png), [complete SVG capture](qa/map-01-opening.png). |
| Coins | The red C6 → C2 attack and supporting paths are distinct; no text/shape overlaps: [presentation](qa/desktop-02-coins.png), [complete SVG capture](qa/map-02-coins.png). |
| River | Fit now displays the entire chain through R7/R8, including the refutation and ruling: [presentation](qa/desktop-03-river.png), [complete SVG capture](qa/map-03-river.png). |
| Overview | All 22 nodes and 18 relations visible, with distinct cross-episode attacks: [presentation](qa/desktop-overview.png), [complete SVG capture](qa/map-overview.png). |
| Phone layout | Prose and controls stay within the page; Fit shows the complete graph: [opening](qa/mobile-01-opening.png), [coins](qa/mobile-02-coins.png), [river](qa/mobile-03-river.png), [overview](qa/mobile-overview.png). |
| Hebrew and provenance | Right-to-left ordering and wrapping are readable; English remains left to right. Rashi and supplied-bridge attribution stays visible: [Hebrew excerpt](qa/mobile-hebrew.png), [O5](qa/mobile-ledger-O5.png), [R4](qa/mobile-ledger-R4.png), [R5](qa/mobile-ledger-R5.png). |

The initial page's Fit button only reset width, so the tall river map hid its conclusion below the frame and the mobile minimum width prevented a true fit. Fit now uses both frame dimensions. Read restores native label size (14 px in the embedded SVG); +/− adjust it, and all corners remain reachable by scrolling. Tabs reset to Fit. Phones and the dense overview require Read/+ and scrolling for detailed reading; Fit prioritizes the overall structure. This is not a claim that every label is readable at phone-width fit scale.

The generated page also now prefixes embedded SVG IDs by episode to remove duplicate IDs, uses 44 px zoom-button targets, and removes link-arrow glyphs that appeared as missing-glyph boxes in the cloud browser. README and the overview heading now describe cross-episode links rather than a connected graph. The lockfile license and Node engine metadata were reconciled without changing dependency versions.

Automated browser checks exercise all eight tabs, keyboard activation, Fit/Read/+/−, scroll reachability, ledger expansion, Rashi and bridge attribution, and isolated RTL blocks at each viewport. Every SVG text bounding box remains within its node's shape bounds. No page-level horizontal overflow was observed. The screenshots provide the complementary visual check for overlaps and directionality; this is not a cross-browser or screen-reader certification.

## Offline check and environment limits

The page embeds its CSS, JavaScript and all eight SVGs. The identical HTML was loaded into a Chromium context with networking disabled; tabs, zoom and ledger expansion worked and made zero network requests. Local document/SVG links resolve in the repository. Source links naturally require a connection.

Direct `file://` navigation in this managed browser returned **`net::ERR_BLOCKED_BY_ADMINISTRATOR`**. Therefore direct double-click/file opening is **not claimed as browser-tested here**. Interactive and visual inspection used a loopback-only HTTP server; the separate network-disabled test verified the self-contained HTML. No public hosting was created. Safari, Firefox and the user's Mac have not been tested in this completion.

The shell's GitHub REST/GraphQL metadata calls returned `Forbidden`; the authorized GitHub connector successfully confirmed `ashebson/yeush-shelo-midaat-argdown` has **private** visibility and default branch `main`. Git transport was available. Repository visibility and access were not changed.

## Dependency audit limitation

`npm audit --json` reported **12 affected packages: 8 high and 4 moderate, 0 critical**. This check has a nonzero exit status because advisories remain; it is not represented as a clean security audit. The [saved audit report](qa/npm-audit.json) records exact dependency paths, ranges and advisory URLs.

The underlying advisories involve `lodash-es` (template-import code injection and path-based prototype pollution), `file-type` (malformed ASF infinite loop), and `fast-xml-parser` (XMLBuilder comment/CDATA injection). Other affected packages inherit those advisories through the Argdown authoring toolchain. npm reports no available fix for the pinned top-level `@argdown/node` and `@argdown/cli` package paths. No forced or incompatible upgrades were applied.

All installed packages are development tooling. None of those dependencies is embedded as browser JavaScript in the exported presentation. The build here processed the repository's authored inputs; this verification does not establish exploitability or non-exploitability for arbitrary untrusted Argdown, XML or media. Dependency remediation remains a tooling limitation, not an unreported passing check.
