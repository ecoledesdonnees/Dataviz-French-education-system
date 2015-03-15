import copy

import particle_filter


    
def extract_tree(path, tree):
    # Given a path, extract the subtree descending from it

    extracted_tree = copy.copy(tree)
    remaining_path = path
    ind = 0
    while len(remaining_path) > 0:
        ind = ind + 1
        if remaining_path[0] == extracted_tree["name"]:
            remaining_path.pop(0)
        else:
            for option in extracted_tree["leadsTo"]:
                if len(remaining_path) > 0 and option["name"] == remaining_path[0]:
                    extracted_tree = copy.copy(option)
                    remaining_path.pop(0)
    return extracted_tree
    
def extend_paths_by_1_year(paths, tree):
    # Given a series of paths, generate all possible paths after 1 year.

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