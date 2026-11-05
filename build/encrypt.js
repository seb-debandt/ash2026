const fs=require('fs'); const {webcrypto:c}=require('crypto');
(async()=>{
 const [,,dataPath,tplPath,outPath,pw]=process.argv;
 const data=fs.readFileSync(dataPath);
 const salt=c.getRandomValues(new Uint8Array(16)), iv=c.getRandomValues(new Uint8Array(12)), iter=310000;
 const base=await c.subtle.importKey('raw',new TextEncoder().encode(pw),'PBKDF2',false,['deriveKey']);
 const key=await c.subtle.deriveKey({name:'PBKDF2',salt,iterations:iter,hash:'SHA-256'},base,{name:'AES-GCM',length:256},false,['encrypt']);
 const ct=new Uint8Array(await c.subtle.encrypt({name:'AES-GCM',iv},key,data));
 const b=u=>Buffer.from(u).toString('base64');
 const payload=JSON.stringify({salt:b(salt),iv:b(iv),iter,ct:b(ct)});
 const body=fs.readFileSync(tplPath,'utf8').replace('__PAYLOAD__',()=>payload);
 const doc='<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n</head>\n<body>\n'+body+'\n</body>\n</html>\n';
 fs.writeFileSync(outPath,doc);
 console.log('ok',fs.statSync(outPath).size);
})();
