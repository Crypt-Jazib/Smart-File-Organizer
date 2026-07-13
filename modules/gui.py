import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from modules.organizer import FileOrganizer
from modules.report import generate_report

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

WINDOW_WIDTH = 950
WINDOW_HEIGHT = 720

ENTRY_WIDTH = 500
PREVIEW_WIDTH = 600
PREVIEW_HEIGHT = 220

PROGRESS_WIDTH = 500


class SmartFileOrganizerApp(ctk.CTk):

    def __init__(self) -> None:
        super().__init__()

        self.title("Smart File Organizer v1.0")
        self.resizable(False, False)

        self.folder_path = ""
        self.statistics = {}

        self.center_window()
        self.create_widgets()

    def center_window(self) -> None:

        self.update_idletasks()

        x = (self.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
        y = (self.winfo_screenheight() // 2) - (WINDOW_HEIGHT // 2)

        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    def create_widgets(self) -> None:

        title = ctk.CTkLabel(
            self,
            text="Smart File Organizer",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)

        self.theme_switch = ctk.CTkSwitch(
            self,
            text="Dark Mode",
            command=self.change_theme
        )
        self.theme_switch.select()
        self.theme_switch.pack(pady=5)

        self.path_entry = ctk.CTkEntry(
            self,
            width=ENTRY_WIDTH
        )
        self.path_entry.pack(pady=10)

        browse_btn = ctk.CTkButton(
            self,
            text="Browse Folder",
            command=self.browse_folder
        )
        browse_btn.pack()

        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(
            padx=20,
            pady=15,
            fill="x"
        )

        self.total_label = ctk.CTkLabel(
            stats_frame,
            text="Total Files : 0",
            font=("Arial", 15, "bold")
        )
        self.total_label.grid(row=0, column=0, padx=20, pady=10)

        self.image_label = ctk.CTkLabel(
            stats_frame,
            text="Images : 0"
        )
        self.image_label.grid(row=0, column=1, padx=20)

        self.document_label = ctk.CTkLabel(
            stats_frame,
            text="Documents : 0"
        )
        self.document_label.grid(row=0, column=2, padx=20)

        self.other_label = ctk.CTkLabel(
            stats_frame,
            text="Others : 0"
        )
        self.other_label.grid(row=0, column=3, padx=20)

        self.preview_box = ctk.CTkTextbox(
            self,
            width=PREVIEW_WIDTH,
            height=PREVIEW_HEIGHT
        )
        self.preview_box.pack(pady=20)
        self.preview_box.configure(state="disabled")

        self.progress = ctk.CTkProgressBar(
            self,
            width=PROGRESS_WIDTH
        )
        self.progress.pack(pady=10)
        self.progress.set(0)

        self.status_label = ctk.CTkLabel(
            self,
            text="Status : Ready",
            font=("Arial", 14)
        )
        self.status_label.pack(pady=5)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)

        self.preview_btn = ctk.CTkButton(
            button_frame,
            text="Preview",
            command=self.preview_files
        )
        self.preview_btn.grid(row=0, column=0, padx=10)

        self.organize_btn = ctk.CTkButton(
            button_frame,
            text="Organize",
            command=self.start_organizing
        )
        self.organize_btn.grid(row=0, column=1, padx=10)

        self.report_btn = ctk.CTkButton(
            button_frame,
            text="Generate Report",
            command=self.export_report
        )
        self.report_btn.grid(row=0, column=2, padx=10)

        self.reset_btn = ctk.CTkButton(
            button_frame,
            text="Reset",
            command=self.reset
        )
        self.reset_btn.grid(row=0, column=3, padx=10)

        self.exit_btn = ctk.CTkButton(
            button_frame,
            text="Exit",
            width=120,
            fg_color="red",
            hover_color="#B22222",
            command=self.destroy
        )
        self.exit_btn.grid(row=0, column=4, padx=10)

        self.about_btn = ctk.CTkButton(
            button_frame,
            text="About",
            command=self.about
        )
        self.about_btn.grid(row=0, column=5, padx=10)

        self.create_footer()
    
        self.iconbitmap("assets/icon.ico")

    def create_footer(self) -> None:

        footer = ctk.CTkLabel(
            self,
            text="© 2026 Smart File Organizer | Developed by Syed Jazib Ali Shah",
            font=("Arial", 11)
        )
        footer.pack(side="bottom", pady=8)

    def set_buttons_state(self, state: str) -> None:
        self.preview_btn.configure(state=state)
        self.organize_btn.configure(state=state)
        self.report_btn.configure(state=state)
        self.reset_btn.configure(state=state)
        self.exit_btn.configure(state=state)

    def change_theme(self) -> None:
        """Switch between Dark and Light mode."""

        if self.theme_switch.get():
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    def about(self) -> None:
    
        messagebox.showinfo(
            "About",
            "Smart File Organizer\n\n"
            "Version : 1.0\n\n"
            "Developed by:\n"
            "Syed Jazib Ali Shah"
        )

    def browse_folder(self) -> None:
         folder = filedialog.askdirectory()

         if not folder:
            return

         self.folder_path = folder

         self.path_entry.delete(0, "end")
         self.path_entry.insert(0, folder)

         self.status_label.configure(
            text="Status : Folder Selected"
        )

    def preview_files(self) -> None:
        if not self.folder_path:
            messagebox.showwarning(
                "Warning",
                "Please select a folder first."
            )
            return

        file_organizer = FileOrganizer(self.folder_path)

        self.statistics = file_organizer.preview()
        self.update_statistics()

        report = "=" * 40 + "\n"
        report += "      SMART PREVIEW REPORT\n"
        report += "=" * 40 + "\n\n"

        for category, count in self.statistics.items():
            report += f"{category:<18}{count}\n"

        self.preview_box.configure(state="normal")
        self.preview_box.delete("1.0", "end")
        self.preview_box.insert("end", report)
        self.preview_box.configure(state="disabled")

    def update_progress(self, value: float) -> None:
        self.progress.set(value)

        percentage = int(value * 100)

        self.status_label.configure(
            text=f"Status : Organizing... {percentage}%"
        )

        self.update_idletasks()

    def start_organizing(self) -> None:
        organize_thread = threading.Thread(
            target=self.organize_files,
            daemon=True
        )

        organize_thread.start()

    def organize_files(self) -> None:
        if not self.folder_path:
            messagebox.showwarning(
                "Warning",
                "Please select a folder first."
            )
            return

        answer = messagebox.askyesno(
            "Confirmation",
            "Do you want to organize this folder?"
        )

        if not answer:
            return

        self.set_buttons_state("disabled")

        self.status_label.configure(
            text="Status : Organizing..."
        )

        try:

            self.progress.set(0)

            file_organizer = FileOrganizer(self.folder_path)

            self.statistics = file_organizer.organize(
                self.update_progress
            )

            self.update_statistics()

            report = "=" * 40 + "\n"
            report += "      ORGANIZATION REPORT\n"
            report += "=" * 40 + "\n\n"

            for category, count in self.statistics.items():
                report += f"{category:<18}{count}\n"

            self.preview_box.configure(state="normal")
            self.preview_box.delete("1.0", "end")
            self.preview_box.insert("end", report)
            self.preview_box.configure(state="disabled")

            self.progress.set(1)

            self.status_label.configure(
                text="Status : Completed"
            )

            messagebox.showinfo(
                "Organization Complete",
                f"""
Total Files : {self.statistics.get('Total',0)}

Duplicates : {self.statistics.get('Duplicates',0)}

Files organized successfully.
"""
            )
        except Exception as error:

            self.status_label.configure(
                text="Status : Error"
            )

            messagebox.showerror(
                "Error",
                str(error)
            )

        finally:

            self.set_buttons_state("normal")

    def export_report(self) -> None:

        if not self.statistics:

            messagebox.showwarning(
                "Warning",
                "Please organize files first."
            )
            return

        report_path = generate_report(self.statistics)

        messagebox.showinfo(
            "Report Generated",
            f"Report saved successfully.\n\n{report_path}"
        )


    def reset(self) -> None:

        self.folder_path = ""
        self.statistics = {}

        self.path_entry.delete(0, "end")

        self.preview_box.configure(state="normal")
        self.preview_box.delete("1.0", "end")
        self.preview_box.configure(state="disabled")

        self.progress.set(0)

        self.status_label.configure(
            text="Status : Ready"
        )

        self.total_label.configure(
            text="Total Files : 0"
        )

        self.image_label.configure(
            text="Images : 0"
        )

        self.document_label.configure(
            text="Documents : 0"
        )

        self.other_label.configure(
            text="Others : 0"
        )

    def update_statistics(self) -> None:
        """Update statistics labels."""

        if not self.statistics:
            return

        self.total_label.configure(
            text=f"Total Files : {self.statistics.get('Total', 0)}"
        )

        self.image_label.configure(
            text=f"Images : {self.statistics.get('Images', 0)}"
        )

        self.document_label.configure(
            text=f"Documents : {self.statistics.get('Documents', 0)}"
        )

        self.other_label.configure(
            text=f"Others : {self.statistics.get('Others', 0)}"
        )