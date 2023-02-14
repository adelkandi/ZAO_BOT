# ZAO_BOT
A Costomized Discord BOT for fun and jokes
_____________________________________________________________________________________________________
ZAO_BOT is a simple Discord chatbot that uses the Discord API to communicate with users. This bot has been designed to bring joy and laughter to the conversation by providing random jokes from the OpenAI API text-davinci-003 API and local jokes stored in a JSON data file.The bot also can generate random jokes from the Chuck Norris joke API.

# Features
1. Respond to users with a random jok from the Chuck Norris API whenever a user mentions a word from the "Words_List".
2. Provide a random jok from the Chuck Norris API when the user types "$jk".
3. Add a New Local Joke to the JSON data file using "$joke/update" command.
4. Delet a local joke from the JSON data file using the "$joke/delete" command.
5. Show the list words that trigger the bot to send a joke using the "$Word_List" command.

# Requirments
1. A Discord account and a server.
2. A OpenAi API key , wich can be obtained from OpenAI website.
3. A Chuck Norris API key, Which can be obtained from the Chuck Norris API website.
4. the latest version of python.
5. The following Python libraries:
    + discord
    + requests
    + json
    + os
    + dotenv 
    + openai
- Or you can use replite to past the code and Host the bot from there using some methodes that will help if your server is online 24/7 so the bot will stay Online even the computer is OFF

# Setup
1. Clone or download the ZAO_BOT repositry.
2. Install the python Librarys ``` pip install -r requirments.tx```
3. Creat a new file named ".env" in same directory as the code.
4. In the ".env" file, store the Discord API token as a key-value : `DiSCORD_TOKEN = your_token`.
5. Store the OpenAi key in the ```.env``` file as a key-value : `API_Key = your_key`
6. Run the code using the command `python3 ZAO_BOT.py`.

# Contribution

Feel Free to contribute to this BOT by fixing bugs,adding new features, or improving the code. if you have any questions or suggestions,, please open an issue in the repository.

# License

This Project is licensed under the MIT License.

