
import igraph
import re
import sys

# will define the scholar_tree in json format from two files:
# 'states.dat' which contains the list of possible states (could be removed). 
# 'transitions.dat' stroing the possible transitions btw states. 
# the second file should be 'tab separated' while on the first one,
# one state per line is expected.
# defining transition to 'Drop' state for every state after '3eme' can be
# easily done using the graph 'g'.    

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
		#print(succ)
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
for line in states:
	g.add_vertex(line.rstrip())

for line in transitions:
	st = line.split('\t')
	g.add_edge(st[0],st[1].rstrip())

#add edge to 'Drop' from every level >=3eme
states = [ g.vs["name"].index("3eme") ]
drop = g.vs["name"].index("Drop")
while(len(states)!=0):
	c_state = states[0]
	succ = g.successors(c_state)
	states = states + succ
	if ( len(succ)!=0 & (not g.are_connected(c_state,drop)) ):
		g.add_edge(c_state,drop)
	states.pop(0)

#print(g)

#
do_next_level(g,0,json,0,"true")
#


