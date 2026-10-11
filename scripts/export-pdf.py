"""Export the verified demo as a vector PDF with a separate commentary layer.

Requires Python Playwright, pypdf, and Chromium. Run from any directory:
  python3 scripts/export-pdf.py --browser /usr/bin/chromium
The PDF goes to docs/yeush-shelo-midaat.pdf; intermediate HTML/PDF and a
geometry report go to ignored output/pdf/. No network or public hosting is used.
"""
import argparse
import hashlib
from html import escape
from importlib.metadata import version
import json
from pathlib import Path

from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output' / 'pdf'
DESTINATION = ROOT / 'docs' / 'yeush-shelo-midaat.pdf'
OUT.mkdir(parents=True, exist_ok=True)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--browser', default='/usr/bin/chromium')
args = parser.parse_args()
ledger = json.loads((ROOT / 'sources/model.json').read_text())
excerpts = json.loads((ROOT / 'sources/hebrew-excerpts.json').read_text())
commentary = json.loads((ROOT / 'sources/commentary.json').read_text())
native = json.loads((ROOT / 'sources/reconstructions.json').read_text())
all_nodes = {node['id']: node for node in ledger['nodes'] + commentary['nodes'] + native['nodes']}
anchors = json.loads((ROOT / 'sources/anchors.json').read_text())['nodes']
source_catalog = {source['id']: source for source in commentary['sources']}
source_catalog.update({'gemara-'+source['ref'].removeprefix('Bava Metzia ').replace(':','.'):source for source in excerpts})
TOTAL = commentary['pdf_page_count']
commentary_sources = {source['id']: source for source in commentary['sources']}

CSS = '''
*{box-sizing:border-box}html,body{margin:0;padding:0}
body{font:16px/1.5 Arial,sans-serif;color:#173c3a;background:#f7f5ef;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:var(--width);height:var(--height);padding:var(--padding);display:flex;flex-direction:column;gap:20px;overflow:hidden}
.page>*{flex-shrink:0}h1,h2,h3,p{margin:0}h1,h2{font-family:Georgia,serif;font-weight:400;line-height:1.08;letter-spacing:-.02em}
h1{font-size:64px}h2{font-size:42px}h3{font-size:18px}.eyebrow{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#5b6b68;font-weight:700;margin-bottom:14px}
.intro{max-width:1050px;font-size:18px;color:#5b6b68;margin-top:16px}.hero{margin:28px 0}.hero p{font-size:23px;margin-top:24px}.he-title{font-size:36px;margin:30px 0 8px}.he-ref{font-size:18px;color:#5b6b68}
.rule{border-top:1px solid #d9dfd7;padding-top:22px}.legend{display:flex;gap:24px;align-items:center;flex-wrap:wrap;font-size:15px}.legend strong{font-weight:700}.support{color:#267565}.attack{color:#bd5143}
.badge{display:inline-block;padding:2px 8px;border-radius:4px;font-weight:700;font-size:13px}.S{background:#dcece7}.E,.C{background:#e4e8f6}.R{background:#fceaca}
.map-slot{flex:1;min-height:0;background:white;border:1px solid #d9dfd7;border-radius:8px;padding:18px;display:flex;align-items:center;justify-content:center}.map-slot svg{display:block;width:100%;height:100%}
.reading-note{border-left:3px solid #267565;background:#edf1e9;padding:12px 18px;font-size:16px;line-height:1.5}.footer{margin-top:auto;display:flex;justify-content:space-between;gap:20px;border-top:1px solid #d9dfd7;padding-top:12px;font-size:12px;color:#5b6b68}
.cover .footer{margin-top:auto}.cover .guide{display:grid;grid-template-columns:40px 1fr;gap:15px 12px;margin-top:8px}.guide b{font-size:15px;color:#267565}.guide p{font-size:16px}.scope{font-size:15px;color:#5b6b68}.small{font-size:13px;color:#5b6b68}a[href]{color:#267565;text-decoration:underline;text-underline-offset:3px}
.notes h2,.excerpts h2{font-size:36px}.notes{gap:16px}.notes p{font-size:15px;line-height:1.5}.notes table{width:100%;border-collapse:collapse;font-size:14px}.notes th{text-align:left;background:#e8eee7}.notes th,.notes td{padding:7px 10px;border-bottom:1px solid #d9dfd7}.notes .explanations{display:grid;gap:12px}.excerpts{gap:10px}.excerpts article{padding-bottom:6px;border-bottom:1px solid #d9dfd7}.excerpts h3{font-size:13px;margin-bottom:5px}.excerpts blockquote{font-size:17px;line-height:1.45;margin:0;unicode-bidi:isolate}.excerpts .excerpt-list{display:grid;gap:7px}.excerpts .intro{font-size:15px;margin-top:10px}
'''


def legend():
    return '''<div class="legend"><strong class="support">→ support</strong><strong class="attack">→ attack</strong><span>Rectangle: claim · Hexagon: argument sketch / numbered inference</span><span><b class="badge S">S</b> Source <b class="badge E">E</b> Explanation <b class="badge R">R</b> Reconstruction</span></div>'''


def footer(number, right):
    return f'<footer class="footer"><span>Before awareness · Bava Metzia 21b–22b · 11 October 2026</span><span>{escape(right)} · {number} / {TOTAL}</span></footer>'


def document(body, width, height, padding, kind):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Before awareness · Yeush shelo midaat</title><style>
@page{{size:{width}mm {height}mm;margin:0}}{CSS}
</style></head><body><main class="page {kind}" style="--width:{width}mm;--height:{height}mm;--padding:{padding}mm">{body}</main></body></html>'''


def link(ref):
    return f'<a href="https://www.sefaria.org/Bava_Metzia.{ref}?vhe=Wikisource_Talmud_Bavli">{ref.replace(".", ":", 1)}</a>'


report = {'page_count': TOTAL, 'pages': [], 'source_sha256': {}, 'network_requests': []}
for file in ['index.html', 'sources/model.json', 'sources/hebrew-excerpts.json', 'scripts/export-pdf.py', 'sources/commentary.json', 'sources/reconstructions.json', 'sources/anchors.json', *[f'maps/{stem}.svg' for stem in ['overview', '01-opening', '02-coins', '03-river']+[view['id'] for view in commentary['views'] + native['views']]]]:
    report['source_sha256'][file] = hashlib.sha256((ROOT / file).read_bytes()).hexdigest()

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=args.browser, args=['--no-sandbox'])
    context = browser.new_context(offline=True)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('request', lambda request: report['network_requests'].append(request.url))
    page.set_content((ROOT / 'index.html').read_text())
    episodes = page.locator('.episode').evaluate_all('''sections=>Object.fromEntries(sections.map(s=>[s.id,{
        title:s.querySelector('h2').textContent,
        ref:s.querySelector('.eyebrow').textContent,
        intro:s.querySelector('.episode-head p:not(.eyebrow)').textContent,
        note:s.querySelector('.reading-note').textContent
    }]))''')
    pages = []
    cover = '''<div><p class="eyebrow">Aryeh × Judd · Argument mapping demonstration</p>
<div class="hero"><h1>Before<br>awareness.</h1><p>When an owner would give up a lost object, but does not yet know it is lost—does that future response count now?</p></div>
<div class="he-title" dir="rtl" lang="he">יאוש שלא מדעת</div><p class="he-ref" dir="rtl" lang="he">בבא מציעא כא ע״ב–כב ע״ב</p></div>
<div class="rule"><p class="eyebrow">A four-minute conversation</p><div class="guide">
<b>01</b><p><strong>Frame the dispute.</strong> Contrast future despair with present awareness. Keep the agreed scope restrictions visible.</p>
<b>02</b><p><strong>Test one premise.</strong> The coins reply attacks the assumed unawareness, leaving the Mishnah intact.</p>
<b>03</b><p><strong>Inspect the bridge.</strong> Separate the final river comparison from Rashi’s timing clarification and the supplied reconstruction.</p>
<b>04</b><p><strong>Invite revision.</strong> Which node or relation would you redraw? Compare it with the source excerpts.</p></div></div>
<p class="scope">22 base nodes · 18 base relations · Three selected episodes. A separate ledger adds 21 commentary claims and argument sketches: Rashi, Tosafot, Rashba, and Ritva via Shittah Mekubbetzet. This is an argument reconstruction for discussion, not a complete encoding of the sugya, a machine proof, or a system for deciding halakhah.</p>
<p class="small">Reading order: base maps and sources (pages 2–7), then four commentary maps and their Hebrew sources (pages 8–15), inference detail maps (16–18), numbered reconstructions (19–23), and exact Hebrew claim anchors (24–25). The overview is an A1 landscape foldout; episode pages use A3 to keep node text readable. Source notes use A4. View pages individually or print at actual size; shrinking the foldout onto A4 makes its labels small.</p>'''
    pages.append(('cover', 210, 297, 15, document(cover + footer(1, 'Reader’s guide'), 210, 297, 15, 'cover')))
    for number, (stem, width, height) in enumerate([
        ('overview', 841, 594), ('01-opening', 420, 297),
        ('02-coins', 420, 297), ('03-river', 297, 420)
    ], start=2):
        e = episodes[stem]
        svg = (ROOT / 'maps' / f'{stem}.svg').read_text()
        # Preserve all authored SVG labels, shapes and relations; scale only.
        body = f'''<header><p class="eyebrow">{escape(e['ref'])} · {'Overview' if stem == 'overview' else 'Selected episode'}</p>
<h2>{escape(e['title'])}</h2><p class="intro">{escape(e['intro'])}</p></header>
{legend()}<div class="map-slot" role="img" aria-label="{escape(e['title'])}">{svg}</div>
<p class="reading-note">{escape(e['note'])}</p>{footer(number, 'Sources and provenance: pages 6–7')}'''
        pages.append((stem, width, height, 15, document(body, width, height, 15, 'diagram')))

    groups = [
        ('O1, O4, O6, O7', '21b.4'), ('O2', '21b.2'), ('O3', '21b.3'), ('O5', '21b.1'),
        ('C1–C7', '21b.7'), ('R1–R2', '22b.5'), ('R3, R4, R6, R7', '22b.6'),
        ('R5', '22b.5-6'), ('R8', '22b.7')
    ]
    rows = ''.join(f'<tr><td>{nodes}</td><td>Bava Metzia {link(ref)}</td></tr>' for nodes, ref in groups)
    notes = f'''<header><p class="eyebrow">Sources · Attribution · Method</p><h2>What comes from where?</h2></header>
<p><b class="badge S">S</b> <strong>Source:</strong> an explicit claim or question, in original English paraphrase. <b class="badge E">E</b> <strong>Explanation:</strong> attributed expansion. <b class="badge R">R</b> <strong>Reconstruction:</strong> a supplied bridge, argument summary or local assessment. These classes are provenance, not truth scores.</p>
<table><thead><tr><th>Nodes</th><th>Source passage</th></tr></thead><tbody>{rows}</tbody></table>
<div class="explanations"><p><strong>C6 · Awareness before the find.</strong> Following Rashi’s <bdi dir="rtl" lang="he">עשוי למשמש</bdi> on 21b, the reply treats awareness and despair as preceding discovery. C6 attacks C2’s factual assumption; it is not an undercut of C4’s inference.</p>
<p><strong>R4 and R6 · The temporal qualification.</strong> Following <a href="https://www.sefaria.org/Rashi_on_Bava_Metzia.22b.6.1-3">Rashi on 22b:6</a>, especially <bdi dir="rtl" lang="he">אף איסורא</bdi>, the ordinary-loss prohibition concerns an owner who has not learned of the loss before pickup. This is not a universal prohibition on keeping all unmarked objects.</p>
<p><strong>R5 · Supplied bridge.</strong> Compare the ordinary prohibition with the exceptional permission under R4’s temporal qualification. River permission alone does not refute Rava. The final comparison is on 22b:5–7, distinct from the earlier river exchange on 22a.</p></div>
<p>All arrows are editorial reconstruction in Argdown’s loose mode, not formal entailments. O1–O3 are isolated scope notes. The Gemara’s refutation and ruling are recorded, not computed. Intervening challenges, including figs/olives/carobs, are deliberately omitted.</p>
<p class="small">Edition: Wikisource Talmud Bavli via Sefaria and Hebrew Wikisource; saved source verification dated 11 October 2026. English is original paraphrase, not a modern published translation. Scholarly content and presentation: CC BY-SA 4.0. See the repository’s LICENSE.md and docs/source-notes.md for full attribution and boundaries.</p>'''
    pages.append(('provenance', 210, 297, 14, document(notes + footer(6, 'Provenance and boundaries'), 210, 297, 14, 'notes')))
    text_rows = ''.join(f'''<article><h3><a href="{escape(e['url'], quote=True)}">{escape(e['ref'])}</a></h3><blockquote dir="rtl" lang="he">{escape(e['text'])}</blockquote></article>''' for e in excerpts)
    source_page = f'''<header><p class="eyebrow">Primary text · Selected excerpts</p><h2>Return to the words.</h2><p class="intro">Unvocalized Wikisource Talmud Bavli via Sefaria. These are selected excerpts; intervening discussions are omitted.</p></header><div class="excerpt-list">{text_rows}</div><p class="small">Attribution: Hebrew Wikisource contributors / Sefaria; edition metadata: CC-BY-SA. Saved on 11 October 2026. Exact excerpt hashes and reference URLs are retained in sources/hebrew-excerpts.json.</p>'''
    pages.append(('primary-text', 210, 297, 14, document(source_page + footer(7, 'Hebrew / Aramaic'), 210, 297, 14, 'excerpts')))

    for view in commentary['views']:
        number = len(pages) + 1
        stem = view['id']
        width, height = view['pdf_size_mm']
        svg = (ROOT / 'maps' / f'{stem}.svg').read_text()
        body = f'''<header><p class="eyebrow">Layer 2 · Commentary · {escape(view['ref'])}</p><h2>{escape(view['title'])}</h2><p class="intro">{escape(view['intro'])}</p></header>
<div class="legend"><strong class="support">→ supports / explains</strong><span><b class="badge C">C</b> Attributed commentator <b class="badge R">R</b> Supplied editorial bridge</span><span>All arrows are editorial; base maps remain separate.</span></div>
<div class="map-slot">{svg}</div><p class="reading-note">{escape(view['note'])}</p>{footer(number, 'Hebrew commentary sources: pages 12–15')}'''
        pages.append((stem, width, height, 15, document(body, width, height, 15, 'diagram')))
    for view in commentary['views']:
        number = len(pages) + 1
        selected = [commentary_sources[id] for id in view['sources']]
        rows = ''.join(f'''<article><h3><a href="{escape(source['url'], quote=True)}">{escape(source['ref'])}</a></h3><blockquote dir="rtl" lang="he">{escape(source['text'])}</blockquote><p class="small">{escape(source['context'])}</p></article>''' for source in selected)
        body = f'''<header><p class="eyebrow">Layer 2 · Classical Hebrew · Selected excerpts</p><h2>{escape(view['name'])}</h2><p class="intro">For map nodes {escape(', '.join(view['nodes']))}. English map text is our own paraphrase; C names its commentator and R marks our supplied synthesis.</p></header><div class="excerpt-list">{rows}</div><p class="small">Hebrew Wikisource, classical commentary transcription, checked 11 October 2026. Classical Hebrew public domain; digital edition attribution retained under CC BY-SA 4.0. Exact excerpt hashes, daf and dibbur are retained in sources/commentary.json. Selected comments only; no exhaustive commentary survey or formal proof.</p>{footer(number, 'Commentary source ledger')}'''
        width, height = 210, 297
        pages.append((view['id']+'-sources', width, height, 15, document(body, width, height, 15, 'excerpts')))

    for view in native['views']:
        number = len(pages) + 1
        width, height = view['pdf_size_mm']
        svg = (ROOT / 'maps' / f"{view['id']}.svg").read_text()
        body = f'<header><p class="eyebrow">Numbered reconstruction · {escape(view["ref"])}</p><h2>{escape(view["title"])}</h2><p class="intro">{escape(view["intro"])}</p></header>{legend()}<div class="map-slot">{svg}</div><p class="reading-note">{escape(view["note"])}</p>{footer(number,"Numbered structures: pages 19–23")}'
        pages.append((view['id'],width,height,15,document(body,width,height,15,'diagram')))
    for reconstruction in native['arguments']:
        number = len(pages) + 1
        argument = all_nodes[reconstruction['argument']]
        rows = []
        for index, step in enumerate(reconstruction['steps'],1):
            node = all_nodes[step['statement']]
            if step.get('uses'):
                rows.append(f'<p class="reading-note"><strong>{escape(step["rule"])}</strong><br>Uses: {escape(str(step["uses"]))}. {escape(step["interpretation"])}</p>')
            rows.append(f'<p><strong>({index}) {escape(node["id"] + " · " + node["label"])}</strong><br><span class="badge {node["class"]}">{node["class"]}</span> {escape(node["text"])}</p>')
        citations = []
        for source_id in dict.fromkeys(source for step in reconstruction['steps'] for source in step.get('sourceIds',[])):
            if source_id in commentary_sources:
                source = commentary_sources[source_id]
                citations.append(f'<a href="{escape(source["url"],quote=True)}">{escape(source["ref"])}</a>')
            else:
                citations.append('Bava Metzia ' + link(source_id.removeprefix('gemara-')))
        body = f'<header><p class="eyebrow">Native Argdown · Premise–conclusion structure</p><h2>{escape(argument["id"] + " · " + argument["label"])}</h2></header><p>{escape(argument["text"])}</p><p><strong>{escape(reconstruction["editorialStatus"])}</strong></p>'+''.join(rows)+f'<p class="small">'+ ' · '.join(citations) + f'</p><p class="small">Numbering and rule names are editorial. Native uses metadata records dependencies; it does not establish formal validity. Same named statements retain the same meaning across views.</p>{footer(number,"Numbered argument ledger")}'
        pages.append(('pcs-'+argument['id'],210,297,14,document(body,210,297,14,'notes')))

    for title, node_ids in [('The comparison, step by step.', ['R4','KR3','KR4','KR5']), ('Custody, despair, and theft.', ['KO4','KO5','KO6'])]:
        number = len(pages) + 1
        rows = []
        for node_id in node_ids:
            node = all_nodes[node_id]
            spans = []
            for span in anchors[node_id]['spans']:
                source = source_catalog[span['sourceId']]
                spans.append(f'<p class="small"><a href="{escape(source["url"],quote=True)}">{escape(source["ref"])}</a> · Unicode [{span["startCodePoint"]}, {span["endCodePoint"]}) · {escape(span["purpose"])}</p><blockquote dir="rtl" lang="he">{escape(span["quote"])}</blockquote>')
            rows.append(f'<article><h3>{escape(node_id+" · "+node["label"])}</h3><p class="small">{escape(node["text"])}</p>'+''.join(spans)+'</article>')
        body = f'<header><p class="eyebrow">Exact source spans · Verbatim Hebrew</p><h2>{escape(title)}</h2><p class="intro">English claims remain attributed paraphrases. Offsets address the exact saved source text: Unicode code points, zero-based, start inclusive and end exclusive, without normalization. Full passages appear on pages 12–15.</p></header><div class="excerpt-list">'+''.join(rows)+f'</div><p class="small">All 49 claim records and 68 checked spans are available in the HTML ledger and sources/anchors.json. Editorial claims use context-only anchors; a span never upgrades an editorial inference to a quotation.</p>{footer(number,"Claim-specific Hebrew anchors")}'
        pages.append(('anchors-'+node_ids[0],210,297,14,document(body,210,297,14,'excerpts')))

    writer = PdfWriter()
    for number, (name, width, height, padding, html) in enumerate(pages, start=1):
        (OUT / f'{number:02}-{name}.html').write_text(html)
        page.set_content(html)
        page.evaluate('document.fonts.ready')
        page.emulate_media(media='print')
        geometry = page.evaluate('''()=>{
            const main=document.querySelector('main'), box=main.getBoundingClientRect();
            const overflow=[...main.querySelectorAll('header,footer,p,h1,h2,h3,article,table,.map-slot,.guide')].filter(e=>{
                const r=e.getBoundingClientRect();return r.left<box.left-1||r.right>box.right+1||r.top<box.top-1||r.bottom>box.bottom+1;
            }).map(e=>e.className||e.tagName);
            const texts=[...document.querySelectorAll('.map-slot svg text')];
            const sizes=texts.map(t=>parseFloat(getComputedStyle(t).fontSize)*t.getScreenCTM().a*.75);
            return {overflow,scrollOverflow:main.scrollHeight>main.clientHeight+1,
                minMapFontPt:sizes.length?Math.min(...sizes):null,
                rtlBlocks:[...document.querySelectorAll('[dir=rtl]')].length};
        }''')
        assert not geometry['overflow'] and not geometry['scrollOverflow'], f'{name}: page overflow {geometry}'
        if geometry['minMapFontPt'] is not None:
            assert geometry['minMapFontPt'] >= 10, f'{name}: map font too small {geometry}'
        single = OUT / f'{number:02}-{name}.pdf'
        page.pdf(path=str(single), print_background=True, prefer_css_page_size=True, tagged=True)
        reader = PdfReader(single)
        assert len(reader.pages) == 1, f'{name}: unexpected extra print page'
        assert reader.pages[0].extract_text().strip(), f'{name}: no extractable text'
        writer.add_page(reader.pages[0])
        writer.add_outline_item(episodes.get(name, {}).get('title', {'cover': 'Reader’s guide', 'provenance': 'Sources and provenance', 'primary-text': 'Primary text excerpts'}.get(name, name)), number - 1)
        report['pages'].append({'number': number, 'name': name, 'size_mm': [width, height], **geometry})
    assert not errors, errors
    assert not report['network_requests'], report['network_requests']
    writer.add_metadata({'/Title': 'Before awareness · Yeush shelo midaat', '/Author': 'Aryeh · Argdown demonstration', '/Subject': 'A bounded argument map of Bava Metzia 21b–22b', '/Keywords': 'Argdown, Bava Metzia, yeush shelo midaat, argument map', '/Creator': 'scripts/export-pdf.py · Chromium + pypdf'})
    with DESTINATION.open('wb') as file:
        writer.write(file)
    pdf = PdfReader(DESTINATION)
    assert len(pdf.pages) == TOTAL
    all_text = '\n'.join(page.extract_text() for page in pdf.pages)
    # Every authored node label must survive text extraction; figures remain vectors.
    normalized = ' '.join(all_text.split())
    for node in ledger['nodes'] + commentary['nodes'] + native['nodes']:
        assert ' '.join(f"{node['id']} · {node['label']}".split()) in normalized, f'Missing PDF label: {node["id"]}'
        assert ' '.join(node['text'].split()) in normalized, f'Missing PDF claim: {node["id"]}'
    report['pdf_sha256'] = hashlib.sha256(DESTINATION.read_bytes()).hexdigest()
    report['bytes'] = DESTINATION.stat().st_size
    report['chromium'] = browser.version
    report['python_dependencies'] = {name: version(name) for name in ['playwright', 'pypdf']}
    report['checks'] = [f'{TOTAL} single-page exports merged with bookmarks', 'All base, commentary and numbered-addition labels and complete claims extract from PDF', 'No HTML page overflow; map text at least 10 pt', 'No network requests or page errors']
    report['status'] = 'passed'
    (OUT / 'export-report.json').write_text(json.dumps(report, indent=2) + '\n')
    (ROOT / 'docs' / 'pdf-export-report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    browser.close()
