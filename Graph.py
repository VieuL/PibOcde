import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff


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

    def get_list_dates_q(self, start, end):
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
                'text': title,
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            hovermode="x unified"
        )

    def correlation(self, dates, countries=[], frequency='Q', measure='PC_CHGPY'):
        corrMatrix = []
        country_corr = []

        for country in countries:
            country_corr = []
            ref_country = self.filter_df([country], frequency, 'TOT', measure, dates)['Value'].to_numpy()

            for c in countries:
                c_df = self.filter_df([c], frequency, 'TOT', measure, dates)['Value'].to_numpy()
                corr = np.corrcoef(ref_country, c_df)

                country_corr.append(np.abs(np.round(corr[0, 1], 3)))

            corrMatrix.append(country_corr)

        return corrMatrix


    def display_correlation_heatmap(self, dates, countries=[]):
        countries_title = ""
        for country in countries:
            countries_title += country + ", "

        corrMatrix = self.correlation(dates, countries)

        fig = ff.create_annotated_heatmap(corrMatrix[::-1],
            x=countries,
            y=countries[::-1],
            colorscale='YlGnBu'
        )

        fig.update_layout(title_text="Corrélation entre le PIB de "+countries_title[:len(countries_title)-2])

        fig.show()


    def display_correlation_line(self, dates, countries=[]):
        corrMatrix = list()
        pd_dates = list()

        for i in range(8, len(dates), 8):
            temp_dates=dates[i-8:i]  
            pd_dates.append("-".join([temp_dates[0].split('-')[0], temp_dates[::-1][0].split('-')[0]]))

            corr = self.correlation(temp_dates, countries, frequency='Q', measure='PC_CHGPP')
            corrMatrix.append(corr[0][1])

        pd_corr = pd.DataFrame(list(zip(["-".join(countries)]*len(corrMatrix), pd_dates, corrMatrix)), columns=['LOCATION', 'TIME', 'Value'])

        return pd_corr

    def display(self):
        self.fig.show()
