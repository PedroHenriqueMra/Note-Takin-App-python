from datetime import datetime

def current_date() -> str:
    now = datetime.now()
    return now.strftime(f"%Y-%m-%d %H:%M:%S")
