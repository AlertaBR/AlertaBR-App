from utils import helpers as h

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
    if not (h.containsValue(email, '@') and h.containsValue(email, '.com')):
        return False
    return True
