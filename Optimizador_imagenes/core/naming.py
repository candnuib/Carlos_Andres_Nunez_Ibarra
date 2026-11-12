import os
from datetime import datetime
from typing import List, Tuple

def generate_output_folder_name(prefix: str = "WebP_Optimizadas") -> str:
    """
    Genera el nombre de la carpeta con la fecha y hora actual.
    Ejemplo: WebP_Optimizadas_2026-11-09_10-05-30
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    clean_prefix = prefix.strip() if prefix.strip() else "WebP_Optimizadas"
    return f"{clean_prefix}_{timestamp}"

def format_filename(
    original_filepath: str,
    index: int,
    base_name: str = "",
    zero_padding: int = 3,
    start_index: int = 1,
    extension: str = ".webp"
) -> str:
    """
    Formatea el nombre de archivo destino según las reglas especificadas:
    - Si base_name tiene texto: se utiliza '{base_name}_{numero_con_ceros}{extension}'
    - Si base_name está vacío: se conserva el nombre original '{nombre_original}{extension}'
    """
    if not extension.startswith('.'):
        extension = f".{extension}"
        
    num = index + (start_index - 1)
    padded_num = str(num).zfill(max(1, zero_padding))
    
    clean_base = base_name.strip()
    if clean_base:
        filename = f"{clean_base}_{padded_num}{extension}"
    else:
        orig_stem = os.path.splitext(os.path.basename(original_filepath))[0]
        filename = f"{orig_stem}{extension}"
        
    return filename

def preview_filenames(
    base_name: str,
    zero_padding: int,
    start_index: int = 1,
    count: int = 3,
    sample_original: str = "foto_ejemplo.jpg"
) -> List[str]:
    """Genera una lista de previsualización de nombres."""
    samples = []
    for i in range(1, count + 1):
        samples.append(
            format_filename(
                original_filepath=sample_original,
                index=i,
                base_name=base_name,
                zero_padding=zero_padding,
                start_index=start_index
            )
        )
    return samples
