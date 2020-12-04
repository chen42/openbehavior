



import board, neopixel

p = neopixel.NeoPixel(board.D18,12)


for i in range(len(p)):
    p[i] = (0,0,0)
