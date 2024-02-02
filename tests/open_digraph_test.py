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
        print(g)
        g.add_edge(0,1)
        print(g)
        
            
            
            
            
if __name__ == '__main__': # the following code is called only when
    unittest.main()
