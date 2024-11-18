from PIL import Image


def rgb_to_hex(rgb):
    return '#{:02X}{:02X}{:02X}'.format(rgb[0], rgb[1], rgb[2])

allowed_colors = [
    "#e46e6e", "#FFD635", "#7EED56", "#00CCC0", "#51E9F4", "#94B3FF", "#E4ABFF", "#FF99AA",
    "#FFB470", "#FFFFFF", "#BE0039", "#FF9600", "#00CC78",
    "#009EAA", "#3690EA", "#6A5CFF", "#B44AC0", "#FF3881", "#9C6926", "#898D90", "#6D001A", "#BF4300"
]

background = Image.new('RGBA', (1000, 1000), (255, 255, 255, 0))
overlay = Image.open('111.png').convert('RGBA')
overlay_width = int(input("Введите ширину изображения: "))
overlay = overlay.resize((overlay_width, overlay_width))
x = int(input("Введите координату X : ".format(1000 - overlay_width)))
y = int(input("Введите координату Y : ".format(1000 - overlay_width)))
if 0 <= x <= (1000 - overlay_width) and 0 <= y <= (1000 - overlay_width):
    background.paste(overlay, (x, y), overlay.split()[3])
    background.save('orig3.png', format='PNG')

image = Image.open('orig3.png').convert('RGBA')
width, height = image.size

color_coordinates = {}
unique_color_map = [[None for _ in range(height)] for _ in range(width)]

for x in range(width):
    for y in range(height):
        pixel_color = image.getpixel((x, y))
        hex_color = rgb_to_hex(pixel_color[:3])
        if pixel_color[3] > 0 and hex_color in allowed_colors:
            if unique_color_map[x][y] is None:
                unique_color_map[x][y] = hex_color
                if hex_color not in color_coordinates:
                    color_coordinates[hex_color] = []
                color_coordinates[hex_color].append((x, y))

color_coords_list = []
for color, coordinates in color_coordinates.items():
    for coord in coordinates:
        color_coords_list.append((color, coord))


with open('list.py', 'w') as file:
    file.write("color_coords_list = [\n")
    for color, coord in color_coords_list:
        file.write(f"    ('{color}', {coord}),\n")
    file.write("]\n")

print("Список записан в файл list.py")
