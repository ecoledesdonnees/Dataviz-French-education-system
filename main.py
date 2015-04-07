import json

from lib import tree as t
from lib import particle_filter as pf
from lib import dag
	
if __name__ == '__main__':

	# Building the orientation tree. 
	g = dag.get_graph("data/transitions.dat")
	# Write the corresponding JSON file.
	dag.write_orientation_tree(g,"CP","data/scholar_tree.json")

	# Scholar system tree stored as JSON.
	tree = json.load(open("data/scholar_tree.json"))
	observations = json.load(open("data/observations.json"))

	# Arbitrary parameter vector to start experimenting

	theta = {
		"repeat_primaire": { "value": 0.05, "fixed": False },
		"repeat_college": { "value": 0.05, "fixed": False },
		"repeat_2nde": { "value": 0.16, "fixed": True },
		"repeat_1ere": { "value": 0.15, "fixed": True },
		"repeat_Tale": { "value": 0.17, "fixed": True },
		"repeat_BEP": { "value": 0.05, "fixed": False },
		"repeat_CAP": { "value": 0.05, "fixed": False },

		"CP_to_CE1": { "value": 1, "fixed": True },

		"CE1_to_CE2": { "value": 1, "fixed": True },

		"CE2_to_CM1": { "value": 1, "fixed": True },

		"CM1_to_CM2": { "value": 1, "fixed": True },

		"CM2_to_6eme": { "value": 1, "fixed": True },

		"6eme_to_5eme": { "value": 1, "fixed": True },

		"5eme_to_4eme": { "value": 1, "fixed": True },

		"4eme_to_3eme": { "value": 1, "fixed": True },

		"3eme_to_2nde_GT": { "value": 0.54, "fixed": True },
		"3eme_to_2nde_Pro": { "value": 0.05, "fixed": True },
		"3eme_to_CAP1": { "value": 0.118, "fixed": True },
		"3eme_to_BEP1": { "value": 0.255, "fixed": True },
		"3eme_to_Drop": { "value": 0.018, "fixed": True },

		"BEP1_to_BEP2": { "value": 0.98, "fixed": False },
		"BEP1_to_Drop": { "value": 0.02, "fixed": False },

		"BEP2_to_got_BEP": { "value": 0.98, "fixed": False },
		"BEP2_to_1ere_Pro": { "value": 0.044, "fixed": True },
		"BEP2_to_Drop": { "value": 0.02, "fixed": False },

		"CAP1_to_CAP2": { "value": 1, "fixed": True },
		"CAP1_to_Drop": { "value": 0, "fixed": True },

		"CAP2_to_got_CAP": { "value": 1, "fixed": True },
		"CAP2_to_Drop": { "value": 0, "fixed": True },

		"2nde_Pro_to_1ere_Pro": { "value": 0.99, "fixed": True },
		"2nde_Pro_to_Drop": { "value": 0.01, "fixed": True },

		"2nde_GT_to_1ere_G": { "value": 0.515, "fixed": True },
		"2nde_GT_to_1ere_T": { "value": 0.259, "fixed": True },
		"2nde_GT_to_1ere_Pro": { "value": 0.065, "fixed": True },
		"2nde_GT_to_Drop": { "value": 0.01, "fixed": True },

		"1ere_G_to_Tale_G": { "value": 0.84, "fixed": True },
		"1ere_G_to_Drop": { "value": 0.01, "fixed": True },

		"1ere_T_to_Tale_T": { "value": 0.84, "fixed": True },
		"1ere_T_to_Drop": { "value": 0.01, "fixed": True },

		"1ere_Pro_to_Tale_Pro": { "value": 0.84, "fixed": True },
		"1ere_Pro_to_Drop": { "value": 0.01, "fixed": True },

		"Tale_G_to_got_BAC_G": { "value": 0.89, "fixed": True },
		"Tale_G_to_Drop": { "value": 0.05, "fixed": False },

		"Tale_T_to_got_BAC_T": { "value": 0.80, "fixed": True },
		"Tale_T_to_Drop": { "value": 0.05, "fixed": True },

		"Tale_Pro_to_got_BAC_Pro": { "value": 0.88, "fixed": True },
		"Tale_Pro_to_Drop": { "value": 0.05, "fixed": True }
	}
	
	# filtered state after 3 years
	[filtered_state, log_likelihood] = pf.particle_filter(12, tree, theta, observations, 3)

	# filtered_state = filtered_state[0].values()
	# filtered_state = filter(lambda traj: traj['size'] > 100, filtered_state)
	# filtered_state = sorted(filtered_state, key=lambda traj: traj['size'], reverse=False)
	# for traj in filtered_state:
	# 	print traj['path'], traj['size']

	print log_likelihood

