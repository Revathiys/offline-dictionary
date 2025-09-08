import customtkinter as ctk
import sqlite3
import pyttsx3
import json
from tkinter import messagebox, filedialog

# ---------------- Database Setup ----------------
def init_db():
    conn = sqlite3.connect("dictionary.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dictionary (
        word TEXT PRIMARY KEY,
        meaning TEXT
    )
    """)
    # Add some sample words
    data = [
        ("apple", "A sweet fruit that grows on trees."),
        ("application", "A formal request or a software program."),
        ("python", "A programming language that is powerful and easy to learn."),
        ("dictionary", "A collection of words and their meanings."),
        ("computer", "An electronic device that processes data."),
        ("student", "A person who is studying at a school or college."),
        ("teacher", "A person who helps students gain knowledge.")
    ]
    cursor.executemany("INSERT OR REPLACE INTO dictionary (word, meaning) VALUES (?, ?)", data)
    conn.commit()
    conn.close()

def lookup(word):
    conn = sqlite3.connect("dictionary.db")
    cursor = conn.cursor()
    cursor.execute("SELECT meaning FROM dictionary WHERE word = ?", (word,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# ---------------- Favorites & History ----------------
FAV_FILE = "favorites.json"
HIS_FILE = "history.json"

def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return []

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

favorites = load_json(FAV_FILE)
history = load_json(HIS_FILE)

def add_to_favorites(word):
    if word and word not in favorites:
        favorites.append(word)
        save_json(FAV_FILE, favorites)
        messagebox.showinfo("Saved", f"'{word}' added to favorites!")

def add_to_history(word):
    if word and word not in history:
        history.append(word)
        save_json(HIS_FILE, history)

# ---------------- Text-to-Speech ----------------
def speak_word(word):
    if not word:
        messagebox.showinfo("Error", "No word to speak!")
        return
    engine = pyttsx3.init()
    engine.say(word)
    engine.runAndWait()

# ---------------- Export ----------------
def export_to_txt():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            for w in history:
                meaning = lookup(w)
                f.write(f"{w}: {meaning}\n")
        messagebox.showinfo("Exported", f"History saved to {file_path}")

# ---------------- GUI ----------------
init_db()
app = ctk.CTk()
app.title("Advanced Offline Dictionary")
app.geometry("700x500")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Input Box
entry = ctk.CTkEntry(app, placeholder_text="Type a word...", width=400, height=40)
entry.pack(pady=20)

# Result Label
result_label = ctk.CTkLabel(app, text="", wraplength=600, justify="left", font=("Arial", 16))
result_label.pack(pady=20)

# Search Function
def search():
    word = entry.get().strip().lower()
    if not word:
        messagebox.showinfo("Error", "Please enter a word!")
        return
    meaning = lookup(word)
    if meaning:
        result_label.configure(text=f"✔ {word.capitalize()}:\n{meaning}")
        add_to_history(word)
    else:
        result_label.configure(text=f"❌ Word '{word}' not found in dictionary.")

# Buttons
search_btn = ctk.CTkButton(app, text="🔍 Search", command=search, width=200)
search_btn.pack(pady=5)

speak_btn = ctk.CTkButton(app, text="🔊 Speak", command=lambda: speak_word(entry.get()), width=200)
speak_btn.pack(pady=5)

fav_btn = ctk.CTkButton(app, text="⭐ Add to Favorites", command=lambda: add_to_favorites(entry.get().strip().lower()), width=200)
fav_btn.pack(pady=5)

export_btn = ctk.CTkButton(app, text="📤 Export History", command=export_to_txt, width=200)
export_btn.pack(pady=5)

# Show Favorites & History
def show_favorites():
    favs = "\n".join(favorites) if favorites else "No favorites yet."
    messagebox.showinfo("Favorites", favs)

def show_history():
    his = "\n".join(history) if history else "No history yet."
    messagebox.showinfo("History", his)

fav_list_btn = ctk.CTkButton(app, text="📚 Show Favorites", command=show_favorites, width=200)
fav_list_btn.pack(pady=5)

his_list_btn = ctk.CTkButton(app, text="📖 Show History", command=show_history, width=200)
his_list_btn.pack(pady=5)

# Run Application
app.mainloop()
