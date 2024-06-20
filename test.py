import XMLtkinter as XTKML

@XTKML.XTKML
def hello():
    print("hello")

XTKML.xmltkinter("test.xml").start()