import sys
import os

# Thêm thư mục "lab-03" vào sys.path để Python có thể tìm thấy `ui/`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import requests
from ui.rsa import Ui_MainWindow  # Import giao diện

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối các nút với API
        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    # Gọi API tạo khóa
    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.show_message("Success", data["message"])
            else:
                self.show_message("Error", "API call failed")
        except requests.exceptions.RequestException as e:
            self.show_message("Error", str(e))

    # Gọi API mã hóa
    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {
            "message": self.ui.txt_plain_text.toPlainText(),
            "key_type": "public"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setPlainText(data["encrypted_message"])
                self.show_message("Success", "Encrypted Successfully")
            else:
                self.show_message("Error", "API call failed")
        except requests.exceptions.RequestException as e:
            self.show_message("Error", str(e))

    # Gọi API giải mã
    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        payload = {
            "ciphertext": self.ui.txt_cipher_text.toPlainText(),
            "key_type": "private"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setPlainText(data["decrypted_message"])
                self.show_message("Success", "Decrypted Successfully")
            else:
                self.show_message("Error", "API call failed")
        except requests.exceptions.RequestException as e:
            self.show_message("Error", str(e))

    # Gọi API ký số
    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_sign.setPlainText(data["signature"])  # Sử dụng setPlainText()
                self.show_message("Success", "Signed Successfully")
            else:
                self.show_message("Error", "API call failed")
        except requests.exceptions.RequestException as e:
            self.show_message("Error", str(e))

    # Gọi API xác minh chữ ký
    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText()  # Nếu là QLineEdit, dùng text()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data["is_verified"]:
                    self.show_message("Success", "Verified Successfully")
                else:
                    self.show_message("Error", "Verification Failed")
            else:
                self.show_message("Error", "API call failed")
        except requests.exceptions.RequestException as e:
            self.show_message("Error", str(e))

    # Hiển thị thông báo
    def show_message(self, title, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information if "Success" in title else QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
