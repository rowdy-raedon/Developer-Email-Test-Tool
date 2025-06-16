import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QMessageBox, QComboBox, QDialog
)
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
import sys, os
from PyQt5.QtCore import Qt

CONFIG_FILE = "config.txt"

SMTP_PROVIDERS = {
    "Gmail": "smtp.gmail.com",
    "Outlook": "smtp.office365.com",
    "Yahoo": "smtp.mail.yahoo.com",
    "Custom": ""
}

def load_config():
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    config[k] = v
    return config

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        for k, v in config.items():
            f.write(f"{k}={v}\n")

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ Settings")
        self.setFixedSize(300, 200)
        self.set_dark_theme()

        layout = QVBoxLayout()
        # Top bar with Help button
        top_row = QHBoxLayout()
        top_row.addStretch()
        self.help_btn = QPushButton("❓ Help")
        self.help_btn.setFixedWidth(70)
        self.help_btn.clicked.connect(self.open_help)
        top_row.addWidget(self.help_btn)
        layout.addLayout(top_row)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Your Email")
        layout.addWidget(self.email_input)

        pass_layout = QHBoxLayout()
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("App Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        pass_layout.addWidget(self.pass_input)
        self.show_pass_btn = QPushButton("Show")
        self.show_pass_btn.setCheckable(True)
        self.show_pass_btn.setFixedWidth(50)
        self.show_pass_btn.clicked.connect(self.toggle_password_visibility)
        pass_layout.addWidget(self.show_pass_btn)
        layout.addLayout(pass_layout)

        self.provider_select = QComboBox()
        self.provider_select.addItems(SMTP_PROVIDERS.keys())
        layout.addWidget(self.provider_select)

        self.custom_smtp = QLineEdit()
        self.custom_smtp.setPlaceholderText("Custom SMTP Server (if any)")
        layout.addWidget(self.custom_smtp)

        self.save_button = QPushButton("💾 Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.load_existing()

    def load_existing(self):
        config = load_config()
        self.email_input.setText(config.get("email", ""))
        self.pass_input.setText(config.get("password", ""))
        smtp = config.get("smtp", "")

        for key, value in SMTP_PROVIDERS.items():
            if smtp == value:
                self.provider_select.setCurrentText(key)
                self.custom_smtp.setText("")
                return
        self.provider_select.setCurrentText("Custom")
        self.custom_smtp.setText(smtp)

    def save_settings(self):
        selected = self.provider_select.currentText()
        smtp = SMTP_PROVIDERS[selected]
        if selected == "Custom":
            smtp = self.custom_smtp.text().strip()
        if not smtp:
            QMessageBox.warning(self, "Missing", "SMTP server required.")
            return

        config = {
            "email": self.email_input.text().strip(),
            "password": self.pass_input.text().strip(),
            "smtp": smtp
        }
        save_config(config)
        QMessageBox.information(self, "Saved", "Settings saved.")
        self.close()

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.setPalette(palette)
        self.setFont(QFont("Arial", 10))

    def toggle_password_visibility(self):
        if self.show_pass_btn.isChecked():
            self.pass_input.setEchoMode(QLineEdit.Normal)
            self.show_pass_btn.setText("Hide")
        else:
            self.pass_input.setEchoMode(QLineEdit.Password)
            self.show_pass_btn.setText("Show")

    def open_help(self):
        dlg = HelpDialog(self)
        dlg.exec_()

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help: Finding App Passwords")
        self.setFixedSize(400, 300)
        self.set_dark_theme()
        layout = QVBoxLayout()
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setPlainText(
            """
How to find your App Password for each provider:

Gmail:
1. Go to https://myaccount.google.com/security
2. Under 'Signing in to Google', select 'App Passwords'.
3. Generate a new app password for 'Mail'.

Outlook:
1. Go to https://account.live.com/proofs/Manage
2. Under 'App passwords', create a new app password.

Yahoo:
1. Go to https://login.yahoo.com/account/security
2. Under 'App Password', generate a new password for your app.

Custom:
- Refer to your provider's documentation for app password or SMTP credentials.
            """
        )
        layout.addWidget(help_text)
        self.setLayout(layout)
        self.set_dark_theme()

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.setPalette(palette)
        self.setFont(QFont("Arial", 10))

class EmailTester(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Developer Email Test Tool")
        if hasattr(sys, '_MEIPASS'):
            # Running as a PyInstaller bundle
            icon_path = os.path.join(sys._MEIPASS, "rowdymail.ico")
        else:
            icon_path = "rowdymail.ico"
        self.setWindowIcon(QIcon(icon_path))
        self.setGeometry(300, 300, 420, 150)
        self.set_dark_theme()

        layout = QVBoxLayout()

        top_bar = QHBoxLayout()
        self.to_input = QLineEdit()
        self.to_input.setPlaceholderText("Target Email")
        top_bar.addWidget(self.to_input)

        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.setFixedWidth(40)
        self.settings_btn.clicked.connect(self.open_settings)
        top_bar.addWidget(self.settings_btn)

        layout.addLayout(top_bar)

        self.send_button = QPushButton("🚀 Send Test Email")
        self.send_button.clicked.connect(self.send_email)
        layout.addWidget(self.send_button)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        # Add credit label at the bottom
        credit_label = QLabel("Coded 💻 By: RowdyRaedon 😈")
        credit_label.setAlignment(Qt.AlignCenter)
        credit_label.setStyleSheet("color: #aaa; font-size: 10pt; margin-top: 4px;")
        layout.addWidget(credit_label)

        self.setLayout(layout)
        self.config = load_config()

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.setPalette(palette)
        self.setFont(QFont("Arial", 10))

    def open_settings(self):
        dlg = SettingsDialog(self)
        dlg.exec_()
        self.config = load_config()

    def send_email(self):
        to_email = self.to_input.text()
        from_email = self.config.get("email", "")
        from_pass = self.config.get("password", "")
        smtp_server = self.config.get("smtp", "")

        if not all([from_email, from_pass, smtp_server]):
            QMessageBox.warning(self, "Config Missing", "Please set your email and SMTP in ⚙️ Settings.")
            return

        subject = "Test Email from Developer Email Test Tool"
        body_text = "Hello,\n\nThis is a test email sent from your Developer Email Test Tool.\n\nBest regards,\nRowdyRaedon"
        body_html = """
        <html>
          <body>
            <p>Hello,<br><br>
               This is a <b>test email</b> sent from your <i>Developer Email Test Tool</i>.<br><br>
               Best regards,<br>
               RowdyRaedon
            </p>
          </body>
        </html>
        """

        msg = MIMEMultipart("alternative")
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Date'] = formatdate(localtime=True)
        msg['Message-ID'] = make_msgid()
        msg['Reply-To'] = from_email

        part1 = MIMEText(body_text, 'plain')
        part2 = MIMEText(body_html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        try:
            server = smtplib.SMTP(smtp_server, 587)
            server.starttls()
            server.login(from_email, from_pass)
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            self.log_output.append(f"[+] Sent to {to_email}")
        except Exception as e:
            self.log_output.append(f"[-] Error: {e}")
            QMessageBox.critical(self, "Error", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tester = EmailTester()
    tester.show()
    sys.exit(app.exec_())
