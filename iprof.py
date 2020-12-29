import time
import contextlib
import builtins
import pdb
import sys
import time
from typing import Set, Optional
import itertools
import collections
from pprint import pprint 
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
        builtins.__import__ = py_import

    def profile_import(self, *args, **kwargs):
        mod_name = args[0]
        is_new = mod_name not in self.import_start_times and mod_name not in self.sys_module_names
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

    @property
    def sys_module_names(self) -> Set[str]:
        return set(sys.modules.keys())

    def raw_times(self):
        """The raw time duration in seconds that it took to import each module"""
        return {mod_name: self.import_end_times[mod_name] - self.import_start_times[mod_name]
                for mod_name in self.import_end_times}

    def non_import_times(self):
        """The time duration in seconds that it took to import each module after subtracting 
        the time taken to import any modules were imported while importing this module"""
        raw_times = self.raw_times()
        non_import_times = {}
        for mod_name in raw_times:
            raw_time = raw_times[mod_name]
            for edge_mod_name in self.adjacency_list[mod_name]:
                raw_time -= raw_times[edge_mod_name] 
            non_import_times[mod_name] = raw_time    
        return non_import_times
        
def main():
    prof = ImportProfiler()
    with prof.profiling():
        import pandas
    # ten worst offenders
    pprint(sorted(prof.non_import_times().items(), key=lambda tup: tup[1], reverse=True)[:10])
    return prof


if __name__ == "__main__":
    main()
