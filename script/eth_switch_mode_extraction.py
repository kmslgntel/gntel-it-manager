import json
import os
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


def get_current_dir():
    """
    현재 실행 중인 파이썬 파일이 위치한 디렉터리 경로 반환
    """
    return os.path.dirname(os.path.abspath(__file__))


def load_key():
    current_dir = get_current_dir()
    with open(current_dir + "/json/encryption_key.key", "rb") as key_file:
        key = key_file.read()
    return key

def load_encrypted_credentials():
    # 암호화된 자격 증명 로드
    current_dir = get_current_dir()
    with open(current_dir + "/json/credentials.json", "r") as file:
        credentials = json.load(file)

    # 암호화 객체 생성
    key = load_key()
    cipher_suite = Fernet(key)

    # 복호화
    decrypted_id = cipher_suite.decrypt(credentials["ID"].encode()).decode()
    decrypted_pw = cipher_suite.decrypt(credentials["PW"].encode()).decode()

    return decrypted_id, decrypted_pw

def backup_device_config(ip, username, password):
    # SSH 클라이언트 초기화
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # SSH 연결
        ssh_client.connect(ip, username=username, password=password, timeout=10)
        print(f"Connected to {ip}")


        # 주니퍼 장비의 ethernet-switching table 조회
        stdin, stdout, stderr = ssh_client.exec_command("show ethernet-switching table")
        # exec_command("show ethernet-switching table")
        # exec_command("show configuration | display set")
        # 결과 저장
        config_output = stdout.read().decode('utf-8')


        # 스위치 포트별 설정 (trunk, access)
        stdin, stdout, stderr = ssh_client.exec_command("show configuration interfaces | display set | match mode")

        port_set_output = stdout.read().decode('utf-8')
    
        #print(config_output)

    finally:
        # SSH 연결 닫기
        ssh_client.close()

    return config_output, port_set_output

# 설정 값 전처리
def ethernet_preprocessing(output_list):
    data = []
    for config_output, switch_id in output_list:
        lines = config_output.strip().split('\n')
        # 초기 값이 col명, 요약 결과가 출력되기 때문에 3번째부터 시작
        for line in lines[2:]:
            values = line.split()

            vlan = values[0]
            tmp_mac = values[1]
            ttype = values[2]
            age = values[3]
            interface = values[4]

            mac = tmp_mac.replace(":", "")

            data.append([switch_id, vlan, mac, ttype, age, interface])

    return data

def port_set_preprocessing(output_list):
    data = []
    for config_output, switch_id in output_list:
        lines = config_output.strip().split('\n')
        for line in lines:
            values = line.split(' ')
            interface = values[2]
            interface += '.0'
            set_conf = values[-1]
            


            data.append([switch_id, interface, set_conf])

    return data


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

def compare_and_fetch_values(data, target_column_index, compare_value, other_column_index):
    # data (list): MariaDB에서 가져온 데이터 (행 리스트)
    # target_column_index (int): 비교할 열 인덱스
    # compare_values (list): 비교할 값들 리스트
    # other_column_index (int): 조건에 맞는 경우 가져올 열 인덱스
    for row in data:
        if row[target_column_index] in compare_value:
            result = row[other_column_index]

    return result

# db에서 ip-ID 값 뽑아와서 그 값으로 df 구축 후 db에 저장 241114


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
        ip = tmp_data[2]
        switch_id = compare_and_fetch_values(switch_ip_data, 2, ip, 0)
        config_output, port_set_output  = backup_device_config(ip, ID, PW)
        # ethernet-switching table 설정 값
        output_list.append((config_output, switch_id))
        # port 별 설정 값 trunk, access
        port_set_list.append((port_set_output, switch_id))
    
    
    ethernet_data = ethernet_preprocessing(output_list)
    #data.append([ip_id, vlan, mac, ttype, age, interface])
    ethernet_switching_df = pd.DataFrame(ethernet_data, columns=['SWITCH_ID', 'VLAN', 'MAC', 'ENTRY_TYPE', 'AGE', 'INTERFACE'])

    port_set_data = port_set_preprocessing(port_set_list)
    
    port_set_df = pd.DataFrame(port_set_data, columns=['SWITCH_ID', 'INTERFACE', 'PORT_MODE'])
    
    # engine = create_engine("mariadb+mariadbconnector://root:root123@220.95.197.246:3306/network_db")
    engine = create_engine(
        "mariadb+mariadbconnector://it_user:1234!@220.95.197.246:3306/network_db"
    )

    
    ethernet_switching_df.to_sql(name='ETH_SWT_INF', con=engine, if_exists='replace', index=False)
    
    port_set_df.to_sql(name='SWT_PRT_MD_INF', con=engine, if_exists='replace', index=False)
    




def main():
    # 계정 정보 로드  
    ID, PW = load_encrypted_credentials()

    # 
    rack_data, switch_ip_data = fetch_data_from_db(network_connection)
    
    backup_process(rack_data, ID, PW, switch_ip_data)

        


if __name__== "__main__":
    main()
