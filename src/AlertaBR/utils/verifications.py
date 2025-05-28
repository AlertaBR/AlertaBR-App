from AlertaBR.utils import helpers as h

def forceInputIsNumber(msg):
    """
    Função que força o input de número inteiro do usuárioh    msg (param) => Mensagem contida no input do usuário\n
    Tipo de retorno => int
    """
    num = input(msg)
    while not num.isnumeric():
       print('Digite um número inteiro válido')
       num = input(msg)
    return int(num)

def checkIfEmailIsValid(email):
    """
    Função a qual irá verificar o email do usuário 
    email (param) => endereço de email do usuário\n
    Tipo de retorno => boolean
    """
    if not (h.containsValue(email, '@') and h.containsValue(email, '.com')):
        return False
    return True
