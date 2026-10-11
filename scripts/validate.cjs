// Artifact integrity checks, not a proof of the reconstruction or its interpretation.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const { createHash } = require('node:crypto');
const { execFileSync } = require('node:child_process');
const root = path.resolve(__dirname, '..');
const read = file => fs.readFileSync(path.join(root, file), 'utf8');
const json = file => JSON.parse(read(file));
const sorted = values => values.map(value => JSON.stringify(value)).sort();
const equalSet = (actual, expected, message) => assert.deepEqual(sorted(actual), sorted(expected), message);
const id = title => title.split(' · ')[0];
const escape = value => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');

async function validate() {
  const { argdown } = await import('@argdown/node');
  const config = json('argdown.config.json');
  const ledger = json('sources/model.json');
  const excerpts = json('sources/hebrew-excerpts.json');
  const commentary = json('sources/commentary.json');
  const commentarySources = new Map(commentary.sources.map(source => [source.id, source]));
  const commentaryNodes = new Map(commentary.nodes.map(node => [node.id, node]));
  assert.equal(commentarySources.size, commentary.sources.length, 'Unique commentary sources');
  assert.equal(commentaryNodes.size, commentary.nodes.length, 'Unique commentary nodes');
  for (const [file, hash] of Object.entries(commentary.base_sha256)) {
    assert.equal(createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex'), hash, `Base reconstruction preserved: ${file}`);
  }
  for (const source of commentary.sources) {
    assert.equal(createHash('sha256').update(source.text, 'utf8').digest('hex'), source.sha256, `Commentary excerpt hash: ${source.id}`);
    assert(source.ref.includes(source.author), `Source attribution: ${source.id}`);
    assert(source.url.startsWith('https://'), `Source URL: ${source.id}`);
    assert(source.context && source.edition && source.license && source.retrieved, `Source provenance: ${source.id}`);
  }
  for (const node of commentary.nodes) {
    assert(['C','R'].includes(node.class));
    assert(node.sources.length && node.base_nodes.length, `Grounded commentary: ${node.id}`);
    assert(node.base_nodes.every(id=>ledger.nodes.some(n=>n.id===id)), `Base references: ${node.id}`);
    assert(node.sources.every(id=>commentarySources.has(id)), `Commentary citations: ${node.id}`);
    if(node.class==='C') {
      assert(node.label.startsWith(node.speaker+':'), `Visible commentator attribution: ${node.id}`);
      assert(node.sources.every(id=>commentarySources.get(id).author===node.speaker), `No collapsed commentator attribution: ${node.id}`);
    } else assert.equal(node.speaker,'Editorial', `Supplied bridge: ${node.id}`);
  }
  equalSet(commentary.views.flatMap(view=>view.nodes), commentary.nodes.map(n=>n.id), 'Each commentary node appears in one small map');
  for (const view of commentary.views) {
    for (const [from, relation, to] of view.edges) {
      assert(view.nodes.includes(from) && view.nodes.includes(to), `Commentary edge stays in its view: ${view.id}`);
      assert.equal(relation, '+>', 'Selected commentaries explain and qualify; no manufactured disagreement');
    }
    assert.equal(new Set(view.edges.map(e=>e.join(' '))).size, view.edges.length);
    equalSet(view.sources, [...new Set(view.nodes.flatMap(id=>commentaryNodes.get(id).sources))], `Complete source appendix: ${view.id}`);
  }
  assert(commentaryNodes.get('KO6').text.includes('need not mean an intention to steal'));
  assert(commentarySources.get('ri-possession').context.includes('Shittah Mekubbetzet'));
  assert(commentaryNodes.get('KR7').text.includes('Rava knew'));
  assert(!commentary.views.flatMap(v=>v.edges).some(e=>e[0]==='KR7'||e[2]==='KR7'), 'Tosafot explains the refutation; not another proof');
  assert(commentaryNodes.get('KC3').class==='R', 'Coins map relation explanation is editorial');
  assert(commentaryNodes.get('KB1').text.includes('expressly refuses to despair'));
  assert(commentaryNodes.get('KB2').text.includes('not fully like loss to everyone'));
  const packageInfo = json('package.json');
  const lock = json('package-lock.json').packages[''];
  for (const key of ['name', 'version', 'license', 'engines', 'devDependencies']) {
    assert.deepEqual(lock[key], packageInfo[key], `Lockfile root metadata: ${key}`);
  }
  assert.equal(config.model.mode, 'loose');
  assert.equal(config.selection.excludeDisconnected, false);
  assert.equal(ledger.nodes.length, 22);
  assert.equal(new Set(ledger.nodes.map(n => n.id)).size, 22, 'Unique ledger IDs');
  assert.equal(ledger.edges.length, 18);
  const byId = new Map(ledger.nodes.map(n => [n.id, n]));
  for (const [from, relation, to] of ledger.edges) {
    assert(byId.has(from) && byId.has(to), `Known endpoints: ${from} ${to}`);
    assert(['+>', '->'].includes(relation), 'Only support and attack; no undercuts');
  }
  const edgeKeys = ledger.edges.map(e => e.join(' '));
  assert.equal(new Set(edgeKeys).size, 18, 'No duplicate relations');
  for (const key of ['O4 +> O5', 'O6 +> O7', 'O5 -> O7', 'C6 -> C2', 'C4 -> O5', 'R6 -> O7']) {
    assert(edgeKeys.includes(key), `Required direction and target: ${key}`);
  }
  equalSet(ledger.edges.filter(e => e[0] === 'C6' && e[1] === '->'), [['C6', '->', 'C2']], 'Coins reply attacks only the unawareness premise');
  for (const key of ['O1', 'O2', 'O3']) {
    assert(!ledger.edges.some(e => e[0] === key || e[2] === key), `${key} is an isolated scope note`);
  }
  for (const key of ['C6', 'R4', 'R6']) assert.equal(byId.get(key).class, 'E', `${key}: attributed expansion`);
  assert.equal(byId.get('R5').class, 'R', 'River bridge is supplied reconstruction');

  const specs = [
    ['01-opening', 'O', 7, 3], ['02-coins', 'C', 7, 6],
    ['03-river', 'R', 8, 7], ['overview', '', 22, 18]
  ];
  for(const view of commentary.views) specs.push([view.id,null,view.nodes.length,view.edges.length,view]);
  equalSet(fs.readdirSync(path.join(root, 'argdown')).filter(f => f.endsWith('.argdown')), specs.map(([stem]) => `${stem}.argdown`), 'Exact base and commentary map inventory');
  const report = [];
  for (const [stem, prefix, nodeCount, edgeCount, commentaryView] of specs) {
    const file = `${stem}.argdown`;
    const input = read(`argdown/${file}`);
    const result = await argdown.runAsync({ ...config, input, throwExceptions: true,
      process: ['parse-input', 'build-model', 'build-map', 'colorize', 'export-dot', 'export-svg', 'export-json'] });
    assert.equal(result.parserErrors?.length || 0, 0, `${file}: parser errors`);
    assert.equal(result.lexerErrors?.length || 0, 0, `${file}: lexer errors`);
    const expectedNodes = commentaryView ? commentaryView.nodes.map(id=>commentaryNodes.get(id)) : ledger.nodes.filter(n => n.id.startsWith(prefix));
    const expectedIds = new Set(expectedNodes.map(n => n.id));
    const expectedEdges = (commentaryView ? commentaryView.edges : ledger.edges).filter(([from, , to]) => expectedIds.has(from) && expectedIds.has(to))
      .map(([from, relation, to]) => [from, relation === '+>' ? 'support' : 'attack', to]);
    const model = JSON.parse(result.json);
    assert.equal(model.map.nodes.length, nodeCount, `${stem}: node count`);
    assert.equal(model.map.edges.length, edgeCount, `${stem}: edge count`);
    equalSet(model.map.nodes.map(n => id(n.title)), [...expectedIds], `${stem}: exact node IDs`);
    equalSet(Object.keys(model.statements).concat(Object.keys(model.arguments)), expectedNodes.map(n => `${n.id} · ${n.label}`), `${stem}: no implicit or extra model nodes`);
    for (const node of expectedNodes) {
      const actual = model.map.nodes.find(n => id(n.title) === node.id);
      assert.equal(actual.title, `${node.id} · ${node.label}`);
      assert.equal(actual.labelText.trim(), `${node.class} · ${node.text}`, `${stem}: text/provenance ${node.id}`);
      assert.equal(actual.type, `${node.kind}-map-node`, `${stem}: shape ${node.id}`);
      if(!commentaryView) assert(input.includes(`/* ${node.class} | Bava Metzia ${node.ref} | https://www.sefaria.org/Bava_Metzia.${node.ref} | ${node.hebrew} */`), `${stem}: provenance comment ${node.id}`);
    }
    const mapIds = new Map(model.map.nodes.map(n => [n.id, id(n.title)]));
    equalSet(model.map.edges.map(e => [mapIds.get(e.from), e.relationType, mapIds.get(e.to)]), expectedEdges, `${stem}: exact rendered relations; no propagation`);
    equalSet(model.relations.map(e => [id(e.from), e.relationType, id(e.to)]), expectedEdges, `${stem}: exact model relations; no undercuts`);
    for (const ext of ['svg', 'dot', 'json']) {
      assert.equal(read(`maps/${stem}.${ext}`), result[ext], `Stale ${stem}.${ext}; run npm run build`);
    }
    assert.equal((result.svg.match(/class="node"/g) || []).length, nodeCount, `${stem}: SVG nodes`);
    assert.equal((result.svg.match(/class="edge"/g) || []).length, edgeCount, `${stem}: SVG edges`);
    report.push({ file, parserErrors: 0, lexerErrors: 0, nodes: nodeCount, edges: edgeCount });
    console.log(`PASS ${stem}: ${nodeCount} nodes / ${edgeCount} relations, exact ledger and fresh SVG/DOT/JSON parity`);
  }
  assert.deepEqual(json('docs/build-report.json'), report.sort((a,b)=>a.file.localeCompare(b.file)), 'Build report matches fresh parsing');
  assert.equal(excerpts.length, 8);
  assert.equal(new Set(excerpts.map(e => e.ref)).size, 8);
  for (const excerpt of excerpts) {
    assert.equal(createHash('sha256').update(excerpt.text, 'utf8').digest('hex'), excerpt.sha256, `Source hash: ${excerpt.ref}`);
    assert.equal(excerpt.edition, 'Wikisource Talmud Bavli');
    assert.equal(excerpt.api_license, 'CC-BY-SA');
    assert.match(excerpt.retrieved, /^\d{4}-\d{2}-\d{2}$/);
    assert.equal(new URL(excerpt.url).searchParams.get('vhe'), 'Wikisource_Talmud_Bavli');
  }
  for (const node of ledger.nodes) {
    assert(ledger.classes[node.class], `Known provenance class: ${node.id}`);
    const segments = node.ref.split('-');
    const excerpt = excerpts.find(e => e.ref === `Bava Metzia ${segments[0].replace('.', ':')}`);
    assert(excerpt, `Source reference exists: ${node.id}`);
    assert(!node.hebrew || excerpt.text.includes(node.hebrew), `Hebrew anchor belongs to cited excerpt: ${node.id}`);
  }

  const html = read('index.html');
  const htmlIds = [...html.matchAll(/\bid="([^"]+)"/g)].map(m => m[1]);
  assert.equal(new Set(htmlIds).size, htmlIds.length, 'Unique document IDs, including embedded SVGs');
  assert.equal((html.match(/<svg\b/g) || []).length, specs.length);
  assert.equal((html.match(/<details(?: |>|$)/g) || []).length, 30+commentary.nodes.length+commentary.sources.length, 'Base and commentary ledgers/excerpts');
  assert(!/<(?:script|img|iframe)\b[^>]*\bsrc\s*=|<link\b|@import\b|url\(\s*["']?https?:|\b(?:fetch|XMLHttpRequest|WebSocket)\s*\(/i.test(html), 'No external runtime resources or network calls');
  const hebrewBlocks = [...html.matchAll(/<blockquote\b([^>]*)>([\s\S]*?)<\/blockquote>/g)];
  assert.equal(hebrewBlocks.length, ledger.nodes.filter(n => n.hebrew).length + excerpts.length + commentary.sources.length);
  for (const [, attrs] of hebrewBlocks) assert(attrs.includes('dir="rtl"') && attrs.includes('lang="he"'), 'Hebrew is explicitly RTL');
  for (const node of ledger.nodes) {
    assert(html.includes(escape(node.text)), `HTML ledger text: ${node.id}`);
    if (node.hebrew) assert(html.includes(escape(node.hebrew)), `HTML anchor: ${node.id}`);
  }
  for (const excerpt of excerpts) assert(html.includes(escape(excerpt.text)), `HTML excerpt: ${excerpt.ref}`);
  for (const source of commentary.sources) assert(html.includes(escape(source.text)), `HTML commentary excerpt: ${source.id}`);
  for (const node of commentary.nodes) assert(html.includes(escape(node.text)), `HTML commentary claim: ${node.id}`);

  // Regenerate the page away from the working tree to detect stale presentation output.
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'yeush-validate-'));
  try {
    for (const directory of ['sources', 'maps']) fs.cpSync(path.join(root, directory), path.join(temporary, directory), { recursive: true });
    execFileSync(process.execPath, [path.join(__dirname, 'site.cjs')], { cwd: temporary, stdio: 'pipe' });
    assert.equal(html, fs.readFileSync(path.join(temporary, 'index.html'), 'utf8'), 'Stale index.html; run npm run build');
  } finally {
    fs.rmSync(temporary, { recursive: true, force: true });
  }
  const documents = ['README.md', 'LICENSE.md', 'index.html', ...fs.readdirSync(path.join(root, 'docs')).filter(f => f.endsWith('.md')).map(f => `docs/${f}`)];
  let links = 0;
  for (const file of documents) {
    const text = read(file);
    const matches = file.endsWith('.html') ? [...text.matchAll(/\bhref="([^"]+)"/g)] : [...text.matchAll(/\[[^\]]*\]\(([^\s)]+)\)/g)];
    for (const [, target] of matches) {
      if (/^(?:[a-z][a-z\d+.-]*:|\/\/|#)/i.test(target)) continue;
      const local = decodeURIComponent(target.split(/[?#]/)[0]);
      assert(fs.existsSync(path.resolve(root, path.dirname(file), local)), `${file}: broken local link ${target}`);
      links++;
    }
  }
  console.log(`PASS 8 Gemara and ${commentary.sources.length} commentary hashes, Hebrew/provenance, offline page parity, unique IDs, and ${links} local links`);
  const pdfReport = json('docs/pdf-export-report.json');
  assert.equal(pdfReport.status, 'passed');
  assert.equal(pdfReport.page_count, commentary.pdf_page_count);
  for (const [file, hash] of Object.entries(pdfReport.source_sha256)) {
    assert.equal(createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex'), hash, `PDF source changed: ${file}; run npm run pdf`);
  }
  assert.equal(createHash('sha256').update(fs.readFileSync(path.join(root, 'docs/yeush-shelo-midaat.pdf'))).digest('hex'), pdfReport.pdf_sha256, 'PDF bytes match verified export');
  assert(pdfReport.pages.every(p => !p.overflow.length && !p.scrollOverflow && (p.minMapFontPt === null || p.minMapFontPt >= 10)), 'PDF layout passed export checks');
  console.log(`PASS ${pdfReport.page_count}-page PDF integrity, source freshness, and recorded layout checks`);
  console.log('Artifact validation passed. This checks encoding and integrity, not scholarly truth or formal validity.');
}

validate().catch(error => { console.error(error); process.exitCode = 1; });
