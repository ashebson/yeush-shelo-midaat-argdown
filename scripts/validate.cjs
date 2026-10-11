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
  const native = json('sources/reconstructions.json');
  const allNodes = new Map([...ledger.nodes,...commentary.nodes,...native.nodes].map(n=>[n.id,n]));
  const flatten = nodes => nodes.flatMap(n=>n.children ? flatten(n.children) : [n]);
  const mapKey = title => id(title) + (/ - (\d+)$/.test(title) ? '.' + title.match(/ - (\d+)$/)[1] : '');
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
  for(const view of commentary.views) specs.push([view.id,null,view.id==='06-river-commentary'?8:view.nodes.length,view.id==='06-river-commentary'?6:view.edges.length,view]);
  for(const view of native.views) specs.push([view.id,null,view.id.startsWith('08')?8:10,view.id.startsWith('08')?7:9,view]);
  equalSet(fs.readdirSync(path.join(root, 'argdown')).filter(f => f.endsWith('.argdown')), specs.map(([stem]) => `${stem}.argdown`), 'Exact base and commentary map inventory');
  const report = [];
  for (const [stem, prefix, nodeCount, edgeCount, commentaryView] of specs) {
    const file = `${stem}.argdown`;
    const input = read(`argdown/${file}`);
    const result = await argdown.runAsync({ ...structuredClone(config), input, throwExceptions: true,
      process: ['parse-input', 'build-model', 'build-map', 'colorize', 'export-dot', 'export-svg', 'export-json', 'highlight-source'] });
    assert.equal(result.parserErrors?.length || 0, 0, `${file}: parser errors`);
    assert.equal(result.lexerErrors?.length || 0, 0, `${file}: lexer errors`);
    const expectedNodes = commentaryView ? commentaryView.nodes.map(id=>allNodes.get(id)) : ledger.nodes.filter(n => n.id.startsWith(prefix));
    const extra = native.nodes.filter(n=>expectedNodes.some(x=>x.id===n.argument));
    const exploded = ['06-river-commentary','09-river-inference'].includes(stem);
    const visibleExtra = stem.startsWith('08') || stem.startsWith('09') ? extra : [];
    const nodeKeys = expectedNodes.flatMap(n=>exploded && ['KR6','R5'].includes(n.id) ? [n.id+'.1',n.id+'.2'] : [n.id]).concat(visibleExtra.map(n=>n.id));
    const expectedIds = new Set(expectedNodes.map(n => n.id));
    const originalEdges = (commentaryView?.edges || ledger.edges).filter(([from, , to]) => expectedIds.has(from) && expectedIds.has(to));
    let expectedEdges = originalEdges;
    if(stem==='08-coins-inference') expectedEdges=[...originalEdges,['C4','+>','C8']];
    if(stem==='09-river-inference') expectedEdges=[['R1','+>','R2'],['R2','+>','R5.1'],['R3','+>','R5.1'],['R5.1','+>','R9'],['R9','+>','R5.2'],['R4','+>','R5.2'],['R5.2','+>','R6'],['R6','+>','R7'],['R7','+>','R8']];
    if(stem==='06-river-commentary') expectedEdges=[['KR3','+>','KR6.1'],['KR6.1','+>','KR4'],['KR4','+>','KR6.2'],['KR1','+>','KR6.2'],['KR2','+>','KR6.2'],['KR6.2','+>','KR5']];
    const relationNames = edges => edges.map(([a,r,b])=>[a,r==='+>'?'support':'attack',b]);
    const model = JSON.parse(result.json);
    const mapNodes = flatten(model.map.nodes);
    assert.equal(mapNodes.length, nodeCount, `${stem}: leaf node count`);
    assert.equal(model.map.edges.length, edgeCount, `${stem}: edge count`);
    equalSet(mapNodes.map(n => mapKey(n.title)), nodeKeys, `${stem}: exact selected node IDs`);
    const modelTitles=[...expectedNodes,...extra].flatMap(n=>exploded && ['KR6','R5'].includes(n.id)?[`${n.id} · ${n.label} - 1`,`${n.id} · ${n.label} - 2`]:[`${n.id} · ${n.label}`]);
    equalSet(Object.keys(model.statements).concat(Object.keys(model.arguments)),modelTitles,`${stem}: exact canonical and generated model nodes`);
    for (const node of [...expectedNodes,...extra]) {
      const values = node.kind==='argument' ? Object.values(model.arguments).filter(a=>id(a.title)===node.id) : [model.statements[`${node.id} · ${node.label}`]];
      for(const actual of values) {
        assert(actual, `${stem}: model member ${node.id}`);
        const member = actual.members.find(m=>m.text);
        assert.equal(member.text.trim(), `${node.class} · ${node.text}`, `${stem}: exact claim/provenance ${node.id}`);
        const data=actual.data;
        for(const field of ['id','sourceRef','sourceUrl','speaker','provenanceClass','hebrewAnchor','temporalScope','baseNodeIds','sourceIds','reconstructionStatus']) assert(data[field]!==undefined,`${stem}: metadata ${node.id}.${field}`);
        assert.equal(data.id,node.id);assert.equal(data.provenanceClass,node.class);
        assert(data.sourceRef.length && data.sourceUrl.length && data.hebrewAnchor.length);
        assert(data.sourceUrl.every(url=>new URL(url).protocol==='https:'));
        assert(data.baseNodeIds.every(id=>byId.has(id)));
        assert(data.sourceIds.every(id=>commentarySources.has(id)||/^gemara-(21b|22b)\.\d+(?:-\d+)?$/.test(id)));
        assert(actual.tags.includes(node.class==='S'?'source':node.class==='R'?'reconstruction':'explanation'));
      }
    }
    const mapIds = new Map(mapNodes.map(n => [n.id, mapKey(n.title)]));
    equalSet(model.map.edges.map(e => [mapIds.get(e.from), e.relationType, mapIds.get(e.to)]), relationNames(expectedEdges), `${stem}: exact rendered edges including native PCS; no unintended propagation`);
    const replaced = native.arguments.flatMap(p=>p.replacesEdges).map(e=>e.join(' '));
    const explicit = originalEdges.filter(e=>!replaced.includes(e.join(' '))).map(([a,r,b])=>[a==='C4'?'C8':a,r,b]);
    equalSet(model.relations.map(e => [id(e.from), e.relationType, id(e.to)]), relationNames(explicit), `${stem}: explicit model relations; C4 conclusion transfer is intentional`);
    assert(!model.map.edges.some(e=>e.from===e.to),`${stem}: no self-relations`);
    if(stem==='overview') {
      assert.equal(model.map.nodes.filter(n=>n.type==='group-map-node').length,3,'Three native episode groups');
      for(const scope of ['O1','O2','O3']) assert(!expectedEdges.some(([a,,b])=>a===scope||b===scope),'Scope notes remain visible and isolated');
    }
    // Inspect the canonical PCS before native explodeArguments splits inference views.
    const end=input.indexOf('\n===',4), settings=JSON.parse(input.slice(4,end));
    settings.model.explodeArguments=false;
    const canonical=await argdown.runAsync({...structuredClone(config),input:'===\n'+JSON.stringify(settings)+'\n==='+input.slice(end+4),throwExceptions:true,process:['parse-input','build-model']});
    assert.equal(canonical.parserErrors?.length||0,0);
    for(const reconstruction of native.arguments.filter(p=>expectedIds.has(p.argument))) {
      const argument=canonical.arguments[`${reconstruction.argument} · ${allNodes.get(reconstruction.argument).label}`];
      equalSet(argument.pcs.map((step,index)=>[index+1,id(step.title)]),reconstruction.steps.map((step,index)=>[index+1,step.statement]),`${stem}: exact ordered PCS`);
      assert.equal(argument.pcs.at(-1).role,'main-conclusion');
      reconstruction.steps.forEach((step,index)=>{
        const actual=argument.pcs[index];
        if(step.uses) {
          assert.deepEqual(actual.inference.data.uses,step.uses,`${stem}: joint premises and intermediate dependency`);
          assert.deepEqual(actual.inference.inferenceRules,[step.rule]);
          assert.deepEqual(actual.inference.data.sourceIds,step.sourceIds);
          assert(step.uses.every(n=>n>0&&n<=index),'Only preceding numbered statements are used');
          assert.equal(actual.role,index===argument.pcs.length-1?'main-conclusion':'intermediary-conclusion');
        } else assert.equal(actual.role,'premise');
      });
    }
    assert.equal(read(`maps/${stem}.source.html`),result.highlightedSource,'Fresh official source highlighting');
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
    fs.mkdirSync(path.join(temporary,'scripts'));
    fs.mkdirSync(path.join(temporary,'argdown'));
    fs.copyFileSync(path.join(__dirname,'author-native.py'),path.join(temporary,'scripts','author-native.py'));
    execFileSync('python3',[path.join(temporary,'scripts','author-native.py')],{stdio:'pipe'});
    for(const [stem] of specs) assert.equal(read(`argdown/${stem}.argdown`),fs.readFileSync(path.join(temporary,'argdown',`${stem}.argdown`),'utf8'),`Stale authored source ${stem}; regenerate from scholarly ledgers`);
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
