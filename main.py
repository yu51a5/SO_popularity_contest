import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np

my_color_palette = {'superGold'   : '#ffb000',
                      'Burgundy'   : "#920000",
                     'superPink'   : '#dc267f',
                     'superViolet' : '#785ef0',
                     'superOrange' : '#fe6100',
                      'superBlue'   : '#648fff'}


df = pd.DataFrame({'tagged': [70205, 1991, 46978, 7271, 3159, 87727, 2153, 15655, 3628]},
                  index=['list', 'range', 'dictionary', 'tuple', 'set', 'dataframe', 'series', 'class',  'ndarray'])
plot = df.plot.pie(y='tagged', figsize=(8, 5), startangle=15, 
                  colors=[c for c in my_color_palette.values()] + ["white", 'black', 'silver'],
                  labels=[''] * len(df.index))
#plot.legend(labels=df.index, loc="upper left", bbox_to_anchor=(-0.4, 0.5))
plot.set_title("Number of Stackoverflow Questions With Tags [python] and [<type name>]\nas of 01 June 2023")
plot.yaxis.label.set_visible(False)
plot.get_legend().remove()

# source: https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_and_donut_labels.html#sphx-glr-gallery-pie-and-polar-charts-pie-and-donut-labels-py
bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

wedges = [w for w in plot.get_children() if type(w) is Wedge]
ang_mult_dict = {'tuple' : 0.2, 'class' : 0.57, 'list' : 0.35}
for label_, how_many, p in zip(df.index, df['tagged'], wedges):
    mult_ang = ang_mult_dict[label_] if label_ in ang_mult_dict else 0.5
    ang = (p.theta2 - p.theta1)*mult_ang + p.theta1
    ang2 = np.deg2rad(ang)
    y = np.sin(ang2)
    x = np.cos(ang2)
    kw["arrowprops"]["connectionstyle"] =  f"angle,angleA=0,angleB={ang}"
    plot.annotate(label_ + "\n" + str(how_many) + " questions", xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y), horizontalalignment="left" if x >= 0 else "right", **kw)
  
plt.show()
