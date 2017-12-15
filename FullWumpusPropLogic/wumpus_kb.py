from agents import *
from utils import *
from logic import *


def wumpus_prop_knowledge_base(xmax,ymax):
    kb = PropKB();

    for i in range(2,xmax-2):
            for j in range(2,ymax-2):
                    kb.tell(expr("Connect_%do%d_%do%d"%(i,j,i+1,j)));
                    kb.tell(expr("Connect_%do%d_%do%d"%(i,j,i-1,j)));
                    kb.tell(expr("Connect_%do%d_%do%d"%(i,j,i,j+1)));
                    kb.tell(expr("Connect_%do%d_%do%d"%(i,j,i,j-1)));
                    kb.tell(expr("Connect_%do%d_%do%d"%(i+1,j,i,j)));
                    kb.tell(expr("Connect_%do%d_%do%d"%(i-1,j,i,j)));
                    kb.tell(expr("Connect_%do%d_%do%d"%(i,j+1,i,j)));
                    kb.tell(expr("Connect_%do%d_%do%d"%(i,j-1,i,j)));
                    kb.tell(expr("Breeze_%do%d"%(i,j)) |'==>' |
                            (expr("Pit_%do%d"%(i+1,j)) |
                             expr("Pit_%do%d"%(i-1,j)) |
                             expr("Pit_%do%d"%(i,j+1)) |
                             expr("Pit_%do%d"%(i,j-1))))
                    kb.tell((expr("Stench_%do%d"%(i,j)) & expr('WumpusIsAlive')) | '==>' |
                            (expr("Wumpus_%do%d"%(i+1,j)) |
                             expr("Wumpus_%do%d"%(i-1,j)) |
                             expr("Wumpus_%do%d"%(i,j+1)) |
                             expr("Wumpus_%do%d"%(i,j-1))))
                    kb.tell(expr("None_%do%d"%(i,j)) | '==>' |
                            (expr("Safe_%do%d"%(i+1,j)) &
                             expr("Safe_%do%d"%(i-1,j)) &
                             expr("Safe_%do%d"%(i,j+1)) &
                             expr("Safe_%do%d"%(i,j-1))))


    for i in range(1,xmax):
            for j in range(1,ymax):
                    kb.tell(expr("Safe_%do%d"%(i,j))  | '==>' |
                           (expr("~Wumpus_%do%d"%(i,j)) &
                            expr("~Pit_%do%d"%(i,j))));
                    kb.tell(expr("None_%do%d"%(i,j)) | '==>' | expr("Safe_%do%d"%(i,j)));
                    kb.tell((expr("Stench_%do%d"%(i,j)) & expr("~WumpusIsAlive") & expr("~Breeze_%do%d"%(i,j))) | '==>' | expr("None_%do%d"%(i,j)));
                    #for k in range(1,xmax):
                    #    for l in range(1,ymax)
                    #        kb.tell(expr("Connect_%do%d_%do%d"%(i,j,j,k)) | '<=>' | expr("Connect_%do%d_%do%d"%(j,k,i,j)));
                    kb.tell(expr("Scream") | '==>' | (expr('~WumpusIsAlive') & expr('~HaveArrow')));
                    #kb.tell((expr("Wumpus_%do%d"%(i,j)) & expr("At_%do%d"%(i,j))) | '==>' | (expr('~AgentIsAlive')));
                    #kb.tell((expr("Pit_%do%d"%(i,j)) & expr("At_%do%d"%(i,j))) | '==>' | (expr('~AgentIsAlive')));

    # Connect the tiles of the world which are near the walls (we don't connect the walls)
    if((xmax>3) & (ymax>3)):
        for j in range(2,ymax-2):
            kb.tell(expr("Connect_%do%d_%do%d"%(1,j,1,j+1)))
            kb.tell(expr("Connect_%do%d_%do%d"%(1,j,1,j-1)))
            kb.tell(expr("Connect_%do%d_%do%d"%(1,j,2,j)))
            kb.tell(expr("Connect_%do%d_%do%d"%(xmax-2,j,xmax-2,j+1)))
            kb.tell(expr("Connect_%do%d_%do%d"%(xmax-2,j,xmax-2,j-1)))
            kb.tell(expr("Connect_%do%d_%do%d"%(xmax-2,j,xmax-3,j)))

            kb.tell(expr("Connect_%do%d_%do%d"%(1,j+1,1,j)))
            kb.tell(expr("Connect_%do%d_%do%d"%(1,j-1,1,j)))
            kb.tell(expr("Connect_%do%d_%do%d"%(2,j,1,j)))
            kb.tell(expr("Connect_%do%d_%do%d"%(xmax-2,j+1,xmax-2,j)))
            kb.tell(expr("Connect_%do%d_%do%d"%(xmax-2,j-1,xmax-2,j)))
            kb.tell(expr("Connect_%do%d_%do%d"%(xmax-3,j,xmax-2,j)))
            kb.tell(expr("Breeze_%do%d"%(1,j)) |'==>' |
                                (expr("Pit_%do%d"%(1,j+1)) |
                                 expr("Pit_%do%d"%(1,j-1)) |
                                 expr("Pit_%do%d"%(2,j))))
            kb.tell((expr("Stench_%do%d"%(1,j)) & expr('WumpusIsAlive')) | '==>' |
                                (expr("Wumpus_%do%d"%(1,j+1)) |
                                 expr("Wumpus_%do%d"%(1,j-1)) |
                                 expr("Wumpus_%do%d"%(2,j))))
            kb.tell(expr("Breeze_%do%d"%(xmax-2,j)) |'==>' |
                                (expr("Pit_%do%d"%(1,j+1)) |
                                 expr("Pit_%do%d"%(1,j-1)) |
                                 expr("Pit_%do%d"%(2,j))))
            kb.tell((expr("Stench_%do%d"%(xmax-2,j)) & expr('WumpusIsAlive')) | '==>' |
                                (expr("Wumpus_%do%d"%(xmax-2,j+1)) |
                                 expr("Wumpus_%do%d"%(xmax-2,j-1)) |
                                 expr("Wumpus_%do%d"%(xmax-3,j))))
            kb.tell(expr("None_%do%d"%(1,j)) |'==>' |
                                (expr("Safe_%do%d"%(1,j+1)) &
                                 expr("Safe_%do%d"%(1,j-1)) &
                                 expr("Safe_%do%d"%(2,j))))
            kb.tell(expr("None_%do%d"%(xmax-2,j)) | '==>' |
                                (expr("Safe_%do%d"%(xmax-2,j+1)) &
                                 expr("Safe_%do%d"%(xmax-2,j-1)) &
                                 expr("Safe_%do%d"%(xmax-3,j))))

        for i in range(2,xmax-2):
            kb.tell(expr("Connect_%do%d_%do%d"%(i,1,i+1,1)))
            kb.tell(expr("Connect_%do%d_%do%d"%(i,1,i-1,1)))
            kb.tell(expr("Connect_%do%d_%do%d"%(i,1,i,2)))
            kb.tell(expr("Connect_%do%d_%do%d"%(i,ymax-2,i+1,ymax-2)))
            kb.tell(expr("Connect_%do%d_%do%d"%(i,ymax-2,i-1,ymax-2)))
            kb.tell(expr("Connect_%do%d_%do%d"%(i,ymax-2,i,ymax-3)))

            kb.tell(expr("Connect_%do%d_%do%d"%(i+1,1,i,1)))
            kb.tell(expr("Connect_%do%d_%do%d"%(i-1,1,i,1)))
            kb.tell(expr("Connect_%do%d_%do%d"%(i,2,i,1)))
            kb.tell(expr("Connect_%do%d_%do%d"%(i+1,ymax-2,i,ymax-2)))
            kb.tell(expr("Connect_%do%d_%do%d"%(i-1,ymax-2,i,ymax-2)))
            kb.tell(expr("Connect_%do%d_%do%d"%(i,ymax-3,i,ymax-2)))
            kb.tell(expr("Breeze_%do%d"%(i,1)) |'==>' |
                                (expr("Pit_%do%d"%(i+1,1)) |
                                 expr("Pit_%do%d"%(i-1,1)) |
                                 expr("Pit_%do%d"%(i,2))))
            kb.tell(( expr("Stench_%do%d"%(i,1)) & expr('WumpusIsAlive')) | '==>' |
                                (expr("Wumpus_%do%d"%(i+1,1)) |
                                 expr("Wumpus_%do%d"%(i-1,1)) |
                                 expr("Wumpus_%do%d"%(i+1,2))))
            kb.tell(expr("Breeze_%do%d"%(i,ymax-2)) |'==>' |
                                (expr("Pit_%do%d"%(i+1,ymax-2)) |
                                 expr("Pit_%do%d"%(i-1,ymax-2)) |
                                 expr("Pit_%do%d"%(i,ymax-3))))
            kb.tell((expr("Stench_%do%d"%(i,ymax-2)) & expr('WumpusIsAlive')) | '==>' |
                                (expr("Wumpus_%do%d"%(i+1,ymax-2)) |
                                 expr("Wumpus_%do%d"%(i-1,ymax-2)) |
                                 expr("Wumpus_%do%d"%(i,ymax-3))))
            kb.tell(expr("None_%do%d"%(i,1)) |'==>' |
                                (expr("Safe_%do%d"%(i+1,1)) &
                                 expr("Safe_%do%d"%(i-1,1)) &
                                 expr("Safe_%do%d"%(i,2))))
            kb.tell(expr("None_%do%d"%(i,ymax-2)) | '==>' |
                                (expr("Safe_%do%d"%(i+1,ymax-2)) &
                                 expr("Safe_%do%d"%(i-1,ymax-2)) &
                                 expr("Safe_%do%d"%(i,ymax-3))))
    if((xmax>4) & (ymax>4)):
        kb.tell(expr("Connect_%do%d_%do%d"%(1,1,1,2)))
        kb.tell(expr("Connect_%do%d_%do%d"%(1,1,2,1)))
        kb.tell(expr("Connect_%do%d_%do%d"%(xmax-2,ymax-2,xmax-2,ymax-3)))
        kb.tell(expr("Connect_%do%d_%do%d"%(xmax-2,ymax-2,xmax-3,ymax-2)))
        kb.tell(expr("Connect_%do%d_%do%d"%(1,ymax-2,1,ymax-3)))
        kb.tell(expr("Connect_%do%d_%do%d"%(1,ymax-2,2,ymax-2)))
        kb.tell(expr("Connect_%do%d_%do%d"%(xmax-2,1,xmax-2,2)))
        kb.tell(expr("Connect_%do%d_%do%d"%(xmax-2,1,xmax-3,1)))

        kb.tell(expr("Connect_%do%d_%do%d"%(1,2,1,1)))
        kb.tell(expr("Connect_%do%d_%do%d"%(2,1,1,1)))
        kb.tell(expr("Connect_%do%d_%do%d"%(xmax-2,ymax-3,xmax-2,ymax-2)))
        kb.tell(expr("Connect_%do%d_%do%d"%(xmax-3,ymax-2,xmax-2,ymax-2)))
        kb.tell(expr("Connect_%do%d_%do%d"%(1,ymax-3,1,ymax-2)))
        kb.tell(expr("Connect_%do%d_%do%d"%(2,ymax-2,1,ymax-2)))
        kb.tell(expr("Connect_%do%d_%do%d"%(xmax-2,2,xmax-2,1)))
        kb.tell(expr("Connect_%do%d_%do%d"%(xmax-3,1,xmax-2,1)))
        kb.tell(expr("Breeze_%do%d"%(1,1)) |'==>' |
                                (expr("Pit_%do%d"%(1,2)) |
                                 expr("Pit_%do%d"%(2,1))))
        kb.tell((expr("Stench_%do%d"%(1,1)) & expr('WumpusIsAlive')) | '==>' |
                                (expr("Wumpus_%do%d"%(1,2)) |
                                 expr("Wumpus_%do%d"%(2,1))))
        kb.tell(expr("None_%do%d"%(1,1)) | '==>' |
                                (expr("Safe_%do%d"%(1,2)) &
                                 expr("Safe_%do%d"%(2,1))))
        kb.tell(expr("Breeze_%do%d"%(xmax-2,ymax-2)) |'==>' |
                                (expr("Pit_%do%d"%(xmax-2,ymax-3)) |
                                 expr("Pit_%do%d"%(xmax-3,ymax-2))))
        kb.tell((expr("Stench_%do%d"%(xmax-2,ymax-2)) & expr('WumpusIsAlive')) | '==>' |
                                (expr("Wumpus_%do%d"%(xmax-2,ymax-3)) |
                                 expr("Wumpus_%do%d"%(xmax-3,ymax-2))))
        kb.tell(expr("None_%do%d"%(xmax-2,ymax-2)) | '==>' |
                                (expr("Safe_%do%d"%(xmax-2,ymax-3)) &
                                 expr("Safe_%do%d"%(xmax-3,ymax-2))))
        kb.tell(expr("Breeze_%do%d"%(1,ymax-2)) |'==>' |
                                (expr("Pit_%do%d"%(1,ymax-3)) |
                                 expr("Pit_%do%d"%(2,ymax-2))))
        kb.tell((expr("Stench_%do%d"%(1,ymax-2)) & expr('WumpusIsAlive')) | '==>' |
                                (expr("Wumpus_%do%d"%(1,ymax-3)) |
                                 expr("Wumpus_%do%d"%(2,ymax-2))))
        kb.tell(expr("None_%do%d"%(1,ymax-2)) | '==>' |
                                (expr("Safe_%do%d"%(1,ymax-3)) &
                                 expr("Safe_%do%d"%(2,ymax-2))))
        kb.tell(expr("Breeze_%do%d"%(xmax-2,1)) |'==>' |
                                (expr("Pit_%do%d"%(xmax-2,2)) |
                                 expr("Pit_%do%d"%(xmax-3,1))))
        kb.tell((expr("Stench_%do%d"%(xmax-2,1)) & expr('WumpusIsAlive')) | '==>' |
                                (expr("Wumpus_%do%d"%(xmax-2,2)) |
                                 expr("Wumpus_%do%d"%(xmax-3,1))))
        kb.tell(expr("None_%do%d"%(xmax-2,1)) | '==>' |
                                (expr("Safe_%do%d"%(xmax-2,2)) &
                                 expr("Safe_%do%d"%(xmax-3,1))))


    kb.tell(expr('At_1o1'))
    kb.tell(expr('Visited_1o1'))
    kb.tell(expr('WumpusIsAlive'))
    kb.tell(expr('AgentIsAlive'))
    kb.tell(expr('HaveArrow'))

    return kb
