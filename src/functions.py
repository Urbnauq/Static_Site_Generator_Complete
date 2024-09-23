import re

from htmlnode import LeafNode, ParentNode
from textnode import TextNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

paragraph_block = "paragraph"
heading_block = "heading"
code_block = "code"
quote_block = "quote"
unordered_list = "unordered_list"
ordered_list = "ordered_list"

bold = "**"
italic = "*"
code = "`"

def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href" : text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src" : text_node.url, "alt" : text_node.text})
    raise Exception(f"Invalid text type. {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes       
        
def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        
        node_text = node.text
        images = extract_markdown_images(node_text)
        
        if len(images) == 0:
            new_nodes.append(node)
            continue
        
        for image in images:
            sections = node_text.split(f"![{image[0]}]({image[1]})", 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(image[0], text_type_image, image[1]))
            
            node_text = sections[1]
        
        if node_text != "":
            new_nodes.append(TextNode(node_text, text_type_text))
    
    return new_nodes
        
def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        
        node_text = node.text
        links = extract_markdown_links(node_text)
        
        if len(links) == 0:
            new_nodes.append(node)
            continue
        
        for link in links:
            sections = node_text.split(f"[{link[0]}]({link[1]})", 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            
            node_text = sections[1]
            
        if node_text != "":
            new_nodes.append(TextNode(node_text, text_type_text))

    return new_nodes
            
def text_to_textnodes(text):
    text_node = TextNode(text, text_type_text)
    nodes = [text_node]
    
    nodes = split_nodes_delimiter(nodes, bold, text_type_bold)
    nodes = split_nodes_delimiter(nodes, italic, text_type_italic)
    nodes = split_nodes_delimiter(nodes, code, text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown):
    blocks = []
    markdown_split = markdown.splitlines()
    
    for block in markdown_split:
        if block == "":
            continue        
        block = block.strip()
        blocks.append(block)
    
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return heading_block
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return code_block
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return paragraph_block
        return quote_block
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return paragraph_block
        return unordered_list
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return paragraph_block
        return unordered_list
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return paragraph_block
            i += 1
        return ordered_list
    return paragraph_block

def strip_heading(block):
    if block.startswith("# "):
        heading_tag = "h1"
        return block.lstrip("# "), heading_tag
    if block.startswith("## "):
        heading_tag = "h2"
        return block.lstrip("# "), heading_tag        
    if block.startswith("### "):
        heading_tag = "h3"
        return block.lstrip("# "), heading_tag
    if block.startswith("#### "):
        heading_tag = "h4"
        return block.lstrip("# "), heading_tag 
    if block.startswith("##### "):
        heading_tag = "h5"
        return block.lstrip("# "), heading_tag
    if block.startswith("###### "):
        heading_tag = "h6"
        return block.lstrip("# "), heading_tag  
        
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == paragraph_block:
        return paragraph_to_html_node(block)
    if block_type == heading_block:
        return heading_to_html_node(block)
    if block_type == code_block:
        return code_to_html_node(block)
    if block_type == ordered_list:
        return olist_to_html_node(block)
    if block_type == unordered_list:
        return ulist_to_html_node(block)
    if block_type == quote_block:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
    

    
