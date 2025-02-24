from PIL import Image
import os

def crop_rectangles(image_path, output_path):
    # Carica l'immagine
    img = Image.open(image_path)
    
    # Nuove dimensioni dei rettangoli
    rect_width = 32
    rect_height = 32
    num_columns = 12  # Numero di rettangoli per riga
    num_rows = 7  # Numero di righe
    spacing_x = 24  # Spostamento sull'asse X tra i ritagli
    
    # Coordinate Y per ogni riga
    y_positions = [14, 52, 94, 134, 174, 204, 254]
    special_spacing_x = 35  # Offset per l'ultima riga
    
    # Creare un'unica immagine per contenere tutti i ritagli
    combined_width = num_columns * rect_width
    combined_height = rect_height*num_rows  # Altezza sufficiente per l'ultima riga
    combined_image = Image.new("RGB", (combined_width, combined_height), "white")  # Rimosso lo sfondo trasparente
    
    # Esegui il ritaglio e posiziona nell'immagine finale
    for row in range(num_rows):
        current_spacing_x = special_spacing_x if row == 6 else spacing_x  # Usa il nuovo offset solo per l'ultima riga
        for col in range(num_columns):
            x1 = col * current_spacing_x
            y1 = y_positions[row]
            x2 = x1 + rect_width
            y2 = y1 + rect_height
            
            cropped_img = img.crop((x1, y1, x2, y2))
            
            # Posiziona l'immagine ritagliata nella nuova immagine
            combined_image.paste(cropped_img, (col * rect_width, row * rect_height))
    
    # Salva l'immagine combinata
    combined_image.save(output_path)
    print(f'Saved {output_path}')

# Esempio di utilizzo
def process_images_in_subfolders(root_folder):
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".png") and not file.endswith("__.png"):
                image_path = os.path.join(subdir, file)
                output_path = os.path.join(subdir, file.replace(".png", "__.png"))
                crop_rectangles(image_path, output_path)

# Esempio di utilizzo
root_folder = "./"  # Sostituisci con il percorso della cartella radice
process_images_in_subfolders(root_folder)
