# -*- coding: utf-8 -*-
#
# lcrn_network.py
#
# Copyright 2017 Arvind Kumar, Sebastian Spreizer
# The MIT License

import numpy as np
import noise

__all__ = [
    'lcrn_skewed_gauss'
    'lcrn_gauss_targets',
    'lcrn_gamma_targets',
    'plot_targets',
]

def lcrn_skewed_gauss(s_id, srow, scol, trow, tcol, ncon, con_std):
    grid_scale = float(trow)/float(srow)
    s_x = np.remainder(s_id, scol)  # column id
    s_y = int(s_id) / int(scol)  # row id
    s_x1 = s_x * grid_scale  # column id in the new grid
    s_y1 = s_y * grid_scale  # row_id in the new grid

    # pick up ncol values for phi and radius
    tilesinrow = 4;
    phi = perlin_phi(s_x1, s_y1, trow, tilesinrow, ncon)
    radius = np.random.normal(0,con_std,size = ncon)
    # print("phi")
    # print(phi)
    # print("numberOFConnections")
    # print(ncon)
    # print("")

    t_x = np.remainder(np.round(radius * np.cos(phi) + s_x1), tcol)
    t_y = np.remainder(np.round(radius * np.sin(phi) + s_y1), trow)
    target_ids  = t_y * tcol + t_x

    target = np.array(target_ids).astype('int')
    delays = np.abs(radius) / tcol        #Do we model as square matrix?
    return target, delays

def perlin_phi(x,y,trow, size, ncon):
    scale = trow/size
    scaled_x = float(x)/float(scale)
    scaled_y = float(y)/float(scale)
    mean = noise.pnoise2(scaled_x, scaled_y, repeatx = size, repeaty = size)
    return np.random.normal(mean, np.pi / 2, size = ncon)



def lcrn_gauss_targets(s_id, srow, scol, trow, tcol, ncon, con_std):
    grid_scale = float(trow) / float(srow)
    s_x = np.remainder(s_id, scol)  # column id
    s_y = int(s_id) / int(scol)  # row id
    s_x1 = s_x * grid_scale  # column id in the new grid
    s_y1 = s_y * grid_scale  # row_id in the new grid

    # pick up ncol values for phi and radius
    phi = np.random.uniform(low=-np.pi, high=np.pi, size=ncon)
    radius = con_std * np.random.randn(ncon)

    #t_x = np.remainder(radius * np.cos(phi) + s_x1, tcol)
    #t_y = np.remainder(radius * np.sin(phi) + s_y1, trow)  #If tcol = 10 and t_x = 9.9 target_id is misplaced.
    #target_ids = np.remainder(
    #    np.round(t_y) * tcol + np.round(t_x), trow * tcol)

    t_x = np.remainder(np.round(radius * np.cos(phi) + s_x1), tcol)
    t_y = np.remainder(np.round(radius * np.sin(phi) + s_y1), trow)
    target_ids  = t_y * tcol + t_x

    target = np.array(target_ids).astype('int')
    delays = np.abs(radius) / tcol        #Do we model as square matrix?
    return target, delays


def lcrn_gamma_targets(s_id, srow, scol, trow, tcol, ncon, k=2, theta=1, shift=1):
    grid_scale = float(trow) / float(srow)
    s_x = np.remainder(s_id, scol)  # column id
    s_y = int(s_id) / int(scol)  # row id
    s_x1 = s_x * grid_scale  # column id in the new grid
    s_y1 = s_y * grid_scale  # row_id in the new grid

    # pick up ncol values for phi and radius
    phi = np.random.uniform(low=-np.pi, high=np.pi, size=ncon)
    radius = np.concatenate(
        (-np.random.gamma(k, theta, ncon / 2), np.random.gamma(k, theta, ncon / 2)))
    radius[radius > 0] = radius[radius > 0] + shift + .1
    radius[radius < 0] = radius[radius < 0] - shift - .1
    t_x = np.remainder(radius * np.cos(phi) + s_x1, tcol)
    t_y = np.remainder(radius * np.sin(phi) + s_y1, trow)
    target_ids = np.remainder(
        np.round(t_y) * tcol + np.round(t_x), trow * tcol)
    target = np.array(target_ids).astype('int')
    delays = np.abs(radius) / tcol
    return target, delays


def plot_targets(popE, popI, nrowE, ncolE, nrowI, ncolI):
    centerE = (nrowE * (ncolE + 1)) / 2
    centerI = (nrowI * (ncolI + 1)) / 2

    offsetE = popE[0]
    offsetI = popI[0]

    tEE = np.array(nest.GetStatus(nest.GetConnections(
        [centerE + offsetE], popE), 'target')) - offsetE
    tEI = np.array(nest.GetStatus(nest.GetConnections(
        [centerE + offsetE], popI), 'target')) - offsetI
    tIE = np.array(nest.GetStatus(nest.GetConnections(
        [centerI + offsetI], popE), 'target')) - offsetE
    tII = np.array(nest.GetStatus(nest.GetConnections(
        [centerI + offsetI], popI), 'target')) - offsetI

    fig, ax = pl.subplots(2, 2, sharex=True, sharey=True)
    ax = np.ravel(ax)
    ax[0].plot(tEE % nrowE, tEE // ncolE, '.', markersize=8)
    ax[1].plot((tEI % nrowI) * 2, (tEI // ncolI) * 2, '.', markersize=8)
    ax[2].plot(tIE % nrowE, tIE // ncolE, '.', markersize=8)
    ax[3].plot((tII % nrowI) * 2, (tII // ncolI) * 2, '.', markersize=8)

    pl.show()
