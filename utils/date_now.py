from datetime import datetime

def date_now() -> str:
    now = datetime.now()
    return now.strftime(f"%Y-%m-%d %H:%M:%S")
