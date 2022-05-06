import re


def isurl(self):
    for lettre in self:
        if re.search("[A-Za-z0-9]", lettre) is None:
            return False
    return True


def format_texte(self):
    if re.search("[%\\\[\]\{\}|”~\#<>]+", self) is None:
        return True
    return False


def format_nom(self):
    if re.search("[%\\\[\]\{\}|”~\#<>0-9]+", self) is None:
        return True
    return False
