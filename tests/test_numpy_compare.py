import os
import timeit
import importlib.util
import subprocess
import sysconfig

import numpy as np


def compile_extension():
    if os.path.exists("tensor_ext.so"):
        os.remove("tensor_ext.so")
    if os.path.exists("tensor_ext.o"):
        os.remove("tensor_ext.o")
    if os.path.exists("add_arrays.o"):
        os.remove("add_arrays.o")
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
    pow_b = [2] * len(a)
    np_a = np.array(a, dtype=np.int32)
    np_b = np.array(b, dtype=np.int32)
    np_pow_b = np.array(pow_b, dtype=np.int32)

    def add_ext():
        tensor_ext.add_flat(a, b)

    def add_py():
        [x + y for x, y in zip(a, b)]

    def add_np():
        (np.array(a, dtype=np.int32) + np.array(b, dtype=np.int32)).tolist()

    def sub_ext():
        tensor_ext.sub_flat(a, b)

    def sub_py():
        [x - y for x, y in zip(a, b)]

    def sub_np():
        (np.array(a, dtype=np.int32) - np.array(b, dtype=np.int32)).tolist()

    def mul_ext():
        tensor_ext.mul_flat(a, b)

    def mul_py():
        [x * y for x, y in zip(a, b)]

    def mul_np():
        (np.array(a, dtype=np.int32) * np.array(b, dtype=np.int32)).tolist()

    def div_ext():
        tensor_ext.div_flat(a, b)

    def div_py():
        [x // y for x, y in zip(a, b)]

    def div_np():
        (np.array(a, dtype=np.int32) // np.array(b, dtype=np.int32)).tolist()

    def mod_ext():
        tensor_ext.mod_flat(a, b)

    def mod_py():
        [x % y for x, y in zip(a, b)]

    def mod_np():
        (np.array(a, dtype=np.int32) % np.array(b, dtype=np.int32)).tolist()

    def pow_ext():
        tensor_ext.pow_flat(a, pow_b)

    def pow_py():
        [x ** 2 for x in a]

    def pow_np():
        (np.array(a, dtype=np.int32) ** np_pow_b).tolist()

    def sum_ext():
        tensor_ext.sum_flat(a)

    def sum_py():
        total = 0
        for x in a:
            total += x
        return total

    def sum_np():
        int(np.sum(np_a))

    def dot_ext():
        tensor_ext.dot_flat(a, b)

    def dot_py():
        total = 0
        for x, y in zip(a, b):
            total += x * y
        return total

    def dot_np():
        int(np.dot(np.array(a, dtype=np.int32), np.array(b, dtype=np.int32)))

    assert tensor_ext.add_flat(a, b) == list((np_a + np_b).tolist())
    assert tensor_ext.sub_flat(a, b) == list((np_a - np_b).tolist())
    assert tensor_ext.mul_flat(a, b) == list((np_a * np_b).tolist())
    assert tensor_ext.div_flat(a, b) == list((np_a // np_b).tolist())
    assert tensor_ext.mod_flat(a, b) == list((np_a % np_b).tolist())
    assert tensor_ext.pow_flat(a, pow_b) == list((np_a ** np_pow_b).tolist())
    assert tensor_ext.sum_flat(a) == int(np.sum(np_a))
    assert tensor_ext.dot_flat(a, b) == int(np.dot(np_a, np_b))

    # Compare execution times
    timings = {
        "add_py": _timed(add_py),
        "add_ext": _timed(add_ext),
        "add_np": _timed(add_np),
        "sub_py": _timed(sub_py),
        "sub_ext": _timed(sub_ext),
        "sub_np": _timed(sub_np),
        "mul_py": _timed(mul_py),
        "mul_ext": _timed(mul_ext),
        "mul_np": _timed(mul_np),
        "div_py": _timed(div_py),
        "div_ext": _timed(div_ext),
        "div_np": _timed(div_np),
        "mod_py": _timed(mod_py),
        "mod_ext": _timed(mod_ext),
        "mod_np": _timed(mod_np),
        "pow_py": _timed(pow_py),
        "pow_ext": _timed(pow_ext),
        "pow_np": _timed(pow_np),
        "sum_py": _timed(sum_py),
        "sum_ext": _timed(sum_ext),
        "sum_np": _timed(sum_np),
        "dot_py": _timed(dot_py),
        "dot_ext": _timed(dot_ext),
        "dot_np": _timed(dot_np),
    }

    for op in ["add", "sub", "mul", "div", "mod", "pow", "sum", "dot"]:
        assert timings[f"{op}_ext"] < timings[f"{op}_py"]

