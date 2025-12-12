import os
import base64

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
# ⭐⭐⭐ 이제 이 비밀번호가 우리의 공식 비밀번호다! 복호화 스크립트와 '압도적으로 동일'해야 함! ⭐⭐⭐
CORRECT_KEY_PASSWORD = "pythonProject1"

RAW_DATA_FILE_NAME = "Temporary personal data.csv"  # 암호화할 '원본 데이터 파일명'
ENCRYPTED_PER_RECORD_FILE_NAME = "encrypted_records.bin"  # 각 레코드가 암호화되어 저장될 파일
SALT_FILE_NAME = "salt_per_record.bin"  # 이 방식에서 사용할 솔트 파일

# --- 초강력 3. 암호화 과정 실행 ---
# '초강력 3. 가짜 개인 정보 생성 및 CSV 저장' 섹션은 주현이의 지시로 제거되었다!
print(f"\n--- '{RAW_DATA_FILE_NAME}' 파일 레코드별 암호화 시작 ---")

try:
    # 4-1. 기존 암호화된 파일 및 솔트 파일 정리 - 주현이의 지시로 제거되었다!
    # 4-2. 원본 데이터 파일 (Temporary personal data.csv)이 없으면 생성! - 주현이의 지시로 제거되었다!

    # 4-1. 원본 데이터 파일 (Temporary personal data.csv) 존재 여부 확인
    if not os.path.exists(RAW_DATA_FILE_NAME):
        raise FileNotFoundError(f"오류: 원본 파일 '{RAW_DATA_FILE_NAME}'을 찾을 수 없습니다. 파일을 생성하거나 경로를 확인하세요.")

    # 4-2. 초강력 솔트(salt) 생성 (여기서 단 한 번! 무작위 솔트를 만든다!)
    generated_salt = os.urandom(16)

    # 4-3. 생성된 솔트를 파일로 저장 (복호화 시 사용해야 함!)
    # 기존 salt_per_record.bin이 있다면 덮어쓰게 됩니다.
    with open(SALT_FILE_NAME, 'wb') as f:
        f.write(generated_salt)
    print(f"[*] '{SALT_FILE_NAME}' 파일에 솔트 저장 완료.")

    # 4-4. ⭐⭐⭐ 암호화 키 생성 (CORRECT_KEY_PASSWORD와 생성된 솔트 사용) ⭐⭐⭐
    encryption_key_bytes = derive_key(CORRECT_KEY_PASSWORD, generated_salt)
    encryption_key_str = encryption_key_bytes.decode('utf-8')  # 디버깅용 확인 출력!
    print(f"--- [암호화 시점] 생성된 최종 키 (Base64): '{encryption_key_str}' ---")

    # 4-5. Fernet 암호화기 초기화 (생성된 키를 Fernet 객체에 넘겨준다!)
    fernet_encryptor = Fernet(encryption_key_bytes)
    print(f"[*] Fernet 암호화기 초기화 완료 (키 생성 성공).")

    # 4-6. 원본 CSV 파일에서 각 레코드(줄)을 읽어와 개별 암호화
    encrypted_records = []
    # RAW_DATA_FILE_NAME이 'Temporary personal data.csv' 일 경우, 파일이 비어 있으면 헤더만 읽힙니다.
    with open(RAW_DATA_FILE_NAME, 'r', encoding='utf-8') as raw_file:
        for i, line in enumerate(raw_file):
            # 헤더 라인을 암호화할지 말지 결정. 여기서는 모든 라인을 암호화하는 예시.
            # 만약 헤더를 암호화하지 않고 싶다면:
            # if i == 0:
            #     # 헤더 처리 로직 (예: encrypted_records.append(line.strip('\n').encode('utf-8')))
            #     # 혹은 헤더를 따로 저장
            #     continue

            line_bytes = line.strip('\n').encode('utf-8')  # 각 줄의 끝에 있는 개행문자(\n) 제거 후 바이트로 인코딩
            encrypted_line = fernet_encryptor.encrypt(line_bytes)  # 개별 줄 암호화
            encrypted_records.append(encrypted_line)
    print(f"[+] 총 {len(encrypted_records)}개의 레코드를 개별 암호화 완료.")

    # 4-7. 암호화된 레코드들을 새로운 바이너리 파일에 저장 (각 암호화된 레코드는 한 줄)
    # 기존 encrypted_records.bin이 있다면 덮어쓰게 됩니다.
    with open(ENCRYPTED_PER_RECORD_FILE_NAME, 'wb') as output_file:
        for record_bytes in encrypted_records:
            output_file.write(record_bytes)
            output_file.write(b'\n')  # 각 암호화된 레코드 뒤에 개행 바이트 추가 (복호화 시 줄 단위로 읽기 위함)
    print(f"[+] 개별 암호화된 레코드가 '{ENCRYPTED_PER_RECORD_FILE_NAME}' 파일로 저장되었습니다. (암호화 성공)")

    print("\n--- 레코드별 암호화 과정 완료 ---")

except FileNotFoundError as e:
    print(f"[!] 암호화 실패: 필요한 파일이 없습니다. {e}")
    traceback.print_exc()
except Exception as e:
    print(f"[!] 예상치 못한 초강력 오류 발생: {type(e).__name__} - {e}")
    traceback.print_exc()