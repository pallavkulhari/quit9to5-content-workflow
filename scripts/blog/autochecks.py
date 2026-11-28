import re,sys
# Ported from the box (blog/post13-work/autochecks.py). Pre-publish mechanical checks for REVIEW-PROCESS section B.
# Usage: python3 autochecks.py postNN.md ["So, how do you <answer lead-in>"]
#   The optional 2nd argument is the opening words of the answer paragraph, to check it starts within ~150 words.
if len(sys.argv)<2: sys.exit('usage: autochecks.py postNN.md [answer lead-in]')
p=sys.argv[1]
t=open(p,encoding='utf-8').read()
fm,body=t.split('---\n',2)[1:]
txt=re.sub(r'\]\([^)]*\)',']',body); txt=re.sub(r'[#*_>()\[\]]',' ',txt); txt=re.sub(r'—+','',txt)
words=txt.split(); low=body.lower()
print('word count:',len(words))
banned=['delve','tapestry','testament','pivotal','robust','seamless','powerful','cutting-edge','leverage','utilize','utilise','foster','embark','realm','landscape','comprehensive','crucial','paramount','game-changer','game changer','revolutionize','unlock','unleash','harness','furthermore','moreover','navigate',"it's worth noting","in today's fast-paced world","here's the thing","let that sink in",'lifeboat','anchor','dive into','transformative','multifaceted']
print('banned hits:',[b for b in banned if re.search(r'\b'+re.escape(b),low)])
body_nodiv=re.sub(r'—{5,}','',body)
print('em/en dashes in text:',body_nodiv.count('—')+body_nodiv.count('–'))
print('curly quotes/ellipsis:',[c for c in '\u2018\u2019\u201c\u201d\u2026' if c in body])
print('filler:',{w:len(re.findall(r'\b'+w+r'\b',low)) for w in ['actually','really','simply','just']})
print('X, not Y / isnt-its:',re.findall(r"[^.]*,\s*not\s+[^.]*\.|[^.]*\bisn't\b[^.]*\. it's[^.]*|it's not [^.]*, it's|you don't need [^.]*\. you need",low))
print('"Here" openers:',len(re.findall(r'(^|\n)here',low)))
print('₹ count:',body.count('₹'),'| ÷ count:',body.count('÷'))
h2=re.findall(r'^## (.*)$',body,re.M); print('H2s:',len(h2),'all questions:',all(h.endswith('?') for h in h2))
for h in h2: print('   ',h)
print('H1/H3 in body:',re.findall(r'^(#|###) ',body,re.M))
links=re.findall(r'\[([^\]]+)\]\(([^)]+)\)',body); print('links:',len(links))
for a,u in links: print('   ',a,'->',u)
print('waitlist links:',sum('quit9to5.in/?' in u for a,u in links))
print('anchor "here":',[a for a,u in links if a.strip().lower() in ('here','click here')])
bold=sum(len(m.split()) for m in re.findall(r'\*\*(.+?)\*\*',body)); print(f'bold words: {bold} ({100*bold/len(words):.1f}%)')
print('blockquotes:',re.findall(r'^> (.*)$',body,re.M))
print('book mentions (Quit 9to5 in italics/bold, excl. URLs):',len(re.findall(r'\*Quit 9to5\*|\*\*_Quit 9to5_\*\*|Quit 9to5 waitlist',body)))
for ph in ['my upcoming book','on your own terms','first-principles','do you see it?','thought exercise:']: print(f'  "{ph}":',low.count(ph))
# answer position
plain=re.sub(r'\]\([^)]*\)',']',body)
lead=sys.argv[2] if len(sys.argv)>2 else None
if lead and lead in plain:
    i=plain.find(lead); print('answer starts at word',len(re.sub(r'[#*_>()\[\]]',' ',plain[:i]).split()))
    ans=re.search(re.escape(lead)+r'.*',plain).group(0); print('answer block words:',len(ans.split()))
elif lead: print('answer lead-in NOT FOUND:',lead)
# paragraph line length check (approx 4 lines ~ 75 words)
paras=[p for p in body.split('\n\n') if p.strip() and not p.startswith(('-','1.','2.','3.','#','>'))]
print('longest paragraph words:',max(len(p.split()) for p in paras))
for k in ['title','seo_title','subtitle','slug','meta_description']:
    m=re.search(rf'^{k}: "?(.*?)"?$',fm,re.M); print(k,len(m.group(1)))
