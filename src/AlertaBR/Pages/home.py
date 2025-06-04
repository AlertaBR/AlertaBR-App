import customtkinter as ctk
from tkintermapview import TkinterMapView
from CTkMessagebox import CTkMessagebox
from PIL import Image
import pywinstyles
from datetime import datetime
from src.AlertaBR.logic.maps import getStreetResponse
from src.AlertaBR.logic.climatic import enviromentInfos
from src.AlertaBR.logic import verifications as verif

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")




class App(ctk.CTk):
    defaultLat = -23.5831527
    defaultLng = -46.6568236
    width = 390
    height = 844
    criticalpct = 70
    alertpct = 50
    noRainpct = 30
   
    
    # Códigos de Clima obtidos na table universal WMO Code Table 4677 (Não estamos considerando névoa ou neve)
    okCodes = [range(0,10), 20, 50, 51, 60, 61, 80]
    alertCodes = [11, 12, 21, 52, 53, 62, 63, 81, 91, 92]
    criticalCodes = [22, 32, 54, 55, 64, 65, 82, 94, 95, 96, 97, 98, 99]
    
    floodCritic = 300
    floodAlert = 100
    rainCritic = 30
    rainAlert = 10
    showerCritic = rainCritic / 2
    showerAlert = rainAlert / 2
    

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
        self.gmapWidget = self.creatingMapView()
        
        #Criando botão de Ver previsão enchente em 7 dias
        self.buttonFlood =  self.createFloodButton()

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


        # Criando Menu do usuário
        self.userMenuFrame = ctk.CTkFrame(
            self, width=self.width, height=70, fg_color="#001D3D"
        )
        self.userMenuFrame.grid_columnconfigure((0, 1, 2), weight=1)

        # Criando Icones do menu
        mapIcon = ctk.CTkImage(light_image=Image.open("src/AlertaBR/Pages/images/map.png"), size=(33, 33))
        profileIcon = ctk.CTkImage(light_image=Image.open("src/AlertaBR/Pages/images/profile.png"),size=(33, 33))
        reportsIcon = ctk.CTkImage(light_image=Image.open("src/AlertaBR/Pages/images/reports.png"),size=(33, 33))

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
        # Layout do menu
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
            text=f"{datetime.now().strftime('%d/%m/%y - %H:%M')}",
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

        # Layout do clima
        self.rainTotal.grid(row=1, column=1, padx=0, pady=0, sticky='w')
        self.rainStatus.grid(row=2, column=0)
        self.data.grid(row=0, column=1, padx=0, pady=0, sticky='n')
        self.humid.grid(row=1, column=2)
        self.rainInMM.grid(row=2, column=2)
        self.floodtitle.grid(row=3, column=2)
        
        

        # Criando TopLevel das infos de enchentes
        self.floodPopup = ctk.CTkScrollableFrame(self, width=350, height=350, corner_radius=20, fg_color="white")
        
        self.exitIcon = ctk.CTkImage(light_image=Image.open('src/AlertaBR/Pages/images/Exit.png'))
        self.exitButton = ctk.CTkButton(self.floodPopup, width=20, height=20, fg_color='transparent', image=self.exitIcon, text='', command=self.exitPopUp)
        self.exitButton.pack(anchor='e')
        

    def setOnMapRegion(self):
        address = self.searchEntry.get()
        if verif.checkAddresIsValid(address):
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
        self.showRainOrShowerValue(currWeather['rain'], currWeather['showers'])
        self.inputFloodStatusLabel(flood['river_discharge'][0], currWeather['rain'], currWeather['showers'])

    def inputRainStatusLabel(self, precip, wcode):
        self.weatherImage = ctk.CTkImage(size=(40, 40), light_image=Image.open("src/AlertaBR/Pages/images/WeathterisNormal.png"))

        if wcode in self.criticalCodes or precip >= self.criticalpct:
            self.weatherImage.configure(light_image=Image.open("src/AlertaBR/Pages/images/WeatherisCritical.png"))
            self.rainStatus.configure(text_color="#f00d0d")
            self.rainTotal.configure(text_color="#f00d0d")
            self.rainStatus.configure(text="Chuva Forte")
        elif wcode in self.alertCodes or precip >= self.alertpct:
            self.weatherImage.configure(light_image=Image.open("src/AlertaBR/Pages/images/WeatherisAlert.png"))
            self.rainStatus.configure(text_color="#f0aa0d")
            self.rainTotal.configure(text_color="#f0aa0d")
            self.rainStatus.configure(text="Chuva Moderada")
        elif wcode in self.okCodes or precip >= self.noRainpct:
            self.weatherImage.configure(light_image=Image.open("src/AlertaBR/Pages/images/WeatherisOk.png"))
            self.rainStatus.configure(text_color="#14AE5C")
            self.rainTotal.configure(text_color="#14AE5C")
            self.rainStatus.configure(text="Chuva Fraca")
        else:
            self.rainStatus.configure(text_color="#006CD2")
            self.rainTotal.configure(text_color="#006CD2")
            self.rainStatus.configure(text="Sem Chuva")

        self.weatherImgLabel = ctk.CTkLabel(self.weatherFrame, image=self.weatherImage, text='', bg_color='white')
        pywinstyles.set_opacity(self.weatherImgLabel, color="white")
        self.weatherImgLabel.grid(row=1, column=0, padx=0, pady=0, sticky='nsew')
    
    def inputFloodStatusLabel(self, river, rain, shower, icon = None):
        state = 0
        riskPrecip = (
            2 if rain > self.rainCritic else
            1 if rain >= self.rainAlert else
            0
        )

        riskShower = (
            2 if shower > self.showerCritic else
            1 if shower >= self.showerAlert else
            0
        )

        riskRiver = (
            2 if river > self.floodCritic else
            1 if river >= self.floodAlert else
            0
        )
        
        riskAvg = (riskShower + riskPrecip + riskRiver) / 3
        
        if riskAvg < 1:
            flood = "Sem Enchente"
            state = 0
        elif riskAvg < 2:
            flood = "Possível Enchente"
            state = 1
        else:
            flood = "Terá Enchente"
            state = 2
        
        self.floodtitle.configure(text=flood)
        if icon == None:
            return
        
        color = ''
        match(state):
            case 0:
                icon.configure(light_image=Image.open("src/AlertaBR/Pages/images/FloodisOk.png"))
                color = '#14AE5C'
            case 1:
                icon.configure(light_image=Image.open("src/AlertaBR/Pages/images/FloodisAlert.png"))
                color = '#F0AA0D'
            case 2:
                icon.configure(light_image=Image.open("src/AlertaBR/Pages/images/FloodisCritical.png"))
                color = '#F00D0D'
                
        self.setFloodStatus(flood, color)
    
    
    def showRainOrShowerValue(self, rain, shower):
        if shower > 0:
            self.rainInMM.configure(text=f"{shower:.1f} mm")
            return
        self.rainInMM.configure(text=f"{rain:.1f} mm")

    def creatingMapView(self):
        mapView = TkinterMapView(self, width=self.width, height=self.height)
        mapView.place(x=0, y=0, relwidth=1, relheight=1)  # Ocupa tudo
        mapView.set_tile_server(
            "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22
        )  # Define o Mapa exibido como no Google Maps
        mapView.set_position(self.defaultLat, self.defaultLng)

        # Desabilitando botões de zoom superior
        mapView.canvas.itemconfig(
            mapView.button_zoom_in.canvas_rect, state="hidden"
        )
        mapView.canvas.itemconfig(
            mapView.button_zoom_in.canvas_text, state="hidden"
        )
        mapView.canvas.itemconfig(
            mapView.button_zoom_out.canvas_rect, state="hidden"
        )
        mapView.canvas.itemconfig(
            mapView.button_zoom_out.canvas_text, state="hidden"
        )
        return mapView

    def createFloodButton(self):
        iconFlood = ctk.CTkImage(light_image=Image.open('src/AlertaBR/Pages/images/Flood.png'), size=(54, 54))
        btnFlood = ctk.CTkButton(self, width=54, height=54, corner_radius=5, fg_color="transparent", image=iconFlood, hover='lightgray', text='', bg_color="#000001", command=self.seeFloodForecast, hover_color='#81A8CD')
        pywinstyles.set_opacity(btnFlood, color="#000001")
        btnFlood.place(relx=0.9, rely=0.75, anchor='center')
        return btnFlood
    
    def seeFloodForecast(self):
        if (len(self.gmapWidget.canvas_marker_list) == 0):
            return
        
        coords = self.gmapWidget.get_position()
        
        enviroment = enviromentInfos(coords[0], coords[1])
        # criar alternativa de rain e shower para 7 dias em climatic.py
        flood = enviroment.createFloodData()
        week = 7
        
        if len(self.floodPopup.children) > 0:
            self.deleteAllContent(self.floodPopup)
        for i in range(week):
            date = flood['date'][i]
            river = flood['river_discharge'][i]
            self.createFloodStatusFrame(date, river, 10, 5)
        self.floodPopup.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)  
    
    def setFloodStatus(self, floodText, color):
        self.floodtext = floodText
        self.color = color
    
    
    def createFloodStatusFrame(self, date, river, rain, shower):
        floodFontTitle = ctk.CTkFont(family="Arial", weight="bold", size=18)
        floodFontText = ctk.CTkFont(family="Arial", weight="normal", size=16, slant='italic')
        
        frame = ctk.CTkFrame(self.floodPopup, width=300, height=96, fg_color='transparent')
        frame.grid_rowconfigure((0, 1, 2), weight=1)
        frame.grid_columnconfigure((0, 1), weight=1)
        
        lblDate = ctk.CTkLabel(frame, font=self.fontText, text=date, compound='left')
        lblFloodState = ctk.CTkLabel(frame, font=floodFontTitle)
        lblRainSum = ctk.CTkLabel(frame, font=floodFontText)
        
        
        # Icone
        icon = ctk.CTkImage(size=(37, 42), light_image=Image.open("src/AlertaBR/Pages/images/FloodisOk.png"))
        
        # Chamando função que define o status da enchente
        self.inputFloodStatusLabel(river, rain, shower, icon)
        lblFloodState.configure(text_color=self.color)
        lblFloodState.configure(text=self.floodtext)
        lblRainSum.configure(text_color=self.color)
        if shower > 1:
            rainTxt = f'Chuva: {shower:.1f} mm'
        else:
            rainTxt = f'Chuva: {shower:.1f} mm'
        lblRainSum.configure(text=rainTxt)
        
        lblIcon = ctk.CTkLabel(master=frame, text="", image=icon)
        
        # Montando Layout
        lblDate.grid(row=0, column=0)
        lblIcon.grid(row=1, column=0)
        lblFloodState.grid(row=1, column=1, pady=0, sticky='nsew')
        lblRainSum.grid(row=2, column=1)
        
        frame.pack(anchor='w')
        
    def exitPopUp(self):
        self.floodPopup.place_forget()
        
    def deleteAllContent(self, frame: ctk.CTkFrame):
        i = len(frame.winfo_children())
        childs = frame.winfo_children()
        
        # Deixa de remover 1 child, que é justamente o botão de sair do popup
        while i > 1:
            child = childs[i-1]
            child.destroy()
            i -= 1
            