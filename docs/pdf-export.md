# PDF edition and export record

[Open the 30-page PDF](yeush-shelo-midaat.pdf).

The edition includes all thirteen vector maps, base and commentary Hebrew sources, five readable numbered premise–conclusion reconstructions two exact Hebrew anchor appendices, and five pages of contested inferences and sources. Source claims, attributed explanations and editorial synthesis remain distinct. This is a bounded reading of three selected episodes, not a formal proof or complete encoding of the sugya.

## Page plan and measured type

| Page | Content | Page size | Minimum map type |
| --- | --- | --- | ---: |
| 1 | cover | 210 × 297 mm | — |
| 2 | overview | 841 × 594 mm | 11.20 pt |
| 3 | 01-opening | 420 × 297 mm | 12.05 pt |
| 4 | 02-coins | 420 × 297 mm | 11.27 pt |
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
| 18 | 10-opening-inference | 594 × 420 mm | 12.71 pt |
| 19 | pcs-C4 | 210 × 297 mm | — |
| 20 | pcs-R5 | 210 × 297 mm | — |
| 21 | pcs-KR6 | 210 × 297 mm | — |
| 22 | pcs-OA | 210 × 297 mm | — |
| 23 | pcs-OB | 210 × 297 mm | — |
| 24 | anchors-R4 | 210 × 297 mm | — |
| 25 | anchors-KO4 | 210 × 297 mm | — |
| 26 | 11-river-objections | 594 × 420 mm | 12.91 pt |
| 27 | 12-river-alternative | 594 × 420 mm | 14.60 pt |
| 28 | ri-22b-repair | 210 × 297 mm | — |
| 29 | rb-22b-repair | 210 × 297 mm | — |
| 30 | objection-guide | 210 × 297 mm | — |

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

If needed, install the optional Python packages in a virtual environment. The exporter reads generated HTML, thirteen SVGs and six source ledgers. Chromium runs with networking disabled; pages print separately and pypdf combines them with bookmarks. Input/PDF hashes, geometry and versions are in [pdf-export-report.json](pdf-export-report.json). Intermediate files stay under ignored `output/pdf/`. Byte-identical reproduction across different platforms is not promised.

## Inspection · 11 October 2026

All 30 pages were rendered with PyMuPDF. The new objection maps, Hebrew sources, guide and changed earlier pages were opened for visual inspection; the earlier eleven SVGs match their previously inspected hashes. Map labels, shapes, relation routing and isolated notes are visible; no label clipping was found. Hebrew direction, wrapping, source attribution and footers were reviewed. The numbered C4, R5, KR6, OA and OB pages preserve inference rules, joint uses dependencies and editorial qualifications. Every base, commentary and editorial addition label and complete claim survives text extraction.

The exporter recorded no overflow, external requests or page errors. The minimum map label size is 10.05 pt. The [PDF-object report](qa/pdf-object-report.json) confirms 30 pages, 83 link annotations, no text outside page bounds and no raster images. Figures remain vectors with selectable text. Chromium 154.0.8037.57, Playwright 1.62.0, pypdf 6.10.0 and PyMuPDF 1.26.6 were used. PDF/UA or screen-reader certification is not claimed.
