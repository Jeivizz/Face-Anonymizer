import customtkinter as ctk
from tkinter import filedialog
import os
from PIL import Image, ImageTk
import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import process_img as pimg

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class DropArea(ctk.CTkFrame):
    def __init__(self, master, on_file_selected=None, filetypes=None, **kwargs):
        super().__init__(
            master,
            fg_color=("gray90", "gray20"),
            border_width=2,
            border_color=("gray70", "gray40"),
            corner_radius=12,
            **kwargs
        )
        self.on_file_selected = on_file_selected
        self.filetypes = filetypes or [("All Files", "*.*")]
        self.filepath = None

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.icon_label = ctk.CTkLabel(self.content_frame, text="📁", font=ctk.CTkFont(size=40))
        self.icon_label.pack(pady=(30, 5))

        self.text_label = ctk.CTkLabel(
            self.content_frame,
            text="Click to Select an Image",
            font=ctk.CTkFont(size=13),
            text_color=("gray30", "gray70"),
        )
        self.text_label.pack(pady=(0, 30))

        for widget in (self, self.icon_label, self.text_label):
            widget.bind("<Button-1>", self._browse)
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)

    def _on_enter(self, event=None):
        self.configure(border_color=("#1f6aa5", "#3b8ed0"))

    def _on_leave(self, event=None):
        self.configure(border_color=("gray70", "gray40"))

    def _browse(self, event=None):
        path = filedialog.askopenfilename(filetypes=self.filetypes)
        if path:
            self.set_file(path)

    def set_file(self, path):
        self.filepath = path
        self.icon_label.configure(text="✅")
        self.text_label.configure(text=os.path.basename(path))
        if self.on_file_selected:
            self.on_file_selected(path)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Face Anonymizer")
        self.geometry("750x500")
        self.resizable(False, False)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Inicializa o Detector do MediaPipe do backend
        model_path = './blaze_face_full_range.tflite'
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceDetectorOptions(base_options=base_options)
        self.detector = vision.FaceDetector.create_from_options(options)

        self.processed_cv_img = None  # Guarda a imagem processada em memória (BGR do OpenCV)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="Mode", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.active = 1

        self.btn_image = ctk.CTkButton(self.sidebar_frame, text="Image", command=lambda: self.event_click(1))
        self.btn_image.grid(row=1, column=0, padx=20, pady=10)

        self.btn_video = ctk.CTkButton(self.sidebar_frame, text="Video", command=lambda: self.event_click(2))
        self.btn_video.grid(row=2, column=0, padx=20, pady=10)

        self.btn_webcam = ctk.CTkButton(self.sidebar_frame, text="Webcam", command=lambda: self.event_click(3))
        self.btn_webcam.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.sidebar_frame, values=["System", "Dark", "Light"], command=self.change_appearance
        )
        self.appearance_mode_menu.grid(row=5, column=0, padx=20, pady=20, sticky="s")
        self.appearance_mode_menu.set("System")

        # --- Área Principal (Conteúdo) ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(
            self.main_frame, text="Image Anonymizer", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w", pady=(0, 15))

        self.drop_area = None
        self.preview_label = None
        self.selected_path = None

        self.status_label = ctk.CTkLabel(
            self.main_frame, text="", font=ctk.CTkFont(size=12), text_color=("gray30", "gray70")
        )
        self.status_label.grid(row=2, column=0, sticky="w", pady=(1, 0))


        self.run_button = ctk.CTkButton(
            self.main_frame, text="Anonymize", state="disabled", command=self.run_anonymize
        )
        self.run_button.grid(row=3, column=0, sticky="ew", pady=(5, 5))


        self.save_button = ctk.CTkButton(
            self.main_frame, text="Save As...", state="disabled", fg_color="green", hover_color="darkgreen",
            command=self.save_processed_image
        )
        self.save_button.grid(row=4, column=0, sticky="ew", pady=(0, 5))

        self.show_drop_area(filetypes=[("Images", "*.jpg *.jpeg *.png")])

    def change_appearance(self, new_mode: str):
        ctk.set_appearance_mode(new_mode)

    def event_click(self, value):
        self.active = value
        self.selected_path = None
        self.processed_cv_img = None
        self.status_label.configure(text="")
        self.save_button.configure(state="disabled")

        if self.active == 1:
            self.title_label.configure(text="Image Anonymizer")
            self.show_drop_area(filetypes=[("Images", "*.jpg *.jpeg *.png")])
            self.run_button.configure(state="disabled", text="Anonymize")
        elif self.active == 2:
            self.title_label.configure(text="Video Anonymizer")
            self.show_drop_area(filetypes=[("Videos", "*.mp4 *.avi *.mov")])
            self.run_button.configure(state="disabled", text="Anonymize")
        elif self.active == 3:
            self.title_label.configure(text="Webcam Anonymizer")
            if self.drop_area is not None:
                self.drop_area.destroy()
                self.drop_area = None
            self.run_button.configure(text="Start Webcam", state="normal")
            return

    def show_drop_area(self, filetypes):
        if self.drop_area is not None:
            self.drop_area.destroy()
        if self.preview_label is not None:
            self.preview_label.destroy()

        self.drop_area = DropArea(
            self.main_frame, on_file_selected=self.handle_file, filetypes=filetypes
        )
        self.drop_area.grid(row=1, column=0, sticky="nsew")

    def handle_file(self, path):
        self.selected_path = path
        self.run_button.configure(state="normal")
        self.status_label.configure(text=f"Ready to Process: {os.path.basename(path)}")

        # Mostra a thumbnail da imagem selecionada
        self.show_image_preview(path)

    def show_image_preview(self, path_or_cv_img):
        if self.drop_area is not None:
            self.drop_area.destroy()
            self.drop_area = None

        if self.preview_label is not None:
            self.preview_label.destroy()

        if isinstance(path_or_cv_img, str):
            pil_img = Image.open(path_or_cv_img)
        else:
            rgb_img = cv2.cvtColor(path_or_cv_img, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_img)

        pil_img.thumbnail((400, 300))

        photo_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size)

        self.preview_label = ctk.CTkLabel(self.main_frame, text="", image=photo_img)
        self.preview_label.grid(row=1, column=0, sticky="nsew")

    def run_anonymize(self):
        if self.active == 3:
            self.status_label.configure(text="Starting webcam...")
            return

        if not self.selected_path:
            return

        self.run_button.configure(state="disabled", text="Processing...")
        self.status_label.configure(text="Processing...")
        self.update_idletasks()

        try:
            img = cv2.imread(self.selected_path)
            self.processed_cv_img = pimg.process_img(img, self.detector)

            self.show_image_preview(self.processed_cv_img)

            self.status_label.configure(text="Anonymizing Done! Ready to save.")
            self.save_button.configure(state="normal")
        except Exception as e:
            self.status_label.configure(text=f"❌ Error: {e}")
        finally:
            self.run_button.configure(state="normal", text="Anonymize")

    def save_processed_image(self):
        if self.processed_cv_img is None:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG file", "*.png"), ("JPEG file", "*.jpg"), ("All Files", "*.*")],
            initialfile="blurred-image.png"
        )

        if file_path:
            try:
                cv2.imwrite(file_path, self.processed_cv_img)
                self.status_label.configure(text=f"Saved successfully to: {os.path.basename(file_path)}")
            except Exception as e:
                self.status_label.configure(text=f"❌ Error saving: {e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()