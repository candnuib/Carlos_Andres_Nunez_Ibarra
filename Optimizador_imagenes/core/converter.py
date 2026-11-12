import os
from typing import List, Callable, Optional, Dict, Any, Tuple
from dataclasses import dataclass
from PIL import Image, ImageOps
from core.naming import generate_output_folder_name, format_filename

SUPPORTED_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif", ".gif", ".ico", ".jfif"
}

@dataclass
class ConversionConfig:
    quality: int = 85
    lossless: bool = False
    base_name: str = ""
    zero_padding: int = 3
    start_index: int = 1
    max_width: Optional[int] = None
    max_height: Optional[int] = None
    preserve_aspect_ratio: bool = True
    strip_metadata: bool = True
    output_folder_prefix: str = "WebP_Optimizadas"
    target_directory: Optional[str] = None  # None = mismo directorio que las imágenes

@dataclass
class FileResult:
    original_path: str
    output_path: str
    original_size: int
    output_size: int
    width: int
    height: int
    success: bool
    error_message: Optional[str] = None

    @property
    def saved_bytes(self) -> int:
        return max(0, self.original_size - self.output_size)

    @property
    def savings_percent(self) -> float:
        if self.original_size <= 0:
            return 0.0
        return max(0.0, ((self.original_size - self.output_size) / self.original_size) * 100.0)

def prepare_image_for_webp(img: Image.Image) -> Image.Image:
    """
    Asegura que el modo de color de la imagen sea compatible con WebP,
    preservando transparencia si existe y corrigiendo rotaciones EXIF.
    """
    # Corregir orientación basada en EXIF si existe
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    # Manejo de modos de color
    if img.mode in ("RGBA", "LA"):
        return img.convert("RGBA")
    elif img.mode == "P":
        # Imágenes con paleta (por ejemplo PNG de 8 bits o GIF)
        if "transparency" in img.info:
            return img.convert("RGBA")
        else:
            return img.convert("RGB")
    elif img.mode in ("CMYK", "YCbCr"):
        return img.convert("RGB")
    elif img.mode == "1":
        # Monocromo de 1 bit
        return img.convert("L")
    elif img.mode in ("RGB", "L"):
        return img
    else:
        # Cualquier otro modo exótico
        return img.convert("RGB")

def resize_image_if_needed(
    img: Image.Image,
    max_w: Optional[int],
    max_h: Optional[int]
) -> Image.Image:
    """
    Redimensiona la imagen si excede el ancho o alto máximo especificado,
    manteniendo la proporción y utilizando interpolación Lanczos de alta calidad.
    Nunca amplía imágenes pequeñas.
    """
    if not max_w and not max_h:
        return img

    orig_w, orig_h = img.size
    target_w = max_w if max_w and max_w > 0 else orig_w
    target_h = max_h if max_h and max_h > 0 else orig_h

    # Solo reducir si es más grande
    if orig_w <= target_w and orig_h <= target_h:
        return img

    ratio = min(target_w / orig_w, target_h / orig_h)
    new_w = max(1, int(orig_w * ratio))
    new_h = max(1, int(orig_h * ratio))

    return img.resize((new_w, new_h), Image.Resampling.LANCZOS)

def convert_single_image(
    source_path: str,
    output_path: str,
    config: ConversionConfig
) -> FileResult:
    """
    Convierte una sola imagen a formato WebP optimizado para web.
    """
    original_size = os.path.getsize(source_path)
    
    try:
        with Image.open(source_path) as raw_img:
            # Procesar modo de color y rotación
            img = prepare_image_for_webp(raw_img)
            
            # Redimensionar si se especificó
            img = resize_image_if_needed(img, config.max_width, config.max_height)
            w, h = img.size

            # Parámetros de guardado para WebP
            save_kwargs: Dict[str, Any] = {
                "format": "WEBP",
                "method": 6,  # Método de compresión más avanzado y óptimo
            }

            if config.lossless:
                save_kwargs["lossless"] = True
            else:
                save_kwargs["lossless"] = False
                save_kwargs["quality"] = max(1, min(100, config.quality))

            # Preservar o eliminar metadatos EXIF
            if not config.strip_metadata and "exif" in raw_img.info:
                save_kwargs["exif"] = raw_img.info["exif"]

            img.save(output_path, **save_kwargs)

        output_size = os.path.getsize(output_path)
        return FileResult(
            original_path=source_path,
            output_path=output_path,
            original_size=original_size,
            output_size=output_size,
            width=w,
            height=h,
            success=True
        )
    except Exception as e:
        return FileResult(
            original_path=source_path,
            output_path=output_path,
            original_size=original_size,
            output_size=0,
            width=0,
            height=0,
            success=False,
            error_message=str(e)
        )

def process_batch(
    file_list: List[str],
    config: ConversionConfig,
    progress_callback: Optional[Callable[[int, int, FileResult], None]] = None
) -> Tuple[str, List[FileResult]]:
    """
    Procesa un lote de imágenes creando la carpeta fechada y convirtiendo cada archivo.
    Retorna la ruta de la carpeta creada y la lista de resultados.
    """
    if not file_list:
        raise ValueError("No se proporcionaron imágenes para procesar.")

    # Determinar la carpeta base de destino
    if config.target_directory and os.path.isdir(config.target_directory):
        base_dir = config.target_directory
    else:
        # Por defecto, en la misma carpeta que la primera imagen
        base_dir = os.path.dirname(os.path.abspath(file_list[0]))

    folder_name = generate_output_folder_name(config.output_folder_prefix)
    output_dir = os.path.join(base_dir, folder_name)
    os.makedirs(output_dir, exist_ok=True)

    results: List[FileResult] = []
    total = len(file_list)

    for idx, filepath in enumerate(file_list, start=1):
        filename = format_filename(
            original_filepath=filepath,
            index=idx,
            base_name=config.base_name,
            zero_padding=config.zero_padding,
            start_index=config.start_index,
            extension=".webp"
        )
        out_filepath = os.path.join(output_dir, filename)

        result = convert_single_image(filepath, out_filepath, config)
        results.append(result)

        if progress_callback:
            progress_callback(idx, total, result)

    return output_dir, results
