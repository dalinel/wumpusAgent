from ipythonblocks import BlockGrid
from agents import *
from utils import *
from logic import *
from wumpus_kb import *
import numpy as np
from formula import *
import random
from dpll import *
from search import *
import time


#dpll_ask use dpll.py and formula.py from the course. The constructor of formula has been modified in
#order to take as an input the PropKB and its caracteristics instead of an input file
def dpll_ask(kb,alpha):
    kb.tell(Expr("~",alpha))
    [kb_dict,symbols,numb]=kb_to_dictionnary(kb)
    formula=Formula(kb,kb_dict,symbols,numb)
    model=fast_dpll(formula, choose_variable_at_random)
    kb.retract(Expr("~",alpha))

    if(model== []):
        return True
    else:
        return False

#From the aima PropKB map the symbols of the kb (python Expressions) with integers
#The output is a dictionnary where the Expresssions are the keys
def kb_to_dictionnary(kb):
    symbols =[]
    for clause in kb.clauses :
        for symbol in prop_symbols(clause):
            symbols.append(repr(symbol))
    numb = list(range(1,len(symbols)+1))
    kb_dict = dict(zip(symbols, numb))
    return [kb_dict,symbols,numb]


#Returns a List of actions to move through the grid points provided in final_list_of_action
def getActs(final_list_of_action, currentD=0):
    x = 0
    y = 0
    prevx = 0
    prevy = 0
    actions = []

    i = 0
    for token in final_list_of_action:

        if (i % 2 == 0):
            if (i != 0):
                prevx = x
                prevy = y
            x = int(token)

        else:
            y = int(token)


        if ((i - 1) > 1 and (i - 1) % 2 == 0):
            if (x - prevx > 0):
                if (currentD == 0):
                    actions.append('Forward');
                elif (currentD == 1):
                    actions.append('TurnLeft');
                    actions.append('Forward');
                elif (currentD == 2):
                    actions.append('TurnRight');
                    actions.append('TurnRight');
                    actions.append('Forward');
                elif (currentD == 3):
                    actions.append('TurnRight');
                    actions.append('Forward');
                currentD = 0;
            elif (prevx - x > 0):
                if (currentD == 0):
                    actions.append('TurnLeft');
                    actions.append('TurnLeft');
                    actions.append('Forward');
                elif (currentD == 1):
                    actions.append('TurnRight');
                    actions.append('Forward');
                elif (currentD == 2):
                    actions.append('Forward');
                elif (currentD == 3):
                    actions.append('TurnLeft');
                    actions.append('Forward');
                currentD = 2;
            elif (y - prevy > 0):
                if (currentD == 0):
                    actions.append('TurnRight');
                    actions.append('Forward');
                elif (currentD == 1):
                    actions.append('Forward');
                elif (currentD == 2):
                    actions.append('TurnLeft');
                    actions.append('Forward');
                elif (currentD == 3):
                    actions.append('TurnLeft');
                    actions.append('TurnLeft');
                    actions.append('Forward');
                currentD = 1;
            elif (prevy - y > 0):
                if (currentD == 0):
                    actions.append('TurnLeft');
                    actions.append('Forward');
                elif (currentD == 1):
                    actions.append('TurnRight');
                    actions.append('TurnRight');
                    actions.append('Forward');
                elif (currentD == 2):
                    actions.append('TurnRight');
                    actions.append('Forward');
                elif (currentD == 3):
                    actions.append('Forward');
                currentD = 3;
            else:
                print('No Movement %i x %i y %i px %i py %i',i,x,y,prevx,prevy);

        i=i+1
    actions.append(currentD);
    return actions

#Adds the x-y location to the percept
def addLocToPercept(loc, percept):
    ans = []
    txt = ''
    for p in percept:
        if(str(p) == 'None'):
            txt = str(p) + '_' + str(loc[0]) + 'o' + str(loc[1])
        else:
            txt = str(p)[1:-1] + '_' + str(loc[0]) + 'o' + str(loc[1])
        ans.append(txt)
    return ans

# Takes a list and removes all the redundant values
def reduceToUniqueList(numbers):
    result = []
    se = set(tuple(i) for i in numbers)
    for num in se:
        result.append([num[0],num[1]])
    return result

#Returns the X,Y values of the location the move command is trying to move to
def getXYofMove(moves):
    loc = []
    for move in moves:
        cl = repr(move)[10:]

        x,y = cl.split('o')

        y,er = y.split('\'')
        loc.append([x,y])
    return loc

#Returns a random action from the possible actions
def select_random_action(possible_acts, possible_moves_unvisited):
    i = len(possible_acts)
    if (i == 0):
        return []
    elif (i == 1):
        return possible_acts[0]
    else:
        r = random.randint(0,i-1)
        action = possible_acts.pop(r)
        trackXY = getXYofMove(possible_acts)
        possible_moves_unvisited.extend(trackXY)
        return action

#Finds all possible moves on tiles we have already visited
def visitedMoves(kb):

    moves = [];
    loc = [];
    loc2 = [];

    for clause in kb.clauses:
        if repr(clause)[0:2] == 'At':
            len(repr(clause))
            cl = repr(clause)[3:]
            x,y = cl.split('o');
            loc.append(x)
            loc.append(y)
            break


    for clause in kb.clauses:
        if repr(clause)[0:7] == 'Connect':
            cl = repr(clause)[8:]
            term1, term2 = cl.split('_')
            x,y = term1.split('o')
            if loc[0] == x and loc[1] == y:
                x2, y2 = term2.split('o')
                loc2.append(x2)
                loc2.append(y2)


    i = int(len(loc2)/2);
    if (i != 0):
        for m in range (0,i):
            safe = 'Safe_'+loc2[m*2]+'o'+loc2[m*2+1]
            if (dpll_ask(kb,safe)):
                move = 'Move_' + str(loc[0]) + 'o' + str(loc[1]) + '_' + str(loc2[m*2]) + 'o' + str(loc2[m*2+1])
                moves.append(move)


    return moves;


#Finds all possible moves that go onto unexplored squares
def possibleNewMoves(kb):

    moves = [];
    loc = [];
    loc2 = [];
    loc3 = [];
    loc4 = [];

    for clause in kb.clauses:
        if repr(clause)[0:2] == 'At':
            len(repr(clause))
            cl = repr(clause)[3:]
            x,y = cl.split('o');
            loc.append(x)
            loc.append(y)
            break

    for clause in kb.clauses:
        if repr(clause)[0:7] == 'Connect':
            cl = repr(clause)[8:]
            term1, term2 = cl.split('_')
            x,y = term1.split('o')
            if loc[0] == x and loc[1] == y:
                x2, y2 = term2.split('o')
                loc2.append(x2)
                loc2.append(y2)

    i = int(len(loc2)/2);
    if (i != 0):
        for m in range (0,i):
            safe = 'Safe_'+loc2[m*2]+'o'+loc2[m*2+1]
            if (dpll_ask(kb,safe)):
                loc3.append(loc2[m*2])
                loc3.append(loc2[m*2+1])

    for clause in kb.clauses:
        if repr(clause)[0:7] == 'Visited':
            cl = repr(clause)[8:]
            x,y = cl.split('o')
            i = int(len(loc3)/2);

            for m in range (0,i):
                if loc3[m*2] == x and loc3[m*2+1] == y:
                    loc4.append(m*2)
                    loc4.append(m*2+1)
    loc4.sort()
    count = 0
    for i in loc4:
        loc3.pop(i - count)
        count = count + 1

    loc3len = len(loc3)
    if loc3len != 0:
        i = int(len(loc3)/2);
        for m in range(0,i):
            move = 'Move_' + str(loc[0]) + 'o' + str(loc[1]) + '_' + loc3[m*2] + 'o' + str(loc3[m*2+1])
            moves.append(move)



    return moves;

#Checkts to see if it should try to grab the gold
def possibleGrab(kb):
    loc = [];
    for clause in kb.clauses:
        if repr(clause)[0:2] == 'At':
            len(repr(clause))
            cl = repr(clause)[3:]
            x,y = cl.split('o');
            loc.append(x)
            loc.append(y)
            break
    for clause in kb.clauses:
        if repr(clause)[0:7] == 'Glitter':
            cl = repr(clause)[8:]
            x,y = cl.split('o')
            if loc[0] == x and loc[1] == y:
                return ['Grab']
    return []

#Gets rid of extra possible moves that are in the visited space span
def ridOfExtra(kb,possible_moves):
    moves_to_remove = []
    for p_m in possible_moves:
        p_m_str = "Visited_"+p_m[0]+"o"+p_m[1]
        if(dpll_ask(kb,p_m_str)):
            moves_to_remove.append(p_m)
    for m_t_r in moves_to_remove:
        index = possible_moves.index([m_t_r[0],m_t_r[1]])
        possible_moves.pop(index)

    return possible_moves

#Returns the x,y coordinates of the move command in sequence of the location it is
#moving from to the location it is moving to
def getNumOfMove(move):
    m = str(move)[5:]
    term1, term2 = m.split('_')
    x,y = term1.split('o')
    w,z = term2.split('o')
    return [x, y, w, z]

#Updates the knowledge base of the changes for At and Visited tiles
def changeAt(kb,moveNum):
    at_rem = 'At_' + moveNum[0] + 'o' +  moveNum[1]
    at_add = 'At_' + moveNum[2] + 'o' +  moveNum[3]
    visited_add = 'Visited_'  + moveNum[0] + 'o' +  moveNum[1]
    kb.tell(expr(at_add))
    if (dpll_ask(kb,expr(visited_add)) == False):
        kb.tell(expr(visited_add))
    visited_add = 'Visited_'  + moveNum[2] + 'o' +  moveNum[3]
    if (dpll_ask(kb,expr(visited_add)) == False):
        kb.tell(expr(visited_add))
    kb.retract(expr(at_rem))

#Removes Glitter from the knowledge base
def remGlitter(kb,moveNum):
    glitter_rem = 'Glitter_' + str(moveNum[0]) + 'o' +  str(moveNum[1])
    gold_rem = 'Gold_' + str(moveNum[0]) + 'o' +  str(moveNum[1])
    kb.retract(expr(glitter_rem))
    kb.retract(expr(gold_rem))

#Adds percepts to the knowledge base but only if it is not there already
def addPercepts(kb, perceptsList,w):
    AsBreeze = False
    AsStench = False
    for percepts in perceptsList:
        for p in percepts:
            if("Stench" in p):
                AsStench = True
            if("Breeze" in p):
                AsBreeze = True
            if (dpll_ask(kb,expr(p)) == False):
                kb.tell(expr(p))
    if(AsBreeze == False):
        [xo,yo]=w.getlocation()
        strB = "~Breeze_"+str(xo)+"o"+str(yo)
        if (dpll_ask(kb,expr(strB)) == False):
                kb.tell(expr(strB))
    if(AsStench == False):
        [xo,yo]=w.getlocation()
        strB = "~Stench_"+str(xo)+"o"+str(yo)
        if (dpll_ask(kb,expr(strB)) == False):
                kb.tell(expr(strB))

#Returns a random move from the possible moves in the list m
def getRandMove(m):
    i = len(m)

    if (i == 1):
        return m[0]
    if (i == 0):
        return None

    r = random.randint(0,i-1)
    m = m[r]
    return m

#Returns all tiles that have been visited
def getAllVisited(kb):
    loc = []
    for clause in kb.clauses:
        if repr(clause)[0:7] == 'Visited':
            cl = repr(clause)[8:]
            x,y = cl.split('o');
            loc.append([int(x),int(y)])
    return loc

#Returns all tiles with Stench
def findStenchLocations(kb):
    loc = []
    for clause in kb.clauses:
        if repr(clause)[0:6] == 'Stench':
            cl = repr(clause)[7:]
            x,y = cl.split('o');
            loc.append([x,y])
    return loc

#Provides a random stench tile from the possible ones
def getRandomStench(stenchLocations):
    i = len(stenchLocations)

    if (i == 1):
        return stenchLocations[0]
    if (i == 0):
        return None

    r = random.randint(0,i-1)
    stench = stenchLocations[r]
    return stench

#Provides a random direction from the directions provided
def getRandD(D):
    i = len(D)

    if (i == 1):
        return D[0]
    if (i == 0):
        return None

    r = random.randint(0,i-1)
    de = D[r]
    return de

#Based on the stench tiles, it attempts to figure out
# a direction to attempt to shoot the wumpus
# when in a stench tile
def stenchDirection(kb, sten, stenchLocations):
    D = [ 0, 1, 2 ,3 ]

    sx = int(sten[0])
    sy = int(sten[1])
    index = 0
    visit = 'Visited_'+str(sx+1)+'o'+str(sy)
    if(dpll_ask(kb, expr(visit))):
        D.pop(index)
    visit = 'Visited_'+str(sx-1)+'o'+str(sy)
    if(dpll_ask(kb, expr(visit))):
        index = D.index(2)
        D.pop(index)

    visit = 'Visited_'+str(sx)+'o'+str(sy+1)
    if(dpll_ask(kb, expr(visit))):
        index = D.index(1)
        D.pop(index)
    visit = 'Visited_'+str(sx)+'o'+str(sy-1)
    if(dpll_ask(kb, expr(visit))):
        index = D.index(3)
        D.pop(index)
    if len(D) == 1:
        return D

    for loc in stenchLocations:
        x,y = loc
        x = int(x)
        y = int(y)
        if (x == sx) and (y == sy):
            continue
        else:

            if (x < sx):
                if 0 in D:
                    index = D.index(0)
                    D.pop(index)
                    if (y == sy):
                        D = [2]
            if (x > sx):
                if 2 in D:
                    index = D.index(2)
                    D.pop(index)
                    if (y == sy):
                        D = [0]
            if (y < sy):
                if 1 in D:
                    index = D.index(1)
                    D.pop(index)
                    if (x == sx):
                        D = [3]
            if (y > sy):
                if 3 in D:
                    index = D.index(3)
                    D.pop(index)
                    if (x == sx):
                        D = [1]
    votes = [0, 0, 0, 0];
    Dvotes = []
    if len(D) > 1:

        for loc in stenchLocations:
            x,y = loc
            x = int(x)
            y = int(y)
            wumpus = 'Wumpus_'+str(x+1)+'o'+str(y)

            if(dpll_ask(kb, expr(wumpus))):
                votes[0] = votes[0] + 1
            wumpus = 'Wumpus_'+str(x-1)+'o'+str(y)
            if(dpll_ask(kb, expr(wumpus))):
                votes[2] = votes[2] + 1

            wumpus = 'Wumpus_'+str(x)+'o'+str(y+1)
            if(dpll_ask(kb, expr(wumpus))):
                votes[1] = votes[1] + 1
            wumpus = 'Wumpus_'+str(x)+'o'+str(y-1)
            if(dpll_ask(kb, expr(wumpus))):
                votes[3] = votes[3] + 1
        for direction in D:
            Dvotes.append(votes[direction])

        mx = max(Dvotes)
        index = Dvotes.index(mx)
        D = [Dvotes[index]]


    return D

#Figures out how many turns you have to do to
#turn to your desired direction
def getTurnActs(currentD=0, desiredD=0):
    actions = []
    count = desiredD - currentD
    if count > 0:
        for i in range(0,count):
            actions.append('TurnRight')
    if count < 0:
        for i in range(0,abs(count)):
            actions.append('TurnLeft')


    actions.append(currentD);
    return actions

#Find the wumpus from the world data to be able to delete
# the wumpus in the world data
def find_the_wumpus(world):
    loc =[]
    for x in range(0, len(world)):
        for y in range(0, len(world[x])):
            if len(world[x][y]):
                g = -1
                for i in world[x][y]:
                    h = world[x][y].index(i)
                    if(isinstance(i, Wumpus)):
                        g = h
                        loc = [x,y]
                        return [loc,i]
    return loc
    
#Get Rid of _ when the map is bigger   
def purgeExtraChar(li):
    newli = []
    for loc in li:
        x,y = loc
        if '_' in x:
            x = x.replace('_','')
        if '_' in y:
            y = y.replace('_','')
        newli.append([x,y])
    return newli
