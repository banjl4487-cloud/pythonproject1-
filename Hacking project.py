# 필요한 라이브러리를 임포트합니다.
# os: 파일 시스템 관련 작업을 처리합니다.
# base64: 키를 안전하게 표현하기 위해 사용됩니다.
# cryptography.fernet: Fernet 대칭키 암호화를 구현합니다.
# cryptography.hazmat.primitives: 해시 및 PBKDF2HMC 같은 암호화 원시 함수를 제공합니다.
# cryptography.hazmat.backends: 암호화 연산의 백엔드를 제공합니다.
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

# ====================================================================
# [암호화 설정 및 파일 경로 정의]
# ====================================================================
# 데이터를 암호화/복호화할 때 사용될 비밀번호(인증키).
# 실제 시스템에서는 이 비밀번호가 안전하게 관리되어야 합니다.
CORRECT_KEY_PASSWORD = "pythonProject1"

# 암호화할 원본 CSV 파일의 경로.
# 이 파일은 반드시 이 스크립트와 동일한 디렉토리에 존재해야 합니다.
original_data_file = "Temporary personal data.csv"
# 암호화된 데이터를 저장할 바이너리 파일의 경로.
# 이 파일은 텍스트 편집기로 내용을 확인할 수 없게 됩니다.
encrypted_data_file = "encrypted_personal_data.bin"


# ====================================================================
# [보조 함수: 비밀번호로부터 Fernet 암호화 키 생성]
# ====================================================================
# 사용자 비밀번호로부터 Fernet 암호화에 사용될 키를 안전하게 생성합니다.
# PBKDF2HMAC는 비밀번호를 기반으로 키를 도출하는 표준적인 방법입니다.
def generate_fernet_key(password: str) -> bytes:
    password_bytes = password.encode()  # 비밀번호 문자열을 바이트열로 변환
    salt = b'juhyuns_secret_salt_value!'  # 키 파생 시 사용될 솔트 값 (반드시 바이트열 형태)

    # PBKDF2HMAC: 비밀번호로부터 안전하게 키를 파생하기 위한 KDF (Key Derivation Function)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),  # SHA256 해시 알고리즘 사용
        length=32,  # 파생될 키의 길이 (256비트 = 32바이트)
        salt=salt,  # 키 파생에 사용될 솔트
        iterations=480000,  # 반복 횟수 (보안 강도와 성능 트레이드오프 지점)
        backend=default_backend()  # 암호화 연산을 수행할 백엔드 (시스템 기본)
    )
    # 파생된 키를 Fernet 포맷에 맞게 base64 URL-safe 인코딩
    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    return key


# ====================================================================
# [1단계: 원본 CSV 파일을 읽어 암호화 후 바이너리 파일로 저장]
# ====================================================================
print(f"--- 1단계: 원본 '{original_data_file}' 파일을 읽어 암호화합니다. ---")

# 이전에 생성된 암호화 파일이 있다면 삭제하여 깨끗한 상태로 시작합니다.
if os.path.exists(encrypted_data_file):
    os.remove(encrypted_data_file)
    print(f"이전 암호화 파일 '{encrypted_data_file}'을 삭제했습니다.")

try:
    # 암호화할 원본 파일이 존재하는지 확인합니다.
    if not os.path.exists(original_data_file):
        raise FileNotFoundError(f"원본 파일 '{original_data_file}'을 찾을 수 없습니다. 먼저 파일을 생성해 주세요.")

    # 설정된 비밀번호로부터 Fernet 암호화 키를 생성합니다.
    encryption_key = generate_fernet_key(CORRECT_KEY_PASSWORD)
    f = Fernet(encryption_key)

    # 원본 CSV 파일의 내용을 바이트열 형태로 읽어들입니다.
    with open(original_data_file, 'rb') as file:
        original_bytes = file.read()

    # 읽어들인 바이트열 데이터를 암호화합니다.
    encrypted_bytes = f.encrypt(original_bytes)

    # 암호화된 바이트열을 바이너리 파일로 저장합니다.
    with open(encrypted_data_file, 'wb') as file:
        file.write(encrypted_bytes)

    print(f"--- '{encrypted_data_file}'에 암호화된 데이터가 저장되었습니다. ---")
    print(f"--- 이제 이 파일은 올바른 인증키 없이는 내용을 확인할 수 없습니다. ---")

except FileNotFoundError as e:
    print(f"--- 파일 암호화 실패: {e} ---")
except Exception as e:
    print(f"--- 파일 암호화 중 오류 발생: {e} ---")

print("\n--- 데이터 암호화 과정이 완료되었습니다. ---")
print(f"--- 다음 단계에서는 '{encrypted_data_file}' 파일을 복호화할 예정입니다. ---")