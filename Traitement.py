# Fonction pour le calule des moyennes mob
import pandas as pd
import matplotlib.pyplot  as plt
import numpy as np
from Graph import Graph

def mobilMoy(data, fenetre):
    '''
    Cette fonction calcule les moyennes et les variances mobile.
    :param data: Dataframe, Le data frame doit sortir de la fonction traitementParPays()
    :param fenetre: Taille de la fenetre pour le calcule
    :return: Deux liste constituée de index de la données et du calcule, [[index dans DataFrame, moyenne/var], ...]
    '''

    valM = []
    valV = []
    longeur = len(data.index)
    if fenetre % 2 == 0:
        # Si nous sommes dans le cas paire
        for µ in range(longeur):
            # Parcour des données, nous ne gardons pas les premières données ni les dernières
            if µ > (fenetre // 2) - 1 and µ < (longeur - ((fenetre // 2))):
                inter = [data.iloc[µ]['Value']]
                # dans le cas paire il y a un traitement spé pour les données à l'extrémité
                extrem = (data.iloc[µ - (fenetre // 2)]['Value'] + data.iloc[µ + (fenetre // 2)]['Value'])
                # print(str(µ) + " et " + str(µ - (fenetre//2)) + " et " + str(µ + (fenetre//2)))
                inter.append(extrem / 2)
                for i in range((fenetre // 2) - 1):
                    # print(str(µ - (i+1)) + " et " + str(µ + (i+1)) + " pour " + str(µ))
                    inter.append(data.iloc[µ - (i + 1)]['Value'])
                    inter.append(data.iloc[µ + (i + 1)]['Value'])
                valM.append(['moyenne mobille ' + str(fenetre), data.iloc[µ]['TIME'], np.mean(inter)])
                valV.append(['moyenne-mobille ' + str(fenetre), data.iloc[µ]['TIME'], np.var(inter)])
                    # print('\n')

    else:
        # Si nous sommes dans le cas impaire
        for µ in range(longeur):
            if µ > (fenetre // 2) - 1 and µ < (longeur - ((fenetre // 2))):
                inter = [data.iloc[µ]['Value']]
                for i in range(fenetre // 2):
                    # print(str(µ - (i+1)) + " et " + str(µ + (i+1)) + " pour " + str(µ))
                    inter.append(data.iloc[µ - (i + 1)]['Value'])
                    inter.append(data.iloc[µ + (i + 1)]['Value'])
                    # data.iloc[µ].name
                valM.append(['moyenne-mobille '+ str(fenetre),  data.iloc[µ]['TIME'], np.mean(inter)])
                valV.append(['moyenne-mobille '+ str(fenetre),  data.iloc[µ]['TIME'], np.var(inter)])
    return valM, valV



def traitementParPays(data, F):
    med = data[data['FREQUENCY'] == F]
    chgpy =  med[med['MEASURE'] == 'PC_CHGPY']
    chgpp = med[med['MEASURE'] == 'PC_CHGPP']
    indice = med[med['MEASURE'] == 'IDX']
    return chgpy, chgpp, indice


def saisonier(data):
    gpy, gppQ, ind = traitementParPays(data, 'Q')
    dataQ1 = []
    dataQ2 = []
    dataQ3 = []
    dataQ4 = []
    for µ in range(len(gppQ)):
        if 'Q1' in gppQ.iloc[µ]['TIME']:
            dataQ1.append([gppQ.iloc[µ]['TIME'].split('-')[0], gppQ.iloc[µ]['Value']])
        elif 'Q2' in gppQ.iloc[µ]['TIME']:
            dataQ2.append([gppQ.iloc[µ]['TIME'].split('-')[0], gppQ.iloc[µ]['Value']])
        elif 'Q3' in gppQ.iloc[µ]['TIME']:
            dataQ3.append([gppQ.iloc[µ]['TIME'].split('-')[0], gppQ.iloc[µ]['Value']])
        elif 'Q4' in gppQ.iloc[µ]['TIME']:
            dataQ4.append([gppQ.iloc[µ]['TIME'].split('-')[0], gppQ.iloc[µ]['Value']])
    # %%
    dataQ1 = pd.DataFrame(dataQ1, columns=['Annee', 'ValeurQ1'])
    dataQ2 = pd.DataFrame(dataQ2, columns=['Annee', 'ValeurQ2'])
    dataQ3 = pd.DataFrame(dataQ3, columns=['Annee', 'ValeurQ3'])
    dataQ4 = pd.DataFrame(dataQ4, columns=['Annee', 'ValeurQ4'])

    dataTrim = pd.merge(dataQ1, dataQ2)
    dataTrim = pd.merge(dataTrim, dataQ3)
    dataTrim = pd.merge(dataTrim, dataQ4)

    return dataTrim

def affichageMoyenneM(data, country, ordre, per):
    g = Graph(data)

    if per == 'A':
        lDate = []
        for µ in range(1961, 2021):
            lDate.append(str(µ))
        # gpy, gpp, ind = tr.traitementParPays(dataFR, 'A')
        gpp = g.filter_df([country],'A','TOT','PC_CHGPP',lDate)
        data = pd.DataFrame(columns=['LOCATION', 'TIME', 'Value'])
        for µ in ordre:
            moy = pd.DataFrame(mobilMoy(gpp,µ)[0],columns=['LOCATION','TIME','Value'])
            data = pd.concat([data,moy])
        g.line_graph(pd.concat([data,gpp]), x='TIME', y='Value', x_label="Trimestre", y_label="Evolution du PIB (%)",
                     title='Evolution du PIB au cours du temps')  # Création des courbes
        g.display()

    if per == 'Q':
        lDate = g.get_list_dates_q(1961,2021)
        gpp = g.filter_df([country],'Q','TOT','PC_CHGPP',lDate)
        r = gpp
        data = pd.DataFrame(columns=['LOCATION', 'TIME', 'Value'])
        for µ in ordre:
            moy = pd.DataFrame(mobilMoy(gpp,µ)[0],columns=['LOCATION','TIME','Value'])
            data = pd.concat([data,moy])
        g.line_graph(pd.concat([r,data]), x='TIME', y='Value', x_label="Trimestre", y_label="Evoltion du PIB (%)",
                     title='Evolution du pib au cours du temps')  # Création des courbes
        g.display()


        