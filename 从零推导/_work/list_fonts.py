import re, sys
s = open(sys.argv[1], encoding='utf-8').read()
blocks = re.findall(r'@font-face\{(.{0,400}?)\}', s, re.S)
print('blocks', len(blocks))
for b in blocks:
    fam = re.search(r'font-family:([^;]+)', b)
    print(('DATA' if 'data:font' in b else 'NONE'),
          fam.group(1) if fam else '?',
          'len', len(b))
