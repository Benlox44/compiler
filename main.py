from parser import parser

# Leer el contenido del archivo input.txt
with open('input.txt', 'r') as file:
    code = file.readlines()

# Procesar cada línea del archivo
for line in code:
    line = line.strip()  # Eliminar espacios o saltos de línea
    if line:  # Solo procesar si la línea no está vacía
        try:
            parser.parse(line)
        except Exception as e:
            print(f"Error procesando la línea '{line}': {e}")
