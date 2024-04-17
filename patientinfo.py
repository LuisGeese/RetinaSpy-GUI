import customtkinter as ctk
import tkinter as tk

# Sets the appearance mode and color theme
ctk.set_appearance_mode("Dark")  # Dark mode
ctk.set_default_color_theme("green")  # Green color theme

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.overrideredirect(True)

        self.placeholderFunction = None
        appWidth, appHeight = 480, 288  # Adjusted window size to ensure there's enough space for the keyboard
        self.title("GUI Application")
        self.geometry(f"{appWidth}x{appHeight}")

        # Initialize variable to keep track of the current active entry
        self.current_active_entry = None

        # Main UI Setup
        self.setup_ui()

        # Keyboard setup
        self.keyboard_frame = ctk.CTkFrame(self)
        self.keyboard_frame.grid(row=5, column=0, columnspan=4, pady=(0, 0), sticky="nsew")
        self.grid_rowconfigure(5, weight=1)  # Give the keyboard frame expandable space
        self.grid_columnconfigure(0, weight=1)  # Ensure the column expands as needed
        self.create_keyboard(self.keyboard_frame)

    def setup_ui(self):
        # Name Label and Entry
        self.nameLabel = ctk.CTkLabel(self, text="")
        self.nameLabel.grid(row=0, column=0, padx=0, pady=5, sticky="ew")
        self.nameEntry = ctk.CTkEntry(self, placeholder_text="Name")
        self.nameEntry.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Age Label and Entry
        self.ageLabel = ctk.CTkLabel(self, text="")
        self.ageLabel.grid(row=1, column=0, padx=0, pady=5, sticky="ew")
        self.ageEntry = ctk.CTkEntry(self, placeholder_text="Age")
        self.ageEntry.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Gender Label and Radio Buttons
        self.genderLabel = ctk.CTkLabel(self, text="Gender")
        self.genderLabel.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.genderVar = tk.StringVar(value="Other")
        self.maleRadioButton = ctk.CTkRadioButton(self, text="Male", variable=self.genderVar, value="Male")
        self.maleRadioButton.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.femaleRadioButton = ctk.CTkRadioButton(self, text="Female", variable=self.genderVar, value="Female")
        self.femaleRadioButton.grid(row=2, column=2, padx=10, pady=5, sticky="ew")
        self.noneRadioButton = ctk.CTkRadioButton(self, text="Other", variable=self.genderVar, value="Prefer not to say")
        self.noneRadioButton.grid(row=2, column=3, padx=10, pady=5, sticky="ew")

        # Choice Label and Checkboxes
        self.choiceLabel = ctk.CTkLabel(self, text="Results")
        self.choiceLabel.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.checkboxVar = tk.StringVar(value="Choice 1")
        self.choice1 = ctk.CTkCheckBox(self, text="DR", variable=self.checkboxVar, onvalue="choice1", offvalue="c1")
        self.choice1.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.choice2 = ctk.CTkCheckBox(self, text="No DR", variable=self.checkboxVar, onvalue="choice2", offvalue="c2")
        self.choice2.grid(row=3, column=2, padx=10, pady=5, sticky="ew")
        self.choice3 = ctk.CTkCheckBox(self, text="Consultation Needed", variable=self.checkboxVar, onvalue="choice3", offvalue="c3")
        self.choice3.grid(row=3, column=3, padx=10, pady=5, sticky="ew")

        # Exit and Save Information Buttons
        self.ExitButton = ctk.CTkButton(self, text="Exit", command=self.exit_application)
        self.ExitButton.grid(row=1, column=3, columnspan=1, padx=(10, 18), pady=0, sticky="ew")

        self.SaveButton = ctk.CTkButton(self, text="Save Information", command=self.placeholderFunction)
        self.SaveButton.grid(row=0, column=3, columnspan=1, padx=(10, 18), pady=0, sticky="ew")
        
        # Ensure all entries and interactive widgets bind the focus-in event to set the active entry
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkEntry):
                widget.bind("<FocusIn>", self.set_current_active_entry)

    def create_keyboard(self, frame):  # Added self parameter here
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
                btn = ctk.CTkButton(master=row_frame, text=key, width=100 if key in ["Space", "Backspace"] else 30,
                                    height=30,
                                    command=lambda k=key: self.keyboard_action(
                                        k))  # Changed keyboard_action to self.keyboard_action
                btn.pack(side='left', expand=True if key in ["Space", "Backspace"] else False,
                         fill='x' if key in ["Space", "Backspace"] else None, padx=2)

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
        # Placeholder function for save information button
        print("Save information function called")

    def exit_application(self):  # Defined method
            self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
