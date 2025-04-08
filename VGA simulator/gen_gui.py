from flask import Flask, send_file, render_template_string, request
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io, time, traceback
import importlib, sys


app = Flask(__name__)
i = 1
# Screen Dim
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# =======================
# access GUI image code
# =======================
def safe_create_gui_image():
    global i
    try:
        if 'gui_code' in sys.modules:
            del sys.modules['gui_code']
        gui_code = importlib.import_module('gui_code')

        img = gui_code.create_gui_image(i)
        i = (i + 1) % 6
        if i==0:
            i = 1
        return img
    except Exception as e:
        print("[Error in code]:", e)
        traceback.print_exc()
        error_img = Image.new('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT), (255,0,0))
        draw = ImageDraw.Draw(error_img)
        draw.text((10,10), f"ERROR: {str(e)}", fill=(255,255,255))
        return error_img


# =======================
# RGB888-RGB444 (12-bit)
# =======================
def rgb888_to_rgb444(r,g,b):
    r4 = np.uint16(r >> 4)
    g4 = np.uint16(g >> 4)
    b4 = np.uint16(b >> 4)
    color = (r4 << 8) | (g4 << 4) | b4
    #print(hex(color))
    return np.uint16(color)


# =======================
# Flask webpage
# =======================
@app.route('/')
def index():
    html = '''
    <html>
        <head><title>FPGA GUI Live Preview</title></head>
        <body style="font-family:sans-serif;">
            <h3>FPGA GUI Live Preview (Auto-refresh every second)</h3>
            <img id="gui_img" src="/gui_image?{{t}}" width="640" height="480" style="border: 3px solid black;"/><br/>
            <h4>📌 Capture area (x, y, width, height): </h4>
            <form action="/generate_rom" method="get">
                X: <input type="number" name="x" value="0" min="0" max="639">
                Y: <input type="number" name="y" value="0" min="0" max="479"><br>
                Width: <input type="number" name="w" value="8" min="1" max="640">
                Height: <input type="number" name="h" value="11" min="1" max="480"><br><br>
                <input type="submit" value="⚡ Generate files (RGB444)">
            </form>
            <script>
                setInterval(()=>{
                    document.getElementById("gui_img").src = "/gui_image?" + new Date().getTime();
                }, 1000);
            </script>
        </body>
    </html>
    '''
    return render_template_string(html, t=time.time())


# =======================
# Update GUI image to webpage
# =======================
@app.route('/gui_image')
def gui_image():
    img = safe_create_gui_image()

    # change image to RGB444
    pixels = np.array(img)
    h, w = img.height, img.width
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[y,x]
            # RGB888 -> RGB444 -> RGB888
            r4, g4, b4 = r>>4, g>>4, b>>4
            pixels[y,x] = [(r4<<4)+15, (g4<<4)+15, (b4<<4)+15]

    img_rgb444_preview = Image.fromarray(pixels)

    img_io = io.BytesIO()
    img_rgb444_preview.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


# =======================
# Generate files
# =======================
@app.route('/generate_rom')
def generate_rom():
    try:
        img = safe_create_gui_image()
        pixels = np.array(img)

        # Read param with GET
        x = int(request.args.get('x', 0))
        y = int(request.args.get('y', 0))
        w = int(request.args.get('w', 8))
        h = int(request.args.get('h', 11))

        # check if size are out of bound
        x = max(0, min(x, SCREEN_WIDTH - 1))
        y = max(0, min(y, SCREEN_HEIGHT - 1))
        w = max(1, min(w, SCREEN_WIDTH - x))
        h = max(1, min(h, SCREEN_HEIGHT - y))


        # generate VHDL
        with open(f"element.vhd", "w") as f:
            f.write(f"type gui_ele_type is array (0 to {h-1}, 0 to {w-1}) of std_logic_vector(11 downto 0);\n")
            f.write(f"constant element_12 : gui_ele_font12_type := (\n")

            # 生成 VHDL ROM 数据
            rom_data = []
            for row in range(y, y + h):
                line_data = []
                for col in range(x, x + w):
                    r, g, b = pixels[row, col]
                    color = rgb888_to_rgb444(r, g, b)
                    line_data.append(f'x"{color:03X}"')
                rom_data.append("    (" + ", ".join(line_data) + ")")

            f.write(",\n".join(rom_data) + "\n);\n")

        # generate .png file
        cropped_img = img.crop((x, y, x + w, y + h))
        png_filename = f"element.png"
        cropped_img.save(png_filename)

        # return messages
        return f'''
        <html><body>
        <h3 style="color:green;">✅ Generation succeed (RGB444)</h3>
        <h4>Area: (X={x}, Y={y}, W={w}, H={h})</h4>
        <pre>Saved {w}x{h} GUI data</pre>
        <a href="/">⬅️ Return to GUI preview</a>
        </body></html>
        '''

    except Exception as e:
        traceback.print_exc()
        return f'''
        <html><body>
        <h3 style="color:red;">❌ Generation failed:</h3>
        <pre>{str(e)}</pre>
        <a href="/">⬅️ Return to GUI preview</a>
        </body></html>
        '''

# =======================
# start FLASK server
# =======================
if __name__ == "__main__":
    app.run(debug=True)
