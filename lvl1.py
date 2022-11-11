from pathlib import Path
#import numpy as np
#import itertools

def exec(code):
    return str(code.count('C'))
    out = ''
    printint = False
    started = False
    for n, line in enumerate(code.split('\n')):
        line = line.strip()
        if n == 0:
            continue
        tokens = line.split(' ')
        for token in tokens:
            if token == 'start' and not started:
                started = True
                continue
            if started:
                if token == 'print':
                    printint = True
                elif printint:
                    out+= token
                    printint = False
    return out

def run(lvl, tc, extra=''):
    text = Path(f'lvl{lvl}/level{lvl}_{tc}.in').read_text()
    out = exec(text)
    Path(f'lvl{lvl}/level{lvl}_{tc}{extra}.out').write_text(out)

print(Path.cwd())

run(1, 'example', '_ours')
for tc in range(1, 6):
    run(1, tc)
