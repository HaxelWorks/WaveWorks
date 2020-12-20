def f():
    while True:
        print("before")
        val = yield
        print('after')
        yield val*10

next(g := f())
g.send(1)

next(g)
g.send(10)

next(g)
g.send(0.5)

