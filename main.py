import json

from lib import particle_filter as pf
	
if __name__ == '__main__':

	trajectories = pf.generate_trajectories()

	for trajectory in trajectories:
		print trajectory
