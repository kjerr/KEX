import pickle
import lib.connection_matrix as cm

nrowE, ncolE = 12, 12
nrowI, ncolI = 6, 6
p = 0.1                     # connection probability
stdE = 6                    # space constant for E targets
stdI = 3                    # space constant for I targets

connection_matrix = cm.EI_networks(nrowE, ncolE, nrowI, ncolI, p, stdE, stdI)

pickle.dump( connection_matrix, open( "connections.p", "wb" ) )