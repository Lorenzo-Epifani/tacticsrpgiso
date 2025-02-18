from PIL import Image, ImageEnhance
import cv2
import numpy as np
import os

def process_image(input_path, output_path):
    # Apri l'immagine mantenendo il canale alfa
    img = Image.open(input_path).convert("RGBA")

    # Separiamo i canali RGBA
    r, g, b, alpha = img.split()

    # Creiamo una maschera per identificare le parti non trasparenti
    alpha_array = np.array(alpha)
    mask = alpha_array > 0  # True dove l'immagine è visibile, False dove è trasparente

    # Unisci i canali RGB in un array per OpenCV
    img_rgb = Image.merge("RGB", (r, g, b))
    img_cv = np.array(img_rgb)

    # 📌 **Ridimensioniamo anche il canale alpha per evitare mismatch di dimensioni**
    img_resized = img_rgb.resize((64, 64), Image.NEAREST)
    alpha_resized = alpha.resize((64, 64), Image.NEAREST)  # Ridimensioniamo la trasparenza

    # Converti in array per OpenCV
    img_cv_resized = np.array(img_resized)

    # 📌 **Ricalcoliamo la maschera dopo il ridimensionamento**
    alpha_array_resized = np.array(alpha_resized)
    mask_resized = alpha_array_resized > 0  # Creiamo di nuovo la maschera sulle nuove dimensioni

    # **Posterizzazione (Riduzione colori)**
    img_cv_resized = cv2.cvtColor(img_cv_resized, cv2.COLOR_RGB2Lab)
    img_cv_resized = cv2.cvtColor(img_cv_resized, cv2.COLOR_Lab2RGB)

    # **Aumento del Contrasto e Nitidezza**
    img_processed = Image.fromarray(img_cv_resized)
    img_processed = ImageEnhance.Sharpness(img_processed).enhance(0.3)  # Aumenta la nitidezza
    img_processed = ImageEnhance.Contrast(img_processed).enhance(1.5)  # Aumenta il contrasto

    # **Applichiamo la maschera ridimensionata alla parte visibile**
    img_final_array = np.array(img_processed)
    img_final_array[~mask_resized] = [0, 0, 0]  # Rimuoviamo l'elaborazione dalle parti trasparenti

    # **Convertiamo di nuovo in immagine PIL**
    img_final_pil = Image.fromarray(img_final_array)

    # **Ricombiniamo con il canale alpha ridimensionato**
    img_output = Image.merge("RGBA", (*img_final_pil.split(), alpha_resized))

    # **Salviamo in PNG mantenendo la trasparenza**
    img_output.save(output_path, "PNG")
    print(f"✅ Immagine processata salvata in {output_path}")

# Cartelle di input e output
input_folder = "original"
output_folder = "pixelized"

# Crea la cartella di output se non esiste
os.makedirs(output_folder, exist_ok=True)

# Processa tutte le immagini nella cartella originale
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):  # Filtra solo immagini
        input_path = os.path.join(input_folder, filename)

        # Dividi il nome file e l'estensione
        name, ext = os.path.splitext(filename)

        # Aggiungi "_px" prima dell'estensione
        output_filename = f"{name}_px.png"
        output_path = os.path.join(output_folder, output_filename)

        # Processa l'immagine
        process_image(input_path, output_path)

print("🎉 Elaborazione completata per tutte le immagini!")


input_folder = "original"
output_folder = "pixelized"

# Crea la cartella di output se non esiste
os.makedirs(output_folder, exist_ok=True)

# Processa tutte le immagini nella cartella originale
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):  # Filtra solo immagini
        input_path = os.path.join(input_folder, filename)
        
        # Dividi il nome file e l'estensione
        name, ext = os.path.splitext(filename)
        
        # Aggiungi "_px" prima dell'estensione
        output_filename = f"{name}_px.png"
        output_path = os.path.join(output_folder, output_filename)
        
        # Processa l'immagine
        process_image(input_path, output_path)

print("Elaborazione completata per tutte le immagini!")
