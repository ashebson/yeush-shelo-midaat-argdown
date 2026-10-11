# PDF edition and export record

[Open the seven-page PDF](yeush-shelo-midaat.pdf).

This edition preserves the verified SVG maps as vectors, with selectable text, a repeated legend, episode introductions and reading notes, source references, Rashi/reconstruction attribution, and all eight saved Hebrew/Aramaic excerpts. The authored claims, relations and `.argdown` files are unchanged. It is a bounded reconstruction, not a formal proof or complete encoding of the sugya.

## Page plan

| Page | Content | Page size | Minimum map label size |
| --- | --- | --- | ---: |
| 1 | Reader’s guide and four-minute conversation | A4 portrait | — |
| 2 | 22-node overview with cross-episode links | A2 landscape foldout | 11.03 pt |
| 3 | Opening dispute and isolated scope notes | A3 landscape | 12.05 pt |
| 4 | Scattered coins challenge and factual reply | A3 landscape | 11.71 pt |
| 5 | Final river comparison, refutation and ruling | A3 portrait | 12.53 pt |
| 6 | Node-to-source index and interpretive boundaries | A4 portrait | — |
| 7 | Selected Hebrew/Aramaic source excerpts | A4 portrait | — |

The larger map pages keep the original node wording readable without redesigning the argument. View each page independently in a PDF reader, or print at actual size on the indicated paper. Fitting the entire A2 overview onto A4 shrinks the labels; use the separate episode pages or zoom for close reading. The primary excerpts use 12.75 pt Hebrew text with explicit RTL direction.

## Regenerate

Requirements: existing Node build dependencies, Python 3, Chromium, and the pinned optional Python packages in [requirements-pdf.txt](../scripts/requirements-pdf.txt). The PDF export does not change the Node dependency tree.

```sh
npm ci
npm run build
python3 -m venv .venv-pdf
.venv-pdf/bin/python -m pip install -r scripts/requirements-pdf.txt
.venv-pdf/bin/python scripts/export-pdf.py --browser /usr/bin/chromium
npm test
```

Supply the path of your installed Chromium/Chrome executable on other systems. If the Python packages are already available to `python3`, use `npm run pdf -- --browser /path/to/chromium` instead.

The exporter reads the generated `index.html` for episode headings, introductions and notes, the four SVG maps, and the existing source ledgers. Chromium runs with networking disabled. It prints one intentionally sized page at a time; pypdf assembles them and adds navigation bookmarks. The final files are `docs/yeush-shelo-midaat.pdf` and [pdf-export-report.json](pdf-export-report.json). Intermediate HTML and per-page PDFs are kept in ignored `output/pdf/`.

The report records input and PDF SHA-256 hashes, exact page dimensions, minimum map font sizes and tool versions. `npm test` checks those hashes to catch stale PDF exports. PDF bytes can vary with browser/font versions and generated metadata; regeneration promises the same source-backed layout, not byte-identical files across environments.

## Inspection completed · 11 October 2026

The final seven PDF pages were rendered to PNG with Poppler and opened for visual inspection, rather than relying only on the source HTML. For example:

```sh
pdftoppm -scale-to 1800 -png docs/yeush-shelo-midaat.pdf output/pdf/page
pdfinfo docs/yeush-shelo-midaat.pdf
```

The local review covered every embedded figure: the overview’s cross-episode paths, opening scope notes and Abaye/Rava direction, coins C6 → C2 attack, and the river chain through R7/R8. Each figure reuses the already verified SVG; the PDF pass checks final-size labels, shape/text separation, boundaries and legend consistency. All four figures passed this fresh local inspection. No agent delegation or new figure design was needed.

All seven pages passed page-bound checks. PDF extraction retained all 22 exact node labels and complete claims. The PDF contains vector figures, with zero raster-image objects, and 18 clickable source links on the final two pages. No text spans fall outside page boundaries. The Hebrew title, inline Rashi anchors and all eight Hebrew excerpts were visually checked for right-to-left order, wrapping and missing glyphs.

The first export pass revealed underlining inherited by SVG node labels from the link style and insufficient space below the primary-text page. Link styling was scoped to actual hyperlinks and page layout was adjusted. The final inspection found neither issue, no clipped labels or footers, and no overlapping nodes. Export checks also enforce at least 10 pt map text and exactly one printed page for each page design.

Verified with Chromium 154.0.8037.57, Playwright 1.62.0 and pypdf 6.10.0. PyMuPDF 1.26.6 was used for additional text-bound and vector/link inspection. The PDF has bookmarks and selectable text; it is not certified as a tagged or PDF/UA-accessible document. No public hosting or visibility change was performed.
