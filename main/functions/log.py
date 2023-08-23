from PyQt5.QtWidgets import QApplication

console_log_gui = None
logs = ''
counter = 1

def color(color, text):
    return (f"<font color='{color}'>{text}</font>")

def bold(text):
    return (f"<b>{text}</b>")

def initialise_log(gui):
    global console_log_gui
    console_log_gui = gui
    log("⚙️ Console Log GUI initialized !", True)
    
def log(text, br):
    global logs, counter, console_log_gui
    if (br and counter > 1):
        logs += "<br/>"
    if (br):
        logs += f"{bold(color('#a13047',f'[{counter}] '))}"
        counter+=1
    logs += f'{text}'
    
    if console_log_gui:
        console_log_gui.setText(logs)
        QApplication.processEvents()