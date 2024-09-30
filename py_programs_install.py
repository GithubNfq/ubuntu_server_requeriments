import curses
import os
import subprocess

# Listado de programas disponibles para instalar
PROGRAMAS = [
    "vim",
    "git",
    "curl",
    "htop",
    "wget",
    "gimp",
    "python3-pip",
    "vlc",
    "build-essential",
    "net-tools",
]

# Función para verificar si un programa está instalado
def esta_instalado(programa):
    try:
        subprocess.run(["dpkg", "-l", programa], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

# Función para mostrar y permitir seleccionar programas usando curses
def mostrar_menu(stdscr, programas, instalados):
    curses.curs_set(0)  # Ocultar el cursor
    current_row = 0  # Fila actual seleccionada
    seleccionados = [False] * len(programas)  # Estado de selección de los programas

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Selecciona los programas que deseas instalar (Espacio para seleccionar, Enter para confirmar):")

        # Mostrar programas y si están seleccionados
        for idx, programa in enumerate(programas):
            # Marcar con 'X' si ya está instalado
            x = "X" if instalados[idx] or seleccionados[idx] else " "
            stdscr.addstr(idx + 1, 0, f"[{x}] {programa}", curses.A_REVERSE if idx == current_row else curses.A_NORMAL)

        key = stdscr.getch()  # Leer entrada de teclado

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(programas) - 1:
            current_row += 1
        elif key == ord(" "):  # Alternar selección con barra espaciadora (si no está ya instalado)
            if not instalados[idx]:  # No se puede deseleccionar si ya está instalado
                seleccionados[current_row] = not seleccionados[current_row]
        elif key == ord("\n"):  # Confirmar selección con Enter
            break

        stdscr.refresh()

    return [programa for idx, programa in enumerate(programas) if seleccionados[idx]]

# Función para instalar programas seleccionados
def instalar_programas(programas):
    if not programas:
        print("No se seleccionaron programas para instalar.")
        return

    print("Instalando programas...")
    for programa in programas:
        try:
            print(f"Instalando {programa}...")
            subprocess.run(["sudo", "apt", "install", "-y", programa], check=True)
        except subprocess.CalledProcessError:
            print(f"Error al instalar {programa}.")
        else:
            print(f"{programa} instalado correctamente.")

def main():
    # Verificar cuáles programas ya están instalados
    instalados = [esta_instalado(programa) for programa in PROGRAMAS]

    # Ejecutar la interfaz de selección
    seleccionados = curses.wrapper(mostrar_menu, PROGRAMAS, instalados)

    # Mostrar los programas seleccionados y proceder a instalarlos
    if seleccionados:
        print(f"Programas seleccionados: {', '.join(seleccionados)}")
        instalar_programas(seleccionados)
    else:
        print("No se seleccionó ningún programa.")

if __name__ == "__main__":
    main()
