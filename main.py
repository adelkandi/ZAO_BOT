#Imports:
import discord
import os
from dotenv import load_dotenv
import requests  #  Make HTTPs requists to get DATA from API 
import json   
import openai 


#ZAO_BOT: 


load_dotenv()   # Load the .env file to hide the TOKEN
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")   
openai.api_key = os.getenv("API_Key")  # API_Key from OpenAI 

intents= discord.Intents.default()
intents.message_content = True
BOT = discord.Client(intents=intents)     # make the Bot connect with Discord 


# Helper function to get a Joke from the API 
def get_Joke():
    response = requests.get("https://api.chucknorris.io/jokes/random")  
    json_data = json.loads(response.text) # Convert the response to json file to store data
    Joke = json_data
    return(Joke['value'])



def get_Dav_Joke():        #function to requist text-davinci-003
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = "Give me a random funny joke",
        max_tokens = 50,
        n = 1,
        stop = None,
        temperature = 0.5,
        )
    dav_Joke = response.choices[0].text.strip()
    print("Joke data:",dav_Joke)   # to see on terminal and debug 
    return dav_Joke



def Update_jk(jk_message):               # Update and add new Local Jokes to json data file 
    with open("Data.json","r") as file:
        Data= json.load(file)
    if "jk" in Data:
        jk =Data["jk"]                  # on "jk" key its stored all the data 
        jk.append(jk_message)
        with open("Data.json","w") as file :
            json.dump(Data,file)
        Data["jk"] = jk
    else :
        Data["jk"] = [jk_message]

def Delet_jk(index):            # Delete a Local Joke from json data file 
    with open("Data.json","r") as file:
        Data= json.load(file)
    jk= Data["jk"]
    if len(jk) > index :
        del jk[index]
        with open("Data.json","w") as file:
            json.dump(Data,file)
        Data["jk"] = jk




# Event when the Bot has switched from Offline  to Online
@BOT.event
async def on_ready():
    print ("We have logged in as{0.user}".format(BOT))      # When the Bot get ready it will be activated


# Event When the Bot sence a Message 
@BOT.event
async def on_message(message):
    #check if the message from the same BOT
    if message.author == BOT.user:
        return
    
    # User command reply :
    # with text-davenci-003:
    if message.content.startswith('$jk/dav'):
        print("openai api key:",openai.api_key)
        Joke = get_Dav_Joke()
        print("joke data:",Joke)
        await message.channel.send(Joke)

    if message.content.startswith('$jk/Norris'):
        Joke = get_Joke()
        await message.channel.send('Here is the joke: ')
        await message.channel.send(Joke)
    
    # Open the Data json file :
    with open("Data.json","r") as file :
        Data = json.load(file)

    msg = message.content
    if any(word in msg for word in Data["Word_List"]):
        Joke= get_Joke()
        await message.channel.send('here is a joke: '+ Joke )

    # Command To Update and Delet from user

    # Update the Data :
    if message.content.startswith('$joke/update'):
        jk_message = msg.split('$joke/update ',1)[1]
        Update_jk(jk_message)
        await message.channel.send("The new joke is added") 

    # Delete a content on Data:
    if message.content.startswith('$Joke/Delete'):
        index = int(msg.split('$Joke/delete',1)[1])
        Delet_jk(index)
        jk = Data["jk"]
        await message.channel.send(jk)

    if message.content.startswith("$Word_List"):
        Words_List=[]
        if "Word_List" in Data :
            Words_List = Data["Word_List"]
        await message.channel.send(Words_List)



BOT.run(DISCORD_TOKEN)   # Run Token