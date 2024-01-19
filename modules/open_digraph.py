

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
        
        def __str__ (self):
            return f"Node {self.id}: \nLabel : {self.label}\nParents : {self.children}\nChildre : {self.children}"




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
        
    def __str__(self):
        return f"Inputs : {self.inputs}\nOutputs : {self.outputs}\nNodes : "