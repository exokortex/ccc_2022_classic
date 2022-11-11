from pathlib import Path
#import numpy as np
#import itertools
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import sys

PACMAN = '.'
GHOST = 'G'

if True:
    def print(*args, **aargs):
        pass

def parse_filed(lines):
    f = []
    for line in lines:
        f.append([x for x in line.strip()])
    return f

def str_to_vec(move):
    match move:
        case 'U': return (-1, 0)
        case 'D': return ( 1, 0)
        case 'L': return ( 0,-1)
        case 'R': return ( 0, 1)
        case _: raise Exception('no') 
        
def vec_to_str(v):
    match v:
        case (-1, 0): return 'U' 
        case ( 1, 0): return 'D' 
        case ( 0,-1): return 'L' 
        case ( 0, 1): return 'R' 
        case _: raise Exception('no') 
    
        
def path_to_moves(path):
    dirs = []
    for i in range(len(path)-1):
        p1 = path[i]
        p2 = path[i+1]
        dirs.append(vec_to_str((p2[0]-p1[0],p2[1]-p1[1])))
    return dirs


def print_field(field, agents):
    for r, row in enumerate(field):
        for c, pixel in enumerate(row):
            for agent in agents:
                if agent.pos == (r,c):
                    print(agent.type, end='')
                else:
                    print(pixel, end='')
        print()
        
def str_to_pos(s):
    return tuple(int(x)-1 for x in s.split(' '))

class Agent:
    initial_pos = (0, 0)
    pos = (0, 0)
    moves = ""
    moves_left = []
    moves_hist = []
    
    def __init__(self, type, pos, moves):
        self.type = type
        self.initial_pos = pos
        self.pos = pos
        self.moves = moves
        self.moves_left = [x for x in moves]
        
    def make_move(self, grid, field):
        # find target
        if len(self.moves_left) == 0:
            found = False
            for r, row in enumerate(field):
                for c, pixel in enumerate(row):
                    if pixel == 'C':
                        coin_pos = (r, c)
                        found = True
                        break
                if found: break
            if not found:   
                if self.pos != self.initial_pos:
                    coin_pos = self.initial_pos
                else:
                    return None
            #coin_pos = (2, 1) # TODO
            #if self.pos == (2, 1):
            #    coin_pos = (1, 2) # TODO
            # cal route
            print('xxx', self.pos)
            start = grid.node(self.pos[1], self.pos[0])
            end = grid.node(coin_pos[1], coin_pos[0])
            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
            path, runs = finder.find_path(start, end, grid)
            grid.cleanup()
            print('path', path)
            path = [(b,a) for (a,b) in path]
            print('path', path)
            new_moves = path_to_moves(path)
            print('new_moves', new_moves)
            self.moves_left += new_moves
        # move to target
        move = self.moves_left.pop(0)
        mvect = str_to_vec(move)
        new_pos = (mvect[0] + self.pos[0], mvect[1] + self.pos[1])
        self.moves_hist.append(move)
        return new_pos
    
        if len(self.moves_left) == 0:
            return None
        move = self.moves_left.pop(0)
        mvect = str_to_vec(move)
        new_pos = (mvect[0] + self.pos[0], mvect[1] + self.pos[1])
        return new_pos
    
    def __str__(self):
        return f'{self.type} {self.pos} {self.moves_left}'
        
    
def parse_agent(type, lines, n):
    start = str_to_pos(lines[n])
    moves = lines[n+2]
    agent = Agent(type, start, moves)
    return agent, n+3

def valid_pos(H, W, pos):
    return (0 <= pos[0] < H) and (0 <= pos[1] < W)

def is_wall(field, pos):
    return field[pos[0]][pos[1]] == 'W'

def game_loop(field, pacman, ghosts):
    
    matrix = [[0 if (x == 'W' or x == 'G') else 1 for x in row] for row in field]
    for x in matrix:
        print(x)
    grid = Grid(matrix=matrix)
    
    
    agents = [pacman] + ghosts
    print(field)
    for agent in agents:
        print(agent)

    collected = 0
    survived = True
    i = 0
    moves = []
    while True:
        print('====================== round', i)
        print_field(field, agents)
        for agent in agents:
            agent_str = str(agent)
            new_pos = agent.make_move(grid, field)
            print(agent_str, '->', new_pos)
            if new_pos == None:
                return ''.join(pacman.moves_hist)
            agent.pos = new_pos
        # pacman ghost check
        for ghost in ghosts:
            if ghost.pos == pacman.pos:
                survived = False
                print('dead by ghost')
                return collected, survived
        # wall check
        if not valid_pos(H, W, pacman.pos) or is_wall(field, pacman.pos):
            survived = False
            print('dead by wall')
            return collected, survived
        # coin check
        #field[pacman.pos[0]][pacman.pos[1]] = '?' # tmp
        if field[pacman.pos[0]][pacman.pos[1]] == 'C':
            collected += 1
            field[pacman.pos[0]][pacman.pos[1]] = '_'
        i += 1
    return collected, survived
    

def exec(code):
    global H, W
    lines = code.split('\n')
    n = int(lines[0])
    H = W = n
    field_lines = lines[1:n+1]
    field = parse_filed(field_lines)
    n += 1
    max_moves = int(lines[n+1])
    pacman, n = parse_agent(PACMAN, lines, n)
    #n_ghosts = int(lines[n])
    #n += 1
    ghosts = []
    #ghosts = [None for _ in range(n_ghosts)]
    #for gid in range(n_ghosts):
    #    ghosts[gid], n = parse_agent(GHOST, lines, n)
    #collected, survived = game_loop(field, pacman, ghosts)
    allmoves = game_loop(field, pacman, ghosts)
    assert(len(allmoves) < max_moves)
    return allmoves
    #return f'{collected} {"YES" if survived else "NO"}'

def run(lvl, tc, extra=''):
    text = Path(f'lvl{lvl}/level{lvl}_{tc}.in').read_text()
    out = exec(text)
    Path(f'lvl{lvl}/level{lvl}_{tc}{extra}.out').write_text(out)

print(Path.cwd())

run(4, 5)
#run(4, 'example', '_ours')
#for tc in range(1, 6):
#    run(4, tc)
#