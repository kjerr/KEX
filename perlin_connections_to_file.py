import lib.connection_matrix as cm
import csv

nrowE, ncolE = 30, 30
nrowI, ncolI = 15, 15
p = 0.1                     # connection probability
stdE = 6                    # space constant for E targets
stdI = 3                    # space constant for I targets

connection_matrix = cm.EI_networks(nrowE, ncolE, nrowI, ncolI, p, stdE, stdI)

with open("cmPerlinTest.csv", "wb") as f:
    writer = csv.writer(f, delimiter='*')
    writer.writerows(connection_matrix)

