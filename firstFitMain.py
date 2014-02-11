# First-fit algoritam - Rjesavanje problema pakiranja

# Needed DS implementation and testing modlules (python3 print in ())

import math
import sys
import time
import numpy as np
import binModule
from binModule import Bin
from binModule import Item

print "\n\n"

# Korisnik unosi kapacitet spremnika
cap = 5

# Korisnik unosi elemente
#items = binModule.getItems()
items = []

for i in range(0,1000):
    items.append(Item(i, np.random.randint(1,5), 0, -1, 0))

maxBins = len(items)
#minBins = int(math.ceil(sum(items)/cap))
bins = []

print "Vasi elementi su:", items, "\nVasi spremnici imaju kapacitet ", cap, "\n"

bins.append(Bin(0, cap, [])) # moramo instancirati jedan spremnik kako bi mogli poceti

for item in items:
    # Dodavanje elemenata u prvi spremnik koji ih moze primiti
    # Ukoliko ih niti jedan spremnik ne moze prihvatiti, napravi novi spremnik
    if item.value > cap:
        print "Neki od elemenata ne mogu se staviti u niti jedan od spremnika. PREKID!"
        sys.exit()
    for xBin in bins:
        if xBin.capacity - sum(xBin.contents) >= item.value:
            xBin.add(item.value)
            item.startTime = time.time()
            item.binId = xBin.binId
            if xBin.capacity -sum(xBin.contents) == 0:
                for i in range(0, item.itemId+1):
                    if items[i].binId == xBin.binId:
                        items[i].exeTime = time.time() - items[i].startTime 
            break
        if bins.index(xBin) == len(bins) - 1:
            bins.append(Bin(bins.index(xBin)+1, cap, []))

f = open('results.txt', 'w')        
for i in range(0,1000):
    f.write(repr(items[i].itemId) + ' - ' + repr(items[i].value) + ' - ' + repr(items[i].binId) + ' - ' + repr(items[i].startTime) + ' - ' + repr(items[i].exeTime) + ' \n')

print "First-fit algoritam za", items, "sa kapacitetom", cap, "koristio je", len(bins), "spremika"
print "Konfiguracija: ", bins

f.close()
