import sys
import os
sys.path[0] = os.path.abspath(os.path.join(sys.path[0], '..'))
print(sys.path) # allows us to fetch files from the project root
import unittest
from modules.open_digraph import * 



class InitTest(unittest.TestCase):
    
    
    def test_init_node(self):
        n0 = node(0, 'i', {}, {1:1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1:1})
        self.assertIsInstance(n0, node)
        self.assertIsNot(n0.copy() , n0)
            
            
    def test_init_open_digraph(self):
        n0 = [node(0, 'a', {}, {}) , node(1, 'b', {}, {})]
        inp= [] 
        outputs = []
        g = open_digraph(inp , outputs , n0)
        
        self.assertEqual(g.nodes[0], n0[0])
        self.assertEqual(g.inputs, inp)
        self.assertEqual(g.outputs, outputs)
        self.assertIsNot(g.copy() , g)
    def test_add_node_edges(self):
        n0 = [node(0, 'a', {}, {}) , node(1, 'b', {}, {})]
        inp= [] 
        outputs = []
        g = open_digraph(inp , outputs , n0)
        g.add_edge(0,1)
        self.assertEqual(g.get_node_by_id(0).get_children() , {1:1})
        self.assertEqual(g.get_node_by_id(1).get_parents() , {0:1})
        g.add_node('c', {1:1}, {0:2})
        self.assertEqual(g.get_node_by_id(2).get_children() , {0:2})
        self.assertEqual(g.get_node_by_id(2).get_parents() , {1:1})
        self.assertEqual(g.get_node_by_id(0).get_parents() , {2:2})
        self.assertEqual(g.get_node_by_id(1).get_children() , {2:1})
        g.remove_edge(0,1)
        self.assertEqual(g.get_node_by_id(0).get_children() , {})
        self.assertEqual(g.get_node_by_id(1).get_parents() , {})
        g.remove_edge(2,0);    
        self.assertEqual(g.get_node_by_id(2).get_children() , {0:1})
        self.assertEqual(g.get_node_by_id(0).get_parents() , {2:1})
        g.add_edge(2,0)
        g.add_edge(2,0)
        self.assertEqual(g.get_node_by_id(2).get_children() , {0:3})
        self.assertEqual(g.get_node_by_id(0).get_parents() , {2:3})
        g.remove_parallel_edges(2,0)
        self.assertEqual(g.get_node_by_id(2).get_children() , {})
        self.assertEqual(g.get_node_by_id(0).get_parents() , {})
        
        g.add_edges([(2,0) , (1,0) , (2,1)] ,[2,3,1])
        self.assertEqual(g.get_node_by_id(2).get_children() , {0:2 , 1:1})
        self.assertEqual(g.get_node_by_id(0).get_parents() , {2:2 , 1:3})
        self.assertEqual(g.get_node_by_id(1).get_children() , {2:1 , 0:3})
        g.remove_several_parallel_edges([(2,0) , (1,0) , (2,1)])
        self.assertEqual(g.get_node_by_id(2).get_children() , {})
        self.assertEqual(g.get_node_by_id(0).get_parents() , {})
        self.assertEqual(g.get_node_by_id(1).get_children() , {2:1})
        self.assertEqual(g.get_node_by_id(1).get_parents() , {})
        
        g.add_edges([(2,0) , (1,0) , (2,1) , (0,2)] ,[2,3,1,5])
        g.remove_nodes_by_id([1,2])
        self.assertEqual(g.nodes[0], n0[0])
        self.assertEqual(g.nodes.keys().__len__(), 1)
        g.add_node(label="b" , parents={0:1} , children={})
        g.add_node(label="b" , parents={1:2} , children={0:1})
        g.add_input_node(0)
        self.assertEqual(g.get_node_by_id(3).get_children() , {0:1})
        self.assertEqual(g.get_node_by_id(3).get_parents() , {})
        self.assertEqual(g.get_inputs_ids() , [3])
        g.add_output_node(2)
        self.assertEqual(g.get_node_by_id(4).get_children() , {})
        self.assertEqual(g.get_node_by_id(4).get_parents() , {2:1})
        self.assertEqual(g.get_outputs_ids() , [4])
    
    def test_parallel(self):
        n0 = [node(0, '&', {}, {}) , node(1, '', {}, {})]
        inp= []
        outputs = []
        op = open_digraph(inp,outputs, n0)
        g = bool_circ(op)
        g.add_node('|', {1:1}, {0:1})
        empt = open_digraph([],[],[])
        g_nouv = g.parallel(g)
        g.iparallel(g.copy())
        empt.iparallel(g)

        self.assertEqual(g_nouv,g)
        self.assertEqual(g, open_digraph([],[],[node(0, '&', {2:1}, {}) , node(1, '', {}, {2:1}),node(2,'|', {1:1}, {0:1}),node(3, '&', {5:1}, {}) , node(4, '', {}, {5:1}),node(5,'|', {4:1}, {3:1})]))
        self.assertEqual(g,empt)
        

        n02 = [node(0, '0', {}, {2:1}) , node(1, 'ss', {}, {3:1}),node(2, 'zs', {0:1}, {4:3}),node(3, 'ee', {1:1}, {4:2}) , node(4, '5', {2:3,3:2}, {5:1}),node(5, '&', {4:1}, {})]
        n02bis = [node.copy() for node in n02]
        inp2= [0,1]
        outputs2 = [5]
        n1 = [node(0, '&', {}, {1:1}) , node(1, 'ss', {0:1}, {2:1, 3:1}),node(2, 'zs', {1:1}, {}),node(3, 'bb', {1:1}, {}) ]
        inp1= [0]
        outputs1 = [2,3]
        gtest1 = open_digraph(inp2,outputs2,n02)
        gtest2 = open_digraph(inp1,outputs1,n1)
        gtestNULL = gtest1.parallel(open_digraph([],[],[]))
        gtestNULL2 = open_digraph([],[],{}).parallel(gtest2)
        gtest3 = gtest1.parallel(gtest2)

        self.assertEqual(gtest1, open_digraph(inp2,outputs2,n02))
        self.assertEqual(gtest1,gtestNULL)

        gtest1.iparallel(gtest2)

        self.assertNotEqual(gtest1,open_digraph([0,1],[5],n02bis))
        self.assertEqual(gtest3,gtest1)
        self.assertEqual(gtest2,gtestNULL2)

        g.add_node()

        self.assertNotEqual(g,empt)
    
    def test_connected_components(self):
        #the code of list_components is so basic and so dependant on connected_components 
        #that checking the first would be the same as checking the second
        n02 = [node(0, '0', {}, {2:1}) , node(1, 'ss', {}, {3:1}),node(2, 'zs', {0:1}, {4:3}),node(3, 'ee', {1:1}, {4:2}) , node(4, '5', {2:3,3:2}, {5:1}),node(5, '&', {4:1}, {})]
        n02bis = [node.copy() for node in n02]
        inp2= [0,1]
        outputs2 = [5]
        n1 = [node(0, '&', {}, {1:1}) , node(1, 'ss', {0:1}, {2:1, 3:1}),node(2, 'zs', {1:1}, {}),node(3, 'bb', {1:1}, {}) ]
        inp1= [0]
        outputs1 = [2,3]
        gtest1 = open_digraph(inp2,outputs2,n02)
        gtest2 = open_digraph(inp1,outputs1,n1)
        testlist = gtest1.component_list()
        testliste2 = gtest1.parallel(gtest2).component_list()
        m = gtest2.compose(gtest1)
        testliste3 = m.component_list()
        #m.display_graph()
        self.assertEqual(len(testliste3),2)
        self.assertEqual(testliste3[0],open_digraph([],[8,9],[node(7,"ss",{},{8:1,9:1}),node(8,"zs",{7:1},{}),node(9,"bb",{7:1},{})]))
        self.assertEqual(testliste3[1],open_digraph([0,1],[],[node(4,"5",{2:3,3:2},{5:1}),node(5,"&",{4:1},{}),
                                                              node(2,"zs",{0:1},{4:3}),node(3,"ee",{1:1},{4:2}),node(1,"ss",{},{3:1}),node(0,"0",{},{2:1})]))
        self.assertEqual(len(testlist),1)
        self.assertEqual(gtest1.component_list()[0],gtest1)
        self.assertEqual(len(testliste2),2)
        gtest1.shift_indices(4)
        self.assertEqual(testliste2[0],gtest1)
        self.assertEqual(testliste2[1],gtest2)



    def matrix_creation(self):
        n0 = [node(0, '&', {}, {}) , node(1, '', {}, {})]
        inp= []
        outputs = []
        g = open_digraph(inp,outputs, n0)
        adj = g.adj_mat()
        self.assertEqual(graph_from_adjacency_matrix(adj) == g)
        # print_m(random_symetric_int_matrix(5,9,True))
        # print_m(random_oriented_int_matrix(5,9))
        # print_m(random_dag_int_matrix(5,9))
        rand_mat = random_dag_int_matrix(5,5,False)
        m = graph_from_adjacency_matrix(rand_mat)

if __name__ == '__main__': # the following code is called only when
    unittest.main()
