import os
from dotenv import load_dotenv

load_dotenv()


def GET_DB_CONFIG(prefix):
    DB_CONFIG = {
        "host": os.getenv(f"{prefix}_HOST"),
        "port": int(os.getenv(f"{prefix}_PORT")),
        "user": os.getenv(f"{prefix}_USER"),
        "password": os.getenv(f"{prefix}_PASSWORD"),
        "database": os.getenv(f"{prefix}_NAME"),
        "charset": os.getenv(f"{prefix}_CHATSET"),
    }

    return DB_CONFIG

# DB_CONFIG = {
#     "host" : os.getenv("DB_HOST", "localhost"),
#     "port" : int(os.getenv("DB_PORT", 3306)),
#     "user" : os.getenv("DB_USER", "root"),
#     "password" : os.getenv("DB_PASSWORD", ""),
#     "database" : os.getenv("DB_NAME", "network_db"),
#     "chatset" : "utf8",
# }