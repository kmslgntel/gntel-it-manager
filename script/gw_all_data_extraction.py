import pyodbc
import pandas as pd
from sqlalchemy import create_engine
from db_config import GET_DB_CONFIG
from sqlalchemy import text

DB_CONFIG = GET_DB_CONFIG("GW_ALL")


server = DB_CONFIG['host']
database = DB_CONFIG['database']
username = DB_CONFIG['user']
password = DB_CONFIG['password']

# server = '220.95.197.10'
# database = ''

user_list = []
user_col = ['USER_ID', 'USER_NAME', 'USER_NAME_EN', 'DEPT_CODE', 'GRADE_NM', 'GRADE_NM_EN', 'USE_YN', 'RESIGN_DT', 'EMP_NO', 'EMAIL', 'COCD', 'TEL', 'HP']
dept_list = []
dept_col = ['COCD', 'DEPT_CODE', 'DEPT_NAME', 'DEPT_NAME_EN', 'STEP', 'VIEW_ORDER', 'HIGH_DEPT_CODE', 'USEYN', 'REGDT']

try:
    # 데이터베이스 연결
    conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    

    cursor = conn.cursor()

    # SQL 쿼리 실행
    user_query = "select * from SC.T_LX_USER_SYNC_ALL_2;"
    cursor.execute(user_query)

    # 결과 출력
    #user_columns = [column[0] for column in cursor.description]  # 컬럼명 가져오기
    user_result = cursor.fetchall()

    for user_row in user_result:
        user_user_id = user_row[0]
        user_user_name = user_row[1]
        user_user_name_en = user_row[2]
        user_dept_code = user_row[3]
        user_grade_nm = user_row[4]
        user_grade_nm_en = user_row[5]
        user_useyn = user_row[6]
        user_resign_dt = user_row[7]
        user_emp_no = user_row[8]
        user_email = user_row[9]
        user_cocd = user_row[10]
        user_tel = user_row[11]
        user_hp = user_row[12]

        

        user_list.append([user_user_id, user_user_name, user_user_name_en, user_dept_code, user_grade_nm, user_grade_nm_en, user_useyn, user_resign_dt, user_emp_no, user_email, user_cocd, user_tel, user_hp])


    dept_query = "SELECT * FROM SC.T_LX_DEPT_SYNC_ALL;"
    cursor.execute(dept_query)

    # 결과 출력
    #dept_columns = [column[0] for column in cursor.description]  # 컬럼명 가져오기
    dept_data = cursor.fetchall()
    
    for dept_row in dept_data:
        dept_cocd = dept_row[0]
        dept_dept_code = dept_row[1]
        dept_dept_name = dept_row[2]
        dept_dept_name_en = dept_row[3]
        dept_step = dept_row[4]
        dept_view_order = dept_row[5]
        dept_high_dept_code = dept_row[6]
        dept_useyn = dept_row[7]
        dept_regdt = dept_row[8]

        dept_list.append([dept_cocd, dept_dept_code, dept_dept_name, dept_dept_name_en, dept_step, dept_view_order, dept_high_dept_code, dept_useyn, dept_regdt])





    user_df = pd.DataFrame(user_list, columns=user_col)
    dept_df = pd.DataFrame(dept_list, columns=dept_col)

finally:
    # 연결 닫기
    cursor.close()
    conn.close()

user_df = user_df.fillna('')
dept_df = dept_df.fillna('')
# engine = create_engine("mariadb+mariadbconnector://root:root123@220.95.197.246:3306/network_db")
engine = create_engine(
    "mariadb+mariadbconnector://it_user:1234!@220.95.197.246:3306/network_db"
)


user_df.to_sql(name='USR_INF', con=engine, if_exists='replace', index=False)
dept_df.to_sql(name='DPT_INF', con=engine, if_exists='replace', index=False)

with engine.connect() as conn:

    conn.execute(text("""
        CREATE INDEX idx_usr_uid ON USR_INF(USER_ID);
    """))

    conn.execute(text("""
        CREATE INDEX idx_dpt_code ON DPT_INF(DEPT_CODE);
    """))

    conn.commit()