import re
import datetime

#画面のhtmlの中から年を取る
def get_year(soup):
    h2 = soup.find(class_="htBlock-mainContents").find("h2")
    spans = h2.find("span").find_all(class_="htBlock-subHeading")
    for span in spans:
        span.extract()
    date_range = h2.find("span").text.strip().replace('\r', '').replace('\n', '')
    year = date_range.split('/')[0]
    return year

#画面のhtmlの中から月を取る
def get_month(soup):
    h2 = soup.find(class_="htBlock-mainContents").find("h2")
    spans = h2.find("span").find_all(class_="htBlock-subHeading")
    for span in spans:
        span.extract()
    date_range = h2.find("span").text.strip().replace('\r', '').replace('\n', '')
    month = date_range.split('/')[1]
    return month

#日付から曜日を消して、年と/で結合して返す
def format_date(year, date):
    date = re.sub('[(（].+[)）]','',date)
    date = year + '/' + date
    return date

#"時.分"を0.25刻みの時間に変換する
def conv_mins_to_quarter(hr, min):
    hr = int(hr)
    min = int(min)

    if min < 8:
        min = 0
    elif 8 <= min and min < 23:
        min = 25
    elif 23 <= min and min < 38:
        min = 50
    elif 38 <= min and min < 53:
        min = 75
    else:
        hr += 1
        min = 0

    time = str(hr) + '.' + str(min)
    return time

#昼休憩を除いた休憩時間を算出してHH:MMで返す
def calc_not_work_time(hr, min):
    hr = str(hr)
    min = str(min)
    time = datetime.datetime.strptime(hr + ':' + min, '%H:%M')
    #45分減算
    time -= datetime.timedelta(minutes=45)

    hr = time.hour
    min = time.minute
    time = str(hr) + ':' + str(min)

    if hr == 0 and min == 0:
        return ''
    return time
