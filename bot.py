from telegram.ext import CommandHandler, MessageHandler, Filters, Updater,CallbackQueryHandler,MessageHandler,ConversationHandler
import telegram
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
import os,sys


TOKEN = "650923941:AAEWpsq6ZCDMcc_7wHTnyY4wUWDJPfcT3ag"
PORT = int(os.environ.get('PORT', '8443'))

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('QRReviews-fe5cd1a8da85.json',scope)

BUSINES = ''
PHONE = 0

user_data =[]
users = {}

def update_table(busines_title, phone_number):
	try:
		gc = gspread.authorize(credentials)
		sheet=gc.open('Павел Шуба бот').sheet1
		sheet.append_row([busines_title,phone_number])
	except:
		os.startfile(sys.argv[0])
		os.abort()

def busines(bot,update):
	text = update.message.text
	users[update.message.chat_id].append(text)
	update.effective_message.reply_text('Куда я могу вам отправить подарок на 50$ (напиши свой номер телефона)?')

	return PHONE

def phone(bot,update):
	text = update.message.text
	users[update.message.chat_id].append(text)

	update.effective_message.reply_text('Спасибо что ответили на вопросы 😉\nОт меня подарок 50$ на любую услугу из любой из моих компаний.')
	update_table(users[update.message.chat_id][0],users[update.message.chat_id][1])
	time.sleep(1) 
	bot.sendPhoto(chat_id=update.message.chat_id, photo=open('1.jpg', 'rb'))
	time.sleep(1) 
	bot.send_message(chat_id=update.message.chat_id,
				 text='Чем буду полезен'+'\nМои бизнесы 🔽🔽🔽' +'\n'+'⚡ Студия интернет-маркетинга (контекст, таргет, чат-боты, контент, smm, youtube-продвижение)\nТестовый набросок моего сайта shubamarketing.tilda.ws\n⚡ Изготовление и монтаж наружной рекламы www.instagram.com/jackfruit.ua\n⚡ Размещение рекламы на асфальте по всей Украине www.instagram.com/ground_branding\n⚡ Организация промо-акций по Украине\nwww.instagram.com/lap_studio/'
				 )
	time.sleep(2) 
	bot.send_message(chat_id=update.message.chat_id,
				 text='Немного обо мне:\n▶️ 27 лет\n▶️ 9 лет в рекламе\n▶️ Обучаю интернет-маркетингу участников бизнес-клубов\n▶️ Сам постоянно обучаюсь в разных дорогостоящих программах по интернет-маркетингу в том числе у Олеся\n▶️ Участник крутейшего сообщества Digital маркетологов "Дижитализатор"\nМой инстаграмм, подпишитесь🔽\nhttps://instagram.com/shuba_pavel\n⬆️⬆️⬆️')
	time.sleep(3) 
	bot.send_message(chat_id=update.message.chat_id,text='Если увидите меня - Дай пятюню и скажите "прикольный бот"')
	return ConversationHandler.END

def start(bot, update):
	users[update.message.chat_id] = []
	update.effective_message.reply_text('Чем занимаетесь? Какой у вас бизнес?')
	return BUSINES

def cancel(bot, update):
	update.effective_message.reply_text('Извини')
	return ConversationHandler.END

def main():
	ch = ConversationHandler([CommandHandler('start', start)], {
        BUSINES: [MessageHandler(Filters.text, busines)], 
        PHONE: [MessageHandler(Filters.text, phone)]}, 
         fallbacks=[CommandHandler('cancel', cancel)]
        )

	u = Updater(TOKEN)
	dp = u.dispatcher
	dp.add_handler(ch)
	
	u.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
	u.bot.set_webhook("https://pavel-bot-1.herokuapp.com/" + TOKEN)
	u.idle()

if __name__ == '__main__':
	main()