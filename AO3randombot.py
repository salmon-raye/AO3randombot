# -*- coding: utf-8 -*-
# pip install python-telegram-bot==13.7
# pip install ao3-api
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import os
import AO3
import random


TOKEN = os.environ['TELE_BOT_TOKEN']  
SERVER = 'local' # local or heroku
PORT = int(os.environ.get('PORT', '8443'))
CRITERIA_ERROR_MESSAGE = "Please enter search criteria after '/set'.\n\nE.g. '/set warrior nun angst'\n\nThis will search all tags in AO3 fics based on your criteria."

"""
TO DO LIST:  

Set other criteria e.g. completed, word count, language, kudos
Sort by kudos, set threshold to search top 50% of fics? TOO COMPLICATED

CHANGELOG:
29/05/24: 
    - edited AO3 search.py line 101 remove comma
    - edited AO3 works.py line 830 get str(html), not just text
    - changed commands to /set and /show, changed text
    - added start function
    - removed ChatAction
    
21/06/24:
    - set it up to run in Azure VM with auto-restart:
    sudo nano /etc/systemd/system/ao3randombot.service
    sudo systemctl daemon-reload
    sudo systemctl start ao3randombot
    sudo systemctl enable ao3randombot
    sudo systemctl status ao3randombot

    *******
    [Unit]
    Description=AO3 Random Bot
    After=network.target
    
    [Service]
    User=azureuser
    WorkingDirectory=/home/azureuser/ao3/
    ExecStart=/home/azureuser/ao3/telegram/bin/python3 /home/azureuser/ao3/AO3randombot.py
    StandardOutput=file:/home/azureuser/ao3//ao3randombot.log
    StandardError=file:/home/azureuser/ao3/ao3randombot.log
    Restart=always
    
    [Install]
    WantedBy=multi-user.target
    *******

"""
def start(update, context):
    update.message.reply_text('Welcome!\n\nType "/set + your search tags" to set search criteria.\n\nE.g. "/set warrior nun angst"')


# Search for a random fic with this text    
def random_search(update, context):
    # Get person
    chat_id = update._effective_chat.id
    # Get search terms
    try:
        search_term = context.user_data['search_term']
        #context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        print('Searching for ', search_term)
    except:
        context.bot.send_message(chat_id=chat_id, text=CRITERIA_ERROR_MESSAGE)
        return 

    # Get total number of pages if there is new criteria
    if (context.user_data['new_criteria'] == 1): 
        search = AO3.Search(any_field=search_term)
        search.update()
        if (search.total_results != 0):
            context.user_data['new_criteria'] = 0
            print('No longer new criteria')
            context.user_data['total_results'] = search.total_results
            print('Total search results: ', context.user_data['total_results'])
        else:
            print('No search results for these search terms')
            context.bot.send_message(chat_id=chat_id, text='No results found. Try a different search?')
            return
    
    # Search a random page from total results/20 
    # If there are between 0 to 20 search results only
    results_count = context.user_data['total_results']
    if (context.user_data['total_results'] < 20):
        random_page = 1
        works_in_page = context.user_data['total_results'] - 1
    else:
        random_page = random.randint(1, context.user_data['total_results']//20)
        works_in_page = 19 # 19 instead of 20 because Python starts from 0
    print('Randomised page no.: ', random_page)
    search = AO3.Search(any_field=search_term, page=random_page)
    search.update()
    random_work = random.randint(0, works_in_page)
    print('Randomised work no.: ', random_work)
    fic = search.results[random_work]
    fic_url = fic.url
    # summary doesnt have HTML formatting idk why :(
    fic_summary = AO3.Work(fic.id).summary.replace('<blockquote class="userstuff">', '').replace('</blockquote>', '').replace('</p>', '').replace('<p>', '\n\n').replace('<br/>', '\n\n')
    print(fic_url)
    print(fic_summary)
    # Show random_search button
    keyboard = [
        [
            InlineKeyboardButton("Random fic", callback_data='1')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send a message containing the random fic to the person
    result_string = f"<i>Random fic from {results_count} results:</i>{fic_summary}\n\n{fic_url}"
    context.bot.send_message(chat_id=chat_id, text=result_string, reply_markup=reply_markup,parse_mode=ParseMode.HTML)

def random_button(update, context):
    # what does query do?!
    # query = update.callback_query
    # query.answer()
    random_search(update,context)
    return
    
def set_criteria(update, context):
    # Get person
    chat_id = update._effective_chat.id
    # Get search terms and save it in user_data
    try:
        search_term = update.message.text.split(" ",1)[1]
        context.user_data['search_term'] = search_term
        context.user_data['new_criteria'] = 1
        print('Set new criteria')
        print('Criteria set as: ', search_term)
        # Show random_search button
        keyboard = [
            [
                InlineKeyboardButton("Random fic", callback_data='1')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Send a message containing search terms to the person
        context.bot.send_message(chat_id=chat_id, text='Search criteria is set as: '+ search_term, reply_markup=reply_markup)
    except:
        # Person did not enter search terms correctly
        context.bot.send_message(chat_id=chat_id, text=CRITERIA_ERROR_MESSAGE)
        return 

def show_criteria(update, context):
    # Get person
    chat_id = update._effective_chat.id
    # Get search terms from user_data, if any
    try:
        search_term = context.user_data['search_term']
        # Show random_search button
        keyboard = [
            [
                InlineKeyboardButton("Random fic", callback_data='1')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Send a message containing search terms to the person
        context.bot.send_message(chat_id=chat_id, text='Search criteria is set as: '+ search_term, reply_markup=reply_markup)
    except:
        # No search terms saved yet
        context.bot.send_message(chat_id=chat_id, text=CRITERIA_ERROR_MESSAGE)
        return 

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Linking commands to functions
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('random', random_search))
    dp.add_handler(CommandHandler('set', set_criteria))
    dp.add_handler(CommandHandler('show', show_criteria))
    dp.add_handler(CallbackQueryHandler(random_button))
    
    # Start the Bot
    if (SERVER == 'local'):    
        updater.start_polling()
        print('Listening via polling')
        
    elif (SERVER == 'heroku'):
        """
        # Use webhook instead of polling when running on server!
        """
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN,
                              webhook_url="https://ao3randombot.herokuapp.com/" + TOKEN)
        print('Listening via webhook')
    else:
        print('You want to use local or heroku? Make up your mind')
        return

    updater.idle()
    
if __name__ == '__main__':
    print ("Running bot...")
    main()
    

