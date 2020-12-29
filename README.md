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
