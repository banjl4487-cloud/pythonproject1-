import os
import base64

import cryptography
# import random # 이 시나리오에서는 랜덤 손상이 없으므로 필요 없음!
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import traceback


# --- 초강력 1. 핵심 파생 함수 정의 ---
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
        backend=default_backend()
    )
    # password가 빈 문자열일 경우에도 키 파생은 시도되지만, 암호화 키와는 다른 값이 됨.
    return base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))


# --- 초강력 2. 상수 정의 ---
# ⭐⭐⭐⭐ 이 비밀번호를 '빈 문자열'로 만들어, 인증키가 없거나 알 수 없는 상황을 시뮬레이션한다! ⭐⭐⭐⭐
CORRECT_KEY_PASSWORD = ""  # 🚨🚨🚨 여기가 핵심! 암호화 시 사용한 비밀번호를 '빈 문자열'로 변경! 🚨🚨🚨

ENCRYPTED_PER_RECORD_FILE_NAME = "encrypted_records.bin"  # 각 레코드가 암호화되어 저장된 파일
SALT_FILE_NAME = "salt_per_record.bin"  # 이 방식에서 사용할 솔트 파일
DECRYPTED_OUTPUT_FILE_NAME = "decrypted_records_no_key_leak_final.csv"  # 유출 데이터 0 검증 결과 저장할 최종 파일

# --- 초강력 3. 복호화 과정 실행 ---
print(f"\n--- '{ENCRYPTED_PER_RECORD_FILE_NAME}' 파일 - 인증키 제거 시 데이터 유출 0 검증 시뮬레이션 시작 ---")
print(f"--- 현재 설정된 인증키(비밀번호): '{CORRECT_KEY_PASSWORD}' (비어있음/잘못됨!) ---")

try:
    # 3-1. salt 파일 불러오기
    if not os.path.exists(SALT_FILE_NAME):
        raise FileNotFoundError(f"오류: '{SALT_FILE_NAME}' 파일이 존재하지 않습니다. 먼저 암호화 스크립트를 실행하세요!")
    with open(SALT_FILE_NAME, "rb") as f:
        loaded_salt_for_decryption = f.read()
    print(f"[*] '{SALT_FILE_NAME}' 파일에서 복호화용 솔트 로드 완료.")

    # 3-2. ⭐⭐⭐ 복호화 키 생성 (CORRECT_KEY_PASSWORD가 빈 문자열이므로, 잘못된 키 생성!) ⭐⭐⭐
    decryption_key_bytes = derive_key(CORRECT_KEY_PASSWORD, loaded_salt_for_decryption)
    decryption_key_str = decryption_key_bytes.decode('utf-8')
    print(f"--- [복호화 시점] 생성된 키 (Base64): '{decryption_key_str}' (정상 키와 '압도적으로' 다름!) ---")

    fernet_decryptor = Fernet(decryption_key_bytes)
    print(f"[*] Fernet 복호화기 초기화 완료 (키 생성 성공 - 하지만 틀린 키!).")

    # 3-3. 암호화된 레코드 파일 불러오기
    if not os.path.exists(ENCRYPTED_PER_RECORD_FILE_NAME):
        raise FileNotFoundError(f"오류: 암호화된 레코드 파일 '{ENCRYPTED_PER_RECORD_FILE_NAME}'을 찾을 수 없습니다. 먼저 암호화 스크립트를 실행하세요!")

    all_encrypted_records_raw = []
    with open(ENCRYPTED_PER_RECORD_FILE_NAME, 'rb') as encrypted_file:
        for line in encrypted_file:
            stripped_line = line.strip(b'\n')
            if stripped_line:
                all_encrypted_records_raw.append(stripped_line)

    total_records = len(all_encrypted_records_raw)

    print(f"[*] 총 {total_records}개의 레코드에 대해 복호화를 시도합니다.")

    # ⭐⭐⭐ 이 시나리오에서는 데이터 손상 로직 (random import 및 관련 코드)은 '싹 다 제거'되어야 합니다! ⭐⭐⭐
    # 즉, all_encrypted_records_raw 리스트의 내용은 암호화된 원본 그대로여야 합니다.

    # 3-4. 모든 레코드에 대해 복호화 시도 (키가 틀리므로 모두 실패 예상)
    decrypted_lines = []
    failed_decryptions = 0

    for line_number, encrypted_line_bytes in enumerate(all_encrypted_records_raw):  # 원본 레코드 리스트 사용!
        try:
            decrypted_single_record_bytes = fernet_decryptor.decrypt(encrypted_line_bytes)
            decrypted_lines.append(decrypted_single_record_bytes.decode('utf-8'))
        except cryptography.fernet.InvalidToken:
          
            failed_decryptions += 1
            decrypted_lines.append(f"[복호화 실패 - 인증키 불일치: {line_number + 1}]")
        except Exception as e:
            print(f"[!] 경고: {line_number + 1}번째 레코드 복호화 중 예상치 못한 오류 발생: {e}")
            failed_decryptions += 1
            decrypted_lines.append(f"[복호화 실패 - 오류: {line_number + 1}]")

    successful_decryptions = len(decrypted_lines) - failed_decryptions
    print(f"\n[결과 요약]")
    print(f"[*] 총 {total_records}개 레코드 시도")
    print(f"[+] 성공적으로 복호화된 레코드 수: {successful_decryptions}개")
    print(f"[!] 복호화에 실패한 레코드 수: {failed_decryptions}개")

    if successful_decryptions == 0 and failed_decryptions == total_records:
        print("[!!!] 🎉🎉🎉 압도적인 성공: 인증키 없이는 '단 한 건의 유출 데이터'도 없습니다! 보안 시스템 완벽 작동! 🎉🎉🎉")
    else:
        print("[!] 오류: 예상과 다른 결과가 나왔습니다. 코드를 다시 확인하세요.")

    # 3-5. 복호화 결과들을 새로운 CSV 파일로 저장
    with open(DECRYPTED_OUTPUT_FILE_NAME, 'w', encoding='utf-8') as output_csv_file:
        for line in decrypted_lines:
            output_csv_file.write(line + '\n')
    print(f"[+] 복호화 시도 결과가 '{DECRYPTED_OUTPUT_FILE_NAME}' 파일로 저장되었습니다.")

    print("\n--- 인증키 제거 시 데이터 유출 0 검증 시뮬레이션 완료 ---")

except FileNotFoundError as e:
    print(f"[!] 초강력 오류: 필요한 파일이 없습니다. {e}")
    traceback.print_exc()
except Exception as e:
    print(f"[!] 예상치 못한 초강력 오류 발생: {type(e).__name__} - {e}")
    traceback.print_exc()