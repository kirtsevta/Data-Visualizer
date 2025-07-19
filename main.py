import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt

class DataVisualizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("📊 Interactive Data Visualizer")
        self.master.geometry("950x680")
        self.master.configure(bg="#e8f0fe")  # Soft gradient-like background

        self.df = None

        # Header
        tk.Label(master, text="📊 Interactive Data Visualizer", font=("Segoe UI", 24, "bold"),
                 bg="#e8f0fe", fg="#2c3e50").pack(pady=(20, 10))

        # Setup ttk styles
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=8)
        style.configure("TLabel", background="#e8f0fe", font=("Segoe UI", 10))
        style.configure("TCombobox", font=("Segoe UI", 10), padding=4)

        # Upload button
        self.upload_btn = tk.Button(master, text="📂 Upload CSV File", command=self.upload_file,
                                    font=("Segoe UI", 11, "bold"), bg="#28a745", fg="white", bd=0,
                                    activebackground="#218838", activeforeground="white", padx=15, pady=5)
        self.upload_btn.pack(pady=10)

        # Chart type
        ttk.Label(master, text="Select Chart Type:").pack()
        self.chart_type = ttk.Combobox(master, values=["Bar Chart", "Line Plot", "Pie Chart", "Scatter Plot", "Histogram"], state="readonly")
        self.chart_type.current(0)
        self.chart_type.pack(pady=5)

        # Marker Style
        ttk.Label(master, text="Select Marker Style (for Line/Scatter):").pack()
        self.marker_style = ttk.Combobox(master, values=["o (Circle)", "s (Square)", "^ (Triangle)", "* (Star)", "x (Cross)", "d (Diamond)"], state="readonly")
        self.marker_style.current(0)
        self.marker_style.pack(pady=5)

        # Marker Color
        ttk.Label(master, text="Select Marker Color:").pack()
        self.marker_color = ttk.Combobox(master, values=["blue", "red", "green", "orange", "purple", "black", "brown"], state="readonly")
        self.marker_color.current(0)
        self.marker_color.pack(pady=5)

        # Columns listbox
        ttk.Label(master, text="Select Columns:").pack(pady=(10, 0))
        self.column_frame = tk.Frame(master, bg="#ffffff", highlightbackground="#cccccc", highlightthickness=1)
        self.column_frame.pack(pady=10)
        self.column_listbox = tk.Listbox(self.column_frame, selectmode="multiple", exportselection=False,
                                         font=("Consolas", 10), width=60, height=12, bg="#ffffff", relief="flat")
        self.column_listbox.pack()

        # Generate button
        self.generate_btn = tk.Button(master, text="📊 Generate Chart", command=self.generate_chart,
                                      font=("Segoe UI", 12, "bold"), bg="#007bff", fg="white", bd=0,
                                      activebackground="#0056b3", activeforeground="white", padx=20, pady=7)
        self.generate_btn.pack(pady=15)

        # Status label
        self.status_label = tk.Label(master, text="", fg="green", bg="#e8f0fe", font=("Segoe UI", 10, "italic"))
        self.status_label.pack()

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[["CSV files", "*.csv"]])
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                self.column_listbox.delete(0, tk.END)
                for col in self.df.columns:
                    self.column_listbox.insert(tk.END, col)
                self.status_label.config(text="✅ File loaded successfully!", fg="green")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read CSV:\n{e}")
                self.status_label.config(text="❌ Failed to load file.", fg="red")

    def generate_chart(self):
        if self.df is None:
            self.status_label.config(text="⚠️ Please upload a CSV file first.", fg="red")
            return

        selected_indices = self.column_listbox.curselection()
        selected_columns = [self.column_listbox.get(i) for i in selected_indices]
        chart = self.chart_type.get()
        marker = self.marker_style.get().split()[0]
        color = self.marker_color.get()

        if chart in ["Bar Chart", "Line Plot", "Histogram"] and not selected_columns:
            self.status_label.config(text="⚠️ Select at least one column.", fg="red")
            return
        if chart == "Scatter Plot" and len(selected_columns) != 2:
            self.status_label.config(text="⚠️ Scatter plot needs 2 numeric columns.", fg="red")
            return
        if chart == "Pie Chart" and len(selected_columns) != 1:
            self.status_label.config(text="⚠️ Pie chart needs 1 column.", fg="red")
            return

        try:
            plt.figure(figsize=(10, 6))

            if chart == "Bar Chart":
                ax = self.df[selected_columns].sum().plot(kind='bar', color='skyblue', edgecolor='black')
                for p in ax.patches:
                    ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2, p.get_height()),
                                ha='center', va='bottom')
                plt.legend(selected_columns, title="Columns")

            elif chart == "Line Plot":
                for col in selected_columns:
                    plt.plot(self.df[col], marker=marker, label=col, color=color)
                plt.legend(title="Columns")

            elif chart == "Pie Chart":
                counts = self.df[selected_columns[0]].value_counts()
                top_counts = counts[:10]
                others = counts[10:].sum()
                if others > 0:
                    top_counts["Others"] = others
                top_counts.plot(kind='pie', autopct='%1.1f%%', label="")
                plt.title(f"Pie Chart of {selected_columns[0]} (Top 10 + Others)")
                plt.ylabel("")

            elif chart == "Scatter Plot":
                x, y = selected_columns
                plt.scatter(self.df[x], self.df[y], marker=marker, color=color, edgecolors='black', label=f"{x} vs {y}")
                plt.legend(title="Scatter")

            elif chart == "Histogram":
                self.df[selected_columns].plot(kind='hist', bins=30, alpha=0.7, edgecolor='black')
                plt.legend(title="Columns")

            plt.title(chart, fontsize=14, fontweight='bold')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
            self.status_label.config(text="✅ Chart generated successfully.", fg="green")

        except Exception as e:
            messagebox.showerror("Error", f"Chart failed:\n{e}")
            self.status_label.config(text="❌ Chart generation failed.", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizerApp(root)
    root.mainloop()
