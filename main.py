import json

from lib import particle_filter as pf
from lib import dag

if __name__ == '__main__':

	# trajectories = pf.generate_trajectories()

	# with open('data/trajectories.json', 'w') as outfile:
	#     json.dump(trajectories, outfile)

	g = dag.get_graph("data/transitions.dat")
	theta = json.load(open('data/theta.json'))
	trajectories = json.load(open('data/trajectories.json'))

	print dag.compute_zoomed_graphs_from_trajectories(trajectories)


