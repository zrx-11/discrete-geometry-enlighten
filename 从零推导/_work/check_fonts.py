import re, sys
for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    bad = re.findall(r'url\((?!data:)[^)]*\)', s)
    print(f, len(bad), 'data-fonts:', s.count('data:font/woff2'), bad[:3])
