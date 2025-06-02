from src.AlertaBR.logic import verifications as verif
from enum import Enum
from time import sleep

class Color(Enum):
    TRANSPARENT = '\033[m'
    WHITE = '\033[1;30m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[1;34m'
    PURPLE = '\033[1;35m'
    CYAN = '\033[1;36m'
    GRAY = '\033[1;37m'

def menu(options=[], color = Color.TRANSPARENT):
    while True:
        for i in range(len(options)):
            print(f'{color.value}[ {i+1} ] {Color.TRANSPARENT.value}{options[i]}')
            sleep(0.3)
        return verif.forValidAnswer('\033[32mEscolha uma das opções:\033[m ', options)
    
    
def getLocalTime():
    from datetime import datetime
    return datetime.now()