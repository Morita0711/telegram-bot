import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import pandas as pd
import os
from constants import API_KEY
# Create and configure logger
logging.basicConfig(filename="bot_logs.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
 
# Creating an object
logger = logging.getLogger()
 
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)



base_path=os.getcwd()
command_file_path=os.path.join(base_path,'commands.xlsx')

if(os.path.isfile(command_file_path)):
    commands={}
    command_list=[]
    df=pd.read_excel(command_file_path)
    for ind in df.index:
        command=df['command'][ind]
        response=df['response'][ind]
        commands[command]=response
        command_list.append(command)
else:
    print("Commands.xlsx file not found in "+base_path)
    print('exiting.....')
    exit()



def bothandle(update: Update, context: CallbackContext) -> None:
    """Send a message when the other command is issued."""
    #print(update)
    command=update.message['text'][1:]
    response=commands[command].replace('Binance.US','Binance US')
    update.message.reply_text(response)

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    coms=[]
    for com in command_list:
        coms.append('/'+com)
    text='list of commands\n'+'\n'.join(coms)
    update.message.reply_text(text)



def main() -> None:
    """Start the bot."""
    updater = Updater(API_KEY)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler(command_list, bothandle))
    dispatcher.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()


