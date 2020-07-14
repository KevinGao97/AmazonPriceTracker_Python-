# AmazonPriceTracker_Python-

This python script allows users to track when one or multiple Amazon item has dropped below their desired price through the use of gmail.
The script will periodically check the prices of the items, specified by the user. 

### Dependencies 
```text
bs4(Beautiful Soup)
requests
html5lib
```
### Setup
1. Please ensure you are using Python version 3.6.0 or up.
2. To install the necessary dependencies, run the following: ```pip install -r requirements ```
3. This script requires the use of a Google Mail(Gmail) account with the option 'Less secure app access' enabled in the gmail settings.

### Features
- Price tracks multiple amazon items with a different desired price for each item. 
- Saves all tracked items into a csv file, keeps track of items in the file that have fallen below desired price. 
- First time setup that saves the user's sender email, password, and recipient email into a text file. The script checks for this file everytime it's used.
- Adjustable checking time delay specified by the user(Default is 15 minutes).
  - Can be changed to be a 1 minute to 1 day delay when checking each item's amazon link.  
- Tracks the lowest price on the page, even when there is a 'lightning' or 'limited-time' deal. 

### Notes
Please do not use Pycharm to run this script. There is a known issue in Pycharm when inputting a hyperlink into the terminal

### Contributors

Kevin Gao

### License & Copywrite

Licensed under [MIT License](LICENSE)
