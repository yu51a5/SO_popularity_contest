from plot_pies import plot_pies

################################################################################################
# filename is the name of the file that contains data
# it has 4 columns: key_word, viewed, question, unanswered_question
# it can be generated with https://data.stackexchange.com/stackoverflow/query/1805161

# start_angles - the angle (degrees, between 0 and 360) at which to start the pie chart. 

# annotation_angle_adjustments is used to adjest the angle of annotations arrows.
# It's optional, only set it if you are unhappy with the angles.
# The values should be between 0.0 and 1.0.
# By default, it's set to 0.5. Values smaller than 0.5 will move it clockwise,
# and greater than 0.5 will move it counter-clockwise

################################################################################################
containers_params = dict(filename="Containers.csv", title="Python Containers",
                         start_angles={'question' : 15, 'viewed' : 10},
                         annotation_angle_adjustments={'question' : {'tuples' : 0.9, 'list' : 0.4}, 
                                                       'viewed' : {'tuples' : 0.9, 'list' : 0.2}})
matplotlib_params = dict(filename="Matplotlib.csv", title="Python Plotting",
                         start_angles={'question' : 240, 'viewed' : 30},
                         annotation_angle_adjustments={'viewed' : {'bokeh' : 1., 'plotly' : 0.65}})

plot_pies(**matplotlib_params)

print('all done!')
