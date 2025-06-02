from enum import Enum

class Time:
    Minutes = 0
    Seconds = 1

def forceInputIsNumber(msg):
    """
    Função que força o input de número inteiro do usuárioh    msg (param) => Mensagem contida no input do usuário\n
    msg (param) => Mensagem do usuário
    Tipo de retorno => int
    """
    num = input(msg)
    while not num.isnumeric():
       print('Digite um número inteiro válido')
       num = input(msg)
    return int(num)

def containsValue(obj, value):
    return value in obj

def forValidAnswer(msg, options):
    """
    Função que força o usuário ser uma das opções que o menu exige
    msg (param) => Mensagem do usuário
    options => Opções mostradas para o usuário
    Tipo de retorno => string
    """
    answ = input(msg).strip();
    while not answ.isnumeric() or options[int(answ)-1] not in options:
        print('Digite uma opção válida')
        answ = input(msg);
    return answ

def checkIfEmailIsValid(email):
    """
    Função a qual irá verificar o email do usuário 
    email (param) => endereço de email do usuário\n
    Tipo de retorno => boolean
    """
    if not (containsValue(email, '@') and containsValue(email, '.com')):
        return False
    return True


def replaceString(strValue):
    fstring = ''
    for i in range(len(strValue)):
        char = strValue[i]
        if strValue[i] == ' ':
            char = '+'
        fstring += char
    
    return fstring

def ConvertUnix(timestamp):
    """Função que converte um tempo Unix atual em horas

    Args:
        timestamp (_int_): Tempo atual que o usuário quer converter
    Returns:
        int: O tempo enviado convertido em horas
    """
    from datetime import datetime as dt
    
    date = dt.fromtimestamp(timestamp)
    
    return f'{date.hour}:{date.minute}h'
    

    