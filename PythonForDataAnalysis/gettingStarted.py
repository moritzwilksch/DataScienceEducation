def squares(n):
    for i in range(n):
        yield i ** 2
gen = squares(15)
for x in gen:
    print(x)