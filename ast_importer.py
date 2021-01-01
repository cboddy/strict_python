from importlib.abc import Loader, MetaPathFinder
import sys
import os.path
from importlib.machinery import ModuleSpec
import ast

def exec_ast_tree(ast_tree):
    """executes the AST-tree and returns locals after  exec-ing"""
    exec(compile(ast_tree, filename="<ast>", mode="exec"))
    return locals()

class ASTLoader(Loader):
    
    def transform(self, ast_tree): 
        #
        # transformations go here
        #
        return ast_tree
        
    def exec_module(self, module):
        with open(module.__spec__.name) as f:
            src =  f.read()
        ast_tree = ast.parse(src)
        ast_tree = self.transform(ast_tree)
        attrs = exec_ast_tree(ast_tree)

        # don't add ast_tree or self if it weren't defined in the module
        if attrs['ast_tree'] == ast_tree:
            del attrs['ast_tree']
        if attrs['self'] == self:
            del attrs['self']
        # https://docs.python.org/3/reference/import.html#import-mod-attrs
        # _init_module_attrs
        for k,v in attrs.items():
            setattr(module ,k, v)
        return module
        
class ASTFinder(MetaPathFinder):

    def find_spec(self, fullname, path, target = None):
        if fullname =="blah":
            return ModuleSpec(os.path.realpath(fullname + ".py"), ASTLoader())

def add_finder():
    sys.meta_path.insert(0, ASTFinder())


def main():
    add_finder()
    import blah
    print("dir(blah)", dir(blah))

if __name__ == "__main__":
    main()
