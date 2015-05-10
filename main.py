import json

from lib import particle_filter as pf
	
if __name__ == '__main__':

	trajectories = pf.generate_trajectories()

	with open('data/trajectories.json', 'w') as outfile:
	    json.dump(trajectories, outfile)
