#This file is just to test codes NOT A PART OF MAIN CODE


#user starts the bot
@bot.on_message(filters.command(commands=['start']) & filters.private)
def Intro(Client,message):
    p = open("DataEng.py" , "a") # this is file where we gonno save dicitonary of user
    b = str(get.chat_id) #i cant get it , code glt hai help
    c = f"Chimku+{b}"
    p.write(f"dic{c} = []\n\n") #as dictonary cannot start with a number , so creating a dictinary in format chimku{user.id}
    p.close()

    message.reply_text(text="Hi")