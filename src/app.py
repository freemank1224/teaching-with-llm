import gradio as gr
from parser import DocumentParser
from evaluator import Evaluator
from config import config

class App:
    def __init__(self):
        self.parser = DocumentParser()
        self.evaluator = Evaluator()
        
    def create_interface(self):
        """创建Gradio界面"""
        # TODO: 实现Gradio界面
        pass

def launch():
    app = App()
    interface = app.create_interface()
    interface.launch()

if __name__ == "__main__":
    launch() 