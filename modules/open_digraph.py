
class node:
    
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

    
    
    #Getters and setters
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
    
    
    #Adding and removing
    def add_parent_id(self, par_id , multiplicity=1):
        self.parents[par_id] = multiplicity
    
    def add_child_id(self, child_id , multiplicity=1):
        self.children[child_id] = multiplicity

    def remove_parent_once(self,id):
        self.parents[id] -=1
        if self.parents[id] == 0:
            del  self.parents[id]
            
    def remove_child_once(self,id):
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



class open_digraph: # for open directed graph
    
    def __init__(self, inputs, outputs, nodes):
        
        """
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        """
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id:node for node in nodes} 


    @classmethod
    def empty(cls):
        return open_digraph([],[],{})

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
        self.inputs.append(id)

    def add_output_id(self , id):
        self.outputs.append(id)
    
    def new_id(self):
        id = 0
        for i in self.nodes.keys():
            if id==i :
                id+=1
        return id
    
    
    
    #Adding and removing edges/nodes
    
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
        new_node = node(new_ID,label=label , parents=parents , children=children)
        self.nodes[new_ID] = new_node
        
        #ajout des arretes
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


    
    def is_well_formed(self):
        for i in self.inputs:
            if i not in self.nodes.keys():
                return False          
            if self.get_node_by_id(i).get_children() != {}:
                return False
            children = [self.get_node_by_id(i).get_children().values()]
            if len(children) !=1 or children[0] != 1:
                return False
            
        for o in self.outputs:
            if o not in self.nodes.keys():
                return False          
            if self.get_node_by_id(i).get_parents() != {}:
                return False
            parents = [self.get_node_by_id(i).get_parents().values()]
            if len(parents) !=1 or parents[0] != 1:
                return False
            

        for key , node in self.nodes.items():
            if key != node.get_id():
                return False

            parents = self.get_node_by_ids(nodes.get_parents().keys())
            for p in parents:
                if p.get_children()[key] != node.get_parents()[p.get_id()]:
                    return False
            
            children = self.get_node_by_ids(nodes.get_children().keys())
            for c in children:
                if p.get_parents()[key] != node.get_children()[c.get_id()]:
                    return False
        return True
    
    def assert_is_well_formed(self):
        assert self.is_well_formed() , "The graph is not well formed."
    
    
    def add_input_node(self , child_id):
        assert child_id in self.nodes.values() , "Node connected to input doesn't exist."
        new_inp = self.add_node(children={child_id: self.nodes[child_id]})
        self.add_input_id(new_inp)
    
    def add_output_node(self , par_id):
        assert par_id in self.nodes.values() , "Node connected to output doesn't exist."
        new_out = self.add_node(parents={par_id: self.nodes[par_id]})
        self.add_output_id(new_out)
    
    
    def copy(self):
        return open_digraph(self.inputs, self.outputs , self.nodes.values())

    def __str__(self):
        s =  f"*********Graph*********\nInputs : {self.inputs}\nOutputs : {self.outputs}\nNodes :\n "
        for n in self.nodes.values():
            s += " \n-------\n"+n.__str__()
        return s
    def __repr__(self):
            return repr(self.__str__)



