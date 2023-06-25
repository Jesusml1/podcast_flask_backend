from dotenv import load_dotenv
import os
import json
from dataclasses import dataclass

load_dotenv() 

@dataclass
class settings:
    CREDENTIALS: any
    #Variable: str -- se puede añadir más variables

credentials_str = os.getenv("CREDENTIALS_GOOGLE_SHEETS")
CREDENTIALS = json.loads(credentials_str)

settings(CREDENTIALS=CREDENTIALS) #Aqui agregas la variable