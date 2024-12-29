import os
import subprocess
import core.module
import core.widget
import core.input

class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.display_text))

        self.__display_text = "📸"  # Set the button text/icon
        self.__tooltip_text = "Click to take a screenshot"

        # Register a click handler
        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.take_screenshot)

    def display_text(self, widget):
        """Return the text/icon to display in the bar."""
        return self.__display_text

    def take_screenshot(self, widget=None):
        """Run the screenshot command."""
        # Path to your external shell script
        script_path = os.path.expanduser("~/.config/scr.py")

        try:
            # Run the script in the background without opening a terminal
            subprocess.run(
                f"nohup python {script_path} &",
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,  # Suppress output
                stderr=subprocess.DEVNULL   # Suppress errors
            )
            self.__display_text = "✔️"  # Temporary success indicator
        except subprocess.CalledProcessError as e:
            self.__display_text = "❌"  # Temporary error indicator
            print(f"Error running screenshot script: {e}")
        finally:
            # Reset the text/icon after 2 seconds
            self.reset_display_text()

    def reset_display_text(self):
        """Reset the button text/icon to its original state."""
        self.__display_text = "📸"

    def state(self, widget):
        """Return the widget's state."""
        return "default"
