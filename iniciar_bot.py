# -*- coding: utf-8 -*-
import os
import telebot
import urllib
import json
import rodar

bot = telebot.TeleBot('TOKEN_TELEGRAM_API')
cpu,plmae,mem = rodar.main()

@bot.message_handler(commands=['start', 'help'])
def send_start_message(message):
    bot.reply_to(message, "Olá, eu sou o bot 'BuscaPreço'\n"
                          "minha lista de comandos é : \n"
                          "/ryzen7 /mem /plmae")


@bot.message_handler(commands=['ryzen7'])
def send_people(message):
    bot.reply_to(message, cpu_msg())

@bot.message_handler(commands=['mem'])
def send_people(message):
    bot.reply_to(message, mem_msg())
    
@bot.message_handler(commands=['plmae'])
def send_people(message):
    bot.reply_to(message, plmae_msg())
    
    
def cpu_msg():
    message = 'O {} está R${} na loja {}'.format(cpu[0],cpu[1],cpu[2])
    return message

def mem_msg():
    message = ' A Memoria {} está R${} na loja{}'.format(mem[0],mem[1],mem[2])
    return message

def plmae_msg():
    message = ' A Placa Mãe {} está R${} na loja{}'.format(plmae[0],plmae[1],plmae[2])
    return message

bot.polling()