import sys
sys.path.insert(0, '/home/user/Doubao/chats/38451880444500994/离散几何处理点化学习/从零推导/_work')
import build
css = build.font_css()
print('blocks', css.count('@font-face'), 'data', css.count('data:font'), 'srcrefs', css.count('src:'))
import re
print(re.findall(r'@font-face\{font-family:([^;]+)', css))
