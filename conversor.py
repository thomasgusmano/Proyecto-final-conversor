import os
from tkinter import Tk, Label, Button, filedialog, OptionMenu, StringVar
from charset_normalizer import from_path

def detect_encoding(path):
    """Detecta BOM (UTF-8/UTF-16). Si no es UTF detectado, asume ANSI (windows-1252)."""
    try:
        with open(path, 'rb') as f:
            start = f.read(4)
        if start.startswith(b'\xEF\xBB\xBF'): return 'utf-8-sig'
        if start.startswith(b'\xFE\xFF'): return 'utf-16-be'
        if start.startswith(b'\xFF\xFE'): return 'utf-16-le'

        result = from_path(path).best()
        if result:
            enc = result.encoding.lower()
            if enc in ('utf_8','utf-8','utf_16','utf_16_be','utf_16_le'):
                return enc
        return 'windows-1252'
    except Exception:
        return 'windows-1252'

def friendly_name(enc):
    """Convierte codificación técnica a nombre amigable para mostrar en la UI."""
    if not enc: return 'desconocida'
    enc = enc.lower()
    if enc == 'windows-1252': return 'ANSI'
    if enc == 'utf-8-sig': return 'UTF-8-BOM'
    if enc == 'utf-8': return 'UTF-8'
    if enc in ('utf-16-le','utf-16-be','utf-16'): return enc.upper()
    return enc

def convert_file(src, dst, enc_from, enc_to):
    """Convierte archivo leyendo en enc_from y escribiendo en enc_to.
       Reemplaza caracteres no soportados para evitar errores."""
    text = open(src, 'r', encoding=enc_from, errors='replace').read()
    with open(dst, 'wb') as f:
        # Agregar BOM explícito para UTF-16 BE/LE
        if enc_to in ('utf-16-be', 'utf-16-le'):
            f.write(b'\xFE\xFF' if enc_to.endswith('be') else b'\xFF\xFE')
        # Para utf-8-sig, escribir el BOM lo maneja encode('utf-8-sig'), pero aquí usamos encode con errors='replace'
        # Encodificar y escribir bytes
        if enc_to == 'utf-8-sig':
            f.write(text.encode('utf-8-sig', errors='replace'))
        else:
            f.write(text.encode(enc_to, errors='replace'))

    status_label.config(text=f"Convertido a {friendly_name(enc_to)}: {os.path.basename(dst)}")

def select_file():
    path = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Archivos de texto","*.txt;*.csv;*.log"),("Todos","*.*")]
    )
    if not path: return
    app.file = path
    app.enc = detect_encoding(path)
    input_label.config(text=os.path.basename(path))
    status_label.config(text=f"Detectado: {friendly_name(app.enc)}")

def convert():
    if not hasattr(app, 'file'): 
        status_label.config(text="Seleccioná un archivo primero.")
        return
    enc_from = getattr(app, 'enc', 'windows-1252')
    enc_to = enc_map[enc_var.get()]
    save = filedialog.asksaveasfilename(
        title="Guardar como",
        defaultextension=".txt",
        filetypes=[("Archivos de texto","*.txt"),("Todos","*.*")],
        initialdir=os.path.dirname(app.file),
        initialfile=f"{os.path.splitext(os.path.basename(app.file))[0]}-converted-{enc_var.get().replace(' ','_')}.txt"
    )
    if save:
        convert_file(app.file, save, enc_from, enc_to)

# --- Interfaz ---
app = Tk()
app.title("Conversor de Codificación (Notepad++ compatible)")

Label(app, text="Archivo:").grid(row=0, column=0, padx=10, pady=6, sticky="w")
Button(app, text="Seleccionar", command=select_file).grid(row=0, column=1)
input_label = Label(app, text="(ninguno)", fg="gray")
input_label.grid(row=0, column=2, sticky="w", padx=10)

Label(app, text="Codificación destino:").grid(row=1, column=0, padx=10, pady=6)
enc_opts = ["ANSI", "UTF-8", "UTF-8-BOM", "UTF-16 BE BOM", "UTF-16 LE BOM"]
enc_map = {
    "ANSI": "windows-1252",
    "UTF-8": "utf-8",
    "UTF-8-BOM": "utf-8-sig",
    "UTF-16 BE BOM": "utf-16-be",
    "UTF-16 LE BOM": "utf-16-le"
}
enc_var = StringVar(app, "UTF-8")
OptionMenu(app, enc_var, *enc_opts).grid(row=1, column=1, padx=10)

Button(app, text="Convertir", command=convert, width=20).grid(row=2, column=0, columnspan=3, pady=12)
status_label = Label(app, text="")   # barra de estado
status_label.grid(row=3, column=0, columnspan=3, pady=6)

app.mainloop()
