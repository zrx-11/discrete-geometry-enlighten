import io, re
p = '/home/user/Doubao/chats/38451880444500994/离散几何处理点化学习/从零推导/_work/build.py'
s = open(p, encoding='utf-8').read()
start = s.index('def font_css():')
end = s.index('CSS = r"""')
new = '''def font_css():
    css = open(os.path.join(ASSETS, "katex.min.css"), encoding="utf-8").read()

    def fix_block(m):
        block = m.group(0)
        names = sorted(set(re.findall(r"fonts/([A-Za-z0-9_\\-]+)\\.woff2", block)))
        parts = []
        for n in names:
            fp = os.path.join(ASSETS, "fonts", n + ".woff2")
            if not os.path.exists(fp):
                continue
            b64 = base64.b64encode(open(fp, "rb").read()).decode()
            parts.append('url(data:font/woff2;base64,%s) format("woff2")' % b64)
        if not parts:
            return block
        i = block.find("src:")
        j = block.rfind("}")
        return block[:i] + "src:" + ",".join(parts) + block[j:]

    css = re.sub(r"@font-face\\{[^}]*\\}", fix_block, css)
    return css


'''
s = s[:start] + new + s[end:]
open(p, 'w', encoding='utf-8').write(s)
print('patched font_css')
