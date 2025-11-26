#!/usr/bin/env python3
import os
import subprocess

# Carpeta de wallpapers
WALLPAPER_DIR = os.path.expanduser("~/Wallpapers")
ROFI_THEME = os.path.expanduser("~/.config/rofi/launchers/type-1/style-1.rasi")

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')

def get_wallpapers():
    """Lista imágenes recursivamente en la carpeta de wallpapers y subcarpetas"""
    wallpapers = []
    for root, _, files in os.walk(WALLPAPER_DIR):
        for f in files:
            if f.lower().endswith(IMAGE_EXTENSIONS):
                # Mostrar ruta relativa desde WALLPAPER_DIR
                rel_path = os.path.relpath(os.path.join(root, f), WALLPAPER_DIR)
                wallpapers.append(rel_path)
    return sorted(wallpapers)

def rofi_select(options, prompt="Wallpaper Selector", selected_row=0):
    """Selector con rofi, permite resaltar la opción seleccionada"""
    if not options:
        return None
    rofi_input = "\n".join(options)
    cmd = [
        "rofi", "-dmenu", "-i", "-p", prompt, "-theme", ROFI_THEME,
        "-mesg", "Selecciona un wallpaper. Se aplicará al elegirlo.",
        "-selected-row", str(selected_row)
    ]
    result = subprocess.run(
        cmd,
        input=rofi_input,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None

def set_wallpaper(rel_path):
    """Establece el wallpaper con feh usando ruta relativa y guarda el path en ~/.config/wallpaper"""
    path = os.path.join(WALLPAPER_DIR, rel_path)
    if os.path.exists(path):
        subprocess.run(["feh", "--bg-scale", path])
        subprocess.run(["notify-send", "Wallpaper cambiado", rel_path])
        # Guardar el path absoluto en ~/.config/wallpaper
        config_path = os.path.expanduser("~/.config/wallpaper")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as f:
            f.write(path + "\n")
        return True
    return False

def main():
    wallpapers = get_wallpapers()
    if not wallpapers:
        subprocess.run(["notify-send", "No se encontraron wallpapers", WALLPAPER_DIR])
        return
    selected = None
    selected_row = 0
    while True:
        if selected and selected in wallpapers:
            selected_row = wallpapers.index(selected)
        else:
            selected_row = 0
        selected = rofi_select(wallpapers, selected_row=selected_row)
        if not selected or selected not in wallpapers:
            break  # Sale si se pulsa Esc o clic fuera
        set_wallpaper(selected)

if __name__ == "__main__":
    main()
