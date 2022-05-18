import threading
import Global_var
from Core import *
from Memory import *

t_detectwaitingprocessqueue = threading.Thread(target=detectwaitingprocessqueue, args=(), daemon=True)
t_cputiming = threading.Thread(target=cputiming, args=(), daemon=True)
t_detectreadyprocessqueue = threading.Thread(target=detectreadyprocessqueue, args=(), daemon=True)

