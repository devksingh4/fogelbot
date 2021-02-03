from bs4 import BeautifulSoup 
import requests 
import json

URL = "https://mathshistory.st-andrews.ac.uk/Miscellaneous/Popular/"
page = requests.get(URL).text
soup = BeautifulSoup(page, features="html.parser")
datas = soup.find_all("li")
data = []
for li in datas:
    item = li.find('a')
    data.append({"name": item.text, "url": item['href']})
for item in data:
    try:
        name = 'bios/' + item["name"].lower() + '.json'
        link = 'https://mathshistory.st-andrews.ac.uk/' + item['url'][6:]
        page = requests.get(link).text
        soup = BeautifulSoup(page, features="html.parser")
        # ===Extract Bio===
        realName = soup.find_all("h1")[1].text
        born_place = soup.find_all("dd")[0].find('a').text.strip()
        born = soup.find_all("dd")[0].text.strip().partition('\n')[0].strip()
        died = soup.find_all("dd")[1].text.strip().partition('\n')[0].strip()
        died_place = soup.find_all("dd")[1].text.strip().partition('\n')[2].strip()
        summary = soup.find_all("dd")[2].text.strip()
        ourDict = {"name": realName, "born": born, "born_place": born_place, "died": died, "died_place": died_place, "summary": summary, "link": link }
        app_json = json.dumps(ourDict)
        with open(name, 'w+') as f:
            f.write(app_json)
        print('processed ' + realName)
    except:
        print('skipped one')    