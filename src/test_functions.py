import unittest

from textnode import TextNode
from htmlnode import LeafNode
from functions import (
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
    text_node_to_html_node, 
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link, 
    text_to_textnodes,
    markdown_to_blocks)

class Testfunctions(unittest.TestCase):
    
    def test_text_node_to_html_node_text_eq(self):
        text_node = TextNode("This is a text node", "text")
        text_to_html_node_text = text_node_to_html_node(text_node)
        results = "This is a text node"
        self.assertEqual(text_to_html_node_text, results)
        
    def test_text_node_to_html_node_bold_eq(self):
        text_node = TextNode("This is a text node", "bold")
        text_to_html_node_bold = text_node_to_html_node(text_node)
        results = LeafNode("b", "This is a text node", None)
        self.assertEqual(str(text_to_html_node_bold), str(results))
        
    def test_text_node_to_html_node_italic_eq(self):
        text_node = TextNode("This is a text node", "italic")
        text_to_html_node_bold = text_node_to_html_node(text_node)
        results = LeafNode("i", "This is a text node", None)
        self.assertEqual(str(text_to_html_node_bold), str(results))
        
    def test_text_node_to_html_node_code_eq(self):
        text_node = TextNode("This is a text node", "code")
        text_to_html_node_bold = text_node_to_html_node(text_node)
        results = LeafNode("code", "This is a text node", None)
        self.assertEqual(str(text_to_html_node_bold), str(results))
        
    def test_text_node_to_html_node_link_eq(self):
        text_node = TextNode("This is a text node", "link")
        text_to_html_node_bold = text_node_to_html_node(text_node)
        results = LeafNode("a", text_node.text, {"href" : text_node.url})
        self.assertEqual(str(text_to_html_node_bold), str(results))
        
    def test_text_node_to_html_image_eq(self):
        text_node = TextNode("This is a text node", "image")
        text_to_html_node_bold = text_node_to_html_node(text_node)
        results = LeafNode("img", "", {"src" : text_node.url, "alt" : text_node.text})
        self.assertEqual(str(text_to_html_node_bold), str(results))
        
# split_nodes_delimiter test-------------------------------------------------------------------------------

    def test_text_split_nodes_delimiter_code(self):
        old_nodes = TextNode("This is text with a `code block` word", "text")
        split_to_text_node_delimiter = split_nodes_delimiter([old_nodes], "`", "text")
        results = "[TextNode(This is text with a , text, None), TextNode(code block, code, None), TextNode( word, text, None)]"
        self.assertEqual(str(split_to_text_node_delimiter), str(results))
        
    def test_text_split_nodes_delimiter_italic(self):
        old_nodes = TextNode("This is text with a *italic block* word", "text")
        split_to_text_node_delimiter = split_nodes_delimiter([old_nodes], "*", "text")
        results = "[TextNode(This is text with a , text, None), TextNode(italic block, italic, None), TextNode( word, text, None)]"
        self.assertEqual(str(split_to_text_node_delimiter), str(results))
        
    def test_text_split_nodes_delimiter_bold(self):
        old_nodes = TextNode("This is text with a **bold block** word", "text")
        split_to_text_node_delimiter = split_nodes_delimiter([old_nodes], "**", "text")
        results = "[TextNode(This is text with a , text, None), TextNode(bold block, bold, None), TextNode( word, text, None)]"
        self.assertEqual(str(split_to_text_node_delimiter), str(results))
        
    def test_text_split_nodes_delimiter_italic_double(self):
        old_nodes = TextNode("This is *text* with a *italic block* word", "text")
        split_to_text_node_delimiter = split_nodes_delimiter([old_nodes], "*", "text")
        results = "[TextNode(This is , text, None), TextNode(text, italic, None), TextNode( with a , text, None), TextNode(italic block, italic, None), TextNode( word, text, None)]"
        self.assertEqual(str(split_to_text_node_delimiter), str(results))
        
    def test_text_split_delimiter_exception(self):
        old_nodes = TextNode("This is *text* with a *italic block word", "text")
        with self.assertRaises(Exception):
            split_nodes_delimiter([old_nodes], "*", "text")
            
# Extract_markdown_images test--------------------------------------------------------------------------------------

    def test_extract_markdown_images(self):
        image_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extract_images = extract_markdown_images(image_text)
        results = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertEqual(extract_images, results)
        
    def test_extract_markdown_links(self):
        link_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extract_links = extract_markdown_links(link_text)
        results = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_links, results)
        
# Split images and links into Testnodes test--------------------------------------------------------------------------------------    

    def test_split_image_text_nodes(self):
        text_node_image = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) okay", "text")
        split_image = split_nodes_image([text_node_image])
        results = [
            TextNode("This is text with a ", "text", None), 
            TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif"), 
            TextNode(" okay", "text", None), 

            ]
        self.assertEqual(split_image, results)
    
    def test_split_images_text_nodes(self):
        text_node_image = TextNode('This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)', "text")
        split_image = split_nodes_image([text_node_image])
        results = [
            TextNode("This is text with a ", "text", None), 
            TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif"), 
            TextNode(" and ", "text", None), 
            TextNode("obi wan", "image", "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        self.assertEqual(split_image, results)
        
    def test_split_link_text_nodes(self):
        text_node_link = TextNode("This is text with a link [to boot dev](https://www.boot.dev) are you okay", "text")
        split_link = split_nodes_link([text_node_link])
        results = [
            TextNode("This is text with a link ", "text", None), 
            TextNode("to boot dev", "link", "https://www.boot.dev"), 
            TextNode(" are you okay", "text", None), 

            ]
        self.assertEqual(split_link, results)
        
    def test_split_links_text_nodes(self):
        text_node_link = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", "text")
        split_link = split_nodes_link([text_node_link])
        results = [
            TextNode("This is text with a link ", "text", None), 
            TextNode("to boot dev", "link", "https://www.boot.dev"), 
            TextNode(" and ", "text", None), 
            TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev")
            ]
        self.assertEqual(split_link, results)
        
# Text to Textnode test--------------------------------------------------------------------------------------    

    def test_text_to_text_node_eq(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_text_node = text_to_textnodes(text)
        results = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),]
        self.assertEqual(text_text_node, results)

# Markdown to blocks test--------------------------------------------------------------------------------------    
    
    def test_markdown_to_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        markdown_block = markdown_to_blocks(markdown)
        results = ['# This is a heading', 
                   'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', 
                   '* This is the first list item in a list block', 
                   '* This is a list item', 
                   '* This is another list item']
        self.assertEqual(markdown_block, results)
        
if __name__ == "__main__":
    unittest.main() 