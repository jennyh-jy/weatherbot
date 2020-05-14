import requests
import telepot
from bs4 import BeautifulSoup
from pprint import pprint
from config import BOT_TOKEN, CHAT_ID


def get_weather(time):
    BASE_URL = "https://n.weather.naver.com/"
    res = requests.get(BASE_URL)
    soup = BeautifulSoup(res.content, 'html.parser')

    # 오늘 날씨
    today_weather = soup.select(
        '#content > div > div.card.card_today > div.today_weather')[0]

    today_current_weather = today_weather.select(
        'div.weather_area > p')[0].text.split('아요')[1]
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

    today_weather_result = f'Today: {today_current_weather}, {today_current_temp}\n' + \
        f'🌡{today_lowest_temp} / {today_highest_temp}\n' + \
        f'🌬Air quality: Fine dust {today_finedust_status} {today_finedust_number} / Ultrafine dust {today_ultrafinedust_status} {today_ultrafinedust_number}\n' + \
        f'☔️Chance of rain: {today_precipitation_chance}'

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

    tomorrow_weather_result = f'Tomorrow\n' + \
        f'🌡{tomorrow_lowest_temp} / {tomorrow_highest_temp}\n' + \
        f'{tomorrow_morning_weather} / {tomorrow_afternoon_weather}'

    # 주간 날씨 (5일)
    weekly_weather = soup.select(
        '#weekly > div.scroll_control.end_left > div > ul')[0]

    first_day = weekly_weather.select(
        'li:nth-child(2) > div > div.cell_date > span > strong')[0].text
    second_day = weekly_weather.select(
        'li:nth-child(3) > div > div.cell_date > span > strong')[0].text
    third_day = weekly_weather.select(
        'li:nth-child(4) > div > div.cell_date > span > strong')[0].text
    fourth_day = weekly_weather.select(
        'li:nth-child(5) > div > div.cell_date > span > strong')[0].text
    fifth_day = weekly_weather.select(
        'li:nth-child(6) > div > div.cell_date > span > strong')[0].text

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

    weekly_weather_result = f'This week\n' + \
        f'{first_day}:\n' + \
        f'  🌡{first_day_lowest_temp} / {first_day_highest_temp}\n' + \
        f'  {first_day_morning_weather} / {first_day_afternoon_weather}\n\n' + \
        f'{second_day}:\n' + \
        f'  🌡{second_day_lowest_temp} / {second_day_highest_temp}\n' + \
        f'  {second_day_morning_weather} / {second_day_afternoon_weather}\n\n' + \
        f'{third_day}:\n' + \
        f'  🌡{third_day_lowest_temp} / {third_day_highest_temp}\n' + \
        f'  {third_day_morning_weather} / {third_day_afternoon_weather}\n\n' + \
        f'{fourth_day}:\n' + \
        f'  🌡{fourth_day_lowest_temp} / {fourth_day_highest_temp}\n' + \
        f'  {fourth_day_morning_weather} / {fourth_day_afternoon_weather}\n\n' + \
        f'{fifth_day}:\n' + \
        f'  🌡{fifth_day_lowest_temp} / {fifth_day_highest_temp}\n' + \
        f'  {fifth_day_morning_weather} / {fifth_day_afternoon_weather}'

    return {
        'today': today_weather_result,
        'tomorrow': tomorrow_weather_result,
        'weekly': weekly_weather_result
    }[time]


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    pprint(msg)

    if content_type != 'text':
        return

    if 'today' in msg['text']:
        send(get_weather('today'))
    elif 'tomorrow' in msg['text']:
        send(get_weather('tomorrow'))
    elif 'this week' in msg['text']:
        send(get_weather('weekly'))
    else:
        send('Not sure what you\'re saying...')


def send(text):
    bot.sendMessage(CHAT_ID, text)


bot = telepot.Bot(BOT_TOKEN)
bot.message_loop(handle, run_forever=True)
