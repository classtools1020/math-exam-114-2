# -*- coding: utf-8 -*-
"""把 _figs/*.png 依錨點插入考卷 document.xml。先驗證錨點唯一，否則中止。"""
import re, os, shutil, sys
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
UNP = os.path.join(ROOT, '_unpacked')
DOCXML = os.path.join(UNP, 'word', 'document.xml')
RELS = os.path.join(UNP, 'word', '_rels', 'document.xml.rels')
MEDIA = os.path.join(UNP, 'word', 'media')
FIGS = os.path.join(ROOT, '_figs')

# (圖檔, 錨點文字) — 圖插在「含此錨點的段落」之後
MAP = [
    ('fA3q2.png', '如果 AD = 8，AB = 5'),
    ('fA3q3.png', '如果 ∠A = 70°'),
    ('fA5q1.png', '請判斷下列生活中的物品'),
    ('fB1q1.png', '判斷下列三條線段能否組成三角形？（寫出驗證過程）'),
    ('fB1q2.png', '三角形兩邊長分別是 5 和 8'),
    ('fB1q3.png', '三角形兩邊長分別是 4 和 9'),
    ('fB1q4.png', '小明家到學校有兩條路'),
    ('fB2q2.png', '∠1 = 110°，求 ∠2'),
    ('fB2q3.png', '∠1 = 75°，求 ∠2'),
    ('fB2q4.png', '判斷下列敘述是否正確？（打 O 或 X）'),
    ('fB2q5.png', '公園小路有兩條平行的直路甲、乙'),
    ('fB3q1.png', 'AD = 12，AB = 7'),
    ('fB3q2.png', '∠A = 55°，求所有角'),
    ('fB3q3.png', '若 AO = 6，BO = 4'),
    ('fB3q4.png', '判斷下列四邊形是否為平行四邊形'),
    ('fB3q5.png', '飛毯遊樂設施的座椅框架'),
    ('fB4q1.png', '判斷下列四邊形的類型'),
    ('fB4q2.png', '菱形 ABCD 的周長是 36'),
    ('fB4q3.png', '長方形 ABCD 中，AC 和 BD 交於 O 點。若 AC = 10'),
    ('fB4q4.png', '箏形 ABCD 中，AB = 6，CD = 12'),
    ('fB4q5.png', '等腰梯形 ABCD 中，AB // CD，∠A = 65°'),
    ('fB4q6.png', '菱形 ABCD 中，AC = 8，BD = 6'),
    ('fC1q1.png', '下列哪組線段可以組成三角形'),
    ('fC1q2.png', '夾角為 72°'),
    ('fC1q3.png', '∠A = 3∠B'),
    ('fC1q4.png', '下列何者不是平行四邊形的性質'),
    ('fC1q5.png', '正方形的兩條對角線具有哪些性質'),
    ('fC2q1.png', '三角形兩邊長為 7 和 12'),
    ('fC2q2.png', '三角形兩邊長為 6 和 10'),
    ('fC2q3.png', '∠1 = 48°'),
    ('fC2q4.png', 'AB = 15，BC = 9'),
    ('fC2q5.png', 'AC = 16，BD = 10'),
    ('fC2q6.png', '菱形 ABCD 的對角線 AC = 10，BD = 24'),
    ('fC2q7.png', '∠A = 72°'),
    ('fC2q8.png', '正方形 ABCD 的對角線長為 10'),
    ('fC3q1.png', 'AB = x + 3，BC = 2x - 1'),
    ('fC3q2.png', '∠1 = 100°，∠2 = 127°'),
    ('fC3q3.png', '∠A 比 ∠B 多 40°'),
    ('fC3q4.png', '若 OA = 5，AB = 6'),
    ('fC4q1.png', '竹籬笆圍花圃'),
    ('fC4q2.png', '校園平行步道'),
    ('fC4q3.png', '風箏面積'),
    ('fC4q4.png', '四邊形分類'),
]

def para_text(block):
    return ''.join(re.findall(r'<w:t[^>]*>(.*?)</w:t>', block, re.S))

def emu_size(path):
    im = Image.open(path); w, h = im.size
    aspect = w / h
    if aspect > 2.3:
        win = 5.2
    elif aspect > 1.45:
        win = 4.3
    else:
        win = 3.4
    hin = win / aspect
    return int(win * 914400), int(hin * 914400)

def drawing_para(rid, name, cx, cy):
    return f'''<w:p>
      <w:pPr>
        <w:spacing w:after="120" w:before="60" w:lineRule="auto"/>
        <w:jc w:val="center"/>
        <w:rPr/>
      </w:pPr>
      <w:r>
        <w:rPr/>
        <w:drawing>
          <wp:inline distB="0" distT="0" distL="0" distR="0">
            <wp:extent cx="{cx}" cy="{cy}"/>
            <wp:effectExtent b="0" l="0" r="0" t="0"/>
            <wp:docPr descr="題目圖解" id="0" name="{name}"/>
            <a:graphic>
              <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
                <pic:pic>
                  <pic:nvPicPr>
                    <pic:cNvPr descr="題目圖解" id="0" name="{name}"/>
                    <pic:cNvPicPr preferRelativeResize="0"/>
                  </pic:nvPicPr>
                  <pic:blipFill>
                    <a:blip r:embed="{rid}"/>
                    <a:srcRect b="0" l="0" r="0" t="0"/>
                    <a:stretch><a:fillRect/></a:stretch>
                  </pic:blipFill>
                  <pic:spPr>
                    <a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
                    <a:prstGeom prst="rect"/>
                    <a:ln/>
                  </pic:spPr>
                </pic:pic>
              </a:graphicData>
            </a:graphic>
          </wp:inline>
        </w:drawing>
      </w:r>
    </w:p>'''

def main():
    doc = open(DOCXML, encoding='utf-8').read()
    rels = open(RELS, encoding='utf-8').read()
    blocks = re.findall(r'<w:p\b(?:(?!</w:p>).)*?</w:p>', doc, re.S)

    # 1) 驗證錨點唯一
    errors = []
    targets = {}
    for fig, anchor in MAP:
        hits = [b for b in blocks if anchor in para_text(b)]
        if len(hits) != 1:
            errors.append(f'  {fig}: 錨點「{anchor}」命中 {len(hits)} 個段落')
        else:
            targets[fig] = hits[0]
    if errors:
        print('錨點驗證失敗，已中止：')
        print('\n'.join(errors))
        sys.exit(1)
    print(f'錨點驗證通過：{len(targets)} 題全部唯一命中')

    # 2) 既有 rId 最大值
    ids = [int(m) for m in re.findall(r'Id="rId(\d+)"', rels)]
    nid = max(ids) + 1
    # 既有 media image 編號最大值
    imgs = [int(m) for m in re.findall(r'image(\d+)\.png', rels)]
    nimg = max(imgs) + 1

    new_rels = []
    for fig, anchor in MAP:
        rid = f'rId{nid}'; nid += 1
        imgname = f'image{nimg}.png'; nimg += 1
        shutil.copy(os.path.join(FIGS, fig), os.path.join(MEDIA, imgname))
        new_rels.append(f'<Relationship Id="{rid}" '
                        f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                        f'Target="media/{imgname}"/>')
        cx, cy = emu_size(os.path.join(FIGS, fig))
        para = drawing_para(rid, imgname, cx, cy)
        block = targets[fig]
        assert doc.count(block) == 1, f'{fig} 段落非唯一'
        doc = doc.replace(block, block + '\n    ' + para, 1)

    rels = rels.replace('</Relationships>', '\n  '.join(new_rels) + '\n</Relationships>')
    open(DOCXML, 'w', encoding='utf-8').write(doc)
    open(RELS, 'w', encoding='utf-8').write(rels)
    print(f'插入完成：{len(MAP)} 張圖，新增 rId 起始 {max(ids)+1}，image 起始 {max(imgs)+1}')

if __name__ == '__main__':
    main()
