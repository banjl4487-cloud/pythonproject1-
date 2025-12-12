import os
import base64
# import pandas as pd # 가짜 데이터 생성 함수를 삭제했으므로 pandas 임포트는 더 이상 필요 없습니다.
# from faker import Faker # 가짜 데이터 생성 함수를 삭제했으므로 faker 임포트는 더 이상 필요 없습니다.
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import traceback


# --- 초강력 1. 핵심 파생 함수 정의 (암호화/복호화 모두 이 함수를 사용한다!) ---
def derive_key(password: str, salt: bytes) -> bytes:
    """
    주어진 비밀번호와 솔트를 사용하여 Fernet 암호화 키를 파생합니다.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode('utf-8'))
    return base64.urlsafe_b64encode(key)


# --- 초강력 2. 시뮬레이션용 상수 정의 ---
# ⭐⭐⭐ 이 비밀번호가 핵심! 복호화 스크립트와 '압도적으로 동일'해야 함! ⭐⭐⭐
CORRECT_KEY_PASSWORD = "pythonProject1"

RAW_DATA_FILE_NAME = "Temporary personal data.csv"  # 암호화할 '원본 데이터 파일명' (이 파일이 반드시 존재해야 함!)
ENCRYPTED_FILE_NAME = "encrypted_personal_data.bin"  # 암호화된 데이터를 저장할 파일
SALT_FILE_NAME = "salt.bin"  # 솔트(salt)를 저장할 파일

# --- 초강력 3. 암호화 과정 실행 ---
# 이제 더 이상 가짜 데이터를 만들지 않고, 기존에 존재하는 RAW_DATA_FILE_NAME 파일을 사용합니다.
print(f"\n--- '{RAW_DATA_FILE_NAME}' 파일 암호화 시작 ---")

try:
    # 3-1. 원본 개인 정보 CSV 파일 불러오기 (암호화할 대상)
    # 이 시점에서 RAW_DATA_FILE_NAME 파일이 반드시 존재해야 합니다.
    if not os.path.exists(RAW_DATA_FILE_NAME):
        raise FileNotFoundError(f"오류: 원본 파일 '{RAW_DATA_FILE_NAME}'을 찾을 수 없습니다. 파일을 생성하거나 경로를 확인하세요.")
    with open(RAW_DATA_FILE_NAME, 'rb') as f:
        raw_data_bytes = f.read()
    print(f"[*] '{RAW_DATA_FILE_NAME}' 파일 로드 완료.")

    # 3-2. 초강력 솔트(salt) 생성 (여기서 단 한 번! 무작위 솔트를 만든다!)
    # 이 솔트는 암호화와 복호화 모두에 사용되므로, 반드시 안전하게 salt.bin 파일에 저장해야 합니다.
    # 기존 salt.bin이 있다면 덮어쓰게 됩니다.
    generated_salt = os.urandom(16)

    # 3-3. 생성된 솔트를 파일로 저장 (복호화 시 사용해야 함!)
    with open(SALT_FILE_NAME, 'wb') as f:
        f.write(generated_salt)
    print(f"[*] '{SALT_FILE_NAME}' 파일에 솔트 저장 완료.")

    # 3-4. ⭐⭐⭐ 암호화 키 생성 (CORRECT_KEY_PASSWORD와 생성된 솔트 사용) ⭐⭐⭐
    encryption_key_bytes = derive_key(CORRECT_KEY_PASSWORD, generated_salt)
    encryption_key_str = encryption_key_bytes.decode('utf-8')  # 디버깅용 확인 출력!
    print(f"--- [암호화 시점] 생성된 최종 키 (Base64): '{encryption_key_str}' ---")

    # 3-5. Fernet 암호화기 초기화 (생성된 키를 Fernet 객체에 넘겨준다!)
    fernet_encryptor = Fernet(encryption_key_bytes)
    print(f"[*] Fernet 암호화기 초기화 완료 (키 생성 성공).")

    # 3-6. 데이터 암호화 및 파일 저장
    # 기존 encrypted_personal_data.bin이 있다면 덮어쓰게 됩니다.
    encrypted_data = fernet_encryptor.encrypt(raw_data_bytes)
    with open(ENCRYPTED_FILE_NAME, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)
    print(f"[+] 암호화된 개인 정보가 '{ENCRYPTED_FILE_NAME}' 파일로 저장되었습니다. (암호화 성공)")

    print("\n--- 암호화 과정 완료 ---")

except FileNotFoundError as e:
    print(f"[!] 암호화 실패: 필요한 파일이 없습니다. {e}")
    traceback.print_exc()
except Exception as e:
    print(f"[!] 예상치 못한 초강력 오류 발생: {type(e).__name__} - {e}")
    traceback.print_exc()
