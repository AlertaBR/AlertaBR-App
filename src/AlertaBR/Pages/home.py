import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue") 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AlertaBR")
        self.geometry("390x844")
        self.resizable(0, 0)
        self.wm_iconbitmap(default="./images/favicon.ico")
        self.eval("tk::PlaceWindow . center")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        
            
        frame = ctk.CTkFrame(master=self, width=390, height=844)
        frame.pack(fill="both", expand=True)


        searchBar = ctk.CTkEntry(frame, width=350, height=50, corner_radius=30, placeholder_text="Pesquise Aqui", placeholder_text_color="gray")
        searchBar.pack(pady=80)
        searchBar.focus()


app = App()
app.mainloop()
