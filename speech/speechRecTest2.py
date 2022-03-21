import speech_recognition as sr

listening = True

# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(
#         'Microphone with name "{1}" found for `Microphone(device_index={0})`'.format(
#             index, name
#         )
#     )

while listening:
    with sr.Microphone() as source:
        print(source)
        r = sr.Recognizer()
        r.adjust_for_ambient_noise(source)
        r.dyanmic_energythreshhold = 3000

        try:
            print("listening")
            audio = r.listen(source)
            print("Got audio")
            word = r.recognize_google(audio)
            print(word)
        except sr.UnknownValueError:
            print("Don't knoe that werd")

# mic = sr.Microphone()

# with mic as source:
#     au = r.listen(source)

# print("here")
# word = r.recognize_google(au)
# print ("here", word)
