# Sway Screenshot Tool

A Python script for taking screenshots on the [Sway](https://swaywm.org/) Wayland compositor.

## Features

- Select windows or regions to capture.
- Automatically names files based on window names.
- Saves screenshots to `~/Pictures/Screenshots`.
- Copies screenshots to the clipboard.
- Sends desktop notifications.

## Prerequisites

Ensure you have the following dependencies installed:

- **System Tools:**
  - `swaymsg`
  - `slurp`
  - `grim`
  - `wl-copy` (part of `wl-clipboard`)
  - `notify-send` (from `libnotify`)

- **Python Version:**
  - Python 3.x

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/sway-screenshot.git
cd sway-screenshot
```

### Install Dependencies

#### Arch Linux

```bash
sudo pacman -S sway slurp grim wl-clipboard libnotify
```

#### Debian/Ubuntu

```bash
sudo apt install sway slurp grim wl-clipboard libnotify-bin
```

### Make the Script Executable

```bash
chmod +x sway_screenshot.py
```

### Optional: Install to System Path

```bash
sudo cp sway_screenshot.py /usr/local/bin/sway-screenshot
```

## Usage

### Run the Script

```bash
./sway_screenshot.py
```

Or, if installed in the system path:

```bash
sway-screenshot
```

### Bind to a Key Combination in Sway

Add the following line to your Sway configuration file (`~/.config/sway/config`):

```bash
bindsym Print exec sway-screenshot
```

## Troubleshooting

If you encounter issues:

- Ensure that all dependencies are installed and accessible.
- Check the script's output for error messages.
- Verify that the script has executable permissions.
- Ensure that `sway-screenshot` is in your `PATH` if you installed it there.

## Contributing

Contributions are welcome! Please:

- Open an issue for bug reports or feature requests.
- Submit a pull request for code contributions.
