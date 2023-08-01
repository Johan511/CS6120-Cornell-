import json
import sys
from collections import deque


TERMINATORS = ["jmp"]

class Block:
    def __init__(self, blockName=""):
        self.blockName = blockName
        self.instructions = []
        self.trueJmp = None
        self.falseJmp = None
        self.parents = set()

    def append(self, instruction):
        self.instructions.append(instruction)

    def setBlockName(self, blockName):
        if(self.blockName != ""):
            raise Exception(f"block name is already set to ${self.blockName}")
        self.blockName = blockName

    def __str__(self):
        print(f"Block Name : {self.blockName}")
        print(self.parents)
        return ""

    

def mycfg():    
    irJson = json.load(sys.stdin)
    blocks = []
    block = Block("main")
    for func in irJson['functions']:
        for instr in func['instrs']:
            if instr.get('label') != None:
                blocks.append(block)
                block = Block(instr['label'])
            else:            
                block.append(instr)

                if instr['op'] in TERMINATORS:
                    blocks.append(block)
                    block = Block()
        blocks.append(block)

    blockMap = {}

    for block in blocks:
        if(block.blockName != ""):
            blockMap[block.blockName] = block

    blockMap['main'].parents.add(None)

    for i, block in enumerate(blocks):
        lastInstr = block.instructions[-1]
        if(lastInstr['op'] == 'jmp'):
            block.trueJmp = blockMap[lastInstr['labels'][0]]
            block.falseJmp = blockMap[lastInstr['labels'][0]]
            blockMap[lastInstr['labels'][0]].parents.add(block)
        elif i != len(blocks)-1:
            block.trueJmp = blocks[i+1]
            block.falseJmp = blocks[i+1]
            blocks[i+1].parents.add(block)

    inDegreeMap = {}
    queue = deque()


    for block in blocks:
        inDegreeMap[block] = len(block.parents)
        if(inDegreeMap[block] == 0):
            queue.appendleft(block)


    while(len(queue) != 0):
        front = queue.popleft()
        trueJmp = front.trueJmp
        falseJmp = front.falseJmp 
        trueJmp.parents.remove(front)
        if(len(trueJmp.parents) == 0):
            queue.appendleft(trueJmp)
        
        if(trueJmp != falseJmp):
            falseJmp.parents.remove(front)
            if(len(falseJmp.parents) == 0):
                queue.appendleft(falseJmp)
        
        blocks.remove(front)


    for block in blocks:
        print(block)
    









if (__name__ == '__main__'):
    mycfg()