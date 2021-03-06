import glob
import string
from collections import OrderedDict 
  
import math
from stop_words import get_stop_words
import re
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
class treenode(object):
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1
 

class avltree(object):
 
   
    def insert(self, root, key):
     
         
        if not root:
            return treenode(key)
        elif key < root.val:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
 
       
        root.height = 1 + max(self.getheight(root.left),
                           self.getheight(root.right))
 
         
        balance = self.getbalance(root)
 
        if balance > 1 and key < root.left.val:
            return self.rightrotate(root)
 
       
        if balance < -1 and key >= root.right.val:
            return self.leftrotate(root)
 
       
        if balance > 1 and key > root.left.val:
            root.left = self.leftrotate(root.left)
            return self.rightrotate(root)
 
       
        if balance < -1 and key <= root.right.val:
            root.right = self.rightrotate(root.right)
            return self.leftrotate(root)
 
        return root
 
    def leftrotate(self, z):
 
        y = z.right
        T2 = y.left
 
       
        y.left = z
        z.right = T2
 
         
        z.height = 1 + max(self.getheight(z.left),
                         self.getheight(z.right))
        y.height = 1 + max(self.getheight(y.left),
                         self.getheight(y.right))
 
       
        return y
 
    def rightrotate(self, z):
 
        y = z.left
        T3 = y.right
 
       
        y.right = z
        z.left = T3
 
       
        z.height = 1 + max(self.getheight(z.left),
                        self.getheight(z.right))
        y.height = 1 + max(self.getheight(y.left),
                        self.getheight(y.right))
 
         
        return y
 
    def getheight(self, root):
        if not root:
            return 0
 
        return root.height
 
    def getbalance(self, root):
        if not root:
            return 0
 
        return self.getheight(root.left) - self.getheight(root.right)
 
    def preorder(self, root,prelist):
 
        if not root:
            return []
 
        prelist.append(root.val)
        self.preorder(root.left,prelist)
        self.preorder(root.right,prelist)
        return prelist
 

class TrieNode():
    def __init__(self):
        self.children = [None]*26
        self.isEndOfWord = None
   

class Trie:
     
   
    def __init__(self):
        self.root = self.getnode()
 
    def getnode(self):
     
        return TrieNode()
 
    def chartoindex(self,ch):
        return ord(ch)-ord('a')
 
 
    def insert(self,key,id):
         
         
        p = self.root
        length = len(key)
        for level in range(length):
            if self.chartoindex(key[level]) >=0 and self.chartoindex(key[level]) <26:
                index = self.chartoindex(key[level])
               
                if not p.children[index]:
                    p.children[index] = self.getnode()
                p = p.children[index]
            else:
                return
           
 
        avl=avltree();
        root=None
       
       
        root=avl.insert(None,id);

       
       
        p.isEndOfWord = root;
       

 
    def search(self, key):
         
       
        p = self.root
        length = len(key)
        for level in range(length):
            if self.chartoindex(key[level]) >=0 and self.chartoindex(key[level]) <26:
                index = self.chartoindex(key[level])
                if not p.children[index]:
                    return None
                p = p.children[index]
            else:
                return None
 
        if p != None and p.isEndOfWord :
            return p.isEndOfWord
    def dothis(self,key,node):
        p = self.root
        length = len(key)
        for level in range(length):
            if self.chartoindex(key[level]) >=0 and self.chartoindex(key[level]) <26:
                index = self.chartoindex(key[level])
               
                p = p.children[index]
           
 
        if p != None and p.isEndOfWord :
            p.isEndOfWord=node




def createinvertedindex(words,t,id):
    for i in words:
       
        node=t.search(i)
        if node:

            avl=avltree()
            node=avl.insert(node,id)
            t.dothis(i,node)


        else:
            t.insert(i,id)


def edit(str1, str2, m, n):
 
  
    if m == 0:
        return n
 
  
    if n == 0:
        return m
 
   
    if str1[m-1] == str2[n-1]:
        return edit(str1, str2, m-1, n-1)
 
    return 1 + min(edit(str1, str2, m, n-1),    # Insert
                   edit(str1, str2, m-1, n),    # Remove
                   edit(str1, str2, m-1, n-1)    # Replace
                   )
def findLen(str): 
    counter = 0    
    for i in str: 
        counter += 1
    return counter 
def Sum(myDict): 
      
    sum = 0
    for i in myDict: 
        sum = sum + myDict[i]*myDict[i]
      
    return math.sqrt(sum)





list_of_files = glob.glob('./Downloaded_Files/*.txt')   
id=0
orddic={}
t=Trie()
di={}
allwords=[]
stopwords=get_stop_words('english')
for fl in list_of_files:
    id=id+1
    num=int(fl[19:-4])
    orddic[id]=num
    fh=open(fl,encoding="utf8")
    punc = '''!???()???-???[]{};:'"\, <>./?@#$%^&*_~'''
    for line in fh:
        line = line.replace('???','')
        line = line.replace('???','')
        line= line.replace("???","")
        words=line.split()
        for ele in punc:  
            line = line.replace(ele, " ")
        words=line.split()
        words=[x.lower() for x in words]
        for i in words:
            if i in stopwords:
                words.remove(i)
        
        allwords.extend(words)
        createinvertedindex(words,t,id)
allwords = list(dict.fromkeys(allwords))
avl=avltree()
for i in allwords:

    node=t.search((i))
    ls=[]
    di={}
    ls=avl.preorder(node,ls)
    for j in ls:
        if j in di:
            di[j]=di[j]+1
        else:
            di[j]=1
    ls=list(dict.fromkeys(ls))
    if node:
        with open('postinglist.txt','a') as f:

            print(i,end="=>",file=f)
            print(len(ls),end="  ",file=f)
            for j in di:
                print(j,end="-",file=f)
                print(di[j],end=";",file=f)
            print("\n",file=f)

N=1400

query=input("Enter query\n")

words=query.split()
words=[x.lower() for x in words]
for i in words:
    if i in stopwords:
        words.remove(i)
for si in words:
    zero=99999
    if si not in allwords:

        print(si,end=" ")
        print("not found in dicionary!!Do you mean ")
        for sj in allwords:
            
          
            hmm=edit(si,sj,len(si),len(sj))
            if hmm<zero:
                zero=hmm
                replac=sj



        print(replac)
        print("For yes click 1 else enter 0")
        flag=int(input())
        if flag==1:
            l=words.index(si)
            words[l]=replac

exits=[]
tf={}
for i in words:
    if i not in exits:
        exits.append(i)
        tf[i]=1
    else:
        words.remove(i)
        tf[i]=tf[i]+1


idf={}
dtf={}
docs=[]
for i in words:
    dtf[i]={}
for i in words:

    node=t.search((i))
    ls=[]
    di={}
    ls=avl.preorder(node,ls)

    for j in ls:
        if j in di:
            di[j]=di[j]+1
        else:
            di[j]=1
    ls=list(dict.fromkeys(ls))
    df=len(ls)
    
    if node:
        idf[i]=(1+math.log(tf[i]))*(math.log(N/df))
        for j in di:
            dtf[i][j]=1+math.log(di[j])
            if j not in docs:
                docs.append(j)


total={}
for i in words:
    total[i]=Sum(dtf[i])      
score={}
docscore={}
for t in words:
    score[t]={}     
for d in docs:
    docscore[d]=0
    
    for t in words:
        score[t][d]=0

        if d in dtf[t]:

            score[t][d]=score[t][d]+(idf[t]*dtf[t][d]/total[t])
            
            docscore[d]=docscore[d]+score[t][d]


        else:
            score[t][d]=0

docscore={k: v for k, v in sorted(docscore.items(), key=lambda item: item[1])}
count=0
res=OrderedDict(reversed(list(docscore.items()))) 
print("The top 10 urls that are most relavant to query are :")
print(" ")
for i in res:
    count=count+1
    x=orddic[i]
    file=str(x)+".txt"
    s="./Downloaded_Files/" + file
    
    fh=open(s,encoding="utf8")
    for line in fh:
        print(line,end="")
        break
    if count==10:
        break