test = "text\ntext\ntext"
a = 0
for line in test.split():
    print(f"{a}.{line}")
    a += 1