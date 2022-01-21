import eel

eel.init("templates/kurs")
eel.start("index.html")

@eel.expose
def call_in_js(x):
    print(x)





