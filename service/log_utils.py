from string import Template


class LogUtils:
    def __init__(self, name_template):
        """ Обязательные поля в шаблоне:
                $name - имя
        """
        self.__name_template = name_template

    def gen_name(self, obj) -> str:
        """ Генерация имени логгера. Если передана строка - то используем ее, если объект - то используем имя класса.
        :param obj:
        :return:
        """
        t = Template(self.__name_template)
        if isinstance(obj, str):
            return t.substitute(name=obj)
        elif '__class__' in obj.__dict__ and '__name__' in obj.__class__.__dict__:
            return t.substitute(name=obj.__class__.__name__)
        else:
            return ''
