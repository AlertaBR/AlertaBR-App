# 🌊 AlertaBR - Aplicativo

<div align="center">

![GitHub language count](https://img.shields.io/github/languages/count/AlertaBR/AlertaBR-App?style=for-the-badge)
![GitHub repo size](https://img.shields.io/github/repo-size/AlertaBR/AlertaBR-App?style=for-the-badge)
![GitHub Downloads (all assets, latest release)](https://img.shields.io/github/downloads/AlertaBR/AlertaBR-App/latest/total?style=for-the-badge)

<img src="./assets/App-presentGIF.gif" alt="Demonstração do app AlertaBR" width=650 style="border-radius: 20px; border: 2px solid gray;">
</div>

**AlertaBR é um aplicativo mobile** voltado à prevenção de enchentes em quaisquer região do Brasil e principalmente as regiões de risco. Monitorando em tempo real com base na localização selecionadas pelo usuário dentro do app, utiliza de alertas visuais geolocalizados sobre condições climáticas críticas, moderadas ou normais, notificando o usuário com antecedência para que possa agir de forma segura e preventiva.

<!-- Link do vídeo no YT -->
[Saiba Mais sobre o app](#)
---

## 🚀 Funcionalidades

- Pesquisa por localização (nome da rua, CEP ou coordenadas)
- Visualização em mapa interativo (*OpenStreetMap*)
- Previsão do tempo detalhada (*chuva, umidade, risco de enchente, total de chuva*)
- Interface moderna usando CustomTkinter
- Classificação de risco em 3 níveis:
    * 🔵 **Sem Chuvas**
    * 🟢 **Fraco**
    * 🟡 **Moderado**
    * 🔴 **Crítico**

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia         | Descrição                                                  |
|--------------------|------------------------------------------------------------|
| [Python](https://www.python.org/)    | Linguagem principal para o desenvolvimento do aplicativo   |
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)  | Biblioteca de UI moderna baseada em Tkinter                |
| [TkinterMapView](https://github.com/TomSchimansky/TkinterMapView)  | Mapa interativo usando OpenStreetMap via Tkinter           |
| [Open-Meteo API](https://open-meteo.com/)  | API gratuita para previsão do tempo e dados meteorológicos |
| [Nominantim](https://nominatim.org/)   | Fonte de dados geográficos para exibição no mapa com [OpenStreetMap](https://www.openstreetmap.org)           |
| [Pandas](https://pandas.pydata.org/)        | Manipulação e análise de dados, utilizado para datas                  |



---

## 📦 Como executar o AlertaBR
Para instalar o **AlertaBR**, siga estas etapas:

### 📱 Download do executável (Recomendado)

A versão compilada do aplicativo está disponível na seção de Releases do repositório.

Você pode baixá-la para executar o programa diretamente, sem a necessidade de instalar o Python ou bibliotecas adicionais.

👉 **[Baixe o aplicativo agora!]()**

### 🖥️ Usando o repositório


#### Windows
```bash
git clone https://github.com/AlertaBR/AlertaBR-App.git

cd AlertaBR-App # Acessa o diretório

pip install -r requirements.txt # Importante para baixar todas as bibliotecas necessárias

python main.py # Executa o projeto
```

## 📝 Licença

Esse projeto está sob licença. Veja o arquivo [LICENCE](LICENSE) para mais detalhes.
