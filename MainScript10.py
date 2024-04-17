import customtkinter
import pygame
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QDialogButtonBox, \
                QProgressBar, QSlider, \
                QDial, QPushButton
from PySide6.QtGui import QPainter, QPixmap, QBitmap
from PySide6.QtCore import Qt


pygame.init()

# Get the screen's current resolution
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

# Create a full-screen window
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("SVG Animation")

background_color = (0, 0, 0)

def load_and_smoothly_scale_image(path, target_width, target_height):
    image = pygame.image.load(path)
    width, height = image.get_size()
    scaling_factor = min(target_width / width, target_height / height)
    new_size = (int(width * scaling_factor), int(height * scaling_factor))
    scaled_image = pygame.transform.smoothscale(image, new_size)
    return scaled_image

# Adjust the scaling factor based on your full-screen resolution
logo_5_path = "C:/Users/Frogs/Downloads/Color logo with background (5).svg"
logo_6_path = "C:/Users/Frogs/Downloads/Color logo with background (6).svg"
logo_5 = load_and_smoothly_scale_image(logo_5_path, screen_width * 3.5 // 4, screen_height * 3.5 // 4)
logo_6 = load_and_smoothly_scale_image(logo_6_path, screen_width * 3.5 // 4, screen_height * 3.5 // 4)

logo_5_pos = [-logo_5.get_width(), (screen_height - logo_5.get_height()) // 15]
logo_6_pos = [screen_width, (screen_height + logo_5.get_height()) // 2.9]

logo_5_target_x = (screen_width - logo_5.get_width()) // 2
logo_6_target_x = (screen_width - logo_6.get_width()) // 2
speed = 5

animation_complete = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if logo_5_pos[0] < logo_5_target_x:
        logo_5_pos[0] += speed
    else:
        logo_5_pos[0] = logo_5_target_x

    if logo_6_pos[0] > logo_6_target_x:
        logo_6_pos[0] -= speed
    else:
        logo_6_pos[0] = logo_6_target_x

    if logo_5_pos[0] == logo_5_target_x and logo_6_pos[0] == logo_6_target_x and not animation_complete:
        animation_complete = True
        pygame.time.wait(3000)
        break

    screen.fill(background_color)
    screen.blit(logo_5, logo_5_pos)
    screen.blit(logo_6, logo_6_pos)
    pygame.display.flip()

pygame.quit()

def start_tkinter_app():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    app = ctk.CTk()
    app.overrideredirect(True)
    app.geometry(f"{app.winfo_screenwidth()}x{app.winfo_screenheight()}+0+0")
    app.title("RetinaSpy")

    current_active_entry = None

    def login():
        username = "retinaspy"
        password = "12345"

        if user_entry.get() == username and user_pass.get() == password:
            messagebox.showinfo(title="Login Successful", message="You have logged in Successfully")
            app.destroy()
            display_app = DisplayWindow()
            display_app.mainloop()
        elif user_entry.get() == username and user_pass.get() != password:
            messagebox.showwarning(title='Wrong password', message='Please check your password')
        elif user_entry.get() != username and user_pass.get() == password:
            messagebox.showwarning(title='Wrong username', message='Please check your username')
        else:
            messagebox.showerror(title="Login Failed", message="Invalid Username and password")

    def set_current_active_entry(entry_widget):
        nonlocal current_active_entry
        current_active_entry = entry_widget

    def keyboard_action(key):
        if current_active_entry:
            if key == "Backspace":
                current_text = current_active_entry.get()[:-1]
            elif key == "Space":
                current_text = current_active_entry.get() + " "
            else:
                current_text = current_active_entry.get() + key
            current_active_entry.delete(0, tk.END)
            current_active_entry.insert(0, current_text)

    frame = ctk.CTkFrame(master=app)
    frame.pack(pady=20, padx=40, fill='both', expand=True)

    user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username", height=80, width=500, font=("Lato", 50))
    user_entry.pack(pady=10, padx=10)
    user_entry.bind("<FocusIn>", lambda event: set_current_active_entry(user_entry))

    user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*", height=80, width=500, font=("Lato", 50))
    user_pass.pack(pady=10, padx=10)
    user_pass.bind("<FocusIn>", lambda event: set_current_active_entry(user_pass))

    button = ctk.CTkButton(master=frame, text='Login', command=login, height=80, width=500, font=("Lato", 50))
    button.pack(pady=10, padx=10)

    def create_keyboard(frame):
        keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '='],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'Backspace'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm', 'Space']
        ]

        for i, row in enumerate(keys):
            row_frame = ctk.CTkFrame(master=frame)
            row_frame.pack(fill='x', padx=5, pady=5)
            for key in row:
                btn = ctk.CTkButton(master=row_frame, text=key, width=200 if key in ["Space", "Backspace"] else 90, height=80,
                                    command=lambda k=key: keyboard_action(k), font=("Lato", 50))
                btn.pack(side='left', expand=True if key in ["Space", "Backspace"] else False, fill='x' if key in ["Space", "Backspace"] else None, padx=5)

    create_keyboard(frame)

    class DisplayWindow(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.overrideredirect(True)
            self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
            self.title("CustomTkinter complex_example.py")
            self.camera_on = False
            self.camera = None

            self.grid_columnconfigure(2, weight=1)
            self.grid_rowconfigure((0, 1, 2), weight=1)

            self.sidebar_frame = ctk.CTkFrame(self, width=300, corner_radius=0)
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
            self.sidebar_frame.grid_rowconfigure(5, weight=1)

            self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="RetinaSpy",
                                           font=ctk.CTkFont(size=50, weight="bold"))
            self.logo_label.grid(row=0, column=0, pady=(20, 10), padx=(100, 100), sticky="ew")

            # Buttons are larger to fit the new sidebar size
            button_height = 80
            button_padding = (10, 60)

            self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="On", height=button_height, font=("Lato", 40),
                                                  command=lambda: self.sidebar_button_event(self.sidebar_button_1))
            self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=button_padding, sticky="ew")
            self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text="Capture", height=button_height, font=("Lato", 40),
                                                  command=lambda: self.sidebar_button_event(None))
            self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=button_padding, sticky="ew")

            self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame, text="Settings", height=button_height, font=("Lato", 40),
                                                  command=self.open_settings_window)
            self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=button_padding, sticky="ew")

            self.sidebar_button_4 = ctk.CTkButton(self.sidebar_frame, text="Logout", height=button_height, font=("Lato", 40),
                                                  command=self.destroy)
            self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=button_padding, sticky="ew")

            # Bigger squares and properly aligned
            square_size = 300  # New square size
            self.gray_square_1 = ctk.CTkFrame(self, width=square_size, height=square_size, corner_radius=0,
                                              fg_color="gray")
            self.gray_square_1.grid(row=1, column=2, padx=(30, 0), pady=(0, 0))
            self.gray_square_2 = ctk.CTkFrame(self, width=square_size, height=square_size, corner_radius=0,
                                              fg_color="gray")
            self.gray_square_2.grid(row=1, column=3, padx=30, pady=(0,0))

            # Larger rectangle below squares
            self.rectangle_below_squares = ctk.CTkFrame(self, height=150, corner_radius=0, fg_color="gray")
            self.rectangle_below_squares.grid(row=2, column=2, columnspan=2, padx=(60, 30), pady=(35, 60), sticky="ew")

            # Thicker and longer slider/progress bar
            self.slider_progressbar_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.slider_progressbar_frame.grid(row=1, column=4, rowspan=2, padx=(0, 20), pady=(15,70), sticky="nsew")
            self.slider_progressbar_frame.grid_rowconfigure(0, weight=1)
            self.slider_2 = ctk.CTkSlider(self.slider_progressbar_frame, orientation="vertical", width=22)
            self.slider_2.grid(row=0, column=0, padx=(10, 10), pady=10, sticky="ns")
            self.slider_2.set(0)
            self.progressbar_3 = ctk.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical", width=25)
            self.progressbar_3.grid(row=0, column=1, padx=(10, 10), pady=10, sticky="ns")
            self.progressbar_3.set(0)

            self.sidebar_button_3.configure(state="normal", text="Settings")
            self.slider_2.configure(command=self.progressbar_3.set)

        def sidebar_button_event(self, button):
            if button is not None:
                current_text = button.cget('text')
                if current_text == "On":
                    button.configure(text="Off")
                elif current_text == "Off":
                    button.configure(text="On")
                else:
                    print("sidebar_button click")

        def open_settings_window(self):
            settings_window = SettingsWindow()
            settings_window.mainloop()

    class SettingsWindow(ctk.CTk):
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("green")

        def __init__(self):
            super().__init__()
            self.overrideredirect(True)
            self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
            self.title("Settings")

            self.grid_columnconfigure(1, weight=1)
            self.grid_columnconfigure((1, 2,), weight=0)
            self.grid_rowconfigure((1, 2, 3), weight=1)

            self.normal_frame = customtkinter.CTkFrame(self)
            self.normal_frame.grid(row=0, column=1, padx=(10, 1), pady=(5, 0), sticky="nsew")
            self.normal_frame.grid_columnconfigure(1, weight=1)

            self.box1 = customtkinter.CTkLabel(self.normal_frame, fg_color="#3B3B3B", text="Options", corner_radius=5)
            self.box1.grid(row=0, column=0, padx=(8.5, 7.5), pady=(0, 5), sticky="ew")

            self.button1 = customtkinter.CTkButton(self.normal_frame, text="Retake Image")
            self.button1.grid(row=1, column=0, padx=42, pady=2, sticky="ew")

            self.button2 = customtkinter.CTkButton(self.normal_frame, text="Patient Information", command=self.open_patient_information_window)
            self.button2.grid(row=2, column=0, padx=42, pady=2, sticky="ew")

            self.button3 = customtkinter.CTkButton(self.normal_frame, text="Further Analysis", command=self.launchFurtherAnalysis)
            self.button3.grid(row=3, column=0, padx=42, pady=2, sticky="ew")

            self.button4 = customtkinter.CTkButton(self.normal_frame, text="Exit", command=self.exit_application)
            self.button4.grid(row=4, column=0, padx=42, pady=2, sticky="ew")

            for i in range(5):
                self.normal_frame.grid_rowconfigure(i, weight=1)

            self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
            self.slider_progressbar_frame.grid(row=1, column=1, columnspan=5, padx=75, pady=(2, 5), sticky="nsew")
            self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
            self.slider_progressbar_frame.grid_rowconfigure(0, weight=1)
            self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
            self.progressbar_1.grid(row=1, column=1, columnspan=5, padx=65, pady=(2, 5), sticky="ew")

            self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Patient Number")
            self.scrollable_frame.grid(row=0, column=2, padx=(5, 0), pady=(5, 0), sticky="nsew")
            self.scrollable_frame.grid_columnconfigure(0, weight=0)
            self.scrollable_frame_switches = []
            for i in range(1, 101):
                switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"Patient {i}")
                switch.grid(row=i, column=0, padx=(50, 0), pady=(0, 20))
                self.scrollable_frame_switches.append(switch)

            self.scrollable_frame_switches[0].select()
            self.progressbar_1.configure(mode="indeterminnate")
            self.progressbar_1.start()

        def change_appearance_mode_event(self, new_appearance_mode: str):
            customtkinter.set_appearance_mode(new_appearance_mode)

        def change_scaling_event(self, new_scaling: str):
            new_scaling_float = int(new_scaling.replace("%", "")) / 100
            customtkinter.set_widget_scaling(new_scaling_float)

        def exit_application(self):
            self.destroy()

        def open_patient_information_window(self):
            patient_information_window = PatientInformationWindow(self)
            patient_information_window.mainloop()

        def launchFurtherAnalysis(self):

            if hasattr(self, 'dialog') and self.dialog.isVisible():
                self.dialog.raise_()
                return
            class CustomDial(QDial):
                def __init__(self, parent=None, image_path=""):
                    super().__init__(parent)
                    self.setMinimum(0)
                    self.setMaximum(100)
                    self.setValue(0)
                    self.loadAndPrepareImage(image_path)

                def loadAndPrepareImage(self, image_path):
                    pixmap_size = 170
                    original_pixmap = QPixmap(image_path)
                    if original_pixmap.width() != original_pixmap.height():
                        scaled_pixmap = original_pixmap.scaled(pixmap_size, pixmap_size, Qt.KeepAspectRatioByExpanding,
                                                               Qt.SmoothTransformation)
                        x0 = (scaled_pixmap.width() - pixmap_size) // 2
                        y0 = (scaled_pixmap.height() - pixmap_size) // 2
                        original_pixmap = scaled_pixmap.copy(x0, y0, pixmap_size, pixmap_size)
                    else:
                        original_pixmap = original_pixmap.scaled(pixmap_size, pixmap_size, Qt.IgnoreAspectRatio,
                                                                 Qt.SmoothTransformation)

                    mask = QBitmap(pixmap_size, pixmap_size)
                    mask.fill(Qt.color0)
                    painter = QPainter(mask)
                    painter.setRenderHint(QPainter.Antialiasing)
                    painter.setBrush(Qt.color1)
                    painter.drawEllipse(0, 0, pixmap_size, pixmap_size)
                    painter.end()

                    original_pixmap.setMask(mask)
                    self.pixmap = original_pixmap
                    self.setFixedSize(200, 200)

                def paintEvent(self, event):
                    super().paintEvent(event)
                    painter = QPainter(self)
                    painter.setRenderHint(QPainter.Antialiasing)
                    angle = 360 * self.value() / (self.maximum() - self.minimum())
                    painter.translate(self.width() / 2, self.height() / 2)
                    painter.rotate(angle)
                    painter.translate(-self.width() / 2, -self.height() / 2)
                    painter.drawPixmap((self.width() - self.pixmap.width()) / 2,
                                       (self.height() - self.pixmap.height()) / 2,
                                       self.pixmap)

            class Dialog(QDialog):
                def __init__(self):
                    super().__init__()
                    self.setWindowFlags(Qt.FramelessWindowHint)
                    self.leftEyeImage = "C:/Users/Frogs/Downloads/Example.jpg"
                    self.rightEyeImage = "C:/Users/Frogs/Downloads/Example2.jpg"
                    self.currentImage = self.leftEyeImage

                    self.dial = CustomDial(self, self.currentImage)
                    self.initUI()
                    self.showFullScreen()

                def initUI(self):
                    self.slider = QSlider(Qt.Horizontal)
                    self.slider.setMinimum(0)
                    self.slider.setMaximum(100)
                    self.slider.setValue(0)
                    self.slider.setFixedWidth(240)

                    self.progressBar = QProgressBar()
                    self.progressBar.setMinimum(0)
                    self.progressBar.setMaximum(100)
                    self.progressBar.setValue(0)
                    self.progressBar.setFixedWidth(275)

                    self.slider.valueChanged.connect(self.dial.setValue)
                    self.dial.valueChanged.connect(self.progressBar.setValue)
                    self.dial.valueChanged.connect(self.slider.setValue)

                    self.buttonBox = QVBoxLayout()
                    self.leftEyeButton = QPushButton("Left Eye")
                    self.rightEyeButton = QPushButton("Right Eye")
                    self.exitButton = QPushButton("Exit")
                    self.buttonBox.addWidget(self.leftEyeButton)
                    self.buttonBox.addWidget(self.rightEyeButton)
                    self.buttonBox.addWidget(self.exitButton)
                    self.buttonBox.addStretch()

                    self.leftEyeButton.clicked.connect(self.showLeftEye)
                    self.rightEyeButton.clicked.connect(self.showRightEye)
                    self.exitButton.clicked.connect(self.close)

                    self.showLeftEye()

                    mainLayout = QHBoxLayout()
                    controlsLayout = QVBoxLayout()
                    controlsLayout.addWidget(self.dial)
                    controlsLayout.addWidget(self.slider)
                    controlsLayout.addWidget(self.progressBar)
                    mainLayout.addLayout(controlsLayout)
                    mainLayout.addLayout(self.buttonBox)

                    self.setLayout(mainLayout)

                def showLeftEye(self):
                    self.currentImage = self.leftEyeImage
                    self.dial.loadAndPrepareImage(self.currentImage)
                    self.dial.update()  # Force the dial to repaint with the new image
                    self.leftEyeButton.setStyleSheet("background-color: #555555;")  # Indicate active selection
                    self.rightEyeButton.setStyleSheet("")  # Reset to default style
                    self.leftEyeButton.setDisabled(True)
                    self.rightEyeButton.setEnabled(True)

                def showRightEye(self):
                    self.currentImage = self.rightEyeImage
                    self.dial.loadAndPrepareImage(self.currentImage)
                    self.dial.update()  # Force the dial to repaint with the new image
                    self.rightEyeButton.setStyleSheet("background-color: #555555;")  # Indicate active selection
                    self.leftEyeButton.setStyleSheet("")  # Reset to default style
                    self.rightEyeButton.setDisabled(True)
                    self.leftEyeButton.setEnabled(True)

                    self.exitButton.clicked.connect(self.close)

            if __name__ == '__main__':
                import sys

                app = QApplication(sys.argv)

                # Apply dark theme style sheet
                app.setStyleSheet("""
                        QWidget {
                            background-color: #2d2d2d;
                            color: #cccccc; /* General text color */
                        }
                        QDialog {
                            background-color: #2d2d2d;
                        }
                        QPushButton {
                            background-color: #30BD82;
                            border: 1px solid #555;
                            border-radius: 2px;
                            padding: 5px;
                            min-height: 18px;
                            color: #ffffff; /* White text */
                        }
                        QPushButton:pressed {
                            background-color: #555555;
                        }
                        QPushButton:disabled {
                            background-color: #333333;
                            border-color: #444444;
                        }

                        QSlider::groove:horizontal {
                            border: 1px solid #999999;
                            height: 8px;
                            background: #3a3a3a;
                            margin: 2px 0;
                        }
                        QSlider::handle:horizontal {
                            background: #bcbcbc;
                            border: 1px solid #5c5c5c;
                            width: 18px;
                            margin: -2px 0;
                            border-radius: 3px;
                        }

                    """)

                self.dialog = Dialog()
                self.dialog.show()

    class PatientInformationWindow(ctk.CTk):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")

        def __init__(self, parent, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.parent = parent
            self.overrideredirect(True)
            self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

            self.placeholderFunction = None
            self.title("Patient Information")

            self.current_active_entry = None

            self.setup_ui()

            self.keyboard_frame = ctk.CTkFrame(self)
            self.keyboard_frame.grid(row=5, column=0, columnspan=4, pady=(0, 0), sticky="nsew")
            self.grid_rowconfigure(5, weight=1)
            self.grid_columnconfigure(0, weight=1)
            self.create_keyboard(self.keyboard_frame)

        def setup_ui(self):
            self.nameLabel = ctk.CTkLabel(self, text="")
            self.nameLabel.grid(row=0, column=0, padx=0, pady=5, sticky="ew")
            self.nameEntry = ctk.CTkEntry(self, placeholder_text="Name")
            self.nameEntry.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

            # Age Label and Entry
            self.ageLabel = ctk.CTkLabel(self, text="")
            self.ageLabel.grid(row=1, column=0, padx=0, pady=5, sticky="ew")
            self.ageEntry = ctk.CTkEntry(self, placeholder_text="Age")
            self.ageEntry.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

            self.genderLabel = ctk.CTkLabel(self, text="Gender")
            self.genderLabel.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
            self.genderVar = tk.StringVar(value="Other")
            self.maleRadioButton = ctk.CTkRadioButton(self, text="Male", variable=self.genderVar, value="Male")
            self.maleRadioButton.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
            self.femaleRadioButton = ctk.CTkRadioButton(self, text="Female", variable=self.genderVar, value="Female")
            self.femaleRadioButton.grid(row=2, column=2, padx=10, pady=5, sticky="ew")
            self.noneRadioButton = ctk.CTkRadioButton(self, text="Other", variable=self.genderVar,
                                                      value="Prefer not to say")
            self.noneRadioButton.grid(row=2, column=3, padx=10, pady=5, sticky="ew")

            self.choiceLabel = ctk.CTkLabel(self, text="Results")
            self.choiceLabel.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
            self.checkboxVar = tk.StringVar(value="Choice 1")
            self.choice1 = ctk.CTkCheckBox(self, text="DR", variable=self.checkboxVar, onvalue="choice1", offvalue="c1")
            self.choice1.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
            self.choice2 = ctk.CTkCheckBox(self, text="No DR", variable=self.checkboxVar, onvalue="choice2",
                                           offvalue="c2")
            self.choice2.grid(row=3, column=2, padx=10, pady=5, sticky="ew")
            self.choice3 = ctk.CTkCheckBox(self, text="Consultation Needed", variable=self.checkboxVar,
                                           onvalue="choice3", offvalue="c3")
            self.choice3.grid(row=3, column=3, padx=10, pady=5, sticky="ew")

            self.ExitButton = ctk.CTkButton(self, text="Exit", command=self.exit_application)
            self.ExitButton.grid(row=1, column=3, columnspan=1, padx=(10, 18), pady=0, sticky="ew")

            self.SaveButton = ctk.CTkButton(self, text="Save Information", command=self.placeholderFunction)
            self.SaveButton.grid(row=0, column=3, columnspan=1, padx=(10, 18), pady=0, sticky="ew")

            for widget in self.winfo_children():
                if isinstance(widget, ctk.CTkEntry):
                    widget.bind("<FocusIn>", self.set_current_active_entry)

        def create_keyboard(self, frame):
            keys = [
                ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-'],
                ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '='],
                ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'Backspace'],
                ['z', 'x', 'c', 'v', 'b', 'n', 'm', 'Space']
            ]

            for i, row in enumerate(keys):
                row_frame = ctk.CTkFrame(master=frame)
                row_frame.pack(fill='x', padx=5, pady=2)
                for key in row:
                    btn = ctk.CTkButton(master=row_frame, text=key, width=100 if key in ["Space", "Backspace"] else 30, height=30, command=lambda k=key: self.keyboard_action(k))
                    btn.pack(side='left', expand=True if key in ["Space", "Backspace"] else False, fill='x' if key in ["Space", "Backspace"] else None, padx=2)

        def set_current_active_entry(self, event):
            self.current_active_entry = event.widget

        def keyboard_action(self, key):
            if self.current_active_entry:
                if key == "Backspace":
                    current_text = self.current_active_entry.get()[:-1]
                elif key == "Space":
                    current_text = self.current_active_entry.get() + " "
                else:
                    current_text = self.current_active_entry.get() + key
                self.current_active_entry.delete(0, tk.END)
                self.current_active_entry.insert(0, current_text)

        def placeholder_function(self):
            print("Save information function called")

        def exit_application(self):
            self.destroy()

    app.mainloop()


start_tkinter_app()
