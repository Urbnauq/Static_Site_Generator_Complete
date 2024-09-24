import unittest

from textnode import TextNode
from htmlnode import LeafNode
from functions import (
    text_node_to_html_node)

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TestFunctions(unittest.TestCase):
    def test_text_eq(self):
        text_node_html_node = text_node_to_html_node(TextNode("This is a test", text_type_text))
        results = LeafNode(None, "This is a test", None)
        self.assertEqual(str(text_node_html_node), str(results))
    
    def test_bold_eq(self):
        text_node_html_node = text_node_to_html_node(TextNode("This is a test", text_type_bold))
        results = LeafNode("b", "This is a test", None)
        self.assertEqual(str(text_node_html_node), str(results))
        
    def test_italic_eq(self):
        text_node_html_node = text_node_to_html_node(TextNode("This is a test", text_type_italic))
        results = LeafNode("i", "This is a test", None)
        self.assertEqual(str(text_node_html_node), str(results))
    
    def test_code_eq(self):
        text_node_html_node = text_node_to_html_node(TextNode("This is a test", text_type_code))
        results = LeafNode("code", "This is a test", None)
        self.assertEqual(str(text_node_html_node), str(results))
        
    def test_link_eq(self):
        text_node_html_node = text_node_to_html_node(TextNode("This is a test", text_type_link, "https://www.boot.dev"))
        results = LeafNode("a", "This is a test", {"href" : "https://www.boot.dev"})
        self.assertEqual(str(text_node_html_node), str(results))
        
    def test_image_eq(self):
        text_node_html_node = text_node_to_html_node(TextNode("This is a test", text_type_image, "https://www.boot.dev"))
        results = LeafNode("img", None, {"src" : "https://www.boot.dev", "alt" : "This is a test"})
        self.assertEqual(str(text_node_html_node), str(results))
        
    def test_exception_eq(self):
        with self.assertRaises(Exception):
            text_node_to_html_node(TextNode("This is a test", "big", "https://www.boot.dev"))
    

if __name__ == "__main__":
    unittest.main()