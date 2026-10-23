import {readFileSync,writeFileSync} from 'node:fs';import vm from 'node:vm';import {spawnSync} from 'node:child_process';import assert from 'node:assert/strict';
const root=new URL('../docs/',import.meta.url).pathname;
for(const file of ['units/lessons-app.js','challenges/challenges.js']){
 const s=readFileSync(root+file,'utf8'),start=s.indexOf(file.startsWith('units')?'function harness(':'function probe(');let end=s.indexOf('\nfunction ',start+10);if(end<0)end=s.indexOf('\nasync function ',start+10);
 const harness=vm.runInNewContext('('+s.slice(start,end).trim()+')',{marker:'CS1_PUBLIC_CASES='});
 for(const [kind,source] of [['named','def increment_number(number):\n    return number + 1'],['legacy','def solution(number):\n    return number + 1'],['incorrect','def increment_number(number):\n    return number']]){
  const py=harness(source,[{call:'increment_number(4)',expected:'5'}]);const r=spawnSync('python',['-c',py],{encoding:'utf8'});assert.equal(r.status,0,r.stderr);const result=JSON.parse(r.stdout.slice(r.stdout.indexOf('=')+1));assert.equal(result[0].ok??result[0].passed,kind!=='incorrect',r.stdout);console.log('PASS Python checker',file,kind);
 }
}

const {readdirSync}=await import('node:fs');
const scope={window:{}};
for(const folder of ['units','challenges'])for(const file of readdirSync(root+folder).filter(f=>/^data.*\.js$/.test(f)))vm.runInNewContext(readFileSync(root+folder+'/'+file,'utf8'),scope);
let count=0;for(const item of [...scope.window.CS1_UNITS,...scope.window.CS1_CHALLENGES]){if(!item.functionName)continue;count++;assert.match(item.functionName,/^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$/);assert(item.starter.includes('def '+item.functionName+'('));for(const c of item.cases||item.examples||[])assert(c.call.startsWith(item.functionName+'('));}
console.log('PASS descriptive Python contracts:',count);
