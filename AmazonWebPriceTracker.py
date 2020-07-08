import requests
from bs4 import BeautifulSoup
import smtplib
import time
import os.path
import csv

"""
NOTES:

Please do not use Pycharm as there is a known bug with the IDE when inputting a hyperlink into the terminal 

"""


headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}

print("Welcome to the Amazon Price Tracking Script!")


"""
Creates a new file to store senderEmail, senderPassword, and receipientEmail as needed by the mail server when running the script the first time. 
If the text file already exists, the program pulls these information from the text file.
"""
def firstTimeCheck():

    filename = 'info.txt'
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            senderEmail = f.readline().strip('\n')
            print(senderEmail)
            senderPassword = f.readline().strip('\n')
            print(senderPassword)
            recipientEmail = f.readline().strip('\n')
            print(recipientEmail)
            f.close()
    else:
        print("The info.txt file is not found. The program will prompt you for the necessary information to create a new info.txt file.")
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
If the user only wishes to price track 1 item, we run this function.
"""
def oneItemCheck():

    senderEmail, senderPassword, recipientEmail = firstTimeCheck()
    URL = input("Please enter full Amazon URL: ")

    desired_price = float(input("Please enter desired price: "))

    print("This next part will prompt for the subject and body of the email")

    subjectMsg = input("Please enter the subject line of the email: ")
    bodyMsg = input("Please enter the body of the email: ")

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html5lib')

    try:
        title = soup.find(id = "productTitle").get_text()
    except AttributeError:
            print("There was a problem retrieving the item. Please try again later.")
            exit(1)
    try:
        price = soup.find(id = "priceblock_ourprice").get_text()
    except AttributeError:
        try:
            price = soup.find(id = "priceblock_saleprice").get_text()
        except AttributeError:
            print("Cannot find price of the item.")
            exit(1)
     
    converted_price = float(price[5:10].replace(',', '')) 
    print(converted_price)
    print(title.strip())

    if(converted_price < desired_price):
        send_email(subjectMsg, bodyMsg, senderEmail, senderPassword, recipientEmail)
        exit(0)
    

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
        elif numEntries is 1:
            while True:
                oneItemCheck()
                time.sleep(60)
    except ValueError:
        print("Not a valid integer. Please enter a positive integer")


    for i in range(numEntries):
        response = input("Please enter the full Amazon URL of item {}: ".format(i+1))
        urlLst.append(response)
    return urlLst


"""
Takes the list of URLS, scraps the title and price of each respective link, and appends these information, along with user's desired price to a text file called 'items.txt'
'item.txt' has the following format:

title, amazon price, desired price, link
"""
def convertLinkToFile(lst):
    
    nameLst = []
    
    for i in range(len(lst)):
        page = requests.get(lst[i], headers=headers)
        soup = BeautifulSoup(page.content, 'html5lib')
        title = soup.find(id = "productTitle").get_text()
        try:
            price = soup.find(id = "priceblock_ourprice").get_text()
        except AttributeError:
            try:
                price = soup.find(id = "priceblock_saleprice").get_text()
            except AttributeError:
                print("Cannot find price of the item.")
                exit(1)
        converted_price = float(price[5:10].replace(',', '')) 
        price = input("Please enter desired price of {}: ".format(title.rstrip().strip()))
        myfile = open('items.txt', 'a')    
        myfile.write(title.replace(",", "").rstrip().strip() +',')          
        myfile.write(str(converted_price) + ',')
        myfile.write(price +',')
        myfile.write(lst[i])
        myfile.write('\n')
        
        nameLst.append(title.rstrip().strip())
    myfile.close()
     

    for i in range(len(nameLst)):
        print(nameLst[i])
    return nameLst


def readItemFile():

    senderEmail, senderPassword, recipientEmail = firstTimeCheck()
    URL = ''
    desired_price = ''
    subjectMsg = 'Price Drop On: '
    bodyMsg = 'Please check the following link: '

    
    with open ('items.txt', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        itemCount = 0
        for row in csv_reader:
            print(f'\t Title: {row[0]} Amazon Price: {row[1]} Desired Price: {row[2]}. URL: {row[3]}.')
            URL = row[3]
            desired_price = float(row[2])
            subjectMsg = subjectMsg + row[0]
            bodyMsg = bodyMsg + row[3]

            page = requests.get(URL, headers=headers)
            soup = BeautifulSoup(page.content, 'html5lib')
            try:
                price = soup.find(id = "priceblock_ourprice").get_text()
            except AttributeError:
                try:
                    price = soup.find(id = "priceblock_saleprice").get_text()
                except AttributeError:
                    print("Cannot find price of the item.")
                    exit(1)
            converted_price = float(price[5:10].replace(',', ''))
            if(converted_price < desired_price):
                send_email(subjectMsg, bodyMsg, senderEmail, senderPassword, recipientEmail)
            itemCount += 1

        print(f'There are {itemCount} items.')

    return itemCount



"""
To do price check on multiple items:

check the first item, if not desired price, move on to next item.
Repeat this process every minute

"""

def main():

    senderEmail, senderPassword, recipientEmail = firstTimeCheck()

    urlLst = createItemLst()
    convertLinkToFile(urlLst)
    readItemFile()
    

"""
This function initializes the Gmail port, connecting with the sender email and the specified generated password from gmail.
Once this connection has been established, it creates a new email with a subject and mail body, as specified by the user, and sends the email.

"""
def send_email(subjectMsg, bodyMsg, senderEmail, senderPassword, recipientEmail):

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login(senderEmail, senderPassword)

    msg = f"Subject: {subjectMsg}\n\n{bodyMsg}"

    #sendmail(FROM, TO, MSG)
    server.sendmail(senderEmail, recipientEmail, msg)
    print("An email has been successfully sent!")
    server.quit()

main()

"""
#Continous checking every minute
while(True):
    main()
    time.sleep(60)

"""
