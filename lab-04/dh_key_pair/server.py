from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

# Hàm tạo tham số Diffie-Hellman
def generate_dh_parameters():
    parameters = dh.generate_parameters(generator=2, key_size=2048)  # Tạo tham số DH
    return parameters

# Hàm tạo cặp khóa DH cho server
def generate_server_key_pair(parameters):
    private_key = parameters.generate_private_key()  # Tạo khóa riêng
    public_key = private_key.public_key()  # Lấy khóa công khai từ khóa riêng
    return private_key, public_key

def main():
    # Tạo tham số DH
    parameters = generate_dh_parameters()

    # Tạo cặp khóa cho server
    private_key, public_key = generate_server_key_pair(parameters)

    # Lưu khóa công khai vào file
    with open("server_public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

# Kiểm tra nếu script được chạy trực tiếp
if __name__ == "__main__":
    main()