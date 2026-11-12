const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1350}});
const dir=path.join(__dirname,'html'),out=path.join(__dirname,'png');fs.mkdirSync(out,{recursive:true});
for(const f of fs.readdirSync(dir).filter(f=>f.endsWith('.html')).sort()){
 await pg.goto('file://'+path.join(dir,f));await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(150);
 await pg.screenshot({path:path.join(out,f.replace('.html','.png'))});}
await b.close();})();
