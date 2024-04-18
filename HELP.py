import customtkinter
import pygame
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QDialogButtonBox, \
    QProgressBar, QSlider, \
    QDial, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPainter, QPixmap, QBitmap, QFont
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
logo_5_path = "./Top Part Logo.svg"
logo_6_path = "./Bottom part logo.svg"
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
    app.geometry("1280x720")
    app.title("RetinaSpy")

    current_active_entry = None

    def login():
        username = "p"
        password = "1"

        if user_entry.get() == username and user_pass.get() == password:
            app.destroy()
            display_app = DisplayWindow()
            display_app.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password", parent=app)

    def set_current_active_entry(entry_widget):
        nonlocal current_active_entry
        current_active_entry = entry_widget
        current_active_entry.focus_set()


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
            self.title("CustomTkinter complex_example.py")
            self.geometry(f"{1280}x{720}")
            self.resizable(False, False)

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

            self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="On", height=button_height, font=("Lato", 50),
                                                  command=lambda: self.sidebar_button_event(self.sidebar_button_1))
            self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=button_padding, sticky="ew")
            self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text="Capture", height=button_height, font=("Lato", 50),
                                                  command=lambda: self.sidebar_button_event(None))
            self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=button_padding, sticky="ew")

            self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame, text="Settings", height=button_height, font=("Lato", 50),
                                                  command=self.open_settings_window)
            self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=button_padding, sticky="ew")

            self.sidebar_button_4 = ctk.CTkButton(self.sidebar_frame, text="Logout", height=button_height, font=("Lato", 50),
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
            self.title("Settings")
            self.geometry("1280x720")
            # Configure the grid to expand the middle column and rows
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=2)
            self.grid_columnconfigure(2, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=1)
            self.grid_rowconfigure(2, weight=8)
            self.grid_rowconfigure(3, weight=1)

            # Normal frame adjustments
            self.normal_frame = customtkinter.CTkFrame(self)
            self.normal_frame.grid(row=0, column=1, padx=(0, 25), pady=(10, 10), sticky="nsew")
            self.normal_frame.grid_columnconfigure(0, weight=1)
            self.normal_frame.grid_rowconfigure(0, weight=1)

            self.box1 = customtkinter.CTkLabel(self.normal_frame, fg_color="#3B3B3B", text="Options", height=80, font=("Lato", 50), corner_radius=5)
            self.box1.grid(row=0, column=0, padx=(10, 10), pady=(10, 50), sticky="ew")

            self.button1 = customtkinter.CTkButton(self.normal_frame, text="Retake Image", height=80, font=("Lato", 50))
            self.button1.grid(row=1, column=0, padx=75, pady=30, sticky="ew")

            self.button2 = customtkinter.CTkButton(self.normal_frame, text="Patient Information", height=80, font=("Lato", 50), command=self.open_patient_information_window)
            self.button2.grid(row=2, column=0, padx=75, pady=30, sticky="ew")

            self.button3 = customtkinter.CTkButton(self.normal_frame, text="Further Analysis", height=80, font=("Lato", 50), command=self.launchFurtherAnalysis)
            self.button3.grid(row=3, column=0, padx=75, pady=30, sticky="ew")

            self.button4 = customtkinter.CTkButton(self.normal_frame, text="Exit", height=80, font=("Lato", 50), command=self.exit_application)
            self.button4.grid(row=4, column=0, padx=75, pady=30, sticky="ew")

            # Slider and progressbar adjustments
            self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
            self.slider_progressbar_frame.grid(row=4, column=0, columnspan=3, padx=75, pady=(2, 5), sticky="nsew")
            self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
            self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
            self.progressbar_1.grid(row=0, column=0, columnspan=5, padx=65, pady=(2, 5), sticky="ew")

            # Scrollable frame adjustments
            self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Patient Number", label_font=("Lato", 50), width=550)
            self.scrollable_frame.grid(row=0, column=2, padx=(0, 20), pady=(10, 10), sticky="nsew")
            self.scrollable_frame.grid_columnconfigure(0, weight=1)

            self.scrollable_frame_switches = []
            for i in range(1, 101):
                switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"Patient {i}", height=20, font=("Lato", 50))
                switch.grid(row=i, column=0, padx=(0, 0), pady=(40, 0))
                self.scrollable_frame_switches.append(switch)

            self.scrollable_frame_switches[0].select()
            self.progressbar_1.configure(mode="indeterminate")
            self.progressbar_1.start()

        def change_appearance_mode_event(self, new_appearance_mode: str):
            customtkinter.set_appearance_mode(new_appearance_mode)

        def change_scaling_event(self, new_scaling: str):
            new_scaling_float = int(new_scaling.replace("%", ""))
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
                    pixmap_size = 500
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
                    self.setFixedSize(600, 600)

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
                    self.setFixedSize(1280, 720)
                    self.leftEyeImage = "./Left Eye.jpg"
                    self.rightEyeImage = "./Right Eye.jpg"
                    self.currentImage = self.leftEyeImage

                    self.dial = CustomDial(self, self.currentImage)
                    self.initUI()

                def initUI(self):
                    self.slider = QSlider(Qt.Horizontal)
                    self.slider.setMinimum(0)
                    self.slider.setMaximum(100)
                    self.slider.setValue(0)
                    self.slider.setFixedWidth(600)

                    self.progressBar = QProgressBar()
                    self.progressBar.setMinimum(0)
                    self.progressBar.setMaximum(100)
                    self.progressBar.setValue(0)
                    self.progressBar.setFixedWidth(600)
                    self.progressBar.setTextVisible(False)

                    self.progressLabel = QLabel("0%")
                    font = QFont("Lato", 28)  # Change "Arial" to your preferred font and "16" to your desired size
                    self.progressLabel.setFont(font)
                    self.progressLabel.setStyleSheet("color: white;")
                    self.progressLabel.setFixedWidth(98)

                    self.slider.valueChanged.connect(self.dial.setValue)
                    self.dial.valueChanged.connect(self.progressBar.setValue)
                    self.dial.valueChanged.connect(self.slider.setValue)
                    self.dial.valueChanged.connect(lambda value: self.progressLabel.setText(f"{value}%"))

                    self.buttonBox = QVBoxLayout()
                    self.leftEyeButton = QPushButton("Left Eye")
                    self.rightEyeButton = QPushButton("Right Eye")
                    self.exitButton = QPushButton("Exit")
                    self.buttonBox.addWidget(self.leftEyeButton)
                    self.buttonBox.addSpacing(25)
                    self.buttonBox.addWidget(self.rightEyeButton)
                    self.buttonBox.addSpacing(25)
                    self.buttonBox.addWidget(self.exitButton)
                    self.buttonBox.addStretch()

                    self.leftEyeButton.clicked.connect(self.showLeftEye)
                    self.rightEyeButton.clicked.connect(self.showRightEye)
                    self.exitButton.clicked.connect(self.close)

                    self.showLeftEye()

                    mainLayout = QHBoxLayout()
                    controlsLayout = QVBoxLayout()
                    controlsLayout.setSpacing(20)
                    controlsLayout.setContentsMargins(20, 0, 0, 40)
                    controlsLayout.addWidget(self.dial)
                    controlsLayout.addWidget(self.slider)
                    progressLayout = QHBoxLayout()
                    progressLayout.addWidget(self.progressBar)
                    progressLayout.addWidget(self.progressLabel)  # Add the label next to the progress bar
                    controlsLayout.addLayout(progressLayout)
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
                            padding: 10px;
                            min-height: 80px;
                            min-width: 450px; /* Minimum width of the button */
                            max-width: 450px; /* Maximum width of the button */
                            color: #ffffff; /* White text */
                            font-size: 50px;  /* Set font size directly in stylesheet */
                            font-family: 'Lato';  /* Set font family directly in stylesheet */
                        }
                        QPushButton:pressed {
                            background-color: #555555;
                        }
                        QPushButton:disabled {
                            background-color: #333333;
                            border-color: #444444;
                        }
                        QProgressBar {
                            border: 2px solid grey;
                            border-radius: 5px;
                            text-align: center;
                            background: #FFFFFF; /* Background color set to white */
                            height: 50px; /* Increased height of progress bar */
                        }

                        QProgressBar::chunk {
                            background-color: #30BD82; /* Green color for the progress chunk */
                            width: 40px; /* Optional, for chunky progress bar style */
                        }
                        QSlider::groove:horizontal {
                            border: 1px solid #999999;
                            height: 40px;
                            background: #3a3a3a;
                            margin: 2px 0;
                        }
                        QSlider::handle:horizontal {
                            background: #bcbcbc;
                            border: 1px solid #5c5c5c;
                            width: 40px;
                            margin: -2px 0;
                            border-radius: 3px;
                        }
                    """)

                dialog = Dialog()
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
            # Name Label and Entry
            self.nameLabel = ctk.CTkLabel(self, text="")
            self.nameLabel.grid(row=0, column=0, padx=0, pady=5, sticky="ew")
            self.nameEntry = ctk.CTkEntry(self, placeholder_text="Name", height=80, font=("Lato", 50))
            self.nameEntry.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

            # Age Label and Entry
            self.ageLabel = ctk.CTkLabel(self, text="")
            self.ageLabel.grid(row=1, column=0, padx=0, pady=5, sticky="ew")
            self.ageEntry = ctk.CTkEntry(self, placeholder_text="Age", height=80, font=("Lato", 50))
            self.ageEntry.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

            self.genderLabel = ctk.CTkLabel(self, text="Gender", font=("Lato", 50))
            self.genderLabel.grid(row=2, column=0, padx=(10, 70), pady=5, sticky="ew")
            self.genderVar = tk.StringVar(value="Other")
            self.maleRadioButton = ctk.CTkRadioButton(self, text="Male", font=("Lato", 30), variable=self.genderVar, value="Male")
            self.maleRadioButton.grid(row=2, column=1, padx=(10, 70), pady=5, sticky="ew")
            self.femaleRadioButton = ctk.CTkRadioButton(self, text="Female", font=("Lato", 30), variable=self.genderVar, value="Female")
            self.femaleRadioButton.grid(row=2, column=2, padx=(10, 70), pady=5, sticky="ew")
            self.noneRadioButton = ctk.CTkRadioButton(self, text="Other", font=("Lato", 30), variable=self.genderVar,
                                                      value="Prefer not to say")
            self.noneRadioButton.grid(row=2, column=3, padx=(10, 70), pady=5, sticky="ew")

            self.choiceLabel = ctk.CTkLabel(self, text="Results", font=("Lato", 50))
            self.choiceLabel.grid(row=3, column=0, padx=(10, 70), pady=5, sticky="ew")
            self.checkboxVar = tk.StringVar(value="Choice 1")
            self.choice1 = ctk.CTkCheckBox(self, text="DR", font=("Lato", 30), variable=self.checkboxVar, onvalue="choice1", offvalue="c1")
            self.choice1.grid(row=3, column=1, padx=(10, 70), pady=5, sticky="ew")
            self.choice2 = ctk.CTkCheckBox(self, text="No DR", font=("Lato", 30), variable=self.checkboxVar, onvalue="choice2",
                                           offvalue="c2")
            self.choice2.grid(row=3, column=2, padx=(10, 70), pady=5, sticky="ew")
            self.choice3 = ctk.CTkCheckBox(self, text="Consultation Needed", font=("Lato", 30), variable=self.checkboxVar,
                                           onvalue="choice3", offvalue="c3")
            self.choice3.grid(row=3, column=3, padx=10, pady=5, sticky="ew")

            self.ExitButton = ctk.CTkButton(self, text="Exit", height=80, font=("Lato", 50), command=self.exit_application)
            self.ExitButton.grid(row=1, column=3, columnspan=1, padx=(10, 18), pady=20, sticky="ew")

            self.SaveButton = ctk.CTkButton(self, text="Save Information", height=80, font=("Lato", 50), command=self.placeholderFunction)
            self.SaveButton.grid(row=0, column=3, columnspan=1, padx=(10, 18), pady=20, sticky="ew")

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
                row_frame.pack(fill='x', padx=5, pady=5)
                for key in row:
                    btn = ctk.CTkButton(master=row_frame, text=key, width=200 if key in ["Space", "Backspace"] else 90,
                                        height=80,
                                        command=lambda k=key: keyboard_action(k), font=("Lato", 50))
                    btn.pack(side='left', expand=True if key in ["Space", "Backspace"] else False,
                             fill='x' if key in ["Space", "Backspace"] else None, padx=5)

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
