import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue") 

root = ctk.CTk()
root.title("AlertaBR")
root.iconbitmap("./images/favicon.ico")
root.geometry("390x844")


frame = ctk.CTkFrame(master=root, width=390, height=844)
frame.pack(fill="both", expand=True)

searchBar = ctk.CTkEntry(frame, width=350, height=55, corner_radius=30, placeholder_text="Pesquise Aqui", placeholder_text_color="gray")
searchBar.pack(pady=40)
searchBar.focus()

root.mainloop()
