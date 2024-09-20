# Cat Typing Detector

The **Cat Typing Detector** is a fun Python app that automatically detects when your cat is typing on your keyboard by recognizing specific typing patterns using lightweight machine learning. When cat-like typing is detected, the app redirects the activity to a friendly GUI window. It also integrates with the system tray, making it easy to run in the background and manage from the tray.

## Features

- Detects cat-like typing patterns using a machine learning model (Logistic Regression).
- Shows a special GUI window to notify the user when cat typing is detected.
- Includes a "Let me use my computer!" button for dismissing the cat-typing window.
- Integrates into the system tray for background operation.
- Tray menu allows the user to start, stop, or exit the detector easily.
- Works on macOS, Windows, and Linux.

## Requirements

- Python 3.x
- Dependencies:
  - **PyQt5**: For the GUI window.
  - **pystray**: For system tray integration.
  - **Pillow**: For creating tray icons.
  - **scikit-learn**: For the machine learning model.
  - **pynput**: For detecting keyboard inputs.

### Installation

First, clone the repository and install the required dependencies:

```bash
git clone <repo-url>
cd CatTypingDetector
pip install -r requirements.txt
```

### Running the Application

Simply run the Python script to start the system tray application:

```bash
python cat_typing_detector.py
```

Once running, you’ll find the tray icon in your system tray. From there, you can:

    Start the cat typing detector.
    Stop it.
    Exit the application.

When the detector finds cat-like typing, it will pop up a window prompting you to enter "human" or click a button to dismiss the message.

### Packaging for macOS

To package the app for macOS:

Install py2app:

```bash
pip install py2app
```

Run the setup script to build the app:

```bash
python setup.py py2app
```

### Packaging for Windows

To create a standalone executable for Windows:

Install PyInstaller:

```bash
pip install pyinstaller
```

Generate the executable:

```bash
pyinstaller --onefile --windowed cat_typing_detector.py
```
### Packaging for Linux

For Linux, you can run the app as a background process using the nohup command:

```bash
nohup python cat_typing_detector.py &
```

Alternatively, you can create a systemd service for starting the app at boot.
### License

This project is licensed under the WTFPL. In short, you can do whatever the fuck you want with this software.

Happy coding! And keep those cats from sending too many keyboard messages! 😸

