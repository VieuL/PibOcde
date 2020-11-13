# Fonction pour le calule des moyennes mob
import pandas as pd
import matplotlib.pyplot  as plt
import numpy as np


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
                    valM.append([data.iloc[µ].name, np.mean(inter)])
                    valV.append([data.iloc[µ].name, np.var(inter)])
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
                valM.append([data.iloc[µ].name, np.mean(inter)])
                valV.append([data.iloc[µ].name, np.var(inter)])
    return valM, valV



def traitementParPays(data, F):
    med = data[data['FREQUENCY'] == F]
    chgpy =  med[med['MEASURE'] == 'PC_CHGPY']
    chgpp = med[med['MEASURE'] == 'PC_CHGPP']
    indice = med[med['MEASURE'] == 'IDX']
    return chgpy, chgpp, indice


