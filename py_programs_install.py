import subprocess
import os

# Función para verificar si una aplicación está instalada
def check_installed(package):
    try:
        subprocess.run(['dpkg', '-s', package], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

# Función para instalar una aplicación desde apt-get
def install_package(package):
    print(f"\n{'*'*20}\nInstalando {package}...")
    try:
        subprocess.run(['sudo', 'apt-get', 'install', '-y', package], check=True)
        print(f"{'*'*20}\n{package} instalado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"{'*'*20}\nError al instalar {package}: {e}\n{'*'*20}")

# Función para instalar Docker y Docker Compose desde el repositorio oficial
def install_docker():
    print(f"\n{'*'*20}\nInstalando Docker desde el repositorio oficial...")
    try:
        # Actualizar el sistema e instalar dependencias necesarias
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'ca-certificates', 'curl', 'gnupg', 'lsb-release'], check=True)

        # Comprobar si el directorio /etc/apt/keyrings ya existe
        if not os.path.exists('/etc/apt/keyrings'):
            subprocess.run(['sudo', 'mkdir', '-m', '0755', '/etc/apt/keyrings'], check=True)

        # Agregar la clave GPG oficial de Docker
        gpg_key_url = 'https://download.docker.com/linux/ubuntu/gpg'
        keyring_path = '/etc/apt/keyrings/docker.gpg'
        
        # Descargar la clave GPG y guardarla en el keyring
        subprocess.run(['curl', '-fsSL', gpg_key_url, '-o', keyring_path], check=True)

        # Agregar el repositorio de Docker
        docker_repo = f'deb [arch=$(dpkg --print-architecture) signed-by={keyring_path}] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable'
        with open('/etc/apt/sources.list.d/docker.list', 'w') as f:
            f.write(docker_repo + '\n')

        # Instalar Docker
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'docker-ce', 'docker-ce-cli', 'containerd.io', 'docker-buildx-plugin', 'docker-compose-plugin'], check=True)
        
        print(f"{'*'*20}\nDocker y Docker Compose instalados correctamente.\n{'*'*20}")
    except subprocess.CalledProcessError as e:
        print(f"{'*'*20}\nError al instalar Docker: {e}\n{'*'*20}")

# Función para leer el listado de aplicaciones desde un archivo
def read_applications(file_path):
    if not os.path.exists(file_path):
        print(f"\n{'*'*20}\nEl archivo {file_path} no existe.\n{'*'*20}")
        return []
    
    with open(file_path, 'r') as file:
        apps = [line.strip() for line in file.readlines()]
    return apps

# Función para mostrar el menú de selección
def display_menu(apps):
    print("\n" + "="*40)
    print("Seleccione las aplicaciones que desea instalar (marcadas con * si ya están instaladas):\n")
    selected_apps = []
    
    for i, app in enumerate(apps):
        if app == "docker":
            installed = check_installed("docker-ce")
        else:
            installed = check_installed(app)
        mark = "*" if installed else " "
        print(f"[{mark}] {i+1}. {app}")
    
    print("\n" + "="*40)
    print("Ingrese los números de las aplicaciones que desea instalar separados por comas (ej: 1,3,5), o presione Enter para seleccionar todas:")
    user_input = input("Seleccionar: ")
    
    if user_input.strip() == "":
        selected_apps = apps  # Seleccionar todas si el usuario presiona Enter
    else:
        selections = [int(num.strip()) - 1 for num in user_input.split(",") if num.strip().isdigit()]
        selected_apps = [apps[i] for i in selections if 0 <= i < len(apps)]
    
    return selected_apps

# Función principal
def main():
    # Ruta del archivo que contiene el listado de aplicaciones
    file_path = 'applications.txt'
    
    # Leer las aplicaciones desde el archivo
    apps = read_applications(file_path)
    if not apps:
        return
    
    # Mostrar el menú de selección
    selected_apps = display_menu(apps)
    
    # Actualizar la lista de paquetes antes de instalar
    print("\n" + "="*40)
    print("Actualizando el sistema...")
    subprocess.run(['sudo', 'apt-get', 'update'], check=True)
    
    # Instalar las aplicaciones seleccionadas
    for app in selected_apps:
        if app == "docker":
            if check_installed("docker-ce"):
                print(f"\n{'*'*20}\nDocker ya está instalado.\n{'*'*20}")
            else:
                install_docker()
        elif check_installed(app):
            print(f"\n{'*'*20}\n{app} ya está instalado.\n{'*'*20}")
        else:
            install_package(app)

if __name__ == "__main__":
    main()
