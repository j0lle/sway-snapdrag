# Sway Snapdrag Tool

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
git clone https://github.com/j0lle/sway-snapdrag.git
cd sway-snapdrag
```

### Install Dependencies

#### Arch Linux

```bash
sudo pacman -S sway slurp grim wl-clipboard libnotify
```

## Usage

Use however you want! Some ideas:

### 1. Run the Script

```bash
python sway-snapdrag.py
```

### 2. Bind to a Key Combination in Sway

Add the following line to your Sway configuration file (`~/.config/sway/config`):

```bash
bindsym Print exec sway-snapdrag
```

### 3. Add to [bumblebee-status](https://github.com/tobi-wan-kenobi/bumblebee-status)

Copy bumblebee-status-snapdrag.py to your modules/contrib (`~/.config/bumblebee_status/modules/contrib/`) (or where you installed it):

```bash
cp bumblebee-status-snapdrag.py ~/.config/bumblebee_status/modules/contrib/
```

Now add it to your bar config in the Sway config file
e.g.: 
```
bar {
	status_command bumblebee-status -m git time date nic publicip cpu memory nvidiagpu disk docker_ps getcrypto bumblebee-status-snapdrag system -p getcrypto.getltc=0 nvidiagpu.format="GPU {temp}°C {mem_used}/{mem_total} MiB" -t zengarden
}
```
Then reload sway
```bash
sway reload
```

## Troubleshooting

If you encounter issues:

- Ensure that all dependencies are installed and accessible.
- Check the script's output for error messages.
- Verify that the script has executable permissions.
- Ensure that `sway-snapdrag` is in your `PATH` if you installed it there.

## Contributing

Contributions are welcome! Please:

- Open an issue for bug reports or feature requests.
- Submit a pull request for code contributions.
