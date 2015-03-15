import json

from lib import tree as t
from lib import particle_filter as pf
	
if __name__ == '__main__':

	# Scholar system tree stored as JSON.
	tree = json.load(open("data/scholar_tree.json"))
	observations = json.load(open("data/observations.json"))

	# Arbitrary parameter vector to start experimenting
	theta = {
		"repeat": 0.05,
		"CP_to_CE1": 1,
		"CE1_to_CE2": 1,
		"CE2_to_CM1": 1,
		"CM1_to_CM2": 1,
		"CM2_to_6eme": 1,
		"6eme_to_5eme": 1,
		"5eme_to_4eme": 1,
		"4eme_to_3eme": 1,
		"3eme_to_2nde": 0.8,
		"3eme_to_CAP1": 0.2,
		"CAP1_to_CAP2": 0.2,
		"2nde_to_1ere": 1,
		"CAP2_to_Finish": 0.2,
		"1ere_to_Tale": 1,
		"Tale_to_Finish": 1
	}

	# filtered state after 3 years
	[filtered_state, log_likelihood] = pf.particle_filter(9, tree, theta, observations, 3)
	print log_likelihood
	# print filtered_state




