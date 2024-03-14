import random
import os
import sys

"""  Generating Random Lists and Matrices  """

def random_int_list(n , bound):
    return [random.randint(0 , bound) for k in range(n)]

def random_int_matrix(n ,bound , null_diag = True, number_generator=(lambda : random.betavariate(1,5))):
    random.seed(number_generator)
    if not null_diag:
        return [random_int_list(n , bound) for k in range(n)]
    return [random_int_list(k , bound)+[0]+random_int_list(n-k-1 , bound) for k in range(n)]


def random_symetric_int_matrix(n , bound , null_diag = True, number_generator=(lambda : random.betavariate(1,5))):
    random.seed(number_generator)
    mat = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if i==j:
                mat[i][j] = int(not null_diag)* random.randint( 0,bound )
            else:
                v = random.randint(0,bound)
                mat[i][j] = v
                mat[j][i] = v
    return mat


def random_oriented_int_matrix(n , bound , null_diag = True, number_generator=(lambda : random.betavariate(1,5))):
    random.seed(number_generator)
    m = random_int_matrix(n , bound , null_diag=null_diag)
    for i in range(n):
        for j in range(n):
            if i<j and m[i][j] != 0 and m[j][i] != 0:
                if random.randint(0,1):
                    m[i][j] = 0
                else:
                    m[j][i] = 0
    return m
    
def random_dag_int_matrix(n,bound,null_diag=True, number_generator=(lambda : random.betavariate(1,5))):
    random.seed(number_generator)
    mat = [[0 for j in range(n)] for i in range(n)]
    if random.randint(0,1):
        for i in range(n):
            for j in range(n):
                if i<=j:
                    mat[i][j]= int(not(null_diag and i==j))*random.randint(0,bound)
    else:
        for i in range(n):
            for j in range(n):
                if i<=j:
                    mat[j][i]= int(not(null_diag and i==j))*random.randint(0,bound)
    return mat

def print_m(m):
    print("[")
    for i in range(len(m)):
        print(m[i].__str__() + ",")
    print("]")
    
def graph_from_adjacency_matrix(mat , inp = 0 , out = 0):
    """ 
    Generate a graph from an adjacency matrix with the number input and output nodes.

    Parameters:
    -----------
    mat (list list): A square representing the adjacency matrix of the graph.
    inp (int): Number of input nodes. Default is 0.
    out (int): Number of output nodes. Default is 0.
    number_generator (function): A function that generates random numbers. 
                                 Default is a function generating numbers from a beta distribution.

    Returns:
    --------
    open.diGraph: A directed graph generated from the provided adjacency matrix,
                       with optional input and output nodes.
    """
    graph = open_digraph([],[],[])
    nodelistIDS= {i:node(i,"",{},{}) for i in range(len(mat[0]))}
    graph.nodes= nodelistIDS
    N = range(len(mat[0]))
    for i in N:
        iemeNode = nodelistIDS[i]
        for j in N:
            graph.add_edge(i,j,mat[i][j])
    
    ids = list(graph.get_node_ids()).copy()
    for i in range(inp):
        choice = random.choice(ids)
        graph.add_input_id(choice)
        ids.remove(choice)
        
    for i in range(out):
        choice = random.choice(ids)
        graph.add_output_id(choice)
        ids.remove(choice)
    return graph


def identity_matrix(n):
    identity = [[0] * n for i in range(n)]
    for i in range(n):
        identity[i][i] = 1
    return identity

def copy_matrix(mat):
    return [row[:] for row in mat]

def degree_matrix(mat):
    """ Meant for adjacency matrices """
    res = copy_matrix(mat)
    for i in range(len(mat)):
        deg = 0 
        for j in range(len(mat)):
            deg += res[i][j]
        res[i][i] = deg
    return res

def laplacian(mat):
    return degree_matrix(mat) - mat

#Pivot de Gauss
def swap_rows(mat, row1, row2):
    mat[row1], mat[row2] = mat[row2], mat[row1]

def scale_row(mat, row, scalar):
    mat[row] = [scalar * element for element in mat[row]]

def add_scaled_row(mat, source_row, destination_row, scalar):
    scaled_row = [scalar * element for element in mat[source_row]]
    mat[destination_row] = [sum(pair) for pair in zip(mat[destination_row], scaled_row)]

def gauss(mat):
    n = len(mat)

    for pivot_row in range(n):
        if mat[pivot_row][pivot_row] == 0:
            for row_below in range(pivot_row + 1, n):
                if mat[row_below][pivot_row] != 0:
                    swap_rows(mat, pivot_row, row_below)
                    break
            else:
                continue  

        scale_row(mat, pivot_row, 1.0 / mat[pivot_row][pivot_row])

        for row_below in range(pivot_row + 1, n):
            if mat[row_below][pivot_row] != 0:
                add_scaled_row(mat, pivot_row, row_below, -mat[row_below][pivot_row])

def rank(mat):
    copy = copy_matrix(mat)
    gauss(copy)
    rank = sum(1 for row in copy if any(row))
    return rank

def kernel_dim(mat):
    return len(mat) - rank(mat)



class node:
    
    ###Constructor
    
    def __init__(self , identity , label , parents , children):
        
        """
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent nodes id to its multiplicity
        children: int->int dict; maps a child nodes id to its multiplicity 
        """
        
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children 
    

    def copy(self):
        return node(self.id , self.label , self.parents , self.children)

    
    
    ### Getters and setters
    def get_id(self):
        return self.id
    
    def get_label(self):
        return self.label
    
    def get_parents(self):
        return self.parents
    
    def get_children(self):
        return self.children   

    def set_id(self , id):
        self.id = id
    
    def set_label(self, label):
        self.label = label
    
    def set_children(self , children):
        self.children = children

    def set_parents(self, parents):
        self.parents = parents
    
    
    ###Adding and removing
    
    def add_parent_id(self, par_id , multiplicity=1):
        """ 
            Adds par_id to the node's parent dictionary with a given multiplicy
        """
        if par_id in self.parents.keys():
            self.parents[par_id] += multiplicity
        else:
            self.parents[par_id] = multiplicity
    
    def add_child_id(self, child_id , multiplicity=1):
        """ 
            Adds child_id to the node's children dictionary with a given multiplicy
        """
        
        if child_id in self.children.keys():
            self.children[child_id] += multiplicity
        else:
            self.children[child_id] = multiplicity


    #Note: if multiplicity == 0 the map to the node is removed
    
    def remove_parent_once(self,id):
        """ 
            removes a parent from the node's parent dictionary (one multiplicity)
        """
        self.parents[id] -=1
        if self.parents[id] == 0:
            del  self.parents[id]
            
    def remove_child_once(self,id):
        """ 
            removes a child from the node's children dictionary (one multiplicity)
        """
        self.children[id] -=1
        if self.children[id] == 0:
            del  self.children[id]
    
    def remove_parent_id(self , id):
        del  self.parents[id]
    
    def remove_child_id(self , id):
        del  self.children[id]
    
    def __str__ (self):
        return f"Node {self.id}: \nLabel : {self.label}\nParents : {self.parents}\nChildren : {self.children}"
        
    def __repr__(self):
        return repr(self.__str__)
    
    def __eq__(self,g):
        if type(self)!=type(g):
            return False
        return self.id == g.get_id() and self.label == g.get_label() and self.children == g.get_children() and self.parents == g.get_parents()
    def __ne__(self,g):
        return not self.__eq__(g)
    
    def indegree(self):
        """
            Returns the number on ingoing edges towards the node
        """
        
        acc = 0
        p = self.get_parents()
        for i in p:
            acc += p[i]
        return acc
    
    def outdegree(self):
        """
            Returns the number on outgoing edges from the node
        """
        acc = 0
        p = self.get_children()
        for i in p:
            acc += p[i]
        return acc
    
    def degree(self):
        """
            returns the degree of the node
        """
        return self.indegree()+self.outdegree()

class open_digraph: # for open directed graph
    
    
    ###Constructor 
    
    def __init__(self, inputs, outputs, nodes):
        
        """
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        """
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id:node for node in nodes} 
        self.assert_is_well_formed()

    def __eq__(self, g):
        if len(self.inputs) != len(g.get_inputs_ids()):
            return False
        if len(self.outputs) != len(g.get_outputs_ids()):
            return False
        for i in self.inputs:
            if i not in g.get_inputs_ids():
                return False
        for j in self.outputs:
            if j not in g.get_outputs_ids():
                return False
        # Check if nodes are equal
        if len(self.nodes) != len(g.get_id_node_map()):
            return False
        for node in self.nodes.values():
            if node not in g.get_nodes():
                return False
        return True
    def __ne__(self,g):
        return not self.__eq__(g)


    @classmethod
    def empty(cls):
        return open_digraph([],[],[])


    ### Getters and Setters
    def get_inputs_ids(self):
        return self.inputs

    def get_outputs_ids(self):
        return self.outputs

    def get_id_node_map(self):
        return self.nodes

    def get_nodes(self):
        return self.nodes.values()

    def get_node_ids(self):
        return self.nodes.keys()

    def get_node_by_id(self,id):
        return self.nodes[id]
    
    def get_nodes_by_ids(self , ids):
        return [self.nodes[id] for id in ids]
    
    def set_inputs(self , inputs):
        self.inputs = inputs
    
    def set_outputs(self , outputs):
        self.outputs = outputs

    def add_input_id(self , id):
        """
            Adds id to the list of inputs of the graph
        """
        assert id in self.nodes.keys() , "Input Node doesn't exist in graph"
        self.inputs.append(id)

    def add_output_id(self , id):
        """
            Adds id to the list of outputs of the graph
        """
        assert id in self.nodes.keys(), "Ouput Node doesn't exist in graph"
        self.outputs.append(id)
    
    def new_id(self):
        """
            Generates a new unique id usable in the graph
        """
        id = 0
        for i in self.nodes.keys():
            if id==i :
                id+=1
        return id
    
    
    
    ###Adding and removing edges/nodes
    
    def add_edge(self , src , tgt , m=1):
        assert src in self.nodes.keys()
        assert tgt in self.nodes.keys()
        
        n1 = self.get_node_by_id(tgt)
        n2 = self.get_node_by_id(src)
        n1.add_parent_id(src,m)
        n2.add_child_id(tgt,m)
    
    
    def add_edges(self , edges , m_list):
        n = len(m_list)
        assert n == len(edges)
        for i in range(n):
            self.add_edge(edges[i][0] , edges[i][1], m=m_list[i])
    
    def add_node(self,label="",parents={},children={}):
        p_ids = list(parents.keys())
        c_ids = list(children.keys())
        r = p_ids + c_ids
        assert ( (elem not in self.nodes.keys()) for elem in r)
        new_ID= self.new_id()
        new_node = node(new_ID,label=label , parents= {} , children={})
        self.nodes[new_ID] = new_node
        
        
        #Adding edges
        p = [(par , new_ID) for par in p_ids]
        c = [(new_ID, chi) for chi in c_ids]
        total=p+c
        mult = list(parents.values()) + list(children.values())
        self.add_edges(total,mult)
        return new_ID
    
    
    #**************A FACTORISER PLUS TARD*******************
    
    def remove_edge(self, src, tgt):
        s = self.get_node_by_id(src)
        t = self.get_node_by_id(tgt)
        
        s.remove_child_once(tgt)
        t.remove_parent_once(src)
    
    def remove_parallel_edges(self, src ,tgt):
        s = self.get_node_by_id(src)
        t = self.get_node_by_id(tgt)
        
        s.remove_child_id(tgt)
        t.remove_parent_id(src)
        
    def remove_node_by_id(self , id):
        all_edges =  [(p,id) for p in self.get_node_by_id(id).get_parents()] + [(id,p) for p in self.get_node_by_id(id).get_children()]
        
        for pair in all_edges:
            self.remove_parallel_edges(pair[0] , pair[1])
        
        del self.nodes[id]
        
    def remove_edges(self , edges):
        for p in edges:
            self.remove_edge(p[0] , p[1])
    
    def remove_several_parallel_edges(self ,edges):
        for p in edges:
            self.remove_parallel_edges(p[0] , p[1])
            
    def remove_nodes_by_id(self, ids):
        for id in ids:
            self.remove_node_by_id(id)


    ### integrity checks
    
    def is_well_formed(self):
        """
            Checks if the graph is well formed 
        """
        for i in self.inputs:
            if i not in self.nodes.keys():
                return False          
            if self.get_node_by_id(i).get_parents() != {}:
                return False
            children = list(self.get_node_by_id(i).get_children().values())
            if len(children) !=1 or children[0] != 1:
                return False
            
        for o in self.outputs:
            if o not in self.nodes.keys():
                return False          
            if self.get_node_by_id(o).get_children() != {}:
                return False
            parents = list(self.get_node_by_id(o).get_parents().values())
            if len(parents) !=1 or parents[0] != 1:
                return False
            

        for key , node in self.nodes.items():
            if key != node.get_id():
                return False

            parents = self.get_nodes_by_ids(node.get_parents().keys())
            for p in parents:
                if p.get_children()[key] != node.get_parents()[p.get_id()]:
                    return False
            
            children = self.get_nodes_by_ids(node.get_children().keys())
            for c in children:
                if c.get_parents()[key] != node.get_children()[c.get_id()]:
                    return False
        return True
    
    def assert_is_well_formed(self):
        assert self.is_well_formed() , "The graph is not well formed."
    
    
    def add_input_node(self , child_id):
        assert child_id in self.nodes.keys() , "Node connected to input doesn't exist."
        new_inp = self.add_node(children={child_id: 1})
        self.add_input_id(new_inp)
    
    def add_output_node(self , par_id):
        assert par_id in self.nodes.keys() , "Node connected to output doesn't exist."
        
        new_out = self.add_node(parents={par_id: 1})
        self.add_output_id(new_out)
    
    
    def copy(self):
        new_nodes =[node.copy() for node in self.nodes.values()]
        new_inputs = self.inputs.copy()
        new_outputs = self.outputs.copy()
        return open_digraph(new_inputs, new_outputs , new_nodes)

    def __str__(self):
        s =  f"*********Graph*********\nInputs : {self.inputs}\nOutputs : {self.outputs}\nNodes :\n "
        for n in self.nodes.values():
            s += " \n-------\n"+n.__str__()
        return s
    def __repr__(self):
            return repr(self.__str__)
    
    def adjacency_matrix(self):
        mat = [[0 for _ in self.nodes] for _ in self.nodes]
        node_ids = self.nodes
        
        for i in node_ids:
            node_i = self.nodes[i]
            children_ids = node_i.get_children()
            
            for j in node_ids:
                node_j = self.nodes[j]
                if node_j.get_id() in children_ids:
                    mat[i][j] = children_ids[node_j.get_id()]      
        return mat

    @classmethod
    def random(cls,n, bound, inputs=0, outputs=0, form="free", number_generator=(lambda :random.betavariate(1,5))): 
        if form=="free":
            return graph_from_adjacency_matrix(random_int_matrix(n,bound,False), inp = inputs , out = outputs, number_generator=number_generator) 
        elif form=="DAG":
            return graph_from_adjacency_matrix(random_dag_int_matrix(n,bound), inp = inputs , out = outputs, number_generator=number_generator)
        elif form=="oriented": 
            return graph_from_adjacency_matrix(random_oriented_int_matrix(n,bound,False), inp = inputs , out = outputs, number_generator=number_generator)
        elif form=="loop-free": 
            return graph_from_adjacency_matrix(random_int_matrix(n,bound), inp = inputs , out = outputs, number_generator=number_generator)
        elif form=="undirected":
            return graph_from_adjacency_matrix(random_symetric_int_matrix(n,bound), inp = inputs , out = outputs, number_generator=number_generator)
        elif form=="loop-free undirected":
            return  graph_from_adjacency_matrix(random_symetric_int_matrix(n,bound), inp = inputs , out = outputs, number_generator=number_generator)
        elif form=="loop-free oriented": 
            return graph_from_adjacency_matrix(random_oriented_int_matrix(n,bound), inp = inputs , out = outputs, number_generator=number_generator)
        else : return [[]]

    def save_as_dot_file(self, path, verbose = True):
        assert path[-4:] == ".dot" , "Not the right extension"
        s = "digraph G {\n"
        edges = ""
        for iden, node in self.nodes.items():
            s += f'v{iden} [label="{node.get_label()}"'
            if verbose:
                s += f"id = {iden}"
            if iden in self.inputs:
                s+= f",input={True} ,output={False} "
            elif iden in self.inputs:
                s+= f",input={False},output={True}"
            else:
                s+= f",input={False},output={False}"
            s += "];\n"
            for child in node.get_children():
                edges += f"v{iden} -> v{child};\n"
        edges += "}"
        
        f = open(path, "w")
        f.write(s + edges)
        f.close()


    def display_graph(self,verbose=False):
        self.save_as_dot_file("display.dot",verbose = verbose)
        os.system("dot -Tpdf display.dot -o display.pdf ")
        if sys.platform.startswith('win'):
            os.system("icacls display.pdf  /grant %USERNAME%:F")
        elif sys.platform.startswith('linux'):
            os.system("chmod 777 display.pdf")
        
        os.system("explorer.exe display.pdf")


    @classmethod
    def from_dot_file(cls , path):
        assert path[-4:] == ".dot" , "Not the right extension"
        f = open(path, "r")
        text  = f.read()
        g = open_digraph([], [] , {})
        st = text.index("{")
        end = text.index("}")
        assert st != -1 and end != -1 , "Invalid File , no {}"
        text = text[st+1 : end]
        elements = text.split(";")
        nodes_dict = {}  # dict from nodes names to their ids in the graph
        for e in elements:
            if "[" in e: #declaration de noeud
                bracketstart = e.index("[")
                bracketend = e.index("]")
                if bracketstart != -1:
                    node_name = e[:bracketstart].strip()
                    att_val_liste = [(attribute.split("=")[0] ,attribute.split("=")[1].replace("\"" , "") ) for attribute in e[bracketstart+1 : bracketend].split(",")]
                    for pair in att_val_liste:
                        lab = ""
                        inp = out = False
                        if pair[0] == "label":
                            lab = pair[1]
                        elif pair[0] == "input":
                            inp = True
                        elif  pair[0] == "output":
                            out = True
                        assert not (inp and out) , "The node is both an input and output node"
                        nid = g.add_node(label= lab)
                        if inp:
                            g.add_input_id(nid)
                        if out:
                            g.add_input_id(nid)
                        nodes_dict[node_name] = nid
            elif "->" in e:
                chain = e.strip().split(" -> ")
                parent = chain[0]
                children = chain[1:]
                if parent not in nodes_dict.keys():
                    parent_id = g.add_node()
                    nodes_dict[parent] = parent_id
                for child in children:
                    if child not in nodes_dict.keys():
                        child_id = g.add_node()
                        nodes_dict[child] = child_id
                    g.add_edge(nodes_dict[parent],nodes_dict[child])
        return g

    def is_acyclic(self):
        visited = set()
        stack = set()

        def dfs(node):
            if node.get_id() in stack:
                return False
            if node.get_id() in visited:
                return True

            visited.add(node.get_id())
            stack.add(node.get_id())

            children = node.get_children()
            for child_id in children:
                if not dfs(self.nodes[child_id]):
                    return False  # Cycle detected

            stack.remove(node.get_id())
            return True

        for id in self.nodes:
            if id not in visited:
                if not dfs(self.nodes[id]):
                    return False  # Cycle detected

        return True  # No cycle found

    def min_id(self):
        m = -1
        for node in self.nodes.values():
            cid = node.get_id() 
            if m==-1:
                m = cid
            elif cid < m:
                m = cid
        return m
    
    def max_id(self):
        m = -1
        for node in self.nodes.values():
            cid = node.get_id() 
            if cid > m:
                m = cid
        return m

    def shift_indices(self,n):
        def shift_keys(dictionary, m):
            shifted_dict = {}
            for key, value in dictionary.items():
                new_key = key + m
                shifted_dict[new_key] = value
            return shifted_dict
        
        if n != 0:
            for node in self.nodes.values():
                cid = node.get_id() 
                node.set_id(cid+n)
                node.set_children(shift_keys(node.get_children(),n))
                node.set_parents(shift_keys(node.get_parents(),n))
            for i in range(len(self.inputs)):
                self.inputs[i] += n
            for i in range(len(self.outputs)):
                self.outputs[i] += n
        self.nodes = shift_keys(self.nodes, n)
        
    def iparallel(self, g):
        minId1 = self.min_id()
        maxId2 = g.max_id()
        
        self.shift_indices(-minId1+maxId2+1)
        for key,nnode in g.get_id_node_map().items():
            self.nodes[key]= nnode.copy()
        for j in g.get_inputs_ids():
            self.add_input_id(j)
        for i in g.get_outputs_ids():
            self.add_output_id(i)
     

    def parallel(self, g):
        c = self.copy()
        c.iparallel(g)
        return c

    def icompose(self, f):
        assert len(f.get_outputs_ids()) == len(self.get_inputs_ids()) , "error, domains don't match"
        self.iparallel(f)
        print(self.get_inputs_ids())
        old_input = [inp for inp in self.get_inputs_ids() if inp not in f.get_inputs_ids()] #inputs that used to belong to self after shift
        print(old_input)
        print(f.get_outputs_ids())
        for k,f_out in enumerate(f.get_outputs_ids()):
            self.get_node_by_id(f_out).set_children(self.get_node_by_id(old_input[k]).get_children())
            self.remove_node_by_id(old_input[k])


        for inp in self.get_inputs_ids():
            if inp in old_input:
                self.get_inputs_ids().remove(inp)

        for out in self.get_outputs_ids():
            if out  in f.get_outputs_ids():
                self.get_outputs_ids().remove(out)


    def compose(self , f):
        c = self.copy()
        c.icompose(f)
        return c


    @classmethod
    def identity(cls , n):
        g = cls.empty()
        for i in range(n):
            inp = g.add_node()
            out = g.add_node()
            g.add_edge(inp, out)
            g.add_input_id(inp)
            g.add_output_id(out)
        return g


    def connected_components(self):
        
        visited = set()
        nb = 0
        component_dict = {}


        def dfs(node):
            if node.get_id() in visited:
                component_dict[node.get_id()] = nb 
            
            else:
                visited.add(node.get_id())
                children = node.get_children()
                parents = node.get_parents()
                for child_id in children:
                    dfs(self.nodes[child_id])
                    component_dict[child_id] = nb 
                for parent_id in parents:
                    dfs(self.nodes[parent_id])
                    component_dict[parent_id] = nb 

                
        
        for node in self.nodes.values():
            if node.get_id() not in visited:
                dfs(node)
                nb +=1
        return (nb , component_dict)

    def component_list(self):
        nb , dict_ = self.connected_components()
        componentMat = [[] for i in range(nb)]
        for i in dict_ :
            componentMat[dict_[i]].append(self.nodes[i])
        
        
        for i in range(nb):
            component_input = [inp for inp in self.get_inputs_ids() if dict_[inp]==i]
            component_output = [out for out in self.get_outputs_ids() if dict_[out]==i]
            componentMat[i] = open_digraph(component_input , component_output , componentMat[i])
        return componentMat

class bool_circ(open_digraph):
    def __init__(self, g):
        super().__init__(g.get_inputs_ids(), g.get_outputs_ids(), [])
        self.nodes = g.get_id_node_map()
        #self.is_well_formed()
    
    def is_well_formed(self):
        #super().assert_is_well_formed()
        if super().is_acyclic():
            for key,node in self.nodes.items():
                if (node.get_label() == "" or node.get_label() == "1" or node.get_label() == "0") and node.indegree() > 1 : 
                        return False
                elif node.get_label() != "" and node.outdegree() > 1 :
                        return False
            return True
        return False
    

# n0 = [node(0, '&', {}, {}) , node(1, '', {}, {})]
# inp= []
# outputs = []
# op = open_digraph(inp,outputs, n0)
# g = bool_circ(op)
# g.add_node('|', {1:1}, {0:1})
# # print_m(g.adj_mat())
# # print_m(random_symetric_int_matrix(5,9,True))
# # print_m(random_oriented_int_matrix(5,9))
# # print_m(random_dag_int_matrix(5,9))
# rand_mat = random_dag_int_matrix(5,5,False)
# m = graph_from_adjacency_matrix(rand_mat)
# #print(m)
# #m.shift_indices(5)
# # print(m)
# # print_m(rand_mat)
# # print(g.is_well_formed())
# empt = open_digraph([],[],{})
# #empt.iparallel(g)
# # print(empt)
# # print(g)
# g.iparallel(g.copy())
# #print(g)
# empt.iparallel(g)
# #print(empt)
# #test_g = open_digraph.from_dot_file("modules/test.dot")
# #test_g.display_graph()

# n02 = [node(0, '0', {}, {2:1}) , node(1, 'ss', {}, {3:1}),node(2, 'zs', {0:1}, {4:3}),node(3, 'ee', {1:1}, {4:2}) , node(4, '5', {2:3,3:2}, {5:1}),node(5, '&', {4:1}, {})]
# inp2= [0,1]
# outputs2 = [5]

# n1 = [node(0, '&', {}, {1:1}) , node(1, 'ss', {0:1,2:1}, {2:1, 3:1}),node(2, 'zs', {1:1}, {1:1}),node(3, 'bb', {1:1}, {}) ]
# inp1= [0]
# outputs1 = [3]

# gtest1 = open_digraph(inp2,outputs2,n02)

# gtest2 = open_digraph(inp1,outputs1,n1)

# #test3 = open_digraph([],[],n0)
# print(gtest2.parallel(gtest1).connected_components())
# print(gtest2.is_acyclic())
# print(gtest2)
# n = gtest2.add_node(node(4,"a",{},{0:1}))
# gtest2.add_edge(3,n)
# #gtest2.add_edge(n,0)
# print(gtest2.is_acyclic())
# print(gtest2)
# # for g in gtest2.parallel(gtest1).component_list()[:1]:
# #     g.display_graph()
# #print(open_digraph.identity(5))
# g.add_node()
# print(g == empt)