import db
from datetime import datetime

def action(type):
    time = datetime.now()
    db.execute("""INSERT INTO app_stats (action_type, action_time) VALUES (?, ?)""", [type, time])