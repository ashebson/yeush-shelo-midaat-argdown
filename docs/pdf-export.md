# PDF edition and export record

[Open the 15-page PDF](yeush-shelo-midaat.pdf).

The edition preserves the original four SVG maps and adds four separate commentary maps with Rashi, three Tosafot comments, Rashba, and Ritva through Shittah Mekubbetzet. Figures remain vectors with selectable text. Base reconstruction and commentary are clearly separated; source ledgers identify supplied bridges, exact authors and Hebrew excerpts. This is a bounded reconstruction, not a formal proof or complete encoding of the sugya.

## Page plan

| Page | Content | Page size | Minimum map label size |
| --- | --- | --- | ---: |
| 1 | Reader’s guide | A4 portrait | — |
| 2 | 22-node overview with cross-episode links | A2 landscape foldout | 11.03 pt |
| 3 | Opening dispute and scope notes | A3 landscape | 12.05 pt |
| 4 | Scattered coins | A3 landscape | 11.71 pt |
| 5 | Final river comparison | A3 portrait | 12.53 pt |
| 6 | Base provenance and boundaries | A4 portrait | — |
| 7 | Eight Gemara excerpts | A4 portrait | — |
| 8 | Opening commentary: Rashi, Tosafot, Ritva via Shittah | A3 landscape | 11.37 pt |
| 9 | Coins commentary: Rashi and supplied mapping explanation | A3 portrait | 19.76 pt |
| 10 | River commentary: Rashi and Tosafot | A3 portrait | 10.14 pt |
| 11 | River boundary: Rashba and supplied qualification | A3 landscape | 10.05 pt |
| 12–15 | Commentary Hebrew excerpts with exact attribution and context | A4 portrait | — |

Large map pages preserve the complete claims. View pages individually, zoom, or print at actual size. Shrinking A2 to A4 makes labels small. Hebrew excerpts use 12.75 pt type with isolated RTL direction. There are eleven unique commentary excerpts; Rashi’s same-verse explanation is repeated on page 15 to document the source of the supplied KB4 qualification.

## Regenerate

Requirements: Node build dependencies, Python 3, Chromium and the pinned optional packages in [requirements-pdf.txt](../scripts/requirements-pdf.txt). No Node dependencies were changed for this export.

```sh
npm ci
npm run build
python3 -m venv .venv-pdf
.venv-pdf/bin/python -m pip install -r scripts/requirements-pdf.txt
.venv-pdf/bin/python scripts/export-pdf.py --browser /usr/bin/chromium
npm test
```

Supply your Chromium/Chrome executable on other systems. If packages are available to `python3`, use `npm run pdf -- --browser /path/to/chromium`.

The exporter reads the generated HTML, eight SVGs and source ledgers. Chromium runs with networking disabled. Each intentionally sized page is printed separately, then pypdf assembles the document with bookmarks. Outputs are the PDF and [pdf-export-report.json](pdf-export-report.json); intermediate HTML/PDF files remain in ignored `output/pdf/`.

The report records input and PDF SHA-256 hashes, dimensions, minimum map font sizes and tool versions. `npm test` checks the hashes to reject stale exports. PDF metadata and fonts can differ by environment; byte-identical reproduction across machines is not promised.

## Inspection · 11 October 2026

All 15 final pages were rendered with Poppler and opened for visual inspection. All eight figures were reviewed for label size, node boundaries, relation routing and legend consistency. The original Gemara sources, labels and relations remain unchanged. Commentary claims and arrows were checked separately; no edges were added to the base overview. Source appendices were inspected for Hebrew ordering, wrapping, author attribution, clipping and footers.

The first commentary export made the new river map too small (7.98 pt). Its page was changed from A3 landscape to portrait; the final minimum is 10.14 pt. Compact A4 source pages retain the Hebrew at 12.75 pt. The final export passes the 10 pt map-text floor, contains exactly 15 pages, and retains all **22 base and 21 commentary labels and full claims** in extracted text. No page overflows or external requests occurred. The PDF-object review found no text outside page bounds and zero raster images. See [pdf-object-report.json](qa/pdf-object-report.json).

```sh
pdftoppm -scale-to 1600 -png docs/yeush-shelo-midaat.pdf output/pdf/expanded
pdfinfo docs/yeush-shelo-midaat.pdf
```

Verified with Chromium 154.0.8037.57, Playwright 1.62.0, pypdf 6.10.0 and PyMuPDF 1.26.6. Bookmarks and selectable text are present; PDF/UA or tagged-accessibility certification is not claimed. No public hosting or visibility changes were performed.
