from foram import Foram

width, height = 600, 450
foram_params = []
foram_params.append({'nchambers': 20, 'GF': 1.02, 'TF': 0.4, 'DeltaPhi': 25})
foram_params.append({'nchambers': 20, 'GF': 1.08, 'TF': 0.9, 'DeltaPhi': 105})
foram_params.append({'nchambers': 85, 'GF': 1.0, 'TF': 0.7, 'DeltaPhi': 270})
foram_params.append({'nchambers': 6, 'GF': 1.2, 'TF': 0.3, 'DeltaPhi': 45})
foram_params.append({'nchambers': 20, 'GF': 1, 'TF': 0.8, 'DeltaPhi': 0})
foram_params.append({'nchambers': 20, 'GF': 1.05, 'TF': 0.7, 'DeltaPhi': -180})

svg_chunks = ["""<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
 xmlns:xlink="http://www.w3.org/1999/xlink"
 width="{}" height="{}" style="background: #ffffff">
""".format(width, height)]

edge_colour = '#331100'
fill_colour = '#eeddbb'
scales = [10, 5, 5, 5, 10, 10]
for i, params in enumerate(foram_params):
    ix, iy = i % 3, i // 3
    cx, cy = width / 3 * (ix + 0.5), height / 2 * (iy + 0.5)
    foram = Foram(**params)
    foram.make_foram()
    for chamber in foram.chambers:
        svg_chunks.append(chamber.svg(scales[i], (cx, cy), fill_colour,
                                      edge_colour))

svg_chunks.append('</svg>')
svg = '\n'.join(svg_chunks)

with open('foraminifera-demo2.svg', 'w') as fo:
        print(svg, file=fo)
