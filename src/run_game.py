import tkinter
import os
import game_ui
import json
from PIL import ImageTk,Image


class main_menu():

    def __init__(self):
        #close_img = Image.open(os.path.join(os.getcwd(),"data","img","x_button.png"))
        #close_img = close_img.resize((40,40),Image.ANTIALIAS)
        #close_img = ImageTk.PhotoImage(close_img)
        self.Name_Label = tkinter.Label(root,text="Enter your username (Will be used for higscores):")
        self.Name_Label.pack()
        self.e1 = tkinter.Entry(root)
        self.e1.pack()
        OK_button = tkinter.Button(root,text="OK",command=lambda:self.init_main_menu(OK_button))
        OK_button.pack()
        self.confirm_window = None

    def init_main_menu(self,button_to_destroy):
        self.username = self.e1.get()
        self.e1.destroy()
        self.Name_Label.destroy()
        button_to_destroy.destroy()
        header = tkinter.Label(root, text="Pyrates")
        header.pack()
        self.start_game_button = tkinter.Button(root, text="New game", command=self.validate_new_game)
        self.load_game_button = tkinter.Button(root, text="Load game", command=self.load_game)
        if len(os.listdir(os.path.join(os.getcwd(), "data", "savegame"))) == 0:
            self.load_game_button["state"] = "disable"
        self.show_highscores_button = tkinter.Button(root,text="Show local highscores",command=self.display_highscores)
        self.exit_button = tkinter.Button(root, text="exit", command=root.destroy)
        self.start_game_button.pack()
        self.load_game_button.pack()
        self.show_highscores_button.pack()
        self.exit_button.pack()


    #TODO: Sort highscores correctly
    def display_highscores(self):
        f = open(os.path.join(os.getcwd(),"data","other","highscores.json"))
        data = json.load(f)
        f.close()
        scores=[]
        for item in data:
            print(item)
            placed = False
            print(len(scores))
            if scores == []:
                scores.append(item)
                continue
            index = 0
            for element in scores:
                if item["score"] >= element["score"]:
                    scores.insert(index, item)
                    if len(scores)>10:
                        del scores[-1]
                    print(scores)
                    placed = True
                    break
                index += 1
            if not placed:
                if len(scores) < 10:
                    scores.append(item)
        score_window = tkinter.Toplevel()
        score_window.geometry("200x275")
        highscores_head_label = tkinter.Label(score_window,text="You local highscores:")
        highscores_head_label.pack()
        cnt = 1
        for item in scores:
            tmp_lbl = tkinter.Label(score_window,text=str(cnt)+".   %s      %s Points!"%(item["username"],item["score"]))
            tmp_lbl.pack()
            cnt+=1
        close_highscores_button = tkinter.Button(score_window,text="Close",command=score_window.destroy)
        close_highscores_button.pack()


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
        for file in os.listdir(os.path.join(os.getcwd(),"data","img","crew_faces")):
            filepath = os.path.join(os.path.join(os.getcwd(), "data", "img","crew_faces", file))
            os.unlink(filepath)
        root.withdraw()
        game_ui.main(self.username)
        root.deiconify()
        self.start_game_button["state"] = "normal"


    def load_game(self):
        root.withdraw()
        game_ui.main(self.username)
        root.deiconify()
        self.start_game_button["state"] = "normal"



if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("MainMenu")
    root.geometry("300x150")
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
    positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)
    root.geometry("+{}+{}".format(positionRight, positionDown))
    main_menu()
    root.mainloop()