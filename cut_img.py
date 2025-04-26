import tkinter as tk
from PIL import ImageGrab, Image, ImageDraw, ImageTk
import pyautogui
import keyboard
x_start, y_start, x_end, y_end = 0, 0, 0, 0
drawing = False
capture_result = None

def on_move(event, canvas):
    global x_end, y_end, drawing

    if drawing:
        x_end, y_end = event.x_root, event.y_root
        draw_rectangle(canvas)

def draw_rectangle(canvas):
    screen_captured = ImageGrab.grab()
    mask = Image.new('L', screen_captured.size, 50)
    draw = ImageDraw.Draw(mask)
    # Garante que o retângulo seja desenhado corretamente, mesmo ao arrastar para cima ou para a esquerda
    xmin, ymin = min(x_start, x_end), min(y_start, y_end)
    xmax, ymax = max(x_start, x_end), max(y_start, y_end)
    draw.rectangle([xmin, ymin, xmax, ymax], fill=255)
    alpha = Image.new('L', screen_captured.size, 100)
    alpha.paste(mask, (0, 0), mask=mask)

    # Aplica a máscara na região selecionada da imagem
    img = Image.composite(screen_captured, Image.new('RGB', screen_captured.size, 'white'), alpha)

    img_tk = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, image=img_tk, anchor=tk.NW)
    canvas.img_tk = img_tk

def on_click(event):
    global x_start, y_start, drawing

    x_start, y_start = event.x_root, event.y_root
    drawing = True

def finalizar_programa(root, filename):
    global x_start, y_start, x_end, y_end, capture_result
    x1, y1 = min(x_start, x_end), min(y_start, y_end)
    x2, y2 = max(x_start, x_end), max(y_start, y_end)
    width = x2 - x1
    height = y2 - y1
    print(f'Left: {x1}, Top: {y1}, Width: {width}, Height: {height}')
    
    root.withdraw()
    img = pyautogui.screenshot(region=(x1, y1, width, height))
    if filename:
        img.save(filename)
    else:
        img.save('oiaaaa.png')
    root.deiconify()
    capture_result = (x1, y1, width, height)
    root.destroy()  # Use destroy em vez de quit
    return capture_result

def on_release(_, root, filename):
    global drawing

    drawing = False
    return finalizar_programa(root, filename)

# Cria a janela principal
def start_capture(filename=None):
    global capture_result
    root = tk.Tk()
    root.overrideredirect(True)  # Remove a barra de título e bordas da janela
    root.attributes('-topmost', True)  # Mantém a janela no topo de outras janelas
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))  # Define o tamanho da janela para a tela inteira
    root.attributes('-alpha', 0.5)  # Define a transparência da janela (0.5 = 50% de opacidade)

    canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(),  highlightthickness=0)
    canvas.pack()

    canvas.bind("<B1-Motion>", lambda event: on_move(event, canvas))
    canvas.bind("<ButtonPress-1>", on_click)
    canvas.bind("<ButtonRelease-1>", lambda _: on_release(_, root, filename))
    root.mainloop()
    return capture_result
if __name__ == "__main__":
    keyboard.wait('h')
    resultado = start_capture()
    print("Resultado:", resultado)