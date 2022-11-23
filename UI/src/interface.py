import tkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from functools import partial
import os 
import shutil
import sys

# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(os.getcwd())
print(os.getcwd())
sys.path.insert(0, os.getcwd()) 

import api  
from ObjectDetection import predict

FIT_WIDTH = "fit_width"
FIT_HEIGHT = "fit_height"

class ScrollableFrame(tk.Frame):
    def __init__(self, master=None, scroll_speed=2,  hscroll=False, vscroll=True, **kwargs):
        assert isinstance(scroll_speed, int), "`scroll_speed` must be an int"
        self.scroll_speed = scroll_speed

        self.master_frame = tk.Frame(master)
        self.dummy_canvas = tk.Canvas(self.master_frame, **kwargs)
        super().__init__(self.dummy_canvas)

        # Create the 2 scrollbars
        if vscroll:
            self.v_scrollbar = tk.Scrollbar(self.master_frame,orient="vertical", command=self.dummy_canvas.yview)
            self.v_scrollbar.pack(side="right", fill="y")
            self.dummy_canvas.configure(yscrollcommand=self.v_scrollbar.set)
        if hscroll:
            self.h_scrollbar = tk.Scrollbar(self.master_frame,orient="horizontal", command=self.dummy_canvas.xview)
            self.h_scrollbar.pack(side="bottom", fill="x")
            self.dummy_canvas.configure(xscrollcommand=self.h_scrollbar.set)

        # Bind to the mousewheel scrolling
        self.dummy_canvas.bind_all("<MouseWheel>", self.scrolling_windows,add=True)
        self.dummy_canvas.bind_all("<Button-4>", self.scrolling_linux, add=True)
        self.dummy_canvas.bind_all("<Button-5>", self.scrolling_linux, add=True)
        self.bind("<Configure>", self.scrollbar_scrolling, add=True)

        # Place `self` inside `dummy_canvas`
        self.dummy_canvas.create_window((0, 0), window=self, anchor="nw")
        # Place `dummy_canvas` inside `master_frame`
        self.dummy_canvas.pack(side="top", expand=True, fill="both")

        self.pack = self.master_frame.pack
        self.grid = self.master_frame.grid
        self.place = self.master_frame.place
        self.pack_forget = self.master_frame.pack_forget
        self.grid_forget = self.master_frame.grid_forget
        self.place_forget = self.master_frame.place_forget

    
    def scrolling_windows(self, event):
        assert event.delta != 0, "On Windows, `event.delta` should never be 0"
        y_steps = int(-event.delta / abs(event.delta) * self.scroll_speed)
        self.dummy_canvas.yview_scroll(y_steps, "units")

    
    def scrolling_linux(self, event):
        y_steps = self.scroll_speed
        if event.num == 4: y_steps *= -1
        self.dummy_canvas.yview_scroll(y_steps, "units")

    
    def scrollbar_scrolling(self, event):
        region = list(self.dummy_canvas.bbox("all"))
        region[2] = max(self.dummy_canvas.winfo_width(), region[2])
        region[3] = max(self.dummy_canvas.winfo_height(), region[3])
        self.dummy_canvas.configure(scrollregion=region)

    
    def resize(self, fit=None, height=None, width=None):
        if fit == FIT_WIDTH:
            super().update()
            self.dummy_canvas.config(width=super().winfo_width())
        if fit == FIT_HEIGHT:
            super().update()
            self.dummy_canvas.config(height=super().winfo_height())
        if height is not None:
            self.dummy_canvas.config(height=height)
        if width is not None:
            self.dummy_canvas.config(width=width)
    fit = resize


class GUI:
    def __init__(self):
        self.homePageWindow()

    
    def homePageWindow(self):
        """
        This function will display the home window 
        """
        self.homeWindow = Tk()
        self.homeWindow.geometry("1100x700")
        self.homeWindow.resizable(False, False)
        self.homeWindow.title("Home Page")
        
        homeCanvas = Canvas(self.homeWindow)
        homeCanvas.pack(fill="both", expand=True)

        backgroundImage = PhotoImage(file="UI/GUI-images/homeBackground.png")
        homeCanvas.create_image(0, 0, image=backgroundImage, anchor="nw")
        
        homeCanvas.create_text(560, 300, text="Where Do You Want To Check?", font=("Inter", 40, "bold", "italic"), justify="center", fill="white")
        
        self.stringVar = StringVar()
        self.userInput = Entry(textvariable=self.stringVar, font=("Inter", 20), justify="center")
        self.userInput.insert(0, "Enter Zip Code")
        #self.userInput.bind("<FocusIn>", self.removeEnterAddress)
        homeCanvas.create_window(460, 400, anchor="nw", window=self.userInput, width=200)
        
        # range
        self.stringVar2 = StringVar()
        self.userInput2 = Entry(textvariable=self.stringVar2, font=("Inter", 20), justify="center")
        self.userInput2.insert(0, "Enter Range (default 500)")
        #self.userInput2.bind("<FocusIn>", self.removeEnterAddress)
        homeCanvas.create_window(460, 450, anchor="nw", window=self.userInput2, width=300)

        searchButton = Button(self.homeWindow, text="Search", command=self.getResults)
        self.homeWindow.bind("<Return>", self.getResults)
        homeCanvas.create_window(540, 510, anchor="nw", window=searchButton)

        self.homeWindow.mainloop()


    def getResults(self):
        """
        This function will get the results from user input and display a loading page
        """
        try:
            self.homeWindow.destroy()
        except:
            pass 

        localStrVar = self.stringVar.get()
        localStrVar2 = self.stringVar2.get()

        if localStrVar == "":
            tkinter.messagebox.showwarning(title="Zipcode cannot be empty", message="Zipcode cannot be empty")
            return
        
        #if localStrVar2 != "":
        #    if localStrVar2.isnumeric():
        #        api.set_range(localStrVar2)

    
        try:
            print(localStrVar2)
            api.set_range(localStrVar2)
            api.download_images(localStrVar)
        except: 
            pass

        # stored list of addresses & save images in UI/result-images
        listOfAddressesAsDictionaryKeyPair = predict.predict() # [{address : maxOverlap}]
        
        self.listOfAddresses = []
        for dictionary in listOfAddressesAsDictionaryKeyPair:
            for key in dictionary.keys():
                self.listOfAddresses.append(key.replace(" ", "_"))

        self.resultPageWindow()


    def resultPageWindow(self):   
        """
        This function will display the result window
        """ 
        try:
            self.homeWindow.destroy()
        except:
            pass 
        
        self.resultWindow = Tk()
        self.resultWindow.geometry("1100x700")
        self.resultWindow.resizable(False, False)
        self.resultWindow.title("List of All Addresses")

        resultFrame = ScrollableFrame(self.resultWindow, width=self.resultWindow.winfo_screenwidth(), height=self.resultWindow.winfo_screenheight(), vscroll=True)
        resultFrame.pack()
        
        homeButtonImage = PhotoImage(file="UI/GUI-images/homeButton.png", master=self.resultWindow)
        homeButtonImage = homeButtonImage.zoom(25)
        homeButtonImage = homeButtonImage.subsample(35)
        homeButton = Button(resultFrame, image=homeButtonImage, height=55, width=60, command=self.returnToHomePageWindow)
        homeButton.image = homeButtonImage
        homeButton.grid(column=0, row=0, sticky=W)

        title = ttk.Label(resultFrame, text="Addresses with the Most Concentrated Data Points", font=("Inter", 25, "bold", "italic"), justify="center")
        title.grid(column=1, row=0, padx=(80, 10))

        eyeButtonImage = PhotoImage(file="UI/GUI-images/eyeButton.png", master=self.resultWindow)
        
        r = 1
        for i in range(len(self.listOfAddresses)):
            index = Label(resultFrame, text=i+1, font=("Inter", 15), justify="center")
            index.grid(column=0, row=r)
            addressText = Label(resultFrame, text=self.listOfAddresses[i].replace("_", " "), font=("Inter", 15), justify="center")
            addressText.grid(column=1, row=r, sticky=W, ipady=30, padx=(120, 10))
            eyeButton1 = Button(resultFrame, image=eyeButtonImage, height=40, width=60, command=partial(self.imagePageWindow, self.listOfAddresses[i]))
            eyeButton1.image = eyeButtonImage
            eyeButton1.grid(column=1, row=r, sticky=E, padx=(10, 80))
            r += 1

        self.stringVar.set("Enter Zip Code")
        self.resultWindow.mainloop()
        


    def imagePageWindow(self, address):
        """
        This function will display the image window after a user clicks on the eye button on the result window 
        """
        self.resultWindow.destroy()

        self.imageWindow = Tk()
        self.imageWindow.geometry("1100x700")
        self.imageWindow.resizable(False, False)
        self.imageWindow.title("Image of Address")

        imageCanvas = Canvas(self.imageWindow)
        imageCanvas.pack(fill="both", expand=True)

        returnButtonImage = PhotoImage(file="UI/GUI-images/returnButton.png")
        returnButtonImage = returnButtonImage.zoom(25)
        returnButtonImage = returnButtonImage.subsample(35)
        returnButton = Button(self.imageWindow, image=returnButtonImage, height=55, width=60, command=self.returnToResultPageWindow)
        returnButton.image = returnButtonImage
        returnButton.pack()
        imageCanvas.create_window(0, 0, anchor="nw", window=returnButton)

        addressImage = PhotoImage(file="UI/result-images/" + address + ".png")
        addressImageLabel = Label(self.imageWindow, image = addressImage)
        imageCanvas.create_window(250, 0, anchor="nw", window=addressImageLabel)

        addresstText = Label(self.imageWindow, text=address, font=("Inter", 20, "bold"))
        addresstText.pack(side=BOTTOM)

        self.imageWindow.mainloop()
    

    def removeEnterAddress(self, event):
        """
        This function will remove the "Enter Address" when a user clicks on the Entry box on the home window 
        """
        self.userInput.delete(0, "end")

    

    def returnToHomePageWindow(self):
        """
        This function will return to the home window after a user clicks on the home button on the result window 
        """
        self.resultWindow.destroy()
        self.homePageWindow()
    

    def returnToResultPageWindow(self):
        """
        This function will return to the result window after a user clicks on the return button on the image window 
        """
        self.imageWindow.destroy()
        self.resultPageWindow()



if __name__ == "__main__":
    # makes a directory of images if the directory does not exist
    if not os.path.exists("results"): 
        os.mkdir('results')

    GUI()

    shutil.rmtree('results')
