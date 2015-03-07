import json

from lib import tree as t
from lib import particle_filter as pf
	
if __name__ == '__main__':

	tree = json.load(open("data/scholar_tree.json"))
	theta = {
		"repeat": 0.05,
		"CP_to_CE1": 1,
		"CE1_to_CE2": 1,
		"CE2_to_CM1": 1
	}


	print pf.particle_filter(3, tree, theta)

	# print t.state_variables_from_tree(tree)




