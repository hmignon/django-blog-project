import requests
from bs4 import BeautifulSoup


def quote_of_the_day():
    response = requests.get("https://goquotes-api.herokuapp.com/api/v1/random?count=1")
    json_response = response.json()
    quote = {
        "quote": json_response["quotes"][0]["text"],
        "author": json_response["quotes"][0]["author"]
    }
    return quote


def get_reading_time(text: str):
    """
    Returns blog post reading time
    """
    word_count = len(text.split())
    reading_time = round(word_count / 200)

    return reading_time


def cleanup_body_html(html):
    """
    Set Bootstrap classes to html elements in ckeditor output
    Remove automatic style attributes to img
    """
    soup = BeautifulSoup(html, "html.parser")

    for table in soup.select("table"):
        table["class"] = "table"

    for blockquote in soup.select("blockquote"):
        blockquote["class"] = "blockquote"

    for img in soup.select("img"):
        del img["style"]

    return str(soup)


def summary_cleanup(text: str):
    text.replace("&#x27;", "'")
