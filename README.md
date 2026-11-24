# Single-File Text Processor & Manipulator (CLI)

A lightweight, dependency-free command-line (CLI) tool built in Python for safely reading, analyzing, and manipulating single `.txt` files. Engineered exclusively with Python's standard library, it features atomic file writes, Turkish-aware character normalization, regex-based word replacement, colored diff previews, and a multi-step undo stack.

---

## Features

* **Basic File Statistics:** Calculates total lines, empty lines, and total word count.
* **Turkish-Aware Word Frequency Analysis:** Handles Turkish character case mapping (`İ` / `I` via `str.maketrans`) and strips punctuation to display the top *N* most frequent words in a dynamically aligned table.
* **Safe RegEx Word Replacement:** Uses `re.escape()` and negative lookarounds (`(?<!\w)` / `(?!\w)`) to perform case-insensitive, whole-token replacements—supporting both standard words and special character terms like `C++` or `config.json` without corrupting substrings.
* **Duplicate Line Removal with Diff Preview:** Detects duplicate non-empty lines while preserving blank lines, displaying a color-coded terminal preview (`KEEP` in green, `REMOVE` in red) before applying changes.
* **Atomic Safe Writes:** Prevents data corruption by writing changes to a temporary `.tmp` file in the target directory (`tempfile`), flushing buffers to disk (`flush` + `os.fsync`), and atomically replacing the original file via `os.replace()`.
* **Undo Mechanism:** Stores snapshots of file states in a history stack prior to every confirmed modification, allowing changes to be reverted step-by-step.

---

## Installation

This project relies solely on Python 3's standard library (`sys`, `os`, `re`, `collections`, `time`, `tempfile`). No external packages or `pip` installations are required.

```bash
git clone [https://github.com/ahmetakif-dev/](https://github.com/ahmetakif-dev/)<repo-name>.git
cd <repo-name>
Usage
Pass the target .txt file path directly as a command-line argument:
python main.py sample.txt
Or run the script without arguments to enter the file path interactively:
python main.py
Menu Options: 
OPTIONS:
1. Show basic statistics
2. Show most repeated words
3. Replace word(s) in the file
4. Undo last change
5. Remove duplicate lines
6. Exit
Roadmap (v2.0)
[ ] Decouple core business logic (FileManipulator) from terminal I/O (input/print) for UI reusability.

[ ] Migrate the undo history stack to a bounded collections.deque for memory efficiency.

[ ] Build a web interface on top of the decoupled core using Streamlit.
