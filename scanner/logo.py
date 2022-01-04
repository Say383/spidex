from colorama import Fore
import pyfiglet

name = pyfiglet.figlet_format("Pwndora", font="slant")
title = "{}{}{}".format(Fore.BLUE,name,Fore.RESET)

