#!/usr/bin/env python3
import os, datetime, urllib.parse, urllib.request

def jalali_to_gregorian(jy, jm, jd):
    jy2 = jy - 979
    days = 365 * jy2 + (jy2 // 33) * 8 + ((jy2 % 33 + 3) // 4)
    jalali_month_days = [31,31,31,31,31,31,30,30,30,30,30,29]
    for i in range(jm - 1):
        days += jalali_month_days[i]
    days += jd - 1
    g_days = days + 79
    gy = 1600 + 400 * (g_days // 146097)
    g_days = g_days % 146097
    if g_days >= 36525:
        g_days -= 1
        gy += 100 * (g_days // 36524)
        g_days = g_days % 36524
        if g_days >= 365:
            g_days += 1
    gy += 4 * (g_days // 1461)
    g_days = g_days % 1461
    if g_days >= 366:
        g_days -= 1
        gy += g_days // 365
        g_days = g_days % 365
    def is_greg_leap(y):
        return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)
    mdays = [31, 28 + (1 if is_greg_leap(gy) else 0), 31,30,31,30,31,31,30,31,30,31]
    gm = 0
    while g_days >= mdays[gm]:
        g_days -= mdays[gm]
        gm += 1
    gd = g_days + 1
    return gy, gm+1, gd

def send_telegram(token, chat_id, text):
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(
        urllib.parse.quote(token, safe=''), urllib.parse.quote(str(chat_id), safe=''), urllib.parse.quote(text, safe='')
    )
    with urllib.request.urlopen(url) as r:
        return r.read()

def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    target_jy = int(os.environ.get("TARGET_JY", "1405"))
    target_jm = int(os.environ.get("TARGET_JM", "7"))
    target_jd = int(os.environ.get("TARGET_JD", "30"))

    if not token or not chat_id:
        print("ERROR: TELEGRAM_TOKEN یا TELEGRAM_CHAT_ID تنظیم نشده‌اند.")
        return

    gy, gm, gd = jalali_to_gregorian(target_jy, target_jm, target_jd)
    target_date = datetime.date(gy, gm, gd)
    today = datetime.date.today()
    days_left = (target_date - today).days

    if days_left < 0:
        text = f"📅 رویداد ({target_jy}/{target_jm}/{target_jd}) گذشته."
    elif days_left == 0:
        text = "🎉 امروز روز موردنظرِ ماست! (۰ روز باقی)"
    else:
        text = f"📅 فقط {days_left} روز تا {target_jd}/{target_jm}/{target_jy} باقی مانده!"

    send_telegram(token, chat_id, text)
    print("Sent:", text)

if name == "main":
    main()
