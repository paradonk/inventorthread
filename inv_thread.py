"""
ISO Metric Thread Calculator with GUI
Author: Paradorn Katananon
Description: Dynamic calculator for ISO metric thread dimensions
             Supports both external (bolt) and internal (nut) threads
             Based on ISO 68-1 and ISO 965-1 standards
"""

import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

def calc_metric_thread(thread_size, pitch, tol_external="6g", tol_internal="6H"):
    """
    Dynamic ISO Metric Thread Calculator
    Inputs:
        thread_size (float)   e.g., 20  → M20
        pitch (float)         e.g., 2.0 → P = 2.0
    """

    # --- Input Validation ---
    if thread_size <= 0:
        raise ValueError("Thread size must be greater than 0")
    if pitch <= 0:
        raise ValueError("Pitch must be greater than 0")
    if pitch > thread_size:
        raise ValueError("Pitch cannot be larger than thread size")

    # --- ISO basic profile constants (ISO 68-1) ---
    H = (math.sqrt(3) / 2) * pitch          # H = 0.866025P, height of fundamental triangle

    # --- basic diameters (ISO 68-1 formulas) ---
    # External thread (bolt):
    external_major_basic = thread_size      # d = D
    external_pitch_basic = thread_size - (0.649519 * pitch)  # d2 = D - 0.75H
    external_minor_basic = thread_size - (1.082532 * pitch)  # d1 = D - 1.25H

    # Internal thread (nut):
    internal_major_basic = thread_size      # D = nominal
    internal_pitch_basic = thread_size - (0.649519 * pitch)  # D2 = D - 0.75H (same as external)
    internal_minor_basic = thread_size - (1.082532 * pitch)  # D1 = D - 1.25H

    # --- ISO 965-1 Tolerances ---
    # Tolerance calculations based on ISO 965-1 formulas
    # These are simplified but more accurate than previous version

    # Pitch diameter tolerance (TD2 for grade 6, varies by pitch range)
    if pitch <= 0.8:
        TD2 = 0.090 * (pitch ** 0.4) * (thread_size ** 0.1)
    elif pitch <= 2.8:
        TD2 = 0.095 * (pitch ** 0.4) * (thread_size ** 0.1)
    else:
        TD2 = 0.100 * (pitch ** 0.4) * (thread_size ** 0.1)

    # Major/Minor diameter tolerances (simplified formulas)
    Td = 0.18 * (pitch ** 0.8)  # Major diameter tolerance
    T1 = TD2  # Minor diameter tolerance ≈ pitch diameter tolerance

    TOL = {
        "external": {
            "6g": {
                "major_max": -0.024 * pitch,  # Fundamental deviation 'g'
                "major_min": -(0.024 * pitch + Td),
                "pitch_max": -0.024 * pitch,  # Fundamental deviation 'g'
                "pitch_min": -(0.024 * pitch + TD2),
                "minor_max": 0.0,  # Not limited
                "minor_min": 0.0,  # Not limited (informational only)
            }
        },
        "internal": {
            "6H": {
                "major_max": TD2,  # Opens up to accommodate bolt
                "major_min": 0.0,  # Fundamental deviation 'H' = 0
                "pitch_max": TD2,  # Grade 6 tolerance
                "pitch_min": 0.0,  # Fundamental deviation 'H' = 0
            }
        }
    }

    # --- Validate tolerance classes ---
    if tol_external not in TOL["external"]:
        raise ValueError(f"Unsupported external tolerance class '{tol_external}'. Available: {list(TOL['external'].keys())}")
    if tol_internal not in TOL["internal"]:
        raise ValueError(f"Unsupported internal tolerance class '{tol_internal}'. Available: {list(TOL['internal'].keys())}")

    # --- EXTERNAL THREAD (bolt) ---
    ext_major_max = external_major_basic + TOL["external"][tol_external]["major_max"]
    ext_major_min = external_major_basic + TOL["external"][tol_external]["major_min"]

    ext_pitch_max = external_pitch_basic + TOL["external"][tol_external]["pitch_max"]
    ext_pitch_min = external_pitch_basic + TOL["external"][tol_external]["pitch_min"]

    # Minor diameter is not precisely controlled for external threads
    ext_minor_max = external_minor_basic  # Informational
    ext_minor_min = external_minor_basic  # Informational

    # --- INTERNAL THREAD (nut) ---
    int_major_max = internal_major_basic + TOL["internal"][tol_internal]["major_max"]
    int_major_min = internal_major_basic + TOL["internal"][tol_internal]["major_min"]

    int_pitch_max = internal_pitch_basic + TOL["internal"][tol_internal]["pitch_max"]
    int_pitch_min = internal_pitch_basic + TOL["internal"][tol_internal]["pitch_min"]

    # Minor diameter for internal threads (not directly specified in ISO, calculated)
    int_minor_max = internal_minor_basic + TD2
    int_minor_min = internal_minor_basic

    # Tapping drill diameter (typically minor diameter for ~75% thread engagement)
    tapping_drill = round(internal_minor_basic, 4)

    # --- Thread Depth & Runouts (Dynamic formula, from ISO machining rules) ---
    thread_depth = round(thread_size * 2.0, 4)       # Thread depth = 2.0 × nominal (practical machining depth)
    thread_runout = round(pitch * 2.5, 4)            # Runout ≈ 2.5 × pitch (standard machining practice)

    return {
        "External": {
            "Major Max": ext_major_max,
            "Major Min": ext_major_min,
            "Pitch Max": ext_pitch_max,
            "Pitch Min": ext_pitch_min,
            "Minor Max": ext_minor_max,
            "Minor Min": ext_minor_min,
        },
        "Internal": {
            "Major Max": int_major_max,
            "Major Min": int_major_min,
            "Pitch Max": int_pitch_max,
            "Pitch Min": int_pitch_min,
            "Minor Max": int_minor_max,
            "Minor Min": int_minor_min,
            "Tap Drill": tapping_drill,
        },
        "Manufacturing": {
            "Thread Depth": thread_depth,
            "Thread Runout": thread_runout,
        }
    }


# ------------------ GUI APPLICATION -------------------
class ThreadCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ISO Metric Thread Calculator for AutoDesk Inventor")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        self.current_result = None

        # Configure style
        style = ttk.Style()
        style.theme_use('clam')

        # Main container
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="ISO Metric Thread Calculator",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Author credit
        author_label = ttk.Label(main_frame, text="by Paradorn Katananon",
                                font=('Arial', 9, 'italic'))
        author_label.grid(row=1, column=0, columnspan=3, pady=(0, 5))

        # Input Frame
        input_frame = ttk.LabelFrame(main_frame, text="Thread Parameters", padding="10")
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        input_frame.columnconfigure(1, weight=1)

        # Thread Size
        ttk.Label(input_frame, text="Thread Size (mm):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.size_var = tk.StringVar(value="20")
        size_entry = ttk.Entry(input_frame, textvariable=self.size_var, width=20)
        size_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Label(input_frame, text="(e.g., 20 for M20)").grid(row=0, column=2, sticky=tk.W, pady=5)

        # Pitch
        ttk.Label(input_frame, text="Pitch (mm):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.pitch_var = tk.StringVar(value="2.0")
        pitch_entry = ttk.Entry(input_frame, textvariable=self.pitch_var, width=20)
        pitch_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Label(input_frame, text="(e.g., 2.0)").grid(row=1, column=2, sticky=tk.W, pady=5)

        # External Tolerance
        ttk.Label(input_frame, text="External Tolerance:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.ext_tol_var = tk.StringVar(value="6g")
        ext_tol_combo = ttk.Combobox(input_frame, textvariable=self.ext_tol_var,
                                     values=["6g"], state="readonly", width=18)
        ext_tol_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Label(input_frame, text="(Bolt)").grid(row=2, column=2, sticky=tk.W, pady=5)

        # Internal Tolerance
        ttk.Label(input_frame, text="Internal Tolerance:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.int_tol_var = tk.StringVar(value="6H")
        int_tol_combo = ttk.Combobox(input_frame, textvariable=self.int_tol_var,
                                     values=["6H"], state="readonly", width=18)
        int_tol_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Label(input_frame, text="(Nut)").grid(row=3, column=2, sticky=tk.W, pady=5)

        # Buttons Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)

        calc_button = ttk.Button(button_frame, text="Calculate", command=self.calculate)
        calc_button.grid(row=0, column=0, padx=5)

        export_button = ttk.Button(button_frame, text="Export to CSV", command=self.export_csv)
        export_button.grid(row=0, column=1, padx=5)

        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_results)
        clear_button.grid(row=0, column=2, padx=5)

        # Results Frame
        results_frame = ttk.LabelFrame(main_frame, text="Calculation Results", padding="10")
        results_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        main_frame.rowconfigure(4, weight=1)

        # Create scrollable text widget for results
        result_scroll = ttk.Scrollbar(results_frame)
        result_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_text = tk.Text(results_frame, wrap=tk.WORD, height=25, width=100,
                                   yscrollcommand=result_scroll.set, font=('Courier', 9))
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        result_scroll.config(command=self.result_text.yview)

        # Configure text tags for formatting
        self.result_text.tag_configure("header", font=('Courier', 10, 'bold'), foreground='blue')
        self.result_text.tag_configure("section", font=('Courier', 9, 'bold'), foreground='darkgreen')
        self.result_text.tag_configure("value", font=('Courier', 9))

    def calculate(self):
        try:
            size = float(self.size_var.get())
            pitch = float(self.pitch_var.get())
            tol_ext = self.ext_tol_var.get()
            tol_int = self.int_tol_var.get()

            self.current_result = calc_metric_thread(size, pitch, tol_ext, tol_int)

            # Display results
            self.display_results(size, pitch, tol_ext, tol_int, self.current_result)

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Calculation Error", f"Unexpected error: {e}")

    def display_results(self, size, pitch, tol_ext, tol_int, result):
        self.result_text.delete(1.0, tk.END)

        ext = result['External']
        inr = result['Internal']
        mfg = result['Manufacturing']

        thread_designation = f"M{int(size)}x{pitch}"

        # Header
        self.result_text.insert(tk.END, f"{'='*80}\n", "header")
        self.result_text.insert(tk.END, f"  ISO METRIC THREAD CALCULATION RESULTS\n", "header")
        self.result_text.insert(tk.END, f"  Thread: {thread_designation}\n", "header")
        self.result_text.insert(tk.END, f"{'='*80}\n\n", "header")

        # External Thread (Bolt)
        self.result_text.insert(tk.END, f"EXTERNAL THREAD (BOLT) - Tolerance Class: {tol_ext}\n", "section")
        self.result_text.insert(tk.END, f"{'-'*80}\n", "section")
        self.result_text.insert(tk.END, f"  Major Diameter:  Max = {ext['Major Max']:9.4f} mm    Min = {ext['Major Min']:9.4f} mm\n", "value")
        self.result_text.insert(tk.END, f"  Pitch Diameter:  Max = {ext['Pitch Max']:9.4f} mm    Min = {ext['Pitch Min']:9.4f} mm\n", "value")
        self.result_text.insert(tk.END, f"  Minor Diameter:  Max = {ext['Minor Max']:9.4f} mm    Min = {ext['Minor Min']:9.4f} mm\n\n", "value")

        # Internal Thread (Nut)
        self.result_text.insert(tk.END, f"INTERNAL THREAD (NUT) - Tolerance Class: {tol_int}\n", "section")
        self.result_text.insert(tk.END, f"{'-'*80}\n", "section")
        self.result_text.insert(tk.END, f"  Major Diameter:  Max = {inr['Major Max']:9.4f} mm    Min = {inr['Major Min']:9.4f} mm\n", "value")
        self.result_text.insert(tk.END, f"  Pitch Diameter:  Max = {inr['Pitch Max']:9.4f} mm    Min = {inr['Pitch Min']:9.4f} mm\n", "value")
        self.result_text.insert(tk.END, f"  Minor Diameter:  Max = {inr['Minor Max']:9.4f} mm    Min = {inr['Minor Min']:9.4f} mm\n", "value")
        self.result_text.insert(tk.END, f"  Tap Drill Size:       {inr['Tap Drill']:9.4f} mm\n\n", "value")

        # Manufacturing Data
        self.result_text.insert(tk.END, f"MANUFACTURING PARAMETERS\n", "section")
        self.result_text.insert(tk.END, f"{'-'*80}\n", "section")
        self.result_text.insert(tk.END, f"  Thread Depth:         {mfg['Thread Depth']:9.4f} mm\n", "value")
        self.result_text.insert(tk.END, f"  Thread Runout:        {mfg['Thread Runout']:9.4f} mm\n\n", "value")

        self.result_text.insert(tk.END, f"{'='*80}\n", "header")

    def export_csv(self):
        if self.current_result is None:
            messagebox.showwarning("No Data", "Please calculate thread parameters before exporting.")
            return

        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"thread_M{self.size_var.get()}x{self.pitch_var.get()}.csv"
            )

            if filename:
                size = float(self.size_var.get())
                pitch = float(self.pitch_var.get())
                ext = self.current_result['External']
                inr = self.current_result['Internal']
                mfg = self.current_result['Manufacturing']

                thread_designation = f"M{int(size)}x{pitch}"

                with open(filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)

                    # Header row
                    writer.writerow([
                        "Size", "Suffix", "Thread Designation", "Custom Thread Designation", "Pitch",
                        "Class", "Max", "Min", "Max", "Min", "Max", "Min", "",
                        "Class", "Min", "Max", "Min", "Max", "Min", "Max",
                        "Tap Drill", "Thread Depth", "Thread Runout"
                    ])

                    # Data row
                    writer.writerow([
                        int(size),                      # Size (Col A)
                        "",                             # Suffix (Col B)
                        thread_designation,             # Thread Designation (Col C)
                        "",                             # Custom Thread Designation (Col D)
                        pitch,                          # Pitch (Col E)
                        self.ext_tol_var.get(),        # External Class (Col F)
                        f"{ext['Major Max']:.4f}",     # External Major Max (Col G)
                        f"{ext['Major Min']:.4f}",     # External Major Min (Col H)
                        f"{ext['Pitch Max']:.4f}",     # External Pitch Max (Col I)
                        f"{ext['Pitch Min']:.4f}",     # External Pitch Min (Col J)
                        f"{ext['Minor Max']:.4f}",     # External Minor Max (Col K)
                        f"{ext['Minor Min']:.4f}",     # External Minor Min (Col L)
                        "",                             # (Col M)
                        self.int_tol_var.get(),        # Internal Class (Col N)
                        f"{inr['Minor Min']:.4f}",     # Internal Minor Min (Col O)
                        f"{inr['Minor Max']:.4f}",     # Internal Minor Max (Col P)
                        f"{inr['Pitch Min']:.4f}",     # Internal Pitch Min (Col Q)
                        f"{inr['Pitch Max']:.4f}",     # Internal Pitch Max (Col R)
                        f"{inr['Major Min']:.4f}",     # Internal Major Min (Col S)
                        f"{inr['Major Max']:.4f}",     # Internal Major Max (Col T)
                        f"{inr['Tap Drill']:.4f}",     # Tap Drill (Col U)
                        f"{mfg['Thread Depth']:.4f}",  # Thread Depth (Col V)
                        f"{mfg['Thread Runout']:.4f}"  # Thread Runout (Col W)
                    ])

                messagebox.showinfo("Export Success", f"Data exported to:\n{filename}")

        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {e}")

    def clear_results(self):
        self.result_text.delete(1.0, tk.END)
        self.current_result = None


# ------------------ MAIN -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ThreadCalculatorGUI(root)
    root.mainloop()
