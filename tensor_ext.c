#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>

extern void add_arrays(int *dest, const int *a, const int *b, long count);
extern void sub_arrays(int *dest, const int *a, const int *b, long count);
extern void mul_arrays(int *dest, const int *a, const int *b, long count);
extern void div_arrays(int *dest, const int *a, const int *b, long count);
extern int dot_product(const int *a, const int *b, long count);
extern void mod_arrays(int *dest, const int *a, const int *b, long count);
extern void pow_arrays(int *dest, const int *a, const int *b, long count);
extern int sum_array(const int *a, long count);

static PyObject* pack_recursive(int *data, long *shape, int depth, int shape_len, long offset) {
    PyObject *list = PyList_New(shape[depth]);
    if (!list) return NULL;
    if (depth == shape_len - 1) {
        for (long i = 0; i < shape[depth]; ++i) {
            PyObject *item = PyLong_FromLong(data[offset + i]);
            PyList_SET_ITEM(list, i, item);
        }
    } else {
        long stride = 1;
        for (int k = depth + 1; k < shape_len; ++k) stride *= shape[k];
        for (long i = 0; i < shape[depth]; ++i) {
            PyObject *sub = pack_recursive(data, shape, depth + 1, shape_len, offset + i * stride);
            if (!sub) { Py_DECREF(list); return NULL; }
            PyList_SET_ITEM(list, i, sub);
        }
    }
    return list;
}

static PyObject* build_tensor_fast(PyObject *self, PyObject *args) {
    PyObject *data_obj, *shape_obj;
    if (!PyArg_ParseTuple(args, "OO", &data_obj, &shape_obj))
        return NULL;

    Py_ssize_t shape_len = PyList_Size(shape_obj);
    Py_ssize_t data_len = PyList_Size(data_obj);

    long *shape = malloc(shape_len * sizeof(long));
    if (!shape) return PyErr_NoMemory();
    for (Py_ssize_t i = 0; i < shape_len; ++i) {
        shape[i] = PyLong_AsLong(PyList_GetItem(shape_obj, i));
    }

    long tensor_len = 1;
    for (Py_ssize_t i = 0; i < shape_len; ++i) tensor_len *= shape[i];

    int *data = malloc(tensor_len * sizeof(int));
    if (!data) { free(shape); return PyErr_NoMemory(); }

    Py_ssize_t copy_len = data_len < tensor_len ? data_len : tensor_len;
    for (Py_ssize_t i = 0; i < copy_len; ++i)
        data[i] = (int)PyLong_AsLong(PyList_GetItem(data_obj, i));
    for (Py_ssize_t i = copy_len; i < tensor_len; ++i)
        data[i] = 0;

    PyObject *result = pack_recursive(data, shape, 0, (int)shape_len, 0);
    free(data);
    free(shape);
    return result;
}

static PyObject* binary_op(PyObject *self, PyObject *args,
                          void (*op)(int*, const int*, const int*, long)) {
    PyObject *a_obj, *b_obj;
    if (!PyArg_ParseTuple(args, "OO", &a_obj, &b_obj))
        return NULL;
    Py_ssize_t len_a = PyList_Size(a_obj);
    if (len_a != PyList_Size(b_obj)) {
        PyErr_SetString(PyExc_ValueError, "length mismatch");
        return NULL;
    }
    int *a = malloc(len_a * sizeof(int));
    int *b = malloc(len_a * sizeof(int));
    int *dest = malloc(len_a * sizeof(int));
    if (!a || !b || !dest) { free(a); free(b); free(dest); return PyErr_NoMemory(); }
    for (Py_ssize_t i = 0; i < len_a; ++i) {
        a[i] = (int)PyLong_AsLong(PyList_GetItem(a_obj, i));
        b[i] = (int)PyLong_AsLong(PyList_GetItem(b_obj, i));
    }
    op(dest, a, b, len_a);
    PyObject *result = PyList_New(len_a);
    if (!result) { free(a); free(b); free(dest); return NULL; }
    for (Py_ssize_t i = 0; i < len_a; ++i) {
        PyObject *item = PyLong_FromLong(dest[i]);
        PyList_SET_ITEM(result, i, item);
    }
    free(a); free(b); free(dest);
    return result;
}

static PyObject* add_flat(PyObject *self, PyObject *args) {
    return binary_op(self, args, add_arrays);
}

static PyObject* sub_flat(PyObject *self, PyObject *args) {
    return binary_op(self, args, sub_arrays);
}

static PyObject* mul_flat(PyObject *self, PyObject *args) {
    return binary_op(self, args, mul_arrays);
}

static PyObject* div_flat(PyObject *self, PyObject *args) {
    return binary_op(self, args, div_arrays);
}

static PyObject* mod_flat(PyObject *self, PyObject *args) {
    return binary_op(self, args, mod_arrays);
}

static PyObject* pow_flat(PyObject *self, PyObject *args) {
    return binary_op(self, args, pow_arrays);
}

static PyObject* dot_flat(PyObject *self, PyObject *args) {
    PyObject *a_obj, *b_obj;
    if (!PyArg_ParseTuple(args, "OO", &a_obj, &b_obj))
        return NULL;
    Py_ssize_t len_a = PyList_Size(a_obj);
    if (len_a != PyList_Size(b_obj)) {
        PyErr_SetString(PyExc_ValueError, "length mismatch");
        return NULL;
    }
    int *a = malloc(len_a * sizeof(int));
    int *b = malloc(len_a * sizeof(int));
    if (!a || !b) { free(a); free(b); return PyErr_NoMemory(); }
    for (Py_ssize_t i = 0; i < len_a; ++i) {
        a[i] = (int)PyLong_AsLong(PyList_GetItem(a_obj, i));
        b[i] = (int)PyLong_AsLong(PyList_GetItem(b_obj, i));
    }
    int result = dot_product(a, b, len_a);
    free(a); free(b);
    return PyLong_FromLong(result);
}

static PyObject* sum_flat(PyObject *self, PyObject *args) {
    PyObject *a_obj;
    if (!PyArg_ParseTuple(args, "O", &a_obj))
        return NULL;
    Py_ssize_t len_a = PyList_Size(a_obj);
    int *a = malloc(len_a * sizeof(int));
    if (!a) return PyErr_NoMemory();
    for (Py_ssize_t i = 0; i < len_a; ++i)
        a[i] = (int)PyLong_AsLong(PyList_GetItem(a_obj, i));
    int result = sum_array(a, len_a);
    free(a);
    return PyLong_FromLong(result);
}

static PyMethodDef TensorMethods[] = {
    {"build_tensor_fast", build_tensor_fast, METH_VARARGS, "Build tensor using C/asm"},
    {"add_flat", add_flat, METH_VARARGS, "Add two flat int lists"},
    {"sub_flat", sub_flat, METH_VARARGS, "Subtract two flat int lists"},
    {"mul_flat", mul_flat, METH_VARARGS, "Multiply two flat int lists"},
    {"div_flat", div_flat, METH_VARARGS, "Divide two flat int lists"},
    {"mod_flat", mod_flat, METH_VARARGS, "Modulus of two flat int lists"},
    {"pow_flat", pow_flat, METH_VARARGS, "Power of two flat int lists"},
    {"dot_flat", dot_flat, METH_VARARGS, "Dot product of two flat int lists"},
    {"sum_flat", sum_flat, METH_VARARGS, "Sum of flat int list"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef tensormodule = {
    PyModuleDef_HEAD_INIT,
    "tensor_ext",
    NULL,
    -1,
    TensorMethods
};

PyMODINIT_FUNC PyInit_tensor_ext(void) {
    return PyModule_Create(&tensormodule);
}

