import os
import timeit
import importlib
import subprocess
import sysconfig

import numpy as np


def compile_extension():
    if os.path.exists("tensor_ext.so"):
        return
    include = sysconfig.get_paths()["include"]
    subprocess.check_call(["gcc", "-O3", "-fPIC", "-c", "tensor_ext.c", f"-I{include}", "-o", "tensor_ext.o"])
    subprocess.check_call(["nasm", "-felf64", "add_arrays.s", "-o", "add_arrays.o"])
    subprocess.check_call(["gcc", "-shared", "tensor_ext.o", "add_arrays.o", "-o", "tensor_ext.so"])


def load_extension():
    compile_extension()
    spec = importlib.util.spec_from_file_location("tensor_ext", os.path.join(os.getcwd(), "tensor_ext.so"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _timed(callable_obj):
    return timeit.timeit(callable_obj, number=100)


def test_operations_against_numpy():
    tensor_ext = load_extension()
    a = list(range(10000))
    b = list(range(1, 10001))
    np_a = np.array(a, dtype=np.int32)
    np_b = np.array(b, dtype=np.int32)

    def add_ext():
        tensor_ext.add_flat(a, b)

    def add_np():
        (np.array(a, dtype=np.int32) + np.array(b, dtype=np.int32)).tolist()

    def sub_ext():
        tensor_ext.sub_flat(a, b)

    def sub_np():
        (np.array(a, dtype=np.int32) - np.array(b, dtype=np.int32)).tolist()

    def mul_ext():
        tensor_ext.mul_flat(a, b)

    def mul_np():
        (np.array(a, dtype=np.int32) * np.array(b, dtype=np.int32)).tolist()

    def div_ext():
        tensor_ext.div_flat(a, b)

    def div_np():
        (np.array(a, dtype=np.int32) // np.array(b, dtype=np.int32)).tolist()

    assert tensor_ext.add_flat(a, b) == list((np_a + np_b).tolist())
    assert tensor_ext.sub_flat(a, b) == list((np_a - np_b).tolist())
    assert tensor_ext.mul_flat(a, b) == list((np_a * np_b).tolist())
    assert tensor_ext.div_flat(a, b) == list((np_a // np_b).tolist())

    assert _timed(add_ext) < _timed(add_np)
    assert _timed(sub_ext) < _timed(sub_np)
    assert _timed(mul_ext) < _timed(mul_np)
    assert _timed(div_ext) < _timed(div_np)
