import nest
import numpy as np
import pickle
nest.ResetKernel()

nrowE, ncolE = 12, 12      # Must be square and same as [Insert Max code]
nrowI, ncolI = 6, 6
npopE =  nrowE * ncolE
npopI = nrowI * ncolI

# Rate of Poisson generator
rate = 5000.

# Parameters of our neurons.
neuron_params = {'V_th': -54., 'V_reset': -70., 't_ref': 2., 'g_L': 12.5, 'C_m': 250.0, 'E_ex': 0.0,
                         'E_in': -80.0,
                         'tau_syn_ex': 0.3, 'tau_syn_in': 1.0, 'E_L': -70.}

syn_param_exc = {'weight': 2., 'delay': 1.0}
syn_param_inh = {'weight': -2., 'delay': 1.0}

# Create the synapse model with the above synapse parameters
nest.CopyModel("static_synapse", "syn_exc", syn_param_exc)
nest.CopyModel("static_synapse", "syn_inh", syn_param_inh)

# Create the neurons
nodes_ex = nest.Create('iaf_cond_exp', npopE, neuron_params)
nodes_in = nest.Create('iaf_cond_exp', npopI, neuron_params)

# Create poisson generator
poiE = nest.Create('poisson_generator', 1, {'rate': rate})

# Connect poisson noise to all neurons
nest.Connect(poiE, nodes_ex, syn_spec={'model': 'syn_exc'})
nest.Connect(poiE, nodes_in, syn_spec={'model': 'syn_exc'})

# Create one spike detector per neuron
sd = nest.Create('spike_detector', npopE + npopI)

#--------------------------------------------------------------------------------------------------------------------
# Input from {Insert Max code} is on the form [conmatEE, conmatEI, conmatIE, conmatII]
# where the connection matrix's are on the form
# [['targets for neuron 0'], ... , ['targets for neuron j], ... , ['targets for neuron npop']]
# (that is, npop arrays in an array)


with open("connections.p", 'rb') as f:
    targets = pickle.load(f)

targetsEE = targets[0]
targetsEI = targets[1]
targetsIE = targets[2]
targetsII = targets[3]

# Make EE and EI connections
for n in range(npopE):
    neuron = (n+1,)
    nest.Connect(neuron, targetsEE[n], syn_spec={'model': 'syn_exc'})  # Add 1 to shift indices
    nest.Connect(neuron, targetsEI[n], syn_spec={'model': 'syn_exc'})  # Add npopE to shift targets to inhibitory neurons
    # nest.Connect(sd[n:n+1], )

# Make IE and II connections
for n in range(npopI):
    neuron = (n + 1 + npopE,)
    nest.Connect(neuron, targetsIE[n], syn_spec={'model': 'syn_inh'})
    nest.Connect(neuron, targetsII[n], syn_spec={'model': 'syn_inh'})


simtime = 1000





