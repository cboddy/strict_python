# strict-python

Tools for working with large python code-bases and teams.

Measuring, monitoring and mitigating start-times (import times).


### definitions

##### raw-import-time
The time tabken to import a module that is not already in `sys.modules`.

##### adjusted-import-time
The `raw-import-time` of a module after subtracting the `raw-import-time` of any other modules that are imported in that module.

### ideas
* an import profiler - iprof
* a custom [module loader](https://docs.python.org/3/reference/import.html#finders-and-loaders)?
    * load with `ast`
    * analyse AST 
    * apply invariants / transformations
    * compile modified AST with `builtin.__compile__`
* tag modules that should enforce some extra set of invariants in the AST analysis
    * should allow  side-effects?
    * flag if non-import time to compile exceeds some threshold or apply some z-score cut on adjusted-import time?
    * replace `__dict__` for classes after `__init__` with `__slots__`
    * allow some side-effects - simple list/dicts with literals 

### refs
https://docs.python.org/3/reference/import.html#finders-and-loaders
https://www.python.org/dev/peps/pep-0451/#terms-and-concepts
https://docs.python.org/3/library/importlib.html#importlib.abc.Loader
https://docs.python.org/3/library/importlib.html#importlib.abc.MetaPathFinder
https://instagram-engineering.com/python-at-scale-strict-modules-c0bb9245c834
https://bayesianbrad.github.io/posts/2017_loader-finder-python.html
