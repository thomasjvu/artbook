"""Build a portable static artbook from a project-owned JSON catalogue."""
from pathlib import Path
import argparse, hashlib, html, json, shutil

def build(catalogue, output, pdf=False):
    catalogue, output = Path(catalogue).resolve(), Path(output).resolve()
    data=json.loads(catalogue.read_text()); output.mkdir(parents=True,exist_ok=True)
    assert data['schema']==1
    esc=lambda value:html.escape(str(value),quote=True)
    media=output/'media';media.mkdir(exist_ok=True); records=[]
    def image(item):
        source=(catalogue.parent/item['image']).resolve()
        if not source.is_file():raise ValueError(f'Missing image: {source}')
        digest=hashlib.sha256(source.read_bytes()).hexdigest();name=digest[:16]+source.suffix.lower()
        shutil.copy2(source,media/name)
        records.append({'id':item['id'],'source':item['image'],'sha256':digest,'file':'media/'+name})
        return 'media/'+name
    plates=[]; chapters=[]
    for chapter in data['chapters']:
        items=[]
        for item in chapter['items']:
            if not item.get('include',True):continue
            if item.get('pixel') and not item.get('grid', {}).get('native_size'):
                raise ValueError('Pixel plates require grid.native_size: '+item['id'])
            src=image(item);items.append((item,src));plates.append((chapter,item,src))
        chapters.append((chapter,items))
    head=f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(data["title"])}</title><link rel="stylesheet" href="theme.css">'
    cover=data.get('cover_id');hero=next((src for _,i,src in plates if i['id']==cover),plates[0][2] if plates else '')
    s=[head,'<header><div class="eyebrow">'+esc(data.get('edition','Art & design'))+'</div><nav><a href="index.html">Artbook</a><a href="bible.html">Working catalogue</a><a href="catalogue.json">Catalogue</a><button class="screen-only" onclick="window.print()">Print / save PDF</button></nav></header><main>',f'<section class="cover"><div><span class="folio">Volume 01 / {esc(data.get("date",""))}</span><h1>{esc(data["title"])}</h1><p>{esc(data.get("subtitle",""))}</p><p>{esc(data.get("rights",""))}</p></div><img src="{hero}" alt="Cover artwork"></section>','<section><h2>Contents</h2><nav>']
    for n,(c,_) in enumerate(chapters,1):s.append(f'<a href="#chapter-{n}">{n:02} / {esc(c["title"])}</a>')
    s.append('</nav></section>');number=0
    for n,(c,items) in enumerate(chapters,1):
        s.append(f'<section class="chapter" id="chapter-{n}"><span class="folio">Chapter {n:02}</span><h2>{esc(c["title"])}</h2><p>{esc(c.get("intro",""))}</p>')
        if c.get('layout')=='gallery':s.append('<div class="gallery">')
        for item,src in items:
            number+=1;s.append(f'<figure data-grid="{esc(json.dumps(item.get("grid",{})))}" class="plate {"pixel" if item.get("pixel") else ""}"><img src="{src}" alt="{esc(item["title"])}"><figcaption class="caption"><span class="folio">{number:03}</span><div><h3>{esc(item["title"])}</h3><p>{esc(item.get("caption",""))}</p><p class="folio">{esc(item.get("status","Study"))}</p></div></figcaption></figure>')
        if c.get('layout')=='gallery':s.append('</div>')
        s.append('</section>')
    s.append('<script src="pixel-grid.js" defer></script></main><footer>'+esc(data.get('rights',''))+'</footer></html>');(output/'index.html').write_text('\n'.join(s))
    bible=[head,'<header><div class="eyebrow">Working catalogue</div><h1>'+esc(data['title'])+'</h1><nav><a href="index.html">Curated artbook</a></nav><p>Project records and revision notes. Inclusion in the book does not grant final art approval.</p></header><main class="gallery">']
    for _,item,src in plates:bible.append(f'<article class="working"><h2>{esc(item["title"])}</h2><span class="badge">{esc(item.get("status","Study"))}</span><figure data-grid="{esc(json.dumps(item.get("grid",{})))}" class="plate {"pixel" if item.get("pixel") else ""}"><img src="{src}" alt="{esc(item["title"])}"></figure><p>{esc(item.get("caption",""))}</p><details><summary>Record</summary><pre>{esc(json.dumps(item,indent=2))}</pre></details></article>')
    bible.append('<script src="pixel-grid.js" defer></script></main></html>');(output/'bible.html').write_text('\n'.join(bible))
    shutil.copy2(Path(__file__).with_name('theme.css'),output/'theme.css');shutil.copy2(Path(__file__).with_name('pixel-grid.js'),output/'pixel-grid.js');(output/'catalogue.json').write_text(json.dumps(data,indent=2)+'\n');(output/'provenance.json').write_text(json.dumps(records,indent=2)+'\n')
    if pdf:export_pdf(data,chapters,output)
    return len(plates)

def export_pdf(data,chapters,output):
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.utils import ImageReader
    from reportlab.lib.pagesizes import A4
    import textwrap
    width,height=A4;c=Canvas(str(output/'artbook.pdf'),pagesize=A4);c.setTitle(data['title'])
    page=0
    def label(text,x,y,size=9):
        c.setFont('Courier',size);c.setFillColorRGB(.12,.12,.12);c.drawString(x,y,text.encode('latin-1','replace').decode('latin-1'))
    def footer():
        nonlocal page
        page+=1;c.setStrokeColorRGB(.8,.8,.8);c.line(42,38,width-42,38);label(data['title'][:60],42,24,7);label(f'{page:03}',width-65,24,8)
    label(data.get('edition','ART & DESIGN'),42,height-55,10)
    for i,line in enumerate(textwrap.wrap(data['title'],22)):label(line,42,height-130-i*36,30)
    for i,line in enumerate(textwrap.wrap(data.get('subtitle',''),75)):label(line,42,height-260-i*14,9)
    label('WORKING ARTBOOK / '+data.get('date',''),42,100,9);footer();c.showPage()
    for index,(chapter,items) in enumerate(chapters,1):
        label(f'CHAPTER {index:02}',42,height-55,10);label(chapter['title'][:50],42,height-95,20)
        for j,line in enumerate(textwrap.wrap(chapter.get('intro',''),80)):label(line,42,height-130-j*14,9)
        footer();c.showPage()
        for item,src in items:
            label(chapter['title'].upper()[:70],42,height-45,8)
            reader=ImageReader(str(output/src));iw,ih=reader.getSize();scale=min((width-84)/iw,(height-245)/ih);w,h=iw*scale,ih*scale
            c.drawImage(reader,(width-w)/2,180+(height-245-h)/2,w,h,mask='auto')
            label(item['title'][:65],42,140,14)
            for j,line in enumerate(textwrap.wrap(item.get('caption',''),83)[:4]):label(line,42,118-j*12,8)
            label(item.get('status','Study').upper()[:80],42,57,7);footer();c.showPage()
    c.save()

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('catalogue');p.add_argument('--output',required=True);p.add_argument('--pdf',action='store_true');a=p.parse_args();print(f'{build(a.catalogue,a.output,a.pdf)} plates built')
if __name__=='__main__':main()
