import requests
from bs4 import BeautifulSoup
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ибя бд",
    user="юзер бд",
    password="пороль"
)
cursor = conn.cursor()

def create_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS advertisements (
            id serial PRIMARY KEY,
            image_url text,
            date text,
            currency text
        )
    """)
    conn.commit()

def insert_data(image_url, date, currency):
    cursor.execute("""
        INSERT INTO advertisements (image_url, date, currency)
        VALUES (%s, %s, %s)
    """, (image_url, date, currency))
    conn.commit()

def scrape_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    ads = soup.find_all("div", class_="search-item")


    for ad in ads:
        image_url = ad.find("img")["src"]
        date = ad.find(class_="date-posted").text
        currency = ad.find("div", class_="price").text.strip()
        insert_data(image_url, date, currency)

if __name__ == '__main__':
    create_table()
    url = "https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273"
    scrape_data(url)
    cursor.close()
    conn.close()
