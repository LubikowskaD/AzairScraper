import requests
from bs4 import BeautifulSoup
import pandas as pd

srcAirport='WMI'
dstAirport='SZZ'
depdate='30.11.2023'
arrdate='30.01.2024'
minDaysStay='2'
maxDaysStay='6'
currency='PLN'

page_url = f'https://www.azair.eu/azfin.php?tp=0&searchtype=flexi&srcAirport=+%5B{srcAirport}%5D&srcTypedText=wa&srcFreeTypedText=&srcMC=&srcFreeAirport=&dstAirport=+%5B{dstAirport}%5D&dstTypedText=anyw&dstFreeTypedText=&dstMC=&adults=1&children=0&infants=0&minHourStay=0%3A45&maxHourStay=23%3A20&minHourOutbound=0%3A00&maxHourOutbound=24%3A00&minHourInbound=0%3A00&maxHourInbound=24%3A00&depdate={depdate}&arrdate={arrdate}&minDaysStay={minDaysStay}&maxDaysStay={maxDaysStay}&nextday=0&autoprice=true&currency={currency}&wizzxclub=false&flyoneclub=false&blueairbenefits=false&megavolotea=false&schengen=false&transfer=false&samedep=true&samearr=true&dep0=true&dep1=true&dep2=true&dep3=true&dep4=true&dep5=true&dep6=true&arr0=true&arr1=true&arr2=true&arr3=true&arr4=true&arr5=true&arr6=true&maxChng=1&isOneway=return&resultSubmit=Search'

page = requests.get(page_url)
soup = BeautifulSoup(page.content, 'html.parser')

oczyszcz = soup.find(id='reslist')
mydivs = oczyszcz.find_all("div", {"class": "result"})
mydivs_all = []
fly_date = []

for div in mydivs:
  ticket_price = div.find("span", {"class" : "sumPrice"}).get_text()
  ticket_price = ticket_price.replace('Total: ','').replace('\n','')
  #ticket_price = float(ticket_price)
  departure = div.find("span", {"class" : "from"}).find("span", {"class" : "code"}).text[:3]
  arrival = div.find("span", {"class" : "to"}).find("span", {"class" : "code"}).text[:3]
  for p in mydivs[0].find_all("p"):
    departure_arrival_date =  p.find_all("span", {"class" : "date"})
    for d in departure_arrival_date:
      fly_date.append(d.get_text()[4:])

  mydivs_all.append([ticket_price, departure, fly_date[0], arrival, fly_date[1]])

df = pd.DataFrame(mydivs_all, columns =['Price','From','Departure Date','To','Departure Date'])
df
df.to_excel('flies.xlsx', index = False)


