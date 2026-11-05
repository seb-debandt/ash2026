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
 fs.writeFileSync(outPath,fs.readFileSync(tplPath,'utf8').replace('__PAYLOAD__',()=>payload));
 console.log('ok',fs.statSync(outPath).size);
})();
