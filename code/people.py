# Import dependencies
from weather import *
from random import randint
from datetime import datetime

# People class
class people:
    # To create a person you need the name, age, zip, and email of the person
    def __init__(self, userName, userAge, userZipCode, userEmail):
        self.name = userName
        self.age = userAge
        self.zipCode = userZipCode
        self.email = userEmail

    # This creates the email for person. New email is created each time it is sent. #NoDuplicates
    def makeEmail(self):
        now = datetime.now()
        timeString = now.strftime("%d/%m/%Y %H:%M")
        subject = "Today's Report: " + timeString
        message = ""
        message +="<html><h1>Get the scoop with Soups</h1><h3>Daily News provided by Soups71</h3><p>Just here to remind you that someone loves you "+self.name+"!!!</p>"
        message += self.createWeatherReport() + self.createNewsReport() + self.randomQuote() + "</html>"
        return subject, message

    # Creates a smaller weather report for the email compared to the original 15 day forcast
    def createWeatherReport(self):
        weatherReport = weather(self.zipCode)
        jsonReport = weatherReport.createTendayJSON()
        weatherMessage = "<h2>Weather</h2><ul>"
        for i in range(3):
            day = jsonReport['longTerm'][i]['day']
            date = jsonReport['longTerm'][i]['date']
            description = jsonReport['longTerm'][i]['description']
            high = jsonReport['longTerm'][i]['highTemp']
            low = jsonReport['longTerm'][i]['lowTemp']
            humidity = jsonReport['longTerm'][i]['humidity']
            wind = jsonReport['longTerm'][i]['wind']
            weatherMessage += "<li><b>" + str(day) + " " + str(date) + "</b></li><ul><li>Descrip: " + str(description) + "</li><li>High Temp: " + str(high) + "</li><li>Low Temp: " + str(low) + "</li><li>Humidity: " + str(humidity) + "</li><li>Wind: " + str(wind) + " mph</li></ul>"
        weatherMessage += "</ul>"
        return weatherMessage

    # UGLY CODE ALERT: I am not really proud of this but it parses out news data from NPR
    def createNewsReport(self):
        wholeReport = "<h2>News</h2>"
        url = 'https://text.npr.org/'
        webObject = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(webObject).read().decode('UTF-8')
        soup = BS(html, "html.parser")
        line = str(soup.find_all('ul')[0])
        line = line.replace('/s.php', 'https://text.npr.org/s.php')
        wholeReport += line
        return wholeReport
    # YET AGAIN UGLY FUCKIN CODE: not proud but parses the text file each time and then selects a random quote each time.
    def randomQuote(self):
        quotes = {}
        randomQuote = "<h2>Random Quote</h2><p>"
        quotes["quotes"] = []
        f = open("quotes.txt", "r", encoding='utf8')
        file = f.readlines()
        quote = ""
        for i in range(len(file)):
            if not file[i].isspace():
                quote += file[i]
            else:
                quotes["quotes"].append({'quote': quote})
                quote = ""

        randomQuote += quotes["quotes"][randint(0, len(quotes["quotes"]))]["quote"].replace('\n', '<br>') + "</p>"
        return randomQuote
    # Getters that I could probably avoid but they just make it easier. It goes back to my JAVA training.
    def getName(self):
        return self.name

    def getAge(self):
        return self.age

    def getZip(self):
        return self.zipCode

    def getEmail(self):
        return self.email
