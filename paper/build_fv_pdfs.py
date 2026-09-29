from __future__ import annotations
import re, html, sys
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, LongTable, TableStyle,
    Preformatted, HRFlowable
)

NAVY = colors.HexColor('#111d35')
BLUE = colors.HexColor('#2563eb')
MUTED = colors.HexColor('#5b6b88')
LIGHT = colors.HexColor('#dbe4f3')
PALE = colors.HexColor('#f5f8fc')
INK = colors.HexColor('#142033')

styles = getSampleStyleSheet()
BODY = ParagraphStyle('BodyFV', parent=styles['BodyText'], fontName='Helvetica', fontSize=9.5, leading=13.2, textColor=INK, spaceAfter=7, allowWidows=1, allowOrphans=1)
BODY_SMALL = ParagraphStyle('BodySmallFV', parent=BODY, fontSize=8.4, leading=11.0, spaceAfter=4)
H1 = ParagraphStyle('H1FV', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=17.5, leading=21, textColor=NAVY, spaceBefore=16, spaceAfter=8, keepWithNext=True)
H2 = ParagraphStyle('H2FV', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13.2, leading=16, textColor=NAVY, spaceBefore=12, spaceAfter=6, keepWithNext=True)
H3 = ParagraphStyle('H3FV', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=10.7, leading=13.2, textColor=NAVY, spaceBefore=9, spaceAfter=4, keepWithNext=True)
QUOTE = ParagraphStyle('QuoteFV', parent=BODY, leftIndent=18, rightIndent=18, borderPadding=6, backColor=PALE, fontName='Helvetica-Oblique')
BULLET = ParagraphStyle('BulletFV', parent=BODY, leftIndent=16, firstLineIndent=0, bulletIndent=5, spaceAfter=4)
NUM = ParagraphStyle('NumFV', parent=BODY, leftIndent=22, firstLineIndent=0, bulletIndent=2, spaceAfter=4)
CODE = ParagraphStyle('CodeFV', parent=BODY_SMALL, fontName='Courier', fontSize=7.2, leading=9.1, leftIndent=8, rightIndent=8, backColor=colors.HexColor('#f4f6f9'), borderPadding=6)
COVER_TITLE = ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=27, leading=31, textColor=NAVY, spaceAfter=20)
COVER_KICKER = ParagraphStyle('CoverKicker', fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=BLUE, tracking=1.2, spaceAfter=20)
COVER_DEK = ParagraphStyle('CoverDek', fontName='Helvetica', fontSize=13, leading=19, textColor=MUTED, spaceAfter=28)
COVER_META = ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=10.4, leading=15, textColor=INK, spaceAfter=6)
DOC_TITLE = ParagraphStyle('DocTitle', fontName='Helvetica-Bold', fontSize=15.5, leading=19, textColor=NAVY, spaceAfter=9)

def inline_md(s: str) -> str:
    supmap = str.maketrans({'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9','⁻':'-'})
    s = re.sub(r'[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+', lambda m: '^' + m.group(0).translate(supmap), s)
    s = html.escape(s, quote=False)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<link href="\2" color="#2563eb">\1</link>', s)
    s = re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', s)
    return s

def table_from(lines, avail_width, small=False):
    rows=[]
    for ln in lines:
        rows.append([c.strip() for c in ln.strip().strip('|').split('|')])
    if len(rows)>=2 and all(re.fullmatch(r':?-{3,}:?', c.replace(' ','')) for c in rows[1]):
        rows.pop(1)
    n=max(len(r) for r in rows)
    rows=[r+['']*(n-len(r)) for r in rows]
    weights=[]
    for j in range(n):
        mx=max(len(re.sub(r'[*\x60]', '', r[j])) for r in rows)
        weights.append(min(max(mx, 8), 36))
    total=sum(weights)
    colWidths=[avail_width*w/total for w in weights]
    cell_style = BODY_SMALL if small or n >= 4 else ParagraphStyle('TableCell', parent=BODY, fontSize=8.2, leading=10.4, spaceAfter=0)
    header_style = ParagraphStyle('TableHeader', parent=cell_style, fontName='Helvetica-Bold', textColor=NAVY)
    data=[[Paragraph(inline_md(c), header_style if i==0 else cell_style) for c in r] for i,r in enumerate(rows)]
    t=LongTable(data, colWidths=colWidths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#edf3ff')),
        ('TEXTCOLOR',(0,0),(-1,0),NAVY),
        ('GRID',(0,0),(-1,-1),0.35,colors.HexColor('#c9d4e6')),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))
    return t

def markdown_flowables(text: str, avail_width: float, skip_first_h1=True):
    lines=text.splitlines(); flows=[]; i=0; current_section=''; paragraph=[]; first_h1_skipped=False
    def flush_para():
        nonlocal paragraph
        if paragraph:
            txt=' '.join(x.strip() for x in paragraph).strip()
            if txt:
                st=BODY_SMALL if current_section.lower()=='references' else BODY
                flows.append(Paragraph(inline_md(txt), st))
            paragraph=[]
    while i<len(lines):
        stripped=lines[i].strip()
        if not stripped:
            flush_para(); i+=1; continue
        if stripped.startswith('```'):
            flush_para(); i+=1; code=[]
            while i<len(lines) and not lines[i].strip().startswith('```'):
                code.append(lines[i]); i+=1
            i+=1; flows.append(Preformatted('\n'.join(code), CODE)); flows.append(Spacer(1,5)); continue
        if stripped.startswith('|') and '|' in stripped[1:]:
            flush_para(); tlines=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                tlines.append(lines[i]); i+=1
            flows.append(table_from(tlines, avail_width, small=(current_section.lower()=='references'))); flows.append(Spacer(1,7)); continue
        m=re.match(r'^(#{1,3})\s+(.*)$', stripped)
        if m:
            flush_para(); level=len(m.group(1)); title=m.group(2)
            if level==1 and skip_first_h1 and not first_h1_skipped:
                first_h1_skipped=True; i+=1; continue
            if level==2: current_section=re.sub(r'^\d+\.\s*','',title)
            style={1:H1,2:H1,3:H2}.get(level,H3)
            flows.append(Paragraph(inline_md(title), style))
            flows.append(HRFlowable(width='100%', thickness=0.8 if level<=2 else 0.4, color=BLUE if level<=2 else LIGHT, spaceBefore=0, spaceAfter=7))
            i+=1; continue
        if stripped=='---':
            flush_para(); flows.append(HRFlowable(width='100%', thickness=0.5, color=LIGHT, spaceBefore=5, spaceAfter=7)); i+=1; continue
        if stripped.startswith('>'):
            flush_para(); q=[]
            while i<len(lines) and lines[i].strip().startswith('>'):
                q.append(lines[i].strip()[1:].strip()); i+=1
            flows.append(Paragraph(inline_md(' '.join(q)), QUOTE)); continue
        if re.match(r'^[-*]\s+', stripped):
            flush_para(); item=re.sub(r'^[-*]\s+','',stripped); i+=1; cont=[]
            while i<len(lines):
                s=lines[i].strip()
                if not s or re.match(r'^[-*]\s+',s) or re.match(r'^\d+\.\s+',s) or s.startswith('#') or s.startswith('|') or s.startswith('```') or s=='---': break
                cont.append(s); i+=1
            if cont: item += ' ' + ' '.join(cont)
            flows.append(Paragraph(inline_md(item), BULLET, bulletText='•')); continue
        om=re.match(r'^(\d+)\.\s+(.*)$', stripped)
        if om:
            flush_para(); num=om.group(1); item=om.group(2); i+=1; cont=[]
            while i<len(lines):
                s=lines[i].strip()
                if not s or re.match(r'^\d+\.\s+',s) or re.match(r'^[-*]\s+',s) or s.startswith('#') or s.startswith('|') or s.startswith('```') or s=='---': break
                cont.append(s); i+=1
            if cont: item += ' ' + ' '.join(cont)
            st=ParagraphStyle(f'Num{num}', parent=BODY_SMALL if current_section.lower()=='references' else NUM, leftIndent=22, firstLineIndent=0, bulletIndent=1, spaceAfter=3)
            flows.append(Paragraph(inline_md(item), st, bulletText=f'{num}.')); continue
        paragraph.append(lines[i]); i+=1
    flush_para(); return flows

def footer(canvas, doc):
    canvas.saveState(); w,h=letter
    canvas.setStrokeColor(colors.HexColor('#d8e0eb')); canvas.setLineWidth(0.4)
    canvas.line(doc.leftMargin, 28, w-doc.rightMargin, 28)
    canvas.setFillColor(MUTED); canvas.setFont('Helvetica', 6.7)
    canvas.drawString(doc.leftMargin, 15, 'Fabric Vitals v0.2 · a technical proposal for discussion')
    canvas.drawRightString(w-doc.rightMargin, 15, str(doc.page))
    canvas.restoreState()

def build_paper(md_path, out_path):
    text=Path(md_path).read_text(encoding='utf-8')
    title=re.search(r'^#\s+(.+)$', text, re.M).group(1)
    status=re.search(r'^\*(Fabric Vitals v0\.2.+?)\*$', text, re.M).group(1)
    body=text[text.index('## Summary'):]
    doc=SimpleDocTemplate(out_path,pagesize=letter,rightMargin=55,leftMargin=55,topMargin=52,bottomMargin=42,title=title,author='Shankar Gopidas')
    avail=letter[0]-doc.leftMargin-doc.rightMargin
    f=[Spacer(1,36), HRFlowable(width='100%', thickness=3.2, color=BLUE, spaceAfter=150),
       Paragraph('TECHNICAL PROPOSAL FOR DISCUSSION', COVER_KICKER),
       Paragraph(inline_md(title), COVER_TITLE),
       Paragraph('A proposed health score for AI data-center back-end scale-out fabrics. It measures how well the fabric is keeping the promises on its Fabric Spec Sheet, under a common Rulebook.', COVER_DEK),
       Paragraph('<b>Shankar Gopidas</b>, Founder &amp; CEO, datacenternetwork.ai', COVER_META),
       Paragraph(inline_md(status.replace('(draft) — ','· ')), ParagraphStyle('CoverStatus', parent=COVER_META, textColor=MUTED)),
       Spacer(1,125), HRFlowable(width='100%', thickness=0.5, color=LIGHT, spaceAfter=10),
       Paragraph('<b>Specification and open questions:</b> github.com/fabric-vitals/spec &nbsp;·&nbsp; <b>Contact:</b> hello@datacenternetwork.ai', ParagraphStyle('coverfoot', parent=BODY_SMALL, textColor=MUTED)),
       Paragraph('Licensed CC BY 4.0. “Fabric Vitals” and “Vitals Score” are claimed as marks of datacenternetwork.ai; see the trademark policy in the repository.', ParagraphStyle('coverfoot2', parent=BODY_SMALL, textColor=colors.HexColor('#8090aa'))),
       PageBreak()]
    f.extend(markdown_flowables(body, avail, skip_first_h1=False))
    doc.build(f,onFirstPage=footer,onLaterPages=footer)

def build_simple(md_path, out_path):
    text=Path(md_path).read_text(encoding='utf-8')
    m=re.search(r'^#\s+(.+)$',text,re.M); title=m.group(1) if m else Path(md_path).stem
    doc=SimpleDocTemplate(out_path,pagesize=letter,rightMargin=54,leftMargin=54,topMargin=54,bottomMargin=42,title=title,author='Shankar Gopidas')
    avail=letter[0]-doc.leftMargin-doc.rightMargin
    flows=[Paragraph(inline_md(title), DOC_TITLE), HRFlowable(width='100%', thickness=1.2, color=BLUE, spaceAfter=8)]
    flows.extend(markdown_flowables(text, avail, skip_first_h1=True))
    doc.build(flows,onFirstPage=footer,onLaterPages=footer)

if __name__=='__main__':
    if len(sys.argv)<4:
        print('usage: build_fv_pdfs.py paper|simple input.md output.pdf'); sys.exit(2)
    mode,inp,out=sys.argv[1:4]
    if mode=='paper': build_paper(inp,out)
    else: build_simple(inp,out)
