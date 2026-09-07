from PIL import Image

img = Image.open('/tmp/approved2.png')
w, h = img.size
th = int(w / 2.5)

for off in (20, 40, 60):
    if off + th <= h:
        crop = img.crop((0, off, w, off + th)).resize((2500, 1000), Image.LANCZOS)
        crop.save(f'/home/hermes-workspace/robot-man/images/tailcat_cover_cand_{off}.png')
        print('saved offset', off)
