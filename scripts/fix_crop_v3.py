from PIL import Image
import numpy as np

img = Image.open('/tmp/approved2.png')
w, h = img.size
print('src', w, h)

arr = np.array(img.convert('L'))
top_content = 0
for row in range(0, h // 3):
    if arr[row].mean() > 40:
        top_content = row
        break

print('top content row:', top_content)
th = int(w / 2.5)
if h - top_content >= th:
    crop = img.crop((0, top_content, w, top_content + th))
    crop = crop.resize((2500, 1000), Image.LANCZOS)
    crop.save('/home/hermes-workspace/robot-man/images/tailcat_cover_approved_v3.png')
    print('saved shifted crop, top at', top_content)
else:
    print('cannot fit by shifting; available height', h - top_content, '< needed', th)
