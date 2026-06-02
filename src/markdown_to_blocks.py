from htmlnode import HTMLNode,ParentNode
from textnode import text_node_to_html_node, TextNode,TextType
from blocktype import block_to_block_type,BlockType
from delimiter import text_to_textnodes
import re

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        block = block.strip()
        if block != "":
            new_blocks.append(block)
    return new_blocks

def text_to_children(text) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        child = text_node_to_html_node(node)
        children.append(child)
    return children


def markdown_to_html_node(markdown):
    blocks_from_markdown = markdown_to_blocks(markdown)
    big_children = []
    for block in blocks_from_markdown:
        blocktype = block_to_block_type(block)
        if blocktype == BlockType.CODE:
            fixed_block = block[4:-3]
            text_node = TextNode(fixed_block, TextType.CODE)
            child_node = text_node_to_html_node(text_node)
            node = ParentNode("pre", [child_node])
        else:
            match blocktype:
                case BlockType.QUOTE:
                    lines = block.split("\n")
                    fixed_line = ""
                    new_lines = []
                    for line in lines:
                        new_lines.append(line.lstrip(">").strip())
                    content = " ".join(new_lines)
                    children = text_to_children(content)
                    node = ParentNode("blockquote", children)
                case BlockType.UNORDERED_LIST:
                    lines = block.split("\n")
                    li_nodes = []
                    for line in lines:
                        stripped_line = line[2:]
                        small_children = text_to_children(stripped_line)
                        li_nodes.append(ParentNode("li", small_children))
                    node = ParentNode("ul", li_nodes)
                case BlockType.ORDERED_LIST:
                    lines = block.split("\n")
                    li_nodes = []
                    for line in lines:
                        stripped_line = line.split(". ", 1)
                        small_children = text_to_children(stripped_line[1])
                        li_nodes.append(ParentNode("li", small_children))
                    node = ParentNode("ol", li_nodes)
                case BlockType.PARAGRAPH:
                    lines = block.split("\n")
                    content = " ".join(lines)
                    children = text_to_children(content)
                    node = ParentNode("p", children)
                case BlockType.HEADING:
                    heading_num = 0
                    for char in block:
                        if char == "#":
                            heading_num += 1
                    children = text_to_children(block[heading_num + 1:])
                    node = ParentNode(f"h{heading_num}", children)
        big_children.append(node)
    parent = ParentNode("div", big_children)
    return parent            