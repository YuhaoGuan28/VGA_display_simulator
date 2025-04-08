from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os


# =======================
# functions
# =======================
current_dir = os.path.dirname(os.path.abspath(__file__))
font_12 = ImageFont.truetype(f"{current_dir}\Monocraft.ttf", 12)
font_30 = ImageFont.truetype(f"{current_dir}\Monocraft.ttf", 30)
def init():
    # Default Setting
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    img = Image.new('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT), (255,255,255))
    img = Image.new('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT), (0,0,0))
    """
    pic = Image.open(f"{current_dir}\img\\bg.jpg").resize((640,480))
    img.paste(pic, (0, 0))
    #"""
    draw = ImageDraw.Draw(img)

    """
    # title
    title_text = "FPGA GUI Preview (RGB444 Mode)"
    bbox_title = draw.textbbox((0,0), title_text, font=font_30)
    title_w, title_h = bbox_title[2]-bbox_title[0], bbox_title[3]-bbox_title[1]
    title_x = (SCREEN_WIDTH - title_w) // 2
    title_y = (SCREEN_HEIGHT - title_h) // 2
    draw.text((title_x, title_y), title_text, font=font_30, fill=(0, 0, 0))
    #"""
    """
    # grid
    for x in range(0, SCREEN_WIDTH, 40):
        draw.line([(x, 0), (x, SCREEN_HEIGHT)], fill="gray", width=1)
    for y in range(0, SCREEN_HEIGHT, 40):
        draw.line([(0, y), (SCREEN_WIDTH, y)], fill="gray", width=1)
    #"""
    return img, draw
    
def gen_char(draw):
    draw.text((2, -1+300), "ABCDEFGHIJKLMN\nOPQRSTUVWXYZ", font=font_30, fill=(62, 62, 62))
    draw.text((0, -3+300), "ABCDEFGHIJKLMN\nOPQRSTUVWXYZ", font=font_30, fill=(0, 0, 255))
    draw.text((2, 67+300), "abcdefghijklmn\nopqrstuvwxyz", font=font_30, fill=(62, 62, 62))
    draw.text((0, 65+300), "abcdefghijklmn\nopqrstuvwxyz", font=font_30, fill=(0, 0, 255))
    draw.text((2, 132+300), "1234567890.-#", font=font_30, fill=(62, 62, 62))
    draw.text((0, 130+300), "1234567890.-#", font=font_30, fill=(0, 0, 255))


# button
btn_dim = (120, 30)
btn_dic = {"btn1": "Blur",
           "btn2": "Outline",
           "btn3": "Sharpen",
           "btn4": "Top sobel",
           "btn5": "Default"}
def create_a_btn(draw, x, y, n):
    draw.rectangle((x, y, x+btn_dim[0]-1, y+btn_dim[1]-1), fill=(141, 141, 141), outline=(0, 0, 0), width=2)
    draw.line((x+2, y+2, x+2, y+btn_dim[1]-6-1), fill=(255, 255, 255), width=2)
    draw.line((x+2, y+2, x+btn_dim[0]-4-1, y+2), fill=(255, 255, 255), width=2)
    draw.line((x+btn_dim[0]-3-1, y+4, x+btn_dim[0]-3-1, y+btn_dim[1]-2-1), fill=(88, 86, 88), width=2)
    draw.line((x+4, y+btn_dim[1]-4-1, x+btn_dim[0]-3-1, y+btn_dim[1]-4-1), fill=(88, 86, 88), width=4)
    text = btn_dic[f"btn{n+1}"]
    textbox = draw.textbbox((0,0), text, font=font_12)
    text_w, text_h = textbox[2]-textbox[0], textbox[3]-textbox[1]
    textbox_x = (btn_dim[0] - text_w) // 2
    textbox_y = (btn_dim[1] - text_h) // 2
    draw.text((x+textbox_x+1, y+textbox_y+1), text, font=font_12, fill=(63, 63, 63))
    draw.text((x+textbox_x, y+textbox_y), text, font=font_12, fill=(255, 255, 255))
def create_btn(draw, n):
    for i in range(n):
        create_a_btn(draw, 480, 410-i*40, i)
def toggle_btn(draw, n):
    x = 480
    y = 410-(n-1)*40
    draw.rectangle((x, y, x+btn_dim[0]-1, y+btn_dim[1]-1), fill=(67, 160, 28), outline=(255, 255, 255), width=2)
    draw.line((x+2, y+2, x+2, y+btn_dim[1]-6-1), fill=(55, 214, 30), width=2)
    draw.line((x+2, y+2, x+btn_dim[0]-4-1, y+2), fill=(55, 214, 30), width=2)
    draw.line((x+btn_dim[0]-3-1, y+4, x+btn_dim[0]-3-1, y+btn_dim[1]-2-1), fill=(3, 115, 0), width=2)
    draw.line((x+4, y+btn_dim[1]-4-1, x+btn_dim[0]-3-1, y+btn_dim[1]-4-1), fill=(3, 115, 0), width=4)
    text = btn_dic[f"btn{n}"]
    textbox = draw.textbbox((0,0), text, font=font_12)
    text_w, text_h = textbox[2]-textbox[0], textbox[3]-textbox[1]
    textbox_x = (btn_dim[0] - text_w) // 2
    textbox_y = (btn_dim[1] - text_h) // 2
    draw.text((x+textbox_x+1, y+textbox_y+1), text, font=font_12, fill=(63, 63, 0))
    draw.text((x+textbox_x, y+textbox_y), text, font=font_12, fill=(255, 255, 0))
def print_title(draw, n):
    text = btn_dic[f"btn{n}"]
    text = f"MODE: {text.upper()}"
    draw.text((40+2, 40+2), text, font=font_12, fill=(63, 63, 0))
    draw.text((40, 40), text, font=font_12, fill=(255, 255, 0))
    text = f"FPS: 60"
    draw.text((40+2, 75+2), text, font=font_30, fill=(63, 63, 0))
    draw.text((40, 75), text, font=font_30, fill=(255, 255, 0))

def print_title_bg(img, draw, n):
    img_array = np.array(img)
    text = btn_dic[f"btn{n}"]
    text = f"MODE: {text.upper()}"
    textbox = draw.textbbox((0,0), text, font=font_30)
    img_array[textbox[1]+40-5:textbox[3]+42+5, textbox[0]+40-5:textbox[2]+42+5] = img_array[textbox[1]+40-5:textbox[3]+42+5, textbox[0]+40-5:textbox[2]+42+5] / [3, 3, 3]

    text = f"FPS: 60"
    textbox = draw.textbbox((0,0), text, font=font_30)
    img_array[textbox[1]+75-4:textbox[3]+77+5, textbox[0]+40-5:textbox[2]+42+5] = img_array[textbox[1]+75-4:textbox[3]+77+5, textbox[0]+40-5:textbox[2]+42+5] / [3, 3, 3]

    img = Image.fromarray(img_array)
    return img



# =======================
# GUI image
# =======================
def create_gui_image(n):
    
    img, draw = init()
    # ------------------------------------------------------- DRAW AREA ------------------------------------------------------- #
    #gen_char(draw)
    btn_sel = 3
    
    """
    if btn_sel == 1:
        pic = Image.open(f"{current_dir}\img\\bg_blur.jpg")
        img.paste(pic, (0, 0))
    elif btn_sel == 2:
        pic = Image.open(f"{current_dir}\img\\bg_edge.jpg")
        img.paste(pic, (0, 0))
    elif btn_sel == 3:
        pic = Image.open(f"{current_dir}\img\\bg_sharp.jpg")
        img.paste(pic, (0, 0))
    elif btn_sel == 4:
        pic = Image.open(f"{current_dir}\img\\bg_top.jpg")
        img.paste(pic, (0, 0))
    else:
        pic = Image.open(f"{current_dir}\img\\bg.jpg")
        img.paste(pic, (0, 0))
    #"""

    #img = print_title_bg(img, draw, btn_sel)
    draw = ImageDraw.Draw(img)
    print_title(draw, btn_sel)
    create_btn(draw, 5)
    toggle_btn(draw, btn_sel)

    
    #draw.rectangle((479, 409, 600, 440), outline=(255, 0, 0), width=1)
    #draw.rectangle((479, 329, 600, 360), outline=(255, 0, 0), width=1)

    ele_name = 'Y'
    draw.text((1, 0), ele_name, font=font_12, fill=(63, 63, 0))
    draw.text((0, -1), ele_name, font=font_12, fill=(255, 255, 0))
    draw.rectangle((-1, -1, 8, 11), outline=(255, 0, 0), width=1)

    # ------------------------------------------------------- DRAW AREA ------------------------------------------------------- #

    return img

"""
# 1px
draw.point((x, y), fill=(r, g, b))

# line
draw.line((x1, y1, x2, y2), fill=(r, g, b), width=1)

# rectangle
draw.rectangle((x1, y1, x2, y2), fill=(r, g, b))
draw.rectangle((x1, y1, x2, y2), outline=(r, g, b), width=1)

# ellipse
draw.ellipse((x1, y1, x2, y2), fill=(r, g, b))
draw.ellipse((x1, y1, x2, y2), outline=(r, g, b), width=1)

# arc
draw.arc((x1, y1, x2, y2), start=0, end=360, fill=(r, g, b), width=1)

# chord
draw.chord((x1, y1, x2, y2), start=0, end=360, fill=(0, 0, 0), outline=(0, 0, 0), width=1)

# polygon
draw.polygon([(x, y), (x, y), (x, y)], fill=(r, g, b))
draw.polygon([(x, y), (x, y), (x, y)], outline=(r, g, b), width=1)

# array
img_array[x1:x2, y1:y2] = [r, g, b]
img = Image.fromarray(img_array)

# pic
pic = Image.open("pic.png").resize((w,h))
img.paste(pic, (x, y))

# txt
font = ImageFont.load_default()
font = ImageFont.truetype("/path/to/font.ttf", 36)
text = "text"
textbox = draw.textbbox((0,0), text, font=font)
#textbox=(x1, y1, x2, y2)
draw.text((x, y), "Hello World!", font=font, fill=(r, g, b))

# get img array
img_array = np.array(img)


"""
