from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

import json
from openalpr import Alpr
import mysql.connector

# Make global variables to capture the values in the functions

global selector

def ImageFilePath():
    selector.filename = filedialog.askopenfilename(initialdir = "/Users/pamelaaudi/", title = " Select A File ", filetypes = (("jpg files", "*.jpg"),("all files", "*.*")))
    global filepath
    global LicensePlateNo
    filepath = selector.filename
    LicensePlateNo = RegExtract()
    my_image = ImageTk.PhotoImage(Image.open(filepath))
    my_image_label = Label(selector, height = 250, width = 400, image=my_image)
    my_image_label.img = my_image
    my_image_label.place(x = 20, y = 20)
   

def RegExtract():
    global c_plateArr
    global c_confidenceArr
    # set the language, path to configuration file and run time data for alpr object
    alpr = Alpr("us", "/etc/openalpr/openalpr.conf", "/usr/local/share/openalpr/runtime_data")
    
    # check if alpr service is active on the machine
    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)
    
    # Define the max number of results
    alpr.set_top_n(20)
    alpr.set_default_region("md")

    # Pass the image to perform OCR on and store the run time results in results
    results = alpr.recognize_file("%s" % filepath)
    
    # Extract relevant information from the results' data structure
    resultsArr = results['results']
    platesdict = resultsArr[0]
    RegNo = platesdict['plate']
    CandidatesArr = platesdict['candidates']
    
    # Obtain top 3 License plate candidates
    Candidatesdict1 = CandidatesArr[0]
    Candidatesdict2 = CandidatesArr[1]
    Candidatesdict3 = CandidatesArr[2]

    c_plateArr =[Candidatesdict1['plate'], Candidatesdict2['plate'], Candidatesdict3['plate']]
    c_confidenceArr =[Candidatesdict1['confidence'], Candidatesdict2['confidence'], Candidatesdict3['confidence']]
    
    alpr.unload()
    
    return RegNo

def DatabaseConnection():
    global myresulttup
    try:
        mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = "Val@123#", database = "ocr_project")
        mycursor = mydb.cursor()
        query = "SELECT FIRST_NAME, LAST_NAME, ADDRESS, CITY, STATE, ZIP_CODE, VEHICLE_BRAND, MODEL, COLOR, TYPE, LICENSE_ID, ISSUE_DATE, EXPIRATION_DATE FROM owner as o INNER JOIN vehicle as v ON o.OWNER_ID = v.OWNER_ID INNER JOIN license as l ON v.OWNER_ID = l.OWNER_ID WHERE LICENSE_ID = %s"
        mycursor.execute(query, (LicensePlateNo,))
        myresult = mycursor.fetchall()
        print(myresult)
        myresulttup = myresult[0]
        
    except mysql.connector.Error as error:
        print("Failed to get record from MySQL table: {}".format(error))

    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
    UIFillUp()
    
    #for x in myresult:
    #   print (x)


def UIFillUp():
    
    DBres1 = StringVar()
    DBres2 = StringVar()
    DBres3 = StringVar()
    DBres4 = StringVar()
    DBres5 = StringVar()
    DBres6 = StringVar()
    DBres7 = StringVar()
    DBres8 = StringVar()
    DBres9 = StringVar()
    DBres10 = StringVar()
    DBres11 = StringVar()
    DBres12 = StringVar()
    DBres13 = StringVar()
    # Fill up the information next to the labels
    NameLabel = Label(selector, textvariable = DBres1, fg = "Black").place(x = 140, y = 440)
    NameLabe2 = Label(selector, textvariable = DBres2, fg = "Black").place(x = 140, y = 480)
    AddressLabel = Label(selector, textvariable = DBres3, fg = "Black").place(x = 140, y = 520)
    CityLabel = Label(selector, textvariable = DBres4, fg = "Black").place(x = 140, y = 560)
    StateLabel = Label(selector, textvariable = DBres5, fg = "Black").place(x = 140, y = 600)
    ZipLabel = Label(selector, textvariable = DBres6, fg = "Black").place(x = 140, y = 640)
    VehicleBrand = Label(selector, textvariable = DBres7, fg = "Black").place(x = 550, y = 440)
    Model = Label(selector, textvariable = DBres8, fg = "Black").place(x = 550, y = 480)
    Color = Label(selector, textvariable = DBres9, fg = "Black").place(x = 550, y = 520)
    TypeOfCar = Label(selector, textvariable = DBres10, fg = "Black").place(x = 550, y = 560)
    LicenseID = Label(selector, textvariable = DBres11, fg = "Black").place(x = 550, y = 600)
    LicIssDate = Label(selector, textvariable = DBres12, fg = "Black").place(x = 550, y = 640)
    LicExpDate = Label(selector, textvariable = DBres13, fg = "Black").place(x = 550, y = 680)
    
    DBres1.set(myresulttup[0])
    DBres2.set(myresulttup[1])
    DBres3.set(myresulttup[2])
    DBres4.set(myresulttup[3])
    DBres5.set(myresulttup[4])
    DBres6.set(myresulttup[5])
    DBres7.set(myresulttup[6])
    DBres8.set(myresulttup[7])
    DBres9.set(myresulttup[8])
    DBres10.set(myresulttup[9])
    DBres11.set(myresulttup[10])
    DBres12.set(myresulttup[11])
    DBres13.set(myresulttup[12])
    
    # Percentage Accuracy of the OPEN ALPR model
    
    Title4 = Label(selector, text = " POSSIBLE LICENSE PLATES DETECTED BY PROGRAM ", fg = "Black").place(x = 700, y = 50)
    
    # Headings
    
    Title4 = Label(selector, text = " ID ", fg = "Black").place(x = 670, y = 80)
    Title4 = Label(selector, text = " PLATE NO# ", fg = "Black").place(x = 750, y = 80)
    Title4 = Label(selector, text = " % CONFIDENCE ", fg = "Black").place(x = 860, y = 80)
    
    # Results from the database passed into label to diplay on the UI
    Plate1 = Label(selector, text = "Plate 1 :", fg = "Black").place(x = 670, y = 120)
    Plate2 = Label(selector, text = "Plate 2 :", fg = "Black").place(x = 670, y = 160)
    Plate3 = Label(selector, text = "Plate 3 :", fg = "Black").place(x = 670, y = 200)
    
    LicensePlateNo1 = StringVar()
    LicensePlateNo2 = StringVar()
    LicensePlateNo3 = StringVar()
    
    RegNo1 = Label(selector, textvariable = LicensePlateNo1, fg = "Black").place(x = 750, y = 120)
    RegNo2 = Label(selector, textvariable = LicensePlateNo2, fg = "Black").place(x = 750, y = 160)
    RegNo3 = Label(selector, textvariable = LicensePlateNo3, fg = "Black").place(x = 750, y = 200)
    
    LicensePlateNo1.set(c_plateArr[0])
    LicensePlateNo2.set(c_plateArr[1])
    LicensePlateNo3.set(c_plateArr[2])
    
    confPerc1 = StringVar()
    confPerc2 = StringVar()
    confPerc3 = StringVar()
    
    Confidence1 = Label(selector, textvariable = confPerc1, fg = "Black").place(x = 860, y = 120)
    Confidence2 = Label(selector, textvariable = confPerc2, fg = "Black").place(x = 860, y = 160)
    Confidence3 = Label(selector, textvariable = confPerc3, fg = "Black").place(x = 860, y = 200)
    
    confPerc1.set(c_confidenceArr[0])
    confPerc2.set(c_confidenceArr[1])
    confPerc3.set(c_confidenceArr[2])

# THe main part of the program
selector = Tk()
selector.title ("LICENSE PLATE DETECTION PROGRAM")
frame = Frame(selector, height = 700, width = 1200).pack()
    
# Car Onwer Personal information
Title1 = Label(selector, text = " CAR OWNER INFORMATION SECTION ", fg = "Black").place(x = 30, y = 400)

NameLabel = Label(selector, text = "First Name :", fg = "Black").place(x = 10, y = 440)
NameLabe2 = Label(selector, text = "Last Name :", fg = "Black").place(x = 10, y = 480)
AddressLabel = Label(selector, text = "Address :", fg = "Black").place(x = 10, y = 520)
CityLabel = Label(selector, text = "City :", fg = "Black").place(x = 10, y = 560)
StateLabel = Label(selector, text = "State :", fg = "Black").place(x = 10, y = 600)
ZipLabel = Label(selector, text = "Zip Code :", fg = "Black").place(x = 10, y = 640)

# Car Information Widget Initial Load Up: Labels
Title2 = Label(selector, text = " CAR INFORMATION SECTION ", fg = "Black").place(x = 400, y = 400)

VehicleBrand = Label(selector, text = "Brand :", fg = "Black").place(x = 370, y = 440)
Model = Label(selector, text = "Model :", fg = "Black").place(x = 370, y = 480)
Color = Label(selector, text = "Color :", fg = "Black").place(x = 370, y = 520)
TypeOfCar = Label(selector, text = "Type of Car :", fg = "Black").place(x = 370, y = 560)
LicenseID = Label(selector, text = "License plate No. :", fg = "Black").place(x = 370, y = 600)
LicenseIssueDate = Label(selector, text = "License Issue Date :", fg = "Black").place(x = 370, y = 640)
LicenseExpirationDate = Label(selector, text = "License Expiration Date :", fg = "Black").place(x = 370, y = 680)
    
# Buttons
ImgUpload = Button(selector, text = " UPLOAD IMAGE ", fg = "Grey", command = ImageFilePath).place(x = 20, y = 350)
SearchDB = Button(selector, text = " SEARCH ", fg = "Grey", command = DatabaseConnection).place(x = 300, y = 350)

selector.mainloop()
