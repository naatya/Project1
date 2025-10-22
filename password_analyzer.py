# filename: password_analyzer.py
# filename: password_analyzer.py
# FINAL PROJECT CODE with Tkinter GUI

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import itertools
from zxcvbn import zxcvbn

# Leetspeak mappings (common substitutions)
LEET_MAP = {
    'a': ['4', '@'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'], 
    's': ['5', '$'], 't': ['7'], 'z': ['2']
}

# --- CORE LOGIC FUNCTIONS (Unchanged from CLI version) ---

def analyze_password_strength(password):
    """
    Analyzes the strength of the provided password using zxcvbn.
    Returns score, crack_time_display, warning, and suggestions.
    """
    if not password:
        return 0, "N/A", "Please enter a password.", [""]

    results = zxcvbn(password)

    score = results['score']
    suggestions = results['feedback']['suggestions']
    warning = results['feedback']['warning']
    crack_time_display = results['crack_times_display']['online_throttling_100_per_hour']
    
    return score, crack_time_display, warning, suggestions

def generate_wordlist(name, pet_name, dob_year, output_file):
    """
    Generates a custom wordlist based on personal inputs.
    """
    base_words = set()
    
    try:
        # 1. Base Words (Name, Pet, Year)
        if name:
            base_words.add(name.lower())
            base_words.add(name.capitalize())
        if pet_name:
            base_words.add(pet_name.lower())
            base_words.add(pet_name.capitalize())
        if dob_year:
            base_words.add(str(dob_year))

        # 2. Add Common Appends (Years, Symbols)
        appends = ['', '123', '!', '@', '1', '2024', str(dob_year), '00']
        temp_list = list(base_words)

        for word in temp_list:
            for append in appends:
                base_words.add(word + append)
        
        # 3. Generate Leetspeak Variations
        leet_list = set()
        for word in base_words:
            word = word.lower()
            possibilities = []
            for char in word:
                if char in LEET_MAP:
                    possibilities.append([char] + LEET_MAP[char])
                else:
                    possibilities.append([char])
            
            for combination in itertools.product(*possibilities):
                leet_list.add("".join(combination))
                
        base_words.update(leet_list)

        # 4. Generate Simple Combinations (Name + Pet)
        if name and pet_name:
            base_words.add(name.lower() + pet_name.lower())
            base_words.add(pet_name.lower() + name.lower())
            base_words.add(name.lower() + str(dob_year))
        
        final_wordlist = sorted([w for w in base_words if w])
        
        # Export to .txt file
        with open(output_file, 'w') as f:
            for word in final_wordlist:
                f.write(word + '\n')
        
        return True, len(final_wordlist)

    except Exception as e:
        return False, str(e)


# --- TKINTER GUI CLASS ---

class PasswordToolGUI:
    def __init__(self, master):
        self.master = master
        master.title("Project 4: Password Security Tool")

        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0')
        
        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")
        
        # --- Tab 1: Analyzer ---
        self.analyzer_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.analyzer_frame, text='Password Analyzer')
        self.create_analyzer_tab(self.analyzer_frame)
        
        # --- Tab 2: Generator ---
        self.generator_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.generator_frame, text='Wordlist Generator')
        self.create_generator_tab(self.generator_frame)

    # --- Analyzer Tab Setup ---
    def create_analyzer_tab(self, frame):
        # 1. Input Field
        ttk.Label(frame, text="Enter Password:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.password_entry = ttk.Entry(frame, width=40, show="*") # show="*" hides password
        self.password_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # 2. Analyze Button
        ttk.Button(frame, text="Analyze Strength", command=self.run_analyzer).grid(row=0, column=2, padx=10, pady=5)

        # 3. Results Display (Labels)
        ttk.Label(frame, text="Score (0-4):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.score_label = ttk.Label(frame, text="N/A", font=('Arial', 10, 'bold'))
        self.score_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(frame, text="Crack Time:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.time_label = ttk.Label(frame, text="N/A")
        self.time_label.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Feedback:").grid(row=4, column=0, padx=5, pady=5, sticky="nw")
        self.feedback_text = tk.Text(frame, height=5, width=40, wrap=tk.WORD)
        self.feedback_text.grid(row=4, column=1, columnspan=2, padx=5, pady=5)
        self.feedback_text.config(state=tk.DISABLED)

    def run_analyzer(self):
        password = self.password_entry.get()
        score, crack_time, warning, suggestions = analyze_password_strength(password)
        
        # Update Score Label Color
        if score == 4:
            color = 'green'
        elif score >= 2:
            color = 'orange'
        else:
            color = 'red'

        self.score_label.config(text=f"{score}/4", foreground=color)
        self.time_label.config(text=crack_time)
        
        # Update Feedback Text Box
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete('1.0', tk.END)
        
        feedback = []
        if warning:
            feedback.append(f"⚠️ Warning: {warning}")
        
        if suggestions:
            for s in suggestions:
                feedback.append(f"• {s}")
        
        if not feedback and score > 2:
            feedback.append("Great job! No major suggestions.")
        
        self.feedback_text.insert(tk.END, "\n".join(feedback))
        self.feedback_text.config(state=tk.DISABLED)

    # --- Generator Tab Setup ---
    def create_generator_tab(self, frame):
        # Input fields for generation
        
        # Name
        ttk.Label(frame, text="Target Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Pet Name
        ttk.Label(frame, text="Pet/Common Word:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.pet_entry = ttk.Entry(frame, width=30)
        self.pet_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Year
        ttk.Label(frame, text="DOB Year (e.g., 1990):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.year_entry = ttk.Entry(frame, width=30)
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)
        self.year_entry.insert(0, "2000") # Default value

        # Output File Selection
        ttk.Label(frame, text="Output File:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.output_entry = ttk.Entry(frame, width=30)
        self.output_entry.grid(row=3, column=1, padx=5, pady=5)
        self.output_entry.insert(0, "custom_wordlist.txt")
        
        # Generate Button
        ttk.Button(frame, text="GENERATE WORDLIST", command=self.run_generator).grid(row=4, column=0, columnspan=2, padx=10, pady=15)

    def run_generator(self):
        name = self.name_entry.get().strip()
        pet = self.pet_entry.get().strip()
        year = self.year_entry.get().strip()
        output_file = self.output_entry.get().strip()

        # Basic validation
        if not name:
            messagebox.showerror("Input Error", "Target Name is required for generation.")
            return
        
        # Get path using file dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=output_file,
            title="Save Wordlist As",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        
        if not file_path:
            return # User cancelled

        try:
            year_int = int(year)
        except ValueError:
            messagebox.showerror("Input Error", "Year must be a valid number.")
            return

        success, result = generate_wordlist(name, pet, year_int, file_path)
        
        if success:
            messagebox.showinfo(
                "Success", 
                f"Wordlist successfully generated!\nTotal Passwords: {result}\nSaved to: {file_path}"
            )
        else:
            messagebox.showerror("Generation Error", f"An error occurred: {result}")


# --- MAIN EXECUTION BLOCK ---

if __name__ == "__main__":
    # Ensure Tkinter is installed via apt on Linux if needed (python3-tk)
    # This block initiates the GUI
    root = tk.Tk()
    app = PasswordToolGUI(root)
    root.mainloop()