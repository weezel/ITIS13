# -*- coding: utf-8 -*-

__title__ = 'transliterate.contrib.languages.el.translit_language_pack'
__author__ = 'Artur Barseghyan'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('GreekLanguagePack',)

from transliterate.base import TranslitLanguagePack, registry

class GreekLanguagePack(TranslitLanguagePack):
    """
    Language pack for Greek language. See http://en.wikipedia.org/wiki/Greek_alphabet for details.
    """
    language_code = "el"
    language_name = "Greek"
    character_ranges = ((0x0370, 0x03FF), (0x1F00, 0x1FFF))
    mapping = (
        u"abgdezhiklmnxoprstyfwuABGDEZHIKLMNXOPRSTYFWU",
        u"αβγδεζηικλμνξοπρστυφωθΑΒΓΔΕΖΗΙΚΛΜΝΞΟΠΡΣΤΥΦΩΘ",
    )
    reversed_specific_mapping = (
        u"θΘ",
        u"uU"
    )
    pre_processor_mapping = {
        u"th": u"θ",
        u"ch": u"χ",
        u"ps": u"ψ",
        u"TH": u"Θ",
        u"CH": u"Χ",
        u"PS": u"Ψ",
    }
    detectable = True


registry.register(GreekLanguagePack)
