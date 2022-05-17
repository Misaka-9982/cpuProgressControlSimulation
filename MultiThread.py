import threading
import Global_var
from Core import *

t_detectwaitingprocessqueue = threading.Thread(target=detectwaitingprocessqueue, args=())
t_cputiming = threading.Thread(target=cputiming, args=())
t_detectreadyprocessqueue = threading.Thread(target=detectreadyprocessqueue, args=())
