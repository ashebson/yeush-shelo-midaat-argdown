const fs=require('node:fs');
const path=require('node:path');
(async()=>{
 const {argdown}=await import('@argdown/node');
 const config=JSON.parse(fs.readFileSync('argdown.config.json','utf8'));
 fs.mkdirSync('maps',{recursive:true});
 const report=[];
 for(const file of fs.readdirSync('argdown').filter(x=>x.endsWith('.argdown')).sort()){
  const input=fs.readFileSync(path.join('argdown',file),'utf8');
  const result=await argdown.runAsync({...structuredClone(config),input,throwExceptions:true,process:['parse-input','build-model','build-map','colorize','export-dot','export-svg','export-json','highlight-source']});
  if(result.parserErrors?.length || result.lexerErrors?.length) throw new Error(JSON.stringify({file,parserErrors:result.parserErrors,lexerErrors:result.lexerErrors}));
  if(!result.svg?.includes('<svg')) throw new Error('No SVG: '+file);
  const stem=file.replace('.argdown','');
  fs.writeFileSync(`maps/${stem}.svg`,result.svg);
  fs.writeFileSync(`maps/${stem}.dot`,result.dot);
  fs.writeFileSync(`maps/${stem}.json`,result.json);
  fs.writeFileSync(`maps/${stem}.source.html`,result.highlightedSource);
  report.push({file,parserErrors:0,lexerErrors:0,nodes:(result.svg.match(/class="node"/g)||[]).length,edges:result.map.edges.length});
 }
 fs.writeFileSync('docs/build-report.json',JSON.stringify(report,null,2)+'\n');
 console.log(report);
 require('./site.cjs');
})().catch(e=>{console.error(e);process.exit(1)});
