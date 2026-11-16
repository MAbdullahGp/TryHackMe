# Tmux: Terminal Multiplexer Cheatsheet & Productivity Guide

![Category](https://img.shields.io/badge/Category-Productivity-blue.svg)
![Tool](https://img.shields.io/badge/Tool-tmux-orange.svg)
![Platform](https://img.shields.io/badge/Platform-Linux-success.svg)

A complete reference guide and visual cheatsheet for **tmux** (Terminal Multiplexer), indispensable for managing multi-stage penetration tests, interactive reverse shells, and long-running network scans.

---

## 📋 Executive Summary
When conducting security assessments, losing an active reverse shell or network scan due to an interrupted SSH connection can jeopardize engagement progress. `tmux` ensures persistent terminal sessions that continue running on remote or local workstations regardless of client disconnection.

* **Artifacts in Directory:**
  * `img.png`: Comprehensive visual cheatsheet mapping tmux commands, splits, and hotkeys.

---

## ⌨️ Essential Keyboard Shortcuts

The default tmux prefix key is **`Ctrl + b`**. Press the prefix, release, and then press the desired command key:

### 🪟 Session Management
| Command | Action |
| :--- | :--- |
| `tmux new -s <name>` | Launch a new named session |
| `tmux ls` | List active running sessions |
| `tmux attach -t <name>` | Attach to an existing session |
| `Ctrl + b` then `d` | Detach safely from the current session |
| `tmux kill-session -t <name>` | Terminate a specific session |

---

### 📑 Window Management (Tabs)
| Shortcut | Action |
| :--- | :--- |
| `Ctrl + b` then `c` | Create a new window |
| `Ctrl + b` then `n` / `p` | Switch to Next / Previous window |
| `Ctrl + b` then `0-9` | Jump directly to window number |
| `Ctrl + b` then `,` | Rename current window |
| `Ctrl + b` then `&` | Kill current window |

---

### 🔲 Pane Management (Splits)
| Shortcut | Action |
| :--- | :--- |
| `Ctrl + b` then `"` | Split active pane **horizontally** (top/bottom) |
| `Ctrl + b` then `%` | Split active pane **vertically** (left/right) |
| `Ctrl + b` then `Arrow Keys` | Navigate between active panes |
| `Ctrl + b` then `z` | Toggle zoom active pane to full screen |
| `Ctrl + b` then `x` | Close active pane |
| `Ctrl + b` then `q` | Display pane index numbers |

---

### 📜 Scroll & Copy Mode (Buffer History)
1. Enter copy mode: **`Ctrl + b` then `[`**
2. Navigate terminal history using arrow keys, `PgUp`/`PgDn`, or Vim motion keys (`h`, `j`, `k`, `l`).
3. Press **`Space`** to begin text selection.
4. Press **`Enter`** to copy selected text to the buffer.
5. Paste buffer: **`Ctrl + b` then `]`**
6. Exit copy mode: **`q`**

---

## ⚙️ Recommended `~/.tmux.conf` Configuration

```tmux
# Enable mouse support (clicking, resizing, scrolling)
set -g mouse on

# Set 256-color support
set -g default-terminal "screen-256color"

# Increase scrollback history limit
set -g history-limit 10000

# Remap split keys to more intuitive shortcuts
bind | split-window -h
bind - split-window -v
```
