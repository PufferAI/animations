import raylib as rl
from cffi import FFI
import imageio

rl.InitWindow(1920, 1080, "Animation".encode())
rl.SetTargetFPS(60)


puf_1 = {
    'Python': 8839,
    'Cython': 83,
    '       C': 0,
}

puf_2 = {
    'Python': 8472,
    'Cython': 2079,
    '       C': 19579,
}


PUFF_BG = [6, 24, 24, 255]
PUFF_WHITE = [241, 241, 241, 255]
PUFF_RED = [187, 0, 0, 255]
PUFF_CYAN = [0, 187, 187, 255]
PUFF_BLUE = [0, 0, 187, 255]

colors = [PUFF_RED, PUFF_BLUE, PUFF_CYAN]

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

def draw_chart(data, x, y):
    total_lines = sum(data.values())
    start_angle = 0
    for i, (lang, lines) in enumerate(data.items()):
        color = colors[i]
        end_angle = start_angle + 360*lines/total_lines
        rl.DrawCircleSector([x, y], total_lines**0.5, start_angle, end_angle, 128, color)
        start_angle = end_angle

        rl.DrawText(lang.encode(), 100, 100 + 100*i, 20, rl.WHITE)
        rl.DrawRectangle(200, 100 + 100*i, 100, 100, color)

def draw_bars(data):
    total_lines = sum(data.values())
    for i, (lang, lines) in enumerate(data.items()):
        color = colors[i]
        box_len = int(lines/15)
        lines = int(lines)
        rl.DrawText(lang.encode(), 100, 730 + 100*i, 40, PUFF_WHITE)
        rl.DrawRectangle(300, 700 + 100*i, box_len, 100, color)
        rl.DrawText(str(lines).encode(), 350 + box_len, 735 + 100*i, 30, PUFF_WHITE)

def load_stars():
    from datetime import datetime
    import csv
    f = open('stars.csv')
    data = csv.reader(f)
    timestamps = []
    stars = []
    for _, date_str, star in data:
        date_str = ' '.join(date_str.split()[:5])
        ts = int(datetime.strptime(date_str, "%a %b %d %Y %H:%M:%S").timestamp())
        timestamps.append(ts)
        stars.append(int(star))

    timestamps = [(e-timestamps[1])/1e4 for e in timestamps]
    timestamps = timestamps[1:]
    stars = stars[1:]

    return timestamps, stars


LERPS = 60
i = 0

timestamps, stars = load_stars()
import numpy as np
stars_interp = np.interp(np.linspace(0, max(timestamps), 60), timestamps, stars)

puffer = rl.LoadTexture('puffers_128.png'.encode())
star_tex = rl.LoadTexture('star.png'.encode())
frames = []
while not rl.WindowShouldClose():
    rl.BeginDrawing()
    rl.ClearBackground(PUFF_BG)

    if i < 80:
        draw_bars(puf_1)
        #draw_chart(puf_1, 960, 540)
    elif i < 80 + LERPS:
        l = i - 80
        data = {}
        for k in puf_1:
            d1 = puf_1[k]
            d2 = puf_2[k]
            data[k] = d1*(LERPS-l)/LERPS + d2*l/LERPS

        draw_bars(data)
        #draw_chart(data, 960, 540)
    else:
        draw_bars(puf_2)
        #draw_chart(puf_2, 960, 540)

    i_min = max(0, min(i-80, 59))
    puffer_x = 100 + i_min/60*max(timestamps) - 64
    puffer_y = 650 - stars_interp[i_min]/4.0 - 64

    for t in range(len(timestamps)):
        ts = timestamps[t]
        star = stars[t]

        xx = int(100 + ts)
        if (xx > puffer_x + 64):
            break

        yy = int(650 - star/4.0)
        rl.DrawTextureRec(star_tex, [384, 384, 128, 128], [xx-64, yy-64], rl.WHITE)

    rl.DrawTextureRec(puffer, [0, 0, 128, 128], [puffer_x, puffer_y], rl.WHITE)
    rl.DrawText(str(int(stars_interp[i_min])).encode(), int(puffer_x) + 48 , int(puffer_y) + 128, 30, PUFF_WHITE)

    color = rl.Fade(PUFF_CYAN, i/30)

    txt = ''
    if i >= 60:
        txt = '2.0'
    elif i >= 40:
        txt = '2.'
    elif i >= 20:
        txt = '2'

    rl.DrawText(txt.encode(), 100, 50, 240, PUFF_CYAN)


    #if i >= 90:

    #color = rl.Fade(rl.WHITE, (i-90)/30)
    txt = ''
    if i >= 160:
        rl.DrawText('PufferAI is fixing RL'.encode(), 500, 65, 60, PUFF_WHITE)

    if i > 250:
        rl.DrawText("Join us".encode(), 520, 65+100, 40, PUFF_CYAN)
        rl.DrawText("www.puffer.ai".encode(), 520, 65+160, 40, PUFF_WHITE)
        rl.DrawText("discord.gg/puffer".encode(), 520, 65+220, 40, PUFF_WHITE)
        rl.DrawText("follow @jsuarez5341".encode(), 520, 65+280, 40, PUFF_WHITE)

    i += 1
    rl.EndDrawing()

    frame = cdata_to_numpy()
    rand = np.random.randint(0, 2, size=(20, frame.shape[1]), dtype=np.uint8)
    frame[:20, :, 3] += rand
    frame[-20:, :, 3] += rand
    frames.append(frame)

    if i >= 400:
        break

rl.CloseWindow()

imageio.mimsave('anim.gif', frames, fps=60, loop=0)
