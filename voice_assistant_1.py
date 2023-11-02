import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import random
import webbrowser
import text_to_speech
import g4f


number_random1 = random.randint(0, 2)
number_random2 = random.randint(0, 3)
number_random3 = random.randint(0, 3)
number_random = random.randint(0, 15) 

lists = ['Рожденный ползать упасть не может',
'Быстро и дешево выполню любую халтуру!',
'Ты же командир! Не делай умное лицо!',
'Пусть меня воспитали люди, но я не глупец!',
'Хочешь устроить Конец Света? Нажми кнопку «Reset».',
'Я расскажу тебе множество тайн, а потом убью тебя!',
'Сгинь нечистая сила, останься чистый спирт!',
'Не гнев правит мной, а я гневом! Чего и вам желаю',
'Властители тьмы делают «это» в темноте.',
'Не оскверняй моё лицо своим курсором!',
'Да повелитель?',
'Да?',
'Чего желает мой повелитель?',
'ЭЭЭ?',
'А?',
'Че?']
lists_1 = ['Я так понял: ','Услышал: ','Распознано: ']
lists_2 = ['Я нихуя не понял','Что?','ты о чем?','не понял']
lists_3 = ['Неизвестная ошибка проверьте интернет','Неизвестная ошибка проверьте интернет','Неизвестная ошибка скинь денег','я устал']


opts = {
	"alias": ('неро','нероо','ннеерроо','ннеро','нерро','неероооо,','нэрра'
				'нерий','нера','нэрроа', 'nero', 'нейрон'),
	"tbr": ('скажи','расскажи','покажи','сколько','произнеси'),
	"cmds": {
		"ctime": ('текущее время','сейчас времени','который час','удыы бэна','удыыы болжэ бэна'),
		"radio": ('включи youtube','возпроизведи ютуб','открой youtube',),
		"joke": ('расскажи анекдот','рассмещи меня','скажи анектод','расскажи топ цитату','цитата')
			}
}


# def
def speak(what):
	print(what)
	tts = pyttsx3.init()
	rate = tts.getProperty('rate') #Скорость произношения
	tts.setProperty('rate', rate-40)

	volume = tts.getProperty('volume') #Громкость голоса
	tts.setProperty('volume', volume+0.9)

	voices = tts.getProperty('voices')

	# Задать голос по умолчанию
	tts.setProperty('voice', 'ru') 

	# Попробовать установить предпочтительный голос
	for voice in voices:
	    if voice.name == 'Irina':
	        tts.setProperty('voice', voice.id)

	tts.say(what)
	tts.runAndWait()


def callback(recognizer, audio):
	try:
		voice = recognizer.recognize_google(audio, language="ru-RU").lower()
		print( '[log]', lists_1[number_random1] + voice)
		gpt(voice)

		if voice.startswith(opts["alias"]):
			cmd = voice
			for x in opts["alias"]:
				cmd = cmd.replace(x, '').strip()

			for x in opts['tbr']:
				cmd = cmd.replace(x, '').strip()

			#Разпознаем
			cmd = recognize_cmd(cmd)
			execute_cmd(cmd['cmd'])


	except sr.UnknownValueError:
		print(lists_2[number_random2])
	except sr.RequestError as e:
		print(lists_3[number_random3])

def recognize_cmd(cmd):
	RC = {'cmd': '', 'percent': 0 }
	for c,v in opts['cmds'].items():

		for x in v:
			vrt = fuzz.ratio(cmd, x)
			if vrt > RC['percent']:
				RC['cmd'] = c
				RC['percent'] = vrt

	return RC

def execute_cmd(cmd):
	if cmd in 'ctime':
		# Показываю текущее время
		now = datetime.datetime.now()
		speak('Сейчас ' + str(now.hour)+ ':' + str(now.minute))

	elif cmd in 'radio':
		webbrowser.open('https://www.youtube.com')

	elif cmd in 'joke':
		speak('''Мужик молится:
				- Сам я несчастный, дети мои несчастные, народ мой несчастный!
				Бог ему:
				- Не ной!
				Мужик:
				- Правильно, я не Ной, я Моисей!''')
	else:
		print(lists_3[number_random3])


def gpt(voice):
	text = []
	text.append({"role":"user", "content":"твоя роль писателя ответы на русском языке не более 150 слов"})

	text.append({"role":"user", "content": voice})
	try:
	    chatgpt_response = g4f.ChatCompletion.create(model="gpt-3.5-turbo", provider=g4f.Provider.Bing, messages=text)
	    if not chatgpt_response:
	        raise Exception("manyrequestempty")
	    if chatgpt_response == "Unable to fetch the response, Please try again.":
	        raise Exception("manyrequest")
	    # Add the bot's response to the user's message history
	    text.append({"role":"assistant", "content": chatgpt_response})
	    speak(chatgpt_response)

	except Exception as ex:
		print(ex)
		if ex == "manyrequest":
			print('Слишком много запросов, подождите некоторое время и попробуйте снова. Либо установите ограничение текста')
		else:
			print(f'Непредвиденная ошибка, подождите некоторое время и попробуйте снова {ex}')


#start
r = sr.Recognizer()
m = sr.Microphone(device_index = 4)
print(m.device_index)

with m as source:
	r.adjust_for_ambient_noise(source)	


speak(lists[number_random])
speak('Я вас слушаю')


stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1)
