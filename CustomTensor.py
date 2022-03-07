class CustomTensor:
    def __init__(self, data, shape):
        self.data = data
        self.shape = shape
        self.end_product = []
        tensor = []
        shape_length = len(self.shape)
        data_length = len(self.data)

        def calculate_tensor_length(s: list) -> int:
            r = 1
            for _ in s:
                r *= _
            return r
        tensor_length = calculate_tensor_length(shape)
        if tensor_length > data_length:
            for i in range(tensor_length-data_length):
                self.data.append(0)
        elif tensor_length < data_length:
            for i in range(data_length - tensor_length):
                self.data.pop(-1)

        def initial_packaging(d: list, s: list) -> list:
            for j in range(tensor_length//s[-1]):
                tensor.append([d.pop(0) for _ in range((s[-1]))])
            return tensor

        def recursive_packaging(t: list, s: list, length: int) -> list:
            if length == 0:
                return t
            else:
                temp = []
                for k in range(len(t) // s[length]):
                    temp.append([t.pop(0) for _ in range((s[length]))])
                return recursive_packaging(temp, s, length-1)

        def build() -> list:
            if shape_length == 1:
                return initial_packaging(self.data, self.shape)
            if shape_length == 0:
                return []
            return recursive_packaging(initial_packaging(self.data, self.shape), self.shape, shape_length - 2)

        self.end_product = build()

    def __str__(self):
        return str(self.end_product)

    def as_list(self):
        return self.end_product


if __name__ == '__main__':
    z = CustomTensor([1, 2, 4, 5, 1, 2, 3, 1, 4, 5, 1, 1, 2], [3, 4, 4])
    print(z)
    print(type(z))
    print(type(z.as_list()))
