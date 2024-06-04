a = {1:1, 2:2, 3:3}
b = {1:1, 2:2, 4:3}

exclusions = set(a.keys())
exclusions.update(set(b.keys()))
print(exclusions)

a = "asd"
print(a[:-0:])