# CustomTensor
Custom N-dimensional Tensor

## Building the extension

The tests compile `tensor_ext.c` together with the assembly file
`add_arrays.s`. On Linux this requires `gcc` and `nasm` to be available
on your `PATH`.

### Windows notes

On Windows 11 you can build the extension using the MinGW toolchain and
NASM. Install [MinGW-w64](https://www.mingw-w64.org/) and NASM, then
open a terminal where both tools are reachable. Assuming Python is
installed in `C:\Python312`, run:

```bash
gcc -O3 -Ic:\Python312\include -c tensor_ext.c -o tensor_ext.o
nasm -f win64 add_arrays.s -o add_arrays.obj
gcc -shared tensor_ext.o add_arrays.obj \
    -Lc:\Python312\libs -lpython312 -o tensor_ext.pyd
```

Place the resulting `tensor_ext.pyd` next to the Python files and run
the tests with:

```bash
pip install numpy pytest
pytest -q
```
