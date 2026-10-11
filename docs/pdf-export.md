# PDF edition and export record

[Open the 20-page PDF](yeush-shelo-midaat.pdf).

The edition includes all ten vector maps, base and commentary Hebrew sources, and three readable numbered premise–conclusion reconstructions. Source claims, attributed explanations and editorial synthesis remain distinct. This is a bounded reading of three selected episodes, not a formal proof or complete encoding of the sugya.

## Page plan and measured type

| Page | Content | Page size | Minimum map type |
| --- | --- | --- | ---: |
| 1 | cover | 210 × 297 mm | — |
| 2 | overview | 841 × 594 mm | 11.20 pt |
| 3 | 01-opening | 420 × 297 mm | 12.05 pt |
| 4 | 02-coins | 420 × 297 mm | 11.71 pt |
| 5 | 03-river | 297 × 420 mm | 12.53 pt |
| 6 | provenance | 210 × 297 mm | — |
| 7 | primary-text | 210 × 297 mm | — |
| 8 | 04-opening-commentary | 420 × 297 mm | 10.86 pt |
| 9 | 05-coins-commentary | 297 × 420 mm | 19.76 pt |
| 10 | 06-river-commentary | 420 × 420 mm | 14.38 pt |
| 11 | 07-river-boundary | 420 × 297 mm | 10.05 pt |
| 12 | 04-opening-commentary-sources | 210 × 297 mm | — |
| 13 | 05-coins-commentary-sources | 210 × 297 mm | — |
| 14 | 06-river-commentary-sources | 210 × 297 mm | — |
| 15 | 07-river-boundary-sources | 210 × 297 mm | — |
| 16 | 08-coins-inference | 420 × 297 mm | 11.19 pt |
| 17 | 09-river-inference | 297 × 420 mm | 10.68 pt |
| 18 | pcs-C4 | 210 × 297 mm | — |
| 19 | pcs-R5 | 210 × 297 mm | — |
| 20 | pcs-KR6 | 210 × 297 mm | — |

The grouped overview uses an A1 landscape foldout to keep all labels above 10 pt; the first A2 attempt failed that check. Most episode maps use A3; the two-step commentary map uses a 420 × 420 mm page. View pages individually and zoom, or print at actual size. Shrinking the overview onto A4 makes its labels small. Source and numbered-argument pages use A4. Hebrew excerpts retain 12.75 pt text and isolated RTL blocks.

## Regenerate

Use Node build dependencies, Python 3, Chromium and the pinned optional packages in [requirements-pdf.txt](../scripts/requirements-pdf.txt):

```sh
python3 scripts/author-native.py
npm run build
npm run pdf -- --browser /usr/bin/chromium
npm test
pdftoppm -scale-to 1600 -png docs/yeush-shelo-midaat.pdf output/pdf/native
```

If needed, install the optional Python packages in a virtual environment. The exporter reads generated HTML, ten SVGs and three scholarly ledgers. Chromium runs with networking disabled; pages print separately and pypdf combines them with bookmarks. Input/PDF hashes, geometry and versions are in [pdf-export-report.json](pdf-export-report.json). Intermediate files stay under ignored `output/pdf/`. Byte-identical reproduction across different platforms is not promised.

## Inspection · 11 October 2026

All 20 pages were rendered with Poppler and opened for visual inspection. Map labels, shapes, relation routing and isolated notes are visible; no label clipping was found. Hebrew direction, wrapping, source attribution and footers were reviewed. The numbered C4, R5 and KR6 pages preserve inference rules, joint uses dependencies and editorial qualifications. Every base, commentary and additional C8/R9 label and complete claim survives text extraction.

The exporter recorded no overflow, external requests or page errors. The minimum map label size is 10.05 pt. The [PDF-object report](qa/pdf-object-report.json) confirms 20 pages, 55 link annotations, no text outside page bounds and no raster images. Figures remain vectors with selectable text. Chromium 154.0.8037.57, Playwright 1.62.0, pypdf 6.10.0 and PyMuPDF 1.26.6 were used. PDF/UA or screen-reader certification is not claimed.
