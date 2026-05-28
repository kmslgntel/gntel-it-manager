import pymysql
import pandas as pd
from sqlalchemy import create_engine
from db_config import GET_DB_CONFIG
from sqlalchemy import text

DB_CONFIG = GET_DB_CONFIG("IPSCAN")

# MySQL 연결 설정
ipscan_connection = pymysql.connect(
    host=DB_CONFIG['host'],
    port=DB_CONFIG['port'],
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password'],
    database=DB_CONFIG['database'],
    charset=DB_CONFIG['charset']  # 잘못된 인코딩으로 저장된 상태를 그대로 불러옴
)

try:
    with ipscan_connection.cursor() as ipscan_cursor:
        # 데이터 조회
        ipscan_cursor.execute("""
            SELECT 
                i.IP,
                i.STR_IP,
                i.MAC,
                i.PROBE_ID,
                COALESCE(m.HNAME, '') AS HNAME,
                MAX(CASE WHEN u.ID = 10276 THEN u.COLUMN_DATA ELSE '' END) AS Division,
                MAX(CASE WHEN u.ID = 10280 THEN u.COLUMN_DATA ELSE '' END) AS User,
                MAX(CASE WHEN u.ID = 10302 THEN u.COLUMN_DATA ELSE '' END) AS Note
            FROM 
                ip_mac_info i
            LEFT JOIN 
                mac_master m
            ON 
                i.MAC = m.MAC
                AND i.PROBE_ID = m.PROBE_ID
            LEFT JOIN 
                user_define_ip_data u
            ON 
                i.IP = u.IP 
                AND i.PROBE_ID = u.PROBE_ID
            GROUP BY
                i.IP, i.STR_IP, i.MAC, i.PROBE_ID, m.HNAME;
        """)
        results = ipscan_cursor.fetchall()
        
        # 결과를 데이터프레임으로 변환
        data = []
        for row in results:
            ip = row[0]
            str_ip = row[1]
            mac = row[2]
            probe_id = row[3]
            # HNAME과 COLUMN_DATA를 euc-kr 인코딩으로 변환
            hname = row[4]
            division = row[5]
            user = row[6]
            note = row[7]
            
            try:
                hname_corrected = hname.encode('latin1').decode('euc-kr', errors='replace')
            except UnicodeDecodeError:
                hname_corrected = hname  # 오류 발생 시 원본 텍스트 그대로 사용

            try:
                division_corrected = division.encode('latin1').decode('euc-kr', errors='replace')
            except UnicodeDecodeError:
                division_corrected = division  # 오류 발생 시 원본 텍스트 그대로 사용

            try:
                user_corrected = user.encode('latin1').decode('euc-kr', errors='replace')
            except UnicodeDecodeError:
                user_corrected = user  # 오류 발생 시 원본 텍스트 그대로 사용

            try:
                note_corrected = note.encode('latin1').decode('euc-kr', errors='replace')
            except UnicodeDecodeError:
                note_corrected = note  # 오류 발생 시 원본 텍스트 그대로 사용

            # IP, STR_IP, MAC, HNAME, COLUMN_DATA 추가
            data.append([ip, str_ip, mac, probe_id, hname_corrected, division_corrected, user_corrected, note_corrected])

        # 데이터프레임 생성 및 STR_IP 기준으로 정렬
        df = pd.DataFrame(data, columns=['IP_ID', 'IP', 'MAC', 'PROBE_ID', 'HNAME', 'DIVISION', 'USER', 'NOTE'])
        
        # STR_IP 컬럼을 자연스러운 IP 주소 순서로 정렬
        df = df.assign(
            str_ip_sort=df['IP'].apply(lambda x: tuple(int(part) for part in x.split('.')))
        ).sort_values('str_ip_sort').drop(columns='str_ip_sort')

finally:
    ipscan_connection.close()




# engine = create_engine("mariadb+mariadbconnector://root:root123@220.95.197.246:3306/network_db")
engine = create_engine(
    "mariadb+mariadbconnector://it_user:1234!@220.95.197.246:3306/network_db"
)
df.to_sql(name='NTWR_DVCS_INF', con=engine, if_exists='replace', index=False)

with engine.connect() as conn:

    conn.execute(text("""
        CREATE INDEX idx_nd_ipid ON NTWR_DVCS_INF(IP_ID);
    """))

    conn.commit()