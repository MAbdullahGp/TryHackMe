# Vim: Practical Terminal Editing & Command Cheatsheet

![Category](https://img.shields.io/badge/Category-Tools-blue.svg)
![Editor](https://img.shields.io/badge/Editor-Vim-brightgreen.svg)
![Platform](https://img.shields.io/badge/Platform-Cross--Platform-lightgrey.svg)

A complete practical guide and reference manual for **Vim**, tailored for penetration testers modifying exploit scripts, configuration files, and payloads in headless terminal environments.

---

## 📋 Executive Summary
Vim is a ubiquitous, highly efficient modal text editor present on virtually every Unix-like system. Mastery of Vim is critical during terminal-only engagements where graphical IDEs are unavailable.

* **Artifacts in Directory:**
  * `hello.txt`: Hands-on training file designed for practicing navigation, line deletion, and regex substitution.

---

## 🧭 Modal Editing Fundamentals

Vim operates in distinct modes:
* **Normal Mode (Esc):** Navigation, commands, and deletion.
* **Insert Mode (`i` / `a`):** Typing and editing text.
* **Visual Mode (`v` / `Ctrl+v`):** Highlighting blocks of text.
* **Command-Line Mode (`:`):** Saving, quitting, and global find/replace.

---

## ⌨️ Essential Keystrokes & Cheatsheet

### 🏃 Navigation (Normal Mode)
* `h`, `j`, `k`, `l`: Move cursor left, down, up, right
* `w` / `b`: Jump forward / backward by word
* `0` / `$`: Jump to beginning / end of line
* `gg` / `G`: Jump to start / end of file
* `:45`: Jump directly to line 45

### ✂️ Editing & Deletion
* `x`: Delete character under cursor
* `dw`: Delete word
* `dd`: Delete entire line (cut)
* `yy`: Copy (yank) entire line
* `p`: Paste after cursor
* `u`: Undo last action
* `Ctrl + r`: Redo

### 🔍 Search & Replace
* `/pattern`: Search forward for `pattern` (`n` for next match, `N` for previous)
* `:%s/old/new/g`: Replace all instances of `old` with `new` across the entire file
* `:%s/old/new/gc`: Replace with interactive confirmation prompt

### 💾 Saving & Quitting
* `:w`: Save (write)
* `:q`: Quit
* `:wq` or `ZZ`: Save and quit
* `:q!`: Quit without saving changes

---

## 🏋️ Interactive Practice Exercise (`hello.txt`)

Using the included `hello.txt` file:
1. Practice navigating between words using `w` and `b`.
2. Practice deleting duplicate lines using `dd`.
3. Practice replacing strings:
   ```text
   :%s/lazy/energetic/g
   ```
