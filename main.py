from helper import getMemoryString
import io, os, time, sys, colorama, re
from colorama import Fore
from typing import List, Tuple
from debug import setSyncData, startServer

grid: List[str] = []
def createGrid(path: str):
    global grid
    grid = open("test.ball").readlines()

    max = 0
    for l in grid:
        if len(l) > max:
            max = len(l)

    for l in range(len(grid)):
        grid[l] = list((grid[l] + (' ' * (max - len(grid[l])))).replace('\n',''))

    # print(f'Ball: {ball.x}, {ball.y}')

    # print(str(' ' * ((pointer * 3) + 1)) + 'v')
    # print(memory)

pointer = 0
memoryLength = 256
memory: List[int] = [0 for i in range(memoryLength)]

class Ball:
    x: int = 0
    y: int = 0
    pointer: int = 0
    direction: int = 0

    def __init__(self, x: int, y: int, pointer: int = 0):
        self.x = x
        self.y = y
        self.pointer = pointer

    def throwError(self, message: str):
        print(Fore.RED + f'ERROR: {message} @ ({self.x}, {self.y})' + Fore.RESET)
        
    def reflectRight(self):
        if self.direction == 1:
            self.direction = 2
            return
        elif self.direction == 2:
            self.direction = 1
            return
        elif self.direction == 0:
            self.direction = 3
            return
        elif self.direction == 3:
            self.direction = 0
            return

    def reflectLeft(self):
        if self.direction == 3:
            self.direction = 2
        elif self.direction == 2:
            self.direction = 3
        elif self.direction == 0:
            self.direction = 1
        elif self.direction == 1:
            self.direction = 0

    def dumbMemory(self):
        print()
        print(getMemoryString(memory, [self.pointer]))
        input('Paused...')

    def destroy(self):
        balls.remove(self)

    def parseCell(self):
        try:
            cell = grid[self.y][self.x].lower()
        except:
            self.throwError(f'Out of bounds! {self.x}, {self.y}')
            self.destroy()
            return
    

        if cell == ' ':
            pass
        elif cell == '^':
            self.direction = 0
        elif cell == '>':
            self.direction = 1
        elif cell == 'v':
            self.direction = 2
        elif cell == '<':
            self.direction = 3
        elif cell == '+':
            memory[self.pointer] = memory[self.pointer] + 1 if memory[self.pointer] < 255 else 0
        elif cell == '-':
            memory[self.pointer] = memory[self.pointer] - 1 if memory[self.pointer] > 0 else 255
        elif cell == 'l':
            if(self.pointer > 0):
                self.pointer -= 1
            else:
                self.throwError(f'Memory out of bounds! {self.pointer - 1}')
                self.destroy()
        elif cell == 'r':
            if(self.pointer < memoryLength - 1):
                self.pointer += 1
            else:
                self.throwError(f'Memory out of bounds! {self.pointer + 1}')
                self.destroy()
        elif cell == '$':
            balls.remove(self)
        elif cell == '/':
            if memory[self.pointer] == 0:
                self.reflectLeft()
        elif cell == '\\':
            if memory[self.pointer] == 0:
                self.reflectRight()
        elif cell == 'p':
            sys.stdout.write(str(memory[self.pointer]))
            sys.stdout.flush()
        elif cell == 'c':
            sys.stdout.write(chr(memory[self.pointer]))
            sys.stdout.flush()
        elif cell == 'g':
            inp = input('\nInput Character: ')
            memory[self.pointer] = ord(inp[0]) if len(inp) > 0 else 0
        elif cell == 'd':
            if not debug:
                self.dumbMemory()
        elif cell == 'q':
            balls.append(Ball(self.x, self.y+1, self.pointer))

    def update(self):
        self.parseCell()

        if self.direction == 0:
            self.y -= 1
        elif self.direction == 1:
            self.x += 1
        elif self.direction == 2:
            self.y += 1
        elif self.direction == 3:
            self.x -= 1

running: bool = True
balls: List[Ball] = []

def getCoords() -> List[Tuple[int, int]]:
    list = []
    for b in balls:
        list.append((b.x, b.y))
    return list

def getPointers() -> List[int]:
    list = []
    for b in balls:
        list.append(b.pointer)
    return list

def loop(debug: bool = False, speed: float = 0):
    balls.append(Ball(0, 0))

    while len(balls) != 0:
        for ball in balls:
            ball.update()
        # if clear:
        #     os.system("cls")
        # printGrid(balls)
        setSyncData({
            'grid': grid,
            'balls': getCoords(),
            'memory': memory,
            'pointers': getPointers()
        })
        time.sleep(speed)
    print(Fore.GREEN + 'Exited Successfully!')
debug = False
def main():
    global debug
    file = ''
    speed = 0
    for i in range(len(sys.argv)):
        if sys.argv[i] == '-d' or sys.argv == '--debug':
            debug = True
        elif sys.argv[i] == '-i' or sys.argv == '--input':
            i += 1
            file = sys.argv[i]
        elif sys.argv[i] == '-s' or sys.argv == '--speed':
            i += 1
            speed = float(sys.argv[i])
            
    if debug:
        speed = 1/30
        startServer()
    
    createGrid(file)
    loop(debug, speed)

if __name__ == '__main__':
    main()


