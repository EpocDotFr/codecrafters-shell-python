from os.path import basename
from subprocess import call
from os import getenv
from glob import glob


def main() -> None:
    executables = {
        directory: [
            basename(executable) for executable in glob(directory + '/*')
        ] for directory in getenv('PATH').split(':')
    }

    while True:
        try:
            line = input('$ ').split(' ')

            if not line:
                print('Could not parse input')
            elif line[0] == 'exit':
                exit(
                    int(line[1]) if len(line) == 2 else 0
                )
            elif line[0] == 'echo':
                print(' '.join(line[1:]))
            elif line[0] == 'type':
                target = line[1] if len(line) == 2 else None

                if target in ('exit', 'echo', 'type'):
                    print(f'{target} is a shell builtin')
                else:
                    found = False

                    for directory, execs in executables.items():
                        if target in execs:
                            print(f'{target} is {directory}/{target}')

                            found = True

                            break

                    if not found:
                        print(f'{target} not found')
            else:
                executable = None

                for directory, execs in executables.items():
                    if line[0] in execs:
                        executable = f'{directory}/{line[0]}'

                        break

                if executable:
                    call(
                        '{} {}'.format(
                            executable,
                            ' '.join(line[1:] if len(line) > 1 else [])
                        ),
                        shell=True
                    )
                else:
                    print(f'{line[0]}: command not found')
        except (KeyboardInterrupt, EOFError):
            exit(130)

    exit(0)


if __name__ == '__main__':
    main()
