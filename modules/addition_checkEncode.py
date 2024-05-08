import os
import sys
sys.path[0] = os.path.abspath(os.path.join(sys.path[0], '..'))
from modules.adders import adders
import random

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
    a_str = adders.convert_to_binary_string(a,size=size)
    b_str = adders.convert_to_binary_string(b,size=size)
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
    g = adders.CLA_adder(quotient-1)
    registre = adders.create_registre(int(res , 2),size=(quotient)*8+1)
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
    a_str = adders.convert_to_binary_string(a,size=size)
    b_str = adders.convert_to_binary_string(b,size=size)
    res = ""
    for i in range(size):
        res +=   b_str[i]+a_str[i]
    res = res + "0" # adding 0 carry bit
    reg_size , n = find_bigger_2_pow(size)
    g = adders.adder(n)
    registre = adders.create_registre(int(res , 2),size=2*reg_size+1)
    g.icompose(registre)
    return g.calculate()

def add_naive(a,b):
    """
        b is added to a without needing to specify size
    """
    size = max(a.bit_length(),b.bit_length())
    return add_registre_naive(a,b,size = size)


def check_invarients():
    enc = adders.encodeur_4bits()
    dec = adders.decodeur_7bits()
    
    for i in range(-1,4): #-1 -> no error is introduced
        noise = adders.perturbe_bit(7,[i]) 
        g = adders(noise.compose(enc))
        g2 = adders(dec.compose(g))
        
        for i in range(0,16):
            reg = adders.create_registre(i,size=4)
            g3 = adders(g2.compose(reg))
            assert (i==g3.calculate())
    
    print("Hamming property verfied when introducing one error at most.")
    
    mistakes = 0
    for i in range(4): 
        for j in range(i+1,4):
            noise = adders.perturbe_bit(7,[i,j]) 
            g = adders(noise.compose(enc))
            g2 = adders(dec.compose(g))
            for k in range(0,16):
                reg = adders.create_registre(k,size=4)
                g3 = adders(g2.compose(reg))
                mistakes += (i!=g3.calculate())
    print(f"Number of time that the original signal couldn't be retreived when introducing 2 errors: {mistakes} out of {6*16} attempts.")
    
    
    




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
check_invarients()

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

# for i in range(16):
#     for j in range(16):
#         print( f"{i} + {j} =", add_registre(i,j,size=4) )



#(adders.CL_4bit()[0]).display_graph()
print(add_registre_CLA(0,16,size= 8))
i = 0
res = True
while i <2000 and res:
    print(i)
    a = random.randint(0,1234567865)
    b = random.randint(0,1234567432)
    i+=1
    res = (add_CLA(a,b)== 
        add_naive(a,b) == a+b)
print(res and (i==2000) )