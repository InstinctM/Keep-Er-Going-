from tkinter import Button, PhotoImage, Label, colorchooser, messagebox
from tkinter import Tk, Canvas, Entry, END
from random import randint as rand
import time
import pickle

# Class for Platforms
class Platforms:
    def __init__(self,x0,y0,x1,y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.c_val = 0

        self.platform = canvas.create_rectangle(x0,y0,x1,y1, fill="green")
        
    #  Making platforms rise from bottom
    def movePlatform(self):
        global pos1
        global currentscore
        pos1 = canvas.coords(self.platform)
        if pos1 [3] < 0:
            x = rand(0,800)
            self.c_val = rand(0,4)
            canvas.coords(self.platform,x,780,x+150,800)
            canvas.itemconfig(self.platform,fill=colour[self.c_val])

            currentscore += 1
            score = "Score: " + str(currentscore)
            canvas.itemconfig(scoreText, text=score)
        canvas.move(self.platform, 0, -speed)

# Detects any collision between ball and platforms
def collison():
    global bp
    global currentHealth
    global invincible
    bp = []
    for i in range(len(p)):
        bp.append(canvas.coords(p[i].platform))
        if bp[i][0] <= ballpos[0] <= bp[i][2] and bp[i][0] <= ballpos[2] <= bp[i][2] and ballpos[3] >= bp[i][1]:
            canvas.move(ball, 0, 2*-speed)
            if p[i].c_val >=3 and invincible < 10:
                currentHealth -= 2
                health = "Health:" + str(currentHealth)
                canvas.itemconfig(healthText, text=health)
                invincible = 100

# Default ball colour
def defaultball():
    global customizeballColour
    
    canvas.delete("all")
    customizeballColour = 0
    defaultPlatform()
    gameStart()
    
# Customize Ball colour
def customizeball():
    canvas.delete("all")
    global ball_colour
    global customizeballColour

    customizeballColour = 1
    opencolourChooser = colorchooser.askcolor()
    ball_colour.append(opencolourChooser[1]) 
    defaultPlatform()
    gameStart()

# Create Ball
def makeBall():
    global ball
    global diameter
    global customizeballColour
    diameter = 40
    ball = canvas.create_oval(0,0,diameter,diameter,fill=ball_colour[customizeballColour])

# Falling of the ball
def moveball():
    global ballpos
    ballpos = canvas.coords(ball)
    if ballpos [1] < 800:
        canvas.move(ball, 0, speed)
        collison()
     
    # Ball appearing from other side of window  
    if ballpos [2] < 0:
        canvas.coords(ball,game_width,ballpos[1],game_width-diameter,ballpos[3])
    elif ballpos [0] > 800:
        canvas.coords(ball,0-diameter,ballpos[1],0,ballpos[3])

# Create Health Count
def healthtxt(loadedHP = 10):
    global healthText
    global currentHealth
    currentHealth = loadedHP
    health = "Health:" + str(currentHealth)
    healthText = canvas.create_text(100, 20, fill="white", font=("Arial Bold",20), text=health)

# Create Score Count
def scoretxt(loadedScore = 0):
    global scoreText
    global currentscore
    currentscore = loadedScore
    score = "Score:" + str(currentscore)
    scoreText = canvas.create_text(100, 50 , fill="white", font=("Arial Bold",20), text=score)

# Game Over when ball exits top and bottom
def healthSystem():
    global currentHealth
    global ballpos
    if ballpos [3] < 0 or ballpos[1] >= 800:
        currentHealth = 0
        health = "Health:" + str(currentHealth)
        canvas.itemconfig(healthText, text=health)

# Checking if the game is paused and update each platforms' location
def clock():
    global paused
    global currentHealth

    if not paused:
        gameUpdate()
    if currentHealth > 0 :
        window.after(20, clock)

# Surprise...?
def afterSurprise():
    pause()
    surprise_label.place(x=-1000,y=1000)
    canvas.create_text(400, 200, fill="white", font="Times 50 italic bold", text="LMAO")
    window.after(500, closeGame)

# User choose colour
def choosecolorPage():
    choosecolorMessage = "Pick a ball colour \n to start the game"
    canvas.create_text(400, 200, fill="white", font="Times 50 italic bold", text=choosecolorMessage)
    backButton.place(x=300,y=600)
    name_label.place(x=-1000,y=1000)
    playButton.place(x=-1000,y=1000)
    loadButton.place(x=-1000,y=1000)
    defaultButton.place(x=150,y=400)
    customizeButton.place(x=450, y=400)

# Back Button
def back():
    canvas.delete("all")
    defaultButton.place(x=-1000,y=1000)
    customizeButton.place(x=-1000,y=1000)
    backButton.place(x=-1000,y=1000)
    name_label.place(x=100,y=100)
    playButton.place(x=300,y=300)
    loadButton.place(x=300,y=400)
    

def defaultPlatform():
    global p

    p = [Platforms(0,0,150,20),
    Platforms(100,100,250,120),
    Platforms(200,200,350,220),
    Platforms(300,300,450,320),
    Platforms(400,400,550,420),
    Platforms(500,500,650,520),
    Platforms(600,600,750,620),
    Platforms(700,700,850,720)]

# Press button to start game
def gameStart():
    global invincible
    
    defaultButton.place(x=-1000,y=1000)
    customizeButton.place(x=-1000, y=1000)
    backButton.place(x=-1000, y=1000)
    saveButton.place(x=690,y=0)
    pauseButton.place(x=750,y=0)

    invincible = 0

    healthtxt()
    scoretxt()
    makeBall()  

    clock()

# Pausing the game  
def pause():
    global paused    
    paused = not paused

# Moving the platforms and ball
def gameUpdate():
    global p
    global invincible
    global currentHealth

    p[0].movePlatform()
    p[1].movePlatform()
    p[2].movePlatform()
    p[3].movePlatform()
    p[4].movePlatform()
    p[5].movePlatform()
    p[6].movePlatform()
    p[7].movePlatform()

    moveball()
    invincible = abs(invincible-2)
    healthSystem()
    gameOver()

# Gameover message
def gameOver():
    if currentHealth == 0:
        canvas.delete("all")
        pauseButton.place(x=-1000,y=1000)
        saveButton.place(x=-1000,y=1000)
        canvas.create_text(400, 100, fill="white", font="Times 50 italic bold", text="Game Over!")
        playagainButton.place(x=300,y=400)
        leaderboardButton.place(x=300,y=500)
        mainMenuButton.place(x=300,y=600)
        playerName()

# Play again after Gameover
def playAgain():
    canvas.delete("all")
    playagainButton.place(x=-1000,y=1000)
    submitButton.place(x=-1000,y=1000)
    leaderboardButton.place(x=-1000,y=1000)
    mainMenuButton.place(x=-1000,y=1000)
    choosecolorMessage = "Pick a ball colour \n to start the game"
    canvas.create_text(400, 200, fill="white", font="Times 50 italic bold", text=choosecolorMessage)
    defaultButton.place(x=150,y=400)
    customizeButton.place(x=450, y=400)
    backButton.place(x=300,y=600)
    choosecolorPage()
    
# Main Meun Button
def mainMenu():
    canvas.delete("all")
    nameEntry.place(x=-1000,y=1000)
    submitButton.place(x=-1000,y=1000)
    playagainButton.place(x=-1000,y=1000)
    mainMenuButton.place(x=-1000,y=1000)
    leaderboardButton.place(x=-1000,y=1000)
    name_label.place(x=100,y=100)
    playButton.place(x=300,y=300)
    loadButton.place(x=300,y=400)

# Display game saved message
def gameSavedtext():
    global gameSaved
    global gameSavedmessage
    gameSaved = "    Game Saved!\nGame closing in 3..."
    gameSavedmessage = canvas.create_text(400, 200, fill="white", font="Times 50 italic bold", text=gameSaved)
    window.after(3000, closeGame)

# Save Game Function
def saveGame():
    pause()
    saveballpos = open("gamefiles/saveBallpos","wb")
    pickle.dump(ballpos, saveballpos)
    saveballpos.close()

    savePlatformpos = open("gamefiles/savePlatformpos","wb")
    pickle.dump(bp, savePlatformpos)
    savePlatformpos.close()

    saveHP = open("gamefiles/currenthealth","wb")
    pickle.dump(currentHealth, saveHP)
    saveHP.close()

    saveScore = open("gamefiles/currentscore", "wb")
    pickle.dump(currentscore, saveScore)
    saveScore.close()

    canvas.delete("all")
    saveButton.place(x=-1000,y=1000)
    pauseButton.place(x=-1000,y=1000)

    window.after(3000, gameSavedtext)

# Load Game Function
def loadGame():
    global ballpos
    global p
    global ball
    global currentHealth
    global currentscore
    global healthText
    global paused

    paused = True

    canvas.delete("all")

    loadballpos = open("gamefiles/saveBallpos","rb")
    ballpos = pickle.load(loadballpos)
    ball = canvas.create_oval(ballpos[0],ballpos[1],ballpos[2],ballpos[3],fill=ball_colour[customizeballColour])

    loadHP = open("gamefiles/currenthealth","rb")
    currentHealth = pickle.load(loadHP)
    healthtxt(currentHealth)

    loadScore = open("gamefiles/currentscore","rb")
    currentscore = pickle.load(loadScore)
    scoretxt(currentscore)

    loadPlatformpos = open("gamefiles/savePlatformpos","rb")
    PL = pickle.load(loadPlatformpos)

    p = [Platforms(PL[0][0],PL[0][1],PL[0][2],PL[0][3]),
    Platforms(PL[1][0],PL[1][1],PL[1][2],PL[1][3]),
    Platforms(PL[2][0],PL[2][1],PL[2][2],PL[2][3]),
    Platforms(PL[3][0],PL[3][1],PL[3][2],PL[3][3]),
    Platforms(PL[4][0],PL[4][1],PL[4][2],PL[4][3]),
    Platforms(PL[5][0],PL[5][1],PL[5][2],PL[5][3]),
    Platforms(PL[6][0],PL[6][1],PL[6][2],PL[6][3]),
    Platforms(PL[7][0],PL[7][1],PL[7][2],PL[7][3])]

    name_label.place(x=-1000,y=1000)
    playButton.place(x=-1000,y=1000)
    loadButton.place(x=-1000,y=1000)
    saveButton.place(x=690,y=0)
    pauseButton.place(x=750,y=0)

    gameUpdate()

    window.after(1000, pause)

    window.after(3000, clock)

# Enter Playername
def playerName():
    global nameEntry
    global nameEntryBox
    nameEntry = Entry(window, font=("Helvetica", 24), width=30, bd=0)
    nameEntry.insert(0,"Insert your name")
    nameEntryBox = canvas.create_window(410, 300, window=nameEntry)
    submitButton.place(x=360,y=350)
    nameEntry.bind("<Button-1>", entry_clear)

# Empty info in entry box
def entry_clear(e):
    if nameEntry.get() == "Insert your name":
        nameEntry.delete(0, END)

# Submit Name Button
def submitName():
    username = nameEntry.get()
    file = open("gamefiles/leaderboard.txt","a")
    file.write(str(currentscore) + "," + username + "|")
    file.close()
    nameEntry.delete(0, END)
    nameEntry.place(x=-1000,y=1000)
    submitButton.place(x=-1000,y=1000)

# Sorting Key
def sortingKey(e):
    return int(e.split(",")[0])

# Leaderboard Button
def leaderboard():
    global Leaderboard
    global topScore1
    global topScore2
    global topScore3

    file = open("gamefiles/leaderboard.txt","r")
    readfile = file.readline()
    Leaderboard = readfile.split("|")
    file.close()
    
    Leaderboard.pop()
    Leaderboard.sort(reverse=True, key=sortingKey)
    topScore1 = Leaderboard[0].split(",")
    topScore2 = Leaderboard[1].split(",")
    topScore3 = Leaderboard[2].split(",")

    leaderboardText()
    
# Leaderboard text 
def leaderboardText():
    canvas.create_text(400,170, fill="yellow", font="Times 20 italic bold", text="Highest Score")
    canvas.create_text(350,200, fill="yellow", font="Times 10 italic bold", text=topScore1[1])
    canvas.create_text(450,200, fill="yellow", font="Times 10 italic bold", text=topScore1[0])
    canvas.create_text(350,220, fill="yellow", font="Times 10 italic bold", text=topScore2[1])
    canvas.create_text(450,220, fill="yellow", font="Times 10 italic bold", text=topScore2[0])
    canvas.create_text(350,240, fill="yellow", font="Times 10 italic bold", text=topScore3[1])
    canvas.create_text(450,240, fill="yellow", font="Times 10 italic bold", text=topScore3[0])

# Closing the game
def closeGame():
    window.destroy()

# Left-Right Movement of character
def leftKey(event):
    canvas.move(ball, -10 ,0)
def rightKey(event):
    canvas.move(ball, 10 ,0)
# Cheatcode: Raise current health
def upKey(event):
    global currentHealth
    currentHealth += 2
    health = "Health:" + str(currentHealth)
    canvas.itemconfig(healthText, text=health)
# Cover window with image
def bossKey(event):
    pause()
    saveButton.place(x=-1000,y=1000)
    bosskey_label.place(x=0,y=0)
# Resume the game
def closebossKey(event):
    pause()
    saveButton.place(x=690,y=0)
    bosskey_label.place(x=-1000,y=1000)
# Surprise
def surprise(event):
    global currentHealth
    saveButton.place(x=-1000,y=1000)
    saveButton.place(x=-1000,y=1000)
    canvas.delete("all")
    surprise_label.place(x=0,y=0)
    currentHealth = 0
    window.after(300, afterSurprise)



window = Tk()
window.title("Keep er' goin'")
window.geometry("800x800")
window.resizable(False, False)

game_width = 800
game_height = 800
speed = 5
background_color = "black"

canvas = Canvas(window, bg=background_color, height=game_height, width=game_width)
canvas.pack()

ball_colour = ["red"]

colour = ["green","green","green", "yellow", "yellow"]
           
window.bind("<Left>", leftKey) 
window.bind("<Right>", rightKey)
window.bind("<Up>", upKey)
window.bind("<Shift-Q>", bossKey)
window.bind("<Shift-W>", closebossKey)
window.bind("<Control-Shift-P>", surprise)
window.focus_set()

paused = False

customizeballColour = 0

currentHealth = 10

invincible = 0

namePic = PhotoImage(file="pictures/gameName.png")
name_label = Label(window, image=namePic)
name_label.place(x=100, y=100)

playPic = PhotoImage(file="pictures/playButton.png")
playButton = Button(window, image=playPic, width="200", height="72", command=lambda: choosecolorPage())
playButton.place(x=300,y=300)

backPic = PhotoImage(file="pictures/back.png")
backButton = Button(window, image=backPic, width="200", height="72", command=lambda: back())

pausePic = PhotoImage(file="pictures/pauseButton.png")
pauseButton = Button(window, image=pausePic, width="50", height="50", command=lambda: pause())

playagainPic = PhotoImage(file="pictures/playagainButton.png")
playagainButton = Button(window, image=playagainPic, width="200", height="72", command=lambda: playAgain())

mainMenuPic = PhotoImage(file="pictures/mainMenu.png")
mainMenuButton = Button(window, image=mainMenuPic, width="200", height="72", command=lambda: mainMenu())

bosskeyPic = PhotoImage(file="pictures/working.png")
bosskey_label = Label(window, image=bosskeyPic)

surprisePic = PhotoImage(file="pictures/surprise.png")
surprise_label = Label(window, image=surprisePic)

savePic = PhotoImage(file="pictures/saveButton.png")
saveButton = Button(window, image=savePic, width="50", height="50", command=lambda: saveGame())

loadPic = PhotoImage(file="pictures/loadButton.png")
loadButton = Button(window, image=loadPic, width="200", height="72", command=lambda: loadGame())
loadButton.place(x=300,y=400)

leaderboardPic = PhotoImage(file="pictures/leaderboard.png")
leaderboardButton = Button(window, image=leaderboardPic, width="200", height="72", command=lambda: leaderboard( ))

submitButton = Button(window, text="Click to submit", command=lambda: submitName())

defaultPic = PhotoImage(file="pictures/default.png")
defaultButton = Button(window, image=defaultPic, width="200", height="72", command=lambda: defaultball())

customizePic = PhotoImage(file="pictures/customize.png")
customizeButton = Button(window, image=customizePic, width="200", height="72", command=lambda: customizeball())

window.mainloop()
