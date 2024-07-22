import socket                                                                   #These are Keys Modules, This is necessary for internet Connection
import threading                                                                #This is necessary for running Functions simultaneously
import datetime                                                                 #
import pygame                                                                   #PYGAMMMEEEEE
                                                                                #
                                                                                #
starttime = str(datetime.datetime.now())[:-13]                                  #Give the date / hour time for a txt file
                                                                                #
                                                                                #Settings are below
SCREENHEIGHT = 480
SCREENWIDTH = 480
pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
SERVER = "192.168.0.13"                                                         #This sets where the Server actually is and where to connect too
FORMAT = "utf8"                                                                 #This is how the encoding works, and needs a consistent format
DISCONNECT_MESSAGE = "!poof"                                                    #When Typed you get a clean disconnect
HEADER = 64                                                                     #Is the standard length that can be sent
PORT = 5050                                                                     #The specifc point in the server you connect too
messagelog = open(f"CHATLOG {starttime}.txt", "a+")                             #Storing The Chat
chatlog = messagelog.readlines()                                                #Reading the file
contalk = True                                                                  #Lets the code be shutdown and unable to work
usernamename = ""                                                               #Username
ADDR = (SERVER, PORT)                                                           #Where the hell you connect
clock = pygame.time.Clock()
                                                                                #
                                                                                #
class Pygameutilities():
    def __init__(self):
        self.inputcheck = ["", True]
        
    def textintoimage(text : str, fontsize : int, fontcolour : str):
        font = pygame.font.SysFont("Arial", fontsize)
        image = font.render(text, 1, fontcolour)
        return image
    
    def textbox(self, events, inputbox):
        if inputbox == True:
            if events.key == pygame.K_BACKSPACE:
                self.inputcheck[0] = str(self.inputcheck[0])[:-1]
            if events.key != pygame.K_RETURN:
                self.inputcheck[0] += events.unicode
            if events.key == pygame.K_RETURN:
                self.inputcheck[1] = False
            if events.key == pygame.K_BACKSPACE:
                self.inputcheck[0] = str(self.inputcheck[0])[:-1]
    
    def button(distance : int, Height : int, text : str, colour : list=[60,60,60], fontsize=20, fontcolour : str="Black", colourighlight=20): #Buttons like hell man
        a,b = pygame.mouse.get_pos()
        buttonfont = pygame.font.SysFont('Arial',fontsize)
        Text = buttonfont.render(str(text), True, fontcolour)
        A = int(pygame.Surface.get_width(Text)) * 1.1
        button = pygame.Rect(SCREENWIDTH / 2 - A / 2 + distance, SCREENHEIGHT / 2 - fontsize *1.1 + Height, A, pygame.Surface.get_height(Text) * 1.4)
        if button.x <= a <= button.x + A and button.y <= b <= button.y + fontsize * 1.1:  
            pygame.draw.rect(screen,(colour[0] + colourighlight,colour[1] + colourighlight, colour[2] + colourighlight), button, border_radius=4)
        else:
            pygame.draw.rect(screen,(colour), button, border_radius= 4)
        screen.blit(Text,(SCREENWIDTH / 2 - int(pygame.Surface.get_width(Text)) / 2 + distance, button.y + fontsize * 1.1 - fontsize))
        return button    
    
class Client():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.usernameflip = True
        self.flipflop = False
        self.usernamename = ""
        self.contalk = True                                                     #Make sure that the code runs only if it's meant too
        self.alive = True                                                       #And Be able to turn the code off properly
        self.client.connect(ADDR)
                                                                                #
    def send_msg(self, msg):                                                    #Functionnssssss
        if self.contalk:                                                        #If you can talk
            message = msg.encode(FORMAT)                                        #Encode the message length
            msg_length = len(message)                                           #Get that length
            send_length = str(msg_length).encode(FORMAT)                        #And encode the message with that length
            send_length += b' ' * (HEADER - len(send_length))                   #Get the length for sending ready
            self.client.send(send_length)                                       #Send the length
            self.client.send(message)                                           #Send the message
            if msg == DISCONNECT_MESSAGE:                                       #If the message is the disconnect message
                self.contalk = False                                            #Don't allow Further message sending
                self.alive = False                                              #and kill the loop
                print(chatlog, file=messagelog)                                 #Record the chatlog
                                                                                #
    def recvmsg(self):                                                          #Receive messages
        if self.contalk:                                                        #if you can talk
            msg_length = self.client.recv(HEADER).decode(FORMAT)                #Get the length of the message
            if msg_length:                                                      #if it's correct
                msg_length = int(msg_length)                                    #get the length of the message as an integer
                msg = self.client.recv(msg_length).decode(FORMAT)               #receive the next message with that original message length
                msg = msg[2:-2]                                                 #take off the front and back of it
                msg = msg.split()                                               #split it into a list
                for message in msg:                                             #for every thing in it
                    if message == "',":                                         #if it is annoying
                        pass                                                    #do nothing
                    else:                                                       #
                        chatlog.append(message)                                 #append that to the log
            print(chatlog)
                                                                                #
                                                                                #
    def usermsg(self):                                                          #
        global contalk                                                          #Can talk
        if contalk:                                                             #If you can talk
            sendingmsg = input("Something to say - ")                           #Get user input to say stuff
            self.send_msg(sendingmsg)                                           #call your functions
                                                                                #
    def username(self):                                                         #Get a username
        sendingmsg = input("Choose a Username - ")                              #
        while len(sendingmsg) > 8 or len(sendingmsg.split()) > 1:               #Check if the name's bad
            sendingmsg = input("Please Choose a Shorter Single Name - ")        #Change that name
        self.usernamename = sendingmsg                                          #Get the name as the username
        self.send_msg(sendingmsg)                                               #send the name
                                                                                #
                                                                                #
    

    def clientstart(self):
        global chatlog
        while self.alive:
            if self.usernameflip:
                self.username()
                self.usernameflip = False
                clientsend = threading.Thread(target=self.usermsg)
                clientsend.start()
                clientrecv = threading.Thread(target=self.recvmsg)
                clientrecv.start()
            additionlength = 0
            currentnumber = 0
            screen.fill([60,60,60])
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    self.alive = False
                if events.type == pygame.K_a:
                    print("Hello?")
                    clientsend = threading.Thread(target=self.usermsg)
                    clientsend.start()
            for message in chatlog:
                if message == "'":
                    self.flipflop = True
                    currentnumber += 1
                if self.flipflop == True:
                    Usernameimg = Pygameutilities.textintoimage(message, 16, "Black")
                    screen.blit(Usernameimg,(30, currentnumber*44+83))
                    currentnumber += 1
                    additionlength = 0
                    self.flipflop = False
                elif message != "'" or message != ",":
                    messageimg  = Pygameutilities.textintoimage(message, 20, "Black")
                    additionlength += pygame.Surface.get_width(messageimg)
                    screen.blit(messageimg, (30 + additionlength, currentnumber*44+67))
            clientrecv = threading.Thread(target=self.recvmsg)
            clientrecv.start()
            pygame.display.update()
            
            
user = Client()
user.clientstart()


            