import pandas as pd
from faker import Faker
import random
import numpy as np
import re

fake = Faker('ko_KR')

# 압도적인 고객 100명의 정보를 만들 시간! (남자 50명, 여자 50명)
num_male = 50
num_female = 50
customers_data = []

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
male_suffixes = ['1'] * 25 + ['3'] * 25 # '1'과 '3'을 25개씩 미리 준비
random.shuffle(male_suffixes) # 랜덤으로 섞어서 배치

for i in range(num_male):
    # 주소 생성 후 괄호 안의 불필요한 내용 제거하는 초강력 로직 추가!
    raw_address = fake.road_address()
    cleaned_address = re.sub(r'\s*\([^)]*\)', '', raw_address).strip() # 압도적으로 주소 정제!

    customer = {
        "customer_id": f"M{i+1:03d}", # 남성 ID 구분을 위해 M 접두어 추가!
        "name": fake.last_name() + random.choice(modern_male_first_names), # << 성과 15개 리스트의 이름을 조합!
        "address": cleaned_address, # 정제된 주소를 사용한다!
        "phone_number": fake.numerify('010-####-####'), # 압도적인 010 핸드폰 번호 강제 생성!
        "email": fake.email(),
        "age": random.randint(20, 30), # 20세~30세 나이!
        "gender": '남',                # 성별 확정!
        "personal_id_last_digit": male_suffixes[i], # 남성 뒷자리 패턴 적용!
    }
    customers_data.append(customer)

# ====================================================================
# [여성 데이터 생성] : 50명, 나이 20~30세, 뒷자리 '2' 25명 / '4' 25명
# ====================================================================
female_suffixes = ['2'] * 25 + ['4'] * 25 # '2'와 '4'를 25개씩 미리 준비
random.shuffle(female_suffixes) # 랜덤으로 섞어서 배치

for i in range(num_female):
    # 주소 생성 후 괄호 안의 불필요한 내용 제거하는 초강력 로직 추가!
    raw_address = fake.road_address()
    cleaned_address = re.sub(r'\s*\([^)]*\)', '', raw_address).strip() # 압도적으로 주소 정제!

    customer = {
        "customer_id": f"F{i+1:03d}", # 여성 ID 구분을 위해 F 접두어 추가!
        "name": fake.last_name() + random.choice(modern_female_first_names), # << 성과 15개 리스트의 이름을 조합!
        "address": cleaned_address, # 정제된 주소를 사용한다!
        "phone_number": fake.numerify('010-####-####'), # 압도적인 010 핸드폰 번호 강제 생성!
        "email": fake.email(),
        "age": random.randint(20, 30), # 20세~30세 나이!
        "gender": '여',                # 성별 확정!
        "personal_id_last_digit": female_suffixes[i], # 여성 뒷자리 패턴 적용!
    }
    customers_data.append(customer)

# 생성된 남성/여성 데이터를 한번 더 섞어서 무작위성을 부여!
random.shuffle(customers_data)

# 왕의 데이터, 압도적인 데이터프레임으로 변환!
df = pd.DataFrame(customers_data)

# ====================================================================
# 압도적인 데이터프레임의 위엄을 제대로 보여준다!
# ====================================================================
print("--- 압도적인 가짜 고객 데이터프레임 100개 생성 완료! ---")
print(f"총 {len(df)}명의 고객 데이터가 생성되었습니다.\n")

print("--- 데이터프레임 상위 5개 미리보기 (이름 - 성별 - 나이 - 전화번호 - 주소) ---")
for index, row in df.head(5).iterrows(): # 압도적인 커스텀 출력!
    print(f"{row['name']} - {row['gender']} - {row['age']}세 - {row['phone_number']} - {row['address']}")
print("\n" + "=" * 50 + "\n") # 구분을 위한 압도적인 선!
