import tkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from functools import partial
from turtle import bgcolor


class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1100x700")
        self.window.resizable(False, False)
        self.window.title("Home")
        
        canvas1 = Canvas(self.window)
        canvas1.pack(fill="both", expand=True)

        backgroundImage = PhotoImage(file="UI/images/homeBackground.png")
        canvas1.create_image(0, 0, image=backgroundImage, anchor="nw")
        
        canvas1.create_text(560, 300, text="Where Do You Want To Check?", font=("Inter", 40, "bold", "italic"), justify="center", fill="white")
        
        self.stringVar = StringVar()
        self.userInput = Entry(textvariable=self.stringVar, font=("Inter", 20), justify="center")
        self.userInput.insert(0, "Enter Zip Code")
        self.userInput.bind("<FocusIn>", self.removeEnterAddress)
        canvas1.create_window(460, 400, anchor="nw", window=self.userInput, width=200)
        
        searchButton = Button(self.window, text="Search", command=partial(self.functionToDisplayText, ""))
        self.window.bind("<Return>", self.functionToDisplayText)
        canvas1.create_window(540, 440, anchor="nw", window=searchButton)

        self.window.mainloop()


    def functionToDisplayText(self, event):
        """
        This function will display the output 
        """
        localStrVar = self.stringVar.get()

        if localStrVar == "":
            tkinter.messagebox.showwarning(title="Zipcode cannot be empty", message="Zipcode cannot be empty")
            return 

        resultWindow = Toplevel()
        resultWindow.geometry("1100x700")
        resultWindow.resizable(False, False)
        resultWindow.title("Top Three Addresses")

        canvas1 = Canvas(resultWindow)
        canvas1.pack(fill="both", expand=True)

        # backgroundImage = PhotoImage(file="UI/images/greyBackground.png")
        # canvas1.create_image(0, 0, image=backgroundImage, anchor="nw")

        title = ttk.Label(resultWindow, text="Top Three Addresses with the Most Concentrated Data Points", font=("Inter", 25, "bold", "italic"), justify="center")
        canvas1.create_window(70, 50, anchor="nw", window=title)
            
        eyeButtonImage = PhotoImage(file="UI/images/eyeButton.png")
        
        canvas1.create_text(200, 200, text=localStrVar, anchor="nw", font=("Inter", 15), justify="center")
        eyeButton1 = Button(resultWindow, image=eyeButtonImage, height=40, width=60)
        eyeButton1.image = eyeButtonImage
        canvas1.create_window(700, 190, anchor="nw", window=eyeButton1)

        canvas1.create_text(200, 350, text=localStrVar, anchor="nw", font=("Inter", 15), justify="center")
        eyeButton2 = Button(resultWindow, image=eyeButtonImage, height=40, width=60)
        eyeButton2.image = eyeButtonImage
        canvas1.create_window(700, 340, anchor="nw", window=eyeButton2)

        canvas1.create_text(200, 500, text=localStrVar, anchor="nw", font=("Inter", 15), justify="center")
        eyeButton3 = Button(resultWindow, image=eyeButtonImage, height=40, width=60)
        eyeButton3.image = eyeButtonImage
        canvas1.create_window(700, 490, anchor="nw", window=eyeButton3)

        self.stringVar.set("Enter Zip Code")
    

    def removeEnterAddress(self, event):
        """
        This function will remove the "Enter Address" when a user clicks on the Entry box 
        """
        self.userInput.delete(0, "end")


if __name__ == "__main__":
    GUI()
