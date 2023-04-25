from colorama import Fore, Style, Back


class Parser:
    def __init__(self) -> None:
       return 
    
    def parse(self, message) -> str:
        ret_message = ""
        username = ""
        text =""
        color = ""
        red = None
        green = None
        blue = None
        sub = ""
        mod = ""
        
        if "reply-parent-msg-id=" in message:
            username = "REPLY MESSAGE\n"
            return username
        if "subscriber=1" in message:
                sub = Style.BRIGHT + Fore.LIGHTWHITE_EX + Back.MAGENTA +  "★ " + Fore.RESET + Style.RESET_ALL
        if "mod=1" in message:
            mod = Style.BRIGHT + Fore.LIGHTWHITE_EX + Back.GREEN +  "⚔ " + Fore.RESET + Style.RESET_ALL
            
        try:
            tags = message.split(";")
            text = message.split(":")
        except:
            pass
        for tag in tags:
            if "color=" in tag:
                color = tag.split("=")[1]
                red = int(color[1:3], 16)
                green = int(color[3:5], 16)
                blue = int(color[5:7], 16)

                color = f"\033[38;2;{red};{green};{blue}m"

            

            if "display-name=" in tag:
                username =  mod+sub+color + tag.split("=")[1]+ Fore.RESET + ": " + Fore.LIGHTWHITE_EX + text[-1] + Fore.RESET



        return username
