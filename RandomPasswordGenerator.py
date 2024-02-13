from tkinter import *
import tkinter.messagebox as tmsg
import string
import random

root = Tk()
root.title("Random Password Generator")
root.geometry("470x200")

def generate_pwd():
    selected["complexity"] = complexity_var.get()
    selected["letters"] = letters_var.get()
    selected["numbers"] = numbers_var.get()
    selected["special characters"] = special_var.get()
    selected["length"] = length_var.get()

    characters = ""
    password = ""

    if selected["complexity"] == "high" and not (selected["letters"] and selected["numbers"] and selected["special characters"]):
        tmsg.showinfo("Suggestion", "It is suggested to select all the character types for high security.")
        return
    
    # Check if at least one checkbox is selected
    if not (selected["letters"] or selected["numbers"] or selected["special characters"]):
        tmsg.showerror("Error", "At least one character type must be selected.")
        return

    # Check if the entered length is greater than 8
    if selected["length"] < 8:
        tmsg.showerror("Error", "The length of the password must be greater than 8.")
        return
    
    if selected["letters"]:
        characters += string.ascii_letters
        password += random.choice(string.ascii_letters)
    if selected["numbers"]:
        characters += string.digits
        password += random.choice(string.digits)
    if selected["special characters"]:
        characters += string.punctuation
        password += random.choice(string.punctuation)

    remaining_length = selected["length"] - len(password)
    if remaining_length > 0:
        if selected["complexity"] == "low":
            password += ''.join(random.choice(characters) for i in range(remaining_length))
        elif selected["complexity"] == "medium":
            password += ''.join(random.sample(characters, remaining_length))
        else:  # high complexity
            password += ''.join(random.SystemRandom().choice(characters) for i in range(remaining_length))

    # Shuffle the password to ensure randomness
    password = ''.join(random.sample(password, len(password)))

    #Clipboard integration
    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()
    tmsg.showinfo("Password", "Password copied to clipboard.")

    print(password)
    
Label(root, text="Select specifications", font="comicsansms 15 italic").grid(column=0,row=1,columnspan=4)

complexity_var = StringVar(value="medium")
list_complexity = ["high","medium","low"]
Label(root, text="Complexity/Security", font="comicsansms 10").grid(column=1)

for i in list_complexity:
    radio = Radiobutton(root, text=i, variable=complexity_var, value=i, justify="left").grid(column=1,padx=10)

letters_var = IntVar()
numbers_var = IntVar()
special_var = IntVar()
list_char = [("letters", letters_var), ("numbers", numbers_var), ("special characters", special_var)]

Label(root, text="Characters", font="comicsansms 10").grid(row=2,column=2)
i=3
for ch, var in list_char:
    check = Checkbutton(root, text=ch, variable=var, justify="left").grid(row=i,column=2,padx=10)
    i+=1

length_var = IntVar(value=8)
Label(root, text="Minimum length of password").grid(row=2,column=3,sticky=NE)
l = Entry(root,textvariable=length_var,width=5).grid(row=2,column=4,sticky=NE)

selected = dict()
Button(root,text="Generate Password",command=generate_pwd).grid(columnspan=4,pady=20)

root.mainloop()