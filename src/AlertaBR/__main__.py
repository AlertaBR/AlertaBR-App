from utils.tools import Color, menu
# from .utils.googleMaps import getLocal

def main():
   # print(f'Localização Atual: {getLocal()}')
    menu(['Buscar região de risco', 'Ligar para autoridades', 'Faça um report', 'Veja os reports da região' 'Configurações'], Color.YELLOW)

if __name__ == '__main__':
    main()