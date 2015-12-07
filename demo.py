from foram import Foram

width, height = 600, 450
foram_params = [{'nchambers': 20, 'GF': 1.02, 'TF': 0.1, 'DeltaPhi': 0}]*6
foram_params[1] = {'nchambers': 25, 'GF': 1.1, 'TF': 0.7, 'DeltaPhi': 235}
foram_params[2] = {'nchambers': 20, 'GF': 1.1, 'TF': 0.05, 'DeltaPhi': 180}
foram_params[3] = {'nchambers': 50, 'GF': 1.2, 'TF': 0.3, 'DeltaPhi': -5}
foram_params[4] = {'nchambers': 60, 'GF': 1.03, 'TF': 0.3, 'DeltaPhi': -45}
foram_params[5] = {'nchambers': 60, 'GF': 1.0, 'TF': 0.6, 'DeltaPhi': -15}


svg_chunks = ["""<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
 xmlns:xlink="http://www.w3.org/1999/xlink"
 width="{}" height="{}" style="background: #ffffff">
""".format(width, height)]

scales = [10, 5, 5, 5, 10, 10]
for i, params in enumerate(foram_params):
    ix, iy = i % 3, i // 3
    cx, cy = width / 3 * (ix + 0.5), height / 2 * (iy + 0.5)
    foram = Foram(**params)
    foram.make_foram()
    for chamber in foram.chambers:
        svg_chunks.append(chamber.svg(scales[i], (cx, cy)))

svg_chunks.append('</svg>')
svg = '\n'.join(svg_chunks)

with open('foraminifera-demo.svg', 'w') as fo:
        print(svg, file=fo)
