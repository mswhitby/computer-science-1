// Pilot metadata compiler. Run: node scripts/build-frontmatter-catalog.mjs
// The legacy JS records remain authoritative for exercises until all lessons migrate.
import { readFileSync, writeFileSync, mkdirSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import vm from 'node:vm';
const root=resolve(import.meta.dirname,'..');
const context=vm.createContext({window:{}});
const files=readdirSync(resolve(root,'docs/units')).filter(x=>/^data-\d\d\.js$/.test(x)).sort();
for(const file of files)vm.runInContext(readFileSync(resolve(root,'docs/units',file),'utf8'),context,{timeout:1000});
const legacy=context.window.CS1_UNITS||[];
const byId=new Map(legacy.map(x=>[x.id,x]));
const paths=new Map();
for(const row of legacy){
 if(!row.markdown)throw Error('Missing Markdown path: '+row.id);
 const p=resolve(root,'units',row.markdown);
 if(!p.startsWith(resolve(root,'units')+'/'))throw Error('Unsafe Markdown path: '+row.markdown);
 if(!paths.has(p))paths.set(p,[]);
 paths.get(p).push(row);
}
const ids=new Set(),aliases=new Set(),slugs=new Set();
const lessons=legacy.map(row=>{
 const file=resolve(root,'units',row.markdown),source=readFileSync(file,'utf8');
 if(!source.startsWith('---\n'))return {...row};
 const end=source.indexOf('\n---\n',4);
 if(end<0)throw Error('Unterminated front matter: '+row.markdown);
 const meta={};let list=null;
 for(const line of source.slice(4,end).split('\n')){
  if(/^  - /.test(line)){if(!list)throw Error('Unexpected list item in '+row.markdown);meta[list].push(line.slice(4).trim());continue;}
  const match=/^([A-Za-z][A-Za-z0-9]*):(?:\s*(.*))?$/.exec(line);
  if(!match)throw Error('Unsupported YAML front matter syntax: '+line);
  const [,key,value='']=match;
  if(Object.hasOwn(meta,key))throw Error('Duplicate front matter field: '+key);
  if(value===''){meta[key]=[];list=key;}else{meta[key]=value;list=null;}
 }
 for(const key of ['id','slug','title','unitId','order','points','status','legacyIds'])
  if(meta[key]===undefined)throw Error('Missing '+key+' in '+row.markdown);
 if(!/^les_[a-z0-9]{8,}$/.test(meta.id)||!/^unt_[a-z0-9]{8,}$/.test(meta.unitId))
  throw Error('Invalid permanent ID in '+row.markdown);
 if(!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(meta.slug))throw Error('Invalid slug: '+meta.slug);
 if(!['active','draft','archived'].includes(meta.status))throw Error('Invalid status');
 if(!Array.isArray(meta.legacyIds)||!meta.legacyIds.includes(row.id))throw Error('Missing current legacy ID: '+row.id);
 if(ids.has(meta.id)||slugs.has(meta.unitId+'/'+meta.slug))throw Error('Duplicate stable ID or unit slug');
 ids.add(meta.id);slugs.add(meta.unitId+'/'+meta.slug);
 for(const alias of meta.legacyIds){
  if(!byId.has(alias)||aliases.has(alias))throw Error('Unknown or duplicate legacy alias: '+alias);
  aliases.add(alias);
 }
 if(paths.get(file).length!==1)throw Error('Shared Markdown file requires separate migration: '+row.markdown);
 const order=Number(meta.order),points=Number(meta.points);
 if(!Number.isInteger(order)||order<1||!Number.isFinite(points)||points<0)throw Error('Invalid order or points');
 // Keep the legacy ID and all exercise/grade keys until the reader migration is verified.
 return {...row,stableId:meta.id,slug:meta.slug,title:meta.title,unitId:meta.unitId,order,points,status:meta.status,legacyIds:meta.legacyIds};
});
const migrationMap=Object.fromEntries(lessons.flatMap(row=>(row.legacyIds||[]).map(alias=>[alias,row.stableId])));
const output=resolve(root,'build/frontmatter');
mkdirSync(output,{recursive:true});
writeFileSync(resolve(output,'course.json'),JSON.stringify({schemaVersion:1,id:'computer-science-1',lessons},null,2)+'\n');
writeFileSync(resolve(output,'legacy-id-map.json'),JSON.stringify(migrationMap,null,2)+'\n');
console.log('Validated '+lessons.length+' lessons, '+Object.keys(migrationMap).length+' legacy aliases; output: build/frontmatter/');
