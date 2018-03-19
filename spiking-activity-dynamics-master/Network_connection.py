import nest
import numpy as np
import pickle
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import animation
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors

nest.ResetKernel()

nrowE, ncolE = 12, 12      # Must be square and same as [Insert Max code]
nrowI, ncolI = 6, 6
npopE =  nrowE * ncolE
npopI = nrowI * ncolI

# Rate of Poisson generator
rate = 5000.

# Parameters of neurons.
neuron_params = {'V_th': -54., 'V_reset': -70., 't_ref': 2., 'g_L': 12.5, 'C_m': 250.0, 'E_ex': 0.0,
                         'E_in': -80.0,
                         'tau_syn_ex': 0.3, 'tau_syn_in': 1.0, 'E_L': -70.}

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


#--------------------------------------------------------------------------------------------------------------------
# Input from "perlin_connections_to_file.py" is on the form [conmatEE, conmatEI, conmatIE, conmatII]
# where the connection matrix's are on the form
# [['target ID's for neuron 1'], ... , ['target ID's for neuron j], ... , ['target ID's for neuron npop']]
# (that is, npop arrays in an array)


# Load the generated targets from file
with open("connections.p", 'rb') as f:
    targets = pickle.load(f)

targetsEE = targets[0]
targetsEI = targets[1]
targetsIE = targets[2]
targetsII = targets[3]


# Connect one spike detector to each node.
nest.Connect(nodes_ex + nodes_in, sd, 'one_to_one') # QUESTION

# Make EE and EI connections
for n in range(npopE):
    neuron = (n+1,)
    nest.Connect(neuron, targetsEE[n], syn_spec={'model': 'syn_exc'})
    nest.Connect(neuron, tuple(targetsEI[n]), syn_spec={'model': 'syn_exc'})


# Make IE and II connections
for n in range(npopI):
    neuron = (n + 1 + npopE,)
    nest.Connect(neuron, tuple(targetsIE[n]), syn_spec={'model': 'syn_inh'})
    nest.Connect(neuron, tuple(targetsII[n]), syn_spec={'model': 'syn_inh'})



simtime = 1000


nest.Simulate(simtime)
# print(sd)
# print(nest.GetStatus(sd)[0]['events']['times'])


# spikesMatrixE = [[0 for x in range(ncolE)] for y in range(nrowE)]
# for n in range(npopE):
#     spikesMatrixE[np.remainder(n, ncolE)][int(n) / int(nrowE)] = len(nest.GetStatus(sd)[n]['events']['times'])
#
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




# make animation

fig = plt.figure()
ax =  plt.axes(xlim=(0,ncolE), ylim=(0,nrowE))
ax.grid(True)
line, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    return line

def animate(i):
    frame = frameArray[i]
    output = plt.pcolormesh(frame, edgecolors = "#774387")
    return output

anim = animation.FuncAnimation(fig, animate, interval=100, frames=numberOfFrames)

plt.show()








