import numpy as np
import pandas as pd
import plotly.express as px

class Graph:
    def __init__(self, df):
        self.df = df
        self.fig = None

    def filter_df(self, location, frequency, subject, measure, time=[]):
        df = self.df
        df = df[df['LOCATION'].isin(location)]
        df = df[df['FREQUENCY'] == frequency]
        df = df[df['SUBJECT'] == subject]
        df = df[df['MEASURE'] == measure]

        if time:
            df = df[df['TIME'].isin(time)]
        return df

    def get_list_dates(self, start, end):
        list_time = list()
        for t in range(start, end):
            for q in range(1, 5):
                list_time.append(str(t)+"-Q"+str(q))
        return list_time

    def line_graph(self, df, x, y, x_label='', y_label='', title='', color='LOCATION', legend_title='Pays', height=400, width=1500):
        self.fig = px.line(df, x=x, y=y, color=color, height=height, width=width)
        self.fig.update_traces(mode="lines", hovertemplate=None)
        self.fig.update_layout(
            xaxis_title=x_label,
            yaxis_title=y_label,
            legend_title=legend_title,
            title = {
                'text': "Evolution du PIB",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            hovermode="x unified"
            )

    def display(self):
        self.fig.show()
