import unittest

class node:
    
    def __init__(self , identity , label , parents , children):
        
        """
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent nodes id to its multiplicity
        children: int->int dict; maps a child nodes id to its multiplicity 
        """
        
        self._id = identity
        self._label = label
        self._parents = parents
        self._children = children 
    

    def copy(self):
        return node(self.id , self.label , self.parents , self.children)

    
    def get_id(self):
        return self._id
    
    def get_label(self):
        return self._label
    
    def get_parents(self):
        return self._parents
    
    def get_children(self):
        return self._children   

    def set_id(self , id):
        self._id = id
    
    def set_label(self, label):
        self._label = label
    
    def set_children(self , children):
        self._children = children
    
    def add_parent_id(self, par_id , multiplicity=1):
        self._parents[par_id] = multiplicity
    
    def add_child_id(self, child_id , multiplicity=1):
        self._children[child_id] = multiplicity

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
        self._inputs = inputs
        self._outputs = outputs
        self._nodes = {node.id:node for node in nodes} 


    @classmethod
    def empty(cls):
        return open_digraph([],[],{})

    def get_inputs_ids(self):
        return self._inputs

    def get_outputs_ids(self):
        return self._outputs

    def get_id_node_map(self):
        return self._nodes

    def get_nodes(self):
        return self._nodes.values()

    def get_node_ids(self):
        return self._nodes.keys()

    def get_node_by_id(self,id):
        return self._nodes[id]
    
    def get_nodes_by_ids(self , ids):
        return [self._nodes[id] for id in ids]
    
    def set_inputs(self , inputs):
        self._inputs = inputs
    
    def set_outputs(self , outputs):
        self._outputs = outputs

    def add_input_id(self , id):
        self._inputs.append(id)

    def add_output_id(self , id):
        self._outputs.append(id)
    

    

    



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


n0 = [node(0, 'i', {}, {1:1})]
inp= [1,2,3] 
outputs = [5]
g = open_digraph(inp , outputs , n0)
n = node(0, 'i', {}, {1:1})
print(n)
n.id = 1
print(n)
            
"""if __name__ == '__main__': # the following code is called only when
    unittest.main() """
