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

if __name__ == '__main__': # the following code is called only when
    unittest.main()
