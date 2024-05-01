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
        self.is_well_formed()
    
    
    def is_well_formed(self):
        """
            Checks if the boolean circuit is well-formed
        """
        if super().is_acyclic():
            for key,node in self.nodes.items():
                if (node.get_label() == "" or node.get_label() == "1" or node.get_label() == "0") and node.indegree() > 1 : 
                        return False
                elif node.get_label() != "" and node.outdegree() > 1 :
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
        circuit = bool_circ(open_digraph([],[],[]))
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
        
        return circuit,list(variables.keys())
    
    @classmethod
    def random_circ_bool(cls, n, nb_inputs,nb_outputs):
        inputs = []
        outputs = []
        #etape 1
        di = open_digraph.random(n,"DAG")

        #etape 2
        for nodess in di.get_nodes():
            if len(nodess.get_parents())==0:
                    inp_id = di.add_node("",{},{nodess.get_id():1})
                    inputs.append(inp_id)
            elif len(nodess.get_children()) == 0:
                    out_id = di.add_node("",{nodess.get_id():1},{})
                    outputs.append(out_id)
        
        #etape 2 bis
        not_out_nor_inp = [id for id in di.get_node_ids()]-di.get_inputs_ids()-di.get_outputs_ids()
        random.shuffle(not_out_nor_inp)
        random.shuffle(inputs)
        random.shuffle(outputs)
        while(len(inputs)!=nb_inputs):
            if(len(inputs)< nb_inputs):
                id = not_out_nor_inp.pop(0)
                new_inp_id = id.add_node("",{},{id:1})
                not_out_nor_inp.append(id)
                inputs.append(new_inp_id)
            else:
                inp1 = inputs.pop(0)
                inp2 = inputs.pop(0)
                new_inp_id = id.add_node("",{},{inp1:1,inp2:1})
                inputs.append(new_inp_id)
                not_out_nor_inp.append(inp1)
                not_out_nor_inp.append(inp2)

        while(len(outputs)!=nb_outputs):
            if(len(outputs)< nb_outputs):
                id = not_out_nor_inp.pop(0)
                new_out_id = id.add_node("",{id:1},{})
                not_out_nor_inp.append(id)
                outputs.append(new_out_id)
            else:
                out1 = outputs.pop(0)
                out2 = outputs.pop(0)
                new_out_id = id.add_node("",{out1:1,out2:1},{})
                outputs.append(new_out_id)
                not_out_nor_inp.append(out1)
                not_out_nor_inp.append(out2)
        #etape 3
        for nodess in di.get_nodes():
            if len(nodess.get_parents()) ==1 and len(nodess.get_children()) == 1:
                nodess.set_label("~")
            elif len(nodess.get_parents()) >1 and len(nodess.get_children()) == 1:
                nodess.set_label(random.choice(["|","^","&"]))
            elif len(nodess.get_parents()) >1 and len(nodess.get_children()) > 1:
                bin_node_id = di.add_node(random.choice(["|","^","&"]),nodess.get_parents(),{})
                cop_node_id = di.add_node("",{},nodess.get_children())
                di.add_edge(bin_node_id,cop_node_id)

        return cls(di)
    
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
            return circuit,carry_in,carry_out
        else:
            adder_1,carry_in1,carry_out1 = cls.adder_helper(n-1)
            adder_2,carry_in2,carry_out2 = cls.adder_helper(n-1)
            n = adder_1.iparallel(adder_2)
            adder_1.add_edge(carry_out1+n,carry_in2)
            return adder_1,carry_in1+n,carry_out2
    
    @classmethod
    def adder(cls,n):
        add,cin,cout = cls.adder_helper(n)
        return add

    @classmethod
    def half_adder(cls,n):
        add,cin,cout = cls.adder_helper(n)
        add.get_node_by_id(cin).set_label("0")
        return add

#g, var = bool_circ.parse_parentheses("((x0)&((x1)&(x2)))|((x1)&(~(x2)))","((x0)&(~(x1)))|(x2)")
#g2 , var2 = bool_circ.parse_parentheses("((x0)&(x1)&(x2))|((x1)&(~(x2)))")
#print(var2)
#g2.display_graph()
# g = bool_circ.adder(1)
# g.display_graph()