import copy
import evaluation

## adapter : call move functions
def moveleft(state):
    return state

def moveright(state):
    return state

def moveup(state):
    return state

def movedown(state):
    return state

def genNodeChildren(instate):
    ## create childrens for 1 node
    node_directionLayer = genDirectionLayer(instate)
    node_children = []

    for direction in node_directionLayer:
        node_children += genAllChild(direction)

    ## return complete tree for 1 node
    return node_children

def genDirectionLayer(instate):
    stack = []
    layer = instate[0].index(0)

    for func in funcs:
        newstate = copy.deepcopy(instate)
        newstate[0][layer] = func[1]
        newstate[1] = func[0](newstate[1])
        stack.append(newstate)

    ## return 4 possible states
    return stack

def genChild2(inboard,i,j):
    newboard2 = copy.deepcopy(inboard)
    newboard2[i][j] = 2
    return newboard2

def genChild4(inboard,i,j):
    newboard4 = copy.deepcopy(inboard)
    newboard4[i][j] = 4
    return newboard4

def genAllChild(direction):
    inboard = direction[1]
    ## gen children for each direction
    stack = []
    for i in range(len(inboard)):
        for j in range(len(inboard[i])):
            if(inboard[i][j] == 0):
                stack.append([direction[0], genChild2(inboard,i,j), direction[2]*0.9])
                stack.append([direction[0], genChild4(inboard,i,j), direction[2]*0.1])

    ## return all possible fill
    return stack

def debugStack(stack):
    count = 0
    for item in stack:
        print("member "+str(count))
        print(item)
        print()
        count+=1

def createState(inBoard):
    state = [ [0, 0, 0], inBoard , 1 ]
    return state

def linearPlay(possibilityTree):
    bestLeaf = ['','',0]
    ## parallel do this method better
    for leaf in possibilityTree:
        leafcopy = copy.deepcopy(leaf)
        leafcopy[2] = evaluation.slopedBoard(leaf[1])*leaf[2]
        if(leafcopy[2] > bestLeaf[2]):
            bestLeaf = leafcopy
    return bestLeaf

def genNodeController(board, funcArray):
    state1 = createState(board)
    layer1 = genNodeChildren(state1)
    layer2 = []
    for leaf in layer1:
        layer2 += genNodeChildren(leaf)
    layer3 = []
    for leaf in layer2:
        layer3 += genNodeChildren(leaf)
    return layer3

if (__name__ == '__main__'):
    request = [[2,4,4,2], [2,2,4,2], [0,0,0,0], [0,0,0,0]]
    funcs = [[moveleft,'l'], [moveright,'r'], [moveup,'u'], [movedown,'d']]

    state1 = createState(request)
    layer1 = genNodeChildren(state1)
    print(len(layer1))

    layer2 = []
    for leaf in layer1:
        layer2 += genNodeChildren(leaf)
    print(len(layer2))

    layer3 = []
    for leaf in layer2:
        layer3 += genNodeChildren(leaf)
    print(len(layer3))

    ## scatter layer3 nodes to slaves
    ### slaves do calculate score for each node then gather back here
    ###     data structure [ ['move1', 'move2', 'move3'], [board], probabilty ]
    ###     select highest score by probability*hueristic score

    print(layer3[0:3])

    bestLeaf = linearPlay(layer3)
    print(bestLeaf)


