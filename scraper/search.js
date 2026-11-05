const { chromium } = require('playwright');
const fs=require('fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  const out={};
  for (const kw of ['mantle','MCL','MIPI','Blastoid']) {
    await p.goto('https://onlineprogram.hematology.org/');
    await p.click('#ashcontent_btnSearch'); await p.waitForLoadState('networkidle');
    await p.fill('#ashcontent_tbKeyword', kw);
    await Promise.all([p.waitForNavigation(), p.click('#ashcontent_btnSubmit')]);
    await p.waitForLoadState('networkidle');
    const total = (await p.innerText('main')).match(/(\d+) Matching Results/);
    let pids=new Set(), sids=new Set();
    for (let pg=1; pg<20; pg++) {
      if (pg>1) { await p.goto(`https://onlineprogram.hematology.org/results-keyword.aspx?page=${pg}&size=50`); await p.waitForLoadState('networkidle'); }
      const links = await p.$$eval('a', as=>as.map(a=>a.getAttribute('href')||''));
      const np = links.filter(h=>h.includes('paper-details')).map(h=>h.match(/pid=(\d+)/)[1]);
      links.filter(h=>h.includes('session-details')).forEach(h=>sids.add(h.match(/sid=(\d+)/)[1]));
      if (!np.length && pg>1) break;
      np.forEach(x=>pids.add(x));
      if (!links.some(h=>h.includes(`page=${pg+1}&`))) break;
    }
    out[kw]={total: total&&total[1], pids:[...pids], sids:[...sids]};
    console.log(kw, total&&total[1], 'papers', pids.size, 'sessions', sids.size);
  }
  fs.writeFileSync('dl/kw.json', JSON.stringify(out));
  await b.close();
})();
