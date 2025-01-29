from enum import Enum

class WordCorrections(Enum):
    TASK = ["tsk", "taks", "taask"]
    COMPLETE = ["complte", "complet", "cmplete"]
    DELETE = ["dlete", "delet", "dlte"]
    WEATHER = ["wether", "weaher", "waether", "wwheather", "wheather", "wheater"]
    WAY = ["wy", "way", "wai"]
    ROUTE = ["rout", "rute", "roue"]
    NAVIGATE = ["navgate", "navgate", "navgate"]
    DIRECTIONS = ["direction", "directons", "dirctions"]
    FORECAST = ["forcast", "forecst", "frecast"]
    CALENDAR = ["calender", "calndar", "clendar"]
    ADD = ["ad", "dd", "aad"]
    REMINDER = ["remindr", "remind", "remnder"]
    NOTE = ["not", "nte", "noe"]
    LIST = ["lst", "lis", "liss"]
    SEARCH = ["serch", "seach", "serach"]
    HELP = ["halp", "hep", "hlp"]
    POZNAN = ["poznan", "pozn", "pozna"]
    SZCZECIN = ["szczecin", "szczec", "szczecn"]
    WROCLAW = ["wroclaw", "wroclw", "wroclv"]
    GDANSK = ["gdansk", "gdans", "gdnsk"]
    KRAKOW = ["krakow", "krkow", "krkow"]
    TODAY = ["tody", "tdy", "td"]
    TOMORROW = ["tomorow", "tomorrow", "tomorow"]
    CURRENT = ["curent", "curernt", "curent"]
    NEXT = ["next", "nxt", "net"]
    INSIDE = ["insde", "insid", "insid"]
    OUTSIDE = ["outsde", "outsid", "outsid"]
    HOME = ["home", "hme", "hom"]
    SCHOOL = ["school", "schol", "scool"]
    OTHER = ["other", "othr", "othr"]
    ALL = ["all", "al", "ll"]

def correct_word(input_word):
    for correct, mistypes in WordCorrections.__members__.items():
        if input_word.lower() in mistypes.value:
            return correct.lower()
    return input_word.lower()

# Example usage
# input_word = "calender"
# corrected_word = correct_word(input_word)
# print(corrected_word)  # Output: "calendar"