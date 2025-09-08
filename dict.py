import tkinter as tk
from tkinter import messagebox


# ---------------- Trie Data Structure ----------------
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]
        return self._get_words(node, prefix)

    def _get_words(self, node, prefix):
        words = []
        if node.is_end:
            words.append(prefix)
        for ch, next_node in node.children.items():
            words.extend(self._get_words(next_node, prefix + ch))
        return words


# ---------------- Edit Distance ----------------
def edit_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]


# ---------------- Load Words and Meanings ----------------
trie = Trie()
word_list = []
meanings_dict = {}

with open("words.txt") as f:
    for line in f:
        word = line.strip().lower()
        trie.insert(word)
        word_list.append(word)

with open("meanings.txt") as f:
    for line in f:
        if ':' in line:
            w, m = line.strip().split(":", 1)
            meanings_dict[w.lower()] = m.strip()


# ---------------- Tkinter GUI ----------------
def lookup_word():
    word = entry.get().strip().lower()
    if not word:
        messagebox.showinfo("Error", "Please enter a word!")
        return

    result_text.delete(1.0, tk.END)

    if trie.search(word):
        meaning = meanings_dict.get(word, "Meaning not available offline.")
        result_text.insert(tk.END, f"✔ Word found!\nMeaning: {meaning}\n")
    else:
        result_text.insert(tk.END, "❌ Word not found.\n")

        # Auto-suggestions
        suggestions = trie.starts_with(word[:2])[:5]
        if suggestions:
            result_text.insert(tk.END, f"Auto-suggestions: {', '.join(suggestions)}\n")

        # Spelling corrections
        corrections = [w for w in word_list if edit_distance(word, w) <= 2][:5]
        if corrections:
            result_text.insert(tk.END, f"Did you mean?: {', '.join(corrections)}\n")


# Tkinter window
window = tk.Tk()
window.title("Offline Word Lookup Dictionary")
window.geometry("500x400")

tk.Label(window, text="Enter Word:").pack(pady=5)
entry = tk.Entry(window, width=30)
entry.pack(pady=5)

tk.Button(window, text="Lookup", command=lookup_word).pack(pady=5)

result_text = tk.Text(window, height=15, width=60)
result_text.pack(pady=10)

window.mainloop()
