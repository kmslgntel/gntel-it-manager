import json
import os
from datetime import datetime
from cryptography.fernet import Fernet
import paramiko
import pandas as pd
import mariadb
from sqlalchemy import create_engine
from db_config import GET_DB_CONFIG

DB_CONFIG = GET_DB_CONFIG("CODING")

network_connection = mariadb.connect(
    host=DB_CONFIG['host'],
    port=DB_CONFIG['port'],
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password'],
    database=DB_CONFIG['database']
)


def load_key():
    with open("json/encryption_key.key", "rb") as key_file:
        key = key_file.read()
    return key

def load_encrypted_credentials():
    # 암호화된 자격 증명 로드
    with open("json/credentials.json", "r") as file:
        credentials = json.load(file)

    # 암호화 객체 생성
    key = load_key()
    cipher_suite = Fernet(key)

    # 복호화
    decrypted_id = cipher_suite.decrypt(credentials["ID"].encode()).decode()
    decrypted_pw = cipher_suite.decrypt(credentials["PW"].encode()).decode()

    return decrypted_id, decrypted_pw

def backup_device_config(switch_ip, username, password):
    # SSH 클라이언트 초기화
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # SSH 연결
        ssh_client.connect(switch_ip, username=username, password=password, timeout=10)
        print(f"Connected to {switch_ip}")


        # 주니퍼 장비의 ethernet-switching table 조회
        stdin, stdout, stderr = ssh_client.exec_command("show configuration | display set")
        # exec_command("show ethernet-switching table")
        # exec_command("show configuration | display set")
        # 결과 저장
        config_output = stdout.read().decode('utf-8')

        status = "Access"
    except:
        status = "Failed"


    finally:
        # SSH 연결 닫기
        ssh_client.close()

    return config_output, status

def compare_and_fetch_values(data, target_column_index, compare_value, other_column_index):
    # data (list): MariaDB에서 가져온 데이터 (행 리스트)
    # target_column_index (int): 비교할 열 인덱스
    # compare_values (list): 비교할 값들 리스트
    # other_column_index (int): 조건에 맞는 경우 가져올 열 인덱스
    for row in data:
        if row[target_column_index] in compare_value:
            result = row[other_column_index]

    return result

def fetch_data_from_db(network_connection):

    try:
        cursor = network_connection.cursor()

        sql_rack = "select * from RCK_INF;"
        cursor.execute(sql_rack)
        rack_info = cursor.fetchall()

        sql_switch = "select * from SWT_INF;"
        cursor.execute(sql_switch)
        switch_info = cursor.fetchall()

        return rack_info, switch_info

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        
        return None

    finally:
        if network_connection:
            network_connection.close()


def config_preprocessing(output_list):
    today = datetime.today()
    formatted_date = today.strftime("%Y-%m-%d")
    formatted_time = today.strftime("%H:%M:%S")
    date_id = today.strftime("%Y%m%d%H%M%S")

    data = []
    for config_output, switch_id, status in output_list:
        data.append([switch_id, config_output, status, date_id])

    time_list = []    
    time_list.append([date_id, formatted_date, formatted_time])

    return data, time_list


def backup_process(rack_data, ID, PW, switch_ip_data):
    # 에러 발생 여부 및 에러 목록
    error_occurred = False
    error_logs = []

    output_list = []
    port_set_list = []
    #pd.DataFrame()


    # 백업 프로세스 진행
    # for rack in rack_data:
    #     for ip in rack_data[rack]:
    for tmp_data in switch_ip_data:
        switch_ip = tmp_data[2]
        switch_id = compare_and_fetch_values(switch_ip_data, 2, switch_ip, 0)

        config_output, status  = backup_device_config(switch_ip, ID, PW)
        # ethernet-switching table 설정 값
        output_list.append((config_output, switch_id, status))

    
    
    config_data, date_id_data = config_preprocessing(output_list)
    #data.append([ip_id, vlan, mac, ttype, age, interface])
    df = pd.DataFrame(config_data, columns=['SWITCH_ID', 'CONFIG_DATA', 'STATUS', 'BACKUP_ID'])
    # data.append([switch_id, config_output, status, formatted_date, formatted_time])
    date_df = pd.DataFrame(date_id_data, columns=['BACKUP_ID', 'BACKUP_DATE', 'BACKUP_TIME'])

    # engine = create_engine("mariadb+mariadbconnector://root:root123@220.95.197.246:3306/network_db")
    engine = create_engine(
        "mariadb+mariadbconnector://it_user:1234!@220.95.197.246:3306/network_db"
    )
    
    df.to_sql(name='SWT_CNF_BCK', con=engine, if_exists='append', index=False)
    date_df.to_sql(name='SWT_BCK_INF', con=engine, if_exists='append', index=False)




def main():
    # 계정 정보 로드  
    ID, PW = load_encrypted_credentials()

    rack_data, switch_ip_data = fetch_data_from_db(network_connection)
    
    backup_process(rack_data, ID, PW, switch_ip_data)

        


if __name__== "__main__":
    main()
