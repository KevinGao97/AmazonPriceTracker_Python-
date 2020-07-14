import requests
from bs4 import BeautifulSoup
import smtplib
import time
import os.path
import csv
import random

"""
NOTES:

Please do not use Pycharm to run this program due to a known bug with the IDE when inputting a hyperlink into the terminal.

"""

headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}


"""
Creates a new file to store senderEmail, senderPassword, and receipientEmail as needed by the mail server when running the script the first time. 
If the text file already exists, the program pulls these information from the text file.
"""
def firstTimeCheck():

    filename = 'info.txt'
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            senderEmail = f.readline().strip('\n')
            print("Sender Email: " + senderEmail)
            senderPassword = f.readline().strip('\n')
            print("Sender Email Password: " + senderPassword)
            recipientEmail = f.readline().strip('\n')
            print("Recipient Email: " + recipientEmail)
            f.close()
    else:
        print("The info.txt file was not found. Please enter the necessary information below to create a new info.txt file.")
        senderEmail = input("Please enter sender email: ")
        senderPassword = input("Please enter sender password: ")
        recipientEmail = input("Please enter recipient email: ")
        with open(filename, 'w') as f:
            f.write(senderEmail +'\n')
            f.write(senderPassword +'\n')
            f.write(recipientEmail +'\n') 
            f.close()

    return senderEmail, senderPassword, recipientEmail


"""
Prompts the user for the time delay, in minutes, to check amazon for all items in the 'items.txt' file.
"""
def checkTimeDelay():

    timeDelayMinutes = 15

    print("Welcome to the Amazon Price Tracking Script!")
    timeDelayMinutes = input("When do you want this script to check amazon periodically(in minutes)? ")

    try:
        timeDelayMinutes = int(timeDelayMinutes)
        if timeDelayMinutes is 0:
                exit(0)
    except ValueError:
        print("Not a valid integer. Please enter a positive integer")
        exit(1)
    except UnboundLocalError:
        print("Not a valid integer. Please enter a positive integer")
        exit(1)
    
    return timeDelayMinutes


"""
Checks whether the script has been ran before with the 'items.txt' and 'itemsPriceDropped.txt' being created.
Asks the user whether they wish to use the existing 'items.txt' or create a new one during execution of the script.
 
"""
def checkExistingItemsFile():

    itemsFile = 'items.txt'
    itemsDroppedLstFile = 'itemsPriceDropped.txt'

    if os.path.isfile(itemsFile) and os.path.isfile(itemsDroppedLstFile):
        while True:
            answer = input("An items.txt file already exist. Would you like to remove the existing 'items.txt' file? ")
            if answer.lower() in ['y', 'yes', 'n', 'no']:
                if answer.lower() in ['y', 'yes']:
                    os.remove(itemsFile)
                    os.remove(itemsDroppedLstFile)
                    break
                else:
                    break
            else:
                print("Please answer with 'y', 'yes', 'n', 'no' ")



"""
Prompts the user for the number of items they wish to track, prompts for the links one by one, and adds all the Amazon URL links into a list.
"""
def createItemLst():    

    urlLst = []
    numEntries = 0

    
    entries = input("How many amazon items would you like to track? ")

    try:
        numEntries = int(entries)
        if numEntries is 0:
            exit(0)
    except ValueError:
        print("Not a valid integer. Please enter a positive integer")
        exit(1)
    except UnboundLocalError:
        print("Not a valid integer. Please enter a positive integer")
        exit(1)

    for i in range(numEntries):
        response = input("Please enter the full Amazon URL of item #{}: ".format(i+1))
        urlLst.append(response)
    return urlLst


"""
Takes the list of URLS, scraps the title of each respective link, and appends these information, along with user's desired price to a text file called 'items.txt'
The function also creates a random int ID to track each item.
'items.txt' has the following format:

title, desired price, unique id, link
"""
def convertLinkToFile(lst):

    for i in range(len(lst)):
        page = requests.get(lst[i], headers=headers)
        soup = BeautifulSoup(page.content, 'html5lib')
        title = soup.find(id = "productTitle").get_text()
        price = input("Please enter desired price of {}: ".format(title.rstrip().strip()))
        myfile = open('items.txt', 'a')    
        myfile.write(title.replace(",", "").rstrip().strip() +',')          
        myfile.write(price +',')
        myfile.write(str(random.randint(0, 1000000) ) + ',')
        myfile.write(lst[i])
        myfile.write('\n')
        
    myfile.close()
     

"""
Opens the saved 'items.txt' and parses each row/item one-by-one, extracting the URL, desired price, ID, and link. 
The function checks whether the desired price is below the current price and sends out an email accordingly. 
If an email was already sent out for an item that has reached the desired price, the function moves onto the next row. 
The function also performs the first time check to ensure all relevant information is collected for the email portion. 
"""
def readItemsFileAndCheck():

    senderEmail, senderPassword, recipientEmail = firstTimeCheck()
    emailSentOnItemsLst = []
    
    #Saves the list of item IDs which the desired price has dropped below the current price and an email was already sent to the user.
    if os.path.isfile("itemsPriceDropped.txt"):
        with open("itemsPriceDropped.txt", "r") as fp:
            data2 = eval(fp.readline())
            emailSentOnItemsLst = data2

    with open ('items.txt', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        itemCount = 0
        
        for row in csv_reader:
            print(f'\t Title: {row[0]} Desired Price: {row[1]}. ID: {row[2]} URL: {row[3]}.') 
            
            id = int(row[2])
            itemCount += 1

            if id in emailSentOnItemsLst:
                print("=========== An email was already sent for this item. ===========")
                print('\n')
            else:
                URL = row[3]
                desiredPrice = float(row[1])

                subjectMsg = 'Price Dropped On: ' + row[0]
                desiredPriceMsg = 'Desired Price: $' + str(desiredPrice)
                bodyMsg = 'Please check the following link: ' + URL
        

                page = requests.get(URL, headers=headers)
                soup = BeautifulSoup(page.content, 'html5lib')
                try:
                    price = soup.find(id = "priceblock_dealprice").get_text()
                except AttributeError:
                    try:
                        price = soup.find(id = "priceblock_saleprice").get_text()
                    except AttributeError:
                        try:
                            price = soup.find(id = "priceblock_ourprice").get_text()
                        except AttributeError:
                            print("Cannot find price of the item.")
                            exit(1)
                actualPrice = float(price[5:10].replace(',', ''))
    
                if(actualPrice < desiredPrice):
                    sendEmail(subjectMsg, bodyMsg, desiredPriceMsg, senderEmail, senderPassword, recipientEmail)
                    emailSentOnItemsLst.append(id)
                
                #Adds the item id to the list of item prices that have dropped below desired price and an email was sent
                with open('itemsPriceDropped.txt', 'w') as fp:
                    fp.write(str(emailSentOnItemsLst))

        #Exits the script when all items have reached desired price and an email was sent out for each item respectively. 
        if itemCount == len(emailSentOnItemsLst):
            print("All items have reached their desired prices and an email was sent out for each item. This script will exit shortly...")
            exit(0)

    return itemCount



"""
This function initializes the Gmail port, connecting with the sender email and the specified generated password from gmail.
Once this connection has been established, it creates a new email with a subject and mail body, as specified by the user, and sends the email.

"""
def sendEmail(subjectMsg, bodyMsg, desiredPriceMsg, senderEmail, senderPassword, recipientEmail):

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    try:
        server.login(senderEmail, senderPassword)
    except smtplib.SMTPAuthenticationError:
        print("The sender username and password combination is invalid. Please check the info.txt file.")
        exit(1)

    msg = f"Subject: {subjectMsg}\n\n{desiredPriceMsg}\n\n{bodyMsg}"

    server.sendmail(senderEmail, recipientEmail, msg)
    print("An email has been successfully sent to: "+ recipientEmail)
    server.quit()


"""
The Main Function

"""
def main():

    timeDelay = checkTimeDelay()
    checkExistingItemsFile()
    urlLst = createItemLst()
    convertLinkToFile(urlLst)

    fileChecks = 1

    #Continous checking
    while True:
        readItemsFileAndCheck()
        time.sleep(60*timeDelay)
        fileChecks += 1
        print("The script is on loop {} with a {} minute checking delay".format(fileChecks,timeDelay))


main()


