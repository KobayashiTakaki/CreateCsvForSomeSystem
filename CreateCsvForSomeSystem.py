import os
import sys
import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import WebScrapingUtil as util

config = configparser.ConfigParser()
config.read('settings.ini')
url = config['DEFAULT']['url']
user = config['DEFAULT']['user']
password = config['DEFAULT']['password']
csv_header = '年月日※必須,オーダーNo※必須,オーダー名称,作業フェーズNo※必須,'\
    '作業フェーズ名称,工数※必須,摘要コード,摘要名,分類１_階層１コード,'\
    '分類１_階層２コード,分類１_階層１名称,分類１_階層２名称,分類２_階層１コード,'\
    '分類２_階層２コード,分類２_階層１名称,分類２_階層２名称,備考,'\
    '勤怠情報ー開始時刻,勤怠情報ー終了時刻,勤怠情報ー休暇時間'

order_no = str(sys.argv[1])
phase_no = str(sys.argv[2])

output_dir = os.path.dirname(os.path.abspath(__file__)) + '/output/'

try:
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)

    driver.get(url)

    elem = driver.find_element_by_id("login_id")
    elem.clear()
    elem.send_keys(user)

    elem = driver.find_element_by_id("login_password")
    elem.clear()
    elem.send_keys(password)

    button = driver.find_element_by_id("login_button")
    button.click()

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    year = util.get_year(soup)
    month = util.get_month(soup)

    output_file = os.path.join(output_dir, year + '_' + month + '.csv')

    with open(output_file, mode='w', encoding='shift_jis') as f:

        #csvファイルにヘッダーを書き込み
        f.write(csv_header)
        f.write('\r\n')

        rows = soup.find(class_="htBlock-adjastableTableF_inner").find("table").find("tbody").find_all("tr")
        for row in rows:
            #出勤が空だったらcontinue
            if len(row.find(attrs={"data-ht-sort-index" : "START_TIMERECORD"}).find("p").text.strip()) == 0:
                continue

            #1
            #日付
            td = row.find(attrs={"data-ht-sort-index" : "WORK_DAY"})
            if td is not None:
                date = td.find("p").text.strip()
                f.write(util.format_date(year, date))
            f.write(",")

            #2
            #オーダーNo.
            f.write(order_no)
            f.write(",")

            #3
            #オーダー名称
            f.write(",")

            #4
            #作業フェーズNo.
            f.write(phase_no)
            f.write(",")

            #5
            #作業フェーズ名称
            f.write(",")

            #6
            #工数
            td = row.find(attrs={"data-ht-sort-index" : "ALL_WORK_MINUTE"})
            if td is not None:
                time = td.find("p").text.strip()
                f.write(util.conv_mins_to_quarter(time.split('.')[0], time.split('.')[1]))
            f.write(",")

            #7
            #摘要コード
            f.write(",")

            #8
            #摘要名
            f.write(",")

            #9
            #分類１_階層１コード
            f.write(",")

            #10
            #分類１_階層２コード
            f.write(",")

            #11
            #分類１_階層１名称
            f.write(",")

            #12
            #分類１_階層２名称
            f.write(",")

            #13
            #分類２_階層１コード
            f.write(",")

            #14
            #分類２_階層２コード
            f.write(",")

            #15
            #分類２_階層１名称
            f.write(",")

            #16
            #分類２_階層２名称
            f.write(",")

            #17
            #備考
            f.write(",")

            #18
            #勤怠情報ー開始時刻
            td = row.find(attrs={"data-ht-sort-index" : "START_TIMERECORD"})
            if td is not None:
                #p要素の中にspan要素があったら削除する
                if td.find("p").find("span") is not None:
                    spans = td.find("p").find_all("span")
                    for span in spans:
                        span.extract()

                f.write(td.find("p").text.strip())
            f.write(",")

            #19
            #勤怠情報ー終了時刻
            td = row.find(attrs={"data-ht-sort-index" : "END_TIMERECORD"})
            if td is not None:
                #p要素の中にspan要素があったら削除する
                if td.find("p").find("span") is not None:
                    spans = td.find("p").find_all("span")
                    for span in spans:
                        span.extract()

                f.write(td.find("p").text.strip())
            f.write(",")

            #20
            #勤怠情報ー休暇時間
            td = row.find(attrs={"data-ht-sort-index" : "REST_MINUTE"})
            if td is not None:
                time = td.find("p").text.strip()
                f.write(util.calc_not_work_time(time.split('.')[0], time.split('.')[1]))

            #改行
            f.write('\r\n')

finally:
    driver.quit()
