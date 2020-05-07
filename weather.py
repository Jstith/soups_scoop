# Import dependencies
from bs4 import BeautifulSoup as BS
from urllib.request import Request, urlopen

# Create weather class
class weather:
    # Only requires zipcode
    def __init__(self, zip):
        # Custom url for the specific zipcode
        self.url = str('https://weather.com/weather/tenday/l/' + str(zip))
        self.webObject = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        # Get the HTML from the webpage
        self.html = urlopen(self.webObject).read()
        # Make the HTML easier to parse
        self.soup = BS(self.html, "html.parser")

    # Pulls out the description of the weather for each day
    def getDescription(self):
        description = []
        for line in (self.soup.find_all('td')):
            if(line.get('class')[0] == 'description'):
                description.append(line.get('title'))
        return(description)

    # Gets the date and day of the week for each day of the forcast
    def getDate(self):
        dayOfWeek = []
        date = []
        for line in (self.soup.find_all('td')):
            if (line.get('class')[0] == 'twc-sticky-col'):
                i = 0
                for each in line.find_all('span'):
                    if (i % 2 == 0):
                        dayOfWeek.append(each.string)
                    else:
                        date.append(each.string)
                    i += 1
        return dayOfWeek, date

    # Simple function to turn HTML into a list
    def convertToList(self, input):
        input = str(input)
        input= input.replace('>', '<')
        input = input.split('<')
        return input

    # Get the humidity for each day
    def getHumidity(self):
        humidities = []
        for line in (self.soup.find_all('td')):
            if (line.get('class')[0] == 'humidity'):
                for each in line.find('span'):
                    each = self.convertToList(each)
                    humidity = ""
                    for item in each:
                        if (item != '' and item.find('span') < 0):
                            humidity += item
                    humidities.append(humidity)
        return(humidities)

    # Get the high and low temp for each day
    def getTemp(self):
        high = []
        low = []
        k = 0
        for line in (self.soup.find_all('td')):
            if (line.get('class')[0] == 'temp'):
                for each in line.find_all('span'):
                    strin = ""
                    # print(each.get('class'))
                    if (each.get('class') != None):
                        if (len(each.get('class')) < 1):
                            each = self.convertToList(each)
                            for item in each:
                                if (str(item).find('span') < 0 and str(item).find('sup') < 0 and str(item) != '' and item.isdigit()):
                                    strin += item
                            if (k % 2 == 0):
                                high.append(strin)
                            else:
                                low.append(strin)
                            k += 1
                    else:
                        each = self.convertToList(each)
                        for item in each:
                            if (str(item).find('span') < 0 and str(item) != ''):
                                if(item.isdigit()):
                                    strin += item
                        if (k % 2 == 0):
                            high.append(strin)
                        else:
                            low.append(strin)
                        k += 1
        return high, low

    # Get the wind speed for each day
    def getWind(self):
        wind = []
        for line in (self.soup.find_all('td')):
            if (line.get('class')[0] == 'wind'):
                for each in line.find_all('span'):
                    wind.append(each.string)
        return(wind)

    # Create a json object which makes it easier to parse later in the people class
    def createTendayJSON(self):
        forcast = {}
        forcast['longTerm'] = []
        wind = self.getWind()
        highTemp, lowTemp = self.getTemp()
        humidity = self.getHumidity()
        weekDay, date = self.getDate()
        descrip = self.getDescription()
        k = 0
        while (k < len(wind)):
            daily = {
                'day': weekDay[k],
                'date': date[k],
                'description': descrip[k],
                'highTemp': highTemp[k],
                'lowTemp': lowTemp[k],
                'humidity': humidity[k],
                'wind': wind[k]
            }
            forcast['longTerm'].append(daily)
            k += 1
        return((forcast))