import nest
import numpy as np
import pickle
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import animation
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors
import csv

nest.ResetKernel()

nrowE, ncolE = 120, 120      # Must be square and same as [Insert Max code]
nrowI, ncolI = 60, 60
npopE = nrowE * ncolE
npopI = nrowI * ncolI

# Simulation time
simtime = 1000

# Rate of Poisson generator
rate = 6000.

# Parameters of neurons.
neuron_params = {'V_th': -54., 'V_reset': -70., 't_ref': 2., 'g_L': 12.5, 'C_m': 250.0, 'E_ex': 0.0,
                         'E_in': -80.0,
                         'tau_syn_ex': 0.3, 'tau_syn_in': 1.0, 'E_L': -70.}

# Synapse parameters
syn_param_exc = {'weight': 2., 'delay': 1.0}
syn_param_inh = {'weight': -2., 'delay': 1.0}

# Create the synapse model with the above synapse parameters
nest.CopyModel("static_synapse", "syn_exc", syn_param_exc)
nest.CopyModel("static_synapse", "syn_inh", syn_param_inh)

# Create the neurons
nodes_ex = nest.Create('iaf_cond_exp', npopE, neuron_params)  # Will have ID's 1 to npopE
nodes_in = nest.Create('iaf_cond_exp', npopI, neuron_params)  # Will have ID's from npopE+1 to npopE+npopI


# Create one spike detector per neuron
sd = nest.Create('spike_detector', npopE + npopI) # Will have ID's from npopE+npopI+1 to 2*(npopE+npopI)

# Create poisson generator
poiE = nest.Create('poisson_generator', 1, {'rate': rate})  # Will have ID 2*(npopE+npopI)+1


# Connect poisson noise to all neurons
nest.Connect(poiE, nodes_ex, syn_spec={'model': 'syn_exc'})
nest.Connect(poiE, nodes_in, syn_spec={'model': 'syn_exc'})

# # Check that ID's are correct
# print(nodes_ex)
# print(npopE)
# print(nodes_in)
# print(npopE+1)
# print(sd)
# print(poiE)
# print(2*(npopE+npopI)+1)


#--------------------------------------------------------------------------------------------------------------------
# Input from "perlin_connections_to_file.py" is on the form [conmatEE, conmatEI, conmatIE, conmatII]
# where the connection matrix's are on the form
# [['target ID's for neuron 1'], ... , ['target ID's for neuron j], ... , ['target ID's for neuron npop']]
# (that is, npop arrays in an array)


# # Load the generated targets from file
# with open("connections.p", 'rb') as f:
#     targets = pickle.load(f)
#
# targetsEE = targets[0]
# targetsEI = targets[1]
# targetsIE = targets[2]
# targetsII = targets[3]


targetsEE = []
targetsEI = []
targetsIE = []
targetsII = []
targets = [targetsEE, targetsEI, targetsIE, targetsII]

with open("cmPerlinE120I60.csv", "rb") as csvfile:
    reader = csv.reader(csvfile, delimiter='*')
    counter = 0
    for row in reader:
        for elem in row:
            noTargets = False
            outputList = elem[1:-1].split(",")
            if len(outputList) == 1 and outputList[0] == '':
                noTargets = True
            if not noTargets:
                outputList = map(int, outputList)
            else:
                outputList = []
            (targets[counter]).append(outputList)
        counter+=1


# Connect one spike detector to each node.
nest.Connect(nodes_ex + nodes_in, sd, 'one_to_one') # QUESTION

# Make EE and EI connections
for n in range(npopE):
    neuron = (n+1,)
    nest.Connect(neuron, tuple(targetsEE[n]), syn_spec={'model': 'syn_exc'})
    nest.Connect(neuron, tuple(targetsEI[n]), syn_spec={'model': 'syn_exc'})



# Make IE and II connections
for n in range(npopI):
    neuron = (n + 1 + npopE,)
    nest.Connect(neuron, tuple(targetsIE[n]), syn_spec={'model': 'syn_inh'})
    nest.Connect(neuron, tuple(targetsII[n]), syn_spec={'model': 'syn_inh'})


#----------------------------------------------------------------------------
# Start simulation
nest.Simulate(simtime)

# Create matrix counting how many times each neuron spikes
# spikesMatrixE = [[0 for x in range(ncolE)] for y in range(nrowE)]
# for n in range(npopE):
#     spikesMatrixE[np.remainder(n, ncolE)][int(n) / int(nrowE)] = len(nest.GetStatus(sd)[n]['events']['times'])

# Save the matrix as a file for plotting as colormesh later
#pickle.dump(spikesMatrixE, open( "Espikesmatrix.p", "wb" ))

# plt.pcolormesh(spikesMatrixE)
# plt.colorbar()
# plt.show()

frametime = 10
numberOfFrames = simtime / frametime
frameArray = [0 for x in range(numberOfFrames)]
for ind in range(len(frameArray)):
    frameArray[ind] = [[0 for x in range(ncolE)] for y in range(nrowE)]

for n in range(npopE):
    times = nest.GetStatus(sd)[n]['events']['times']
    for time in times:
        framenumber = int(time) / int(frametime)
        frameArray[framenumber][int(n) / int(nrowE)][np.remainder(n, ncolE)] += 1

with open("framesPerlinE120I60F100.csv", "wb") as f:
    writer = csv.writer(f, delimiter='*')
    writer.writerows(frameArray)








