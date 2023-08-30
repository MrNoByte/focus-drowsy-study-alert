import tkinter as tk


win = tk.Tk()
showMeme = tk.BooleanVar(value=True)
playSound = tk.BooleanVar(value= True)
alertVolume = tk.IntVar(value=5)

win.title("Settings")
win.geometry("250x250")
tk.Label(win, text="Settings",justify="center").grid(row=0)
tk.Label(win, padx=10).grid(row=1, column=0)
tk.Checkbutton(win,text="Show Meme",variable=showMeme).grid(row=2,column=0)
tk.Checkbutton(win,text="Play Sound",variable=playSound).grid(row=3,column=0)

tk.Label(win, text="Volume: ").grid(row=4,column=0)
tk.Scale(win, from_=0,to=5, variable=alertVolume, orient=tk.HORIZONTAL).grid(row=4, column=1)
print(showMeme.get())

win.mainloop()
