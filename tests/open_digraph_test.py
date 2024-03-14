import sys
import os
sys.path.append(r"..") # allows us to fetch files from the project root
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
        empt = open_digraph([],[],{})
        g.iparallel(g.copy())
        empt.iparallel(g)
        self.assetEqual(g,empt)
        g.add_node()
        self.assertNotEqual(g,empt)

        n02 = [node(0, '0', {}, {2:1}) , node(1, 'ss', {}, {3:1}),node(2, 'zs', {0:1}, {4:3}),node(3, 'ee', {1:1}, {4:2}) , node(4, '5', {2:3,3:2}, {5:1}),node(5, '&', {4:1}, {})]
        inp2= [0,1]
        outputs2 = [5]
        n1 = [node(0, '&', {}, {1:1}) , node(1, 'ss', {0:1}, {2:1, 3:1}),node(2, 'zs', {1:1}, {}),node(3, 'bb', {1:1}, {}) ]
        inp1= [0]
        outputs1 = [2,3]
        gtest1 = open_digraph(inp2,outputs2,n02)
        gtest2 = open_digraph(inp1,outputs1,n1)


if __name__ == '__main__': # the following code is called only when
    unittest.main()
