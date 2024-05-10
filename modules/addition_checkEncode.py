import os
import sys
sys.path[0] = os.path.abspath(os.path.join(sys.path[0], '..'))
from modules.adders import adders
from modules.bool_circ import *
import random 
import numpy as np

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
    a_str = bool_circ.convert_to_binary_string(a,size=size)
    b_str = bool_circ.convert_to_binary_string(b,size=size)
    #bits must be added 4 by 4
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
    g = adders.CLA_adder(quotient-1)
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
    reg_size , n = find_bigger_2_pow(size)
    a_str = bool_circ.convert_to_binary_string(a,size=reg_size)
    b_str = bool_circ.convert_to_binary_string(b,size=reg_size)
    res = ""
    for i in range(reg_size):
        res +=   b_str[i]+a_str[i]
    res = res + "0" # adding 0 carry bit
    
    g = adders.adder(n)
    registre = bool_circ.create_registre(int(res , 2),size=2*reg_size+1)
    g.icompose(registre)
    return g.calculate()

def add_registre_naive_half(a,b, size=8):
    """
        b is added to a
    """
    reg_size , n = find_bigger_2_pow(size)
    a_str = bool_circ.convert_to_binary_string(a,size=reg_size)
    b_str = bool_circ.convert_to_binary_string(b,size=reg_size)
    res = ""
    for i in range(reg_size):
        res +=   b_str[i]+a_str[i]
    res = res
    res = res[::-1]
    

    g,cin = adders.half_adder(n)
    g.get_inputs_ids().remove(cin)
    #We remove the carry bit so that it wont be affected by icompose
    registre = bool_circ.create_registre(int(res , 2),size=2*reg_size)
    n = g.icompose(registre)
    g.display_graph("test2",verbose=True)
    g.get_inputs_ids().append(cin+n) #we put him back in for evaluatio
    return g.calculate()

def add_naive(a,b):
    """
        b is added to a without needing to specify size
    """
    size = max(a.bit_length(),b.bit_length())
    return add_registre_naive(a,b,size = size)


def check_invarients():
    #Initialize our circuits
    enc = bool_circ.encodeur_4bits()
    dec = bool_circ.decodeur_7bits()
    
    for i in range(-1,4): #-1 -> no error is introduced
        noise = adders.perturbe_bit(7,[i])  
        g = bool_circ.compose(noise,enc)  #adding perturbations
        g2 = bool_circ.compose(dec,g)
        
        for i in range(0,16):
            reg = bool_circ.create_registre(i,size=4)
            g3 = bool_circ(bool_circ.compose(g2,reg))
            assert (i==g3.calculate())
    
    print("Hamming property verfied when introducing one error at most.")
    
    mistakes = 0
    for i in range(0,4): 
        for j in range(i+1,4):
            noise = bool_circ.perturbe_bit(7,[i,j]) 
            g = bool_circ.compose(noise,enc)
            g2 = bool_circ.compose(dec,g)
            for k in range(0,16):
                reg = bool_circ.create_registre(k,size=4)
                g3 = bool_circ(bool_circ.compose(g2,reg))
                mistakes += (i!=g3.calculate())
    print(f"Number of time that the original signal couldn't be retreived when introducing 2 errors: {mistakes} out of {6*16} attempts.")
    
    
def count_edges(circuit):
    """
    Counts the number of edges in a graph , with their multiplicity
    """
    s = 0
    for node in circuit.get_nodes():
        s += sum(list(node.get_children().values()))
    return s



#g, var = adders.parse_parentheses("((x0)&((x1)&(x2)))|((x1)&(~(x2)))","((x0)&(~(x1)))|(x2)")

# g2 , var2 = adders.parse_parentheses("((x0)&(x1)&(x2))|((x1)&(~(x2)))")
# #print(var2)
# registre = adders.create_registre(7,size=3)

# g2.icompose(registre)

# g2.evaluate()

# g2.display_graph()


# g = adders.adder(1)

# registre = adders.create_registre(8,size=5)
# g.icompose(registre)
#g.display_graph(verbose=True)

#print(add(120,23459,size=16))
#g = adders.decodeur_7bits()
#g.display_graph()


#g = adders.create_registre(7,size=2)
#g.display_graph()


#c = adders.random_circ_bool(6,14,12)
# c2 = open_digraph.random(7,form="DAG")
#c.display_graph()
#check_invarients()

#adders.decodeur_7bits().display_graph(verbose=True)


# g = adders.CL_4bit()[0]

# reg = adders.create_registre(int("100000000" ,2) , size=9)
# g.icompose(reg)
# g.display_graph(verbose="True")

#print(g.evaluate())
#g = adders.CLA_adder(5)
#g.iparallel(adders.CLA_adder(0))
#print(len(g.get_inputs_ids()))

#print(g.get_outputs_ids())
#print(g.max_id())
#g.display_graph(verbose = True)

for i in range(16):
    for j in range(16):
        print( f"{i} + {j} =", add_registre_naive(i,j,size=4) )



#(adders.CL_4bit()[0]).display_graph()
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



def print_stats():
    diff_nodes = 0
    diff_edges = 0
    vn = 0
    ve = 0
    number_trials = 1000

    for i in range(number_trials):
        inputs = random.choice([8,16,32,64])
        outputs = random.choice([8,16,32,64])
        node_number = inputs + outputs + random.randint(32, 128)
        circuit = bool_circ.random_circ_bool(node_number, inputs, outputs)
        node_number = len(circuit.get_nodes())
        edges_number = count_edges(circuit)
        
        circuit.transform_circuit()
        
        number_left_nodes = len(circuit.get_nodes())
        edges_left = count_edges(circuit)
        
        diff_nodes += node_number - number_left_nodes
        diff_edges += edges_number - edges_left
        
        vn += (node_number - number_left_nodes)**2
        ve += (edges_number - edges_left)**2

    moy_n = diff_nodes / number_trials
    moy_e = diff_edges / number_trials

    var_n = vn / number_trials - moy_n**2
    var_e = ve / number_trials - moy_e**2

    print(f"Average number of removed gates : {moy_n}")
    print(f"Variance : {var_n}, deviation : {np.sqrt(var_n)}")
    print(f"Average number of removed edges : {moy_e}")
    print(f"Variance : {var_e}, deviation : {np.sqrt(var_e)}")



#check_invarients()


# g = adders.half_adder(3)[0]
# # g = adders.CLA_adder(2)
# print(len(g.get_nodes()))
# print(g.depth_acyclic())
# print(len(g.get_inputs_ids()))

############################################################################
#
# depth half_adder(n) = 5*2^n+1
# number of gates half_adder(n) = 14*2^n 
# number of outputs half_adder(n) = 1 + 2^n
# number of inputs half_adder(n) = 2^(n+1) (+1 if counting the fixed 0)
#
############################################################################
#
# depth CLA_adder(n) = 11 + 9*n
# number of gates CLA_adder(n) = 79*(n+1)
# number of outputs CLA_adder(n) = 1 + 4*(n+1)
# number of inputs CLA_adder(n) = 1 + 8*(n+1)
#
############################################################################
#
# We can clearly see the advantages of each compared to the other: with the half_adder, 
# very large numbers can be added with a fairly small number n in a half_adder(n).
# For example, half_adder(10) can add 1024-bit numbers together, while this would take
# a CLA_adder(255) to do. 
# With the CLA_adder, we can add numbers faster than with half_adder, at the cost of having more
# nodes. For example, to add 32-bits integer, CLA_adder(7) does the job with a depth of 74 while
# half_adder(5) does the job with a depth of 161, more than double the depth and with medium sized integers!
#
#
############################################################################

## smallest of smallest paths between inputs and outputs of half_adder:
def shortest_path_input_output(n, half_):
    if (half_):
        g = adders.half_adder(n)[0]
    else :
        g = adders.CLA_adder(n)
    
    smallest_dist = sys.maxsize
    input_id = -1
    output_id = -1
    for i in g.get_inputs_ids():
        for j in g.get_outputs_ids():
            dist = g.shortest_path(i,j)
            if dist<smallest_dist:
                smallest_dist = dist
                input_id = i
                output_id = j
    #g.display_graph("test",verbose = True)
    return smallest_dist,input_id,output_id


# print(shortest_path_input_output(2,False))
# g.display_graph("test",verbose = True)
# print(smallest_dist,input_id,output_id)
# # # check_invarients()

# print(add_registre_naive_half(162,210,size=8))
# print(add_CLA(300,147))

# print_stats()
