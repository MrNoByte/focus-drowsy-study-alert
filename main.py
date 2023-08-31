
# importing files
import cv2
from ultralytics import YOLO
from pygame import mixer
import requests
import tkinter as tk
import json
from PIL import Image, ImageTk
from io import BytesIO

# constants
WIDTH_MEME = 600
WIDTH_SCR, HEIGHT_SCR = (600, 520)
MODEL_PATH = 'model/model-1.pt'
ALERT_AUDIO_PATH = "assets/music/beep.mp3"
MEME_URL = "https://meme-api.com/gimme"
MEME_QUALITY = 2

# tkinter window
root = tk.Tk()
root.title("Focus-Drowsy-Study")
root.geometry(f"{WIDTH_SCR}x{HEIGHT_SCR}")


# variables
showMeme = tk.BooleanVar(value=True)
playSound = tk.BooleanVar(value= True)
alertVolume = tk.IntVar(value=5)
isDrowsy = False


# loading audio
alertAudioPath = "assets/music/beep.mp3"
mixer.init()
mixer.music.load(alertAudioPath)


# loading yolo model
modelPath = 'model/model-1.pt'
model = YOLO(modelPath)

def requestingMeme(quality = 2):
    res = requests.get(MEME_URL)
    js = json.loads(res.content.decode())

    # getting max quality if length exceeds
    # return js['preview'][QUALITY] if QUALITY < len(js['preview']) else js['url']
    
    # for getting low quality 
    return js['preview'][quality % len(js['preview'])]

# Open the video file
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT_SCR)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH_SCR)


imgLbl = tk.Label(root)
imgLbl.pack()

def wakeup(app:tk.Toplevel):
    global isDrowsy, drowsyThread
    app.destroy()
    isDrowsy = False
    mixer.music.stop()

def drowsyAlert():
    global isDrowsy, winImg
    
    if isDrowsy:
        return
    
    isDrowsy = True
    win = tk.Toplevel(root)
    # root.eval(f'tk::PlaceWindow {str(win)} center')
    win.protocol('WM_DELETE_WINDOW', lambda: wakeup(win))
    
    if showMeme.get():
        # load meme
        img_data = requests.get(requestingMeme(MEME_QUALITY)).content
        
        # processing image for tkinter
        imgT = Image.open(BytesIO(img_data))
        w, h = imgT.width, imgT.height
        winImg = ImageTk.PhotoImage(imgT.resize((WIDTH_MEME, int(WIDTH_MEME // (w/h)))))

        # showing image
        tk.Label(win, image=winImg).pack()

    if playSound.get():
        mixer.music.set_volume(alertVolume.get() / 5)
        mixer.music.play(-1)

    tk.Button(win, text= "I woke up!",command=lambda: wakeup(win)).pack(pady=10)

def cameraOp():
    global imgLbl, imgTk
    _, frame = cap.read()
    
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = cv2.flip(img,1)
    results = model(img,verbose=False, stream=True, conf= 0.85)

    # Visualize the results on the frame
    # print(results[0].boxes.cls)
    for r in results:
        print(r.boxes.cls, r.boxes.conf)
        for cl in r.boxes.cls:
            if cl == 1:
                if not isDrowsy:
                    drowsyAlert()

        # getting prediction boxes
        annotated_frame = r.plot()

    # annotated_frame = results[0].plot()

    # showing img on tkinter
    imgT = Image.fromarray(annotated_frame)
    imgTk = ImageTk.PhotoImage(imgT)
    imgLbl.configure(image=imgTk)

    # repeat 10 ms
    imgLbl.after(10,cameraOp)

def settingsWin():
    global showMeme, playSound, alertVolume
    win = tk.Toplevel()

    win.title("Settings")
    win.geometry("250x250")
    tk.Label(win, text="Settings",justify="center").grid(row=0)
    tk.Label(win, padx=10).grid(row=1, column=0)
    tk.Checkbutton(win,text="Show Meme",variable=showMeme).grid(row=2,column=0)
    tk.Checkbutton(win,text="Play Sound",variable=playSound).grid(row=3,column=0)

    tk.Label(win, text="Volume: ").grid(row=4,column=0)
    tk.Scale(win, from_=0,to=5, variable=alertVolume, orient=tk.HORIZONTAL).grid(row=4, column=1)


tk.Button(root,text="Settings",command=settingsWin).pack()

cameraOp()
root.mainloop()
cap.release()
