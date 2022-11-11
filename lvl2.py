from pathlib import Path
#import numpy as np
#import itertools

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

def exec(code):
    lines = code.split('\n')
    n = int(lines[0])
    field_lines = lines[1:n]
    field = parse_filed(field_lines)
    start = [int(x)-1 for x in lines[n+1].split(' ')]
    moves = lines[n+3]
    print(field)
    print('start', start)
    print('moves', moves)
    pos = start
    collected = 0
    for i, move in enumerate(moves):
        print('----------------------- round', i)
        print_field(field)
        mvect = str_to_vec(move)
        new_pos = (mvect[0] + pos[0], mvect[1] + pos[1])
        print(pos, new_pos)
        #field[new_pos[0]][new_pos[1]] = '?' # tmp
        if field[new_pos[0]][new_pos[1]] == 'C':
            collected += 1
            field[new_pos[0]][new_pos[1]] = '_'
        pos = new_pos
    return str(collected)

def run(lvl, tc, extra=''):
    text = Path(f'lvl{lvl}/level{lvl}_{tc}.in').read_text()
    out = exec(text)
    Path(f'lvl{lvl}/level{lvl}_{tc}{extra}.out').write_text(out)

print(Path.cwd())

run(2, 'example', '_ours')
for tc in range(1, 6):
    run(2, tc)
