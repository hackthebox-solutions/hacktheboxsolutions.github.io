
while True:
    print("ctrl+c to exit\n")
    #title= input('\nEnter title')
    #content= input('\nEnter content')

    lines = []
    while True:
        line = input()
        if line!="exit":
            lines.append(line)
        else:
            break
    text = '\n'.join(lines)
    print(text)

    #f= open(title+" Writeup.md","w+")
    #f.write(content)
    #f.close()