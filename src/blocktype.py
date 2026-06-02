from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

#This checks the start of the block to identify its type, can be changed to work exclusively with regex
def block_to_block_type(block):
    pattern = re.compile("\d\.")
    if block[0] == "#":
        return BlockType.HEADING
    elif block[:4] == "```\n" and block[-3:] == "```":
        return BlockType.CODE
    elif block[0] == ">":
        return BlockType.QUOTE
    elif block[:2] == "- ":
        return BlockType.UNORDERED_LIST
    elif pattern.match(block[:2]):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
