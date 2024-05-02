import os
import sys
sys.path[0] = os.path.abspath(os.path.join(sys.path[0], '..'))
import random
from modules.open_digraph import open_digraph

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
            circuit.add_input_node(id)
        
        nodes_dict = circuit.get_id_node_map().copy()
        for node_id,n in nodes_dict.items():
            if n.get_label() in variables:
                circuit.merge_nodes(variables[n.get_label()],node_id)
                circuit.get_node_by_id(variables[n.get_label()]).set_label("")
        
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
                    inp_id = di.add_node("",{},{nodess.get_id():1})
                    di.add_input_id(inp_id)
            if len(nodess.get_children()) == 0:
                    out_id = di.add_node("",{nodess.get_id():1},{})
                    di.add_output_id(out_id)
        #etape 2 bis
        not_out_nor_inp = [id for id in di.get_node_ids() if ((id not in di.get_inputs_ids()) and (id not in di.get_outputs_ids()))]
        random.shuffle(not_out_nor_inp)
        random.shuffle(di.get_inputs_ids())
        random.shuffle(di.get_outputs_ids())
        while(len(di.get_inputs_ids())!=nb_inputs):
            if(len(di.get_inputs_ids())< nb_inputs):
                id = not_out_nor_inp.pop(0)
                new_inp_id = di.add_node("",{},{id:1})
                not_out_nor_inp.append(id)
                di.add_input_id(new_inp_id)
            else:
                inp1 = di.get_inputs_ids().pop(0)
                inp2 = di.get_inputs_ids().pop(0)
                new_inp_id = di.add_node("",{},{inp1:1,inp2:1})
                di.add_input_id(new_inp_id)
                not_out_nor_inp.append(inp1)
                not_out_nor_inp.append(inp2)

        while(len(di.get_outputs_ids())!=nb_outputs):
                if(len(di.get_outputs_ids())< nb_outputs):
                    id = not_out_nor_inp.pop(0)
                    new_out_id = di.add_node("",{id:1},{})
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
        assert circuit.is_well_formed()
        return circuit
    
    @classmethod
    def adder_helper(cls,n):
        if n == 0:
            circuit = cls(open_digraph([],[],[]))
            inp1 = circuit.add_node("",{},{})
            inp2 = circuit.add_node("",{},{})
            carry_in = circuit.add_node("",{},{})
            cop1 =  circuit.add_node("",{inp1:1},{})
            cop2 =  circuit.add_node("",{inp2:1},{})
            and1 = circuit.add_node("&",{cop1:1,cop2:1},{})
            nor1 = circuit.add_node("^",{cop1:1,cop2:1},{})
            cop3 = circuit.add_node("",{nor1:1},{})
            cop4 = circuit.add_node("",{carry_in:1},{})
            and2 = circuit.add_node("&",{cop3:1,cop4:1},{})
            nor2 = circuit.add_node("^",{cop3:1,cop4:1},{})
            or1 =  circuit.add_node("|",{and1:1,and2:1},{})
            carry_out =  circuit.add_node("",{or1:1},{})
            out2 =  circuit.add_node("",{nor2:1},{})
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
            node_inp = registre.add_node(label=bin_string[i])
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
            copied_input = self.add_node(label=inp)
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
                nullifier = self.add_node()
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
                nullifier = self.add_node()
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
        label = node.get_label()
        if label == "|" or label == "^":
            node.set_label("0")
        elif label == "&":
            node.set_label("1")
        

    def evaluate(self):
        #taking care of neutral gates at the beginning which dont result of transformations
        for node in self.get_nodes():
            if (node.get_label() == "|" or node.get_label() == "~" or node.get_label() == "^" or node.get_label() == "&") and len(node.get_parents())==0 :
                self.neutral_element(node.get_id())
        
        calculated = list(self.get_inputs_ids())
        outputs = list(self.get_outputs_ids())
        while outputs != [] and calculated != []:
            node_id = calculated[0]
            calculated.remove(node_id)
                
            node = self.get_node_by_id(node_id)
            
            child = list(node.get_children())[0]
            
            if child in outputs:
                self.get_node_by_id(child).set_label(node.get_label())
                self.remove_node_by_id(node_id)
                outputs.remove(child)

            else:
                label = self.get_node_by_id(child).get_label()
                if label == "&":
                    res = self.and_gate(child,node_id)
                elif label == "|":
                    res = self.or_gate(child,node_id)
                elif label == "^":
                    res = self.xor_gate(child,node_id)
                elif label == "~":
                    res = self.not_gate(child,node_id)
                elif label == "":
                    res = self.copy_gate(child,node_id)
                calculated += res
        #cleanning up the circuit
        for c in calculated:
            self.remove_node_by_id(c)

        res = ""
        for out in self.get_outputs_ids():
            res+= self.get_node_by_id(out).get_label()
        return int(res , 2)
    
    @classmethod
    def encodeur_4bits(cls):
        g , _ = bool_circ.parse_parentheses("((x0)^(x1)^(x2)^(x3))","((x0)^(x2)^(x3))","(x0)","((x1)^(x2)^(x3))","(x1)","(x2)","(x3)")
        return g
    
    @classmethod
    def decodeur_7bits(cls):
        xor1 = "((x0)^(x2)^(x4)^(x6))"
        xor2 = "((x1)^(x2)^(x5)^(x6))"
        xor3 = "((x3)^(x4)^(x5)^(x6))"
        
        
        previous , _ = bool_circ.parse_parentheses(f"({xor1})",f"({xor2})","(x2)",f"({xor3})","(x4)","(x5)","(x6)")
        
        g , _ = bool_circ.parse_parentheses(
            f"(((x0)&(x1)&(~(x3)))^(x2))",
            f"(((x0)&(~(x1))&(x3))^(x4))",
            f"(((~(x0))&(x1)&(x3))^(x5))",
            f"(((x1)&(x2)&(x3))^(x6))"
            )
        g.icompose(previous)
        return g


def convert_to_binary_string(acc , size=8):
    bin_string = bin(acc)[2:]
    if len(bin_string) < size:
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

def add(a,b, size=8):
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
    return g.evaluate()

    

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

print(add(120,23459,size=16))
g = bool_circ.decodeur_7bits()
g.display_graph()


#g = bool_circ.create_registre(7,size=2)
#g.display_graph()


#c = bool_circ.random_circ_bool(6,14,12)
# c2 = open_digraph.random(7,form="DAG")
#c.display_graph()