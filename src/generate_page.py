import os
from htmlnode import HTMLNode
from markdown_to_blocks import markdown_to_html_node
from pathlib import Path

def extract_heading(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line != "":
            if line[0] == "#" and line[1] != "#":
                heading = line[2:]
                return heading

def generate_page(src_path, template_path, dest_path, basepath):
    if not os.path.exists(src_path) or not os.path.exists(template_path):
        raise Exception("one or more path or directory does not exist")
    print(f"Generating page from {src_path} to {dest_path} using {template_path}")

    with open(src_path)as src:
        src_file = src.read()

    with open(template_path)as temp:
        template = temp.read()

    src_as_html = markdown_to_html_node(src_file).to_html()
    title = extract_heading(src_file)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", src_as_html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, mode="w") as f:
        f.write(template)

def generate_pages_recursive(src_path, template_path, dest_path,basepath):
    to_visit = os.listdir(src_path)
    files_to_gen = []
    for path in to_visit:
        if os.path.isdir(os.path.join(src_path, path)):
            generate_pages_recursive(os.path.join(src_path,path),template_path,os.path.join(dest_path,path),basepath)
        elif os.path.isfile(os.path.join(src_path,path)):
            files_to_gen.append(path)
    for file in files_to_gen:
        generate_page(os.path.join(src_path,file), template_path, Path(os.path.join(dest_path,file)).with_suffix(".html"),basepath)
