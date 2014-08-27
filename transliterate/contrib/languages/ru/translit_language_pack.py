# -*- coding: utf-8 -*-

__title__ = 'transliterate.contrib.languages.ru.translit_language_pack'
__author__ = 'Artur Barseghyan'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('RussianLanguagePack',)

from transliterate.base import TranslitLanguagePack, registry

class RussianLanguagePack(TranslitLanguagePack):
    """
    Language pack for Russian language. See http://en.wikipedia.org/wiki/Russian_alphabet for details.
    """
    language_code = "ru"
    language_name = "Russian"
    character_ranges = ((0x0400, 0x04FF), (0x0500, 0x052F))
    mapping = (
        u"abvgdezijklmnoprstuf'y'ABVGDEZIJKLMNOPRSTUF'Y'",
        u"абвгдезийклмнопрстуфъыьАБВГДЕЗИЙКЛМНОПРСТУФЪЫЬ",
    )
    reversed_specific_mapping = (
        u"ёэЁЭъьЪЬ",
        u"eeEE''''"
    )
    pre_processor_mapping = {
    	u"kh": u"х",
        u"zh": u"ж",
        u"ts": u"ц",
        u"ch": u"ч",
        u"sh": u"ш",
        u"shch": u"щ",
        u"iu": u"ю",
        u"ia": u"я",
        u"Kh": u"Х",
        u"Zh": u"Ж",
        u"Ts": u"Ц",
        u"Ch": u"Ч",
        u"Shch": u"Щ",
        u"Iu": u"Ю",
        u"Ia": u"Я"
    }
    detectable = True


registry.register(RussianLanguagePack)
