import argparse
import importlib.util
import os

# Creamos un objeto ArgumentParser para definir los argumentos de línea de comando.
parser = argparse.ArgumentParser(description='Ejecutar un script Python con argumentos opcionales')
parser.add_argument('-t', '--target', help='Dirección IP a escanear', required=True)
parser.add_argument('-p', '--port', help='Puerto a escanear', required=False)
parser.add_argument('script_name', help='Nombre del script a ejecutar')

# Parseamos los argumentos de línea de comando.
args = parser.parse_args()

# Verificamos que el archivo de script exista.
script_path = os.path.join('scripts', args.script_name)
if not os.path.isfile(script_path):
    raise ValueError(f'El archivo {script_path} no existe')

# Importamos el módulo de script.
spec = importlib.util.spec_from_file_location('script_module', script_path)
script_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(script_module)

# Ejecutamos el script con los argumentos de línea de comando.
if args.target and args.port:
    script_module.run(args.target, args.port)
elif args.target:
    script_module.run(args.target)

