import requests
from bs4 import BeautifulSoup
import smtplib
import time
import os.path
from fake_useragent import UserAgent

"""
NOTES:

Please do not use Pycharm as there is a known bug with the IDE when inputting a hyperlink into the terminal 

"""
#ua = UserAgent()

filename = 'info.txt'
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}

print("Welcome to the Amazon Price Tracking Script!")

#Creates a new file to store senderEmail, senderPassword, and receipientEmail when running the script the first time
#If the text file already exists, the program pulls these information from the file
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
    
urlLst = []
numEntries = 0

entries = input("How many amazon items would you like to track? ")

try:
    numEntries = int(entries)
    if numEntries is 0:
        exit(0)
except ValueError:
    print("Not a valid integer. Please enter a positive integer")


for i in range(numEntries):
    response = input("Please enter the full Amazon URL of item {}: ".format(i+1))
    urlLst.append(response)

def convertLinkToFile(lst):
    
    nameLst = []
    
    for i in range(len(lst)):
        page = requests.get(urlLst[i], headers=headers)
        soup = BeautifulSoup(page.content, 'html5lib')
        title = soup.find(id = "productTitle").get_text()
        price = input("Please enter desired price of {}: ".format(title.rstrip().strip()))
        myfile = open('items.txt', 'a')    
        myfile.write(title.rstrip().strip() +',')
        myfile.write(price +',')
        myfile.write(urlLst[i])
        myfile.write('\n')
        
        nameLst.append(title.rstrip().strip())
    myfile.close()
     

    for i in range(len(nameLst)):
        print(nameLst[i])
    return nameLst

convertLinkToFile(urlLst)

URL = input("Please enter full Amazon URL: ")

desired_price = float(input("Please enter desired price: "))

print("This next part will prompt for the subject and body of the email")

subjectMsg = input("Please enter the subject line of the email: ")
bodyMsg = input("Please enter the body of the email: ")



def main():

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
        send_email()
        exit(0)

"""
This function initializes the Gmail port, connecting with the sender email and the specified generated password from gmail.
Once this connection has been established, it creates a new email with a subject and mail body, as specified by the user, and sends the email.

"""
def send_email():
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

#Continous checking every minute
while(True):
    main()
    time.sleep(60)


