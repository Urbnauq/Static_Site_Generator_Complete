from textnode import TextNode
from htmlnode import (
    HTMLNode, 
    LeafNode, 
    ParentNode)
from functions import (
    text_node_to_html_node)

props = {
    "href": "https://www.google.com", 
    "target": "_blank"
    }

def main():
    
    textnode = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(textnode)

    htmlnode = HTMLNode("p", "This is a html node", None, props)
    print(htmlnode)
    
    leafnode = LeafNode("a", "This is a leaf node", props)
    print(leafnode)
    
    parentnode = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
    )
    print(parentnode.to_html())
    
    text_node_html_node = text_node_to_html_node(TextNode("This is a text node", "image", "https://www.boot.dev"))
    print(text_node_html_node)
    
main()