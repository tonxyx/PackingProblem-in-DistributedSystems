# First-fit algoritam - Rjesavanje problema pakiranja u DOTA 2

"""
Testiranje: mpirun -np 5 python3 firstFit.py
"""

import time
import numpy as np
import binModule
import os
from binModule import Bin
from binModule import Item
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def firstFit():
    """
    Funkcija racuna koliko je spremnika kapaciteta 5 igraca potrebno za smjestanje odredenih grupa od 1 do 5 igraca. 
    Dvije klase bin(spremnici) te item(grupe) sadrze odredene podatke koji se obraduju kroz algoritam pa se tako dolazi
    do informacija o vremenu cekanja svake od grupa, o broju iskoristenih spremnika te broju popunjenih spremnika(broj igara).

    Argumenti:
    /

    Vraca:
    Broj popunjenih spremnika, iskoristenih spremnika te prosjecno vrijeme cekanja grupe igraca.
    """

    binFull = 0
    waitTime = 0
    waitSum = 0
    for item in items:
        for xBin in bins:
            if xBin.capacity - sum(xBin.contents) >= item.value:
                xBin.add(item.value)
                item.startTime = time.time()
                item.binId = xBin.binId
                if xBin.capacity - sum(xBin.contents) == 0:
                    for x in range(0, len(items)):
                        if items[x].binId == xBin.binId:
                            items[x].exeTime = time.time() - items[x].startTime
                            waitTime += items[x].exeTime
                            waitSum += 1
                    binFull += 1
                break
            if bins.index(xBin) == len(bins) - 1:
                bins.append(Bin(bins.index(xBin)+1, cap, []))
        if item.exeTime == 0:
            binUsed = item.binId+1
    return [binFull, binUsed, waitTime/waitSum]

# Kapacitet spremnika
cap = 5

# Broj elemenata
n_elem = 10000

if rank == 0:
    #Proces ranga 0 brise datoteke kako bi bile prazne
    try:
        with open('results.txt'):
            os.remove('results.txt')
    except IOError:
        print('Creating results.txt for data input.')

    try:
        with open('statistics.txt'):
            os.remove('statistics.txt')
    except IOError:
        print('Creating statistics.txt for data input.')

    #Random generirani elementi u procesu 0
    items = []
    for i in range(0,n_elem):
        items.append(Item(i, np.random.randint(1,5), 0, -1, 0))
   
    #Polje parts dodjeljuje svakom od procesa element u rasponu od size
    parts = [[] for _ in range(size)]
    for i, part in enumerate(items):
        parts[i % size].append(Item(part.itemId, part.value, 0, -1, 0))
else:
    items = None
    parts = None

#scatter potrebnih elemenata za svaki od procesa
items = comm.scatter(parts, root=0)

#inicijalizacija spremnika za svaki od procesa
bins=[]
bins.append(Bin(0, cap, [])) # moramo instancirati jedan spremnik kako bi mogli poceti

#Pocetak obrade na svakom od procesa
timeStart = time.time()

#Izvodenje first fit algoritma 
result = firstFit()

#Krajnje vrijeme izvodenja
timeEnd = time.time()

#Datoteka sa statistikama
b = open('statistics.txt', 'a')

b.write('Rank: ' + repr(rank) + '\t\t Bins used: ' + repr(result[1]) + '\t Bin full: ' + repr(result[0]) + '\t Execution time: ' + repr(timeEnd-timeStart) + ' sec\t Avg waiting time: ' + repr(result[2]) + ' sec \n\n\n')

#Datoteka sa rezultatima
f = open('results.txt', 'a')

for i in range(0, int(n_elem/size)):
    f.write('Rank: ' + repr(rank) + '\t\t Item id: ' + repr(items[i].itemId) + '\t Item value: ' + repr(items[i].value) + '\t Bin id: ' + repr(items[i].binId) + '\t Execution time: ' + repr(items[i].exeTime) + ' sec \n')

b.close()
f.close()
