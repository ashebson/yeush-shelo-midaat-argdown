"""Render native Argdown from the preserved scholarly ledgers and PCS ledger."""
import json, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
load = lambda name: json.loads((ROOT / name).read_text())
base = load('sources/model.json')
commentary = load('sources/commentary.json')
native = load('sources/reconstructions.json')
sources = {s['id']: s for s in commentary['sources']}
for source in load('sources/hebrew-excerpts.json'):
    sources['gemara-' + source['ref'].removeprefix('Bava Metzia ').replace(':', '.')] = source
anchors = load('sources/anchors.json')['nodes']
nodes = {n['id']: n for n in base['nodes'] + commentary['nodes'] + native['nodes']}
pcs = {p['argument']: p for p in native['arguments']}

def title(id):
    return id + ' · ' + nodes[id]['label']

def token(id):
    return ('<' + title(id) + '>') if nodes[id]['kind'] == 'argument' else ('[' + title(id) + ']')

def metadata(n):
    episode = 'opening' if n['id'].startswith(('O','KO')) else 'coins' if n['id'].startswith(('C','KC')) else 'river'
    evidence = anchors[n['id']]
    for span in evidence['spans']:
        source = sources[span['sourceId']]
        assert hashlib.sha256(source['text'].encode()).hexdigest() == span['sourceSha256']
        assert source['text'][span['startCodePoint']:span['endCodePoint']] == span['quote']
    source_ids = list(dict.fromkeys(n.get('sources', []) + [span['sourceId'] for span in evidence['spans']]))
    refs = [sources[id]['ref'] for id in source_ids]
    urls = [sources[id]['url'] for id in source_ids]
    speaker = n.get('speaker') or ('Editorial' if n['class'] == 'R' else 'Rashi' if n['class'] == 'E' else 'Abaye' if n['id'] in ['O4','O5'] else 'Rava' if n['id'] in ['O6','O7'] else 'Rabbi Yitzhak' if n['id'] == 'C5' else 'Gemara / cited Mishnah or baraita')
    temporal = {'O1':'ordinary unmarked loss; owner unaware at pickup','O2':'marked loss; later despair does not cure prohibited pickup','O3':'inaccessible loss; permission does not depend on prior awareness','O4':'owner unaware of loss now','O5':'ordinary unmarked loss before awareness','O6':'anticipated response after future awareness','O7':'anticipated later despair counted at the present time by Rava','C1':'permission in cited Mishnah; timing tested by C2','C2':'assumed unawareness before discovery','C3':'conditional on permission before awareness','C4':'conditional challenge under assumed unawareness','C5':'habitual checking supports prior awareness in this reply','C6':'awareness and despair before the finder discovers the coins','C7':'challenge loses its assumption of prior unawareness','R1':'ordinary recoverability; verse category','R2':'inaccessible to everyone; exception independent of awareness','R3':'category comparison; temporal scope supplied in R4','R4':'owner unaware before pickup','R5':'ordinary unmarked loss before awareness','R6':'ordinary recoverable loss before awareness; not after established prior despair','R7':'refutation recorded after the final comparison','R8':'ruling recorded after the refutation','KR3':'established despair before pickup already permits ordinary loss','KR4':'exception includes absent awareness even when later despair would not occur','KR5':'ordinary loss without established prior despair; prior despair remains a route to permission','KR7':'Rava knew the baraita before the comparison was drawn','KB1':'complete loss to everyone even when the owner expressly refuses despair','KB2':'recoverable loss where owner has not despaired'}
    return dict(id=n['id'], sourceRef=refs, sourceUrl=urls, speaker=speaker,
                provenanceClass=n['class'], hebrewAnchor=evidence['spans'][0]['quote'],
                hebrewAnchors=evidence['spans'], anchorRelationship=evidence['relationship'],
                anchorOffsetUnit='Unicode code points; zero-based [startCodePoint,endCodePoint); no normalization',
                temporalScope=n.get('temporalScope') or temporal.get(n['id'], 'awareness, despair and possession relative to pickup; scope stated in attributed claim'),
                baseNodeIds=n.get('base_nodes', [n['id']] if n['id'] in {x['id'] for x in base['nodes']} else n.get('baseNodes', [])),
                sourceIds=source_ids,
                anchorScope=evidence['note'],
                reconstructionStatus='numbered PCS; editorial reconstruction' if n['id'] in pcs else 'argument sketch; no PCS' if n['kind']=='argument' else 'statement',
                color={'S':'#267565','E':'#53659c','C':'#53659c','R':'#f3d5a5'}[n['class']]), episode

def body(ids, edges, grouped=False):
    lines=['/* Selected episodes only; loose dialectical reconstruction, not a formal proof. Metadata and numbered bridges preserve provenance. */','']
    previous=None
    # PCS supplies its own support edges. Do not duplicate them as explicit arrows.
    implicit={tuple(e) for p in native['arguments'] if p['argument'] in ids for e in p['replacesEdges']}
    for id in ids:
        n=nodes[id]; meta,episode=metadata(n)
        if grouped and episode!=previous:
            lines.extend(['# '+{'opening':'Opening and scope','coins':'Coins challenge and reply','river':'Final river comparison'}[episode]+' {isGroup: true}', ''])
            previous=episode
        tags=['source' if n['class']=='S' else 'explanation' if n['class'] in ['E','C'] else 'reconstruction', episode]
        if n.get('speaker'): tags.append(n['speaker'].lower().split(' ')[0])
        lines.append(token(id)+': '+n['class']+' · '+n['text']+' '+' '.join('#'+t for t in tags)+' '+json.dumps(meta,ensure_ascii=False))
        lines.extend('  '+rel+' '+token(b) for a,rel,b in edges if a==id and (a,rel,b) not in implicit)
        lines.append('')
        if id in pcs:
            for index, step in enumerate(pcs[id]['steps'],1):
                if 'uses' in step:
                    lines.extend(['--',step['rule'],json.dumps({'uses':step['uses'],'provenanceClass':'R','sourceIds':step['sourceIds'],'interpretation':step['interpretation']},ensure_ascii=False),'--'])
                lines.append(f'({index}) '+token(step['statement']))
            lines.append('')
    return '\n'.join(lines).rstrip()+'\n'

def render(stem, ids, edges, detail=False, grouped=False):
    extra=[n['id'] for n in native['nodes'] if n['argument'] in ids]
    settings={'model':{'mode':'loose'},'selection':{'excludeDisconnected':False,'statementSelectionMode':'all'}}
    if detail:
        settings['model']['explodeArguments']=True
        settings['map']={'argumentLabelMode':'title'}
        # Native tag selection keeps this episode while retaining its isolated notes.
        settings['selection'].update(selectedTags=[metadata(nodes[ids[0]])[1]],selectElementsWithoutTag=False)
    else:
        settings['selection']['excludeStatements']=[title(id) for id in extra]
    if grouped: settings['group']={'groupDepth':1}
    # JSON is valid YAML and keeps frontmatter portable and reproducible.
    ordered=ids+extra
    if grouped: ordered=sorted(ordered,key=lambda id: ['opening','coins','river'].index(metadata(nodes[id])[1]))
    text='===\n'+json.dumps(settings,ensure_ascii=False,indent=2)+'\n===\n\n'+body(ordered,edges,grouped)
    (ROOT/'argdown'/f'{stem}.argdown').write_text(text)

render('overview',[n['id'] for n in base['nodes']],base['edges'],grouped=True)
for stem,prefix in [('01-opening','O'),('02-coins','C'),('03-river','R')]:
    ids=[n['id'] for n in base['nodes'] if n['id'].startswith(prefix)]
    edges=[e for e in base['edges'] if e[0] in ids and e[2] in ids]
    render(stem,ids,edges)
for view in commentary['views']:
    render(view['id'],view['nodes'],view['edges'],detail=view['id']=='06-river-commentary')
for view in native['views']:
    ids=view['nodes']; edges=[e for e in base['edges'] if e[0] in ids and e[2] in ids]
    render(view['id'],ids,edges,detail=True)
print(f'Authored {4+len(commentary["views"])+len(native["views"])} native views and {len(native["arguments"])} numbered arguments with exact Hebrew spans.')
