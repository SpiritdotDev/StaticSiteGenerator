from textnode import TextNode, TextType
import os
import shutil
from generate_page import generate_pages_recursive

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
    copy_directory("static", "public")
    #generate_page("content/index.md", "template.html", "public/index.html")
    #generate_page("content/blog/glorfindel/index.md", "template.html", "public/content/blog/glorfindel/index.html")
    #generate_page("content/blog/tom/index.md", "template.html", "public/content/blog/tom/index.html")
    #generate_page("content/blog/majesty/index.md", "template.html", "public/content/blog/majesty/index.html")
    #generate_page("content/contact/index.md", "template.html", "public/content/contact/index.html")
    generate_pages_recursive("content", 'template.html', "public")


main()