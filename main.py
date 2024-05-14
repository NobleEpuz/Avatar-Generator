import customtkinter as ctk
from PIL import Image, ImageDraw
import numpy as np

def generate_avatar(filename, color1, color2, angle, icon_path, resize_icon=True, icon_scale=0.6):
    # Создаем новое изображение
    width, height = 256, 256
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)

    # Создаем градиент
    for y in range(height):
        for x in range(width):
            ratio = (x * np.cos(np.radians(angle)) + y * np.sin(np.radians(angle))) / (width + height)
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            draw.point((x, y), (r, g, b))

    # Открываем иконку
    icon = Image.open(icon_path)
    
    # Масштабируем иконку, если указано
    if resize_icon:
        icon_size = int(min(width, height) * icon_scale)  # Иконка занимает указанную долю от размера аватарки
        icon_ratio = min(icon_size / icon.width, icon_size / icon.height)
        new_icon_size = (int(icon.width * icon_ratio), int(icon.height * icon_ratio))
        icon = icon.resize(new_icon_size, Image.LANCZOS)
    
    # Проверяем наличие альфа-канала иконки и преобразуем при необходимости
    if icon.mode != 'RGBA':
        icon = icon.convert('RGBA')
    
    # Вставляем иконку в центр
    icon_position = ((width - icon.width) // 2, (height - icon.height) // 2)
    image.paste(icon, icon_position, icon)

    # Сохраняем изображение
    image.save(filename)
    return image

def on_generate_click():
    filename = filename_entry.get()
    color1 = tuple(map(int, color1_entry.get().split()))
    color2 = tuple(map(int, color2_entry.get().split()))
    angle = float(angle_entry.get())
    icon_path = icon_path_entry.get()
    resize_icon = resize_var.get()
    icon_scale = float(icon_scale_entry.get()) if resize_icon else 1.0

    avatar_image = generate_avatar(filename, color1, color2, angle, icon_path, resize_icon, icon_scale)
    preview_image = avatar_image.resize((128, 128), Image.LANCZOS)
    preview_photo = ctk.CTkImage(light_image=preview_image, size=(128, 128))
    preview_label.configure(image=preview_photo)
    preview_label.image = preview_photo

app = ctk.CTk()
app.title("Avatar Generator")
app.geometry("400x500")  # Устанавливаем начальный размер окна
app.minsize(400, 500)    # Устанавливаем минимальный размер окна

# Ввод имени файла
ctk.CTkLabel(app, text="Имя файла:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
filename_entry = ctk.CTkEntry(app)
filename_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

# Ввод первого цвета градиента
ctk.CTkLabel(app, text="Первый цвет (R G B):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
color1_entry = ctk.CTkEntry(app)
color1_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

# Ввод второго цвета градиента
ctk.CTkLabel(app, text="Второй цвет (R G B):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
color2_entry = ctk.CTkEntry(app)
color2_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

# Ввод угла градиента
ctk.CTkLabel(app, text="Угол градиента:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
angle_entry = ctk.CTkEntry(app)
angle_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

# Ввод пути к иконке
ctk.CTkLabel(app, text="Путь к иконке:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
icon_path_entry = ctk.CTkEntry(app)
icon_path_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

# Опция изменения размера иконки
resize_var = ctk.BooleanVar(value=True)
resize_check = ctk.CTkCheckBox(app, text="Изменять размер иконки", variable=resize_var)
resize_check.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

# Ввод коэффициента размера иконки
ctk.CTkLabel(app, text="Коэффициент размера иконки:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
icon_scale_entry = ctk.CTkEntry(app)
icon_scale_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

# Кнопка генерации аватарки
generate_button = ctk.CTkButton(app, text="Сгенерировать аватарку", command=on_generate_click)
generate_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Превью аватарки
preview_label = ctk.CTkLabel(app, text="")
preview_label.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Настройка для изменения размера виджетов вместе с окном
for i in range(9):
    app.grid_rowconfigure(i, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

app.mainloop()
