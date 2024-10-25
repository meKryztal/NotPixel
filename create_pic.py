from PIL import Image
background = Image.new('RGBA', (1000, 1000), (255, 255, 255, 0))
overlay = Image.open('111.png').convert('RGBA')
overlay_width = int(input("Введите ширину изображения: "))
overlay = overlay.resize((overlay_width, overlay_width))
x = int(input("Введите координату X : ".format(1000 - overlay_width)))
y = int(input("Введите координату Y : ".format(1000 - overlay_width)))
if 0 <= x <= (1000 - overlay_width) and 0 <= y <= (1000 - overlay_width):
    background.paste(overlay, (x, y), overlay.split()[3])
    background.save('orig3.png', format='PNG')
    print(f'\nКоординаты ({x}, {x + overlay_width-1}, {y}, {y + overlay_width-1})')
else:
    print("Координаты вне допустимого диапазона.")
