# https://stackoverflow.com/questions/62586521/stack-exchange-api-with-curl-command/62605055#62605055
# https://hoffa.medium.com/finding-the-real-top-stack-overflow-questions-aebf35b095f1
# https://stackoverflow.com/users/12671057/kelly-bundy
# https://stackoverflow.com/questions/62763982/how-can-i-find-the-number-of-views-all-matlab-questions-have-received
# https://data.stackexchange.com/stackoverflow/query/1805161

#addon = "2.3/questions?tagged=stackexchange-api"
#url = f"https://api.stackexchange.com/{addon}&site=stackoverflow&access_token={os.environ['access_token']}&key={os.environ['key']}"
#print(requests.get(url).text)

import os
from datetime import datetime

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

my_color_palette = { 'superGold'   : '#ffb000',
                     'lightBlue'   : "#d1d1ff",
                     'Burgundy'    : "#920000",
                     'superPink'   : '#dc267f',
                     'superViolet' : '#785ef0',
                     'gray'        : '#aaaaaa',
                     'superOrange' : '#fe6100',
                     'superBlue'   : '#648fff',
                     'lightPink'   : "#ffd1d1"}

# source: https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_and_donut_labels.html#sphx-glr-gallery-pie-and-polar-charts-pie-and-donut-labels-py
kw = dict(arrowprops=dict(arrowstyle="-"), 
          bbox=dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72), 
          zorder=0, 
          va="center")

def plot_pies(filename, title=None, annotation_angle_adjustments={}, fig_height=5, fig_width={'question':10, 'viewed': 10}, start_angles={}, dpi=300, image_extension='png'):
  
  last_modif_date = datetime.fromtimestamp(os.path.getmtime(filename)).strftime('%d %b %Y')
  if title is None:
    title = filename[:filename.find('.')].replace('_', ' ').title()

  # reorder data
  df = pd.read_csv(filename)
  df['new_order'] = - abs(-0.25 + 0.5 * len(df) - df.index.to_numpy())
  df = df.set_index('key_word')
  df = df.sort_values('new_order')
  df['unanswered_rate'] = df['unanswered_question'] / df['question']
  df = df.drop(['new_order', 'unanswered_question'], axis=1)

  # check annotation_angle_adjustments key validity
  errors = {'columns' : [e for e in annotation_angle_adjustments if e not in df.columns], 
            'rows' : [k for v in annotation_angle_adjustments.values() for k in v.keys() if k not in df.index.values]}
  assert not errors['columns'] and not errors['rows'], f"Errors in ang_mult_dicts: {errors}"
  assert len(df.index.values) <= len(my_color_palette), \
         f"{len(df.index.values)} colors are required but only defined {len(my_color_palette)} colors are defined"

  # plot
  for col_name in df.columns:
    if col_name == 'unanswered_rate':
      continue
    ang_mult_dict = annotation_angle_adjustments.get(col_name, {})
  
    plot = df.plot.pie(y=col_name, figsize=(fig_width[col_name], fig_height), startangle=start_angles.get(col_name, 0),
                       colors=my_color_palette.values(),
                       labels=[''] * len(df.index))
    wedges = [w for w in plot.get_children() if type(w) is mpatches.Wedge]

    # add a black pie chart
    if col_name.lower() == 'question':
      df.plot.pie(y=col_name, startangle=start_angles.get(col_name, 0),
                  colors=['black']*len(df.index), wedgeprops={'width':0.3}, 
                  labels=['']*len(df.index), ax=plot)
      black_wedges = [w for w in plot.get_children() if (type(w) is mpatches.Wedge) and w not in wedges]
      for how_many_unanswered, w in zip(df['unanswered_rate'], black_wedges):
        w.set_width(w.r*how_many_unanswered)
    
    # title and legend
    plot.set_title(f"Stackoverflow {title} {col_name.upper()} Count\nas of {last_modif_date}")
    plot.yaxis.label.set_visible(False)
    plot.get_legend().remove()

    # add annotations
    for label_, how_many, p in zip(df.index, df[col_name], wedges):
      mult_ang = ang_mult_dict[label_] if label_ in ang_mult_dict else 0.5
      ang = (p.theta2 - p.theta1)*mult_ang + p.theta1
      ang2 = np.deg2rad(ang)
      y = np.sin(ang2)
      x = np.cos(ang2)
      kw["arrowprops"]["connectionstyle"] =  f"angle,angleA=0,angleB={ang}"
      ann = f'{label_}\n'
      if col_name.lower() == 'question':
        ann += f'{how_many:,} questions, {int(100*df.loc[label_, "unanswered_rate"])}% unanswered'
      else:
        ann += f'viewed {how_many:,} times'
      plot.annotate(ann, xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y), horizontalalignment="left" if x >= 0 else "right", **kw)

    # save as a file
    plt.savefig(f'{filename[:filename.find(".")]}_{col_name}.{image_extension}', dpi=300)
    