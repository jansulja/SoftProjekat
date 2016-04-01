from Tkinter import *
import main_frame

root = Tk()
#test

root.title("Music Sheet Reader")
root.geometry("800x50")
root.wm_attributes("-topmost", 1)
app = main_frame.Application(root)

root.mainloop()

