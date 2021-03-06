
import igraph
import re
import sys
import json

# will define the scholar_tree in json format from one file:
# 'transitions.dat' storing the possible transitions btw states.
# this file should be 'tab separated'.

def line_header(state,b):
	if b:
		return "\"name\": \""+state+"\",\n"
	else:
		return "\"name\": \""+state+"\"\n"

def repeat_header():
	return "\"pRepeat\": \"pRepeat\",\n"

def leads_to():
	return "\"leadsTo\": [\n"

def do_next_level(g,vertex,json,level,last):
	succ = g.successors(vertex)
	ts  = "\t"*level
	ts_ = ts + "\t"
	state = g.vs["name"][vertex]
	json.write( ts + "{\n" )
	json.write( ts_ + line_header(state,len(succ)!=0) )
	if(len(succ)!=0):
		json.write( ts_ + repeat_header() )
		json.write( ts_ + leads_to() )
		for s in succ:
			do_next_level(g,s,json,level+2,s==succ[-1])
		json.write( ts_ + "]\n" )
	if last:
		json.write( ts + "}\n" )
	else:
		json.write( ts + "},\n" )



def get_graph(File):
	transitions = open(File,"r")
	g = igraph.Graph()
	igraph.Graph.to_directed(g)
	g.add_vertex("Drop")
	#read the graph from the 'transitions' file.
	for line in transitions:
		st = line.split('\t')
		if (not (st[0] in g.vs["name"])):
			g.add_vertex(st[0])
		if (not (st[1] in g.vs["name"])):
			g.add_vertex(st[1].rstrip())
		g.add_edge(st[0],st[1].rstrip())

	#add edge to 'Drop' from every level >= 3eme [except achievement levels].
	states = [ g.vs["name"].index("3eme") ]
	drop = g.vs["name"].index("Drop")
	while(len(states)!=0):
		c_state = states[0]
		succ = g.successors(c_state)
		states = states + succ
		if ( len(succ)!=0 & (not g.are_connected(c_state,drop)) ):
			g.add_edge(c_state,drop,)
		states.pop(0)

	return g


def write_orientation_tree(g,init,File):
	#generating the orientation tree (which is a DAG).
	json = open(File,"w")
	init = g.vs["name"].index(init) #initial point.
	do_next_level(g,init,json,0,"true")

def normalized_theta(g,theta):
	new_theta = copy.copy(theta)
	for vertex in g.vs:
		succ = g.successors(vertex)
		sum_fixed = 0
		sun_not_fixed = 0
		if(len(succ)!=0):
			for n_vertex in succ:
				transition_name = "%s_to_%s" %(g.vs["name"][vertex],g.vs["name"][n_vertex])
				if(new_theta[transition_name]["fixed"]):
					sum_fixed = sum_fixed + new_theta[transition_name]["value"]
				else:
					sum_not_fixed = sum_not_fixed + new_theta[transition_name]["value"]
			if sum_fixed>1:
				print "Sum of fixed theta value from "+g.vs["name"][vertex]+" is "+string(sum_fixed)
			Z = (1 - sum_fixed)/sum_not_fixed
			for n_vertex in succ:
				transition_name = "%s_to_%s" %(g.vs["name"][vertex],g.vs["name"][n_vertex])
				if(not new_theta[transition_name]["fixed"]):
					new_theta[transition_name]["value"] = new_theta[transition_name]["value"]*Z
	return new_theta


def contains(small, big):
    for i in xrange(len(big)-len(small)+1):
        for j in xrange(len(small)):
            if big[i+j] != small[j]:
                break
        else:
            return i, i+len(small)
    return False

def compute_zoomed_graphs_from_trajectories(trajectories):

	zoomed_graphs = {}

	# get all classes
	all_vertices = []
	for trajectory in trajectories:
		for vertex in trajectory['path']:
			if not vertex in all_vertices:
				all_vertices.append(vertex)


	print all_vertices

	for vertex in all_vertices:
		print vertex
		nodes = []
		nodes.append(vertex)

		# coming out
		o_edges = []
		sum_of_fluxes_to_all_vertices = 0
		for o_vertex in all_vertices:
			sum_of_fluxes_to_this_vertex = 0
			for trajectory in trajectories:
				if contains([vertex, o_vertex], trajectory["path"]):
					sum_of_fluxes_to_this_vertex += trajectory["mean"]
					sum_of_fluxes_to_all_vertices += trajectory["mean"]
			if sum_of_fluxes_to_this_vertex > 0:
				o_edges.append( {'source':vertex, 'target':o_vertex, 'value': sum_of_fluxes_to_this_vertex} )
				nodes.append(o_vertex)
		for e in o_edges:
			#e["value"] = e["value"]/float(sum_of_fluxes_to_all_vertices)
			print "   out - %s    %s" %(e['target'], e['value'])


		# coming in
		i_edges = []
		sum_of_fluxes_from_all_vertices = 0
		for i_vertex in all_vertices:
			sum_of_fluxes_from_this_vertex = 0
			for trajectory in trajectories:
				if contains([i_vertex, vertex], trajectory["path"]):
					sum_of_fluxes_from_this_vertex += trajectory["mean"]
					sum_of_fluxes_from_all_vertices += trajectory["mean"]
			if sum_of_fluxes_from_this_vertex > 0:
				i_edges.append( {'source':i_vertex, 'target':vertex, 'value': sum_of_fluxes_from_this_vertex} )
				nodes.append(i_vertex)
		for e in i_edges:
			#e["value"] = e["value"]/float(max(sum_of_fluxes_to_all_vertices, sum_of_fluxes_from_all_vertices))
			# We need to take max of in & out flux to handle first and last nodes
			print "   in - %s    %s" %(e['source'], e['value'])



		nodes = list(set(nodes))
		nodes = [{ 'name': node } for node in nodes]
		edges = i_edges
		edges.extend(o_edges)
		zoomed_graphs[vertex] = {'links':edges, 'nodes':nodes}

	with open('data/zoomed_graphs_test.json', 'w') as outfile:
	    json.dump(zoomed_graphs, outfile,indent=5,separators=(',', ': '))


def compute_graph_from_trajectories(trajectories):

	graph = {}
	edges = []

	# get all classes
	all_vertices = []
	for trajectory in trajectories:
		for vertex in trajectory['path']:
			if not vertex in all_vertices:
				all_vertices.append(vertex)

	print all_vertices

	for vertex in all_vertices:
		print vertex
		nodes = []

		# only looking at outgoing edges.
		o_edges = []
		sum_of_fluxes_to_all_vertices = 0
		for o_vertex in all_vertices:
			sum_of_fluxes_to_this_vertex = 0
			for trajectory in trajectories:
				if contains([vertex, o_vertex], trajectory["path"]):
					sum_of_fluxes_to_this_vertex += trajectory["mean"]
					sum_of_fluxes_to_all_vertices += trajectory["mean"]
			if sum_of_fluxes_to_this_vertex > 0:
				if o_vertex!=vertex:
					o_edges.append( {'source':vertex, 'target':o_vertex, 'value': sum_of_fluxes_to_this_vertex} )
		for e in o_edges:
			#e["value"] = e["value"]/float(sum_of_fluxes_to_all_vertices)
			print "   out - %s    %s" %(e['target'], e['value'])

		edges.extend(o_edges)

	nodes = [{ 'name': node } for node in all_vertices]
	graph = {'links':edges, 'nodes':nodes}

	with open('data/complete_graph_test.json', 'w') as outfile:
	    json.dump(graph, outfile,indent=5,separators=(',', ': '))

