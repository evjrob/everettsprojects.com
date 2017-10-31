---
id: 1205
title: 'My Life As A Quant: A Neopets Stock Market Bot.'
date: 2014-09-27T16:20:32+00:00
author: Everett
layout: post
guid: http://everettsprojects.com/?p=1205
permalink: /2014/09/27/my-life-as-a-quant-a-neopets-stock-market-bot/
dsq_thread_id:
  - "6140711588"
image: /wp-content/uploads/2014/09/Screenshot-from-2014-09-27-152052-657x372.png
categories:
  - Programming
tags:
  - Bot
  - coding
  - Crawler
  - Neopets
  - Python
  - quant
  - Quantitative Analysis
  - quantitative analyst
  - Stock Trading
  - web
comments: true
---
_This program definitely violates the Neopets Terms of Use. Use at your own risk._

Sometime in the year 2000 or so I was really into the website Neopets. I was about 10, and everyone my age was into Neopets. I don't remember many details, but I do remember trying to get rich using the Neopets stock market. It didn't really work because I didn't have the patience to properly execute the tried and true techniques every one else had already figured out. I knew this, and the brief thought of making a robot to do it for me crossed my mind. The ten year old me had no clue how to go about creating such a robot though, and I'm pretty sure that I had it in my head to build a literal robot that would use the keyboard and mouse. Maybe out of lego or something. I'm not sure.

Some 12 years later (in 2012), something jogged my memory and drew my attention to this unrealized dream of long ago. More importantly, I realized I could make it work now. Sure Neopets isn't much of a thing anymore, but that didn't matter to me. I had to make this happen; it was a loose end! In pursuit of this goal I turned to Python as my language of choice, which conveniently has a library called Mechanize (named after the original Perl Library). Mechanize can programatically interact with webpages as though it is a user. It's a great module that allowed me to finish the project in the span of a couple days between two busy weeks at university. Even today, about two years later, it's still running on an almost daily basis (sometimes computer downtime prevents it from running), and has taken the 1.5 million neopoints of seed capital and turned it into more than 20 million neopoints.

Lets start with the code:

```python
#
# stockbot.py - A webcrawling bot that can automatically play the Neopets stock market game.
#

import mechanize
from lxml import etree
import random
import datetime
import time
import math
import copy
import sys

# Ermagerd, global variables! Bad practice! Bad practice!
logFile = open('<PATH TO FILE>/log.txt', 'a')
errorHTMLdump = open('<PATH TO FILE>/errorHTML.txt', 'a')


##
# Main function controls browser session and logging into Neopets
##  
def main():

    #user credentials
    userName =
    passWord =

    br = mechanize.Browser(factory=mechanize.RobustFactory())

    # User-Agent
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:17.0) Gecko/17.0 Firefox/17.0')]

    # Only necessary if you are using cron instead of anacron, and wish to hide your robotic behaviour.
    #humanizingDelay(300)

    # For potential issues connecting, and a URLError is raised. This sleeps for 30 seconds
    # then retries the connection up to 10 times before giving up and documenting the error.
    for attempt in range(10):
        try:
            br.open("http://www.neopets.com/login/index.phtml")
        except mechanize.URLError:
            time.sleep(30)
        else:
            break
    else:
        logFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - An error occured while trying to connect to the webpage.\n")
        sys.exit()

    br.select_form(nr=0)
    br.form['username'] = userName
    br.form['password'] = passWord

    # Login
    br.submit()

    bankWithdrawal(br)
    stockManager(br)
    bankDeposit(br)

    br.open("http://www.neopets.com/logout.phtml")

##
# Causes the script to pause for a random time to make it appear more
# human by not always executing at the exact same time of day. maxLength
# is the maximum duration of the pause in seconds.
# minLength is optional and defaults to 0.
##
def humanizingDelay(maxLength, minLength=0):
    pauseDuration = random.uniform(minLength,maxLength)
    time.sleep(pauseDuration)

##
# Collects the daily bank interest and decides if it is necessary to withdraw
# neopoints for the day's stock purchase.
##  
def bankWithdrawal(browser):

    bankPage = "http://www.neopets.com/bank.phtml"
    bankHTML = browser.open(bankPage)

    browser.select_form(nr=3)
    browser.submit()

    humanizingDelay(5, minLength=2)

    bankHTMLString = bankHTML.read()
    if getNeopoints(bankHTMLString) < 17000:
        browser.select_form(nr=2)
        browser.form['amount'] = "17000"
        browser.submit()
        logFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - 17000 NP withdrawn from the bank.\n")


##
# Looks at the current neopoint value and deposits any excess
##  
def bankDeposit(browser):

    bankPage = "http://www.neopets.com/bank.phtml"
    bankHTML = browser.open(bankPage)

    humanizingDelay(3, minLength=1)

    bankHTMLString = bankHTML.read()
    if getNeopoints(bankHTMLString) > 32500:
        depositValue = getNeopoints(bankHTMLString) - 32500
        browser.select_form(nr=1)
        browser.form['amount'] = str(depositValue)
        browser.submit()
        logFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - "+str(depositValue)+" NP deposited to the bank.\n")

##
# Takes the current page's HTML and returns the neopoint value.
##     
def getNeopoints(pageHTML):
    startToken = "<a id='npanchor' href=\"/inventory.phtml\">"
    endToken = "</a>"
    startIndex = pageHTML.find(">",pageHTML.find(startToken))+1
    endIndex = pageHTML.find(endToken,startIndex)
    npString = pageHTML[startIndex:endIndex]
    npValue = int(npString.replace(",",""))

    return npValue


##
# A function performing the upper level stock market stuff.
##
def stockManager(br):
    stockListHTML = br.open("http://www.neopets.com/stockmarket.phtml?type=list&full=true")
    portfolioHTML = br.open("http://www.neopets.com/stockmarket.phtml?type=portfolio")

    stockPrices = extractStockPrices(stockListHTML)
    stockHoldings = extractStockHoldings(portfolioHTML)

    todaysBuy = pickStockPurchase(stockPrices, stockHoldings)
    if todaysBuy != "No Stocks at 15-17NP":
        buyResult = buyStocks(todaysBuy, br)
        logFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - "+buyResult+"\n")
    else:
        logFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - No stocks purchased, none available at 15-17NP/share.\n")

    todaysSales = pickStockSales(stockPrices, stockHoldings)

    if len(todaysSales) >= 1:
        successfulSale = sellStocks(todaysSales, br)
        if successfulSale:
            for stock in todaysSales.keys():
                logFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - "+str(int(round(todaysSales.get(stock))))+" shares of ["+stock+"] sold at "+str(stockPrices.get(stock))+" NP each.\n")
        else:
            logFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - Error: Something went wrong when trying to sell stocks.\n")


##
# Extracts the Stock tickers and values into a dictionary
##  
def extractStockPrices(stockListHTML):

    #Put the HTML source into a string
    stockListHTMLString = stockListHTML.read()

    #Trim the source down to just the table we care about
    startToken = "<table cellpadding=3 cellspacing=0 border=1 align=center><tr><td align=center bgcolor='#8888ff'><font color=white><b>Logo"
    endToken = "<br clear="
    startIndex = stockListHTMLString.index(startToken)
    endIndex = stockListHTMLString.index(endToken)    
    stockTableHtml = stockListHTMLString[startIndex:endIndex]

    #Pick out all of the HTML stuff our xml parser will choke on
    removeSubStrings = [["<b>",""],
                        ["</b>",""],
                        ["<table cellpadding=3 cellspacing=0 border=1 align=center>","<table>"],
                        [" bgcolor='#eeeeff'",""],
                        [" bgcolor='#8888ff'",""],
                        [" align=center",""],
                        [" width=60",""],
                        [" height=60",""],
                        [" border=0",""],
                        ["<font color=",""],
                        ["'green'>",""],
                        ["'red'>",""],
                        ["'black'>",""],
                        ["white>",""],
                        ["</font>",""],
                        ["</a>",""]]


    for i in removeSubStrings:
        stockTableHtml = stockTableHtml.replace(i[0], i[1])

    while stockTableHtml.find("<img src=") != -1:
        tempStartIndex = stockTableHtml.find("<img src=")
        tempEndIndex = stockTableHtml.find("gif'>") + 5
        tempSubString = stockTableHtml[tempStartIndex:tempEndIndex]
        stockTableHtml = stockTableHtml.replace(tempSubString, "")

    while stockTableHtml.find("<a href=") != -1:
        tempStartIndex = stockTableHtml.find("<a href=")
        tempEndIndex = stockTableHtml.find("'>") + 2
        tempSubString = stockTableHtml[tempStartIndex:tempEndIndex]
        stockTableHtml = stockTableHtml.replace(tempSubString, "")       

    stockTableHtml = stockTableHtml.replace("<td>Logo</td>", "")
    stockTableHtml = stockTableHtml.replace("<td></td>", "")

    ##
    # Aggregate into dictionary
    ##  


    stockValues = {}

    table = etree.XML(stockTableHtml)
    rows = iter(table)
    next(rows)
    for row in rows:
        stockValues[row[0].text] = int(row[4].text)

    return stockValues

##
# Extracts the Stock tickers and current holdings into a dictionary
#       Only adds stocks which are present in portfolio
##
def extractStockHoldings(portfolioHTML):

    #Put the HTML source into a string
    portfolioHTMLString = portfolioHTML.read()

    #Trim the source down to just the table we care about
    startToken = "<table align=center cellpadding=3 cellspacing=0 border=1>"
    endToken = "<span id='show_sell' style='display:none'><center><input type="
    startIndex = portfolioHTMLString.index(startToken)
    endIndex = portfolioHTMLString.index(endToken)   
    portfolioTableHtml = portfolioHTMLString[startIndex:endIndex]

    #Pick out all of the HTML stuff our xml parser will choke on
    while portfolioTableHtml.find("<tr id=") != -1:
        tempStartIndex = portfolioTableHtml.find("<tr id=")
        tempEndIndex = portfolioTableHtml.find("</table>\n</td>\n<tr>") + 21
        tempSubString = portfolioTableHtml[tempStartIndex:tempEndIndex]
        portfolioTableHtml = portfolioTableHtml.replace(tempSubString, "")    

    while portfolioTableHtml.find("<td align=\"center\" ><img") != -1:
        tempStartIndex = portfolioTableHtml.find("<td align=\"center\" ><img")
        tempEndIndex = portfolioTableHtml.find("\"></td>") + 7
        tempSubString = portfolioTableHtml[tempStartIndex:tempEndIndex]
        portfolioTableHtml = portfolioTableHtml.replace(tempSubString, "")    

    while portfolioTableHtml.find("<a href=") != -1:
        tempStartIndex = portfolioTableHtml.find("<a href=")
        tempEndIndex = portfolioTableHtml.find(">", tempStartIndex) + 1
        tempSubString = portfolioTableHtml[tempStartIndex:tempEndIndex]
        portfolioTableHtml = portfolioTableHtml.replace(tempSubString, "")

    tempStartIndex = portfolioTableHtml.find("<tr bgcolor=\"#BBBBBB\">")
    tempEndIndex = portfolioTableHtml.find("</tr>", tempStartIndex) + 5
    tempSubString = portfolioTableHtml[tempStartIndex:tempEndIndex]
    portfolioTableHtml = portfolioTableHtml.replace(tempSubString, "")  


    removeSubStrings2 = [["<td bgcolor='#ccccff' colspan=2>&nbsp;</td>",""],
                        ["<td bgcolor='#ccccff' align=center colspan=3><b>Today</b></td>",""],
                        ["<td bgcolor='#ccccff' align=center colspan=2><b>Holdings</b></td>",""],
                        ["<td bgcolor='#ccccff' align=center colspan=2><b>Overall</b></td>",""],
                        ["<td align=center bgcolor='#ccccff'><b>Icon</b></a></td>",""],
                        ["<tr>\n\n\n\n\n</tr>",""],
                        ["<tr><td align=\"right\" colspan=\"5\">Totals:</td><td\">4,000</td>",""],
                        ["<tr><td align=\"right\" colspan=\"5\">Totals:</td><td\">4,000</td>",""],
                        ["<tr><td align=\"right\" colspan=\"5\">Totals:</td><td\">4,000</td>",""],
                        ["<b>",""],
                        ["</b>",""],
                        ["<table align=center cellpadding=3 cellspacing=0 border=1>","<table>"],
                        [" bgcolor=\"#EEEEFF\"",""],
                        [" bgcolor=\"#FFFFFF\"",""],
                        [" bgcolor=\"#BBBBBB\"",""],
                        [" bgcolor='#ccccff'",""],
                        [" align=\"center\"",""],
                        [" align=center",""],
                        ["<font color=\"",""],
                        ["<font size=1>(profile)",""],
                        ["green\">",""],
                        ["red\">",""],
                        ["black\">",""],
                        ["</font>",""],
                        ["</a>",""],
                        ["<nobr>",""],
                        ["</nobr>",""],
                        ["<br>",""]]

    for i in removeSubStrings2:
        portfolioTableHtml = portfolioTableHtml.replace(i[0], i[1])


    ##
    # Aggregate into dictionary
    ##  

    stockHoldings = {}

    table = etree.XML(portfolioTableHtml)
    rows = iter(table)
    next(rows)
    for row in rows:
        stockHoldings[(row[0].text).strip()] = int(row[4].text.strip().replace(",",""))

    return stockHoldings

##
# Picks the stock to purchase for the day by checking which ones are at 15 NP
# If multiple stocks are at 15 NP, it buys the one we currently own the least
# amount of. If there is a tie, it decided between them randomly.
##     
def pickStockPurchase(prices, holdings):

    #Make a list of the stocks at 15NP and a list of raw holdings for easy use of min later
    # If no stocks at 15NP / share then look for 16 and even 17 if necessary
    potentialPurchases = []
    holdingsValues = []
    stocksAtPrice = False
    targetPrice = 15
    while not(stocksAtPrice) and targetPrice <= 17:
        for ticker,price in  prices.iteritems():
            if price == targetPrice:
                stocksAtPrice = True
                if ticker in holdings:
                    potentialPurchases.append([ticker, holdings.get(ticker)])
                    holdingsValues.append(holdings.get(ticker))
                else:
                    potentialPurchases.append([ticker, 0])
                    holdingsValues.append(0)
        targetPrice = targetPrice + 1


    #Go through the possible cases for potentialPurchases, act accordingly         
    if len(potentialPurchases) == 0:
        return "No Stocks at 15-17NP"
    elif len(potentialPurchases) == 1:
        return potentialPurchases[0][0]
    else:      #Most complicated possibility, pick one we own the least shares of,
                #randomly selected in event of tie.
        minHoldings = min(holdingsValues)
        shortList = []
        for stock in potentialPurchases:
            if stock[1] == minHoldings:
                shortList.append(stock[0])
        if len(shortList) == 1:
            return shortList[0]
        else:
            randomPick = random.choice(shortList)
            return randomPick


##
# Actually buys 1000 shares of the stock picked buy pickStockPurchase()
# Relies on the index of the form and inputs, hopefully this doesn't change.
##        
def buyStocks(ticker, browser):

    #The stock buying page URL
    buyPage = "http://www.neopets.com/stockmarket.phtml?type=buy"

    browser.open(buyPage)
    #The form we want isn't named, but it's the second one on the page
    browser.select_form(nr=1)
    #selecting the controls by name doesn't work, so we get them by index
    controls = browser.form.controls
    controls[2]._value = ticker # the ticker
    controls[3]._value = "1000"   # the number of shares

    humanizingDelay(5,minLength=1)
    response = browser.submit()

    #check that everything worked, return a string with the result
    if response.geturl() == "http://www.neopets.com/stockmarket.phtml?type=portfolio":
        return "Success: 1000 shares of ["+ticker+"] have been purchased."
    elif response.geturl() == "http://www.neopets.com/process_stockmarket.phtml":
        responseHTML = response.read()
        startToken = "<b>Error:"
        endToken = "</div>"
        startIndex = responseHTML.index(startToken)
        endIndex = responseHTML.index(endToken,startIndex)   
        errorString = responseHTML[startIndex:endIndex].replace("</b>","").replace("<b>","")
        return errorString
    else:
        return "Error: Unknown problem occured while buying stocks."





##
# Decides if any of the stocks in our portfolio are beyond the sale threshold.
# All of the current holdings are sold if they are beyond. Returns a Dictionary
# of Ticker and number of stocks to sell.
##         
def pickStockSales(prices, holdings):

    sellThreshold = 50
    stocksToSell = {}

    # Go through the stocks we own, check if we should sell, then if so
    # add to list at half the currently owned shares (rounded up)
    for ticker in holdings.keys():
        if prices.get(ticker) >= sellThreshold:
            stocksToSell[ticker] = holdings.get(ticker)
    return stocksToSell



##
# Implements the actual selling of the stocks from pickStockSales()
# Returns a boolean indicating success (for log file purposes)
##         
def sellStocks(salesList, browser):

    salesPage = "http://www.neopets.com/stockmarket.phtml?type=portfolio"
    browser.open(salesPage)
    #The form we want isn't named, but it's the second one on the page
    browser.select_form(nr=1)
    #We don't know the exact names of the inputs, they have a ref number, time to search:
    controls = browser.form.controls
    for control in controls:
        try:
            if len(control.name) > 10:
                if control.name[5:control.name.find("]")] in salesList:
                    control._value = "1000"
        except TypeError:
            pass

    humanizingDelay(5,minLength=1)
    response = browser.submit()

    #check that everything worked, return a string with the result
    if response.read().find("There were no successful transactions") == -1:
        return True
    else:
        errorHTMLdump.write("/n"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"/n"+response.read())
        return False


main()
```

The script is broken down into a pretty logical sequence as it's very procedural. It starts with the main function which deals with logging in, collecting bank interest and withdrawing neopoints for the stock market purchase if necessary, and then finally playing the stock market. Finally, it goes to deposit the neopoints gained from the stock market if any sales were made, then logs out. Pretty simple on the face of it, but the real interesting parts are the actual interactions with the webpages. In order for our bot to be able to do anything meaningful we need to first extract the information we care about from the page, then have the script make the right decisions using that information, and finally put the calculated input values into the right fields and submit the data. For the login, and bank portions of this bot, that's fairly simple; it's just a matter of going to the correct url selecting the right forms, and submitting a static or otherwise easy to calculate value that is pulled out of the HTML by finding some substrings that encapsulate the data we're after.

<div id="attachment_1222" style="width: 673px" class="wp-caption aligncenter">
  <a href="/wp-content/uploads/2014/09/Screenshot-from-2014-09-27-144658.png"><img class="wp-image-1222 size-full" src="/wp-content/uploads/2014/09/Screenshot-from-2014-09-27-144658.png" alt="Screenshot from 2014-09-27 14:46:58" width="663" height="797" srcset="/wp-content/uploads/2014/09/Screenshot-from-2014-09-27-144658.png 663w, /wp-content/uploads/2014/09/Screenshot-from-2014-09-27-144658-249x300.png 249w" sizes="(max-width: 663px) 100vw, 663px" /></a>

  <p class="wp-caption-text">
    The list of Neodaq stocks and their prices.
  </p>
</div>

The stockManager() function is a little less straight forward. The Neopets stock market game is a simple html form based game, which makes most of this possible (building a bot to interact with flash content? No thank you!). This means that we use the same techniques as we did for the login and bank pages, we're just after information that is a presented in a slightly more complex way as an HTML table. We're interested in the structure of the table, and we need to maintain that, just without all of the HTML bits that don't mean anything to us. This is done through the extractStockPrices() and extractStockHoldings() functions. They both work in pretty much the same way, by taking the entire HTML page as a string, isolating the table of interest, stripping out some of the problematic HTML bits, then putting it all into a dictionary that maintains the data structure using XML.

<div id="attachment_1223" style="width: 671px" class="wp-caption aligncenter">
  <a href="/wp-content/uploads/2014/09/Screenshot-from-2014-09-27-144728.png"><img class="wp-image-1223 size-full" src="/wp-content/uploads/2014/09/Screenshot-from-2014-09-27-144728.png" alt="Screenshot from 2014-09-27 14:47:28" width="661" height="800" srcset="/wp-content/uploads/2014/09/Screenshot-from-2014-09-27-144728.png 661w, /wp-content/uploads/2014/09/Screenshot-from-2014-09-27-144728-247x300.png 247w" sizes="(max-width: 661px) 100vw, 661px" /></a>

  <p class="wp-caption-text">
    My portfolio of Neodaq stocks.
  </p>
</div>

Finally, with the data isolated from the formatting, we can figure out what it is we actually want to do. This is accompolished using the pickStockPurchase(), buyStocks(), pickStockSales(), and sellStocks() functions. The pickStockPurchases() function goes through the dictionary of stocks with their prices we just made and looks for stocks in the 15-17 NP per share range. It then selects the lowest priced one that we currently own the least of. The buyStocks() function then simply purchases 1000 shares of this stock (which is the maximum number of shares any one user can purchase per day). The pickStockSales() function then looks at our portfolio of stocks and finds any that surpass the user defined sale threshold. It puts all stocks that need to be sold into a list and then the sellStocks() function takes care of actually selling them. The sellStocks() function sells off 100% of the holdings of any stock that meets this criteria which keeps things simpler, as the sales page is built in such a way that a single stock is broken down into each of the individual purchases that went into it rather than the total holdings. We originally purchased the stock in 1000 share units, which means the bot can simple put 1000 into all of the input fields that belong to that ticker to completely divest that stock.

Now you may have noticed that there is no means of ensuring that your bank account contains enough neopoints to facilitate the 17,000 NP withdrawal at the start. This means that it is necessary to ensure your seed capital is sufficient that you won't burn through it before you start seeing returns. How long it takes before you start seeing returns is a matter of what your sales threshold is set at. For the most part, stocks on the Neopets stock market follow a pretty predictable pattern of swinging back and forth between about 6 and 60 NP per share. It's less common, but stocks do periodically move to above this 60 NP range before they begin falling back to the 6 NP area. What this means for you is that the higher you set your sales threshold, the longer it will be before you see returns (although the returns will be larger). So if you are starting with a smaller pool of seed capital, it will make sense to use a lower threshold so that you won't run into an empty bank account. Personally I started with the 1.5 million NP that were in my account from long ago, and used a sales threshold of 45 NP per share to start. If I recall correctly, the balance in my bank account never dropped below about 750,000 NP before I started earning it back. Since there is a strong element of randomness in all of this it is a very good idea to have more seed capital than you think you'll need at your chosen sale threshold. A lot of people like to pick a return of 1,000,000 NP per month as their goal. To achieve this you need to earn a daily return of almost 33,000 NP per day (12 million divided by 365 days). You're buying 1000 shares at up to 17,000 NP each day, so this means you should sell these shares at 33 NP per share above what you paid. This works out to a nice round number of 50 NP per share. Nice. This isn't really a bad sales threshold to start at if you have the bank balance to support it.

For those lucky enough to have a very large sum of neopoints in their bank account, the burn rate will not even be an issue. This is because the bot collects bank interest. If your bank interest is in excess of 17,000 NP per day (the maximum this bot will ever spend on stocks) then you will never see a net decrease in your account balance. You'd need to have a bank balance of 49,640,000 NP before this would be the case though, so you're probably not going to be in this privileged position to begin with. But that's enough theory on burn rates and returns. [If you want to read and learn more about this stuff then there are plenty of places to start.](https://www.google.ca/search?q=neopets+stock+market+guide)

Throughout this whole process the script also keeps detailed logs of what it is doing. This allows you to quickly check up on the progress of the bot without logging in to Neopets and then trying to figure out what has happened since you last looked.

<div id="attachment_1224" style="width: 728px" class="wp-caption aligncenter">
  <a href="/wp-content/uploads/2014/09/Screenshot-from-2014-09-27-150659.png"><img class="wp-image-1224 size-full" src="/wp-content/uploads/2014/09/Screenshot-from-2014-09-27-150659.png" alt="Screenshot from 2014-09-27 15:06:59" width="718" height="396" srcset="/wp-content/uploads/2014/09/Screenshot-from-2014-09-27-150659.png 718w, /wp-content/uploads/2014/09/Screenshot-from-2014-09-27-150659-300x165.png 300w, /wp-content/uploads/2014/09/Screenshot-from-2014-09-27-150659-672x372.png 672w" sizes="(max-width: 718px) 100vw, 718px" /></a>

  <p class="wp-caption-text">
    The log file.
  </p>
</div>

So now that we have the script, it'd be nice to have a way to make it run automatically each day too, right? If you're a linux or mac user, then there're two wonderful tools called cron and anacron that can accomplish this. I prefer anacron since it will work on systems that are not guaranteed to be on when the task is is scheduled; it'll simply ensure the task is run once per day if the computer is turned on at all during that day. Cron also works well on server like systems with near 100% uptime. [Windows users will have to use the windows task scheduler which has a fairly similar mechanic to cron and anacron.](http://windows.microsoft.com/en-ca/windows/schedule-task#1TC=windows-7)

But lets just go ahead and look at the process for setting up anacron:

To schedule a task with anacron, we use anacrontab:

`<br />
sudo nano /etc/anacrontab<br />
`

There will be a few lines in there already. At the bottom you simply want to add the following one:

`<br />
1 6 cron.daily nice python /<PATH TO FILE>/stockbot.py >/dev/null<br />
`

What this does is tells the system to run the task daily, with a delay of 6 minutes after start up. It assigns the task to cron.daily label (you can change this), and then executes the command &#8220;python /<directories>/stockbot.py&#8221; and sends any CLI output to null (basically computer oblivion).

[You can learn more about cron and anacron here.](https://www.digitalocean.com/community/tutorials/how-to-schedule-routine-tasks-with-cron-and-anacron-on-a-vps)

And that's that! You now have a Neopets stock market bot running daily and earning you free neopoints. Congrats. It only took about 10 years.
