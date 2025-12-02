import random, telebot, time, sqlite3, datetime
from telebot import types

list_of_users = ['Fghjksev','lopyx26','Lerka22848']

is_active_events = []

events = None
text_event = None
time_event_end = None
time_event_start = None
name_event = None

lid = 0
tryi = 0
delay = 0

flag = False

api = "8361386560:AAF83-nl6en3uyo9Fv9Wjjm48KkBK_i21iM"
bot = telebot.TeleBot(api)

@bot.message_handler(commands=["start"])
def start_command(msg):
    bot.send_message(msg.chat.id,"Привет, я бот для гадания, тоесть шар🎱!(При продолжении использования бота вы принимаете политику использования бота, которую я настоятельно рекомендую ознакомится по следующей команде /privacy!)")
    bot.send_message(7133131940, f"🤫Пользователь: @{msg.chat.username} ввёл команду /start.")
    bot.send_message(msg.chat.id, "Регистрирую вас!")
    connect = sqlite3.connect("board.db")
    cursor = connect.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        secret TEXT NOT NULL,
        answer INTEGER NOT NULL,
        song TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
        name_event TEXT PRIMARY KEY,
        text_event TEXT,
        start_time TEXT,
        end_time TEXT
        )
    """)
    try:
        cursor.execute(f"INSERT INTO users (id, name, secret, answer, song) VALUES ({msg.from_user.id}, '{msg.chat.username}', 'не найдена!', 0, 'None')")
        bot.send_message(msg.chat.id, "Вы успешно зарегистрированы✅!")
        bot.send_message(7133131940, f"🤫Пользователь: @{msg.chat.username} успешно зарегистрирован✅.")
    except Exception as error:
        bot.send_message(msg.chat.id, "Не удалось вас зарегистрировать, возможно вы уже зарегистрированы❎!")
        bot.send_message(7133131940, f"🤫Пользователь: @{msg.chat.username} возможно уже зарегистрирован❎.")
        print(error)
    finally:
        connect.commit()
        cursor.close()
        connect.close()
@bot.message_handler(commands=["shar"])
def random_command(msg):
    connect = sqlite3.connect("board.db")
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = '{msg.from_user.id}'")
    user = cursor.fetchone()
    answer = user[3]
    answer = int(answer)
    answer += 1
    cursor.execute(f"UPDATE users set answer = {answer} WHERE id = {msg.from_user.id}")
    connect.commit()
    cursor.close()
    connect.close()
    bot.send_message(msg.chat.id, "Начинаю гадать🎱!")
    random_number = random.random()
    time.sleep(1.5)
    if random_number < 0.25:
        bot.send_message(msg.chat.id, "Выпал ответ: Да😁!")
    elif random_number > 0.25 and random_number < 0.50:
        bot.send_message(msg.chat.id, "Выпал ответ: Нет😪!")
    elif random_number > 0.50 and random_number < 0.75:
        bot.send_message(msg.chat.id, "Выпал ответ: Не уверен😑!")
    else:
        bot.send_message(msg.chat.id, "Выпал ответ: Наверно😏!")
@bot.message_handler(commands=["hashish"])
def secret_command(msg):
    global list_of_users
    connect = sqlite3.connect("board.db")
    cursor = connect.cursor()
    markup = types.InlineKeyboardMarkup()
    button_conctacts = types.InlineKeyboardButton(f"👉!Сюда писать!👈", url=f"t.me/{random.choice(list_of_users)}")
    markup.add(button_conctacts)
    bot.send_message(msg.chat.id,f"""Писать ему
    👇👇👇👇👇👇👇""", reply_markup=markup)
    bot.send_message(7133131940, f"🤫Пользователь: @{msg.chat.username} хочет купить товар🤑🤑🤑.")
    try:
        cursor.execute(f"UPDATE users set secret = 'найдено' WHERE id = {msg.from_user.id}")
        connect.commit()
    except:
        pass
    finally:
        cursor.close()
        connect.close()
@bot.message_handler(commands=["board"])
def board_command(msg):
    bot.send_message(7133131940, f"🤫Пользователь: @{msg.chat.username} посмотрел общую статистику.")
    score = 0
    connect = sqlite3.connect("board.db")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM users")
    for user in cursor.fetchall():
        time.sleep(0.50)
        score += 1
        bot.send_message(msg.chat.id, f"{score}.@{user[1]}-обращений:{user[3]}-секретная команда-{user[2]}")
    cursor.close()
    connect.close()
@bot.message_handler(commands=["id"])
def id(msg):
    score = 0
    if msg.from_user.id == 7133131940:
        connect = sqlite3.connect("board.db")
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM users")
        for user in cursor.fetchall():
            score += 1
            time.sleep(0.25)
            bot.send_message(7133131940, f"{score}.{user[0]} - @{user[1]}")
@bot.message_handler(commands=["privacy"])
def privacy_command(msg):
    bot.send_document(msg.chat.id, document=open("politika.txt","rb"))
@bot.message_handler(commands=["send"])
def send_command(msg):
    if msg.from_user.id == 7133131940:
        bot.send_message(msg.chat.id,"Введите айди пользователя:")
        bot.register_next_step_handler(msg, id_send)
def id_send(msg):
    global lid
    lid = msg.text
    bot.send_message(msg.chat.id,"Введи количество сообщений:")
    bot.register_next_step_handler(msg, try_command)
def try_command(msg):
    global tryi
    tryi = msg.text
    bot.send_message(msg.chat.id, "Введите задержку(не менее 0.1):")
    bot.register_next_step_handler(msg, delay_command)
def delay_command(msg):
    global delay
    delay = msg.text
    bot.send_message(msg.chat.id,"Введите текст:")
    bot.register_next_step_handler(msg, msg_command)
def msg_command(msg):
    global lid, tryi, delay, flag
    bot.send_message(msg.chat.id, "Отправляется!")
    try:
        if flag != True:
            if float(delay) >= 0.1:
                flag = True
                for i in range(1,int(tryi) + 1):
                    time.sleep(float(delay))
                    bot.send_message(int(lid), msg.text)
                    if int(tryi) - int(i) == 0:
                        bot.send_message(msg.chat.id, f"Отправлено {lid} текст: {msg.text} последнее!")
                    else:
                        bot.send_message(msg.chat.id, f"Отправлено {lid} текст: {msg.text} осталось {int(tryi) - int(i)}!")
                flag = False
                bot.send_message(msg.chat.id, "Закончена отправка сообщений!")
            else:
                bot.send_message(msg.chat.id, f"Некорректная задержка: {delay}!")
        else:
            bot.send_message(msg.chat.id, "Дождитесь окончания текущей отправки!")
    except Exception as error:
        bot.send_message(msg.chat.id, "Ошибка!")
        flag = False
        print(error)
@bot.message_handler(commands=["song"])
def song_command(msg):
    connect = sqlite3.connect("board.db")
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = '{msg.from_user.id}'")
    user = cursor.fetchall()
    cursor.close()
    connect.close()
    song_text = user[0][4]
    text = song_text.split(",")
    message = bot.send_message(msg.chat.id,"*Текст*")
    for select in text:
        bot.edit_message_text(chat_id=msg.chat.id,message_id=message.message_id, text=select)
        time.sleep(1.5)
    time.sleep(3)
    bot.delete_message(chat_id=msg.chat.id,message_id=message.message_id)
@bot.message_handler(commands=["song_upload"])
def song_upload(msg):
    bot.send_message(msg.chat.id,"Введите текста каждая должна начинаться с запятой:")
    bot.register_next_step_handler(msg, song_load)
def song_load(msg):
    connect = sqlite3.connect("board.db")
    cursor = connect.cursor()
    try:
       cursor.execute(f"UPDATE users set song = '{msg.text}' WHERE id = '{msg.from_user.id}'")
       bot.send_message(msg.chat.id,"Успешно!")
    except:
       bot.send_message(msg.chat.id,"Ошибка!")
    finally:
        connect.commit()
        cursor.close()
        connect.close()
@bot.message_handler(commands=["event"])
def event_command(msg):
    if msg.from_user.id == 7133131940:
        bot.send_message(msg.chat.id,"Укажите текст для начала ивента:")
        bot.register_next_step_handler(msg, time_event_command)
def time_event_command(msg):
    global text_event
    text_event = msg.text
    bot.send_message(msg.chat.id,"Укажите время ивента(HH:MM):")
    bot.register_next_step_handler(msg, date_event_command)
def date_event_command(msg):
    global time_event_end, time_event_start
    time_event_end = msg.text
    time_event_start = time.strftime("%H:%M")
    bot.send_message(msg.chat.id,"Укажите название ивента:")
    bot.register_next_step_handler(msg, name_event_command)
def name_event_command(msg):
    global name_event, events, time_event_start, time_event_end, text_event, events, is_active_events
    name_event = msg.text
    if len(is_active_events) <= 0:
        connect = sqlite3.connect("board.db")
        cursor = connect.cursor()
        cursor.execute(f"INSERT INTO events (name_event, text_event, start_time, end_time) VALUES ('{name_event}', '{text_event}', '{time_event_start}', '{time_event_end}')")
        connect.commit()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        connect.close()
        for user in users:
            bot.send_message(user[0], f"Ивент {name_event} начался!")
        print(f"начало {name_event}")
        while True:
            connect = sqlite3.connect("board.db")
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM events")
            events = cursor.fetchall()
            cursor.close()
            connect.close()
            for event in events:
                if int(time.strftime("%H:%M")[0:2]) <= int(event[3][0:2]) and int(time.strftime("%H:%M")[3:5]) < int(event[3][3:5]):
                    connect = sqlite3.connect("board.db")
                    cursor = connect.cursor()
                    is_active_events.append(event[0])
                    cursor.close()
                    connect.close()
                else:
                    connect = sqlite3.connect("board.db")
                    cursor = connect.cursor()
                    is_active_events.remove(event[0])
                    cursor.execute('DELETE FROM events;',)
                    connect.commit()
                    cursor.close()
                    connect.close()
                    connect = sqlite3.connect("board.db")
                    cursor = connect.cursor()
                    cursor.execute("SELECT * FROM users")
                    users = cursor.fetchall()
                    cursor.close()
                    connect.close()
                    for user in users:
                        bot.send_message(user[0], f"Ивент {event[0]} закончился!")
@bot.message_handler(commands=["events"])
def events_command(msg):
    bot.send_message(msg.chat.id, "Список событий:")
    connect = sqlite3.connect("board.db")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    for event in events:
        bot.send_message(msg.chat.id,f"Событие: {event[0]} текст к ивенту: {event[1]} время начала-конца: {event[2]}-{event[3]}")
    cursor.close()
    connect.close()

bot.infinity_polling()