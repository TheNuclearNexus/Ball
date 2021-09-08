from typing import List, Tuple
from colorama import Fore
import sys, re

def getGridString(grid: List[List[str]], balls: List[Tuple[int, int]]):
    lines = ""
    for y in range(len(grid)):
        line = ""
        for x in range(len(grid[y])):
            found = False
            for ball in balls:
                if ball[0] == x and ball[1] == y:
                    line += Fore.LIGHTGREEN_EX + '●' + Fore.RESET
                    found = True
                    break
            
            if not found:
                cell = grid[y][x]
                if re.search('[\^vV<>/\\\\]$', cell):
                    line += Fore.LIGHTBLUE_EX + cell + Fore.RESET
                elif re.search('[+\- lL rR]$', cell):
                    line += Fore.MAGENTA + cell + Fore.RESET
                elif re.search('[dD cC pP gG qQ]$', cell):
                    line += Fore.LIGHTYELLOW_EX + cell + Fore.RESET
                elif re.search('[\$]$', cell):
                    line += Fore.LIGHTRED_EX + cell + Fore.RESET
                else:
                    line += Fore.WHITE + cell + Fore.RESET
                
        lines += '\n' + line
    return lines

def getMemoryString(memory: List[int], pointers: List[int]):
    lines = ''
    for i in range(len(memory)):
        prefix = '00' if memory[i] < 10 else '0' if memory[i] < 100 else '' 
        if i not in pointers:
            lines += prefix + str(memory[i]) + ' '
        else:
            lines += f'{Fore.CYAN}{prefix}{memory[i]}{Fore.RESET}' + ' '
        if (i + 1) % 32 == 0:
            lines += '\n'
        elif (i + 1) % 4 == 0:
            lines += '\t'
    return lines

def createGrid(path: str):
    grid = open(path).readlines()

    max = 0
    for l in grid:
        if len(l) > max:
            max = len(l)

    for l in range(len(grid)):
        grid[l] = list((grid[l] + (' ' * (max - len(grid[l])))).replace('\n',''))
    return grid
    