## Practical Language Processing Project Team 15
<img src="Images/chatbot.png"
     style="float: left; margin-right: 0px;" />

<br>
## Gastronomy Chatbot

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

**Step 1**. Install virtualenv and then create a python env.
For Mac: python3 -m pip install --user virtualenv
For Windows: "py -m pip install --user virtualenv"

**Step 2**. Install virtualenv and then create a python env.
For Mac: "python3 -m pip install --user virtualenv"

**Step 3**. Activate the python env. You should see (env) next to your command line.
For Mac: "source env/bin/activate"
For Windows: "env\Scripts\activate"

**Step 4**. In the command prompt/terminal CD to the project folder "<your-file-path>/Gastro_advisor_IS_PLP”. Enter "pip install -r requirements.txt" OR "pip3 install -r requirements.txt".  This will install all the required dependencies.

**Step 5**. Once installation is complete, enter " flask run". This will deploy your server locally on your pc.

**Step 6**. You need to open a channel to your computer so that telegram bot can communicate with your server. To do this, we will use ngrok. With a new command prompt/terminal CD to the project root folder "<your-file-path>/Gastro_advisor_IS_PLP". There will be an "ngrok_win" and an "ngrok_mac" file. Rename the file with your OS in use to just "ngrok". E.g If you are using MAC OS, delete the "_mac" from "ngrok_mac".
From your command prompt, enter "ngrok http localhost:5000".
Take note of the https link. It should look something like this "https://f34bb6f6.ngrok.io". Take note of this link.

**Step 7**. Go to https://dialogflow.cloud.google.com/ and log in with your account. Proceed to iImport the dialogflow agent(IPA-AIRBNB.zip) on dialogflow.
To do this, first create a new agent and give it a name e.g. "AIRBNB AGENT".
Once created click on the settings gear icon next the agent name and click the "Export and Import" tab.
Click "Import From Zip" and select the IPA-AGENT zip file. Type in "IMPORT" into the text box and click "IMPORT".

**Step 8**. Once the agent has been imported and training is done, click on the "Fulfillment" option on the left menu bar. Enable the webhook(If it is not enabled), and copy and paste the ngrok https link on the URL field. Add in "/get_recommendations" right at the end of the ngrok link. Scroll to the bottom and click save. Give it some time to save your settings.

**Step 9**. Set up the link between telegram and dialogflow. From dialogflow, click Integrations. Check the Telegram box. A pop-up will appear, enter the bot_token key and click start. This will integrate the bot and dialogflow together.

**Step 10**. Now open up your telegram app from the smartphone. From the search bar of your chat page, type "IPAAIRBNBBot" click on “IPA-AIRBNB-BOT”. A chat window will be created with the bot, click 'Start'. You can now test sending some search queries such as "Can you find some recommendations for 2 adults, 1 child and 1 infant to stay in Vienna from 5th June to 17th June?". Alternatively, you can open the conversation with “Can you find me some recommendations” and the chatbot will proceed to ask you necessary questions before searching on Airbnb for your recommendations.

**Additional notes**: You can also test dialogs from the google assistant via the dialogflow website located on the right side of the screen.

-----------------------------------------------------------------------------------------------------

## SECTION 5 : PROJECT REPORT / PAPER

[Download the Project Report](http://tiny.cc/q2m5nz)

## SECTION 6 : MISCELLANEOUS

-----
