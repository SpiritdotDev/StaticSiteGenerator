from textnode import TextNode, TextType
import os
import shutil
from generate_page import generate_pages_recursive
import sys

def copy_directory(source_dir, target_dir):
    if not os.path.exists(target_dir):
        raise Exception("Target directory does not exist")
    else:
        shutil.rmtree(target_dir)
    if not os.path.exists(source_dir):
        raise Exception("Directory does not exist")
    else:
        shutil.copytree(source_dir,target_dir)


def main():
    basepath = sys.argv
    if basepath == None:
        basepath = "/"
    copy_directory("static", "docs")
    generate_pages_recursive("content", 'template.html', "docs", basepath)


main()