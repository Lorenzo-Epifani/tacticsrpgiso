import os

def delete_files_with_extensions(directory, extensions):
    """
    Elimina tutti i file con le estensioni specificate nella directory e nelle sottodirectory.
    
    :param directory: Directory di partenza
    :param extensions: Tuple di estensioni da eliminare (es: ('.tmp', '.import'))
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Eliminato: {file_path}")
                except Exception as e:
                    print(f"Errore nell'eliminazione di {file_path}: {e}")

if __name__ == "__main__":
    directory = os.getcwd()  # Prende la directory corrente
    extensions = ('.tmp', '.import')
    delete_files_with_extensions(directory, extensions)
