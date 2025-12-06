from typing import Callable

def test(p1='def1', p2='def2'):
  print(f'p1: {p1}, p2: {p2}')

class TUI:
  def __init__(self, title: str, desc: str = '', prompt: str = ''):
    self.title = title
    self.desc = desc
    self.prompt = prompt

    self.currentInput: list[str] = []
    self.inputHistory: list[list[str]] = []

    self.commands: dict[str, Callable] = {
      'quit': self.close,
      'q': self.close,
      'help': self.help,
      'h': self.help
    }

    self.commandsDescs: dict[tuple, str] = {
      ('help', 'h'): 'Print this output.',
      ('quit', 'q'): 'Quit TUI loop.'
    }

    self.maxLenCmd = 4

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
        self.commands[cmd]()
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

      cmds = ''

      for cmd in k:
        cmds += f'{cmd}, '

      cmds = cmds[:-2]

      print(f'{cmds:<{ln}}: {v}')

    print()

  def setCommand(self, trigger: str | list[str], fn: Callable, desc: str) -> bool:
    if len(trigger) < 1:
      return False

    if isinstance(trigger, str):
      trigger = (trigger,)

    for tgr in trigger:
      self.maxLenCmd = max(self.maxLenCmd, len(tgr))

    self.commandsDescs[trigger] = desc

    for tgr in trigger:
      self.commands[tgr] = fn

myTUI = TUI('TUI','A test TUI app', 'input: ')

myTUI.setCommand(('test', 't'), test, 'A test function.')

myTUI.open()
