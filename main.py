from assistant import BRI

ai = BRI()
ai.speak("Welcome Jojo")

while True:
    command = ai.listen()
    print(command)
    if not ai.is_wake_up_command(command):
        continue

    ai.speak("Yes sir?")
    ai.parse_command(ai.listen())

