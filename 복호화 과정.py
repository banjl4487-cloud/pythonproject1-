import os
import base64

import cryptography
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import traceback




# --- 키 파생 함수 정의 (암호화/복호화 공통) ---
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode('utf-8'))
    return base64.urlsafe_b64encode(key)

# --- 상수 정의 ---
CORRECT_KEY_PASSWORD = "pythonProject1"  # 반드시 암호화 시 비밀번호와 동일해야 함
ENCRYPTED_FILE_NAME = "encrypted_personal_data.bin"
SALT_FILE_NAME = "salt.bin"
DECRYPTED_NORMAL_OUTPUT_FILE_NAME = "decrypted_personal_data_normal.csv"

print("\n--- 암호화된 파일 복호화 시작 ---")

try:
    # 솔트 불러오기
    with open(SALT_FILE_NAME, "rb") as f:
        loaded_salt = f.read()
    print(f"[*] '{SALT_FILE_NAME}' 파일에서 솔트 로드 완료.")

    # 암호화된 데이터 불러오기
    with open(ENCRYPTED_FILE_NAME, 'rb') as f:
        encrypted_data = f.read()
    print(f"[*] '{ENCRYPTED_FILE_NAME}' 파일 로드 완료.")

    # 복호화 키 생성
    decryption_key_bytes = derive_key(CORRECT_KEY_PASSWORD, loaded_salt)
    decryption_key_str = decryption_key_bytes.decode('utf-8')
    print(f"--- [복호화 시점] 재생성된 최종 키 (Base64): '{decryption_key_str}' ---")

    # Fernet 복호화기 초기화
    fernet_decryptor = Fernet(decryption_key_bytes)
    print("[*] Fernet 복호화기 초기화 완료.")

    # 데이터 복호화
    decrypted_bytes = fernet_decryptor.decrypt(encrypted_data)

    # 복호화된 데이터를 CSV 파일로 저장
    with open(DECRYPTED_NORMAL_OUTPUT_FILE_NAME, 'w', encoding='utf-8') as decrypted_csv_file:
        decrypted_csv_file.write(decrypted_bytes.decode('utf-8'))
    print("\n--- 복호화 과정 완료 ---")

except FileNotFoundError as e:
    print(f"[!] 오류: 필요한 파일이 없습니다. {e}")
    traceback.print_exc()
except cryptography.fernet.InvalidToken:
    print("[!] 🚨 InvalidToken 에러: 비밀번호 또는 솔트 불일치 가능성이 큽니다.")
    traceback.print_exc()
except Exception as e:
    print(f"[!] 예상치 못한 오류 발생: {type(e).__name__} - {e}")
    traceback.print_exc()