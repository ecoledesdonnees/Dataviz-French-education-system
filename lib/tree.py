import copy

import particle_filter



def state_variables_from_tree(tree):
    state_variables = [ tree["name"] ]
    if "leadsTo" in tree:
        for option in tree["leadsTo"]:
            res = state_variables_from_tree(copy.copy(option))
            state_variables = state_variables + copy.copy(res)
    return list(set(state_variables))
    
def extract_tree(path, tree):
    extracted_tree = copy.copy(tree)
    remaining_path = path
    ind = 0
    while len(remaining_path) > 0:
        ind = ind + 1
        if remaining_path[0] == extracted_tree["name"]:
            remaining_path.pop(0)
        else:
            for option in extracted_tree["leadsTo"]:
                if option["name"] == remaining_path[0]:
                    extracted_tree = copy.copy(option)
                    remaining_path.pop(0)
    return extracted_tree
    
def extend_paths_by_1_year(paths, tree):
    new_paths = []
    for path in paths:
        subtree = copy.copy(extract_tree(copy.copy(path), tree))
        repeat_path = path + [subtree["name"]]
        new_paths += [repeat_path] 

        if "leadsTo" in tree:
            for option in subtree["leadsTo"]:
                option_path = path + [option["name"]]
                new_paths += [option_path]
    return new_paths

def paths_after_n_years(n, tree):
    paths = [["CP"]]
    for i in range(n):
        paths = copy.copy(extend_paths_by_1_year(paths, tree))
    return paths