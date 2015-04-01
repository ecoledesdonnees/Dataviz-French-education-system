import copy
from scipy.stats import norm
from numpy.random import *

import numpy as np

import tree as t
import theta as th

def model_propagation(state, tree, theta): 
	# Randomly propagate the state of the system over 1 year, given theta

	next_state = {}

	# Loop over all the possible current trajectories of students
	for path_name in state:

		path = state[path_name]["path"]
		size = state[path_name]["size"]

		# Extract the descending tree
		subtree = copy.copy(t.extract_tree(copy.copy(path), tree))
		last_class = subtree["name"]

		# Handle students that repeat, drawing from a binomial
		repeat_path_name = path_name + '_' + last_class
		repeat_path = path + [subtree["name"]]

		p_repeat = th.get_p_repeat(theta, last_class)
		repeating_students = np.random.binomial(size, p_repeat)
		passing_students = size - repeating_students

		next_state[repeat_path_name] = {
			"size": repeating_students,
			"path": repeat_path
		}

		# Loop over potential classes students could go to
		if "leadsTo" in subtree:

			# Draw choices following a multinomial distribution
			pvals = []
			for option in subtree["leadsTo"]:
				transition_parameter_name = "%s_to_%s" %(last_class, option["name"])
				pvals.append(theta[transition_parameter_name]['value'])

			choices_draw = np.random.multinomial(passing_students, pvals)

			for ind_option, option in enumerate(subtree["leadsTo"]):
				option_path_name  = path_name + '_' + option["name"]
				option_path = path + [option["name"]]
				next_state[option_path_name] = {
					"size": choices_draw[ind_option],
					"path": option_path
				}

	return next_state

	
def from_state_to_observation(state, observation):
	matching_compartments = []
	for key, compartment in state.items():
		# print compartment["path"][-1], observation["level"]
		if compartment["path"][-1] in observation["level"]:
			matching_compartments.append(compartment)
	return np.sum(map(lambda x: x["size"], matching_compartments))

def resample(weights):
	# from http://wiki.scipy.org/Cookbook/ParticleFilter
	n = len(weights)
	indices = []
	C = [0.] + [sum(weights[:i+1]) for i in range(n)]
	u0, j = random(), 0
	for u in [(u0+i)/n for i in range(n)]:
		while u > C[j]:
			j+=1
			indices.append(j-1)
	return indices

def particle_filter(n, tree, theta, observations, n_particules):
	
	# Initialize state
	state_init = { 
		"CP": {
			"size": 600000,
			"path": ["CP"] 
		}
	}
	states = [ copy.copy(state_init) for i in range(n_particules)]

	observation_years = map(lambda x: x['year'], observations)

	log_likelihood = 0

	for i in range(n):

		# Propagate
		for j in range(n_particules):
			states[j] = model_propagation(states[j], tree, theta)

		# print "year %s entering:" %i
		# print list(set([compartment["path"][-1] for key, compartment in states[0].items()]))


		# Compute weights
		observations_this_year = filter(lambda x: i == x['year'], observations)
		# print observations_this_year
		log_weights = [0] * n_particules
		for observation in observations_this_year:
			for j in range(n_particules):
				# print from_state_to_observation(states[j], observation)
				log_weights[j] = np.log(norm.pdf(
					from_state_to_observation(states[j], observation), 
					observation["size"], 
					observation["size"]*0.1
				))
				log_likelihood += log_weights[j]

		# Resample
		weights = map(lambda x: np.exp(x), log_weights)
		weights /= np.sum(weights)
		indices = resample(weights)
		states = [ states[ind] for ind in indices ]

	return [states, log_likelihood]
