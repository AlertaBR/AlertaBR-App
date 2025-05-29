from utils.tools import Color, menu, getLocalTime

def main():
    # Substituir pela localização atual no google maps
    print(f'Hora Atual: {getLocalTime()}')
    resp = menu(['Buscar região de risco', 'Ligar para autoridades', 'Faça um report', 'Veja os reports da região' 'Configurações'], Color.YELLOW)
    switchMenu(resp)

if __name__ == '__main__':
    main()