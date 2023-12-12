import tkinter as tk
from tkinter import scrolledtext
import openai
import speech_recognition as sr
import pyttsx3
import pywhatkit

# Configure a valid API key
openai.api_key = "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"

class VoiceAssistantApp:
    def __init__(self, master):
        self.master = master
        master.title("Voice Assistant")

        self.text_output = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=40, height=10)
        self.text_output.pack(padx=10, pady=10)

        self.btn_listen = tk.Button(master, text="Ecouter", command=self.listen_command)
        self.btn_listen.pack(pady=10)

        self.btn_exit = tk.Button(master, text="Quitter", command=master.destroy)
        self.btn_exit.pack(pady=10)

        # Initialize the recognizer
        self.recognizer = sr.Recognizer()

        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()

    def listen_command(self):
        # Listen for the voice command
        with sr.Microphone() as source:
            print("Ecoute...")
            self.text_output.insert(tk.END, "Ecoute...\n")
            self.text_output.update_idletasks()
            audio = self.recognizer.listen(source)

        # Transcribe the voice command
        try:
            prompt = self.recognizer.recognize_google(audio, language="fr-FR")
            print("Tu as dit: " + prompt)
            self.text_output.insert(tk.END, "Tu as dit: " + prompt + "\n")
            self.text_output.update_idletasks()

            if prompt.lower() == "exit":
                self.master.destroy()
            elif 'mets la chanson' in prompt.lower():
                chanson = prompt.replace('mets la chanson', '')
                print(chanson)
                pywhatkit.playonyt(chanson)
            else:
                # Send a request to the GPT API
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt,
                    max_tokens=2048,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )

                # Display the response
                print(response["choices"][0]["text"])
                self.text_output.insert(tk.END, response["choices"][0]["text"] + "\n")
                self.text_output.update_idletasks()
                self.engine.say(response["choices"][0]["text"])
                self.engine.runAndWait()

        except sr.UnknownValueError:
            print("Je n'ai pas compris")
            self.text_output.insert(tk.END, "Je n'ai pas compris\n")
            self.text_output.update_idletasks()
        except sr.RequestError as e:
            print("Erreur de service; {0}".format(e))
            self.text_output.insert(tk.END, "Erreur de service; {0}\n".format(e))
            self.text_output.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
