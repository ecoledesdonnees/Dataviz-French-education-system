import json

from lib import tree as t
from lib import particle_filter as pf
	
if __name__ == '__main__':

	# Scholar system tree stored as JSON.
	tree = json.load(open("data/scholar_tree.json"))

	# Arbitrary parameter vector to start experimenting
	theta = {
		"repeat": 0.05,
		"CP_to_CE1": 1,
		"CE1_to_CE2": 1,
		"CE2_to_CM1": 1
	}

	# filtered state after 3 years
	filtered_state = pf.particle_filter(3, tree, theta)

	print filtered_state




