from pathlib import Path
#import numpy as np
#import itertools
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import sys
import random

PACMAN = '.'
GHOST = 'G'

if True:
    oldprint = print
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
                    print(agent.type, end='', flush=True)
                    break
            else:
                print(pixel, end='', flush=True)
        print('', flush=True)
    print(r, c)
        
def str_to_pos(s):
    return tuple(int(x)-1 for x in s.split(' '))

class Agent:
    # TODO WHAT THA FUUUUUUUUUUUCK
    #initial_pos = (0, 0)
    #pos = (0, 0)
    #moves = ""
    #moves_left = []
    #moves_hist = []
    
    def __init__(self, type, pos, moves):
        self.type = type
        self.initial_pos = pos
        self.pos = pos
        self.moves = moves
        self.moves_left = [x for x in self.moves]
        self.moves_hist = []
        
    def make_move(self, field, agents):
        # find target
        if self.type == GHOST:
            if len(self.moves_left) == 0:
                self.moves = self.moves[::-1]
                self.moves_left = [x for x in self.moves]
        else:
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
                    return None
                #    if self.pos != self.initial_pos:
                #        coin_pos = self.initial_pos
                #    else:
                #        return None
                print('xxx', self.pos)
                ghosts = [x for x in agents if x.type == GHOST]
                
                matrix = [[0 if (x == 'W') else 1 for x in row] for row in field]
                for ghost in ghosts:
                    matrix[ghost.pos[0]][ghost.pos[1]] = 0
                for x in matrix:
                    print(x)
                grid = Grid(matrix=matrix)
    
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
                if len(new_moves) == 0:
                    options = []
                    for d in 'LRUD':
                        v = str_to_vec(d)
                        npos = (v[0] + self.pos[0], v[1] + self.pos[1])
                        if is_wall(field, npos):
                            continue
                        options.append(d)
                    new_moves = [random.choice(options)]
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
        
    
def parse_agent(type, lines, n, no_moves=False):
    start = str_to_pos(lines[n])
    if no_moves:
        moves = ''
    else:
        moves = lines[n+2]
    agent = Agent(type, start, moves)
    return agent, n+1 if no_moves else n+3

def valid_pos(H, W, pos):
    return (0 <= pos[0] < H) and (0 <= pos[1] < W)

def is_wall(field, pos):
    return field[pos[0]][pos[1]] == 'W'

def game_loop(field, pacman, ghosts):
    
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
            new_pos = agent.make_move(field, agents)
            #print(agent_str, '->', new_pos)
            if new_pos == None:
                return ''.join(pacman.moves_hist)
            agent.pos = new_pos
        # pacman ghost check
        for ghost in ghosts:
            if ghost.pos == pacman.pos:
                survived = False
                oldprint('dead by ghost')
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
    pacman, n = parse_agent(PACMAN, lines, n, no_moves=True)
    n_ghosts = int(lines[n])
    n += 1
    ghosts = []
    ghosts = [None for _ in range(n_ghosts)]
    for gid in range(n_ghosts):
        ghosts[gid], n = parse_agent(GHOST, lines, n)
    max_moves = int(lines[n])
    
    for r, row in enumerate(field):
        for c, pixel in enumerate(row):
            if pixel in 'PEG':
                field[r][c] = ' '
                
    pacman_possum = (pacman.pos[0] + pacman.pos[1]) % 2
    for i in range(len(ghosts))[::-1]:
        ghost = ghosts[i]
        ghost_possum = (ghost.pos[0] + ghost.pos[1]) % 2
        if pacman_possum != ghost_possum:
            del ghosts[i]
    
    allmoves = game_loop(field, pacman, ghosts)
    assert(len(allmoves) < max_moves)
    return allmoves
    #return f'{collected} {"YES" if survived else "NO"}'

def run(lvl, tc, extra=''):
    text = Path(f'lvl{lvl}/level{lvl}_{tc}.in').read_text()
    out = exec(text)
    Path(f'lvl{lvl}/level{lvl}_{tc}{extra}.out').write_text(out)

print(Path.cwd())

run(5, 4)
#run(5, 'example', '_ours')
#for tc in range(1, 6):
#    run(5, tc)
#