# -*- coding: utf-8 -*-
#
# connection_matrix.py
#
# Copyright 2017 Sebastian Spreizer
# The MIT License


import numpy as np

import lcrn_network as lcrn

#def I_networks(landscape, nrow, ncol, ncon, kappa, theta, seed=0, **kwargs):
#    np.random.seed(seed)
#
#    npop = nrow * ncol
#   landscape_mode = landscape['mode']
#
#    conmat = []
#    for ii in range(npop):
#        targets, delay = lcrn.lcrn_gamma_targets(
#            ii, nrow, ncol, nrow, ncol, ncon, kappa, theta)
#        targets = targets[targets != ii]            # no selfconnections
#        hist_targets = np.histogram(targets, bins=range(npop + 1))[0]
#        conmat.append(hist_targets)
#
#    return np.array(conmat)


def EI_networks(nrowE, ncolE, nrowI, ncolI, p, stdE, stdI, seed=0, **kwargs):
    np.random.seed(seed)
    npopE = nrowE * ncolE
    npopI = nrowI * ncolI

    conmatEE, conmatEI = [], []
    for idx in range(npopE):
        # E-> E
        numberOfConnections = np.random.binomial(npopE,p)  #Binomial distribution of number of connections.
        source = idx, nrowE, ncolE, nrowE, ncolE, numberOfConnections, stdE
        targets, delay = lcrn.lcrn_skewed_gauss(*source)
        targets = targets[targets != idx]           # no selfconnections
        targets += 1
        conmatEE.append(targets)

        # E-> I
        source = idx, nrowE, ncolE, nrowI, ncolI, int(p * npopI), stdI
        targets, delay = lcrn.lcrn_gauss_targets(*source)
        targets += (1 + npopE)
        conmatEI.append(targets)

    conmatIE, conmatII = [], []
    for idx in range(npopI):

        # I-> E
        source = idx, nrowI, ncolI, nrowE, ncolE, int(p * npopE), stdE
        targets, delay = lcrn.lcrn_gauss_targets(*source)
        targets += 1
        conmatIE.append(targets)

        # I-> I
        source = idx, nrowI, ncolI, nrowI, ncolI, int(p * npopI), stdI
        targets, delay = lcrn.lcrn_gauss_targets(*source)
        targets += (1 + npopE)
        conmatII.append(targets)

    return np.array(conmatEE), np.array(conmatEI), np.array(conmatIE), np.array(conmatII)
