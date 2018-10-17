from bs4 import BeautifulSoup
from datetime import date
from dataBase import UsersData
import urllib2
import smtplib

currentYear = 2018
currentMonth = "Oct."
currentDay = 18
todaysDate = (date.today().strftime("%d %b %Y"))
yearLetter = ["Jan.", "Feb.", "Mar.", "Apr.", "May.", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]

def getTitleId(TvSeriesList, emailAddress):
    msg = ""
    try:
        DataBase.addUser(emailAddress, TvSeriesList)
    except:
        print("Error in creating database.")
    for seriesName in TvSeriesList:
        print "Fetching details for " + seriesName + " ....."
        msg += "TV Series: " + seriesName + "\n"
        seriesName = seriesName.replace(' ', '+')
        
        #Finds the result of serch page on IMDb website.
        baseUrl = "https://www.imdb.com/find?ref_=nv_sr_fn&q=" + seriesName +"&s=all"

        content = urllib2.urlopen(baseUrl).read()
        soup = BeautifulSoup(content, "html.parser")
        url = soup.find_all(class_="result_text")

        #Gets the titleID of a particular series.
        seriesURL = "https://www.imdb.com" + str(url[0].a['href'])
        titleId = (seriesURL.split('/')[-2])
        msg += getSeasonEpisodesList(seriesURL, titleId)

    send_email(msg, emailAddress)


def getSeasonEpisodesList(seriesURL, titleId):
        content2 = urllib2.urlopen(seriesURL).read()
        soup = BeautifulSoup(content2, "html.parser")

        #Scrapes the list of episodes and seasons from the IMDb search result of a series.
        seriesInfo = soup.find(class_="seasons-and-year-nav")
        allSeasonsAndEpisodes = seriesInfo.find_all('a')
        episodes = []
        years = []

        #Distinguishes episodes and series years
        for i in allSeasonsAndEpisodes:
            try:
                if len(str(i.text)) == 4:
                    years.append(int(i.text))

                elif len(str(i.text)) < 3:
                    episodes.append(int(i.text))
            except Exception as e:
                pass

        return findReleaseDates(episodes, years, titleId)

def send_email(msg, emailAddress):
    #Sends email with the results.
    subject = "TV Series Updates"
    try:
        print "Sending the email."
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login("lnmiithello@gmail.com","sabbakchodiha")
        message = 'Subject:{}\n\n{}'.format(subject, msg)
        server.sendmail("lnmiithello@gmail.com", emailAddress, message)
        server.quit()
        print("Email sent Successfully: ")
    except Exception as e:
        print("Error in sending the mail.")
    
 


def findReleaseDates(episodes, years, titleId):
    first = "https://www.imdb.com/title/" + str(titleId) + "/episodes?season=" + str(episodes[0])
    content3 = urllib2.urlopen(first).read()
    soup = BeautifulSoup(content3, "html.parser")
    episodesInfo = soup.find_all(class_="airdate")
    dates = []
    nextEpisode = "" 
    for i in episodesInfo:
        dates.append(str(i.text).rsplit())

    flag = True
    msg = ""

    for i in dates[-1::-1]:
        if years[0] < currentYear:
            msg += "The show has finished streaming all its episodes. \n\n"
            flag = False
            break
        if len(i) == 0:
            continue

        elif len(i) == 1:
            if int(i[-1]) > currentYear:
                msg += ("Next season will be aired in " + i[-1] + "\n\n")
                flag = False
                break
            elif int(i[-1] < currentYear):
                msg += (" The show has finished streaming all its episodes.\n\n")
                flag = False
                break

        elif len(i) == 3:
            print i
            if i[-1] >= currentYear:
                if yearLetter.index(i[-2]) >= yearLetter.index(currentMonth):
                    if int(i[-3]) > currentDay:
                        msg += "Next episode will be aired on " + (" ").join(i) + "\n\n"
                        flag = False
                        break

    if flag == True:
        msg += ("Next release isn't announced yet. \n\n")

    return msg

def main():
    emailAddress = raw_input("Email address: ")
    TvSeriesList = raw_input("TV Series: ").split(',')
    getTitleId(TvSeriesList, emailAddress)


DataBase = UsersData()
DataBase.connectData()

if __name__ == '__main__':
    main()