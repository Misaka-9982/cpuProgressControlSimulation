import threading
import Global_var
from Core import *

t_detectwaitingprogressqueue = threading.Thread(target=detectwaitingprogressqueue, args=())
t_cputiming = threading.Thread(target=cputiming, args=())
t_detectreadyprogressqueue = threading.Thread(target=detectreadyprogressqueue, args=())
