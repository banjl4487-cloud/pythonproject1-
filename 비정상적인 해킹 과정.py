import os
import base64
import random  # 랜덤 선택을 위한 라이브러리!

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

ENCRYPTED_PER_RECORD_FILE_NAME = "encrypted_records.bin"  # 각 레코드가 암호화되어 저장된 파일
SALT_FILE_NAME = "salt_per_record.bin"  # 이 방식에서 사용할 솔트 파일
DECRYPTED_OUTPUT_FILE_NAME = "decrypted_records_malicious_random.csv"  # 복호화 결과 저장할 파일

# --- 초강력 3. 복호화 과정 실행 ---
print(f"\n--- '{ENCRYPTED_PER_RECORD_FILE_NAME}' 파일 랜덤 레코드 손상 및 복호화 시뮬레이션 시작 ---")

try:
    # 3-1. salt 파일 불러오기 (복호화 키 재생성 재료!)
    if not os.path.exists(SALT_FILE_NAME):
        raise FileNotFoundError(f"오류: '{SALT_FILE_NAME}' 파일이 존재하지 않습니다. 먼저 암호화 스크립트 (encrypt_per_record.py)를 실행하세요!")
    with open(SALT_FILE_NAME, "rb") as f:
        loaded_salt_for_decryption = f.read()
    print(f"[*] '{SALT_FILE_NAME}' 파일에서 복호화용 솔트 로드 완료.")

    # 3-2. ⭐⭐⭐ 복호화 키 생성 (CORRECT_KEY_PASSWORD와 불러온 솔트 사용) ⭐⭐⭐
    decryption_key_bytes = derive_key(CORRECT_KEY_PASSWORD, loaded_salt_for_decryption)
    decryption_key_str = decryption_key_bytes.decode('utf-8')  # 디버깅용 확인 출력!
    print(f"--- [복호화 시점] 재생성된 최종 키 (Base64): '{decryption_key_str}' ---")

    fernet_decryptor = Fernet(decryption_key_bytes)
    print(f"[*] Fernet 복호화기 초기화 완료 (키 재생성 성공).")

    # 3-3. 암호화된 레코드 파일 불러오기 - 실제로는 모든 레코드를 먼저 로드!
    if not os.path.exists(ENCRYPTED_PER_RECORD_FILE_NAME):
        raise FileNotFoundError(
            f"오류: 암호화된 레코드 파일 '{ENCRYPTED_PER_RECORD_FILE_NAME}'을 찾을 수 없습니다. 먼저 암호화 스크립트 (encrypt_per_record.py)를 실행하세요!")

    all_encrypted_records_raw = []
    with open(ENCRYPTED_PER_RECORD_FILE_NAME, 'rb') as encrypted_file:
        for line in encrypted_file:
            stripped_line = line.strip(b'\n')
            if stripped_line:  # 비어있는 줄은 건너뛰기
                all_encrypted_records_raw.append(stripped_line)

    total_records = len(all_encrypted_records_raw)
    num_to_corrupt = 50

    if total_records == 0:
        raise ValueError(f"오류: '{ENCRYPTED_PER_RECORD_FILE_NAME}' 파일에 암호화된 레코드가 없습니다. 암호화 스크립트를 확인하세요.")
    if total_records < num_to_corrupt:
        print(f"[!] 경고: 전체 레코드 수({total_records}개)가 손상시킬 레코드 수({num_to_corrupt}개)보다 적습니다. 모든 레코드를 손상시킵니다.")
        indices_to_corrupt = list(range(total_records))
    else:
        indices_to_corrupt = random.sample(range(total_records), num_to_corrupt)  # 랜덤으로 50개 인덱스 선택

    # ⭐⭐⭐ 랜덤으로 선택된 레코드 50개 손상시키기! ⭐⭐⭐
    corrupted_records = list(all_encrypted_records_raw)  # 원본 리스트 복사
    print(f"[*] 총 {total_records}개의 레코드 중 {len(indices_to_corrupt)}개의 레코드를 랜덤으로 손상시키는 중...")
    for idx in indices_to_corrupt:
        record_bytes = bytearray(corrupted_records[idx])
        if len(record_bytes) > 10:  # 최소한의 길이 조건
            # 특정 바이트를 변조 (예: 5번째 바이트를 변경. 너무 앞부분은 Base64 헤더일 수 있으니 주의)
            record_bytes[random.randint(0, len(record_bytes) - 1)] = random.randint(0, 255)  # 랜덤 위치의 랜덤 값으로 변경
            corrupted_records[idx] = bytes(record_bytes)
    print("[!!!] 🚨🚨🚨 경고: 랜덤으로 선택된 레코드들이 의도적으로 '손상'되었습니다! 🚨🚨🚨")

    # 3-4. 손상된 레코드를 포함하여 개별 복호화 시도
    decrypted_lines = []
    failed_decryptions = 0

    for line_number, encrypted_line_bytes in enumerate(corrupted_records):  # 수정된 레코드 리스트를 사용!
        try:
            decrypted_single_record_bytes = fernet_decryptor.decrypt(encrypted_line_bytes)
            decrypted_lines.append(decrypted_single_record_bytes.decode('utf-8'))
        except cryptography.fernet.InvalidToken:
            # print(f"[!] 경고: {line_number+1}번째 레코드 복호화 실패 (InvalidToken). (손상 예상 레코드)")
            failed_decryptions += 1
            decrypted_lines.append(f"[복호화 실패 - 손상 레코드: {line_number + 1}]")  # 실패한 레코드 표시
        except Exception as e:
            print(f"[!] 경고: {line_number + 1}번째 레코드 복호화 중 예상치 못한 오류 발생: {e}")
            failed_decryptions += 1
            decrypted_lines.append(f"[복호화 실패 - 오류: {line_number + 1}]")

    successful_decryptions = len(decrypted_lines) - failed_decryptions
    print(f"[+] 총 {successful_decryptions}개의 레코드를 성공적으로 복호화 완료.")
    if failed_decryptions > 0:
        print(f"[!] {failed_decryptions}개의 레코드 복호화에 실패했습니다.")
        if successful_decryptions == total_records - num_to_corrupt:
            print("[!!!] 🎉🎉🎉 압도적인 성공: 예상대로 정확히 손상된 레코드만 복호화 실패했습니다! 🎉🎉🎉")

    # 3-5. 복호화된 레코드들을 새로운 CSV 파일로 저장
    with open(DECRYPTED_OUTPUT_FILE_NAME, 'w', encoding='utf-8') as output_csv_file:
        for line in decrypted_lines:
            output_csv_file.write(line + '\n')  # 각 레코드 뒤에 개행 추가
    print(f"[+] 복호화된 개인 정보가 '{DECRYPTED_OUTPUT_FILE_NAME}' 파일로 저장되었습니다.")

    print("\n--- 랜덤 레코드 손상 및 복호화 시뮬레이션 완료 ---")

except FileNotFoundError as e:
    print(f"[!] 초강력 오류: 필요한 파일이 없습니다. {e}")
    traceback.print_exc()
except Exception as e:
    print(f"[!] 예상치 못한 초강력 오류 발생: {type(e).__name__} - {e}")
    traceback.print_exc()