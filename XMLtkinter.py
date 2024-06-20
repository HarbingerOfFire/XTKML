import tkinter as tk
import xml.etree.ElementTree as ET
import re
from typing import Any

def XTKML(func):
    def register():
        __builtins__[f"{func.__name__}"] = func
    register()

class string(str):
    def __init__(self, value: str) -> None:
        self.value = str(value)
        super().__init__()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self.value in globals().keys():
            return globals()['__name__'][self.value](*args, **kwds)
        else:
            try:
                return globals()['__builtins__'][self.value](*args, **kwds)
            except AttributeError:
                raise NameError(f"name '{self.value}' is not defined")

def pop(d, index):
    # Convert the dictionary keys to a list
    keys = list(d.keys())

    # Check if the index is within the range of keys
    if 0 <= index < len(keys):
        # Get the key at the specified index
        key_to_remove = keys[index]

        # Remove the key-value pair using pop and return the value
        removed_value = d.pop(key_to_remove)
        return removed_value
    else:
        print(f"Index {index} is out of range for the dictionary.")
        return None

class tag:
    def __init__(self, name, text) -> None:
        self.name = name
        self.text = text

    def __repr__(self):
        return self.name

    def config(self, type, **kwargs):
        pattern = r'%([^%]+)%'
        for key in kwargs:
            if kwargs[key] == "%TEXT%":
                kwargs[key] = self.text
            if re.findall(pattern, kwargs[key]):
                kwargs[key] = string(re.findall(pattern, kwargs[key])[0])
        if 'background' not in kwargs.keys() and 'bg' not in kwargs.keys():
            kwargs['bg'] = self.tkroot['bg']
        if type != "Frame":
            self.element = getattr(tk, type)(master=self.tkroot, text=self.text)
        else:
            self.element = getattr(tk, type)(master=self.tkroot)
        self.element.configure(**kwargs)

    def pack(self):
        self.element.pack(fill=tk.BOTH, expand=True)

    def set_root(self, root: tk.Tk | tk.Frame):
        self.tkroot = root

class xmltkinter:
    def __init__(self, file) -> None:
        self.tkroot = tk.Tk()
        self.tree = ET.parse(file)
        self.root = self.tree.getroot()

    def start(self):
        for child in self.root:
            self.main=tag(child.tag, child.text)
            self.main.set_root(self.tkroot)
            self.main.config('Frame', **(child.attrib))
            self.main.pack()
            for children in child:
                self.tag=tag(children.tag, children.text)
                self.tag.set_root(self.main.element)
                self.tag.config(**(children.attrib))
                self.tag.pack()
        self.tkroot.mainloop()