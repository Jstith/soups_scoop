# Soups_Scoop
Email bot that simply gives you weather and news.


### Files
### Code
* **mail.py**
    * This script is manager of the project. It determines who gets an email and when.
* **people.py**
    * Class file used to organize each person and the email that is sent to them.
* **weather.py**
    * This acts as the weather API. It is pretty much just a web scraper but API sounds cooler.
* **users.csv**
    * This is a csv which has 4 columns. `Name, Age, ZipCode, Email` To add people just add them to this file as a new row.
* **quotes.txt**
    * Text file with 346 random quotes which are emailed out by random.
* **creds.txt**
    * This is the file that holds the email and password that the emails will be sent through. 
    * Format: `***EMAIL***:***PASSWORD***`
     * Must be GMAIL account that allows less secure apps.
    
## Looking ahead
At the moment the main changes I hope to make are in the organization of the code. Additionally, I hope to add a little more personality into the emails. Hopefully, I will be able to personalize the news data but that's still a littly ways out. Finally, I might add some css to the email format to make it a little more interesting.

#### Please don't just roast the code. I'd be happy to have a discussion about what I did if you want to shoot me an email at: `information.myevents@gmail.com`
