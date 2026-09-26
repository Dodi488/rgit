import zlib

#hash = "f48405104d79ecbdb16ce311ac7fd862c9343aca"
hash = "a10f4578915f6f9d0aba735cd8b57364cc9235ce"

#path = ".rgit/objects/f4/8405104d79ecbdb16ce311ac7fd862c9343aca"
path = ".rgit/objects/a1/0f4578915f6f9d0aba735cd8b57364cc9235ce"

with open(path, "rb") as f:
    file = f.read()

descompressed = zlib.decompress(file)
print(descompressed)
print()
string = descompressed[2:-1].split(b" ")[1:]
#theory = map(lambda x: x.replace("\\x00", " ", 1), string)
#string = map(lambda x: x.split(" "), list(theory))
#print(list(string))

print(string)

lines = []

for i in range(1, len(string)):
    last_line = string[i - 1]
    line = string[i]

    number = repr(last_line[-6:]).replace("\x00", "0")

    if (i + 1) != len(string):
        name = repr((string[i])[:-27])
        hash = (string[i])[-26:-7]
    else:
        name = repr((string[i])[:-20])
        hash = (string[i])[-26:-6]

    lines.append(f"{number} tree {hash.hex()}    {name}")

    final = "\n".join(lines)

print(final)

#string = descompressed.split(b"\x00")[1]
#string = repr(string)[2:-1]
#string = string.replace(r"\n", "\n")
#print(string)
