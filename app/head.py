import random

from app.mouth import MouthHTTP
from app import config


class Head:
    """
    Голова Бендера
    """

    def __init__(self, bot):
        self.__mouth = MouthHTTP()
        self.__bot = bot

    async def answer(self, event):
        """
        :param event:       Сообщение
        """
        # is_channel - пропускаем (??)
        # is_private - отвечаем всегда
        # is_group - отвечаем всегда на обращение к себе, иногда вмешиваемся в чужие разговоры
        # message.from_id.user_id - от кого
        # message.sender_id - от кого
        # message.sender.first_name - от кого
        # message.message - сообщение  (raw_text, text)
        # message.to_id
        # self.bot.name , self.bot_id
        # ответ:
        #   message.reply_to (constructor_id, subclass_of_id, reply_to_msg_id)
        #   message.replay_to_msg_id

        # Ветки:
        #   Личное сообщение - отвечаем всегда. Обычное сообщение.
        #   Адресованное боту - отвечаем всегда. Сообщение-ответ.
        #   Не касается бота - отвечаем, с вероятностью 10% (ODDS_OF_CUT_IN). Сообщение-ответ
        reply = ""
        reply_to = 0

        # Сообщение в личку
        if event.is_private:
            reply = await self.__mouth.answer(event.message.text)
        # С упоминанием бота
        elif event.message.mentioned or event.message.text.find(self.__bot.name) >= 0:
            msg = await self.__mouth.answer(event.message.text)
            reply = f"{msg}"
            reply_to = event.message.id
        # Не касается бота
        elif random.random() <= config.ODDS_OF_CUT_IN:                                      # nosec
            msg = await self.__mouth.answer(event.message.text)
            reply = f"{msg}"
            reply_to = event.message.id

        if reply:
            await self.__bot.send_message(event.chat_id, message=reply, reply_to=reply_to)
