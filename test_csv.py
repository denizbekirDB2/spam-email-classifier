import csv
import re

with open("emails.csv", "r") as f:
    reader = csv.reader(f, delimiter="\t")
    for i, line in enumerate(reader):
        # if not (line[0][-1:] == "1" or line[0][-1:] == "0"):
    
        s = line[0].lower()
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
        print("URLs:", re.findall(pattern, s))
        
