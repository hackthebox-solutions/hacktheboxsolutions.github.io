import glob
mlist= glob.glob("*.md")
m=[]
for i in mlist:
    i=i.replace("wo", "w/o")
    m.append(i)
print(m)

for i in range(0, len(m)):
    print("      - "+str(i+1)+". "+m[i]+": Retired/"+mlist[i])