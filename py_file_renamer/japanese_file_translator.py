import os
import sys
from googletrans import Translator
from tqdm import tqdm
import re
from unidecode import unidecode

def japanese_to_english(text):
    # Comprobar si el texto contiene solo caracteres ASCII
    if all(ord(char) < 128 for char in text):
        return text
    else:
        translator = Translator()
        translation = translator.translate(text, src='ja', dest='en')
        return translation.text

def rename_files_and_folders(root_path):
    total_files = sum(len(files) for _, _, files in os.walk(root_path))
    progress_bar = tqdm(total=total_files, desc="Procesando archivos", unit="archivo")

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Renombrar archivos
        for filename in filenames:
            original_filepath = os.path.join(dirpath, filename)
            file_name, file_extension = os.path.splitext(filename)
            new_filename = japanese_to_english(file_name)
            new_filename = re.sub(r'[^\w\s.,\'-]', '', new_filename) # Sustituir caracteres especiales excepto alfanuméricos, espacios, '.', ',', '-', '_'
            new_filename = unidecode(new_filename)  # Remover acentos
            if not new_filename.strip():  # Si el nuevo nombre está vacío, conserva el nombre original
                new_filename = file_name
            new_filepath = os.path.join(dirpath, new_filename + file_extension)
            os.rename(original_filepath, new_filepath)
            progress_bar.update(1)
        
        # Renombrar carpetas
        for dirname in dirnames:
            original_dirpath = os.path.join(dirpath, dirname)
            new_dirname = japanese_to_english(dirname)
            new_dirname = re.sub(r'[^\w\s.,\'-]', '', new_dirname) # Sustituir caracteres especiales excepto alfanuméricos, espacios, '.', ',', '-', '_'
            new_dirname = unidecode(new_dirname)  # Remover acentos
            if not new_dirname.strip():  # Si el nuevo nombre está vacío, conserva el nombre original
                new_dirname = dirname
            new_dirpath = os.path.join(dirpath, new_dirname)
            os.rename(original_dirpath, new_dirpath)
            progress_bar.update(1)
            # Renombrar archivos dentro de la carpeta
            rename_files_and_folders(new_dirpath)

    progress_bar.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py ruta_a_la_carpeta")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.exists(folder_path):
        print("La ruta especificada no existe.")
        sys.exit(1)

    print("Ruta proporcionada:", folder_path)
    confirmacion = input("¿Quieres proceder con el renombrado de archivos y carpetas? (S/N): ").strip().lower()
    if confirmacion != 's':
        print("Proceso cancelado.")
        sys.exit()

    rename_files_and_folders(folder_path)
