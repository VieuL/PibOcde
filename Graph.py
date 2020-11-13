import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, df):
        self.df = df
        self.legend = []
        self.fig, self.ax = plt.subplots(figsize=(30,5))

    def filter_df(self, location, frequency, subject, measure, time=[]):
        df = self.df
        df = df[df['LOCATION'] == location]
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

    def get_df_dates(self, df):
        dates = list()
        for index, row in df.iterrows():
            dates.append(row['TIME'])
        return dates

    def plot_graph(self, df, color):
        values = list()
        self.legend.append(df.iloc[0]['LOCATION'])

        for index, row in df.iterrows():
            values.append(row['Value'])

        self.ax.plot(range(len(df)), values, color = color)

    def define_xticks2(self, labels, nbins):

        final_labels = list()
        inter = len(labels)%nbins
        print(inter)
        for label in labels:
            if labels.index(label)%inter == 0:
                final_labels.append(label)
        return final_labels

    def define_xticks(self, labels, nbins):
        final_labels = list()
        indexes = np.arange(0, len(labels), nbins)
        for index in indexes:
            final_labels.append(labels[index])

        return final_labels


    def display(self, dates, nbins):
        plt.xlabel("Trimestre")
        plt.ylabel("Croissance du PIB (%)")
        ticks = self.define_xticks(dates, nbins)
        plt.locator_params(axis='x', nbins=nbins)
        plt.xticks(np.arange(len(ticks)), ticks, rotation='vertical')
        plt.legend(self.legend)

        plt.show()