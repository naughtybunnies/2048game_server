class node:
    myVal = ''
    nextNode = ''

    def __init__(self, val):
        self.myVal = val
        self.nextNode = ''

    def setNextNode(self, nextNode):
        self.nextNode = nextNode

    def getNextNode(self):
        return self.nextNode

    def getNodeVal(self):
        return self.myVal

    def __repr__(self):
        return self.myVal

class queue:
    firstnode = ''
    inListSize = 0

    def __init__(self, inList):
        self.firstnode = node('HEAD')
        self.firstnode.setNextNode('')
        for member in inList:
            if(member != 0):
                self.addNode(member)
        self.inListSize = len(inList)

    def addNode(self, val):
        lastnode = self.firstnode
        newnode = node(val)
        while(lastnode.getNextNode() != ''):
            lastnode = lastnode.getNextNode()
        lastnode.setNextNode(newnode)

    def printQueue(self):
        thisnode = self.firstnode.getNextNode()
        while(1):
            print(thisnode.getNodeVal(), end=" ")
            thisnode = thisnode.getNextNode()
            if(thisnode == ''):
                break
        print("")

    def compress(self):
        thisnode = self.firstnode.getNextNode()
        outlist = []
        while(1):
            if(thisnode == ''):
                break

            if(thisnode.getNextNode() == ''):
                outlist.append(thisnode.getNodeVal())
                break

            if((thisnode.getNodeVal() == thisnode.getNextNode().getNodeVal()) and (thisnode.getNodeVal() != 0)):
                outlist.append(thisnode.getNodeVal()*2)
                thisnode = thisnode.getNextNode().getNextNode()
            elif(thisnode.getNodeVal() == 0):
                thisnode = thisnode.getNextNode()
            else:
                outlist.append(thisnode.getNodeVal())
                thisnode = thisnode.getNextNode()
        outlist = outlist + [0 for i in range(self.inListSize - len(outlist))]
        return outlist

