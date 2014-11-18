from re import findall
from numpy import array,matrix,linalg,full
global nflIndex
nflIndex={'Arizona':0,'Atlanta':1,'Baltimore':2,'Buffalo':3,'Carolina':4,
          'Chicago':5,'Cincinnati':6,'Cleveland':7,'Dallas':8,'Denver':9,
          'Detroit':10,'GB':11,'Houston':12,'Indianapolis':13,'Jacksonville':14,
          'KC':15,'Miami':16,'Minnesota':17,'NE':18,'NO':19,'NYG':20,'NYJ':21,
          'Oakland':22,'Philadelphia':23,'Pittsburgh':24,'SD':25,'SF':26,
          'Seattle':27,'STL':28,'TB':29,'Tennessee':30,'Washington':31}
def read_games():
    infile= open('nfl games.txt')
    content=infile.readlines()
    count=0
    global nfl,c,b,ranks
    b=full((32,1),0)
    c=full((32,32),0)
    #Cr=b
    #solving for r
    #for Cii, or C[i][i],= total games played+2
    #b is 1+difference(W-L)/2...actually (w-L)*2
    nfl={}
    for i in range(len(content)): #content follows: team,score,team,score
        lst=content[i].split()
        if lst[0] not in nfl: #create new key if not already set
            nfl[lst[0]]=[]
            #print nfl
        if lst[2] not in nfl: #same thing
            nfl[lst[2]]=[]
            #print nfl
        if int(lst[1])>int(lst[3]): 
            if lst[0] and lst[2] in nflIndex: #stops any errant spelling mistakes
                c[nflIndex[lst[0]]][nflIndex[lst[2]]]-=1 #in matrix, if team 0 played team 2
                c[nflIndex[lst[2]]][nflIndex[lst[0]]]-=1 #must give -1 for game played as per Colley method
            nfl[lst[0]]+='W'
            nfl[lst[2]]+='L'
        if int(lst[1])<int(lst[3]):
            if lst[0] and lst[2] in nflIndex:
                c[nflIndex[lst[0]]][nflIndex[lst[2]]]-=1
                c[nflIndex[lst[2]]][nflIndex[lst[0]]]-=1
            nfl[lst[2]]+='W'
            nfl[lst[0]]+='L'
        if int(lst[1])==int(lst[3]):
            if lst[0] and lst[2] in nflIndex:
                c[nflIndex[lst[0]]][nflIndex[lst[2]]]-=1
                c[nflIndex[lst[2]]][nflIndex[lst[0]]]-=1
            nfl[lst[2]]+='T' #decided that ties will get no value
            nfl[lst[0]]+='T' #but do count towards total games played
        if len(content[i])!=0:
            count+=1 #a way to check if loop looked at all games
    for key in nflIndex:
        #if key in nfl:
        c[nflIndex[key]][nflIndex[key]]=len(nfl[key])+2 
        b[nflIndex[key]]=1+(nfl[key].count('W')-nfl[key].count('L'))*.5
    ranks=linalg.solve(c,b) #actual linear alegbra solve, Cr=b
    #looking for r
    return count

