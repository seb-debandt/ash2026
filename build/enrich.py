import json,sys
T={}
def a(code,nums): 
    for n in nums.split(): T[n]=code
a('FT','6 1015 1016 1017 1018 1019 1783 1789 1791 3539 3557 3569 5297 5300 5301 5303 5330 5333 5334 5340')
a('RR','237 238 1020 1780 1784 1815 2729 3546 3565 4529 5321 5328 5338 6291 240 3571 3695 3720 3886 5457 5636 1944 3704 3878 5299 5456 5459 5467 5480')
a('CT','235 236 1032 1802 3562 3564 4155 4288 5302 5339 5936 1374 2417 3514 3526 4115 4162 4475 5442 5447 5880 5930 6027 6297 83 564 705 955 1029 1055 1056 1095 2337 2338 2357 2364 2405 2409 2410 2412 2415 2765 4164 4169 4172 4394 4474 4478 5395 5884 5908 5951 5987 6164')
a('BIO','371 393 1511 1512 1733 1748 1754 3230 3513 3518 3541 5249 5270 5274 5305 5875 401 3501 3512 5381 6099 43 368 369 510 657 1459 1767 2586 3623 4346 5036 6109')
a('RW','1796 1803 2629 2715 2749 2854 3540 4404 5315 1874 3644 4513 6265 1850 2083 2650 3631 5550 6244 6254')
a('SAFE','2116 5322 5331 147 307 476 477 2719 2751 4483 2128 3699 3910 4546 6281 6282 6324')
KEY={
'6':'Plenary session. First randomized phase 3 trial to show a chemotherapy-free first treatment (zanubrutinib plus rituximab) beats bendamustine-rituximab on progression-free survival. Authors call it a potential new standard.',
'1791':'Randomized ENRICH trial, longer follow-up: ibrutinib plus rituximab now shows an overall survival benefit over R-CHOP chemotherapy in older patients.',
'1015':'Randomized OASIS-2 trial (210 patients): adding a fixed two-year course of venetoclax to ibrutinib plus anti-CD20 raised the rate of undetectable disease (MRD) after induction.',
'1016':'First report of GATE1: pirtobrutinib, venetoclax and rituximab as first treatment, with high complete response and MRD-negative rates in a high-risk-enriched group.',
'1018':'TrAVeRse: fixed-duration, chemotherapy-free acalabrutinib, venetoclax and rituximab stays effective at about two years, including in TP53-mutated disease.',
'1017':'CARAMEL: first trial designed for older or frail patients unfit for chemotherapy. Acalabrutinib plus rituximab gave a 77% response rate.',
'1019':'Eight-year follow-up: in indolent MCL, stopping ibrutinib once disease is undetectable gives durable remissions, especially in leukemic non-nodal, TP53 wild-type disease.',
'235':'Large European registry analysis: CAR T-cell therapy gave better survival and fewer treatment-related deaths than donor stem cell transplant in relapsed MCL.',
'236':'Longest real-world follow-up of brexucabtagene autoleucel (Tecartus): about 42% of patients remain in remission at four years, and late relapses are rare.',
'1784':'Up to nine years of follow-up for zanubrutinib in relapsed MCL: durable disease control with no new safety signals.',
'237':'Glofitamab plus lenalidomide was highly active in very high-risk relapsed MCL, including after BTK inhibitor and CAR-T failure.',
'238':'FIL-COLUMN met its primary endpoint: loncastuximab tesirine (an antibody-drug conjugate) after short induction gave durable control in patients already exposed to BTK inhibitors.',
'1032':'First multicenter trial of a dual CD20/CD19 CAR-T (zamto-cel) in relapsed MCL: every patient responded at interim analysis, with a 14-day manufacturing time.',
}
d=json.load(open(sys.argv[1]))
for x in d:
    x['topic']=T[x['no']]
    if x['no'] in KEY: x['key']=KEY[x['no']]
missing=[x['no'] for x in d if x['no'] not in T]; assert not missing, missing
json.dump(d,open(sys.argv[2],'w'),ensure_ascii=False)
import collections; print(collections.Counter(x['topic'] for x in d), sum('key' in x for x in d))
