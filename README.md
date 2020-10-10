# Practical Language Processing Project Team 15 - Gastronomy Advisor (Chatbot)
<img src="Images/chatbot.png"
     style="float: left; margin-right: 0px;" />

<br>

## SECTION 1 : EXECUTIVE SUMMARY / PAPER ABSTRACT

To be completed...

## SECTION 2 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name  | Student ID (MTech Applicable)  | Work Items (Who Did What) | Email (Optional) |
| :------------ |:---------------:| :-----| :-----|
| LIM LI WEI | A0087855L | Refer to individual report | E0319479@u.nus.edu |
| YONG QUAN ZHI, TOMMY | A0195353Y | Refer to individual report | E0384984@u.nus.edu |
| RITESH MUNJAL | A0195304H | Refer to individual report | E0384935@u.nus.edu |
| SANTHIYAPILLAI RAJEEVAN PAUL | A0195399E | Refer to individual report | E0385030@u.nus.edu |

## SECTION 3 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO

[Gastronomy Advisor Video](https://www.youtube.com/)

## SECTION 4 : USER GUIDE
For a more detailed look at user guide, please refer to appendix 1 of the report for the user guide. 

Please ensure you are using python 3.6 or higher.
Once you have downloaded and unzipped the project file, CD into your project root folder "<your-file-path>/Gastro_advisor_IS_PLP"

This guide assumes that python 3.6 or higher has already been installed and pip has been installed as well.
**Step 1**. Install virtualenv.
For Mac: python3 -m pip install --user virtualenv
For Windows: py -m pip install --user virtualenv

**Step 2**. Create a python env.
For Mac: python3 -m venv env
For Windows: py -m venv env

**Step 3**. Activate the python env. You should see (env) next to your command line.
For Mac: "source env/bin/activate"
For Windows: "env\Scripts\activate"

**Step 4**. In the command prompt/terminal CD to the project folder "<your-file-path>/Gastro_advisor_IS_PLP”. Enter "pip install -r requirements.txt" OR "pip3 install -r requirements.txt".  This will install all the required dependencies.

**Step 5**. You need to open a channel to your computer so that telegram bot can communicate with your server. To do this, we will use ngrok. With a new command prompt/terminal CD to the project root folder "<your-file-path>/Gastro_advisor_IS_PLP". There will be an "ngrok_win" and an "ngrok_mac" file. Rename the file with your OS in use to just "ngrok". E.g If you are using MAC OS, delete the "_mac" from "ngrok_mac".
From your command prompt, enter "ngrok http localhost:5000".
Take note of the https link. It should look something like this "https://f34bb6f6.ngrok.io". Take note of this link.

**Step 6**. Copy the https ngrok link and go to constants.py file in the project folder. Paste the link into the variable 'URL'. Include a forward slash at the end of the link, it should look like this 'https://f34bb6f6.ngrok.io/'

**Step 7**. After step 4's installation has completed, from the command prompt CD to the project root folder "<your-file-path>/Gastro_advisor_IS_PLP” enter "flask run". This will deploy your server locally on your pc. Do take note that your localhost should be deploying on port 5000 "http://127.0.0.1:5000/"

**Step 8**. Next, go to your web browser and paste your ngrok https link to check if it can connect locally. You should see this text in the browser 'I am running flask server locally...'.

**Step 9**. Now you need to "inform" the telegram bot which server to send requests to. In your web browser, paste your https ngrok link and append it with '/setwebhook' and press Enter. e.g. https://f34bb6f6.ngrok.io/setwebhook. If it is successful you will see the message "webhook setup ok".

**Step 10**. To add the telegram bot to your telegram in the app's search field type "Gastrotomi" click the top result and this will add the bot to your telegram. Now you can use your telegram bot to and send a message it should reply messages you.

-----------------------------------------------------------------------------------------------------

## SECTION 5 : PROJECT REPORT / PAPER

[Download the Project Report](http://tiny.cc/q2m5nz)

## SECTION 6 : MISCELLANEOUS

-----
