import pyttsx3

engine = pyttsx3.init()

# change voice

# getting details of current voice
voices = engine.getProperty('voices')      

for i in range(10,18):
    engine.setProperty('voice', voices[i].id)
    print(engine.getProperty("voice"))
    engine.setProperty('rate', 150)

    # say something

    engine.say("Pick me, pick me! My voice is number " + str(i))
    engine.setProperty('rate', 250)
    print(engine.getProperty("rate"))
    engine.say("faster rate, Pick me, pick me! My voice is number " + str(i))

    engine.runAndWait()
