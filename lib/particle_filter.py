import copy

import numpy as np

import tree as t

def model_propagation(state, tree, theta): 
    next_state = {}
    for path_name in state:
        path = state[path_name]["path"]
        size = state[path_name]["size"]

        subtree = copy.copy(t.extract_tree(copy.copy(path), tree))
        last_class = subtree["name"]

        repeat_path_name = path_name + '_' + last_class
        repeat_path = path + [subtree["name"]]

        repeating_students = np.random.binomial(size, theta["repeat"])
        passing_students = size - repeating_students

        next_state[repeat_path_name] = {
            "size": repeating_students,
            "path": repeat_path
        }

        if "leadsTo" in subtree:

            pvals = []
            for option in subtree["leadsTo"]:
                transition_parameter_name = "%s_to_%s" %(last_class, option["name"])
                pvals.append(theta[transition_parameter_name])

            choices_draw = np.random.multinomial(passing_students, pvals)

            for ind_option, option in enumerate(subtree["leadsTo"]):
                option_path_name  = path_name + '_' + option["name"]
                option_path = path + [option["name"]]
                next_state[option_path_name] = {
                    "size": choices_draw[ind_option],
                    "path": option_path
                }

    return next_state

    

def particle_filter(n, tree, theta):
    
    # Initialize state
    state = { 
        "CP": {
            "size": 600000,
            "path": ["CP"] 
        }
    }

    for i in range(n):

        # Propagate
        state = model_propagation(state, tree, theta)

        # Compute weights

        # Resample

    return state