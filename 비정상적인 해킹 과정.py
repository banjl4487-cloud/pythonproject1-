import os
import base64

import cryptography
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


# --- 초강력 2. 상수 정의 ---
# ⭐⭐⭐ 이 비밀번호는 암호화 스크립트와 '압도적으로 동일'해야 함! ⭐⭐⭐
CORRECT_KEY_PASSWORD = "pythonProject1"

ENCRYPTED_FILE_NAME = "encrypted_personal_data.bin"  # 암호화된 데이터 파일
SALT_FILE_NAME = "salt.bin"  # 솔트(salt) 파일
# 비정상 복호화는 성공하지 못할 것이므로, 복호화 결과 파일은 만들지 않을 수도 있음.
# 필요하다면 다른 이름으로 정의하거나, 오류 발생 시 파일 저장을 건너뛸 수 있음.
DECRYPTED_OUTPUT_FILE_NAME = "decrypted_personal_data_malicious_attempt.csv"  # 비정상 복호화 시도 결과 파일

# --- 초강력 3. 복호화 과정 실행 (손상 시도 포함!) ---
print("\n--- 암호화된 파일 비정상 복호화 시뮬레이션 시작 ---")

try:
    # 3-1. salt 파일 불러오기 (복호화 키 재생성 재료!)
    if not os.path.exists(SALT_FILE_NAME):
        raise FileNotFoundError(f"오류: '{SALT_FILE_NAME}' 파일이 존재하지 않습니다. 먼저 암호화 스크립트 (encrypt_data.py)를 실행하세요!")
    with open(SALT_FILE_NAME, "rb") as f:
        loaded_salt_for_decryption = f.read()
    print(f"[*] '{SALT_FILE_NAME}' 파일에서 복호화용 솔트 로드 완료.")

    # 3-2. 암호화된 파일 불러오기
    if not os.path.exists(ENCRYPTED_FILE_NAME):
        raise FileNotFoundError(
            f"오류: 암호화된 파일 '{ENCRYPTED_FILE_NAME}'을 찾을 수 없습니다. 먼저 암호화 스크립트 (encrypt_data.py)를 실행하세요!")
    with open(ENCRYPTED_FILE_NAME, 'rb') as encrypted_file:
        encrypted_data_for_decryption = encrypted_file.read()
    print(f"[*] '{ENCRYPTED_FILE_NAME}' 파일 로드 완료.")

    # ⭐⭐⭐ 해킹 시뮬레이션: 암호화된 데이터를 의도적으로 '초강력 손상'시키기! ⭐⭐⭐
    # 이 부분에서 암호화된 데이터의 무결성을 깨뜨린다.
    print("[*] 암호화된 데이터를 의도적으로 손상시키는 중...")
    if len(encrypted_data_for_decryption) > 50:  # 데이터가 충분히 길 때만 변조 시도
        # 데이터의 특정 바이트를 임의의 값으로 변경
        # 예를 들어, 50번째 바이트를 '0xff'로 바꾼다.
        # 이렇게 하면 암호화된 데이터의 무결성이 손상됩니다.
        maliciously_modified_data = bytearray(encrypted_data_for_decryption)
        maliciously_modified_data[50] = 0xff  # 특정 바이트 변조
        encrypted_data_for_decryption = bytes(maliciously_modified_data)
        print("[!!!] 🚨🚨🚨 경고: 암호화된 데이터가 의도적으로 '손상'되었습니다! 🚨🚨🚨")
    else:
        print("[!!!] 경고: 암호화된 데이터가 너무 짧아 손상 시도를 건너뜁니다.")
    # ⭐⭐⭐ 손상 시뮬레이션 코드 끝 ⭐⭐⭐

    # 3-3. ⭐⭐⭐ 복호화 키 재생성 (CORRECT_KEY_PASSWORD와 불러온 솔트 사용) ⭐⭐⭐
    decryption_key_bytes = derive_key(CORRECT_KEY_PASSWORD, loaded_salt_for_decryption)
    decryption_key_str = decryption_key_bytes.decode('utf-8')  # 디버깅용 확인 출력!
    print(f"--- [복호화 시점] 재생성된 최종 키 (Base64): '{decryption_key_str}' ---")

    fernet_decryptor = Fernet(decryption_key_bytes)
    print(f"[*] Fernet 복호화기 초기화 완료 (키 재생성 성공).")

    # 3-4. 데이터 복호화 시도 (여기서 InvalidToken 발생!)
    decrypted_bytes = fernet_decryptor.decrypt(encrypted_data_for_decryption)

    # 복호화된 바이트가 비어있지 않다면 (오류가 나지 않았다면) 저장 시도 (하지만 보통 여기에 도달 안함)
    if decrypted_bytes:
        with open(DECRYPTED_OUTPUT_FILE_NAME, 'w', encoding='utf-8') as decrypted_csv_file:
            decrypted_csv_file.write(decrypted_bytes.decode('utf-8'))
        print(f"[+] 복호화된 개인 정보가 '{DECRYPTED_OUTPUT_FILE_NAME}' 파일로 저장되었습니다. (복호화 성공?!)")
    else:
        print("[!] 경고: 복호화된 데이터가 비어 있습니다. (예상된 결과일 수 있습니다.)")

    print("\n--- 비정상 복호화 시뮬레이션 완료 (오류 발생 여부 확인) ---")

except FileNotFoundError as e:
    print(f"[!] 초강력 오류: 필요한 파일이 없습니다. {e}")
    traceback.print_exc()
except cryptography.fernet.InvalidToken:
    print(f"[!] 🚨🚨🚨 초강력 성공: InvalidToken! (예상된 결과!) 🚨🚨🚨")
    print(f"      암호화된 데이터가 손상되었음을 Fernet이 정확히 감지했습니다. ")
    print(f"      이는 데이터의 무결성이 훼손되었음을 의미하며, 시스템의 강력한 보안성을 증명합니다!")
    traceback.print_exc()  # InvalidToken의 트레이스백을 보여줘! 젠장!
except Exception as e:
    print(f"[!] 예상치 못한 초강력 오류 발생: {type(e).__name__} - {e}")
    traceback.print_exc()