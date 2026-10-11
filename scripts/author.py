"""Author the bounded model and its source ledger (no network required)."""
from pathlib import Path
import json,re,hashlib
root=Path(__file__).resolve().parents[1]
# id, kind, label, wording, evidence class, reference, Hebrew anchor
rows=[
('O1','statement','Scope: no identifying mark','The dispute concerns ordinary lost objects without an identifying mark.','S','21b.4','כי פליגי בדבר שאין בו סימן'),
('O2','statement','Marked objects: agreement','Both reject unconscious yeush here; later despair does not repair an already prohibited pickup.','S','21b.2','בדבר שיש בו סימן'),
('O3','statement','Sea / river exception','The Torah permits the exceptional sea or river loss, even with a mark.','S','21b.3','רחמנא שרייה'),
('O4','statement','Abaye: no awareness','The owner has not yet learned of the loss.','S','21b.4','דהא לא ידע דנפל מיניה'),
('O5','statement','Abaye: ineffective','Unconscious yeush is not effective in the disputed case.','S','21b.1','אביי אמר לא הוי יאוש'),
('O6','statement','Rava: future despair','Once aware, the owner will despair because there is no identifying mark.','S','21b.4','דלכי ידע דנפל מיניה מיאש'),
('O7','statement','Rava: effective now','In the disputed case, that anticipated despair counts now.','S','21b.4','מהשתא הוא דמיאש'),
('C1','statement','Scattered coins: permitted','The cited Mishnah lets the finder keep scattered coins.','S','21b.7','מעות מפוזרות הרי אלו שלו'),
('C2','statement','Objection: owner unaware','The objection assumes that the owner has not learned of this loss.','S','21b.7','הא לא ידע דנפל מיניה'),
('C3','statement','Bridge: test Abaye','If permission holds while awareness is absent, this case conflicts with Abaye.','R','21b.7',''),
('C4','argument','Coins challenge','Permission plus assumed unawareness challenges Abaye, using the stated bridge.','R','21b.7','ת"ש'),
('C5','statement','Reply: purse checking','People habitually check their purses, says Rabbi Yitzhak.','S','21b.7','אדם עשוי למשמש בכיסו'),
('C6','statement','Owner already knew','The reply treats the owner as aware and despairing before the finder picked up the coins.','E','21b.7',''),
('C7','statement','Coins do not decide','With unawareness denied, the coins case does not establish Rava over Abaye.','R','21b.7',''),
('R1','statement','Verse: loss from you','Deuteronomy 22:3 is read as addressing loss from the owner that remains accessible to others.','S','22b.5','אשר תאבד ממנו ומצאתה'),
('R2','statement','Inaccessible loss: permitted','A river loss inaccessible to everyone is excluded from that obligation.','S','22b.5','שאבודה ממנו ואינה מצויה אצל כל אדם'),
('R3','statement','Compare both categories','The Gemara compares prohibition and permission: each covers items with or without a mark.','S','22b.6','ואיסורא דומיא דהיתירא'),
('R4','statement','Clarify: before awareness','For the ordinary-loss prohibition, the owner has not learned of the loss before pickup.','E','22b.6',''),
('R5','argument','River comparison','Apply the comparison to ordinary unmarked loss before awareness: anticipated despair does not permit it.','R','22b.5-6',''),
('R6','statement','Ordinary loss: still prohibited','In that unaware-before-pickup case, ordinary recoverable loss is prohibited even without a mark.','E','22b.6','בין דלית בה סימן אסורה'),
('R7','statement','Rava: explicitly refuted','The Gemara declares the refutation of Rava decisive.','S','22b.6','תיובתא דרבא תיובתא'),
('R8','statement','Ruling: follows Abaye','The text rules for Abaye here, within the mnemonic YAAL KAGAM.','S','22b.7','והלכתא כוותיה דאביי')]
nodes=[dict(zip(['id','kind','label','text','class','ref','hebrew'],r)) for r in rows]
# Edges are editorial reconstruction; attack targets are deliberate.
edges=[('O4','+>','O5'),('O6','+>','O7'),('O5','->','O7'),('C1','+>','C4'),('C2','+>','C4'),('C3','+>','C4'),('C4','->','O5'),('C5','+>','C6'),('C6','->','C2'),('C6','+>','C7'),('R1','+>','R2'),('R2','+>','R5'),('R3','+>','R5'),('R4','+>','R5'),('R5','+>','R6'),('R6','->','O7'),('R6','+>','R7'),('R7','+>','R8')]
ledger={'title':'Yeush shelo midaat','nodes':nodes,'edges':edges,'classes':{'S':'Explicit source claim, in our English paraphrase','E':'Explanatory expansion, with commentator attribution in notes','R':'Supplied reconstruction / analytical bridge'}}
(root/'sources/model.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
byid={n['id']:n for n in nodes}
def token(id):
 n=byid[id]; title=id+' · '+n['label']; return ('<'+title+'>') if n['kind']=='argument' else ('['+title+']')
def render(name,title,ids,local_edges):
 s='# '+title+'\n\n/* Selected episodes only. S = source paraphrase; E = attributed explanation; R = reconstruction. All relations are analytical, not a machine proof. See sources/model.json and docs/source-notes.md. */\n\n'
 for id in ids:
  n=byid[id]
  s+=f'/* {n["class"]} | Bava Metzia {n["ref"]} | https://www.sefaria.org/Bava_Metzia.{n["ref"]} | {n["hebrew"]} */\n'
  s+=token(id)+': '+n['class']+' · '+n['text']+' '+json.dumps({'color':{'S':'#267565','E':'#53659c','R':'#f3d5a5'}[n['class']]})+'\n'
  for a,rel,b in local_edges:
   if a==id: s+='  '+rel+' '+token(b)+'\n'
  s+='\n'
 (root/f'argdown/{name}.argdown').write_text(s)
render('overview','Selected episodes · Bava Metzia 21b–22b',[n['id'] for n in nodes],edges)
for name,title,prefixes in [('01-opening','01 · The question and its boundaries',['O']),('02-coins','02 · A challenge to Abaye, then a factual reply',['C']),('03-river','03 · The river comparison and the ruling',['R'])]:
 ids=[n['id'] for n in nodes if n['id'][0] in prefixes]
 # Local episode views omit cross-episode arrows; text below maps explains them.
 render(name,title,ids,[(a,r,b) for a,r,b in edges if a in ids and b in ids])

# Keep the legacy base-ledger authoring entrypoint compatible with native PCS output.
import runpy
runpy.run_path(str(root / "scripts/author-native.py"), run_name="__main__")
