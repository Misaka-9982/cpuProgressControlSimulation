import threading
import Global_var
from Core import *

t_detectwaitingprogressqueue = threading.Thread(target=detectwaitingprogressqueue, args=())
t_cpuselect = threading.Thread(target=cputiming, args=())
