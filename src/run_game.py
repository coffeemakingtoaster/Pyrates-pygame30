import tkinter
import os
import game_ui
from PIL import ImageTk,Image


class main_menu():

    def __init__(self):
        #close_img = Image.open(os.path.join(os.getcwd(),"data","img","x_button.png"))
        #close_img = close_img.resize((40,40),Image.ANTIALIAS)
        #close_img = ImageTk.PhotoImage(close_img)
        header = tkinter.Label(root, text="Pyrates")
        header.pack()
        self.start_game_button = tkinter.Button(root, text="New game", command=self.validate_new_game)
        self.load_game_button = tkinter.Button(root, text="Load game", command =self.load_game)
        if len(os.listdir(os.path.join(os.getcwd(), "data", "savegame"))) == 0:
            self.load_game_button["state"] = "disable"
        self.exit_button = tkinter.Button(root,text="exit", command=root.destroy)
        self.start_game_button.pack()
        self.load_game_button.pack()
        self.exit_button.pack()
        self.confirm_window = None



    def validate_new_game(self):
        if len(os.listdir(os.path.join(os.getcwd(),"data","savegame"))) != 0:
            print("directory not empty")
            self.confirm_window = tkinter.Toplevel()
            self.confirm_window.title("Warning")
            self.start_game_button["state"] = "disable"
            warning_label = tkinter.Label(self.confirm_window,text="Creating a new savegame will overwrite your existing saves!")
            confirm_button = tkinter.Button(self.confirm_window,text="Continue",command=self.start_new_game)
            cancel_button = tkinter.Button(self.confirm_window,text="Cancel",command = self.activate_mm)
            warning_label.pack()
            confirm_button.pack()
            cancel_button.pack()
        else:
            self.start_new_game()

    def activate_mm(self):
        self.start_game_button["state"] = "normal"
        self.confirm_window.destroy()
        self.confirm_window = None


    def start_new_game(self):
        if self.confirm_window:
            self.confirm_window.destroy()
            self.confirm_window = None
        for file in os.listdir(os.path.join(os.getcwd(),"data","savegame")):
            filepath = os.path.join(os.path.join(os.getcwd(),"data","savegame",file))
            os.unlink(filepath)
        root.withdraw()
        game_ui.main()
        root.deiconify()
        self.start_game_button["state"] = "normal"


    def load_game(self):
        root.withdraw()
        game_ui.main()
        root.deiconify()
        self.start_game_button["state"] = "normal"



if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("MainMenu")
    root.geometry("300x100")
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
    positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)
    root.geometry("+{}+{}".format(positionRight, positionDown))
    main_menu()
    root.mainloop()