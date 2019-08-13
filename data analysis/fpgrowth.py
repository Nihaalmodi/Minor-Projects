trans, transline, freq_items,rules=[],[],[],[]
support_count, freq_pattern, tree_count_flag,confidence={},{},{},{}
temp=""
upper_div=0
lower_div=0
minimum_support_value=80
minimum_confidence_value=0.6

class FPNode(object):
    def __init__(self, value, count, parent):
        self.value = value
        self.count = count
        self.parent = parent
        self.children = []

    def has_child(self, value):
        for node in self.children:
            if node.value == value:
                return True
        return False

    def get_child(self, value):
        for node in self.children:
            if node.value == value:
                return node
        return None

    def add_child(self, value, count):
        child = FPNode(value, count, self)
        self.children.append(child)
        return child

def search_tree(node,member,count,modify):
    for item in node.children:
        if(item.has_child(member)):
            node1=item.get_child(member)
        # if(modify=="1"):
                # node1.count=node.count-1
            if(count):
                continue
            else:
                return node1
        else:
            if(node.get_child(item)!=None):
                return search_tree(node.get_child(item),member,count)

with open("transactions.txt","r") as file:
		for i in file.read():
			if(i=="\n"):
				trans.append(transline)
				transline=[]
			elif(i==" "):
				transline.append(temp)
				if temp not in support_count.keys():
					support_count[temp]=1
				else:
					support_count[temp]=support_count[temp]+1
				temp=""
			else:
				temp=temp+str(i)
#------------frequent pattern-------------#
for i in support_count.keys():
	if support_count[i]>minimum_support_value+1:
		freq_pattern[i]=support_count[i]
print("Frequent Pattern")
print(freq_pattern)


for i in range(0,len(trans)):
	for j in freq_pattern.keys():
		if j in trans[i]:
			transline.append(j)
	if(transline!=[]):
		freq_items.append(transline)
	transline=[]

#-----------define root----------------------#
root = FPNode(None,None,None)
tree_count=support_count
for item in support_count.keys():
    tree_count_flag[item]=0
flag=0
tree=root
for itemline in freq_items:
    for item in itemline:
        if(tree.has_child(item)):
            prev_item=item
            tree=tree.get_child(item)
            flag=1
        else:
            if(flag):
                if(tree_count_flag[item]):
                    search_tree(root,item,0,1)
                    tree=tree.add_child(item,tree_count[item])
                    tree_count_flag[item]+=1
                else:
                    tree=tree.add_child(item,tree_count[item])
                    tree_count_flag[item]+=1
                flag=0
            else:
                tree=tree.add_child(item,tree_count[item])
                tree_count_flag[item]+=1
    tree=root
count=0
for j in freq_pattern.keys():
    for k in freq_pattern.keys():
        for n in freq_pattern.keys():
            if(j!=k and k!=n and j!=n):
                node1=None
                while(True):
                    node1 = search_tree(root,j,count,0)
                    count+=1
                    if(node1 is None):
                        count=0
                        break
                    else:
                        node2 = node1.get_child(k)
                        if(node2!=None):
                            lower_div+=node1.count+node2.count
                            node3 = node2.get_child(n)
                            if(node3!=None):
                                upper_div+=node1.count+node2.count+node3.count
                if(upper_div!=0):
                    confidence[(j,k,n)]=(float(lower_div)/float(upper_div),lower_div)
                    if(confidence[(j,k,n)][0]>minimum_confidence_value):
                        rules.append((j,k,n))

                upper_div,lower_div=0,0

# rules=sorted(rules, key=lambda x: support_count[x[0]]+support_count[x[1]]+support_count[x[2]],reverse=True)
with open("output.txt","w") as f:
    f.write("Rule           Confidence   Support\n" )
    for x in range(0,len(rules)):
        print(str(rules[x][0] )+ ", " + str(rules[x][1]) + " ==> " + str(rules[x][2]) + "  " + str(confidence[rules[x][0],rules[x][1],rules[x][2]][0]) +"  "+str(confidence[rules[x][0],rules[x][1],rules[x][2]][1])+"         ")
        f.write(str(rules[x][0] )+ ", " + str(rules[x][1]) + " ==> " + str(rules[x][2]) + "  " + str(confidence[rules[x][0],rules[x][1],rules[x][2]][0]) +"  "+str(confidence[rules[x][0],rules[x][1],rules[x][2]][1])+"         " +"\n")
