def return_x(self):
    return self.x

class Foo():
    def __init__(self):
        self.x = 3

foo = Foo()
Foo.return_x = return_x
print(foo.return_x())
