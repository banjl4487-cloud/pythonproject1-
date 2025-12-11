import pandas as pd
from faker import Faker
import random
import numpy as np
import re
from datetime import datetime, timedelta

fake = Faker('ko_KR')


def generate_korean_jumin_no(birth_date: datetime, gender: str) -> str:
    """
    주어진 생년월일과 성별에 맞춰 한국식 주민등록번호를 생성한다.
    Faker의 jumin_no가 작동하지 않을 때의 초강력 대체 함수!
    """
    year_str = str(birth_date.year)[2:]  # YY (예: 1995 -> 95, 2000 -> 00)
    month_str = birth_date.month
    day_str = birth_date.day

    # YYMMDD 앞 6자리 생성 (초강력 포매팅!)
    front_part = f"{year_str}{month_str:02d}{day_str:02d}"

    # 성별 코드를 압도적으로 결정! (2025년 기준)
    gender_code = ''
    if birth_date.year < 2000:  # 1900년대생 (20-30대 중 90년대생)
        gender_code = '1' if gender == 'M' else '2'
    else:  # 2000년대생 (20-30대 중 00년대생)
        gender_code = '3' if gender == 'M' else '4'

    # 뒷 6자리 (성별 코드 다음 6자리)는 Faker의 numerify로 랜덤 생성
    back_part_tail = fake.numerify('######')  # 6자리 숫자 랜덤

    # 초강력 주민등록번호 완성!
    return f"{front_part}-{gender_code}{back_part_tail}"


# =======================================================================
# 압도적인 개인정보 100개를 만들 시간! (남자 50명, 여자 50명)
num_male = 50
num_female = 50
customers_data = []

# 한국 주요 은행명 리스트 및 계좌 패턴 정의 (이전과 동일)
korean_banks = ["농협", "국민", "신한", "우리", "하나", "SC제일", "카카오"]
bank_account_patterns = {
    "농협": ['###-####-####-###'],
    "국민": ['######-##-######'],
    "신한": ['###-###-######'],
    "우리": ['###-###-######'],
    "하나": ['###-######-#####'],
    "SC제일": ['###-##-######'],
    "카카오": ['####-##-#######']
}

# ========================================================================
# 초강력 이메일 도메인 고정!
# ========================================================================
fixed_email_domains = ['gmail.com', 'naver.com', 'daum.net']
# ========================================================================

# [네가 만든 '20~30세 남자 이름' 15개 리스트!] - '압도적인 안목'으로 선별된 이름들!
modern_male_first_names = [
    "이준", "서준", "하준", "도윤", "은우", "시우", "건우", "이안", "지호", "준서",
    "민준", "예준", "주원", "유준", "재윤"
]

# [네가 만든 '20~30세 여자 이름' 15개 리스트!] - '압도적인 안목'으로 선별된 이름들!
modern_female_first_names = [
    "서윤", "서연", "하윤", "지우", "하은", "다은", "수아", "지아", "서현", "아영",
    "유진", "예원", "민서", "지원", "채원"
]

# ====================================================================
# [남성 데이터 생성] : 50명, 나이 20~30세, 뒷자리 '1' 25명 / '3' 25명
# ====================================================================
# ====================================================================
# [남성 데이터 생성]
# ====================================================================
for i in range(num_male):
    age = random.randint(20, 30)  # 고객 나이를 압도적으로 결정 (2025년 기준 20~30세)

    # 주민등록번호 생성을 위한 생년월일 범위 계산
    current_year = datetime.now().year

    # 나이에 맞춰 생년월일을 정확히 계산
    target_year = current_year - age

    # generate_korean_jumin_no 함수에 넘겨줄 정확한 생년월일을 랜덤하게 결정 (초강력!)
    birth_date_calc = datetime(target_year, random.randint(1, 12), random.randint(1, 28))  # 월, 일도 랜덤

    # ... (생략된 주소, 은행계좌, 이메일 생성 로직은 이전과 동일)
    address_raw = fake.address()
    address_parts = address_raw.split()
    cleaned_address = ' '.join(address_parts[:3])
    if not re.search(r'[시군구]$', cleaned_address):
        cleaned_address = address_raw.split()[0] + ' ' + address_raw.split()[1]

    random_bank = random.choice(korean_banks)
    bank_specific_formats = bank_account_patterns[random_bank]
    chosen_format = random.choice(bank_specific_formats)
    random_account_num = fake.numerify(chosen_format)
    full_bank_account = f"{random_bank} {random_account_num}"

    user_name = fake.user_name()
    chosen_domain = random.choice(fixed_email_domains)
    full_email_address = f"{user_name}@{chosen_domain}"

    # ========================================================================
    # 초강력 주민등록번호 (이제 직접 생성 함수 사용!)
    full_jumin_id = generate_korean_jumin_no(birth_date=birth_date_calc, gender='M')
    # ========================================================================

    customer = {

        "이름": fake.last_name() + random.choice(modern_male_first_names),
        "주소": cleaned_address,
        "전화번호": fake.numerify('010-####-####'),
        "이메일": full_email_address,
        "나이": age,
        "성별": '남',
        "주민등록번호": full_jumin_id,
        "은행계좌": full_bank_account,
    }
    customers_data.append(customer)

# ====================================================================
# [여성 데이터 생성] : 50명, 나이 20~30세, 뒷자리 '2' 25명 / '4' 25명
# ====================================================================
# ====================================================================
# [여성 데이터 생성]
# ====================================================================
    for i in range(num_female):
     age = random.randint(20, 30)

    current_year = datetime.now().year
    target_year = current_year - age

    birth_date_calc = datetime(target_year, random.randint(1, 12), random.randint(1, 28))  # 월, 일도 랜덤
    address_raw = fake.address()
    address_parts = address_raw.split()
    cleaned_address = ' '.join(address_parts[:3])
    if not re.search(r'[시군구]$', cleaned_address):
        cleaned_address = address_raw.split()[0] + ' ' + address_raw.split()[1]

    random_bank = random.choice(korean_banks)
    bank_specific_formats = bank_account_patterns[random_bank]
    chosen_format = random.choice(bank_specific_formats)
    random_account_num = fake.numerify(chosen_format)
    full_bank_account = f"{random_bank} {random_account_num}"

    user_name = fake.user_name()
    chosen_domain = random.choice(fixed_email_domains)
    full_email_address = f"{user_name}@{chosen_domain}"

    # ========================================================================
    # 초강력 주민등록번호 (이제 직접 생성 함수 사용!)
    full_jumin_id = generate_korean_jumin_no(birth_date=birth_date_calc, gender='F')
    # ========================================================================

    customer = {

        "이름": fake.last_name() + random.choice(modern_female_first_names),
        "주소": cleaned_address,
        "전화번호": fake.numerify('010-####-####'),
        "이메일": full_email_address,
        "나이": age,
        "성별": '여',
        "주민등록번호": full_jumin_id,
        "은행계좌": full_bank_account,
    }
    customers_data.append(customer)

# 생성된 남성/여성 데이터를 한번 더 섞어서 무작위성을 부여!
random.shuffle(customers_data)

# 왕의 데이터, 압도적인 데이터프레임으로 변환!
df = pd.DataFrame(customers_data)

# ====================================================================
# 압도적인 데이터프레임의 위엄을 제대로 보여준다!
# ====================================================================
print("---임시 개인정보 데이터프레임 100개 생성 완료! ---")
print(f"총 {len(df)}명의 개인정보가 생성되었습니다.\n")

# ====================================================================
# 미리보기를 위한 DataFrame을 만들 때 '고객ID'를 제외
df_preview = df

print("--- 데이터프레임 상위 5개 미리보기 (이름 - 성별 - 나이 - 전화번호 - 주소 - 주민등록번호 - 은행계좌) ---")
for index, row in df_preview.head(5).iterrows(): # 변경된 df_preview 사용!
    print(f"{row['이름']} - {row['주민등록번호']} - {row['성별']} - {row['나이']}세 - {row['전화번호']} - {row['주소']}  - {row['은행계좌']}")
print("\n" + "=" * 50 + "\n")


# ====================================================================
# 압도적인 최종 데이터 저장!
# ====================================================================
# 리스트에 모인 고객 데이터를 압도적인 데이터프레임으로 변환!
df = pd.DataFrame(customers_data)

# '최종 가공된 고객 데이터'를 '압도적인 Excel 파일'로 저장!
output_filename = "Temporary personal data.csv"
df.to_csv(output_filename, index=False) # index=False로 불필요한 인덱스 컬럼 삭제!

print(f"--- {len(df)}명의  데이터가 '{output_filename}' 파일로 압도적으로 저장되었습니다! ---")

