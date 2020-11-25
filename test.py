import pandas as pd
import matplotlib.pyplot  as plt
import numpy as np
import Traitement as tr
import os
from pandas.plotting import lag_plot
from pandas.plotting import autocorrelation_plot

data = pd.read_csv('data.csv', sep=';')

from Graph import Graph
g = Graph(data)

g.heatmap()