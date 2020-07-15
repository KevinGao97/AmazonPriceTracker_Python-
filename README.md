# AmazonPriceTracker_Python-

This python script allows users to track when one or multiple Amazon item has dropped below their desired price through the use of gmail.
The script will periodically check the prices of the items, specified by the user. 

### Dependencies 
```
bs4(Beautiful Soup)
requests
html5lib
```
### Setup
1. Please ensure you are using Python version 3.6.0 or up.
2. To install the necessary dependencies, run the following in CMD or terminal: ```pip install -r requirements ```
3. This script requires the use of a Google Mail(Gmail) account with the option 'Less secure app access' enabled in the gmail settings.
4. Running the script for the first time, it will prompt for all the necessary information in sending the alert email which includes:
    - Sender's email address
    - Sender's email password(Requires a Gmail generated app password)
    - Recipient email address
5. The script will prompt for the amazon item information and desired price through terminal. Additionally, it will output information regarding the current item currently being tracked.
    - After exiting the script, the current items csv file will be saved locally.  

### Features
- Price tracks multiple amazon items with a different desired price for each item. 
- Saves all tracked items into a csv file, keeps track of items in the file that have fallen below desired price. 
- First time setup that saves the user's sender email, password, and recipient email into a text file. The script checks for this file everytime it's used.
- Adjustable checking time delay specified by the user(Default is 15 minutes).
  - Can be changed to be a 1 minute to 1 day delay when checking each item's amazon link.  
- Tracks the lowest price on the page, even when there is a 'lightning' or 'limited-time' deal. 

### Notes
Please do not use Pycharm to run this script. There is a known issue in Pycharm when inputting a hyperlink into the terminal.

### Contributors

Kevin Gao

### License & Copywrite

Licensed under [MIT License](LICENSE)
