import time
import contextlib
import builtins
import pdb
import sys
import time
from typing import Set, Optional
import itertools
import collections
py_import = builtins.__import__


class ImportProfiler:
    def __init__(self):
        self.import_start_times = {}
        self.import_end_times = {}
        self.stack = collections.deque()
        # graph of packages
        self.adjacency_list = collections.defaultdict(list)

    @contextlib.contextmanager
    def profiling(self):
        builtins.__import__ = self.profile_import
        yield
        now = self.now
        builtins.__import__ = py_import

    def profile_import(self, *args, **kwargs):
        mod_name = args[0]
        is_new = mod_name not in self.import_start_times and mod_name not in self.sys_module_names()
        if is_new:
            if self.head:
                self.adjacency_list[self.head].append(mod_name)
            self.stack.append(mod_name)
            self.import_start_times[mod_name] = self.now
        try:
            return py_import(*args, **kwargs)
        finally:
            if is_new:
                self.import_end_times[mod_name] = self.now
                self.stack.pop()

    @property 
    def head(self) -> Optional[str]:
        """Get the last module name in the stack or None if the stack is empty"""
        try:
            return self.stack[-1]
        except IndexError:
            return None

    @property
    def now(self) -> float:
        return time.perf_counter()

    def sys_module_names(self) -> Set[str]:
        return set(sys.modules.keys())

    def times(self):
        return {mod_name: self.import_end_times[mod_name] - self.import_start_times[mod_name]
                for mod_name in self.import_end_times}

        
def run():
    prof = ImportProfiler()
    with prof.profiling():
        import pandas
    return prof


if __name__ == "__main__":
    run()
