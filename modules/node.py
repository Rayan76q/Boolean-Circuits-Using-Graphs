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
        return node(self.id , self.label , self.parents.copy() , self.children.copy())

    
    
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
    
    def is_copy(self):
        return isinstance(self,copy_node)
    
    def is_or(self):
        return isinstance(self,or_node)
    
    def is_and(self):
        return isinstance(self,and_node)
    
    def is_not(self):
        return isinstance(self,not_node)
    
    def is_xor(self):
        return isinstance(self,xor_node)
    
    def is_constant(self):
        return isinstance(self,constant_node_node)
    
    def transform(self, circuit):
        if self.is_copy():
            copy_node(self).transform(circuit)
        elif self.is_and():
            and_node(self).transform(circuit)
        elif self.is_or():
            or_node(self).transform(circuit)
        elif self.is_not():
            not_node(self).transform(circuit)
        elif self.is_xor():
            xor_node(self).transform(circuit)
        




class copy_node(node):
    
    def __init__(self , identity, parents , children):
        super().__init__(identity,"",parents, children)
        
    def transform(self,circuit):
        r = False
        parents = list(self.get_parents())
        children = list(self.get_children())
                
        if len(children) == 1:  #gets rid of unecessary copies
            circuit.remove_node_by_id(self.get_id())
            circuit.add_edge(parents[0],children[0])
            return True
        else:
            for c in children:
                c_node = circuit.get_node_by_id(c)
                if  c_node.is_copy():
                    r=circuit.assoc_copy(self.get_id(),c)        
                elif c_node.is_xor():
                    r=circuit.involution_xor(c,self.get_id())
                parent_node = circuit.get_node_by_id(parents[0])
                if  parent_node.is_copy() :
                    r=circuit.assoc_copy(parents[0],self.get_id())
        return r

class and_node(node):
    
    def __init__(self , identity, parents , children):
        super().__init__(identity,"&",parents, children)
        
    def transform(self, circuit):
        r = False
        parents = list(self.get_parents())
        
        for p in parents:
            parent_node = circuit.get_node_by_id(p)
            if  parent_node.is_and():
                r=circuit.assoc_and(p,self.get_id())
        return r

class or_node(node):
    
    def __init__(self , identity, parents , children):
        super().__init__(identity,"|",parents, children)
        
    def transform(self, circuit):
        r = False
        parents = list(self.get_parents())
        for p in parents:
            parent_node = circuit.get_node_by_id(p)
            if  parent_node.is_or():
                r = circuit.assoc_or(p,self.get_id())  
        return r 


class not_node(node):
    
    def __init__(self , identity, parents , children):
        super().__init__(identity,"~",parents, children)
        
    def transform(self, circuit):
        r = False
        parent = list(self.get_parents())[0]
        child = list(self.get_children())[0]
                        
        if circuit.get_node_by_id(parent).is_not() :
            r=circuit.involution_not(parent,self.get_id())
        elif circuitget_node_by_id(child).is_not() :
            r=circuit.involution_not(self.get_id(),child)
                            
        elif circuit.get_node_by_id(child).is_copy():
            r=circuit.not_copy(node_id,child)
        return r
    
class xor_node(node):
    
    def __init__(self , identity, parents , children):
        super().__init__(identity,"^",parents, children)
        
    def transform(self, circuit):
        r = False
        parents = list(self.get_parents())
        
        for p in parents:
            parent_node = circuit.get_node_by_id(p)
            if  parent_node.is_xor():
                r=circuit.assoc_xor(p,self.get_id())
            elif parent_node.is_copy():
                r=circuit.involution_xor(self.get_id(),p)
            elif parent_node.is_not():
                r=circuit.not_xor(p,self.get_id())
        return r
        
class constant_node(node):
    
    def __init__(self , identity , label , parents , children):
        assert label == "1" or label == "0"
        super().__init__(identity,label,parents, children)
