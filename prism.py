import customtkinter as ctk
from tkinter import messagebox, StringVar
from PIL import ImageTk, Image
# Asumo que estos ficheros existen en tu proyecto
from constants import EXPECTED_SECRET_LENGTH_BYTES
from shamir import ShamirSecret
import binascii # Necesario para la gestión de errores específicos


class Spinbox(ctk.CTkFrame):
    """A custom spinbox widget with increment and decrement buttons."""
    def __init__(
        self,
        *args,
        width: int = 100,
        height: int = 32,
        step_size: int = 1,
        min_value: int = 0,
        command=None,
        **kwargs
    ):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.min_value = min_value
        self.command = command

        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.value_var = StringVar(value=str(self.min_value))

        self.subtract_button = ctk.CTkButton(self, text="-", width=height-6, height=height-6, command=self.decrement_value)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = ctk.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0, textvariable=self.value_var, state="readonly", justify="center")
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = ctk.CTkButton(self, text="+", width=height-6, height=height-6, command=self.increment_value)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

    def increment_value(self):
        current_value = int(self.value_var.get())
        self.value_var.set(str(current_value + self.step_size))
        if self.command:
            self.command()

    def decrement_value(self):
        current_value = int(self.value_var.get())
        new_value = max(self.min_value, current_value - self.step_size)
        self.value_var.set(str(new_value))
        if self.command:
            self.command()

    def get(self) -> int:
        return int(self.value_var.get())

    def set(self, value: int):
        self.value_var.set(str(max(self.min_value, value)))


class Prism(ctk.CTk):
    """Main application class for the Prism GUI."""

    def __init__(self):
        super().__init__()
        self.title("Prism")
        self.geometry("800x900")
        self.resizable(False, False)

        try:
            image = Image.open("./icon.png")
            image = image.resize((128, 128), Image.LANCZOS)
            icon = ImageTk.PhotoImage(image)
            self.iconphoto(False, icon)
        except FileNotFoundError:
            print("Warning: Icon 'icon.png' not found")

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.create_widgets()

    def create_widgets(self):
        """Create and arrange all widgets in the main window."""
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        # CAMBIO: Añadidos espacios para separar visualmente las pestañas
        self.tabview.add("  Encode Secret  ")
        self.tabview.add("  Decode Secret  ")

        self._create_encode_tab_content(self.tabview.tab("  Encode Secret  "))
        self._create_decode_tab_content(self.tabview.tab("  Decode Secret  "))

    def _create_result_widgets(self, parent_tab, result_name="Result"):
        """Creates the result section widgets for a given tab."""
        result_frame = ctk.CTkFrame(parent_tab, fg_color="transparent")
        result_frame.pack(padx=10, pady=10, fill="both", expand=True)

        ctk.CTkLabel(result_frame, text="", font=ctk.CTkFont(weight="bold")).pack(anchor="w")

        result_output = ctk.CTkTextbox(result_frame, state="disabled")
        result_output.pack(pady=5, fill="both", expand=True)

        copy_button = ctk.CTkButton(result_frame, text=f"Copy {result_name}", width=140, command=self.copy_results)
        copy_button.pack(pady=(5, 0))

        return result_output

    def _create_encode_tab_content(self, tab):
        """Create widgets for the Encode Secret tab."""
        # CAMBIO: Añadido padding superior con pady=(20, 10)
        input_frame = ctk.CTkFrame(tab, fg_color="transparent")
        input_frame.pack(padx=10, pady=(20, 10), fill="x")

        ctk.CTkLabel(input_frame, text=f"Secret").pack(anchor="w")

        secret_input_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        secret_input_frame.pack(pady=5, fill="x")
        secret_input_frame.grid_columnconfigure(0, weight=1)

        self.secret_entry = ctk.CTkEntry(secret_input_frame, placeholder_text="Type or paste your secret here")
        self.secret_entry.grid(row=0, column=0, sticky="ew")

        param_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        param_frame.pack(fill="x", pady=(30, 0))
        param_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(param_frame, text="Total parts").grid(row=0, column=0, sticky="w")
        self.n_spinbox = Spinbox(param_frame, min_value=2, width=150, command=self.validate_parameters)
        self.n_spinbox.set(4)
        self.n_spinbox.grid(row=1, column=0, pady=(0, 5))

        ctk.CTkLabel(param_frame, text="Minimum parts needed to reconstruct").grid(row=2, column=0, pady=(30, 10), sticky="w")
        self.k_spinbox = Spinbox(param_frame, min_value=2, width=150, command=self.validate_parameters)
        self.k_spinbox.set(3)
        self.k_spinbox.grid(row=3, column=0)

        encode_button = ctk.CTkButton(tab, text="Generate Parts", command=self.encode_secret)
        encode_button.pack(padx=10, pady=30)

        self.encode_result_output = self._create_result_widgets(tab, result_name="Parts")

        self.validate_parameters()

    def validate_parameters(self):
        """Ensure k <= n and update button states."""
        n_val = self.n_spinbox.get()
        k_val = self.k_spinbox.get()

        if k_val > n_val:
            self.n_spinbox.set(k_val)

        self.k_spinbox.add_button.configure(state="normal" if k_val < n_val else "disabled")
        self.n_spinbox.subtract_button.configure(state="normal" if n_val > k_val else "disabled")

    def _create_decode_tab_content(self, tab):
        """Create widgets for the Decode Secret tab."""
        # CAMBIO: Añadido padding superior con pady=(20, 10)
        input_frame = ctk.CTkFrame(tab, fg_color="transparent")
        input_frame.pack(padx=10, pady=(20, 10), fill="x")

        ctk.CTkLabel(input_frame, text="Parts").pack(anchor="w")

        shares_input_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        shares_input_frame.pack(pady=5, fill="x")
        shares_input_frame.grid_columnconfigure(0, weight=1)

        self.shares_input = ctk.CTkTextbox(shares_input_frame, height=150)
        self.shares_input.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        paste_shares_button = ctk.CTkButton(shares_input_frame, text="Paste", width=80, command=self.paste_shares_to_textbox)
        paste_shares_button.grid(row=0, column=1, padx=5)

        decode_button = ctk.CTkButton(tab, text="Reconstruct Secret", command=self.decode_secret)
        decode_button.pack(padx=10, pady=15)

        self.decode_result_output = self._create_result_widgets(tab, result_name="Secret")


    def paste_shares_to_textbox(self):
        """Paste clipboard content into the shares textbox."""
        try:
            clipboard_content = self.clipboard_get()
            self.shares_input.delete("1.0", "end")
            self.shares_input.insert("1.0", clipboard_content)
        except ctk.tkinter.TclError:
            return

    def copy_results(self):
        """Copy the result text from the active tab to the clipboard."""
        # CAMBIO: Usar .strip() para eliminar los espacios del nombre de la pestaña antes de comparar
        active_tab = self.tabview.get().strip()
        result_text = ""

        if active_tab == "Encode Secret":
            result_text = self.encode_result_output.get("1.0", "end-1c")
        elif active_tab == "Decode Secret":
            result_text = self.decode_result_output.get("1.0", "end-1c")

        if result_text:
            self.clipboard_clear()
            self.clipboard_append(result_text)

    def encode_secret(self):
        """Encode the secret into shares."""
        try:
            secret = self.secret_entry.get()
            n = self.n_spinbox.get()
            k = self.k_spinbox.get()

            if not secret:
                messagebox.showwarning("Input Error", "The secret cannot be empty.")
                return

            if k > n:
                messagebox.showerror("Input Error", "k cannot be greater than n.")
                return

            formatted_shares, msg = ShamirSecret.split(k, n, secret)

            if not formatted_shares:
                messagebox.showerror("Encoding Error", msg)
                return

            self.show_result(self.encode_result_output, "\n".join(formatted_shares))

            # CAMBIO: Borrar el secreto del campo de entrada por seguridad.
            self.secret_entry.delete(0, 'end')

        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An error occurred during encoding:\n{e}")

    def decode_secret(self):
        """Decode the secret from shares."""
        try:
            shares_text = self.shares_input.get("1.0", "end-1c").strip()

            if not shares_text:
                 messagebox.showwarning("Input Error", "Please paste the parts to decode.")
                 return

            reconstructed_secret, msg = ShamirSecret.combine(shares_text.splitlines())

            if not reconstructed_secret:
                messagebox.showerror("Decoding Error", msg)
                return

            self.show_result(self.decode_result_output, reconstructed_secret)

        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An error occurred during decoding:\n{e}")

    def show_result(self, output_widget, text):
        """Display result text in the specified output textbox."""
        output_widget.configure(state="normal")
        output_widget.delete("1.0", "end")
        output_widget.insert("1.0", text)
        output_widget.configure(state="disabled")


if __name__ == "__main__":
    prism = Prism()
    prism.mainloop()