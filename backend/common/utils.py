import os
import re
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


def custom_exception_handler(exc, context):
    if isinstance(exc, ValidationError):
        return Response({"error": exc.detail}, status=400)
    else:
        return exception_handler(exc, context)


def string_is_english_tag(string):
    additional = "1234567890_"
    english_alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return all(l in english_alphabet + additional for l in string) and not all(l in additional for l in string)


def replace_russian_chars_with_english(string, replacement_dict):
    string = string.lower()

    for ru_letter, en_letter in replacement_dict.items():
        string = string.replace(ru_letter, en_letter)
    return string


def s3_replace_russian_chars_with_english(string):
    s3_ru_to_en = {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'ё': 'e',
        'ж': 'zh',
        'з': 'z',
        'и': 'i',
        'й': 'y',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'f',
        'х': 'h',
        'ц': 'ts',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'sch',
        'ъ': '',
        'ы': 'y',
        'ь': '',
        'э': 'e',
        'ю': 'yu',
        'я': 'ya',
        ' ': '_'
    }
    return replace_russian_chars_with_english(string, s3_ru_to_en)


def parse_file_number_from_filename(filename):
    no_ext_filename = os.path.splitext(filename)[0]
    regex_result = re.search(r"(?P<number>\d+)$", no_ext_filename)
    if regex_result:
        return int(regex_result.group('number'))


def make_rest_standard_response_data(data):
    return {"count": len(data), "next": None, "previous": None, "results": data}
