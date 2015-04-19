from re import findall
from numpy import array,matrix,linalg,full
from numpy import array,matrix,linalg,full
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from datetime import date

def generate_index(league):
    """
    type in either 'nfl', 'nba', 'mlb', or 'cfb' in ()
    creates an index dictionary for teams with value
    associated to alphabetical position
    A:0, B:1, etc...
    """
    global index  
    if league == 'nfl':
        content = BeautifulSoup(
            urlopen(
        'http://www.masseyratings.com/scores.php?s=262648&sub=262648&all=1&mode=3&sch=on&format=0')).find('pre')
    elif league == 'mlb':
        content = BeautifulSoup(
            urlopen(
                'http://www.masseyratings.com/scores.php?s=278762&sub=14342&all=1')).find('pre')
    elif league == 'nba':
        content = BeautifulSoup(
            urlopen(
                'http://www.masseyratings.com/scores.php?s=267444&sub=267444&all=1')).find('pre') 
    content = content.string.replace('\n',' ').replace('@',' ')
    content = re.sub('O\d+',' ',content)
    content = re.sub(r'\d+-\d+-\d+',' ',content)
    content = re.sub('\d+','',content)
    content = content.replace('  ',',').replace(' ','').split(',')
    content = [ x for x in content if x != '']
    content = [ x for x in content if x != 'London']
    content = [ x for x in content if x != 'NFCChampionship']
    content = [ x for x in content if x != 'P']
    content = [ x for x in content if x != 'AFCChampionship']
    content = [ x for x in content if x != 'SuperBowlXLIXGlendale']
    content = [ x for x in content if x != 'Games:']
    content = [ x for x in content if x != 'AZ']
    content = [ x for x in content if x != 'MexicoCity']
    content = sorted(list(set(content)))
    index = dict(zip(content, [ x for x in range(len(content))]))    
    return index

    

def read_games(league):
    """
    type in either 'nfl', 'nba',  or 'mlb' in (leauge)
    creates rankings corresponding to teamm's alphabetical position
    e.g A:0, B:1, ...etc
    Colley Method is unbiased, has no ad hoc adjustments since it only
    looks at wins and loses as well as strength of scheduled oppenents
    
        C-matrix        r vector   b vector  
    | 5  0 -1 -1 -1 |      |r1|     |1/2|                    
    | 0  4 -1  0 -1 |      |r2|     | 1 |     
    |-1 -1  6 -1 -1 |  x   |r3|  =  | 1 |          
    |-1  0 -1  4  0 |      |r4|     | 1 |      
    |-1 -1 -1  0  5 |      |r5|     |3/2|           

    -the diagonal of the matrix is the number of games that team has played+2
    -the other entries signfy how many times row team has played column team
       - 0 means havent played, -2 means played twice
    -the b vector is 1 + (diff in wins and losses)/2 for row team
    see colleyrankings.com for the pdf that fully explains the methodology 
    """
    #generate_index(league)
    
    global ranks,colley,count,sorted_rank_tup, content
    
    if league == 'nfl':
        generate_index(league)
        content = BeautifulSoup(
            urlopen(
        'http://www.masseyratings.com/scores.php?s=262648&sub=262648&all=1&mode=3&sch=on&format=0')).find('pre')
        filename= '{}-{}.txt'.format(date.today().isoformat(),league)
        da = date.today().isoformat()
        file = open(filename,'w')
        file.write(da+"\n\n")
        
    elif league == 'mlb':
        generate_index(league)
        content = BeautifulSoup(
            urlopen(
                'http://www.masseyratings.com/scores.php?s=278762&sub=14342&all=1')).find('pre')
        filename= '{}-{}.txt'.format(date.today().isoformat(),league)
        da = date.today().isoformat()
        file = open(filename,'w')
        file.write(da+"\n\n")
        
    elif league == 'nba':
        generate_index(league)
        content = BeautifulSoup(
            urlopen(
                'http://www.masseyratings.com/scores.php?s=267444&sub=267444&all=1')).find('pre')
        filename= '{}-{}.txt'.format(date.today().isoformat(),league)
        da = date.today().isoformat()
        file = open(filename,'w')
        file.write(da+"\n\n")

    else:
        print('''
    League must be in lowercase, or
    spelling error, or
    that league isn't certified fresh yet.
    ''')
        return
                
    content = content.string.splitlines()
    count = 0
    b = full((len(index),1),0) #creates b vector with entry for each team
    c = full((len(index),len(index)),0) #square matrix depending on size of league
    #Cr=b
    #solving for r
    #for Cii, or C[i][i],= total games played+2
    #b is 1+difference(W-L)/2...actually (w-L)*2
    colley = {}
    excepts = 0
    try:
        for i in range(len(content)): 
            lst = content[i].replace('@',' ')
            lst = re.sub('O\d+',' ',lst)
            lst= lst.replace('  ',',').replace(' ','').replace(',',' ').split() #gets around taking ALL whitespace out
            lst = [ x for x in lst if x != 'London']
            lst = [x for x in lst if x != 'MexicoCity'] #for NBA games
            lst = [x for x in lst if x != ''] #in case of any empty strings
            
            dt, hometeam ,homescore, awayteam, awayscore = lst # date isnt used 
            
            if hometeam not in colley: #create new key if not already set
                colley[hometeam]=[]
                
            if awayteam not in colley: #same thing
                colley[awayteam]=[]
                
            if int( homescore )>int(awayscore): 
                if hometeam and awayteam in index: #stops any errant spelling mistakes
                    c[index[hometeam]][index[awayteam]]-=1
                    c[index[awayteam]][index[hometeam]]-=1 # this gives both teams a connection in the adjacency matrix 
                colley[hometeam]+='W'
                colley[awayteam]+='L'
                
            if int(homescore)<int(awayscore):
                if hometeam and awayteam in index:
                    c[index[hometeam]][index[awayteam]]-=1
                    c[index[awayteam]][index[hometeam]]-=1
                colley[awayteam]+='W'
                colley[hometeam]+='L'
                
            if int( homescore )==int( awayscore ):
                if hometeam and awayteam in index:
                    c[index[hometeam]][index[awayteam]]-=1
                    c[index[awayteam]][index[hometeam]]-=1
                colley[awayteam]+='T' #decided that ties will get no value
                colley[hometeam]+='T' #but do count towards total games played
                
            if len(content[i])!=0:
                count+=1 #a way to check if loop looked at all games
    except ValueError:
        pass #stops the function from working, something is probably wrong
        # so far only occurance is when when 'P' gets concatenated with numbers but has only
        #happened in nfl playoff games which is ok since playoffs determine real ranking
    
    for key in index:
        c[index[key]][index[key]]=len(colley[key])+2 
        b[index[key]]=1+(colley[key].count('W')-colley[key].count('L'))*.5
    ranks=linalg.solve(c,b).tolist() #actual linear alegbra solve, Cr=b
    #looking for r
    rank_tuples = []
    for i in range(len(ranks)):
        rank_tuples.append((ranks[i][0], list(index.keys())[list(index.values()).index(i)]))
    sorted_rank_tup = sorted( rank_tuples, key=lambda rank: rank[0], reverse=True)
    for i in range(len(ranks)):
        str_rank = "{0:.3f}".format(sorted_rank_tup[i][0])
        rankings = "  "+str(i+1) + "  " +str_rank+ "  " + str(sorted_rank_tup[i][1])
        file.write( rankings+"\n")
    file.close()
