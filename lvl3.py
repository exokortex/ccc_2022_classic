from pathlib import Path
#import numpy as np
#import itertools

PACMAN = 'P'
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
        
def print_field(field):
    for row in field:
        print(''.join(row))
        
def str_to_pos(s):
    return tuple(int(x)-1 for x in s.split(' '))

class Agent:
    pos = (0, 0)
    moves = ""
    moves_left = []
    
    def __init__(self, type, pos, moves):
        self.type = type
        self.pos = pos
        self.moves = moves
        self.moves_left = [x for x in moves]
        
    def make_move(self):
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
    agents = [pacman] + ghosts
    print(field)
    for agent in agents:
        print(agent)

    collected = 0
    survived = True
    i = 0
    while True:
        print('====================== round', i)
        print_field(field)
        for agent in agents:
            agent_str = str(agent)
            new_pos = agent.make_move()
            print(agent_str, '->', new_pos)
            if new_pos == None:
                return collected, survived
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
    pacman, n = parse_agent(PACMAN, lines, n)
    n_ghosts = int(lines[n])
    n += 1
    ghosts = [None for _ in range(n_ghosts)]
    for gid in range(n_ghosts):
        ghosts[gid], n = parse_agent(GHOST, lines, n)
    collected, survived = game_loop(field, pacman, ghosts)
    return f'{collected} {"YES" if survived else "NO"}'

def run(lvl, tc, extra=''):
    text = Path(f'lvl{lvl}/level{lvl}_{tc}.in').read_text()
    out = exec(text)
    Path(f'lvl{lvl}/level{lvl}_{tc}{extra}.out').write_text(out)

print(Path.cwd())

run(3, 2)
run(3, 'example', '_ours')
for tc in range(1, 8):
    run(3, tc)
