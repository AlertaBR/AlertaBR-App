# 🌊 AlertaBR - Aplicativo

**AlertaBR** é um aplicativo desenvolvido em Python que permite o usuário verificar, com base em uma localização personalizada (rua, cidade, CEP ou coordenadas geográficas), as **condições climáticas** e o **risco de enchentes para os próximos 7 dias**. A proposta é fornecer previsibilidade meteorológica com usabilidade simples e visual.

---

## 🚀 Funcionalidades

- Pesquisa por localização (nome da rua, CEP ou coordenadas)
- Visualização em mapa interativo (OpenStreetMap)
- Previsão do tempo detalhada (chuva, umidade, risco de enchente, total de chuva)
- Classificação de risco em 3 níveis:
    * 🟢 Baixo
    * 🟡 Moderado
    * 🔴 Crítico
- Interface moderna usando CustomTkinter

---

## 🛠️ Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [Open-Meteo API](https://open-meteo.com/)
- [OpenStreetMap via TkinterMapView](https://github.com/TomSchimansky/TkinterMapView)
- [Pandas](https://pandas.pydata.org/)

---

## 📦 Como executar o AlertaBR

### 📱 Download do executável (Recomendado)
A versão compilada do aplicativo está disponível na seção de Releases do repositório.

Você pode baixá-la para executar o programa diretamente, sem a necessidade de instalar o Python ou bibliotecas adicionais.

👉 [Baixe o aplicativo agora!]()

### 🖥️ Usando o repositório

```bash
git clone https://github.com/AlertaBR/AlertaBR-App.git

cd AlertaBR-App # Acessa o diretório

pip install -r requirements.txt # Importante para baixar todas as bibliotecas necessárias

python main.py # Executa o projeto
```
