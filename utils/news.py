import requests
from bs4 import BeautifulSoup
import mysql.connector
teams = ['mclaren','ferrari','red-bull-racing','mercedes','aston-martin','alpine','haas','rb','williams','kick-sauber']
news_titles,news_links = [],[]
for team in teams:
    r = requests.get(f"https://www.formula1.com/en/teams/{team}")

    soup = BeautifulSoup(r.content, 'html5lib')

    news_cards = soup.find_all("a",href=True,class_= "f1-driver-article-card")
    for card in news_cards:
        p_tag = card.find('p')
        if p_tag:
            text = p_tag.get_text(strip=True)
            news_links.append(team)
            news_links.append(text)
        link = card.get("href")
        news_links.append(link)

conn = mysql.connector.connect(
            host="bdia-finalproject-instance.chk4u4ukiif4.us-east-1.rds.amazonaws.com",
            user="admin",
            password="amazonrds7245",
            database="bdia_team6_finalproject_db"
        )
cursor = conn.cursor()

for i in range(0,len(news_links),3):
    team,title,link = news_links[i:i+3]
    cursor.execute("INSERT INTO news_articles(team_name,news_title,news_link) VALUES(%s,%s,%s)",(team,title,link))
    conn.commit()
cursor.close()
conn.close()
