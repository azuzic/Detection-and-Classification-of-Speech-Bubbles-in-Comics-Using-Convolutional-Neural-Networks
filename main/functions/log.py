from PyQt5.QtWidgets import QApplication

console_log_gui = None
logs = ''
counter = 1

def color(color, text):
    return (f"<font color='{color}'>{text}</font>")

def bold(text):
    return (f"<b>{text}</b>")

def initialiseLog(gui):
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
    
    if console_log_gui.log:
        console_log_gui.log.setText(logs)
        console_log_gui.log_scroll_area.verticalScrollBar().setValue(console_log_gui.log_scroll_area.verticalScrollBar().maximum())
        QApplication.processEvents()

def error(text,e):
    log(f'', True)
    log(f'❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ', True)
    log(f'{bold(color("#ff0000",f"💥 An error in [{text}] occurred:"))} {str(e)}', True)
    log(f'❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ', True)
    log(f'', True)
    print(f"An error occurred: {str(e)}")