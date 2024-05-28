import os
import sys
from pykakasi import kakasi

def japanese_to_romaji(text):
    kakasi_instance = kakasi()
    kakasi_instance.setMode('H', 'a')  # Romaji mode
    kakasi_instance.setMode('K', 'a')  # Hiragana mode
    kakasi_instance.setMode('J', 'a')  # Katakana mode
    conv = kakasi_instance.getConverter()
    return conv.do(text)

def rename_files_and_folders(root_path):
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Renombrar archivos
        for filename in filenames:
            original_filepath = os.path.join(dirpath, filename)
            new_filename = japanese_to_romaji(filename)
            new_filename = ''.join([c if c.isalnum() or c in ['.', '_', '-', ' '] else '_' for c in new_filename]) # Sustituir caracteres especiales
            new_filepath = os.path.join(dirpath, new_filename)
            os.rename(original_filepath, new_filepath)
        
        # Renombrar carpetas
        for dirname in dirnames:
            original_dirpath = os.path.join(dirpath, dirname)
            new_dirname = japanese_to_romaji(dirname)
            new_dirname = ''.join([c if c.isalnum() or c in ['.', '_', '-', ' '] else '_' for c in new_dirname]) # Sustituir caracteres especiales
            new_dirpath = os.path.join(dirpath, new_dirname)
            os.rename(original_dirpath, new_dirpath)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py ruta_a_la_carpeta")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.exists(folder_path):
        print("La ruta especificada no existe.")
        sys.exit(1)

    rename_files_and_folders(folder_path)
