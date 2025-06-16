# Developer Email Test Tool

A modern, user-friendly tool for testing SMTP email delivery from your desktop. Built with PyQt5, it supports Gmail, Outlook, Yahoo, and custom SMTP providers, and is designed for developers and testers.

---

## Features
- Send test emails to any address using your SMTP credentials
- Supports Gmail, Outlook, Yahoo, and custom SMTP servers
- Secure app password input with show/hide toggle
- Settings dialog with persistent config
- Help dialog for finding app passwords for each provider
- Dark theme UI
- Custom window and executable icon
- Credit label at the bottom

---

## Screenshots
![screenshot](https://i.imgur.com/lwfsW3k.png) <!-- Add your screenshot here -->

---

## Requirements
- Python 3.7+
- PyQt5
- Pillow (if converting icons)

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Usage (Run from Source)
1. Place `rowdymail.ico` in the same directory as `email_tester_gui.py`.
2. Run the app:
   ```bash
   python email_tester_gui.py
   ```

---

## Packaging as Windows Executable (.exe)
1. Make sure `rowdymail.ico` is in the same directory.
2. Use the provided `email_tester_gui.spec` file for PyInstaller:
   ```bash
   pyinstaller email_tester_gui.spec
   ```
3. The `.exe` will be in the `dist/` folder, with the icon applied to both the window and the executable.

**Note:** If you change the icon, ensure it is a valid `.ico` file with multiple sizes (16x16, 32x32, 48x48, 256x256).

---

## App Passwords
- For Gmail, Outlook, and Yahoo, you must use an app password (not your main account password).
- Use the Help button in the Settings dialog for step-by-step instructions on generating app passwords for each provider.

---

## Credits
**Coded 💻 By: RowdyRaedon 😈**

---

## License
MIT License (or specify your own) 
