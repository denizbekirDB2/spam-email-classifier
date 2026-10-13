import csv
import re
import string

with open("emails.csv", "r") as f:
    reader = csv.reader(f, delimiter="\t")
    for i, line in enumerate(reader):

        # get label from line
        label = line[0][-1:]
        print(label)

        line = line[0][:-1].lower()

        # sub urls for URL
        LABEL = r"[a-z0-9_-]+"
        DOT   = r"\s*\.\s*"
        HOST  = rf"(?:{DOT})*{LABEL}(?:{DOT}+{LABEL})+"
        SEG   = r"[^\s/]+"

        pattern = re.compile(
            rf"https? *: */ */\s*{HOST}"                     
            rf"(?:\s*/\s*{SEG})*"                            
            rf"(?:\s*/)?",                                  
            re.I,
        )
        
        line = re.sub(pattern, "URL ", line)

        # sub e-mails for EMail

        LOCAL = r"[a-z0-9_%+-]+(?:\s*\.\s*[a-z0-9_%+-]+)*"
        LABEL = r"[a-z0-9-]+"
        DOMAIN = rf"{LABEL}(?:\s*\.\s*{LABEL})+"             

        pattern = re.compile(rf"\b{LOCAL}\s*@\s*{DOMAIN}", re.I)

        line = re.sub(pattern, "EMAIL ", line)

        # sub currencys for CURRENCY

        line = re.sub(r"[\$\€\£\¥]+ *([0-9]+ ?[0-9]?)+", "CURRENCY ", line)

        # sub numbers for NUMBER

        line = re.sub(r"([0-9]+ *[0-9]?)+", "NUMBER ", line)

        # strip punctuation
        translator = str.maketrans('', '', string.punctuation)

        line = line.translate(translator)

        print(line)