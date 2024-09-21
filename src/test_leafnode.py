import unittest

from htmlnode import LeafNode

props = {
        "href": "https://www.google.com", 
        "target": "_blank",
    }

class TestLeafNode(unittest.TestCase):
    def test_tag_eq(self):
        node = LeafNode("a", "This is a leaf node", props)
        node2 = LeafNode("a", "This is a leaf node", props)
        self.assertEqual(node.tag, node2.tag)

    def test_value_eq(self):
        node = LeafNode("a", "This is a leaf node", props)
        node2 = LeafNode("a", "This is a leaf node", props)
        self.assertEqual(node.value, node2.value)
        
    def test_to_html(self):
        node = LeafNode("a", "This is a leaf node", props)
        result = '<a href="https://www.google.com" target="_blank">This is a leaf node</a>'
        self.assertEqual(node.to_html(), result)
        
    def test_to_html_no_tag(self):
        node = LeafNode(None, "This is a leaf node", props)
        result = 'This is a leaf node'
        self.assertEqual(node.to_html(), result)
        
    def test_to_html_no_tag(self):
        node = LeafNode(None, "This is a leaf node", props)
        result = 'This is a leaf node'
        self.assertEqual(node.to_html(), result)            

    def test_to_html_no_props(self):
        node = LeafNode("p", "This is a leaf node")
        result = "<p>This is a leaf node</p>"
        self.assertEqual(node.to_html(), result)     

if __name__ == "__main__":
    unittest.main()