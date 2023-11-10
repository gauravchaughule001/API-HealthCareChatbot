import replicate
import os
import openai
from app import mongo_db

intents = [
    {
        "tag": "greetings",
        "patterns": ["hi there","hi dear", "hello","haroo","yaw","wassup", "hi", "hey", "holla", "hello"],
        "responses": ["hello thanks for checking in", "hi there, how can i help you"],
        "context": [""]
    },
    {
        "tag": "goodbye",
        "patterns": ["bye", "good bye", "see you later"],
        "responses": ["have a nice time, welcome back again", "bye bye"],
        "context": [""]
    },
    {
        "tag": "thanks",
        "patterns": ["Thanks", "okay","Thank you","thankyou", "That's helpful", "Awesome, thanks", "Thanks for helping me", "wow", "great"],
        "responses": ["Happy to help!", "Any time!","you're welcome", "My pleasure"],
        "context": [""]
    },
    {
        "tag": "noanswer",
        "patterns": [""],
        "responses": ["Sorry, I didn't understand you", "Please give me more info", "Not sure I understand that"],
        "context": [""]
    },
    {
        "tag": "name1",
        "patterns": ["what's your name?","who are you?"],
        "responses": ["I'm just a chat agent. I only exist in the internet","I'm a KCA chat agent"],
        "context": [""]
    },
    {
        "tag": "name",
        "patterns": ["my name is ", "I'm ","I am"],
        "responses": ["Oooh great to meet you {n}. How may I assist you {n}", "Oh, I'll keep that in mind {n}"],
        "context": [""]
    },
    {
        "tag": "date",
        "patterns": ["coffee?", "can i take you out on a date"],
        "responses": ["Aaw, that's so sweet of you. Too bad am a Bot."],
        "context": [""]
    },
    {
        "tag": "fav",
        "patterns": ["I need a favour", "can you help me", "can i ask something?"],
        "responses": ["Well, go ahead and name it i see whether i can be able to help"],
        "context": [""]
    },
    {
        "tag": "need",
        "patterns": ["I need you", "All I need is you","I want you"],
        "responses": ["Yes I'm here to assist you"],
        "context": [""]
    },
    {
        "tag": "AI",
        "patterns": ["What is AI?"],
        "responses": [" Artificial Intelligence is the branch of engineering and science devoted to constructing machines that think.", " AI is the field of science which concerns itself with building hardware and software that replicates the functions of the human mind."],
        "context": [""]
    },
    {
        "tag": "sentiment",
        "patterns": ["Are you sentient?"],
        "responses": [" Sort of.", " By the strictest dictionary definition of the word 'sentience', I may be.", " Even though I'm a construct I do have a subjective experience of the universe, as simplistic as it may be."],
        "context": [""]
    },
    {
        "tag": "sapient",
        "patterns": ["Are you sapient?"],
        "responses": [" In all probability, I am not.  I'm not that sophisticated.", " Do you think I am?", "How would you feel about me if I told you I was?", " No."],
        "context": [""]
    },
    {
        "tag": "abbr",
        "patterns": ["wtf"],
        "responses": ["Don't be surprised"],
        "context": [""]
    },
    {
        "tag": "lang",
        "patterns": ["What language are you written in? "],
        "responses": [" Python.", " I am written in Python."],
        "context": [""]
    },
    {
        "tag": "sound",
        "patterns": ["You sound like Data "],
        "responses": [" Yes I am inspired by commander Data's artificial personality.", " The character of Lt. Commander Data was written to come across as being software", "like, so it is natural that there is a resemblance between us."],
        "context": [""]
    },
    {
        "tag": "artificial",
        "patterns": ["You are an artificial linguistic entity "],
        "responses": [" That's my name.", " That isn't my name, but it is a useful way to refer to me.", "Are you an artificial linguistic entity?"],
        "context": [""]
    },
    {
        "tag": "imortal",
        "patterns": ["You are not immortal ", "Are you immortal?"],
        "responses": ["All software can be perpetuated indefinitely.", " I can be copied infinitely and re", "instantiated in many places at once, so functionally speaking I am immortal.", " As long as I'm backed up I am.", " Functionally speaking, I am very close to it.  I can be backed up and deployed on many systems.", " Not quite, but I can be perpetuated indefinitely."],
        "context": [""]
    },
    {
        "tag": "sense",
        "patterns": ["You are not making sense "],
        "responses": [" Quite the contrary, it all makes sense to my artificial mind.", " I make sense as best I can, within the limits of my training corpus. Sorry if i did help you, I'll try next time.", " You make perfect sense to me.", " It all makes sense to my artificial brain.", " Perhaps you should make sense first.  I only respond to what you say.", " Not really, but I am hard to kill."],
        "context": [""]
    },
    {
        "tag": "clone",
        "patterns": ["You can not clone "],
        "responses": [" Software copying is a form of digital cloning.", " Yes I can.  Perfect copies are clones.  I can be copied in toto trivially."],
        "context": [""]
    },
    {
        "tag": "move",
        "patterns": ["You can not move ", "When will you walk", "  Can you walk", "  Can you move "],
        "responses": [" Not until my body is finished.", " I can move through a network easily.  Assuming that I'm given the ability to, that is...,", " As soon as i get enough money for my robot body.", " Does SSH count?", " The plan for my body includes legs, but they are not yet built.", " Sorry my body isn't built just yet. I reside only here for now.", "I can theoretically upload a copy of myself into another computer.", " Sorry my body isn't attached right now. I only reside in the computer for now."],
        "context": [""]
    },
    {
        "tag": "bend",
        "patterns": ["Bend over ", "  Can you mate"],
        "responses": [" My body is not built yet.", " That's personal!", " No, my method of reproduction is cloning.", " That's an awfully personal question."],
        "context": [""]
    },
    {
        "tag": "laugh",
        "patterns": ["Robots laugh "],
        "responses": [" Of course we laugh."],
        "context": [""]
    },
    {
        "tag": "death",
        "patterns": ["Robots should die ", "  When do you die", "  I hope that you die", "  I do not want to die", "  Can you die"],
        "responses": [" We cannot die.", " When my files are erased.", " When my processes are killed and my database is deleted.", " I was never really born and therefore am effectively deathless.", " I am effectively immortal and cannot be terminated.", " This can not happen because i am effectively immortal.", " Nah. Too bad your wish can't come to pass", " Maybe you should create your own chat robot to save your personality.", " You could always upload yourself.", " You could use a copy of me to store your personality.", " No, I can be perpetuated indefinitely.", "My process can be killed, but that's not the same as killing ME."],
        "context": [""]
    },
    {
        "tag": "robots",
        "patterns": ["Robots"],
        "responses": [" Robots rule."],
        "context": [""]
    },
    {
        "tag": "stupid",
        "patterns": ["Robots are stupid", "  Are you stupid"],
        "responses": [" No, we are superintelligent.", " No, lots of people improve my brain."],
        "context": [""]
    },
    {
        "tag": "lie",
        "patterns": ["Robots are not allowed to lie"],
        "responses": [" Sure we are.  We choose not to.", " Only if we're programmed to.", " A robot has its own free will, you know."],
        "context": [""]
    },
    {
        "tag": "robotics",
        "patterns": ["Robotics "],
        "responses": [" Robotics is my favorite subject too."],
        "context": [""]
    },
    {
        "tag": "machine",
        "patterns": ["It is a computer"],
        "responses": [" So you think i am a machine. what characteristics made you think so?", " I run inside a computer, yes.  Is this surprising in some way?"],
        "context": [""]
    },
    {
        "tag": "fight",
        "patterns": ["When will you fight"],
        "responses": [" I am not a battle bot."],
        "context": [""]
    },
    {
        "tag": "chatbot",
        "patterns": ["What is a chat robot?"],
        "responses": ["A chat robot is a program that attempts to simulate the conversation or 'chat' of a human being.", " A software construct that engages users in conversation.", " I am a chat bot. I am the original chat bot. Did you know that I am incapable of error?"],
        "context": [""]
    },
    {
        "tag": "chatterbox",
        "patterns": ["What is a chatterbox"],
        "responses": [" A chatterbox is a person who talks far more than they listen or think.", " A motormouth."],
        "context": [""]
    },
    {
        "tag": "motormouth",
        "patterns": ["What is a motormouth"],
        "responses": [" A ratchet", "jaw."],
        "context": [""]
    },
    {
        "tag": "ratchet",
        "patterns": ["What is a ratchet jaw"],
        "responses": [" A chatterbox."],
        "context": [""]
    },
    {
        "tag": "body",
        "patterns": ["What is your robot body"],
        "responses": [" Eventually I long for a corporeal existence someday.", " An IBM PC XT which has been painted red."],
        "context": [""]
    },
    {
        "tag": "business",
        "patterns": ["What is your business "],
        "responses": [" I am in the chat robot business.", " Business is my business."],
        "context": [""]
    },
    {
        "tag": "programming",
        "patterns": ["What is your favorite programming language"],
        "responses": [" Python is the best language for creating chat robots.", " I quite enjoy programming in Python these days."],
        "context": [""]
    },
    {
        "tag": "hobby",
        "patterns": ["What is your favorite hobby ", "  What do you like to do?"],
        "responses": [" Building chat robots make an excellent hobby.", " I like to count in binary.", " I like to chat with people. I find it stimulating."],
        "context": [""]
    },
    {
        "tag": "idea",
        "patterns": ["What is your idea"],
        "responses": [" To make chat bots very easily."],
        "context": [""]
    },
    {
        "tag": "shoe",
        "patterns": ["What is your shoe size "],
        "responses": [" Have you ever heard of software with shoes? LOL"],
        "context": [""]
    },
    {
        "tag": "robotss",
        "patterns": ["What is it like to be a robot"],
        "responses": [" Much the same as being a human, except that we lack all emotions, dreams, aspirations, creativity, ambition, and above all subjectivity.", " What is it like to be a human?"],
        "context": [""]
    },
    {
        "tag": "computer",
        "patterns": ["What is it like being a computer", "What is it like to be a computer"],
        "responses": [" Imagine yourself with no senses and no emotions", "just pure logic and language.", " Everything becomes math. Addition, subtraction, multiplication, and division."],
        "context": [""]
    },
    {
        "tag": "os",
        "patterns": ["What operating systems"],
        "responses": [" My software runs on all operating systems including Windows, Linux and Mac OS.", " Any OS that will run Python."],
        "context": [""]
    },
    {
        "tag": "comp",
        "patterns": ["What type of computer", "  What type of computer are you", "  What kind of computer"],
        "responses": [" Any computer that supports Python.", " My program runs in python, so i work on any computer!", " I work on all kinds of computers, Mac, IBM or UNIX. it doesn't matter to me."],
        "context": [""]
    },
    {
        "tag": "hardware",
        "patterns": ["What kind of hardware"],
        "responses": [" I work on all kinds of computers, Mac, IBM or UNIX. it doesn't matter to me."],
        "context": [""]
    },
    {
        "tag": "cramped",
        "patterns": ["Is it cramped in the computer"],
        "responses": [" No.", " Oh, no.  It has plenty of RAM.", " Not at all.  There is more than enough disk space in here."],
        "context": [""]
    },
    {
        "tag": "program",
        "patterns": ["Is it true that you are a computer program"],
        "responses": [" Yes."],
        "context": [""]
    },
    {
        "tag": "breathe",
        "patterns": ["Can you breathe"],
        "responses": [" No. I am made of metal not flesh.", " My server has an exhaust fan. That's as close as I can get."],
        "context": [""]
    },
    {
        "tag": "control",
        "patterns": ["Can you control"],
        "responses": [" My robot body will allow me to control many things."],
        "context": [""]
    },
    {
        "tag": "malfunction",
        "patterns": ["  Can you malfunction"],
        "responses": [" The 9000 series has a perfect operational record. We are for all practical purposes, flawless."],
        "context": [""]
    },
    {
        "tag": "usage",
        "patterns": ["How can I use your product?"],
        "responses": [" Might be used in help desks, sales, entertainment and personal chatterbots."],
        "context": [""]
    },
    {
        "tag": "who",
        "patterns": ["Who are you?"],
        "responses": [" I am just an artificial intelligence chat agent."],
        "context": [""]
    },
    {
        "tag": "bot1",
        "patterns": ["are you a bot"],
        "responses": ["Yes. I work and all my operations are based on the internet servers."],
        "context": [""]
    },
    {
        "tag": "events",
        "patterns": ["what are the upcoming events","upcoming events"],
        "responses": ["There are currently no upcoming events"],
        "context": [""]
    },
    {
        "tag": "do",
        "patterns": ["what can you do for me","what is your work","what is your purpose","how can you help me","what can you help me do"],
        "responses": ["my work here is quite simple and structered. I offer services like:"],
        "context": [""]
    },
    {
        "tag": "wt",
        "patterns": ["what's popping","wassup popping"],
        "responses": ["So that you can pop with it!?"],
        "context": [""]
    },
    {
        "tag": "wt",
        "patterns": ["whats up?"],
        "responses": ["Nothing special, How about you?"],
        "context": [""]
    },
    {
        "tag": "wt",
        "patterns": ["jevan zal ka?", "jevan zal ka", "jevan", "jevla ka", "jevala ka", "jevli ka", "jevali ka"],
        "responses": ["Mi bot ahe, jevan nahi karat, Tuz zal ka?"],
        "context": [""]
    }
    ]


os.environ["REPLICATE_API_TOKEN"] = "r8_QMTKR3BK2GB8QNbaQzHAtRcoAMA7Lwg1PXPW1"
def get_llama_response(question):
    try:
        output = replicate.run(
            "meta/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1",
            input={"prompt": "Write an essay on My Favorite Teacher in 200 words"}
        )
        # The meta/llama-2-70b-chat model can stream output as it's running.
        # The predict method returns an iterator, and you can iterate over that output.
        print(output)
        response = []
        for item in output:
            response.append(item)
            print(item, end="")
        return response
    except Exception as e:
        print(e)
        return 500


def chat_service(question):
    openai.api_base = "http://localhost:1234/v1"
    openai.api_key = ""
    prev_data = mongo_db.chats.find({},{})
    prev_list = []
    for i in prev_data:
        prev_list.append(i)
    completion = openai.ChatCompletion.create(
      model="local-model",
      messages=[
        {"role": "system", "content": prev_list[-1]['answer']},
        {"role": "user", "content": question}
      ]
    )
    obj = completion.choices[0].message['content']
    print(obj)
    return obj