__author__ = 'tonycastronova'




import plotly.plotly as py
from plotly.graph_objs import *

# Fill in with your personal username and API key
# or, use this public demo account
py.sign_in('Python-Demo-Account', 'gwt101uhh0')

trace1 = Scatter(
    x=[1, 2, 3, 4],
    y=[10, 15, 13, 17]
)
trace2 = Scatter(
    x=[1, 2, 3, 4],
    y=[16, 5, 11, 9]
)
data = Data([trace1, trace2])

plot_url = py.plot(data, filename='basic-line')