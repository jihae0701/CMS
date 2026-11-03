"""pyhwp로 본문을 끝까지 해석해 본다(구조 검사). python3 validate_pyhwp.py 파일.hwp ..."""
import sys, os, logging
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pyhwp_x', 'pyhwp-0.1b15', 'src'))
logging.disable(logging.CRITICAL)
from hwp5.xmlmodel import Hwp5File
from hwp5.binmodel import ParaText
def check(path):
    f = Hwp5File(path)
    n = 0; texts = 0; problems = []
    for sec in f.bodytext.sections:
        for m in sec.models():
            n += 1
            t = m.get('type')
            name = getattr(t, '__name__', str(t))
            if 'Unknown' in name or 'Error' in name or m.get('unparsed'):
                problems.append((name, m.get('seqno')))
            if name == 'ParaText':
                texts += 1
    # xml 변환까지 (문단·제어 짝 맞추기 검사 포함)
    import io
    from hwp5.xmlmodel import Section
    out = io.BytesIO()
    events = 0
    for sec in f.bodytext.sections:
        for ev in sec.events():
            events += 1
    return n, texts, events, problems[:5]
for p in sys.argv[1:]:
    try:
        print(os.path.basename(p), *check(p))
    except Exception as e:
        print(os.path.basename(p), 'FAIL', type(e).__name__, str(e)[:200])
