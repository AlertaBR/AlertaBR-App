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

fontfamily = "Segoe UI"


class App(ctk.CTk):
    defaultLat = -23.5831527
    defaultLng = -46.6568236
    width = 390
    height = 844
    rainCritic = 10
    rainAlert = 2.6

    def __init__(self):
        super().__init__()

        self.title("AlertaBR")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(0, 0)
        #  self.iconbitmap(default="src/AlertaBR/Pages/images/favicon.ico")
        self.eval("tk::PlaceWindow . center")

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
            font=("Ubunto", 16),
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
        self.weatherFrame = ctk.CTkFrame(self, width=self.width, height=180, fg_color="white", bg_color="#000001")
        pywinstyles.set_opacity(self.weatherFrame, color="#000001")
        self.weatherFrame.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.weatherFrame.grid_columnconfigure((0, 1, 2), weight=1)
        
        
        # Criando Infos showWeatherInfos
        self.data = ctk.CTkLabel(self.weatherFrame, font=(fontfamily, 15), text=datetime.now().strftime('%d/%m/%y'), anchor="center")
        self.rainStatus = ctk.CTkLabel(self.weatherFrame, font=("Ubuntu Medium", 15), anchor="e")
        self.rainTotal = ctk.CTkLabel(self.weatherFrame, font=(fontfamily, 15), text='Total. ', anchor="e")
        self.humid = ctk.CTkLabel(self.weatherFrame, font=(fontfamily, 15), text='Umid. ', anchor="e")
        self.floodVolume = ctk.CTkLabel(self. weatherFrame, font=("Ubuntu Bold", 50), text='0.0', anchor="w")
        self.floodtitle = ctk.CTkLabel(self.weatherFrame, font=("Segoe UI Semibold", 15), text='Volume em m³/s', anchor="w")
        
        # Layout
        self.data.grid(row=0, column=1)
        self.rainStatus.grid(row=1, column=0)
        self.rainTotal.grid(row=2, column=0)
        self.humid.grid(row=3, column=0)
        self.floodVolume.grid(row=2, column=2)
        self.floodtitle.grid(row=3, column=2)
        

    def setOnMapRegion(self):
        self.gmapWidget.delete_all_marker()
        address = self.searchEntry.get()
        if len(address) < 5 or not address:
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

        self.gmapWidget.set_position(lat, lon)
        self.gmapWidget.set_marker(lat, lon, text=coord["name"])
        self.searchEntry.delete(0, len(address))
        self.showWeatherInfos(lat, lon)

    def showWeatherInfos(self, lat, lon):
        enviroment = enviromentInfos(lat, lon)
        currWeather = enviroment.createWeatherData()
        flood = enviroment.createFloodData()
        
        self.weatherFrame.pack(side="bottom", fill="both")
        
        self.inputRainStatusLabel(currWeather['rain'])
        self.rainTotal.configure(text=f'Prev. {currWeather['precipitation_probability']:.0f}%')
        self.humid.configure(text=f'Umid. {currWeather['relative_humidity']:.0f}%')
        self.floodVolume.configure(text=f'{flood['river_discharge'][0]:.1f}')
    
    
    def inputRainStatusLabel(self, rain):
        if rain == 0:
            self.rainStatus.configure(text_color="#006CD2")
            self.rainStatus.configure(text="Sem Chuvas")
            return
        
        if rain >= self.rainCritic:
            self.rainStatus.configure(text_color="#f00d0d")
            self.rainStatus.configure(text="Chuva Forte")
        elif rain >= self.rainAlert:
            self.rainStatus.configure(text_color="#f0aa0d")
            self.rainStatus.configure(text="Chuva Amena")
        else:
            self.rainStatus.configure(text_color="#47f00d")
            self.rainStatus.configure(text="Chuva Fraca")
        


    # def weatherContainer(self):


    # def userMenuContainer(self):
