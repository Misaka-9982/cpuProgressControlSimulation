import threading
import Global_var
from Function import *

t_detectwaitingprogressqueue = threading.Thread(target=detectwaitingprogressqueue, args=())
