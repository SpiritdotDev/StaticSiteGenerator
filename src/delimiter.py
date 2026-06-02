from textnode import TextNode,TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    valid_delimiters = ["**", "_", "`"]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            if delimiter not in valid_delimiters:
                raise Exception("invalid markdown syntax")
            else:
                split_string = node.text.split(delimiter)
                if len(split_string) % 2 == 0:
                    raise Exception("delimiter is unmatched")
                
                for i in range(len(split_string)):
                    if i % 2 == 0 and split_string[i] != "":
                        new_node = TextNode(split_string[i], TextType.TEXT)
                        new_nodes.append(new_node)
                    elif i % 2 != 0 and split_string[i] != "":
                        new_node = TextNode(split_string[i], text_type)
                        new_nodes.append(new_node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
                
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_images(node.text)
        if matches == []:
            new_nodes.append(node)
        else:
            remaining_text = node.text
            for entry in matches:
                image_alt = entry[0]
                image_link = entry[1]
                before, after = remaining_text.split(f"![{image_alt}]({image_link})", 1)
                if before != "":
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                remaining_text = after
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        if matches == []:
            new_nodes.append(node)
        else:
            remaining_text = node.text
            for entry in matches:
                link_text = entry[0]
                link = entry[1]
                before, after = remaining_text.split(f"[{link_text}]({link})", 1)
                if before != "":
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(link_text, TextType.LINK, link))
                remaining_text = after
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    content = TextNode(text, TextType.TEXT)
    content_after_delim = [content]
    delims = ["**", "_", "`"]
    types = [TextType.BOLD,TextType.ITALIC,TextType.CODE]
    for i in range(0,3):
        content_after_delim = split_nodes_delimiter(content_after_delim, delims[i],types[i] )
    content_after_image = split_nodes_image(content_after_delim)
    content_after_link = split_nodes_link(content_after_image)
    return content_after_link