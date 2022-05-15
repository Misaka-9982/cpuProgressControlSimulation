import threading
import Global_var
from Function import *

t_detectwaitingprogressqueue = threading.Thread(target=detectwaitingprogressqueue, args=())
t_cpuselect = threading.Thread(target=cpuselect, args=())
