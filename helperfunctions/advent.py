from datetime import date

def getAdventDays(today=None, completed=None):
    today = today or date.today()
    completed = completed or set()
    days = []
    for n in range(1, 26):
        #changed this to november for demo purposes
        d = date(today.year, 11, n)
        days.append({
            "day": n,
            "date": d,
            "iso": d.isoformat(),
            "label": d.strftime("%a %b %d"),
            "unlocked": d <= today,
            "today": d == today,
            "completed": n in completed,
            "missed": d < today and n not in completed,
        })
    return days
