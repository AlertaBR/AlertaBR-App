import customtkinter as ctk
from tkintermapview import TkinterMapView
from CTkMessagebox import CTkMessagebox
from PIL import Image
from src.AlertaBR.logic.maps import getStreetResponse

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

fontfamily = "Poppins"


class App(ctk.CTk):
  defaultLat = -23.5831527
  defaultLng = -46.6568236
  width = 390
  height = 844
  
  def __init__(self):
      super().__init__()

      self.title("AlertaBR")
      self.geometry(f"{self.width}x{self.height}")
      self.resizable(0, 0)
      # self.wm_iconbitmap(default="./images/favicon.ico")
      self.eval("tk::PlaceWindow . center")
      self.grid_columnconfigure(0, weight=2)

      
      # Criando Mapa
      self.gmapWidget = TkinterMapView(self, width=390, height=844)
      self.gmapWidget.place(x=0, y=0, relwidth=1, relheight=1)  # Ocupa tudo
      self.gmapWidget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # Define o Mapa exibido como no Google Maps
      self.gmapWidget.set_position(self.defaultLat, self.defaultLng)
      
      # Desabilitando botões de zoom superior
      self.gmapWidget.canvas.itemconfig(self.gmapWidget.button_zoom_in.canvas_rect, state='hidden') 
      self.gmapWidget.canvas.itemconfig(self.gmapWidget.button_zoom_in.canvas_text, state='hidden') 
      self.gmapWidget.canvas.itemconfig(self.gmapWidget.button_zoom_out.canvas_rect, state='hidden') 
      self.gmapWidget.canvas.itemconfig(self.gmapWidget.button_zoom_out.canvas_text, state='hidden')

      # Criando barra de pesquisa por região
      self.searchEntry = ctk.CTkEntry(
          self,
          width=350,
          height=50,
          corner_radius=10,
          placeholder_text="Pesquise Aqui",
          placeholder_text_color="gray",
          font=(fontfamily, 20),
          fg_color="transparent"
      )
      self.searchEntry.focus()
      self.searchEntry.grid(row=0, column=0, padx=10, pady=80)
      
      # Criando botão
      searchIcon = ctk.CTkImage(light_image=Image.open("src/AlertaBR/Pages/images/search.png"), size=(20, 20))
      self.searchButton = ctk.CTkButton(self, width=40, height=40, corner_radius=5, image=searchIcon, text='', command=self.setOnMapRegion, fg_color="#00285C", hover_color="#004FB6")
   #   self.searchButton.place(relx=0.5, rely=0.08, anchor="nw")
      self.searchButton.grid(row=0, column=1, padx=10, pady=80)
      
      self.searchEntry.bind("<Return>", self.setOnMapRegion)
      
  def setOnMapRegion(self):
    self.gmapWidget.delete_all_marker()
    address = self.searchEntry.get()
    if len(address) < 8 or not address:
      CTkMessagebox(title="Endereço Inválido", message="O endereço digitado não é válido.", icon="cancel", option_1="Ok")
      self.searchEntry.delete(0, len(address))
      return
    
    coord = getStreetResponse(address)
    lat = float(coord['lat'])
    lon = float(coord['lon'])
    
    self.gmapWidget.set_position(lat, lon)
    self.gmapWidget.set_marker(lat, lon, text=coord['name'])
    self.searchEntry.delete(0, len(address))
