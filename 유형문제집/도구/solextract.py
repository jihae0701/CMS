# 기본서 미주(해설) 중 지정한 번호만 꺼내 한글 파일로 만든다.
# python solextract.py <기본서.hwpx> <출력.hwpx> 27 30 ...
import zipfile, re, sys, os
SRC, OUT, NOS = sys.argv[1], sys.argv[2], sys.argv[3:]
z = zipfile.ZipFile(SRC)
files = {n: z.read(n) for n in z.namelist()}
x = files["Contents/section0.xml"].decode("utf-8")

# 1) 해당 번호의 미주 안 문단들
def note(NO):
    en = next(m.group(0) for m in re.finditer(r"<hp:endNote .*?</hp:endNote>", x, re.S)
              if re.search(r'<hp:autoNum num="%s" numType="ENDNOTE"' % NO, m.group(0)))
    a = en.index(">", en.index("<hp:subList")) + 1
    b = en.rindex("</hp:subList>")
    body = en[a:b]
    body = re.sub(r"<hp:ctrl><hp:autoNum .*?</hp:ctrl>", "", body, flags=re.S)       # 미주 번호 지우기
    body = re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", body, flags=re.S)
    # 'overx'처럼 명령어에 글자가 붙은 곳은 띄어 쓴다(한글 수식이 명령어로 읽도록)
    body = re.sub(r"(<hp:script[^>]*>)([^<]*)(</hp:script>)",
                  lambda m: m.group(1) + re.sub(r"(?<![A-Za-z])(over|root)(?!line)(?=[A-Za-z0-9])", r"\1 ", m.group(2)) + m.group(3), body)
    return body


# 2) 구역 정의: 원본 첫 문단의 secPr만 쓰고 한 단으로, 바탕쪽(머리말 디자인)은 빼기
head = x[:x.index("<hp:p ")]
p_open = re.match(r"<hp:p [^>]*>", x[len(head):]).group(0)
sec = re.search(r"<hp:secPr .*?</hp:secPr>", x, re.S).group(0)
sec = re.sub(r"<hp:masterPage [^>]*/>", "", sec)
sec = re.sub(r'masterPageCnt="\d+"', 'masterPageCnt="0"', sec)
first_cp = re.search(r'<hp:run charPrIDRef="(\d+)"><hp:secPr', x).group(1)
colpr = '<hp:ctrl><hp:colPr id="" type="NEWSPAPER" layout="LEFT" colCount="1" sameSz="1" sameGap="0"/></hp:ctrl>'

# 번호마다 제목 문단 + 해설 문단 (제목은 미주 첫 문단의 모양을 빌려 쓴다)
parts = []
for k, NO in enumerate(NOS):
    body = note(NO)
    fp = re.match(r"<hp:p [^>]*>", body).group(0)
    fcp = re.search(r'<hp:run charPrIDRef="(\d+)"', body).group(1)
    gap = ('%s<hp:run charPrIDRef="%s"><hp:t/></hp:run></hp:p>' % (fp, fcp)) if k else ""
    parts.append(gap + '%s<hp:run charPrIDRef="%s"><hp:t>[%s번 해설]</hp:t></hp:run></hp:p>' % (fp, fcp, NO) + body)
UNIT = re.match(r"(\d+)\.", os.path.basename(SRC))
title_all = "기본서 %s단원 " % (UNIT.group(1) if UNIT else "") + ", ".join(NOS) + "번 해설"

out_sec = (head + p_open + '<hp:run charPrIDRef="%s">' % first_cp + sec + colpr + "</hp:run></hp:p>"
           + "".join(parts) + "</hs:sec>")
files["Contents/section0.xml"] = out_sec.encode("utf-8")
files["Preview/PrvText.txt"] = title_all.encode("utf-8")
with zipfile.ZipFile(OUT, "w") as w:
    for n in z.namelist():
        info = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[n])
print("ok", OUT)
