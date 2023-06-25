from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv() 

@dataclass
class settings:
    CREDENTIALS: str
    #Variable: str -- se puede añadir más variables

CREDENTIALS = os.getenv("CREDENTIALS_GOOGLE_SHEETS")
#primero obtienes su valor

settings(CREDENTIALS=CREDENTIALS) #Aqui agregas la variable