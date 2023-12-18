import tkinter as tk
from tkinter import scrolledtext
import threading
import openai
import speech_recognition as sr
import pyttsx3
import pywhatkit

# Configure OpenAI API key:
openai.api_key = "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"

class VoiceAssistantApp:
    #C'est une référence à la fenêtre principale de l'application (Tkinter Tk instance).
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
        # Start a new thread for listening and processing the command
        threading.Thread(target=self.process_command).start()

    def process_command(self):
        # crée un contexte avec un microphone en utilisant la bibliothèque SpeechRecognition.
        #Tout ce qui est enregistré par le microphone pendant l'exécution de ce bloc de code sera capturé.
        with sr.Microphone() as source:
            print("Ecoute...")
            self.text_output.insert(tk.END, "Ecoute...\n")
            self.text_output.update_idletasks()
            audio = self.recognizer.listen(source)

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
