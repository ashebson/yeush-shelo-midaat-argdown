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
  equalSet(fs.readdirSync(path.join(root, 'argdown')).filter(f => f.endsWith('.argdown')), specs.map(([stem]) => `${stem}.argdown`), 'Exactly four authored maps');
  const report = [];
  for (const [stem, prefix, nodeCount, edgeCount] of specs) {
    const file = `${stem}.argdown`;
    const input = read(`argdown/${file}`);
    const result = await argdown.runAsync({ ...config, input, throwExceptions: true,
      process: ['parse-input', 'build-model', 'build-map', 'colorize', 'export-dot', 'export-svg', 'export-json'] });
    assert.equal(result.parserErrors?.length || 0, 0, `${file}: parser errors`);
    assert.equal(result.lexerErrors?.length || 0, 0, `${file}: lexer errors`);
    const expectedNodes = ledger.nodes.filter(n => n.id.startsWith(prefix));
    const expectedIds = new Set(expectedNodes.map(n => n.id));
    const expectedEdges = ledger.edges.filter(([from, , to]) => expectedIds.has(from) && expectedIds.has(to))
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
      assert(input.includes(`/* ${node.class} | Bava Metzia ${node.ref} | https://www.sefaria.org/Bava_Metzia.${node.ref} | ${node.hebrew} */`), `${stem}: provenance comment ${node.id}`);
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
  assert.deepEqual(json('docs/build-report.json'), report, 'Build report matches fresh parsing');
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
  assert.equal((html.match(/<svg\b/g) || []).length, 4);
  assert.equal((html.match(/<details>/g) || []).length, 30, '22 ledger rows and 8 excerpts');
  assert(!/<(?:script|img|iframe)\b[^>]*\bsrc\s*=|<link\b|@import\b|url\(\s*["']?https?:|\b(?:fetch|XMLHttpRequest|WebSocket)\s*\(/i.test(html), 'No external runtime resources or network calls');
  const hebrewBlocks = [...html.matchAll(/<blockquote\b([^>]*)>([\s\S]*?)<\/blockquote>/g)];
  assert.equal(hebrewBlocks.length, ledger.nodes.filter(n => n.hebrew).length + excerpts.length);
  for (const [, attrs] of hebrewBlocks) assert(attrs.includes('dir="rtl"') && attrs.includes('lang="he"'), 'Hebrew is explicitly RTL');
  for (const node of ledger.nodes) {
    assert(html.includes(escape(node.text)), `HTML ledger text: ${node.id}`);
    if (node.hebrew) assert(html.includes(escape(node.hebrew)), `HTML anchor: ${node.id}`);
  }
  for (const excerpt of excerpts) assert(html.includes(escape(excerpt.text)), `HTML excerpt: ${excerpt.ref}`);

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
  console.log(`PASS 8 source hashes and Hebrew anchors, provenance, offline page parity, unique IDs, and ${links} local links`);
  console.log('Artifact validation passed. This checks encoding and integrity, not scholarly truth or formal validity.');
}

validate().catch(error => { console.error(error); process.exitCode = 1; });
