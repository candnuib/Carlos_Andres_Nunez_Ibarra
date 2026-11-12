"""
Interfaz gráfica de usuario moderna para la optimización de imágenes a WebP.
"""

import os
import sys
import threading
import subprocess
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Dict, Optional
from PIL import Image

from core.converter import ConversionConfig, process_batch, FileResult, SUPPORTED_EXTENSIONS
from core.naming import preview_filenames

def format_size(bytes_size: int) -> str:
    """Formatea bytes a KB o MB legibles."""
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024 * 1024:
        return f"{bytes_size / 1024:.1f} KB"
    else:
        return f"{bytes_size / (1024 * 1024):.2f} MB"

def open_folder_in_explorer(folder_path: str):
    """Abre la carpeta en el explorador de archivos según el sistema operativo."""
    try:
        if sys.platform.startswith("linux"):
            subprocess.run(["xdg-open", folder_path], check=False)
        elif sys.platform == "darwin":
            subprocess.run(["open", folder_path], check=False)
        elif sys.platform in ("win32", "cygwin"):
            os.startfile(folder_path)
    except Exception as e:
        print(f"Error al abrir carpeta: {e}")

class ModernImageOptimizerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Optimizador de Imágenes WebP para Web")
        self.root.geometry("960x780")
        self.root.minsize(860, 680)

        # Estado
        self.selected_files: List[str] = []
        self.is_processing = False
        self.custom_output_dir: Optional[str] = None

        # Configurar Estilos ttk
        self.setup_styles()

        # Construir Interfaz
        self.build_ui()

        # Previsualizar nombres por defecto
        self.update_name_preview()

    def setup_styles(self):
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        # Paleta de colores moderna
        self.color_bg = "#f8fafc"
        self.color_surface = "#ffffff"
        self.color_primary = "#2563eb"       # Azul profesional
        self.color_primary_hover = "#1d4ed8"
        self.color_accent = "#10b981"        # Verde esmeralda para acción principal
        self.color_text = "#0f172a"
        self.color_text_muted = "#64748b"
        self.color_border = "#cbd5e1"

        self.root.configure(bg=self.color_bg)

        self.style.configure(".", font=("Helvetica", 10), background=self.color_bg, foreground=self.color_text)
        
        # Encabezados y Labels
        self.style.configure("Title.TLabel", font=("Helvetica", 16, "bold"), foreground="#1e293b", background=self.color_bg)
        self.style.configure("Subtitle.TLabel", font=("Helvetica", 10), foreground=self.color_text_muted, background=self.color_bg)
        self.style.configure("Section.TLabelframe", background=self.color_surface, relief="solid", borderwidth=1)
        self.style.configure("Section.TLabelframe.Label", font=("Helvetica", 10, "bold"), foreground="#334155", background=self.color_surface)
        self.style.configure("Surface.TFrame", background=self.color_surface)
        
        # Botones
        self.style.configure("Primary.TButton", font=("Helvetica", 10, "bold"), foreground="#ffffff", background=self.color_primary, padding=(12, 6))
        self.style.map("Primary.TButton", background=[("active", self.color_primary_hover), ("disabled", "#94a3b8")])

        self.style.configure("Action.TButton", font=("Helvetica", 11, "bold"), foreground="#ffffff", background=self.color_accent, padding=(14, 8))
        self.style.map("Action.TButton", background=[("active", "#059669"), ("disabled", "#94a3b8")])

        self.style.configure("Secondary.TButton", font=("Helvetica", 9), padding=(8, 4))

        # Treeview (Tabla)
        self.style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", foreground=self.color_text, rowheight=26, bordercolor=self.color_border)
        self.style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#f1f5f9", foreground="#334155")
        self.style.map("Treeview", background=[("selected", "#dbeafe")], foreground=[("selected", "#1e3a8a")])

        # Progressbar
        self.style.configure("TProgressbar", thickness=14, troughcolor="#e2e8f0", background=self.color_primary)

    def build_ui(self):
        # Contenedor principal con margen
        main_frame = ttk.Frame(self.root, padding="16 12 16 12")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. HEADER
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        title_lbl = ttk.Label(header_frame, text="⚡ Optimizador de Imágenes WebP", style="Title.TLabel")
        title_lbl.pack(anchor=tk.W)
        subtitle_lbl = ttk.Label(
            header_frame,
            text="Convierte y comprime imágenes para sitios web manteniendo alta calidad visual, nombres secuenciales y carpetas fechadas.",
            style="Subtitle.TLabel"
        )
        subtitle_lbl.pack(anchor=tk.W, pady=(2, 0))

        # 2. CONTENIDO PRINCIPAL (Dividido en dos columnas: Izq = Archivos, Der = Configuración)
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # --- PANEL IZQUIERDO: SELECCIÓN DE ARCHIVOS ---
        left_frame = ttk.Frame(paned, padding=(0, 0, 8, 0))
        paned.add(left_frame, weight=3)

        files_lf = ttk.LabelFrame(left_frame, text=" 📂 Imágenes Seleccionadas ", style="Section.TLabelframe", padding=10)
        files_lf.pack(fill=tk.BOTH, expand=True)

        # Botones de gestión de archivos
        btn_bar = ttk.Frame(files_lf, style="Surface.TFrame")
        btn_bar.pack(fill=tk.X, pady=(0, 8))

        btn_add_files = ttk.Button(btn_bar, text="➕ Agregar Archivos", style="Primary.TButton", command=self.add_files)
        btn_add_files.pack(side=tk.LEFT, padx=(0, 6))

        btn_add_dir = ttk.Button(btn_bar, text="📁 Agregar Carpeta", style="Secondary.TButton", command=self.add_directory)
        btn_add_dir.pack(side=tk.LEFT, padx=(0, 6))

        btn_clear = ttk.Button(btn_bar, text="🗑️ Limpiar", style="Secondary.TButton", command=self.clear_files)
        btn_clear.pack(side=tk.RIGHT)

        # Tabla de archivos seleccionados
        tree_scroll = ttk.Scrollbar(files_lf, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(
            files_lf,
            columns=("name", "size", "dims", "status"),
            show="headings",
            yscrollcommand=tree_scroll.set,
            selectmode="extended"
        )
        tree_scroll.config(command=self.tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree.heading("name", text="Archivo")
        self.tree.heading("size", text="Tamaño")
        self.tree.heading("dims", text="Resolución")
        self.tree.heading("status", text="Estado")

        self.tree.column("name", width=220, anchor=tk.W)
        self.tree.column("size", width=80, anchor=tk.CENTER)
        self.tree.column("dims", width=95, anchor=tk.CENTER)
        self.tree.column("status", width=90, anchor=tk.CENTER)

        # Barra de resumen inferior izquierda
        self.summary_lbl = ttk.Label(left_frame, text="0 imágenes seleccionadas (0 B)", style="Subtitle.TLabel")
        self.summary_lbl.pack(anchor=tk.W, pady=(4, 0))

        # --- PANEL DERECHO: OPCIONES DE OPTIMIZACIÓN Y NOMBRES ---
        right_frame = ttk.Frame(paned, padding=(8, 0, 0, 0))
        paned.add(right_frame, weight=2)

        # 2.A Configuración de Nombres y Ceros
        name_lf = ttk.LabelFrame(right_frame, text=" 🏷️ Nomenclatura y Metadatos ", style="Section.TLabelframe", padding=10)
        name_lf.pack(fill=tk.X, pady=(0, 10))

        # Nombre Base
        row_name = ttk.Frame(name_lf, style="Surface.TFrame")
        row_name.pack(fill=tk.X, pady=(0, 6))
        ttk.Label(row_name, text="Nombre fijo:", style="Subtitle.TLabel").pack(anchor=tk.W)
        self.entry_basename = ttk.Entry(row_name, font=("Helvetica", 10))
        self.entry_basename.pack(fill=tk.X, pady=(2, 0))
        self.entry_basename.insert(0, "producto")
        self.entry_basename.bind("<KeyRelease>", lambda e: self.update_name_preview())

        note_name = ttk.Label(row_name, text="*(Deja en blanco para conservar el nombre original)*", font=("Helvetica", 8), foreground="#94a3b8", background=self.color_surface)
        note_name.pack(anchor=tk.W)

        # Ceros de relleno (Padding) e Inicio
        num_row = ttk.Frame(name_lf, style="Surface.TFrame")
        num_row.pack(fill=tk.X, pady=(4, 6))

        pad_col = ttk.Frame(num_row, style="Surface.TFrame")
        pad_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        ttk.Label(pad_col, text="Dígitos con ceros:", style="Subtitle.TLabel").pack(anchor=tk.W)
        self.spin_padding = ttk.Spinbox(pad_col, from_=1, to=8, width=5, command=self.update_name_preview)
        self.spin_padding.set(3)
        self.spin_padding.pack(anchor=tk.W, pady=(2, 0))
        self.spin_padding.bind("<KeyRelease>", lambda e: self.update_name_preview())

        start_col = ttk.Frame(num_row, style="Surface.TFrame")
        start_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))
        ttk.Label(start_col, text="Número inicial:", style="Subtitle.TLabel").pack(anchor=tk.W)
        self.spin_start = ttk.Spinbox(start_col, from_=0, to=99999, width=6, command=self.update_name_preview)
        self.spin_start.set(1)
        self.spin_start.pack(anchor=tk.W, pady=(2, 0))
        self.spin_start.bind("<KeyRelease>", lambda e: self.update_name_preview())

        # Previsualización del Nombre
        preview_box = ttk.Frame(name_lf, style="Surface.TFrame")
        preview_box.pack(fill=tk.X, pady=(4, 0))
        ttk.Label(preview_box, text="Vista previa de nombres:", font=("Helvetica", 9, "bold"), foreground="#475569", background=self.color_surface).pack(anchor=tk.W)
        self.lbl_preview = ttk.Label(preview_box, text="", font=("Monospace", 9), foreground="#0284c7", background="#f0f9ff", relief="solid", borderwidth=1, padding=(6, 4))
        self.lbl_preview.pack(fill=tk.X, pady=(3, 0))

        # 2.B Configuración Web y Compresión WebP
        webp_lf = ttk.LabelFrame(right_frame, text=" 🌐 Calidad y Peso Web ", style="Section.TLabelframe", padding=10)
        webp_lf.pack(fill=tk.X, pady=(0, 10))

        # Calidad Slider
        qual_top = ttk.Frame(webp_lf, style="Surface.TFrame")
        qual_top.pack(fill=tk.X)
        ttk.Label(qual_top, text="Calidad WebP:", style="Subtitle.TLabel").pack(side=tk.LEFT)
        self.lbl_quality_val = ttk.Label(qual_top, text="85%", font=("Helvetica", 10, "bold"), foreground=self.color_primary, background=self.color_surface)
        self.lbl_quality_val.pack(side=tk.RIGHT)

        self.scale_quality = ttk.Scale(webp_lf, from_=1, to=100, orient=tk.HORIZONTAL, value=85, command=self.on_quality_change)
        self.scale_quality.pack(fill=tk.X, pady=(2, 6))

        # Checkbox Sin Pérdidas
        self.var_lossless = tk.BooleanVar(value=False)
        self.chk_lossless = ttk.Checkbutton(webp_lf, text="Modo Sin Pérdidas (Lossless)", variable=self.var_lossless, command=self.on_lossless_toggle)
        self.chk_lossless.pack(anchor=tk.W, pady=(0, 4))

        # Redimensión opcional
        self.var_resize = tk.BooleanVar(value=False)
        self.chk_resize = ttk.Checkbutton(webp_lf, text="Redimensionar tamaño máximo para web", variable=self.var_resize, command=self.on_resize_toggle)
        self.chk_resize.pack(anchor=tk.W, pady=(2, 4))

        self.frame_dims = ttk.Frame(webp_lf, style="Surface.TFrame")
        self.frame_dims.pack(fill=tk.X, pady=(0, 4))

        ttk.Label(self.frame_dims, text="Ancho máx:", font=("Helvetica", 9), background=self.color_surface).pack(side=tk.LEFT)
        self.entry_max_w = ttk.Entry(self.frame_dims, width=6)
        self.entry_max_w.insert(0, "1920")
        self.entry_max_w.pack(side=tk.LEFT, padx=(3, 10))

        ttk.Label(self.frame_dims, text="Alto máx:", font=("Helvetica", 9), background=self.color_surface).pack(side=tk.LEFT)
        self.entry_max_h = ttk.Entry(self.frame_dims, width=6)
        self.entry_max_h.insert(0, "1080")
        self.entry_max_h.pack(side=tk.LEFT, padx=(3, 0))

        self.set_resize_fields_state(False)

        # Checkbox Eliminar metadatos
        self.var_strip_exif = tk.BooleanVar(value=True)
        self.chk_exif = ttk.Checkbutton(
            webp_lf,
            text="Limpiar metadatos EXIF / GPS (Ahorra peso web)",
            variable=self.var_strip_exif
        )
        self.chk_exif.pack(anchor=tk.W, pady=(4, 0))

        # 2.C Carpeta con Fecha y Destino
        dest_lf = ttk.LabelFrame(right_frame, text=" 📅 Carpeta con Fecha ", style="Section.TLabelframe", padding=10)
        dest_lf.pack(fill=tk.X, pady=(0, 10))

        row_pref = ttk.Frame(dest_lf, style="Surface.TFrame")
        row_pref.pack(fill=tk.X, pady=(0, 4))
        ttk.Label(row_pref, text="Prefijo de carpeta:", style="Subtitle.TLabel").pack(anchor=tk.W)
        self.entry_folder_prefix = ttk.Entry(row_pref)
        self.entry_folder_prefix.insert(0, "WebP_Optimizadas")
        self.entry_folder_prefix.pack(fill=tk.X, pady=(2, 0))

        # Destino personalizado
        row_dest = ttk.Frame(dest_lf, style="Surface.TFrame")
        row_dest.pack(fill=tk.X, pady=(4, 0))
        self.lbl_target_path = ttk.Label(row_dest, text="Destino: Misma carpeta de las imágenes", font=("Helvetica", 8), foreground=self.color_text_muted, background=self.color_surface)
        self.lbl_target_path.pack(side=tk.LEFT, fill=tk.X, expand=True)

        btn_choose_dest = ttk.Button(row_dest, text="Cambiar...", style="Secondary.TButton", command=self.choose_custom_dest)
        btn_choose_dest.pack(side=tk.RIGHT)

        # 3. SECCIÓN INFERIOR: ACCIÓN, PROGRESO Y RESULTADOS
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(5, 0))

        # Barra de progreso y texto de estado
        self.progress_bar = ttk.Progressbar(bottom_frame, orient=tk.HORIZONTAL, mode="determinate", style="TProgressbar")
        self.progress_bar.pack(fill=tk.X, pady=(0, 6))

        status_row = ttk.Frame(bottom_frame)
        status_row.pack(fill=tk.X, pady=(0, 8))

        self.lbl_status = ttk.Label(status_row, text="Listo. Selecciona imágenes para comenzar.", font=("Helvetica", 9, "bold"), foreground="#475569")
        self.lbl_status.pack(side=tk.LEFT)

        # Botón Principal de Conversión
        self.btn_convert = ttk.Button(
            bottom_frame,
            text="🚀 OPTIMIZAR Y GENERAR PAQUETE CON FECHA",
            style="Action.TButton",
            command=self.start_conversion_thread
        )
        self.btn_convert.pack(fill=tk.X, ipady=4)

    # --- CONTROLADORES DE EVENTOS ---

    def on_quality_change(self, val):
        q = int(float(val))
        self.lbl_quality_val.config(text=f"{q}%")

    def on_lossless_toggle(self):
        if self.var_lossless.get():
            self.scale_quality.state(["disabled"])
            self.lbl_quality_val.config(text="100% (Sin pérdidas)", foreground=self.color_accent)
        else:
            self.scale_quality.state(["!disabled"])
            q = int(self.scale_quality.get())
            self.lbl_quality_val.config(text=f"{q}%", foreground=self.color_primary)

    def on_resize_toggle(self):
        self.set_resize_fields_state(self.var_resize.get())

    def set_resize_fields_state(self, enabled: bool):
        state = ["!disabled"] if enabled else ["disabled"]
        self.entry_max_w.state(state)
        self.entry_max_h.state(state)

    def update_name_preview(self):
        base = self.entry_basename.get().strip()
        try:
            padding = int(self.spin_padding.get())
        except ValueError:
            padding = 3
        try:
            start = int(self.spin_start.get())
        except ValueError:
            start = 1

        previews = preview_filenames(base, padding, start, count=2)
        if base:
            text = f"1º: {previews[0]}  |  2º: {previews[1]}"
        else:
            text = "Conserva nombre original: [nombre_original].webp"
        self.lbl_preview.config(text=text)

    def choose_custom_dest(self):
        folder = filedialog.askdirectory(title="Seleccionar carpeta de destino")
        if folder:
            self.custom_output_dir = folder
            folder_short = folder if len(folder) < 35 else f"...{folder[-32:]}"
            self.lbl_target_path.config(text=f"Destino: {folder_short}")

    def add_files(self):
        types = [
            ("Imágenes soportadas", "*.jpg *.jpeg *.png *.webp *.bmp *.tiff *.tif *.gif *.jfif"),
            ("Todos los archivos", "*.*")
        ]
        files = filedialog.askopenfilenames(title="Seleccionar imágenes", filetypes=types)
        if files:
            self.register_files(files)

    def add_directory(self):
        folder = filedialog.askdirectory(title="Seleccionar carpeta con imágenes")
        if folder:
            found = []
            for root_dir, _, filenames in os.walk(folder):
                for f in sorted(filenames):
                    ext = os.path.splitext(f)[1].lower()
                    if ext in SUPPORTED_EXTENSIONS:
                        found.append(os.path.join(root_dir, f))
            if found:
                self.register_files(found)
            else:
                messagebox.showinfo("Sin imágenes", "No se encontraron imágenes compatibles en la carpeta seleccionada.")

    def register_files(self, filepaths):
        existing_set = set(self.selected_files)
        total_size = 0
        added_count = 0

        for fp in filepaths:
            fp_norm = os.path.normpath(fp)
            if fp_norm not in existing_set and os.path.isfile(fp_norm):
                self.selected_files.append(fp_norm)
                existing_set.add(fp_norm)
                added_count += 1

                # Obtener detalles para la tabla
                size_str = "-"
                dims_str = "-"
                try:
                    size_b = os.path.getsize(fp_norm)
                    size_str = format_size(size_b)
                    with Image.open(fp_norm) as img:
                        dims_str = f"{img.width}x{img.height}"
                except Exception:
                    pass

                self.tree.insert("", tk.END, iid=fp_norm, values=(
                    os.path.basename(fp_norm),
                    size_str,
                    dims_str,
                    "Pendiente"
                ))

        self.update_summary()

    def clear_files(self):
        self.selected_files.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.update_summary()
        self.progress_bar["value"] = 0
        self.lbl_status.config(text="Listo. Selecciona imágenes para comenzar.")

    def update_summary(self):
        count = len(self.selected_files)
        total_bytes = 0
        for fp in self.selected_files:
            try:
                total_bytes += os.path.getsize(fp)
            except Exception:
                pass
        self.summary_lbl.config(text=f"{count} imágenes seleccionadas ({format_size(total_bytes)})")

    # --- PROCESAMIENTO MULTIHILO ---

    def start_conversion_thread(self):
        if not self.selected_files:
            messagebox.showwarning("Atención", "Por favor selecciona al menos una imagen para optimizar.")
            return

        if self.is_processing:
            return

        # Validaciones de configuración
        base_name = self.entry_basename.get().strip()
        try:
            padding = int(self.spin_padding.get())
        except ValueError:
            padding = 3
        try:
            start_index = int(self.spin_start.get())
        except ValueError:
            start_index = 1

        max_w = None
        max_h = None
        if self.var_resize.get():
            try:
                max_w = int(self.entry_max_w.get().strip()) if self.entry_max_w.get().strip() else None
            except ValueError:
                pass
            try:
                max_h = int(self.entry_max_h.get().strip()) if self.entry_max_h.get().strip() else None
            except ValueError:
                pass

        prefix = self.entry_folder_prefix.get().strip() or "WebP_Optimizadas"

        config = ConversionConfig(
            quality=int(self.scale_quality.get()),
            lossless=self.var_lossless.get(),
            base_name=base_name,
            zero_padding=padding,
            start_index=start_index,
            max_width=max_w,
            max_height=max_h,
            strip_metadata=self.var_strip_exif.get(),
            output_folder_prefix=prefix,
            target_directory=self.custom_output_dir
        )

        self.is_processing = True
        self.btn_convert.state(["disabled"])
        self.progress_bar["maximum"] = len(self.selected_files)
        self.progress_bar["value"] = 0

        # Reset estados en la tabla
        for fp in self.selected_files:
            if self.tree.exists(fp):
                vals = list(self.tree.item(fp, "values"))
                vals[3] = "En cola..."
                self.tree.item(fp, values=vals)

        # Iniciar hilo de trabajo
        worker = threading.Thread(target=self._run_batch, args=(config,), daemon=True)
        worker.start()

    def _run_batch(self, config: ConversionConfig):
        total_files = len(self.selected_files)

        def progress_callback(current: int, total: int, result: FileResult):
            self.root.after(0, self._update_item_progress, current, total, result)

        try:
            out_dir, results = process_batch(
                file_list=self.selected_files,
                config=config,
                progress_callback=progress_callback
            )
            self.root.after(0, self._on_batch_complete, out_dir, results)
        except Exception as e:
            self.root.after(0, self._on_batch_error, str(e))

    def _update_item_progress(self, current: int, total: int, result: FileResult):
        self.progress_bar["value"] = current
        filename = os.path.basename(result.original_path)
        
        if result.success:
            status_text = f"✓ {result.savings_percent:.0f}% menos"
            self.lbl_status.config(
                text=f"Procesando ({current}/{total}): {filename} -> {format_size(result.output_size)}"
            )
        else:
            status_text = "❌ Error"
            self.lbl_status.config(text=f"Error en ({current}/{total}): {filename}")

        if self.tree.exists(result.original_path):
            vals = list(self.tree.item(result.original_path, "values"))
            vals[3] = status_text
            self.tree.item(result.original_path, values=vals)

    def _on_batch_complete(self, out_dir: str, results: List[FileResult]):
        self.is_processing = False
        self.btn_convert.state(["!disabled"])

        success_count = sum(1 for r in results if r.success)
        total_orig = sum(r.original_size for r in results if r.success)
        total_final = sum(r.output_size for r in results if r.success)
        savings_bytes = max(0, total_orig - total_final)
        savings_pct = (savings_bytes / total_orig * 100.0) if total_orig > 0 else 0.0

        self.lbl_status.config(
            text=f"¡Completado! {success_count} imágenes optimizadas. Ahorro total: {savings_pct:.1f}%"
        )

        # Mostrar ventana emergente con resumen detallado y botón para abrir carpeta
        self.show_completion_dialog(out_dir, success_count, len(results), total_orig, total_final, savings_pct)

    def _on_batch_error(self, err_msg: str):
        self.is_processing = False
        self.btn_convert.state(["!disabled"])
        self.lbl_status.config(text=f"Error: {err_msg}")
        messagebox.showerror("Error en el procesamiento", f"Ocurrió un error al procesar las imágenes:\n{err_msg}")

    def show_completion_dialog(self, out_dir: str, success: int, total: int, orig_sz: int, final_sz: int, savings_pct: float):
        dlg = tk.Toplevel(self.root)
        dlg.title("¡Optimización Completada!")
        dlg.geometry("520x340")
        dlg.resizable(False, False)
        dlg.transient(self.root)
        dlg.grab_set()

        content = ttk.Frame(dlg, padding=20)
        content.pack(fill=tk.BOTH, expand=True)

        ttk.Label(content, text="🎉 ¡Imágenes Optimizadas con Éxito!", font=("Helvetica", 14, "bold"), foreground="#059669").pack(pady=(0, 10))

        # Cuadro de estadísticas
        stats_frame = ttk.Frame(content, relief="solid", borderwidth=1, padding=12)
        stats_frame.pack(fill=tk.X, pady=(0, 14))

        ttk.Label(stats_frame, text=f"• Archivos procesados: {success} de {total}", font=("Helvetica", 10)).pack(anchor=tk.W, pady=2)
        ttk.Label(stats_frame, text=f"• Peso original total: {format_size(orig_sz)}", font=("Helvetica", 10)).pack(anchor=tk.W, pady=2)
        ttk.Label(stats_frame, text=f"• Peso final WebP: {format_size(final_sz)}", font=("Helvetica", 10, "bold"), foreground="#2563eb").pack(anchor=tk.W, pady=2)
        ttk.Label(stats_frame, text=f"• Espacio ahorrado para web: {savings_pct:.1f}% ({format_size(orig_sz - final_sz)})", font=("Helvetica", 10, "bold"), foreground="#10b981").pack(anchor=tk.W, pady=2)

        folder_name = os.path.basename(out_dir)
        ttk.Label(content, text=f"📁 Carpeta generada:\n{folder_name}", font=("Monospace", 9), foreground="#334155").pack(pady=(0, 14))

        btn_row = ttk.Frame(content)
        btn_row.pack(fill=tk.X)

        btn_open = ttk.Button(btn_row, text="📂 Abrir Carpeta de Resultados", style="Action.TButton", command=lambda: open_folder_in_explorer(out_dir))
        btn_open.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

        btn_close = ttk.Button(btn_row, text="Cerrar", style="Secondary.TButton", command=dlg.destroy)
        btn_close.pack(side=tk.RIGHT, padx=(6, 0))


def start_app():
    root = tk.Tk()
    app = ModernImageOptimizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    start_app()
