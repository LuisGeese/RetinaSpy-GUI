import customtkinter

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)


        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{480}x{288}")
        self.resizable(False, False)  # Disable resizing

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="RetinaSpy", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=1, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="On",
            command=lambda: self.sidebar_button_event(self.sidebar_button_1)
        )
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Image", command=lambda: self.sidebar_button_event(None))
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Inference", command=lambda: self.sidebar_button_event(None))
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Settings", command=lambda: self.sidebar_button_event(None))
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)

        # create live camera feed windows
        self.gray_square_1 = customtkinter.CTkFrame(self, width=100, height=100, corner_radius=0, fg_color="gray")
        self.gray_square_1.grid(row=1, column=1, padx=10, pady=(10,90))

        self.gray_square_2 = customtkinter.CTkFrame(self, width=100, height=100, corner_radius=0, fg_color="gray")
        self.gray_square_2.grid(row=1, column=2, padx=0, pady=(10,90))

        self.rectangle_below_squares = customtkinter.CTkFrame(self, width=10, height=80, corner_radius=0, fg_color="gray")
        self.rectangle_below_squares.grid(row=1, column=1, columnspan=2, padx=(15,0), pady=(130, 0), sticky="ew")

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=3, padx=(5, 0), pady=(50, 10), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)

        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_2.grid(row=0, column=0, rowspan=4, padx=(10, 10), pady=(0, 150), sticky="ns")
        self.slider_2.set(0)  # Set the slider's value to 0
        self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_3.grid(row=0, column=1, rowspan=4, padx=(10, 10), pady=(0, 150), sticky="ns")
        self.progressbar_3.set(0)  # Set the progress bar's value to 0

        # set default values
        self.sidebar_button_3.configure(state="normal", text="Inference")
        self.slider_2.configure(command=self.progressbar_3.set)

    def sidebar_button_event(self, button):
        if button is not None:
            # Use cget to get the current button text
            current_text = button.cget('text')
            if current_text == "On":
                button.configure(text="Off")
            elif current_text == "Off":
                button.configure(text="On")
            else:
                print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()
