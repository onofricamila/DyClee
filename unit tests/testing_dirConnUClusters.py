#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from testing_uClusters import uC1, uC2, uC3, uC4, uC5, uC6, uC8, uC10, uC11, uC12

# TEST 1°: uC2 llega a ser directly conn con uC1
print('Debe dar True: ', uC1.isDirectlyConnectedWith(uC2, 0)) # --> true

# TEST 2°: uC3 por 1 en ambas dimensiones llega a ser directly conn con uC1
print('Debe dar True: ', uC1.isDirectlyConnectedWith(uC3, 0)) # --> true

# TEST 3°: uC4 por 1 en ambas dimensiones no llega a ser directly conn con uC1
print('Debe dar False: ', uC1.isDirectlyConnectedWith(uC4, 0)) # --> false

# TEST 4°: uC5 es re lejano a uC1
print('Debe dar False: ', uC1.isDirectlyConnectedWith(uC5, 0)) # --> false

# TEST 4°: uC6 no llega a ser directly conn con uC1 por lo que vale la dim 2
print('Debe dar False: ', uC1.isDirectlyConnectedWith(uC6, 0)) # --> false

# TEST 5°: uC8 y uC10 estan directamente conectados
print('Debe dar True: ', uC10.isDirectlyConnectedWith(uC8, 0)) # --> true

print('\n')
      
# TEST 6°: uC11 y uC12 estan directamente conectados
print('Debe dar False: ', uC11.isDirectlyConnectedWith(uC12, 0)) # --> false