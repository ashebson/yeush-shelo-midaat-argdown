"""Render the separate commentary ledger into Argdown; never rewrite the base model."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'sources/commentary.json').read_text())
sources = {source['id']: source for source in data['sources']}
nodes = {node['id']: node for node in data['nodes']}


def token(node_id):
    node = nodes[node_id]
    title = node_id + ' · ' + node['label']
    return '<' + title + '>' if node['kind'] == 'argument' else '[' + title + ']'


for view in data['views']:
    lines = ['# ' + view['title'], '',
             '/* Commentary layer only. C = attributed commentator claim; R = supplied editorial bridge or comparison. All arrows are editorial. The base Gemara maps remain separate. See sources/commentary.json. */', '']
    for node_id in view['nodes']:
        node = nodes[node_id]
        refs = '; '.join(sources[source_id]['ref'] for source_id in node['sources'])
        lines.append(f'/* {node["class"]} | {node["speaker"]} | {refs} | Base nodes: {", ".join(node["base_nodes"])} */')
        color = '#53659c' if node['class'] == 'C' else '#f3d5a5'
        lines.append(token(node_id) + ': ' + node['class'] + ' · ' + node['text'] + ' ' + json.dumps({'color': color}))
        lines.extend('  ' + relation + ' ' + token(target) for source, relation, target in view['edges'] if source == node_id)
        lines.append('')
    (ROOT / 'argdown' / (view['id'] + '.argdown')).write_text('\n'.join(lines) + '\n')
print(f'Authored {len(data["views"])} separate commentary maps; base sources untouched.')
