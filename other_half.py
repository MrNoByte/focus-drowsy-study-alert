import requests 
import json
import tkinter as tk
from urllib.request import urlopen
from PIL import ImageTk, Image
from io import BytesIO
from pygame import mixer
 
# for playing mp3 file
alertAudioPath = "assets/music/beep.mp3"
mixer.init()
mixer.music.load(alertAudioPath)



WIDTH = 600
QUALITY = 2
url = "https://meme-api.com/gimme"
res = requests.get(url)
js = json.loads(res.content.decode())

root = tk.Tk()

mixer.music.play()

# loading image from url in byte format
print(len(js['preview']))
# imgUrl = js['preview'][QUALITY] if QUALITY < len(js['preview']) else js['url']
imgUrl = js['preview'][QUALITY % len(js['preview'])]
img_data = requests.get(imgUrl).content

# showing image in tkinter
imgT = Image.open(BytesIO(img_data))
w, h = imgT.width, imgT.height

img = ImageTk.PhotoImage(imgT.resize((WIDTH, int(WIDTH // (w/h)))))
tk.Label(root, image=img).pack()
tk.Button(root, text= "I woke up!",command=root.quit).pack(pady=10)

root.mainloop()