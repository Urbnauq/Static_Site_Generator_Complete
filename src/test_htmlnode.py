import unittest

from htmlnode import HTMLNode

props = {
        "href": "https://www.google.com", 
        "target": "_blank",
    }

class TestHTMLNode(unittest.TestCase):
    def test_tag_eq(self):
        node = HTMLNode("p", "This is a html node", None, props)
        node2 = HTMLNode("p", "This is a html node", None, props)
        self.assertEqual(node.tag, node2.tag)
        
    def test_value_eq(self):
        node = HTMLNode("p", "This is a html node", None, props)
        node2 = HTMLNode("p", "This is a html node", None, props)
        self.assertEqual(node.value, node2.value)
        
    def test_children_eq(self):
        node = HTMLNode("p", "This is a html node", None, props)
        node2 = HTMLNode("p", "This is a html node", None, props)
        self.assertEqual(node.children, node2.children)        

    def test_prop_eq(self):
        node = HTMLNode("p", "This is a html node", None, props)
        node2 = HTMLNode("p", "This is a html node", None, props)
        self.assertEqual(node.props, node2.props)
        
    def test_children_is_none(self):
        node = HTMLNode("p", "This is a html node", None, props)
        self.assertIsNone(node.children)
        
    def test_props_to_html_eq(self):
        node = HTMLNode("p", "This is a html node", None, props)
        result = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), result)           

if __name__ == "__main__":
    unittest.main()