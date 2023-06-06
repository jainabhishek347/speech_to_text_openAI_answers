"""  This script will take input from any active app which produces sound from your system 
then it download the audio and converts the sound into Text and give that Text to openAI. OpenAI 
founds the answer, reply it and then both question and answer will be displayed in the Tkinter GUI 
start and stop buttons are used for start and stop recording. once you start recording you need to 
stop it, once you stop, it will show the Q&A in windows """

import tkinter as tk
import subprocess
import speech_recognition as sr
import os
import openai

# Set the parameters for recording
# duration = 10  # Duration of each recording in seconds
output_file = "output.wav"  # Output file name and path
recording_process = None

def start_recording():
    global recording_process
    # Start recording audio from the system's audio input using PulseAudio
    print("Recording start")
    recording_process = subprocess.Popen(["ffmpeg", "-f", "pulse", "-i", "default", output_file])
    print("Recording done")

def stop_recording():
    global recording_process
    print("In stop_recording outside if block :")
    if recording_process is not None:
        print("In stop_recording inside the if block")
        # Stop the PulseAudio recording process
        recording_process.terminate()
        recording_process.wait()
        print("Recording stopped, Recording saved to", output_file)
        # Convert audio to text
        convert_audio_to_text(output_file)
        os.remove("/home/hp/Desktop/chintu/tran/output.wav")

openai.api_key = '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'
messages = [
    {"role": "system", "content":"You are a helpful assistance."},
]
def ai_reply(message):
    print("ans")
    try:
        if message:
            if message.lower() in ["quit", "bye", "exit"]:
                print("Ram Ram DADA!!")
            messages.append(
                {"role": "user", "content":message},
            )
            chat = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",messages=messages
            )
        if chat:
            print("found ans")
            reply = chat.choices[0].message.content
            print(f"ChatGpt : {reply}")
            Role=messages[-1]['role']
            Question=messages[-1]['content']
            Answer=reply
            messages.append({"role":"assistant", "content":reply})
            # cur.execute(insert_query,(Role,Question,Answer))
            # conn.commit()
    except Exception as err:     
        # conn.rollback()
        print(err)
    return reply

def convert_audio_to_text(audio_file):
    try:
        print("convert_audio_to_text")
        r = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            print("Converted Text:", text)
            text_entry.insert(tk.END, "Question : "+text+"\n","left_align")
            k = ai_reply(text)
            text_entry.insert(tk.END, "Answer : "+k+"\n","left_align")
            # text_entry.insert(tk.END, "Question : "+text+"\n","left_align")
    except sr.UnknownValueError as ee:
        print("could not understand")
        # text_entry.insert(tk.END, "Could not understand audio\n")
    except sr.RequestError as e:
        # text_entry.insert(tk.END, f"Error: {e}"+"\n")
        print(e)
    except Exception as e:
        print(e)
    
def exit_program():
    window.destroy()

# Create the tkinter window
window = tk.Tk()
text_entry = tk.Text(window, height=30, width=110)
text_entry.pack()

# Create a button to start the recording
start_button = tk.Button(window, text="Start Recording", command=start_recording)
start_button.pack()

# Create a button to stop the recording and convert audio to text
stop_button = tk.Button(window, text="Stop Recording", command=stop_recording)
stop_button.pack()

# Closing button
exit_button = tk.Button(window, text="Exit", command=exit_program)
exit_button.pack()

# Start the tkinter event loop
window.mainloop()
