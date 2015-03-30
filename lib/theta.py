


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


def from_theta_to_full_theta(theta):
	full_theta = copy.copy(theta)
	
	for bifurcation in bifurcations:
		probs_sum = 0
		
		for i in range(len(bifurcation)-2):
			full_theta[bifurcation[i]] = max(0, min(1 - probs_sum, full_theta[bifurcation[i]]))
			probs_sum += full_theta[bifurcation[i]]

		full_theta[len(bifurcation)-1] = 1 - probs_sum

	return full_theta

