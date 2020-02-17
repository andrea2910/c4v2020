import telebot
import time
from google.cloud import bigquery
import os
from config import CONFIG_JSON, BOT_TOKEN
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def bot():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CONFIG_JSON
    bot = telebot.TeleBot(token = BOT_TOKEN)
    @bot.message_handler(commands = ['empieza'])
    def send_welcome(message):
        bot.reply_to(message, 'Bienvenido!')
    @bot.message_handler(commands = ['ayuda'])
    def send_help(message):
        bot.reply_to(message, 'Para usar este canal, escribe el estado en el que se encuentra')
    list_states = ['Amazonas',
    'Anzoátegui',
    'Apure',
    'Aragua',
    'Barinas',
    'Bolívar',
    'Carabobo',
    'Cojedes',
    'Delta Amacuro',
    'Dtto Capital',
    'Falcón',
    'Guárico',
    'Lara',
    'Mérida',
    'Miranda',
    'Monagas',
    'Nueva Esparta',
    'Portuguesa',
    'Sucre',
    'Táchira',
    'Trujillo',
    'Vargas',
    'Yaracuy',
    'Zulia']
    @bot.message_handler(func = lambda msg: msg.text is not None and msg.text.title() in list_states)
    def location(message):
        #print(message)
        location = message.text
        client = bigquery.Client()
        sql =  """
        DECLARE max_date DATE;
        SET max_date = (
        SELECT MAX(insert_date) FROM `hulthack.dashboard_v1`);
        SELECT *
        FROM `hulthack.dashboard_v1`
        WHERE insert_date = max_date and federal_entity = '{}'
        """.format(location)
        df = client.query(sql).to_dataframe()
        df = df.replace(to_replace='-1.0', value='Mal', regex=True)
        df = df.replace(to_replace='1.0', value='Bien', regex=True)
        df = df.replace(to_replace='0.0', value='Intermedio', regex=True)
        df = df.replace(to_replace='-1', value='Mal', regex=True)
        df = df.replace(to_replace='1', value='Bien', regex=True)
        df = df.replace(to_replace='0', value='Intermedio', regex=True)
        output = list()
        for row in df.values:
            tmp = """{1}
            Electricidad:\t{3}
            Agua:\t{4}
            Seguridad:\t{5}
            Cirugía:\t{6}
            Emergencia:\t{7}
            Maternidad:\t{10}
            Asma:\t{13}
            Insulina:\t{14}
            """.format(*row)
            output.append(tmp)
        bot.reply_to(message, '\n\n'.join(output))
    bot.polling()

if __name__ == '__main__':
    bot()
