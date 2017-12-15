def getActs(final_list_of_action):

    x = 0
    y = 0
    prevx = 0
    prevy = 0
    actions = []
    currentD = 0
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
    return actions

