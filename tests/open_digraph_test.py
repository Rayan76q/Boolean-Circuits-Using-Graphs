import sys
import os
root = r"C:\Users\HP\Desktop\vscode\graphs-and-logic"
sys.path.append(root) # allows us to fetch files from the project root
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
        if __name__ == '__main__': # the following code is called only when
            unittest.main() 
            
            
    def test_init_open_digraph(self):
        n0 = [node(0, 'i', {}, {1:1})]
        inp= [1,2,3] 
        outputs = [5]
        
        g = open_digraph(inp , outputs , n0)
        self.assertEqual(g.nodes[0], n0)
        self.assertEqual(g.inputs, inp)
        self.assertEqual(g.outputs, outputs)
        if __name__ == '__main__': # the following code is called only when
            unittest.main() 
            
            
            
            
if __name__ == '__main__': # the following code is called only when
    unittest.main()
