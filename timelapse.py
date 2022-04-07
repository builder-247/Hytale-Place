import pandas as pd
import tkinter
import time
from ast import literal_eval

df = pd.read_csv('./data/filtered.csv')

original_height = 32
original_width = 39

x_offset = 323
y_offset = 614

scale = 20

# width of the animation window
animation_window_width = scale * original_width
# height of the animation window
animation_window_height = scale * original_height



# The main window of the animation
def create_animation_window():
  window = tkinter.Tk()
  window.title("Tkinter Animation Demo")
  # Uses python 3.6+ string interpolation
  window.geometry(f'{animation_window_width}x{animation_window_height}')
  return window


# Create a canvas for animation and add it to main window
def create_animation_canvas(window):
  canvas = tkinter.Canvas(window)
  canvas.configure(bg="white")
  canvas.pack(fill="both", expand=True)
  return canvas


def animate_timelapse(window, canvas):
    for idx, row in df.iterrows():
        _, timestamp, user, color, coords = row
        x, y = literal_eval(coords)
        x =  (x - x_offset) * scale
        y = (y - y_offset) * scale
        #print(timestamp, color, x, y)
        canvas.create_rectangle(x, y, x+scale, y+scale, fill=color, outline='')
        window.update()
        time.sleep(0.01)
    return 0

# The actual execution starts here
animation_window = create_animation_window()
animation_canvas = create_animation_canvas(animation_window)
animation_window.update()
# Initialize window so we screenrecord
time.sleep(10)
animate_timelapse(animation_window, animation_canvas)