from tkinter import *
from PIL import ImageTk, Image
import os
 
class QuBookInterface:

    QUESTION_LIST = [
        "How alive is Schrodinger's cat?",
        "Do you think Schrodinger should have a cat?",
        "Do you think Schrodinger should have opened the box?",
        "What is the likelihood that universe is deterministic?",
        "How much do you like cats?",
        "How much do you like quantum mechanics?",
    ]

    def __init__(self, qfb):
        self.qfb = qfb

    def record_answers(self):
        name_info = self.name_q.get()
        file = open(f"database/{name_info}.txt", "w")
        for answer in self.personality_answers:
            file.write(answer.get() + "\n")
        file.close()
    
        Label(self.input_screen, text="Answers recorded", fg="green", font=("calibri", 11)).pack()
        self.input_screen.destroy()

    # for finding friends to entangle with
    '''
    def find_friend():
        friend = friend_verify.get()
        find_friend_entry.delete(0, END) #represents textbox to search for friend
    
        list_of_users = os.listdir()
        if friend in list_of_users:
            file1 = open(friend, "r")
            traits = file1.read().splitlines() #obtains all the traits
        else:
            user_not_found()

    def user_not_found():
        global user_not_found_screen
        user_not_found_screen = Toplevel(login_screen)
        user_not_found_screen.title("Uh-Oh")
        user_not_found_screen.geometry("150x100")
        Label(user_not_found_screen, text="User Not Found :(").pack()
        Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()
    '''
    def input_account_screen(self):
        self.input_screen = Tk()
        self.input_screen.geometry("400x650")
        self.input_screen.title("QuBook")
        Label(self.input_screen, text="Welcome to QuBook!", bg="#AAC79D", width="300", height="2", font=("Calibri", 20)).pack()
        Label(text="").pack()
        Label(text="Please answer these personality questions to quantum-ly generate your profile photo!", bg="#AAC79D", width="300", height="2", font=("Calibri", 13)).pack()


        self.name_q = StringVar()
        self.personality_answers = []
        for question in self.QUESTION_LIST:
            self.personality_answers.append(StringVar())

        Label(text="Please enter 1 for yes, 0 for no", bg="#AAC79D", width="300", height="2", font=("Calibri", 13)).pack()
    
        Label(self.input_screen, text="").pack()
        name_label = Label(self.input_screen, text="Enter your name: ")
        name_label.pack()
        Entry(self.input_screen, textvariable=self.name_q).pack()
        Label(self.input_screen, text="").pack()
        for i in range(len(self.QUESTION_LIST)):
            question, q_var = self.QUESTION_LIST[i], self.personality_answers[i]
            Label(self.input_screen, text=f"Q{i+1}: {question}").pack()
            Entry(self.input_screen, textvariable=q_var).pack()
        
        Label(self.input_screen, text="").pack()

        Button(self.input_screen, text="Done!", width=10, height=1, bg="#AAC79D", command = self.record_answers).pack()

        self.input_screen.mainloop()

    def friendship_add_screen(self):
        self.friendship_screen = Tk()
        self.friendship_screen.geometry("300x450")
        self.friendship_screen.title("QuBook")
        Label(self.friendship_screen, text="Welcome to QuBook!", bg="#AAC79D", width="300", height="2", font=("Calibri", 20)).pack()
        Label(self.friendship_screen, text="").pack()
        Label(self.friendship_screen, text="Enter name of friend 1", bg="#AAC79D", width="300", height="2", font=("Calibri", 13)).pack()
        Label(self.friendship_screen, text="").pack()
        self.friend1_var = StringVar()
        self.friend2_var = StringVar()
        Entry(self.friendship_screen, textvariable=self.friend1_var).pack()
        Label(self.friendship_screen, text="").pack()
        Label(self.friendship_screen, text="Enter name of friend 2", bg="#AAC79D", width="300", height="2", font=("Calibri", 13)).pack()
        Label(self.friendship_screen, text="").pack()
        Entry(self.friendship_screen, textvariable=self.friend2_var).pack()
        Label(self.friendship_screen, text="").pack()
        Button(self.friendship_screen, text="Done!", width=10, height=1, bg="#AAC79D", command = self.record_friendship).pack()
        
        self.friendship_screen.mainloop()

    def record_friendship(self):
        friend1_str = self.friend1_var.get()
        friend2_str = self.friend2_var.get()
        # print(friend1, friend2)
        # friend1_str, friend2_str = 'c', 'y'
        friend1 = self.qfb.get_person(friend1_str)
        friend2 = self.qfb.get_person(friend2_str)
        print(friend1, friend2)
        self.qfb.add_friendship(friend1, friend2)
        self.friendship_screen.destroy()
        self.friends_profile_screen(friend1_str, friend2_str)
        
        


    def display_profile_screen(self):
        self.dp_screen = Tk()
        self.dp_screen.geometry("512x854")
        self.dp_screen.title("QuBook")
        Label(text="Welcome to QuBook!", bg="#AAC79D", width="300", height="2", font=("Calibri", 20)).pack()
        Label(text="").pack()
        Label(text="Here are your friends' profile photos!", bg="#AAC79D", width="300", height="2", font=("Calibri", 13)).pack()
        images = os.listdir("pfps")
        # print(images)
        names = [i.split('.')[0] for i in images]
        Label(text="    ", width="300", height="1", font=("Calibri", 10)).pack()
        for i, image in enumerate(images):
            img = Image.open(f"pfps/{image}")
            img = img.resize((120, 120), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img, master=self.dp_screen, width=64, height=64)
            label1 = Label(image=img, anchor=CENTER)
            label1.image = img
            label1.pack()
            Label(text=names[i], width="300", height="2", font=("Calibri", 12)).pack()
            
        # add friendship button
        Button(text="Add Friends", width="30", height="2", bg="#AAC79D", command=self.friendship_add_screen).pack()
        self.dp_screen.mainloop()

    def friends_profile_screen(self, friend1_name, friend2_name):
        self.friends_screen = Tk()
        self.friends_screen.geometry("512x854")
        self.friends_screen.title("QuBook")
        Label(text="Welcome to QuBook!", bg="#AAC79D", width="300", height="2", font=("Calibri", 20)).pack()
        Label(text="").pack()
        Label(text="Here are your friends' profile photos!", bg="#AAC79D", width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="    ", width="300", height="1", font=("Calibri", 10)).pack()
        img1 = Image.open(f"pfps/{friend1_name}.png")
        img1 = img1.resize((120, 120), Image.ANTIALIAS)
        img1 = ImageTk.PhotoImage(img1, master=self.friends_screen, width=64, height=64)
        label1 = Label(image=img1, anchor=CENTER)
        label1.image = img1
        label1.pack()
        Label(text=friend1_name, width="300", height="2", font=("Calibri", 12)).pack()
        img2 = Image.open(f"pfps/{friend2_name}.png")
        img2 = img2.resize((120, 120), Image.ANTIALIAS)
        img2 = ImageTk.PhotoImage(img2, master=self.friends_screen, width=64, height=64)
        label2 = Label(image=img2, anchor=CENTER)
        label2.image = img2
        label2.pack()
        Label(text=friend2_name, width="300", height="2", font=("Calibri", 12)).pack()
        self.friends_screen.mainloop()
        

        
if __name__ == "__main__":
    Interface = QuBookInterface()
    Interface.display_profile_screen()