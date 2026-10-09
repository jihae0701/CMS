# -*- coding: utf-8 -*-
"""두 HWPX의 header.xml을 합치고, 둘째 문서의 본문 XML을 첫째 문서의 번호 체계로 바꾼다."""
import re

LISTS = [("borderFills", "borderFill"), ("charProperties", "charPr"), ("tabProperties", "tabPr"),
         ("numberings", "numbering"), ("bullets", "bullet"), ("paraProperties", "paraPr"), ("styles", "style")]


def elems(h, tag):
    """(id, xml) 목록"""
    out = []
    for m in re.finditer(r'<hh:%s\b[^>]*?(?:/>|>.*?</hh:%s>)' % (tag, tag), h, re.S):
        x = m.group(0)
        out.append((int(re.search(r'\bid="(\d+)"', x).group(1)), x))
    return out


def strip_id(x):
    return re.sub(r'\bid="\d+"', 'id="#"', x, count=1)


def fonts(h):
    """{lang: [(id, xml)]}"""
    out = {}
    for m in re.finditer(r'<hh:fontface lang="(\w+)" fontCnt="\d+">(.*?)</hh:fontface>', h, re.S):
        out[m.group(1)] = [(int(re.search(r'\bid="(\d+)"', f).group(1)), f)
                           for f in re.findall(r'<hh:font\b.*?</hh:font>|<hh:font\b[^>]*/>', m.group(2), re.S)]
    return out


LANG_ATTR = {"HANGUL": "hangul", "LATIN": "latin", "HANJA": "hanja", "JAPANESE": "japanese",
             "OTHER": "other", "SYMBOL": "symbol", "USER": "user"}


class Merger:
    def __init__(self, hA, hB):
        self.hA, self.hB = hA, hB
        self.map = {}
        self._fonts()
        self._list("borderFill", self._fix_bf)
        self._list("tabPr", lambda x: x)
        self._list("charPr", self._fix_cp)
        self._list("numbering", self._fix_num)
        self._list("bullet", self._fix_num)
        self._list("paraPr", self._fix_pp)
        self._styles()

    # ------------------------------------------------------------ 글꼴
    def _fonts(self):
        fa, fb = fonts(self.hA), fonts(self.hB)
        self.fontmap = {}
        for lang, lst in fb.items():
            mp = {}
            a = fa[lang]
            for fid, fx in lst:
                key = re.sub(r'\bid="\d+"', '', fx)
                hit = [i for i, ax in a if re.sub(r'\bid="\d+"', '', ax) == key]
                if hit:
                    mp[fid] = hit[0]
                else:
                    nid = max(i for i, _ in a) + 1
                    nx = re.sub(r'\bid="\d+"', 'id="%d"' % nid, fx, count=1)
                    a.append((nid, nx))
                    mp[fid] = nid
                    blk = re.search(r'(<hh:fontface lang="%s" fontCnt=")(\d+)(">)(.*?)(</hh:fontface>)' % lang, self.hA, re.S)
                    self.hA = (self.hA[:blk.start()] + blk.group(1) + str(len(a)) + blk.group(3) + blk.group(4) + nx
                               + blk.group(5) + self.hA[blk.end():])
            self.fontmap[lang] = mp

    # ------------------------------------------------------------ 번호 고치기
    def _fix_bf(self, x):
        return x

    def _fix_cp(self, x):
        def fr(m):
            attrs = m.group(1)
            for lang, at in LANG_ATTR.items():
                attrs = re.sub(r'\b%s="(\d+)"' % at, lambda mm: '%s="%d"' % (at, self.fontmap[lang][int(mm.group(1))]), attrs)
            return "<hh:fontRef" + attrs + "/>"
        x = re.sub(r'<hh:fontRef([^>]*)/>', fr, x)
        return re.sub(r'borderFillIDRef="(\d+)"', lambda m: 'borderFillIDRef="%d"' % self.map["borderFill"][int(m.group(1))], x)

    def _fix_num(self, x):
        return re.sub(r'charPrIDRef="(\d+)"', lambda m: m.group(0) if m.group(1) == "4294967295"
                      else 'charPrIDRef="%d"' % self.map["charPr"][int(m.group(1))], x)

    def _fix_pp(self, x):
        x = re.sub(r'tabPrIDRef="(\d+)"', lambda m: 'tabPrIDRef="%d"' % self.map["tabPr"][int(m.group(1))], x)
        x = re.sub(r'borderFillIDRef="(\d+)"', lambda m: 'borderFillIDRef="%d"' % self.map["borderFill"][int(m.group(1))], x)

        def hd(m):
            typ, idr = m.group(1), int(m.group(2))
            if typ == "NUMBER" and idr:
                idr = self.map["numbering"][idr]
            elif typ == "BULLET" and idr:
                idr = self.map["bullet"][idr]
            return '<hh:heading type="%s" idRef="%d"' % (typ, idr)
        return re.sub(r'<hh:heading type="(\w+)" idRef="(\d+)"', hd, x)

    def _list(self, tag, fix):
        plural = [p for p, s in LISTS if s == tag][0]
        A = elems(self.hA, tag)
        B = elems(self.hB, tag)
        mp = {}
        known = {strip_id(x): i for i, x in A}
        nxt = max([i for i, _ in A], default=-1) + 1
        added = []
        for bid, bx in B:
            fx = fix(bx)
            k = strip_id(fx)
            if k in known:
                mp[bid] = known[k]
            else:
                nx = re.sub(r'\bid="\d+"', 'id="%d"' % nxt, fx, count=1)
                known[k] = nxt
                mp[bid] = nxt
                added.append(nx)
                nxt += 1
        self.map[tag] = mp
        if added:
            m = re.search(r'(<hh:%s itemCnt=")(\d+)(">)(.*?)(</hh:%s>)' % (plural, plural), self.hA, re.S)
            if not m:
                raise ValueError("no list " + plural)
            self.hA = (self.hA[:m.start()] + m.group(1) + str(int(m.group(2)) + len(added)) + m.group(3)
                       + m.group(4) + "".join(added) + m.group(5) + self.hA[m.end():])

    def _styles(self):
        A = elems(self.hA, "style")
        B = elems(self.hB, "style")
        byname = {re.search(r'\bname="([^"]*)"', x).group(1): i for i, x in A}
        mp = {}
        nxt = max(i for i, _ in A) + 1
        added = []
        for bid, bx in B:
            name = re.search(r'\bname="([^"]*)"', bx).group(1)
            if name in byname:
                mp[bid] = byname[name]
        for bid, bx in B:
            if bid in mp:
                continue
            mp[bid] = nxt
            nxt += 1
        for bid, bx in B:
            name = re.search(r'\bname="([^"]*)"', bx).group(1)
            if name in byname:
                continue
            nx = re.sub(r'\bid="\d+"', 'id="%d"' % mp[bid], bx, count=1)
            nx = re.sub(r'paraPrIDRef="(\d+)"', lambda m: 'paraPrIDRef="%d"' % self.map["paraPr"][int(m.group(1))], nx)
            nx = re.sub(r'charPrIDRef="(\d+)"', lambda m: 'charPrIDRef="%d"' % self.map["charPr"][int(m.group(1))], nx)
            nx = re.sub(r'nextStyleIDRef="(\d+)"', lambda m: 'nextStyleIDRef="%d"' % mp[int(m.group(1))], nx)
            added.append(nx)
        self.map["style"] = mp
        if added:
            m = re.search(r'(<hh:styles itemCnt=")(\d+)(">)(.*?)(</hh:styles>)', self.hA, re.S)
            self.hA = (self.hA[:m.start()] + m.group(1) + str(int(m.group(2)) + len(added)) + m.group(3)
                       + m.group(4) + "".join(added) + m.group(5) + self.hA[m.end():])

    # ------------------------------------------------------------ 본문
    def body(self, x):
        """둘째 문서 본문 조각의 번호를 첫째 문서 번호로 바꾼다"""
        m = self.map
        x = re.sub(r'paraPrIDRef="(\d+)"', lambda g: 'paraPrIDRef="%d"' % m["paraPr"][int(g.group(1))], x)
        x = re.sub(r'styleIDRef="(\d+)"', lambda g: 'styleIDRef="%d"' % m["style"][int(g.group(1))], x)
        x = re.sub(r'charPrIDRef="(\d+)"', lambda g: 'charPrIDRef="%d"' % m["charPr"][int(g.group(1))], x)
        x = re.sub(r'borderFillIDRef="(\d+)"', lambda g: 'borderFillIDRef="%d"' % m["borderFill"][int(g.group(1))], x)
        return x
