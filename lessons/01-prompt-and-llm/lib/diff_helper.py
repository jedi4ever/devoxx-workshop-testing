from colorama import Fore, Back, Style
import difflib

def diff_code(a: str, b: str) -> str:
    output = []
    matcher = difflib.SequenceMatcher(None, a, b)

    green = Back.GREEN
    red = Back.RED
    endgreen = Back.WHITE
    endred = Back.WHITE

    output.append(Back.WHITE + Fore.BLACK)
    for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
        if opcode == 'equal':
            output.append(a[a0:a1])
        elif opcode == 'insert':
            output.append(f'{green}{b[b0:b1]}{endgreen}')
        elif opcode == 'delete':
            output.append(f'{red}{a[a0:a1]}{endred}')
        elif opcode == 'replace':
            output.append(f'{green}{b[b0:b1]}{endgreen}')
            output.append(f'{red}{a[a0:a1]}{endred}')
    output.append(Style.RESET_ALL)
    return ''.join(output)