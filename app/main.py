from os.path import basename
from subprocess import call
from typing import Dict
from os import getenv
from glob import glob


def collect_executables() -> Dict[str, str]:
    executables = {}

    for directory in getenv('PATH').split(':'):
        executables.update({
            basename(executable): directory for executable in glob(directory + '/*')
        })

    return executables


def main() -> None:
    executables = collect_executables()

    while True:
        try:
            line = input('$ ').split(' ')

            if not line:
                print('Could not parse input')
            else:
                command, arguments = line[0], line[1:]

                if command == 'exit':
                    exit(
                        int(arguments[0]) if arguments else 0
                    )
                elif command == 'echo':
                    print(' '.join(arguments))
                elif command == 'type':
                    target = arguments[0] if arguments else None

                    if target in ('exit', 'echo', 'type'):
                        print(f'{target} is a shell builtin')
                    else:
                        directory = executables.get(target)

                        if directory:
                            print(f'{target} is {directory}/{target}')
                        else:
                            print(f'{target} not found')
                else:
                    if command.startswith('/'):
                        call(
                            '{} {}'.format(
                                command,
                                ' '.join(arguments)
                            ),
                            shell=True
                        )
                    else:
                        directory = executables.get(command)

                        if directory:
                            call(
                                '{}/{} {}'.format(
                                    directory,
                                    command,
                                    ' '.join(arguments)
                                ),
                                shell=True
                            )
                        else:
                            print(f'{command}: command not found')
        except (KeyboardInterrupt, EOFError):
            exit(130)

    exit(0)


if __name__ == '__main__':
    main()
