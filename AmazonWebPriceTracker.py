import requests
from bs4 import BeautifulSoup
import smtplib
import time

"""
NOTES:
Please do not use Pycharm as there is a known bug with the IDE when inputting a hyperlink into the terminal 

"""
print("Welcome to the Amazon Price Tracking Script!")


URL = input("Please enter full Amazon URL: ")
desired_price = float(input("Please enter desired price: "))
senderEmail = input("Please enter sender email: ")
senderPassword = input("Please enter sender password: ")
recipientEmail = input("Please enter recipient email: ")

print("This next part will prompt for the subject and body of the email")

subjectMsg = input("Please enter the subject line of the email: ")
bodyMsg = input("Please enter the body of the email: ")

headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}

def main():


    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')


    title = soup.find(id="productTitle").get_text()
    price = soup.find(id= "priceblock_ourprice").get_text()
    converted_price = float(price[5:10].replace(',', ''))   #extracts the first 5 elements of the price string

    
    if(converted_price < desired_price):
        send_email()


    print(converted_price)
    print(title.strip())

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

main()


#Will check every minute
#60*60 will check every day
'''
while(True):
    check_price()
    time.sleep(60)

'''
