"""P57 independent isolated checks; NOT an upstream checkout or upstream pytest."""
import json,sqlite3,sys,platform,unicodedata,re
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
import fitz
from pypdf import PdfReader

def safe_fts_query(user_input: str, *, advanced: bool = False) -> str:
    # Mirrored verbatim algorithm from upstream core/fts.py @ 7230f8, lines 19-45
    if not isinstance(user_input, str):
        raise TypeError(f"expected str, got {type(user_input).__name__}")
    if advanced:
        return user_input
    if not user_input.strip():
        return ""
    tokens = re.compile(r'[^\s"]+').findall(user_input)
    if not tokens:
        return ""
    quoted = [f'"{t.replace(chr(34), chr(34) * 2)}"' for t in tokens]
    return " ".join(quoted)

def offsets(haystack, needle):
    out=[]; start=0
    while True:
        i=haystack.find(needle,start)
        if i<0: return out
        out.append((i,i+len(needle)));start=i+1

def main():
    c=sqlite3.connect(':memory:')
    c.execute("CREATE VIRTUAL TABLE f USING fts5(text, tokenize='porter unicode61')")
    docs=['anatta anatta anatta anatta anatta','anattā','vô thường','vo thuong','無常','无常','á','á','d','đ','foo\nbar', 'anatta x']
    for k,s in enumerate(docs,1): c.execute('INSERT INTO f(rowid,text) VALUES(?,?)',(k,s))
    queries=['anatta','anattā','vô thường','vo thuong','無常','无常','無','常','无','á','á','d','đ','foo bar','anatta x']
    records=[]
    for q in queries:
        try:
            ids=[r[0] for r in c.execute('SELECT rowid FROM f WHERE f MATCH ? ORDER BY rowid',(safe_fts_query(q),)).fetchall()]
        except Exception as e: ids='ERROR: '+str(e)
        exact_ids=[i for i,s in enumerate(docs,1) if q in s]
        records.append({'q':q,'q_codepoints':[f'U+{ord(ch):04X}' for ch in q], 'fts_ids':ids, 'exact_ids':exact_ids})
    print('ENV',json.dumps({'python':platform.python_version(),'sqlite':sqlite3.sqlite_version,'fitz':fitz.VersionBind,'pypdf':'5.9.0','OS':platform.platform()},ensure_ascii=False))
    print('FTS_ORACLE',json.dumps(records,ensure_ascii=False))
    print('OCCURRENCE',json.dumps({'query':'anatta','row1_offsets':offsets(docs[0],'anatta'), 'row1_fts_result_count':len([r for r in c.execute('SELECT rowid FROM f WHERE f MATCH ? AND rowid=1',(safe_fts_query('anatta'),))])}))
    with TemporaryDirectory() as td:
        p=Path(td)/'sample.pdf'
        doc=fitz.open()
        page=doc.new_page();page.insert_text((40,60),'Synthetic page: anatta, all rights cleared')
        doc.new_page() # blank, no OCR
        page=doc.new_page();page.insert_text((40,60),'Synthetic third page: anatta')
        doc.save(str(p));doc.close()
        reader=PdfReader(str(p));out=[]
        for i,page in enumerate(reader.pages):
            try: content=(page.extract_text() or '').strip()
            except Exception: content=''
            status='ok' if len(content)>=5 else 'no_text_layer'
            out.append({'page':i+1,'status':status,'text_len':len(content),'bbox':None})
        print('PDF_PAGE_EXTRACTION',json.dumps(out,ensure_ascii=False))
    print('NOTE upstream full pytest, actual import/index and reader UI NOT RUN')
if __name__=='__main__':main()
