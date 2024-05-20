import telebot
from telebot import types
from g4f.client import Client
from g4f.Provider import OpenaiChat,Bing,Liaobots,BaseProvider



bot = telebot.TeleBot('7179085561:AAFhk5k82S_ZdiRNZZLvN8tNy1MYmSMn0yw')

# Функция для получения факта или цитаты по теме
def get_gpt_response(prompt: str) -> str:
    try:
        client=Client()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.to_json()['choices'][0]['message']['content']

    except Exception as e:
        return f"Произошла ошибка: {e}"

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    fact_button = types.KeyboardButton("Факт")
    quote_button = types.KeyboardButton("Цитата")
    markup.add(fact_button, quote_button)
    bot.send_message(message.chat.id, "Выберите, что вы хотите получить:", reply_markup=markup)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: message.text in ["Факт", "Цитата"])
def handle_choice(message):
    if message.text == "Факт":
        bot.send_message(message.chat.id, "Укажите тему факта:")
        bot.register_next_step_handler(message, get_fact)
    elif message.text == "Цитата":
        bot.send_message(message.chat.id, "Укажите тему цитаты:")
        bot.register_next_step_handler(message, get_quote)

# Получение факта
def get_fact(message):
    topic = message.text
    bot.send_message(message.chat.id, "Подождите, ищу факт по теме...")
    fact = get_gpt_response(f'Ответь на русском языке.Если не можешь ответить на русском, то переведи на русский язык.    Интересный факт на тему {topic}')
    bot.send_message(message.chat.id, fact)

# Получение цитаты
def get_quote(message):
    topic = message.text
    bot.send_message(message.chat.id, "Подождите, ищу цитату по теме...")
    quote = get_gpt_response(f'Ответь на русском языке.Если не можешь ответить на русском, то переведи на русский язык. Мудрая цитата на тему {topic}')
    bot.send_message(message.chat.id, quote)

# Запуск бота
bot.polling(none_stop=True,interval=0)

#if __name__ == "__main__":
 #   get_fact("Кино")
