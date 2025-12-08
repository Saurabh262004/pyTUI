from typing import Callable

def test(p1='def1', p2='def2'):
  print(f'p1: {p1}, p2: {p2}')

class Arg:
  def __init__(self, cmdLineTriggers: str | int):
    self.cmdLineTriggers = cmdLineTriggers

class Command:
  def __init__(self, fn: Callable, args: list[Arg] | tuple[Arg], trigger: str, aliases: list[str] | tuple[str], desc: str):
    self.fn = fn
    self.args = args
    self.trigger = trigger
    self.aliases = aliases
    self.desc = desc

    self.tgrTuple = [trigger,]

    self.tgrTuple.extend(aliases)

    self.tgrTuple = tuple(self.tgrTuple)

    self.tgrStr = f'{self.trigger}, '

    for tgr in self.aliases:
      self.tgrStr += f'{tgr}, '

    self.tgrStr = self.tgrStr[:-2]

  def call(self, args: dict):
    pass

  def help(self):
    print(f'\nAliases: {self.tgrStr}\n')

class TUI:
  def __init__(self, title: str, desc: str = '', prompt: str = ''):
    self.title = title
    self.desc = desc
    self.prompt = prompt

    self.currentInput: list[str] = []
    self.inputHistory: list[list[str]] = []

    self.commands: dict[str, Command] = {}
    self.commandsDescs: dict[tuple, str] = {}

    self.maxLenCmd = 4

    helpCMD = Command(self.help, (Arg(),), 'help', ('h',), 'Print this output')
    quitCMD = Command(self.close, (Arg(),), 'quit', ('q',), 'Quit TUI loop')

    self.setCommand(helpCMD)
    self.setCommand(quitCMD)

  @staticmethod
  def getProcessedInput(tuiInput: str) -> list[str]:
    return tuiInput.split()

  def loop(self):
    while self.running:
      self.currentInput = TUI.getProcessedInput(input(self.prompt))

      if len(self.currentInput) < 1:
        continue

      self.inputHistory.append(self.currentInput)

      cmd = self.currentInput[0]

      if cmd in self.commands:
        self.commands[cmd].fn()
      else:
        print(f'"{cmd}" is not a recognized command')

  def close(self):
    print(f'Closing {self.title}')

    self.running = False

  def open(self):
    self.running = True

    self.loop()

  def help(self):
    print(f'\n ----- {self.title} -----\n')

    if len(self.desc) > 0:
      print(f' {self.desc}\n')

    for k, v in self.commandsDescs.items():
      ln = max(self.maxLenCmd + 3, 20)

      print(f'{self.commands[k[0]].tgrStr:<{ln}}: {v}')

    print()

  def setCommand(self, cmd: Command) -> bool:
    self.commandsDescs[cmd.tgrTuple] = cmd.desc

    for tgr in cmd.tgrTuple:
      self.maxLenCmd = max(self.maxLenCmd, len(tgr))
      self.commands[tgr] = cmd

myTUI = TUI('TUI','A test TUI app', 'input: ')

myTUI.setCommand(Command(test, (Arg(),), 'test', ('t',), 'A test function.'))

myTUI.commands['h'].help()

myTUI.open()
