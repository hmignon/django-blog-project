import requests


def quote_of_the_day():
    response = requests.get('https://goquotes-api.herokuapp.com/api/v1/random?count=1')
    json_response = response.json()
    quote = {
        'quote': json_response['quotes'][0]['text'],
        'author': json_response['quotes'][0]['author']
    }
    return quote


def get_reading_time(text: str):
    word_count = len(text.split())
    reading_time = round(word_count / 200)

    return reading_time
