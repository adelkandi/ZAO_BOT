#Imports:
import discord
import os
from dotenv import load_dotenv
import requests  #  Make HTTPs requests to get DATA from API 
import json   
import openai 
import io 


#ZAO_BOT: 


load_dotenv()   # Load the .env file to hide the TOKEN
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")   
openai.api_key = os.getenv("API_Key")  # API_Key from OpenAI 

intents= discord.Intents.default()
intents.message_content = True
BOT = discord.Client(intents=intents)     # make the Bot connect with Discord 


# Helper function to get a Joke from the API 
def get_joke():
    response = requests.get("https://api.chucknorris.io/jokes/random")  
    json_data = json.loads(response.text) # Convert the response to json file to store data
    joke = json_data
    return(joke['value'])



def get_dav_joke():        #function to request text-davinci-003
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = "Give me a funny joke",
        max_tokens = 100,
        n = 1,
        stop = None,
        temperature = 0.4,
        )
    dav_joke = response.choices[0].text.strip()
    print("Joke data:",dav_joke)   # to see on terminal and debug 
    return dav_joke

# Function to get dad jokes from the API:
def get_dad_joke():
    response = requests.request("Get","https://icanhazdadjoke.com/slack")
    dad_joke = json.loads(response.content)['attachments'][0]['text']
    return dad_joke

# Function to generate dad joke image :
def get_dadimg_joke():
    response = requests.get("https://icanhazdadjoke.com/j/<joke_id>.png",headers={"Accept": "image/*"})
    image_data= response.content.decode('latin-1').encode('latin-1') # to fix the error  embedded null byte
    file2object = io.BytesIO(image_data)
    return discord.File(file2object , filename="dad_joke.png") 


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

def delet_jk(index):            # Delete a Local Joke from json data file 
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
        Joke = get_dav_joke()
        print("joke data:",Joke)
        await message.channel.send(Joke)

    # Chuck Norris jokes generator :
    if message.content.startswith('$jk/Norris'):
        Joke = get_joke()
        await message.channel.send('Here is the joke: ')
        await message.channel.send(Joke)
    
    # Open the Data json file :
    with open("Data.json","r") as file :
        Data = json.load(file)

    msg = message.content
    if any(word in msg for word in Data["Word_List"]):
        Joke= get_joke()
        await message.channel.send('here is a joke: '+ Joke )

    # Dad jokes text generator :
    if message.content.startswith("$jk/dad"):
        Joke = get_dad_joke()
        await message.channel.send(f"Here is the joke : {Joke}")

    # Dad jokes image generator :
    if message.content.startswith("$jk/img.dad"):
        Joke = get_dadimg_joke()
        await message.channel.send(file=Joke)

    # Command To Update and Delete from user

    # Update the Data :
    if message.content.startswith('$joke/update'):
        jk_message = msg.split('$joke/update ',1)[1]
        Update_jk(jk_message)
        await message.channel.send("The new joke is added") 

    # Delete a content on Data:
    if message.content.startswith('$Joke/Delete'):
        index = int(msg.split('$Joke/delete',1)[1])
        delet_jk(index)
        jk = Data["jk"]
        await message.channel.send(jk)

    if message.content.startswith("$Word_List"):
        Words_List=[]
        if "Word_List" in Data :
            Words_List = Data["Word_List"]
        await message.channel.send(Words_List)



BOT.run(DISCORD_TOKEN)   # Run Token