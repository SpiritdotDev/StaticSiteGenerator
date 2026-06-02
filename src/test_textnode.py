import unittest
from textnode import TextNode, TextType
from delimiter import split_nodes_delimiter,extract_markdown_images,extract_markdown_links,split_nodes_image,split_nodes_link,text_to_textnodes
from markdown_to_blocks import markdown_to_blocks,markdown_to_html_node
from blocktype import block_to_block_type,BlockType
from generate_page import extract_heading

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.BOLD)
        self.assertNotEqual(node,node2)

    def test_url(self):
        node = TextNode("Some Text", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Some Text", TextType.LINK)
        self.assertNotEqual(node,node2)

    def test_delimiter_bold(self):
        node = TextNode("Some **bold** text", TextType.TEXT)
        split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_delimiter_multi(self):
        node = TextNode("Some **bold** text **here** and **here** too!", TextType.TEXT)
        split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_delimiter_wrong_delim(self):
        node = TextNode("Some **bold** text", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "&", TextType.BOLD)
    
    def test_delimiter_unmatched(self):
        node = TextNode("Some **bold text", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node],"**", TextType.BOLD)

    def test_delimiter_italic(self):
        node1 = TextNode("some _italic_ text and **bold** text", TextType.TEXT)
        node2 = TextNode("some _more italic_ text", TextType.TEXT)
        split_nodes_delimiter([node1,node2], "_", TextType.ITALIC)

    def test_multi_delim(self):
        node = TextNode("Some _italic_ and **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node],"_",TextType.ITALIC)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev)"
        )
        self.assertListEqual([("link", "https://boot.dev")], matches)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://boot.dev) and another [second link](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://google.com"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is a long markdown text **full of bold** words, and also some _italic_ words, there might even" \
        "be some `Code blocks` in here somewhere, theres [links](https://boot.dev) and also an ![image](https://i.imgur.com/3elNhQu.png)"
        self.assertListEqual([TextNode("This is a long markdown text ", TextType.TEXT),
                               TextNode("full of bold", TextType.BOLD),
                                 TextNode(" words, and also some ", TextType.TEXT),
                                   TextNode("italic", TextType.ITALIC),
                                     TextNode(" words, there might evenbe some ", TextType.TEXT),
                                       TextNode("Code blocks", TextType.CODE),
                                         TextNode(" in here somewhere, theres ", TextType.TEXT),
                                           TextNode("links", TextType.LINK, "https://boot.dev"),
                                             TextNode(" and also an ", TextType.TEXT),
                                               TextNode("image", TextType.IMAGE,"https://i.imgur.com/3elNhQu.png")],text_to_textnodes(text))
        

    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_too_many_spaces(self):
        md = """This is a paragraph




With way too many spaces"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks, [
                "This is a paragraph",
                "With way too many spaces"
            ]
        )

    def test_block_to_blocktype_heading(self):
        block = "### Some Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = """```
this is code ```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> this is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_unordered_list_block(self):
        block = "- This is an unordered list"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = "1. this is an ordered list"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_block2(self):
        block = "3. this is also an ordered list"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

    def test_extract_heading(self):
        md = """
This is a markdown file
# here is the heading
# here is a fake heading we dont want to see
## here is a level 2 heading"""
        self.assertEqual(extract_heading(md), "here is the heading")

    def test_extract_heading_from_middle(self):
        md = """
## here is a heading we dont want to see
# here is the heading we want
blahhhhhhh"""
        self.assertEqual(extract_heading(md), "here is the heading we want")

if __name__ == "__main__":
    unittest.main()