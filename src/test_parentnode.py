import unittest

from htmlnode import ParentNode, LeafNode
    
props = {
    "href": "https://www.google.com", 
    "target": "_blank",
    }

leaf_node = LeafNode("b", "Bold text")
leaf_node_1 = LeafNode(None, "Normal text")
leaf_node_2 = LeafNode("i", "italic text")
leaf_node_3 = LeafNode(None, "Normal text")

children = [leaf_node, leaf_node_1, leaf_node_2, leaf_node_3]
    
class TestParentNode(unittest.TestCase):
    def test_parent_tag_eq(self):
        node = ParentNode("p", children)
        node2 = ParentNode("p", children)
        self.assertEqual(node.tag, node2.tag)
        
    def test_parent_children_eq(self):
        node = ParentNode("p", children)
        node2 = ParentNode("p", children)
        self.assertEqual(node.children, node2.children)
        
    def test_parent_to_html(self):
        node = ParentNode("p", children)
        result = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(), result)
        
if __name__ == "__main__":
    unittest.main()