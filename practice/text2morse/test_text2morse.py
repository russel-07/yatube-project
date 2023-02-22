#  протестируйте работу text2morse()
from unittest import TestCase

from text2morse import text2morse

class TestMorse(TestCase):
    def test_str(self):
        # Проверьте правильность перевода в морзянку строк 'Hello' и 'Привет'
        self.assertEqual(text2morse('Hello', 'en'), '.... . .-.. .-.. ---', msg="Перевод выполнен неверно")
        self.assertEqual(text2morse('Привет!'), '.--. .-. .. .-- . - --..--', msg="Перевод выполнен неверно")

    def test_wrong_lang(self):
        # Проверьте,  порождаются ли исключения, если в аргументе неправильно указан язык для строки
        with self.assertRaises(ValueError, msg="Исключение не возникло"):
            text2morse('Hello', 'fr')
            text2morse('Hello!', 'en')

    def test_instance(self):
        # Проверьте типы возвращаемых значений
        self.assertIsInstance(text2morse('Привет'), str, msg="Возвращаемое значение не соответствут типу 'str'")