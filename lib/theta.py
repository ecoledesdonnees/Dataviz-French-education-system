import sys


bifurcations = [
	[ 'CP_to_CE1'  ],
	[ 'CE1_to_CE2' ],
	[ 'CE2_to_CM1' ],
	[ 'CM1_to_CM2' ],
	[ 'CE1_to_CE2' ],
	[ 'CM2_to_6eme' ],
	[ '6eme_to_5eme' ],
	[ '5eme_to_4eme' ],
	[ '4eme_to_3eme' ],
	[ '3eme_to_2nde_ge', '3eme_to_2nde_pro', '3eme_to_CAP1' ],
	[ 'CAP1_to_CAP2' ],
	[ '2nde_to_1ere' ],
	[ 'CAP2_to_Finish' ],
	[ '1ere_to_Tale' ],
	[ 'Tale_to_Finish' ]
]

def get_p_repeat(theta, current_class):
	if current_class in ['CP', 'CE1', 'CE2', 'CM1', 'CM2']:
		return theta['repeat_primaire']['value']
	elif current_class in ['6eme', '5eme', '4eme', '3eme']:
		return theta['repeat_college']['value']
	elif current_class in ['2nde_GT', '2nde_Pro']:
		return theta['repeat_2nde']['value']
	elif current_class in ['1ere_T', '1ere_G', '1ere_Pro']:
		return theta['repeat_1ere']['value']
	elif current_class in ['Tale_T', 'Tale_G', 'Tale_Pro']:
		return theta['repeat_Tale']['value']
	elif current_class in ['BEP1', 'BEP2']:
		return theta['repeat_BEP']['value']
	elif current_class in ['CAP1', 'CAP2']:
		return theta['repeat_CAP']['value']
	elif current_class in ['Drop', 'got_BEP', 'got_CAP']:
		return 1
	else:
		print 'unknown class %s g_p_repeat' %current_class
		sys.exit()



def from_theta_to_full_theta(theta):
	full_theta = copy.copy(theta)
	
	for bifurcation in bifurcations:
		probs_sum = 0
		
		for i in range(len(bifurcation)-2):
			full_theta[bifurcation[i]] = max(0, min(1 - probs_sum, full_theta[bifurcation[i]]))
			probs_sum += full_theta[bifurcation[i]]

		full_theta[len(bifurcation)-1] = 1 - probs_sum

	return full_theta

