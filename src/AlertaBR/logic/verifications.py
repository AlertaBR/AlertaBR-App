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
    return not (containsValue(email, '@') and containsValue(email, '.com'))


def replaceString(strValue, c):
    """Função que troca espaços vazios por uma caracterece que o usuário escolher

    Args:
        strValue (_str_): String em que o usuário quer modificar
        c (_str_): String ou caractére que o usuário quer adicionar
    Returns:
        str: String formatada com a nova cartére
    """
    fstring = ''
    for i in range(len(strValue)):
        char = strValue[i]
        if strValue[i] == ' ':
            char = c
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
    

def checkAddresIsValid(address):
    """Função que verifica se o endereço digitado é válido

    Args:
        address (_str_): Endereço digitado pelo usuário
    Returns:
        bool: Retorna se True se for válido e False para inválido.
    """
    address = address.strip()
    special_characters = r'/@#_*()$!:£=+;><][]{}^~`´\'\"\\|'
    return len(address) < 2 or not address or special_characters in address