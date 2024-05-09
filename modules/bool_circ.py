import os
import sys
sys.path[0] = os.path.abspath(os.path.join(sys.path[0], '..'))
import random
from modules.open_digraph import *

class bool_circ(open_digraph):
    
    ###Constructor
    
    def __init__(self, g):
        g.assert_is_well_formed()
        super().__init__(g.get_inputs_ids().copy(), g.get_outputs_ids().copy(), [])
        self.nodes = g.get_id_node_map().copy()
        assert self.is_well_formed()
    
    
    def is_well_formed(self):
        """
            Checks if the boolean circuit is well-formed
        """
        if super().is_acyclic():
            for key,node in self.nodes.items():
                if node.get_label() not in "&|^10~" and node.get_label() != "":
                    return False
                elif (node.get_label() == "" or node.get_label() == "1" or node.get_label() == "0") and node.indegree() > 1 : 
                    return False
                elif (node.get_label() == "&" or node.get_label() == "^" or node.get_label() == "|" or node.get_label() == "1" or node.get_label() == "0") and node.outdegree() > 1:
                    return False
                elif node.get_label() == "~" and (node.outdegree() != 1 or node.indegree()!= 1):
                    return False
                
                
            return True
        return False
    
    def insert_node(self, boolean_circ_node,parents,children):
        """
            Adds a node to the graph
            
            Parameters:
            ----------
            
            boolean_circ_node (node) : a sub-class of node 
            
            Output: (inplace)
            -------
            The graph with the node added to it
        """
        p_ids = list(parents.keys())
        c_ids = list(children.keys())
        r = p_ids + c_ids
        assert r==[] or all(elem in self.nodes.keys() for elem in r)
        self.nodes[boolean_circ_node.get_id()] = boolean_circ_node
        
        
        #Adding the edges from parents and to children
        p = [(par , boolean_circ_node.get_id()) for par in p_ids]
        c = [(boolean_circ_node.get_id(), chi) for chi in c_ids]
        total=p+c
        mult = list(parents.values()) + list(children.values())
        self.add_edges(total,[])
        
    
    
    def add_copy_node(self,parents={},children={},new_ID = None):
        if new_ID == None:
            new_ID = self.new_id()
        self.insert_node(copy_node(new_ID ,{},{}),parents,children)
        return new_ID
    
    def add_and_node(self,parents={},children={},new_ID = None):
        if new_ID == None:
            new_ID = self.new_id()
        self.insert_node(and_node(new_ID,{}, {}),parents,children)
        return new_ID
    
    def add_or_node(self,parents={},children={},new_ID = None):
        if new_ID == None:
            new_ID = self.new_id()
        self.insert_node(or_node(new_ID,{},{}),parents,children)
        return new_ID
    
    def add_not_node(self,parents={},children={},new_ID = None):
        if new_ID == None:
            new_ID = self.new_id()
        self.insert_node(not_node(new_ID,{} ,{}),parents,children)
        return new_ID
    
    def add_xor_node(self,parents={},children={},new_ID = None):
        if new_ID == None:
            new_ID = self.new_id()
        self.insert_node(xor_node(new_ID,{} , {}),parents,children)
        return new_ID
    
    def add_constant_node(self,inp,parents={},children={},new_ID = None):
        if new_ID == None:
            new_ID = self.new_id()
        self.insert_node(constant_node(new_ID,inp,{} , {}),parents,children)
        return new_ID
    
    
    def convert_node(self,node):
        """
        Converts node to the appropriate boolean circuit component according to its current label
        """
        label = node.get_label()
        if label == "":
            new_node = circuit_node.from_node(node)
        elif label == "&":
            new_node = circuit_node.from_node(node)
        elif label == "|":
            new_node = circuit_node.from_node(node)
        elif label == "^":
            new_node = circuit_node.from_node(node)
        elif label == "~":
            new_node = circuit_node.from_node(node)
        elif label == "1" or label == "0":
            new_node = circuit_node.from_node(node)
        
        parents = node.get_parents().copy()
        children = node.get_children().copy()
        self.remove_node_by_id(node.get_id())
        self.insert_node(new_node, parents, children)
    
    
    
    @classmethod
    def identity(cls,n):
        return cls.perturbe_bit(n,[-1])
    
    @classmethod
    def parse_parentheses(cls,*args):
        """
            Creates the boolean circuit that can be associated to the series of propositional formulas given
            
            Parameters:
            -----------
            *args (str): any number of string representing a propositional formula
            
            Returns:
            --------
            
            A boolean circuit where each output is the output of one formula that is given and the list labels given to every variable
        """
        
        circuit = bool_circ(open_digraph.empty())
        variables = {}
        for arg in args:
            first_node = circuit.add_node()
            circuit.add_output_node(first_node)
            current_node = circuit.get_node_by_id(first_node)
            s2 = ""
            for char in arg:
                if char == "(":
                    label = current_node.get_label()
                    if label == "":
                        current_node.set_label(label+s2)
                    parent_node = circuit.add_node()
                    circuit.add_edge(parent_node,current_node.get_id())
                    current_node = circuit.get_node_by_id(parent_node)
                    s2 = ""
                elif char == ")":
                    current_node.set_label(current_node.get_label()+s2)
                    if s2 != "" and s2 not in variables:
                        variables[s2] = current_node.get_id()
                    current_node = circuit.get_node_by_id(list(current_node.get_children().keys())[0])
                    s2 = ""
                else:
                    s2 += char
                    
                
        
        #Creates appropriate inputs above the copy nodes
        for id in variables.values():
            inp = circuit.add_input_node(id)
            
        
        
        nodes_dict = circuit.get_id_node_map().copy()
        for node_id,n in nodes_dict.items():
            if n.get_label() in variables:
                circuit.merge_nodes(variables[n.get_label()],node_id)
                circuit.get_node_by_id(variables[n.get_label()]).set_label("")
                

        nodes = (circuit.get_id_node_map().copy()).values()
        for node in nodes:
            circuit.convert_node(node)  
            
        
        assert circuit.is_well_formed() 
        return circuit,list(variables.keys())
    
    @classmethod
    def random_circ_bool(cls, n, nb_inputs,nb_outputs):
        #etape 1
        di = cls.random(n,form="DAG")

        #etape 2
        d = list(di.get_nodes()).copy()
        for nodess in d:
            if len(nodess.get_parents())==0:
                    inp_id = di.add_node({},{nodess.get_id():1})
                    di.add_input_id(inp_id)
            if len(nodess.get_children()) == 0:
                    out_id = di.add_node({nodess.get_id():1},{})
                    di.add_output_id(out_id)
        #etape 2 bis
        not_out_nor_inp = [id for id in di.get_node_ids() if ((id not in di.get_inputs_ids()) and (id not in di.get_outputs_ids()))]
        random.shuffle(not_out_nor_inp)
        random.shuffle(di.get_inputs_ids())
        random.shuffle(di.get_outputs_ids())
        while(len(di.get_inputs_ids())!=nb_inputs):
            if(len(di.get_inputs_ids())< nb_inputs):
                id = not_out_nor_inp.pop(0)
                new_inp_id = di.add_node({},{id:1})
                not_out_nor_inp.append(id)
                di.add_input_id(new_inp_id)
            else:
                inp1 = di.get_inputs_ids().pop(0)
                inp2 = di.get_inputs_ids().pop(0)
                new_inp_id = di.add_copy_node({},{inp1:1,inp2:1})
                di.add_input_id(new_inp_id)
                not_out_nor_inp.append(inp1)
                not_out_nor_inp.append(inp2)

        while(len(di.get_outputs_ids())!=nb_outputs):
                if(len(di.get_outputs_ids())< nb_outputs):
                    id = not_out_nor_inp.pop(0)
                    new_out_id = di.add_copy_node({id:1},{})
                    not_out_nor_inp.append(id)
                    di.add_output_id(new_out_id)
                else:
                    out1 = di.get_outputs_ids().pop(0)
                    out2 = di.get_outputs_ids().pop(0)
                    new_out_id = di.add_node("",{out1:1,out2:1},{})
                    di.add_output_id(new_out_id)
                    not_out_nor_inp.append(out1)
                    not_out_nor_inp.append(out2)
        #etape 3

        d = list(di.get_nodes()).copy()
        for nnodes in d:
            if len(nnodes.get_parents()) ==1 and len(nnodes.get_children()) == 1:
                nnodes.set_label("~")
            elif len(nnodes.get_parents()) >1 and len(nnodes.get_children()) == 1:
                nnodes.set_label(random.choice(["|","^","&"]))
            elif len(nnodes.get_parents()) >1 and len(nnodes.get_children()) > 1:
                bin_node_id = di.add_node(random.choice(["|","^","&"]),{},{})
                #cop_node_id = di.add_node("",{},{})
                for i in list(nnodes.get_parents().keys()).copy():
                    di.add_edge(i,bin_node_id)
                    di.remove_edge(i,nnodes.get_id())
                di.add_edge(bin_node_id,nnodes.get_id())

        circuit = cls(di)
        return circuit
    
    @classmethod
    def adder_helper(cls,n):
        if n == 0:
            circuit = cls(open_digraph([],[],[]))
            inp1 = circuit.add_copy_node()
            inp2 = circuit.add_copy_node()
            carry_in = circuit.add_copy_node()
            cop1 =  circuit.add_copy_node({inp1:1},{})
            cop2 =  circuit.add_copy_node({inp2:1},{})
            and1 = circuit.add_and_node({cop1:1,cop2:1},{})
            nor1 = circuit.add_xor_node({cop1:1,cop2:1},{})
            cop3 = circuit.add_copy_node({nor1:1},{})
            cop4 = circuit.add_copy_node({carry_in:1},{})
            and2 = circuit.add_and_node({cop3:1,cop4:1},{})
            nor2 = circuit.add_xor_node({cop3:1,cop4:1},{})
            or1 =  circuit.add_or_node({and1:1,and2:1},{})
            carry_out =  circuit.add_copy_node({or1:1},{})
            out2 =  circuit.add_copy_node({nor2:1},{})
            circuit.set_inputs([inp1,inp2,carry_in])
            circuit.set_outputs([carry_out,out2])
            return circuit,carry_in,carry_out
        else:
            adder_1,carry_in1,carry_out1 = cls.adder_helper(n-1)
            adder_2,carry_in2,carry_out2 = cls.adder_helper(n-1)
            n = adder_1.iparallel(adder_2)
            adder_1.add_edge(carry_out1+n,carry_in2)
            adder_1.get_inputs_ids().remove(carry_in2)
            adder_1.get_outputs_ids().remove(carry_out1+n)
            return adder_1,carry_in1+n,carry_out2
    
    @classmethod
    def adder(cls,n):
        add,cin,cout = cls.adder_helper(n)
        add.get_inputs_ids().sort()
        add.get_outputs_ids().sort()
        return add

    @classmethod
    def half_adder(cls,n):
        add,cin,cout = cls.adder_helper(n)
        add.get_node_by_id(cin).set_label("0")
        return add
    
    @classmethod
    def create_registre(cls,acc ,size=8):
        bin_string = convert_to_binary_string(acc,size=size)
        registre = bool_circ(open_digraph.empty())
        for i in range(size):
            node_inp = registre.add_constant_node(bin_string[i],{},{})
            registre.add_input_id(node_inp)
            registre.add_output_node(node_inp)
        assert registre.is_well_formed()
        return registre
    
    
    def copy_gate(self,copy_node_id, input_node_id):
        inp = self.get_node_by_id(input_node_id).get_label()
        assert inp == "1" or inp == "0"
        children = list(self.get_node_by_id(copy_node_id).get_children())
        self.remove_node_by_id(copy_node_id)
        self.remove_node_by_id(input_node_id)
        res = []
        for child in children:
            copied_input = self.add_node(inp)
            self.add_edge(copied_input , child)
            res.append(copied_input)
        return res
    
    def not_gate(self, not_node_id,input_node_id):
        inp = self.get_node_by_id(input_node_id).get_label()
        assert inp == "1" or inp == "0"
        not_node = self.get_node_by_id(not_node_id)
        self.remove_node_by_id(input_node_id)
        if inp == "1":
            not_node.set_label("0")
        else:
            not_node.set_label("1")
        
        return [not_node_id]
            
    def and_gate(self, and_node_id,input_node_id):
        inp = self.get_node_by_id(input_node_id).get_label()
        assert inp == "1" or inp == "0"
        
        self.remove_node_by_id(input_node_id)
        and_node = self.get_node_by_id(and_node_id)
        if inp == "0":
            and_node.set_label("0")
            parents = list(and_node.get_parents()).copy()
            for p in parents:
                self.remove_parallel_edges(p,and_node_id)
                nullifier = self.add_copy_node()
                self.add_edge(p,nullifier)
            return [and_node_id]
        
        if len(and_node.get_parents())==0:
            self.neutral_element(and_node_id)
            return [and_node_id]

        return []
    
    def or_gate(self, or_node_id,input_node_id):
        inp = self.get_node_by_id(input_node_id).get_label()
        assert inp == "1" or inp == "0"
        
        
        self.remove_node_by_id(input_node_id)
        or_node = self.get_node_by_id(or_node_id)
        if inp == "1":
            or_node.set_label("1")
            parents = list(or_node.get_parents()).copy()
            for p in parents:
                self.remove_parallel_edges(p,or_node_id)
                nullifier = self.add_copy_node()
                self.add_edge(p,nullifier)
            return [or_node_id]
        
        if len(or_node.get_parents())==0:
            self.neutral_element(or_node_id)
            return [or_node_id]

        return []
        
    
    def xor_gate(self, xor_node_id,input_node_id):
        inp = self.get_node_by_id(input_node_id).get_label()
        assert inp == "1" or inp == "0"
        
        self.remove_node_by_id(input_node_id)
        xor_node = self.get_node_by_id(xor_node_id)
        new_xor = None
        if inp == "1":
            xor_node.set_label("~")
            
            parents = list(xor_node.get_parents()).copy()
            
            new_xor = self.add_node(label="^")
            self.add_edge(new_xor,xor_node_id)
            for p in parents:
                self.remove_parallel_edges(p,xor_node_id)
                self.add_edge(p,new_xor)
        
        if len(xor_node.get_parents())==0 and xor_node.get_label()=="^":
            self.neutral_element(xor_node_id)
            return [xor_node_id]
        elif new_xor != None and len(self.get_node_by_id(new_xor).get_parents())==0:
            self.neutral_element(new_xor)
            return [new_xor]

        return []
        
    def neutral_element(self, binary_gate):
        node = self.get_node_by_id(binary_gate)
        if node.is_or() or node.is_xor():
            node.set_label("0")
            self.convert_node(node)
        elif node.is_and():
            node.set_label("1")
            self.convert_node(node)
        

    def evaluate(self):
        tmp = []
        #taking care of neutral gates at the beginning which dont result of transformations
        copy = (self.get_id_node_map().copy()).values()
        for node in copy:
            if (node.is_or() or node.is_not() or node.is_xor() or node.is_and()) and len(node.get_parents())==0 :
                self.neutral_element(node.get_id())
                tmp.append(node.get_id())

        calculated = list(self.get_inputs_ids()) + tmp
        outputs = list(self.get_outputs_ids())
        while outputs != [] and calculated != []:
            node_id = calculated[0]
            calculated.remove(node_id)
            node = self.get_node_by_id(node_id)
            calculated += node.eval(self,outputs)
        
        #cleanning up the circuit
        for c in calculated:
            self.remove_node_by_id(c)

        res = ""
        (self.get_outputs_ids()).sort()
        for out in (self.get_outputs_ids()):
            res+= self.get_node_by_id(out).get_label()
        return int(res , 2)
    
    @classmethod
    def encodeur_4bits(cls):
        circuit = bool_circ(open_digraph.empty())
        copies = [circuit.add_copy_node() for i in range(4)]
        xors = [circuit.add_xor_node() for i in range(3)]
        circuit.add_edges([(copies[0],xors[0]),(copies[0],xors[1]),(copies[1],xors[0]),
                        (copies[1],xors[2]),(copies[2],xors[1]),(copies[2],xors[2]),
                        (copies[3],xors[0]), (copies[3],xors[1]), (copies[3],xors[2])]
                        ,[])
        for i in range(4):
            circuit.add_input_node(copies[i])
        
        circuit.add_output_node(xors[0])
        circuit.add_output_node(xors[1])
        circuit.add_output_node(copies[0])
        circuit.add_output_node(xors[2])
        
        for i in range(1,4):
            circuit.add_output_node(copies[i])
        
        return circuit
    
    @classmethod
    def decodeur_7bits(cls):
        circuit = bool_circ(open_digraph.empty())
        copies = [circuit.add_copy_node() for i in range(7)]
        xors = [circuit.add_xor_node() for i in range(7)]
        nots = [circuit.add_not_node() for i in range(3)]
        ands = [circuit.add_and_node() for i in range(4)]
        circuit.add_edges([(copies[0],xors[0]),(copies[0],xors[1]),(copies[1],xors[0]),(copies[1],xors[2]),(copies[2],xors[1]),(copies[2],xors[2]), (copies[3],xors[0]), (copies[3],xors[1]), (copies[3],xors[2])]+
                        [(xors[0],copies[4]),(xors[1],copies[5]),(xors[2],copies[6])]
                        +[(copies[4],ands[0]),(copies[4],ands[1]),(copies[4],ands[3])]
                        + [(copies[5],ands[0]),(copies[5],ands[2]),(copies[5],ands[3])]
                        + [(copies[6],ands[1]),(copies[6],ands[2]),(copies[6],ands[3])]
                        + [(copies[4],nots[2]),(copies[5],nots[1]),(copies[6],nots[0])]
                        + [(nots[i],ands[i]) for i in range(3)]
                        + [(copies[i],xors[i+3]) for i in range(4)]
                        + [(ands[i],xors[i+3]) for i in range(4)],[])
        for i in range(3,7):
            circuit.add_output_node(xors[i])
        circuit.add_input_node(xors[0])
        circuit.add_input_node(xors[1])
        circuit.add_input_node(copies[0])
        circuit.add_input_node(xors[2])
        for i in range(1,4):
            circuit.add_input_node(copies[i])
        
        return circuit
    
    def assoc_xor(self , parent_xor,child_xor):
        parent_node = self.get_node_by_id(parent_xor)
        child_node = self.get_node_by_id(child_xor)
        assert parent_node.get_label() == "^" and child_node.get_label() == "^"
        
        parents_of_parent = list(parent_node.get_parents())
        self.remove_node_by_id(parent_xor)
        
        for p in parents_of_parent:
            self.add_edge(p,child_xor)
        return True
    
    def assoc_and(self , parent_and,child_and):
        parent_node = self.get_node_by_id(parent_and)
        child_node = self.get_node_by_id(child_and)
        assert parent_node.get_label() == "&" and child_node.get_label() == "&"
        
        parents_of_parent = list(parent_node.get_parents())
        self.remove_node(parent_and)
        
        for p in parents_of_parent:
            self.add_edge(p,child_and)
        return True
            
    def assoc_or(self , parent_or,child_or):
        parent_node = self.get_node_by_id(parent_or)
        child_node = self.get_node_by_id(child_or)
        assert parent_node.get_label() == "|" and child_node.get_label() == "|"
        
        parents_of_parent = list(parent_node.get_parents())
        self.remove_node(parent_or)
        
        for p in parents_of_parent:
            self.add_edge(p,child_or)
        return True
    
    def assoc_copy(self, parent_copy,child_copy):
        parent_node = self.get_node_by_id(parent_copy)
        child_node = self.get_node_by_id(child_copy)
        assert parent_node.get_label() == "" and child_node.get_label() == ""
        if child_copy in self.get_outputs_ids() or parent_copy in self.get_inputs_ids():
            return False
        
        children_of_child = list(child_node.get_children())
        self.remove_node_by_id(child_copy)
        
        for c in children_of_child:
            self.add_edge(parent_copy , c)
        return True
            
    def involution_xor(self, xor_id , copy_id):
        xor_node = self.get_node_by_id(xor_id)
        copy_node = self.get_node_by_id(copy_id)
        assert xor_node.get_label() == "^" and copy_node.get_label() == ""
        
        nb_arretes = (copy_node.get_children())[xor_id]
        if nb_arretes >=2:
            if nb_arretes % 2 == 0:
                self.remove_parallel_edges(copy_id, xor_id)
            else:
                self.remove_parallel_edges(copy_id, xor_id)
                self.add_edge(copy_id,xor_id)
            return True
        else:
            return False
    
    def effacement(self , op_id,child_id):
        if child_id in self.get_outputs_ids():
            return False
        parents = list(self.get_node_by_id(op_id).get_parents())
        self.remove_node_by_id(op_id)
        self.remove_node_by_id(child_id)
        
        for p in parents:
            nullifier = self.add_copy_node()
            self.add_edge(p,nullifier)
            
        return True
    
    def not_xor(self , not_id, xor_id):
        xor_node = self.get_node_by_id(xor_id)
        not_node = self.get_node_by_id(not_id)
        assert xor_node.get_label() == "^" and not_node.get_label() == "~"

        parent_of_not = list(not_node.get_parents())[0]
        child_of_xor = list(xor_node.get_children())[0]
        
        self.remove_parallel_edges(xor_id,child_of_xor)
        self.remove_parallel_edges(parent_of_not,not_id)
        self.remove_parallel_edges(not_id,xor_id)
        self.add_edge(xor_id, not_id)
        self.add_edge(not_id , child_of_xor)
        self.add_edge(parent_of_not,xor_id)
        return True
    
    def not_copy(self,not_id,copy_id):
        copy_node = self.get_node_by_id(copy_id)
        not_node = self.get_node_by_id(not_id)
        assert copy_node.get_label() == "" and not_node.get_label() == "~"
        if copy_id in self.get_outputs_ids():
            return False
        
        parent_of_not = list(not_node.get_parents())[0]
        self.remove_node_by_id(not_id)
        self.add_edge(parent_of_not , copy_id)
        
        
        children_of_copy = list(self.get_node_by_id(copy_id).get_children())
        for c in children_of_copy:
            new_not = self.add_not_node()
            self.remove_edge(copy_id,c)
            self.add_edge(copy_id,new_not)
            self.add_edge(new_not,c)
        return True
    
    def involution_not(self, not1, not2):
        node1 = self.get_node_by_id(not1)
        node2 = self.get_node_by_id(not2)
        assert node1.get_label() == "~" and node2.get_label() == "~"
        
        parent_of_node1 = list(node1.get_parents())[0]
        child_of_node2 = list(node2.get_children())[0]
        
        self.remove_node_by_id(not1)
        self.remove_node_by_id(not2)
        self.add_edge(parent_of_node1,child_of_node2)
        return True

        
        
    
    def transform_circuit(self):
        
        def transform_once(self,nodes):
            flag = False
            for node_id in nodes:
                r = False
                if node_id in self.get_inputs_ids() or node_id in self.get_outputs_ids() or node_id not in self.get_node_ids():
                    continue
                node = self.get_node_by_id(node_id)
                label = node.get_label()
                first_child = (self.get_node_by_id((list(node.get_children())[0])))
                if first_child.is_copy() and len(first_child.get_children()) == 0:
                        r=self.effacement(node_id ,list(node.get_children())[0] )
                else:
                    node.transform(self)
                if r:
                    flag = True
            return flag
        
        cont = True
        while cont:
            nodes = list(self.get_node_ids())
            cont = transform_once(self, nodes)
    
    def calculate(self):
        self.transform_circuit()
        return self.evaluate()
        
    @classmethod
    def perturbe_bit(cls,n,list_pos):
        """
            introduit une erreur aux bits de positions donnée
        """
        circuit = bool_circ(open_digraph.empty())
        for i in range(n):
            inp = circuit.add_copy_node()
            circuit.add_input_id(inp)
            out = circuit.add_copy_node()
            circuit.add_output_id(out)
            if i in list_pos:
                erreur = circuit.add_not_node()
                circuit.add_edge(inp,erreur)
                circuit.add_edge(erreur , out)
            else:
                circuit.add_edge(inp,out)
                
        return circuit
    
    
    @classmethod
    def CL_4bit(cls):
        return bool_circ.parse_parentheses("((g3)^((p3)&(g2))^((p3)&(p2)&(g1))^((p3)&(p2)&(p1)&(g0))^((p3)&(p2)&(p1)&(p0)&(c0)))",
                                        "((g2)^((p2)&(g1))^((p2)&(p1)&(g0))^((p2)&(p1)&(p0)&(c0)))",
                                        "((g1)^((p1)&(g0))^((p1)&(p0)&(c0)))" , 
                                        "((g0)^((p0)&(c0)))")
    
    
    @classmethod 
    def CLA_4bit(cls):
        circuit ,inps = bool_circ.CL_4bit()
        dict_inputs = {inps[i]:list(circuit.get_inputs_ids())[i] for i in range(len(inps))}
        
        #circuit.display_graph(verbose=True)
        copies  = [circuit.add_copy_node() for i in range(13)]
        ands = [circuit.add_and_node() for i in range(4)]
        xors = [circuit.add_xor_node() for i in range(8)]
        
        #links for gi pi
        circuit.add_edges(
            [(copies[i],xors[i]) for i in range(4)] + [(copies[i+4],xors[i]) for i in range(4)] +
            [(copies[i],ands[i]) for i in range(4)] + [(copies[i+4],ands[i]) for i in range(4)] +
            [(xors[i],copies[9+i]) for i in range(4)],[]
        )
        
        
        circuit.add_edge(copies[8] , dict_inputs["c0"])
        for i in range(0,4):
            circuit.add_edge(copies[9+i],dict_inputs["p"+str(i)])
            circuit.add_edge(ands[i],dict_inputs["g"+str(i)])
        
        
        for i in range(4):
            circuit.add_edge(copies[9+i],xors[4+i])
        circuit.add_edge(copies[8], xors[4])
        
        circuit.get_outputs_ids().sort()
        for i in range(1,len(circuit.get_outputs_ids())):
            circuit.add_edge(list(circuit.get_outputs_ids())[i] , xors[8-i])
        
        c_n1 = list(circuit.get_outputs_ids())[0]
        circuit.set_outputs([])
        circuit.set_inputs([])
        
        circuit.add_output_node(c_n1)
        for i in range(3,-1,-1):
            circuit.add_output_node(xors[4+i])
        
        circuit.add_input_node(copies[8])
        for i in range(8):
            circuit.add_input_node(copies[i])
        
        return circuit
    
    @classmethod
    def CLA_helper(cls,n):
        if (n==0):
            g = cls.CLA_4bit()
            return 65,g,70
        else :
            cout1,CLA1,cin1 = cls.CLA_helper(0)
            cout2,CLA2,cin2 = cls.CLA_helper(n-1)
            n = CLA1.iparallel(CLA2)
            CLA1.add_edge(cout1+n,cin2)
            CLA1.get_inputs_ids().remove(cin2)
            CLA1.get_outputs_ids().remove(cout1+n)
            return cout2,CLA1,cin1+n
        
    @classmethod
    def CLA_adder(cls,n):
        cout,cla,cin = cls.CLA_helper(n)
        return cla

def convert_to_binary_string(acc , size=8):
    bin_string = bin(acc)[2:]
    if len(bin_string) <= size:
        bin_string = (size-len(bin_string))*"0" + bin_string   #padding
    else:
        bin_string = bin_string[-1:-size-1:-1]  #bufferOverflow
    return bin_string

def find_bigger_2_pow(n):
    acc = 1
    i = 0
    while acc < n:
        acc *=2
        i+=1
    return acc,i

def add_registre_CLA(a,b, size=8):
    """
        b is added to a
    """
    a_str = convert_to_binary_string(a,size=size)
    b_str = convert_to_binary_string(b,size=size)
    #on doit ajouter les bits 4 par 4 coz of how cla is coded
    quotient, remainder = divmod(size, 4)
    res = ""
    for i in range(quotient-1,-1,-1):
        for c in [a_str,b_str]:
            for j in range(3,-1,-1):
                res += c[i*4+j]
    for c in [a_str,b_str]:
        for i in range(size-1,size-remainder-1,-1):
            res+= c[i]
    res = "0"+res  # adding 0 carry bit"
    g = bool_circ.CLA_adder(quotient-1)
    registre = bool_circ.create_registre(int(res , 2),size=(quotient)*8+1)
    g.icompose(registre)
    return g.calculate()
    
def add_CLA(a,b):
    """
        b is added to a without needing to specify size by CLA method
    """
    size = 0
    quotient,mod = divmod(max(a.bit_length(),b.bit_length()),4)
    size = (quotient+1) * 4
    return add_registre_CLA(a,b,size = size)

def add_registre_naive(a,b, size=8):
    """
        b is added to a
    """
    a_str = convert_to_binary_string(a,size=size)
    b_str = convert_to_binary_string(b,size=size)
    res = ""
    for i in range(size):
        res +=   b_str[i]+a_str[i]
    res = res + "0" # adding 0 carry bit
    reg_size , n = find_bigger_2_pow(size)
    g = bool_circ.adder(n)
    registre = bool_circ.create_registre(int(res , 2),size=2*reg_size+1)
    g.icompose(registre)
    return g.calculate()

def add_naive(a,b):
    """
        b is added to a without needing to specify size
    """
    size = max(a.bit_length(),b.bit_length())
    return add_registre_naive(a,b,size = size)


def check_invarients():
    enc = bool_circ.encodeur_4bits()
    dec = bool_circ.decodeur_7bits()
    
    for i in range(-1,4): #-1 -> no error is introduced
        noise = bool_circ.perturbe_bit(7,[i]) 
        g = bool_circ(noise.compose(enc))
        g2 = bool_circ(dec.compose(g))
        
        for i in range(0,16):
            reg = bool_circ.create_registre(i,size=4)
            g3 = bool_circ(g2.compose(reg))
            assert (i==g3.calculate())
    
    print("Hamming property verfied when introducing one error at most.")
    
    mistakes = 0
    for i in range(4): 
        for j in range(i+1,4):
            noise = bool_circ.perturbe_bit(7,[i,j]) 
            g = bool_circ(noise.compose(enc))
            g2 = bool_circ(dec.compose(g))
            for k in range(0,16):
                reg = bool_circ.create_registre(k,size=4)
                g3 = bool_circ(g2.compose(reg))
                mistakes += (i!=g3.calculate())
    print(f"Number of time that the original signal couldn't be retreived when introducing 2 errors: {mistakes} out of {6*16} attempts.")
    
    
    




#g, var = bool_circ.parse_parentheses("((x0)&((x1)&(x2)))|((x1)&(~(x2)))","((x0)&(~(x1)))|(x2)")

# g2 , var2 = bool_circ.parse_parentheses("((x0)&(x1)&(x2))|((x1)&(~(x2)))")
# #print(var2)
# registre = bool_circ.create_registre(7,size=3)

# g2.icompose(registre)

# g2.evaluate()

# g2.display_graph()


# g = bool_circ.adder(1)

# registre = bool_circ.create_registre(8,size=5)
# g.icompose(registre)
#g.display_graph(verbose=True)

#print(add(120,23459,size=16))
#g = bool_circ.decodeur_7bits()
#g.display_graph()


#g = bool_circ.create_registre(7,size=2)
#g.display_graph()


#c = bool_circ.random_circ_bool(6,14,12)
# c2 = open_digraph.random(7,form="DAG")
#c.display_graph()
#check_invarients()

#bool_circ.decodeur_7bits().display_graph(verbose=True)


# g = bool_circ.CL_4bit()[0]

# reg = bool_circ.create_registre(int("100000000" ,2) , size=9)
# g.icompose(reg)
# g.display_graph(verbose="True")

#print(g.evaluate())
#g = bool_circ.CLA_adder(5)
#g.iparallel(bool_circ.CLA_adder(0))
#print(len(g.get_inputs_ids()))

#print(g.get_outputs_ids())
#print(g.max_id())
#g.display_graph(verbose = True)

# for i in range(16):
#     for j in range(16):
#         print( f"{i} + {j} =", add_registre(i,j,size=4) )



#(bool_circ.CL_4bit()[0]).display_graph()
# print(add_registre_CLA(0,16,size= 8))
# i = 0
# res = True
# while i <2000 and res:
#     print(i)
#     a = random.randint(0,1234567865)
#     b = random.randint(0,1234567432)
#     i+=1
#     res = (add_CLA(a,b)== 
#         add_naive(a,b) == a+b)
# print(res and (i==2000) )


bool_circ.random_circ_bool(20,5,3).display_graph()

