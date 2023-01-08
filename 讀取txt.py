f = open('文本.txt', 'r')
print(f.read())

for line in f:
    print(line)

f.close()