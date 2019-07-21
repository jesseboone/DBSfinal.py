
def getField (line, field) :
    l = line.split(field, 1)
    if l[0] == line :
        return 'NA'
    else :
        print(l)
        l = l[1].lstrip(":")
        print(l)
        l = l.split()
        print(l)
        return l[0]

str1 = "DocID:570 Age:34 Gender:2"
str2 = getField(str1, "Age")
print(str2)
