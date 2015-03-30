
import igraph
import re
import sys

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


states = open("states.dat","r")
transitions = open("transitions.dat","r")
json = open("orientation_tree.json","w")

#read the graph from the files 'states.dat' & 'transitions.dat'.
g = igraph.Graph()
igraph.Graph.to_directed(g)
g.add_vertex("Drop")

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
		g.add_edge(c_state,drop)
	states.pop(0)

#generating the orientation tree (which is a DAG).
init = g.vs["name"].index("CP") #initial point.
do_next_level(g,init,json,0,"true")


