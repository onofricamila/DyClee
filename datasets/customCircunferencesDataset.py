#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 19:09:14 2019

@author: camila
"""
from math import pi, cos, sin, radians
import random


# la idea es agarrar un angulo y usar la interpretación geométrica de la 
# circunferencia junto con trigonometria para asi formar un punto en ella 
def point(centro_x, centro_y, radio, maxRadioInc, theta):
    # agrando o no un toque el radio
    r = radio + random.uniform(0, maxRadioInc)
    # cos(theta) * r es la diferencia entre el x del punto y el del centro 
    # sin(theta) * r es la diferencia entre el y del punto y el del centro 
    return [centro_x + cos(theta) * r, centro_y + sin(theta) * r]



def generatePoints(centro_x, centro_y, radio, maxRadioInc):
    # listas de puntos
    puntosArriba = []
    puntosAbajo = []
    puntosCentro = []
    # batch representa la cantidad de puntos a generar por lista cuando estamos en cierto angulo
    # vamos a tener 180 * batch puntos totales en cada lista
    batch = 3
    # theta es el angulo respecto de x en el que rotaremos alrededor del centro
    for theta in range(0, 180):
        for i in range(0, batch):
          # en los puntos de arriba avanzo de derecha a izquierda (de 0° a 180°)
          puntosArriba.append(point(centro_x, centro_y, radio, maxRadioInc, radians(theta)))
          # en los puntos de abajo avanzo de izquierda a derecha (de 180° a 360°)
          puntosAbajo.append(point(centro_x, centro_y, radio, maxRadioInc, pi + radians(theta)))
          # para los puntos del centro considero una porción pequeña del radio original
          puntosCentro.append(point(centro_x, centro_y, 0.5/100 * radio, maxRadioInc, radians(theta)))
    return puntosArriba, puntosCentro, puntosAbajo



def generateDataset():
    # propiedades de la circunferencia
    centro_x = 0
    centro_y = 0
    radio = 5
    maxRadioInc = 0.25
    puntosArriba, puntosCentro, puntosAbajo = generatePoints(centro_x, centro_y, radio, maxRadioInc)
    # para tratar los lotes de puntos
    batchUpperLimit = 0
    batchLowerLimit = 0
    limIterator = len(puntosArriba)
    res = []
    for i in range(0, limIterator):
        # incremento el limite superior del lote de puntos a mostrar
        batchUpperLimit += 10
        # pongo puntos de cada grupo
        res = res + puntosArriba[batchLowerLimit:batchUpperLimit] + puntosCentro[batchLowerLimit:batchUpperLimit] + puntosAbajo[batchLowerLimit:batchUpperLimit]
        batchLowerLimit = batchUpperLimit
    return res



customCircunferencesDataset = generateDataset()
