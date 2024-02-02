import unittest

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
    
    def add_parent_id(self, par_id , multiplicity=1):
        self.parents[par_id] = multiplicity
    
    def add_child_id(self, child_id , multiplicity=1):
        self.children[child_id] = multiplicity

    def __str__ (self):
        return f"Node {self.id}: \nLabel : {self.label}\nParents : {self.children}\nChildre : {self.children}"
        
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
        return self._nodes.keys()

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
                id=+1
        return id
    
    def add_node(self,label="",parents={},children={}):
        p_ids = parents.keys()
        c_ids= children.keys()
        r= p_ids+c_ids
        assert all(elem in r for elem in self.nodes.keys())
        new_ID= self.new_id()
        new_node = node(new_ID,label=label)
        self.nodes[new_ID] = new_node
        #ajout des arretes
        p = [(par , new_ID) for par in p_ids]
        c = [(new_ID, chi) for chi in c_ids]
        total=p+c
        mult = parents.values() + children.values()
        self.add_edges(total,mult)
        
    

    



    def copy(self):
        return open_digraph(self.inputs, self.outputs , self.nodes)

    def __str__(self):
        s =  f"Inputs : {self.inputs}\nOutputs : {self.outputs}\nNodes :\n "
        for n in self.nodes.values():
            s += "-------\n"+n.__str__()
        return s
    def __repr__(self):
            return repr(self.__str__)





class InitTest(unittest.TestCase):
    
    def test_init_node(self):
        n0 = node(0, 'i', {}, {1:1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1:1})
        self.assertIsInstance(n0, node)
        
          
            
            
    def test_init_open_digraph(self):
        n0 = [node(0, 'i', {}, {1:1})]
        inp= [1,2,3] 
        outputs = [5]
        
        g = open_digraph(inp , outputs , n0)
        self.assertEqual(g.nodes[0], n0)
        self.assertEqual(g.inputs, inp)
        self.assertEqual(g.outputs, outputs)



