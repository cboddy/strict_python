import time
import contextlib
import builtins
import pdb
import sys
import time
from typing import Set
import itertools
py_import = builtins.__import__


class ImportProfiler:
    def __init__(self):
        self.import_start_times = {}
        self.import_end_times = {}

    @contextlib.contextmanager
    def profiling(self):
        builtins.__import__ = self.profile_import
        yield
        now = self.now
        """
        for mod_name in set(self.import_start_times.keys()).difference(self.import_end_times.keys()):
            self.import_end_times[mod_name] = now
        """
        builtins.__import__ = py_import

    def profile_import(self, *args, **kwargs):
        mod_name = args[0]
        is_new = mod_name not in self.import_start_times and mod_name not in self.sys_module_names()
        if is_new:
            self.import_start_times[mod_name] = self.now
        try:
            return py_import(*args, **kwargs)
        finally:
            # self.check_finished()
            if is_new:
                self.import_end_times[mod_name] = self.now

    @property
    def now(self) -> float:
        return time.perf_counter()

    def check_finished(self):
        finished_modules = self.sys_module_names()
        unfinished_modules = set(self.import_start_times.keys()).difference(set(self.import_end_times.keys()))
        newly_finished = finished_modules.intersection(unfinished_modules)
        now = self.now
        for mod_name in newly_finished:
            self.import_end_times[mod_name] = now

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
