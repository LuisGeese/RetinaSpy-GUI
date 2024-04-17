import customtkinter


class App(customtkinter.CTk):
    customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

    def __init__(self):
        super().__init__()
        self.overrideredirect(True)


        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{480}x{288}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((1, 2,), weight=0)
        self.grid_rowconfigure((1, 2, 3), weight=1)

        # create tabview
        self.normal_frame = customtkinter.CTkFrame(self)
        self.normal_frame.grid(row=0, column=1, padx=(10,1), pady=(5, 0), sticky="nsew")
        self.normal_frame.grid_columnconfigure(1, weight=1)

        # Adding 5 vertically stacked buttons in the normal frame
        self.box1 = customtkinter.CTkLabel(self.normal_frame, fg_color="#3B3B3B", text="Options", corner_radius=5)
        self.box1.grid(row=0, column=0, padx=(8.5,7.5), pady=(0,5), sticky="ew")

        self.button1 = customtkinter.CTkButton(self.normal_frame, text="Retake Image")
        self.button1.grid(row=1, column=0, padx=42, pady=2, sticky="ew")

        self.button2 = customtkinter.CTkButton(self.normal_frame, text="Patient Information")
        self.button2.grid(row=2, column=0, padx=42, pady=2, sticky="ew")

        self.button3 = customtkinter.CTkButton(self.normal_frame, text="Further Analysis")
        self.button3.grid(row=3, column=0, padx=42, pady=2, sticky="ew")

        self.button4 = customtkinter.CTkButton(self.normal_frame, text="Exit", command=self.exit_application)
        self.button4.grid(row=4, column=0, padx=42, pady=2, sticky="ew")

        # Adjust the normal frame row configure for even spacing
        for i in range(5):  # Assuming 0 is for label or other content and 1-4 for buttons
            self.normal_frame.grid_rowconfigure(i, weight=1)

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, columnspan=5, padx=75, pady=(2,5), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(0, weight=1)
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=1, column=1, columnspan=5, padx=65, pady=(2,5), sticky="ew")

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Patient Number")
        self.scrollable_frame.grid(row=0, column=2, padx=(5,0), pady=(5,0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=0)
        self.scrollable_frame_switches = []
        for i in range(1,101):
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"Patient {i}")
            switch.grid(row=i, column=0, padx=(50,0), pady=(0, 20))
            self.scrollable_frame_switches.append(switch)

        # set default values
        self.scrollable_frame_switches[0].select()
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def exit_application(self):  # Defined method
            self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
