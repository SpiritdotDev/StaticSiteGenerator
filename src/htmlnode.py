class HTMLNode():
    def __init__(self,tag: str =None, value: str =None, children: list =None,props: dict =None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        return NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        else:
            formatted_props = ""
            for key, value in self.props.items():
                formatted_props += f" {key}={value}"
            return formatted_props
            
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props:dict = None):
        super().__init__(tag,value,None,props)

    def to_html(self):
        if self.value == None:
            raise ValueError()
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self,tag: str, children: list, props: dict = None):
        super().__init__(tag,None,children,props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("tag cannot be None")
        elif self.children == None:
            raise ValueError("must have children")
        else:
            children_html = ""
            for child in self.children:
                children_html += child.to_html()
        return f"<{self.tag}>{children_html}</{self.tag}>"