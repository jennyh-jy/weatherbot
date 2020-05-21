import requests
import json
import os
import datetime
from bs4 import BeautifulSoup
from mapping import weather_condition, air_quality_condition


def get_weather(time):
    BASE_URL = "https://n.weather.naver.com/"
    res = requests.get(BASE_URL)
    soup = BeautifulSoup(res.content, 'html.parser')

    # 오늘 날씨
    today_weather = soup.select(
        '#content > div > div.card.card_today > div.today_weather')[0]

    today_current_weather = today_weather.select(
        'div.weather_area > p')[0].get_text('|').split('|')[1]
    today_current_temp = today_weather.select(
        'div.weather_area > strong')[0].text.split('온도')[1]
    today_lowest_temp = today_weather.select(
        'div.weather_area > div > strong.degree_low')[0].text.split('최저온도')[1]
    today_highest_temp = today_weather.select(
        'div.weather_area > div > strong.degree_height')[0].text.split('최고온도')[1]

    today_finedust_number = today_weather.select(
        'div.scroll_control > div > ul > li:nth-child(1) > a > div.chart > strong')[0].text
    today_finedust_status = today_weather.select(
        'div.scroll_control > div > ul > li:nth-child(1) > a > div.ttl_area > em')[0].text
    today_ultrafinedust_number = today_weather.select(
        'div.scroll_control > div > ul > li:nth-child(2) > a > div.chart > strong')[0].text
    today_ultrafinedust_status = today_weather.select(
        'div.scroll_control > div > ul > li:nth-child(2) > a > div.ttl_area > em')[0].text

    today_precipitation_chance = soup.select(
        '#hourly > div.inner_card.climate_rain > ul > li:nth-child(1) > span > span:nth-child(2) > span')[0].text

    today_weather_result = f'*Today* {weather_condition[today_current_weather]}, {today_current_temp}\n' + \
        f'🌡 {today_lowest_temp} / {today_highest_temp}\n' + \
        f'☔ Chance of rain: {today_precipitation_chance}\n' + \
        f'🌬 Air quality\n' + \
        f'  PM10: {air_quality_condition[today_finedust_status]} {today_finedust_number}\n' + \
        f'  PM2.5: {air_quality_condition[today_ultrafinedust_status]} {today_ultrafinedust_number}'

    # 내일 날씨
    tomorrow_weather = soup.select(
        '#weekly > div.scroll_control.end_left > div > ul > li:nth-child(2) > div')[0]

    tomorrow_morning_weather = tomorrow_weather.select(
        'div.cell_weather > span:nth-child(1) > i > span')[0].text
    tomorrow_afternoon_weather = tomorrow_weather.select(
        'div.cell_weather > span:nth-child(2) > i > span')[0].text
    tomorrow_lowest_temp = tomorrow_weather.select(
        'div.cell_temperature > strong')[0].text.split('/')[0].split('최저기온')[1]
    tomorrow_highest_temp = tomorrow_weather.select(
        'div.cell_temperature > strong')[0].text.split('/')[1].split('최고기온')[1]

    tomorrow_weather_result = f'*Tomorrow* 🌡 {tomorrow_lowest_temp} / {tomorrow_highest_temp}\n' + \
        f'Morning: {weather_condition[tomorrow_morning_weather]}\n' + \
        f'Afternoon: {weather_condition[tomorrow_afternoon_weather]}'

    # 주간 날씨 (5일)
    weekly_weather = soup.select(
        '#weekly > div.scroll_control.end_left > div > ul')[0]

    first_day_morning_weather = tomorrow_morning_weather
    first_day_afternoon_weather = tomorrow_afternoon_weather
    second_day_morning_weather = weekly_weather.select(
        'li:nth-child(3) > div > div.cell_weather > span:nth-child(1) > i > span')[0].text
    second_day_afternoon_weather = weekly_weather.select(
        'li:nth-child(3) > div > div.cell_weather > span:nth-child(2) > i > span')[0].text
    third_day_morning_weather = weekly_weather.select(
        'li:nth-child(4) > div > div.cell_weather > span:nth-child(1) > i > span')[0].text
    third_day_afternoon_weather = weekly_weather.select(
        'li:nth-child(4) > div > div.cell_weather > span:nth-child(2) > i > span')[0].text
    fourth_day_morning_weather = weekly_weather.select(
        'li:nth-child(5) > div > div.cell_weather > span:nth-child(1) > i > span')[0].text
    fourth_day_afternoon_weather = weekly_weather.select(
        'li:nth-child(5) > div > div.cell_weather > span:nth-child(2) > i > span')[0].text
    fifth_day_morning_weather = weekly_weather.select(
        'li:nth-child(6) > div > div.cell_weather > span:nth-child(1) > i > span')[0].text
    fifth_day_afternoon_weather = weekly_weather.select(
        'li:nth-child(6) > div > div.cell_weather > span:nth-child(2) > i > span')[0].text

    first_day_lowest_temp = tomorrow_lowest_temp
    first_day_highest_temp = tomorrow_highest_temp
    second_day_lowest_temp = weekly_weather.select(
        'li:nth-child(3) > div > div.cell_temperature > strong')[0].text.split('/')[0].split('최저기온')[1]
    second_day_highest_temp = weekly_weather.select(
        'li:nth-child(3) > div > div.cell_temperature > strong')[0].text.split('/')[1].split('최고기온')[1]
    third_day_lowest_temp = weekly_weather.select(
        'li:nth-child(4) > div > div.cell_temperature > strong')[0].text.split('/')[0].split('최저기온')[1]
    third_day_highest_temp = weekly_weather.select(
        'li:nth-child(4) > div > div.cell_temperature > strong')[0].text.split('/')[1].split('최고기온')[1]
    fourth_day_lowest_temp = weekly_weather.select(
        'li:nth-child(5) > div > div.cell_temperature > strong')[0].text.split('/')[0].split('최저기온')[1]
    fourth_day_highest_temp = weekly_weather.select(
        'li:nth-child(5) > div > div.cell_temperature > strong')[0].text.split('/')[1].split('최고기온')[1]
    fifth_day_lowest_temp = weekly_weather.select(
        'li:nth-child(6) > div > div.cell_temperature > strong')[0].text.split('/')[0].split('최저기온')[1]
    fifth_day_highest_temp = weekly_weather.select(
        'li:nth-child(6) > div > div.cell_temperature > strong')[0].text.split('/')[1].split('최고기온')[1]

    # upcoming dates
    dt_second = datetime.datetime.now() + datetime.timedelta(days=2)
    dt_third = datetime.datetime.now() + datetime.timedelta(days=3)
    dt_fourth = datetime.datetime.now() + datetime.timedelta(days=4)
    dt_fifth = datetime.datetime.now() + datetime.timedelta(days=5)

    weekly_weather_result = f'*Tomorrow*\n' + \
        f'🌡 {first_day_lowest_temp} / {first_day_highest_temp}\n' + \
        f'{weather_condition[first_day_morning_weather]} / {weather_condition[first_day_afternoon_weather]}\n\n' + \
        f'*{dt_second.strftime("%A %d %B")}*\n' + \
        f'🌡 {second_day_lowest_temp} / {second_day_highest_temp}\n' + \
        f'{weather_condition[second_day_morning_weather]} / {weather_condition[second_day_afternoon_weather]}\n\n' + \
        f'*{dt_third.strftime("%A %d %B")}*\n' + \
        f'🌡 {third_day_lowest_temp} / {third_day_highest_temp}\n' + \
        f'{weather_condition[third_day_morning_weather]} / {weather_condition[third_day_afternoon_weather]}\n\n' + \
        f'*{dt_fourth.strftime("%A %d %B")}*\n' + \
        f'🌡 {fourth_day_lowest_temp} / {fourth_day_highest_temp}\n' + \
        f'{weather_condition[fourth_day_morning_weather]} / {weather_condition[fourth_day_afternoon_weather]}\n\n' + \
        f'*{dt_fifth.strftime("%A %d %B")}*\n' + \
        f'🌡 {fifth_day_lowest_temp} / {fifth_day_highest_temp}\n' + \
        f'{weather_condition[fifth_day_morning_weather]} / {weather_condition[fifth_day_afternoon_weather]}'

    return {
        'today': today_weather_result,
        'tomorrow': tomorrow_weather_result,
        'weekly': weekly_weather_result
    }[time]


BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
TELEGRAM_URL = "https://api.telegram.org/bot{}/sendMessage".format(BOT_TOKEN)


def send_message(text, chat_id, is_start):
    data = {'text': text, 'chat_id': chat_id, 'parse_mode': 'Markdown'}
    if is_start:
        data['reply_markup'] = json.dumps(
            {'keyboard': [['Today'], ['Tomorrow'], ['5 days']], 'resize_keyboard': True})
    requests.post(TELEGRAM_URL, data=data)


def handler(event, context):
    try:
        data = json.loads(event['body'])
        print('data[message]::: ', data['message'])

        chat_id = data['message']['chat']['id']

        if 'text' not in data['message']:
            return send_message('Please enter text!', chat_id, is_start=False)

        received_msg = data['message']['text'].lower()
        sender_name = data['message']['from']['first_name'] if (
            'first_name' in data['message']['from']) else 'there'
        reply = ''
        is_start = False

        if received_msg == '/start':
            reply = f'Hi {sender_name}! Ask me about today, tomorrow or 5 days\' weather :)'
            is_start = True
        elif 'today' in received_msg:
            reply = get_weather('today')
        elif 'tomorrow' in received_msg:
            reply = get_weather('tomorrow')
        elif '5 days' in received_msg:
            reply = get_weather('weekly')
        else:
            reply = 'Not sure what you\'re saying...'

        send_message(reply, chat_id, is_start)

        return {'statusCode': 200}

    except Exception as e:
        print('Error: ' + str(e))
