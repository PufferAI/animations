import raylib as rl
from cffi import FFI
import imageio
import numpy as np

rl.InitWindow(1920, 1080, "Animation".encode())
rl.SetTargetFPS(60)



PUFF_BG = [6, 24, 24, 255]
PUFF_WHITE = [241, 241, 241, 255]
PUFF_RED = [187, 0, 0, 255]
PUFF_CYAN = [0, 187, 187, 255]
PUFF_BLUE = [0, 0, 187, 255]

def cdata_to_numpy():
    image = rl.LoadImageFromScreen()
    data_pointer = image.data
    width = image.width
    height = image.height
    channels = 4
    data_size = width * height * channels
    cdata = FFI().buffer(data_pointer, data_size)
    return np.frombuffer(cdata, dtype=np.uint8
        ).reshape((height, width, channels))

i = 0
frames = []

def quad(t, y0):
    return y0 + (540 - 100 - y0) * (1 - (1 - t / 60) ** 2)

font = rl.GetFontDefault()
while not rl.WindowShouldClose():
    rl.BeginDrawing()
    rl.ClearBackground(PUFF_BG)


    if i < 60:
        text_x = 1920 - 21*i
        text_y = quad(i, 0) + 100
        text = '1.0'.encode()
        rot = 0
    elif i > 150 and i < 180:
        text_x = 1920 - 21*60 + 21*(i-150)
        text_y = 540 - 100
        text = '2.0'.encode()
        rot = (i - 150) / 30 * 360
    elif i > 180:
        text_x = 1320
        text_y = 540 - 100
        text = '2.0'.encode()
        rot = 0

    text_x = int(text_x)
    text_y = int(text_y)
    rl.DrawTextPro(font, text, (text_x, text_y), (0, 0), rot, 200, 8, PUFF_CYAN)
    rl.EndDrawing()

    i += 1

    frames.append(cdata_to_numpy())

    if i == 230:
        break

rl.CloseWindow()

imageio.mimsave('intro.gif', frames, fps=60, loop=0)
