import requests
from bs4 import BeautifulSoup
import smtplib
import time
import os.path

"""
NOTES:

Please do not use Pycharm as there is a known bug with the IDE when inputting a hyperlink into the terminal 

"""

filename = 'info.txt'

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
    

URL = input("Please enter full Amazon URL: ")

desired_price = float(input("Please enter desired price: "))


print("This next part will prompt for the subject and body of the email")

subjectMsg = input("Please enter the subject line of the email: ")
bodyMsg = input("Please enter the body of the email: ")

headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}

def main():

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text()
    try:
        price = soup.find(id= "priceblock_ourprice").get_text()
    except AttributeError:
        try:
            price = soup.find(id= "priceblock_saleprice").get_text()
        except AttributeError:
            print("Cannot find price")
     
    converted_price = float(price[5:10].replace(',', ''))   #extracts the first 5 elements of the price string
    print(converted_price)
    print(title.strip())

    if(converted_price < desired_price):
        send_email()
        exit(0)

"""
This function initializes the gmail port, connecting with the sender email and the specified generated password from gmail.
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

#Continous Checking
#60*60 will check every day
while(True):
    main()
    time.sleep(60)


