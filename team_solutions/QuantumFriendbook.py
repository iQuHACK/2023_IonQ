from sprite import Sprite
from qstate_to_repsn import QuantumPersonalityState, EntangledPersonalityState
from QuBookInterface import QuBookInterface
import os

class Friendbook:
    # This is the class that will hold the graph of all the people in the friendbook
    # It will also hold the list of all the people in the friendbook

    def __init__(self):
        self.people = []
        self.graph = {}

    def add_person(self, person):
        self.people.append(person)
        self.graph[person] = person.friends

    def add_friendship(self, person1, person2):
        self.graph[person1].append(person2)
        self.graph[person2].append(person1)
        person1.update_profile(person2)
        print(f"{person1.name} and {person2.name} are now friends!")


    def get_friends(self, person):
        return self.graph[person]

    def get_friends_of_friends(self, person):
        friends = self.get_friends(person)
        friends_of_friends = []
        for friend in friends:
            friends_of_friends.extend(self.get_friends(friend))
        return friends_of_friends

    def data_for_new_profile(self):
        ## this could be done on website
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        person = Person(name, age)
        friend_names = input("Enter the names of your friends, separated by commas: ")
        friend_names = friend_names.split(", ")

        if (input("Would you like to make a new profile? (y/n): ")) == "y":
            self.make_new_profile(person)
            print("Profile created and profile picture saved!")
            self.add_friends(person, friend_names)

    def make_new_profile(self, person):
        self.add_person(person)
        person.update_profile()

    def add_friends(self, person, friend_names):
        for friend_name in friend_names:
            for friend in self.people:
                if friend.name == friend_name:
                    self.add_friendship(person, friend)

    def get_person(self, name):
        for person in self.people:
            if person.name == name:
                return person

    def update(self):
        # open database
        files = os.listdir("database")
        for file in files:
            name = file.split(".")[0]
            with open(f"database/{file}", "r") as f:
                answers = list(map(int, f.read().splitlines()))
            p = Person(name, answers)
            self.make_new_profile(p)
        
        print("Friendbook updated!")

            
        



class Person:
    # This is the class that will hold the information about each person in the friendbook
    # It will hold the name, age, and friends of each person

    PERSONALITY_QUESTIONS = [
        "Do you think Schrodinger's cat is alive or dead?",
        "Do you think Schrodinger should have a cat?",
        "Do you think Schrodinger should have opened the box?",
        "What is the likelihood that universe is deterministic?",
        "How much do you like cats?",
        "How much do you like quantum mechanics?",
    ]

    def __init__(self, name, personality_traits=None):
        self.name = name
        self.friends = []
        self.personality_quantum_state = None
        if personality_traits is None:
            self.get_personality_traits()
        else:
            self.personality_traits = personality_traits

    def get_personality_traits(self):
        self.personality_traits = []

        print("Please enter answers to following questions in between 0 to 1")
        for question in self.PERSONALITY_QUESTIONS:
            print(question)
            self.personality_traits.append(float(input()))
        
    def update_profile(self, new_friend=None):
        self.update_profile_repsn(new_friend)
        self.update_profile_picture(new_friend)
    

    def update_profile_repsn(self, new_friend=None):
        # This function will return from pfp representation from quantum state based on personality traits and friends
        if new_friend is None:
            self.personality_quantum_state = QuantumPersonalityState(self.personality_traits)
            self.pfp_repsn = self.personality_quantum_state.get_pfp_reprn()
        else:
            eps = EntangledPersonalityState(self.personality_traits, new_friend.personality_traits)
            self.pfp_repsn, new_friend.pfp_repsn = EntangledPersonalityState.get_pfp_reprn(eps)
        
    def update_profile_picture(self, new_friend=None):
        self.sprite = Sprite(self.pfp_repsn)
        self.pfp = self.sprite.render()
        self.sprite.save(f"pfps/{self.name}.jpg")
        if new_friend is not None:
            new_friend.update_profile_picture()

    def __eq__(self, __o: object) -> bool:
        return self.name == __o.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"{self.name} ({self.personality_traits})"


if __name__=="__main__":
    qfb = Friendbook()
    qbi = QuBookInterface(qfb)
    while True:
        # qbi.input_account_screen()
        qfb.update()
        print(qfb.people)
        print(qfb.get_person("c"))
        qbi.display_profile_screen()
    # berkin = Person("Berkin", 20, [0,1,0,0,1,1])
    # qfb.make_new_profile(berkin)
    # chirag = Person("Chirag", 20, [1,1,0,0,1,1])
    # qfb.make_new_profile(chirag)
    # qfb.add_friendship(berkin, chirag)
