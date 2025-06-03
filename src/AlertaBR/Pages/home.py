import customtkinter as ctk
from tkintermapview import TkinterMapView
from CTkMessagebox import CTkMessagebox
from PIL import Image
import pywinstyles
from datetime import datetime
from src.AlertaBR.logic.maps import getStreetResponse
from src.AlertaBR.logic.climatic import enviromentInfos

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")




class App(ctk.CTk):
    defaultLat = -23.5831527
    defaultLng = -46.6568236
    width = 390
    height = 844
    rainCritic = 10
    rainAlert = 2.6
    floodCritic = 80
    floodAlert = 60

    def __init__(self):
        super().__init__()

        self.title("AlertaBR")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(0, 0)
        #  self.iconbitmap(default="src/AlertaBR/Pages/images/favicon.ico")
        self.eval("tk::PlaceWindow . center")
        
        self.fontText = ctk.CTkFont(family="Arial", size=16, weight="normal")
        self.fontTitle = ctk.CTkFont(family="Arial", size=30, weight="bold")
        self.fontInfos = ctk.CTkFont(family="Arial", size=18, weight="bold")
        self.fontInfos2 = ctk.CTkFont(family="Arial", size=20, weight="normal", slant='italic');

        # Criando Mapa
        self.gmapWidget = TkinterMapView(self, width=self.width, height=self.height)
        self.gmapWidget.place(x=0, y=0, relwidth=1, relheight=1)  # Ocupa tudo
        self.gmapWidget.set_tile_server(
            "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22
        )  # Define o Mapa exibido como no Google Maps
        self.gmapWidget.set_position(self.defaultLat, self.defaultLng)

        # Desabilitando botões de zoom superior
        self.gmapWidget.canvas.itemconfig(
            self.gmapWidget.button_zoom_in.canvas_rect, state="hidden"
        )
        self.gmapWidget.canvas.itemconfig(
            self.gmapWidget.button_zoom_in.canvas_text, state="hidden"
        )
        self.gmapWidget.canvas.itemconfig(
            self.gmapWidget.button_zoom_out.canvas_rect, state="hidden"
        )
        self.gmapWidget.canvas.itemconfig(
            self.gmapWidget.button_zoom_out.canvas_text, state="hidden"
        )

        self.searchFrame = ctk.CTkFrame(self, width=self.width, bg_color="#000001")
        self.searchFrame.pack(side="top", pady=80)
        self.searchFrame.configure(fg_color="transparent")
        pywinstyles.set_opacity(self.searchFrame, color="#000001")

        # Criando barra de pesquisa por região
        self.searchEntry = ctk.CTkEntry(
            self.searchFrame,
            width=300,
            height=50,
            corner_radius=20,
            placeholder_text="Pesquise Aqui",
            placeholder_text_color="gray",
            font=self.fontText,
            fg_color="white",
            bg_color="#000001",
        )
        self.searchEntry.focus()
        self.searchEntry.pack(side="left", padx=10)

        # Criando botão para pesquisar
        searchIcon = ctk.CTkImage(
            light_image=Image.open("src/AlertaBR/Pages/images/search.png"),
            size=(30, 30),
        )
        self.searchButton = ctk.CTkButton(
            self.searchFrame,
            width=40,
            height=40,
            corner_radius=5,
            image=searchIcon,
            text="",
            command=self.setOnMapRegion,
            fg_color="#001D3D",
            hover_color="#024388",
            bg_color="#000001",
        )
        self.searchButton.pack(side="right", padx=10)

        self.searchEntry.bind("<Return>", self.setOnMapRegion)

        self.userMenuFrame = ctk.CTkFrame(
            self, width=self.width, height=70, fg_color="#001D3D"
        )
        self.userMenuFrame.grid_columnconfigure((0, 1, 2), weight=1)

        # Criando Icones
        mapIcon = ctk.CTkImage(
            light_image=Image.open("src/AlertaBR/Pages/images/map.png"), size=(33, 33)
        )
        profileIcon = ctk.CTkImage(
            light_image=Image.open("src/AlertaBR/Pages/images/profile.png"),
            size=(33, 33),
        )
        reportsIcon = ctk.CTkImage(
            light_image=Image.open("src/AlertaBR/Pages/images/reports.png"),
            size=(33, 33),
        )

        # Criando botões do menu
        self.mapButton = ctk.CTkButton(
            self.userMenuFrame,
            width=33,
            height=33,
            fg_color="transparent",
            bg_color="transparent",
            image=mapIcon,
            hover_color="#003063",
            text="",
        )

        self.profileButton = ctk.CTkButton(
            self.userMenuFrame,
            width=33,
            height=33,
            fg_color="transparent",
            bg_color="transparent",
            image=profileIcon,
            hover_color="#003063",
            text="",
        )

        self.reportsButton = ctk.CTkButton(
            self.userMenuFrame,
            width=33,
            height=33,
            fg_color="transparent",
            bg_color="transparent",
            image=reportsIcon,
            hover_color="#003063",
            text="",
        )

        # Layout menu
        self.userMenuFrame.pack(side="bottom", fill="both")
        self.reportsButton.grid(row=0, column=0, padx=2, pady=2)
        self.mapButton.grid(row=0, column=1, padx=2, pady=2)
        self.profileButton.grid(row=0, column=2, padx=2, pady=2)

        # Criando frame de clima
        self.weatherFrame = ctk.CTkFrame(
            self, width=self.width, height=140, fg_color="white", bg_color="#000001"
        )
        pywinstyles.set_opacity(self.weatherFrame, color="#000001")
        self.weatherFrame.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.weatherFrame.grid_columnconfigure((0, 1, 2), weight=1)

        # Criando Infos showWeatherInfos
        self.data = ctk.CTkLabel(
            self.weatherFrame,
            font=self.fontInfos,
            text=f"Hoje: {datetime.now().strftime('%d/%m/%y')}",
            compound='center',
            anchor='center'
        )
        
        self.rainStatus = ctk.CTkLabel(
            self.weatherFrame,
            font=self.fontText,
            compound='left',
        )
        self.rainTotal = ctk.CTkLabel(
            self.weatherFrame,
            font=self.fontTitle,
            compound='left',
            anchor='e'
        )
        self.humid = ctk.CTkLabel(
            self.weatherFrame,
            font=self.fontInfos,
            text="Umid. ",
            compound='left',
            anchor='e'
        )
        self.rainInMM = ctk.CTkLabel(
            self.weatherFrame,
            font=self.fontInfos2,
            text="0.0",
            compound='left',
            anchor='e'
        )
        self.floodtitle = ctk.CTkLabel(
            self.weatherFrame,
            font=self.fontInfos,
            compound='left',
        )

        # Layout
        self.rainTotal.grid(row=1, column=1)
        self.rainStatus.grid(row=2, column=0)
        self.data.grid(row=0, column=1)
        self.humid.grid(row=1, column=2)
        self.rainInMM.grid(row=2, column=2)
        self.floodtitle.grid(row=3, column=2)

    def setOnMapRegion(self):
        address = self.searchEntry.get()
        special_characters = r'/@#_*()$!:£=+;><][]{}^~`´\'\"\\|'
        if len(address) < 5 or not address or special_characters in address:
            CTkMessagebox(
                title="Endereço Incorreto",
                message="O campo de endereço está vazio ou incorreto e deve ter algum conteúdo.",
                icon="cancel",
                option_1="Ok",
            )
            self.searchEntry.delete(0, len(address))
            return

        coord = getStreetResponse(address)
        if len(coord) == 0:
            CTkMessagebox(
                title="Endereço Inválido",
                message="O endereço digitado não existe ou está incorreto.",
                icon="cancel",
                option_1="Ok",
            )
            self.searchEntry.delete(0, len(address))
            return

        lat = float(coord["lat"])
        lon = float(coord["lon"])

        self.gmapWidget.delete_all_marker()
        self.gmapWidget.set_position(lat, lon)
        self.gmapWidget.set_marker(lat, lon, text=coord["name"])
        self.searchEntry.delete(0, len(address))
        self.showWeatherInfos(lat, lon)

    def showWeatherInfos(self, lat, lon):
        enviroment = enviromentInfos(lat, lon)
        currWeather = enviroment.createWeatherData()
        flood = enviroment.createFloodData()

        self.weatherFrame.pack(side="bottom", fill="both")

        self.inputRainStatusLabel(currWeather['precipitation_probability'], currWeather['weather_code'])
        self.rainTotal.configure(
            text=f"{currWeather['precipitation_probability']:.0f}%"
        )
        self.humid.configure(text=f"Umid. {currWeather['relative_humidity']:.0f}%")
        self.rainInMM.configure(text=f"{currWeather['rain']:.1f} mm")
        self.inputFloodStatusLabel(flood["river_discharge"][0], currWeather['rain'])

    def inputRainStatusLabel(self, precip):
        self.weatherImage = ctk.CTkImage(size=(50, 50), light_image=Image.open("src/AlertaBR/Pages/images/WeathterisNormal.png"), )

        if precip <= 40:
            self.rainStatus.configure(text_color="#006CD2")
            self.rainStatus.configure(text="Sem Chuvas")
            return

        if rain >= self.rainCritic or precip >= 70:
            self.weatherImage.configure(light_image=Image.open("src/AlertaBR/Pages/images/WeatherisCritical.png"))
            self.rainStatus.configure(text_color="#f00d0d")
            self.rainTotal.configure(text_color="#f00d0d")
            self.rainStatus.configure(text="Chuva Forte")
        elif rain >= self.rainAlert or precip >= 50:
            self.weatherImage.configure(light_image=Image.open("src/AlertaBR/Pages/images/WeatherisAlert.png"))
            self.rainStatus.configure(text_color="#f0aa0d")
            self.rainTotal.configure(text_color="#f0aa0d")
            self.rainStatus.configure(text="Chuva Amena")
        else:
            self.weatherImage.configure(light_image=Image.open("src/AlertaBR/Pages/images/WeatherisOk.png"))
            self.rainStatus.configure(text_color="#14AE5C")
            self.rainTotal.configure(text_color="#14AE5C")
            self.rainStatus.configure(text="Chuva Fraca")
            
        self.weatherImgLabel = ctk.CTkLabel(self.weatherFrame, image=self.weatherImage, text='', bg_color='white')
        pywinstyles.set_opacity(self.weatherImgLabel, color="white")
        self.weatherImgLabel.grid(row=1, column=0)

    def inputFloodStatusLabel(self, flood, rain):
        if flood >= self.floodCritic and rain >= self.rainCritic:
            self.floodtitle.configure(text="Enchente CONFIRMADA")
        elif flood >= self.floodAlert and rain >= self.rainAlert:
            self.floodtitle.configure(text="Possível Enchente")
        else:
            self.floodtitle.configure(text="Sem Enchente")

    # def weatherContainer(self):

    # def userMenuContainer(self):
