from cmu_graphics import *

#Program Name: SDLC Mini-Project - Quiz
#Author:       Emily Huynh
# Date:        May 22, 2023
# Description: This is a quiz application.

### Definitions
def setVisibleFalse():
    quizTitle.visible=False
    questionCount.visible=False
    score.visible=False
    scoreDisplay.visible=False
    questionDisplay.visible=False
    questionCountDisplay.visible=False
    blocksGroupedMC.visible=False
    textGroupedMC.visible=False
    TrueOrFalsePage.visible=False

def scoreDisplayProperties(size, left1, left2, y):
    score.size=size
    score.left=left1
    scoreDisplay.size=size
    scoreDisplay.left=left2
    scoreGroup.centerY=y

def displayAttempts():
    for attempt in range(len(quizAttempts)):
        attemptDisplay.append(Label("Attempt "+str(attempt+1)+": "+str(quizAttempts[attempt])+"/100", 80, (attempt+1)*35+60, size=17, fill='lightCyan'))
        viewAttemptsShape.visible=True
        if attempt<8:
            attemptDisplay[attempt].left=35
            attemptDisplay[attempt].centerY= (attempt+1)*35+50
        elif attempt<16:
            attemptDisplay[attempt].left=220
            attemptDisplay[attempt].centerY=(attempt-7)*35+50
        else:
            pass

def mainMenuActions(mouseX, mouseY):
    if startQuiz.hits(mouseX, mouseY):     
        mainPage.visible=False
        quizTitle.visible=True
        score.value=0
        scoreDisplayProperties(15, 80, 26, 380)
        questionCount.value=1
        quiz()                              
    elif viewAttempts.hits(mouseX, mouseY): 
        mainPage.visible=False
        scoreGroup.visible=False
        viewAttemptsHeader.visible=True
        pressBackspace.visible=True
        displayAttempts()                  
    elif quit1.hits(mouseX, mouseY):                                    
        mainPage.visible=False
        scoreGroup.visible=False
        Label("Have a great day!", 200, 200, size=20, fill='lightCyan') 
    else:
        pass

def postQuizActions(mouseX, mouseY):
    if redoQuiz.hits(mouseX, mouseY):              
        score.value=0
        retryAttempt.visible=False
        scoreDisplayProperties(15, 80, 26, 380)
        questionCount.value=1
        questionCount.fill='lightCyan'
        questionCountDisplay.fill='lightCyan'
        postQuiz.visible=False
        quiz()                                      
    elif viewAnswers.hits(mouseX, mouseY):          
        for i in range(10):                         
            viewAnswerDisplay[i].visible=True
            viewAnswerDisplay[i].left=17
        quizTitle.visible=False
        viewAnswersHeader.visible=True
        postQuiz.visible=False
        scoreGroup.visible=False
        pressBackspace.visible=True
        pressBackspace.centerY=380
        lineGroup.visible=True
    elif mainMenu.hits(mouseX, mouseY):             
        mainPage.visible=True                       
        postQuiz.visible=False
        quizTitle.visible=False
        retryAttempt.visible=False
        scoreDisplayProperties(20, 225, 160, 350)
        scoreGroup.centerX=200
    elif quit.hits(mouseX, mouseY):  
        postQuiz.visible=False
        quizTitle.visible=False
        scoreGroup.visible=False
        Label("Thank you for playing.", 200, 185, size=20, fill='lightCyan') 
        Label("Have a great day!", 200, 215, size=20, fill='lightCyan') 

def answerSelection(mouseX, mouseY):
    answer, wrongAnswer, retry=quiz()
    if retryAttempt.visible==True:                                      
        del retryQuestions[0]
    if answer.hits(mouseX, mouseY):                 
        correct.visible=True                      
        # if first time answering question, add 10 points to score
        if retryAttempt.visible==False:             
            score.value+=10                         
            pointsDisplay.value="+10 points" 
        # if second time answering question, add 5 points to score
        else:                                       
            score.value+=5                          
            pointsDisplay.value="+5 points" 
        setVisibleFalse()
    for element in wrongAnswer:
        if (element.hits(mouseX, mouseY)) and (element.visible==True): 
            incorrect.visible=True                                     
            setVisibleFalse()
            if retryAttempt.visible==False:
                retryQuestions.append(retry)       

def onKeyPress(key):
    # goes back to main menu
    if key=='backspace' and viewAttemptsHeader.visible==True:
        mainPage.visible=True                                
        for attempt in range(len(attemptDisplay)): 
            attemptDisplay[0].visible=False
            del attemptDisplay[0]
        pressBackspace.visible=False
        scoreGroup.visible=True
        viewAttemptsHeader.visible=False
        viewAttemptsShape.visible=False
    # goes back to post-quiz page
    elif key=='backspace' and viewAnswersHeader.visible==True:
        for i in range(10):
            viewAnswerDisplay[i].visible=False
        pressBackspace.visible=False
        postQuiz.visible=True                                  
        quizTitle.visible=True
        scoreGroup.visible=True
        viewAnswersHeader.visible=False
        lineGroup.visible=False
    # continues with quiz
    elif key=='enter' and (incorrect.visible==True or correct.visible==True): 
        incorrect.visible=False
        correct.visible=False
        questionCount.value +=1
        quiz()    
    # starts retry attempt
    elif key=='enter' and retryPage.visible==True:  
        retryPage.visible=False
        retryAttempt.visible=True                  
        questionCount.value+=1
        quiz()                                      
    else:
        pass\

# displays question and answer options 
def questionPage(argumentsList):                         
    question, answer, optionsList, questionType = argumentsList   
    incorrectOptions=[]
    questionDisplay.value=question
    questionDisplay.visible=True
    if questionType=="MC":
        for block in range(4):
            if answer!=blocksListMC[block]:
                incorrectOptions.append(blocksListMC[block])
        answerA.value, answerB.value, answerC.value, answerD.value = optionsList
        blocksGroupedMC.visible=True
        textGroupedMC.visible=True
    elif questionType=="True/False":
        TrueOrFalsePage.visible=True
        if answer==blockT:
            incorrectOptions.append(blockF)
        else:
            incorrectOptions.append(blockT)
    return [answer, incorrectOptions, argumentsList]

# runs quiz 
def quiz():               
    quizTitle.visible=True
    score.visible=True
    questionCount.visible=True
    questionCountDisplay.visible=True
    scoreDisplay.visible=True
    if questionCount.value<11: 
        return questionPage(questionsList[questionCount.value-1])   
    # displays retry page to user if quiz is complete and some answers are incorrect
    elif questionCount.value==11 and len(retryQuestions)>0: 
        questionCount.fill=None
        questionCountDisplay.fill=None
        retryPage.visible=True                        
    # gives user second chance to answer questions after retry page is displayed
    elif questionCount.value>11 and len(retryQuestions)>0:
        return questionPage(retryQuestions[0])    
    # brings user to post-quiz page and saves score if quiz and retry attempt are complete(if necessary)
    else:                                          
        questionCountDisplay.visible=False
        questionCount.visible=False
        postQuiz.visible=True                     
        quizAttempts.append(score.value)          
        scoreDisplayProperties(20, 215, 150, 350) 
        scoreGroup.centerX=200
        questionCount.value=0

# highlights actions and answer options in gold if user hovers mouse over them    
def onMouseMove(mouseX, mouseY):                  
    actions=[startQuiz, viewAttempts, quit1, redoQuiz, viewAnswers, mainMenu, quit]
    for index in range(7):
        if actions[index].hits(mouseX, mouseY):             
            actions[index].fill='gold'                            
        else:
            actions[index].fill='midnightBlue'         
    for index in range(4):
        if blocksListMC[index].hits(mouseX, mouseY):              
            blocksListMC[index].border='gold'                        
        else:
            blocksListMC[index].border='black'
    for index in range(2):
        if blocksTF[index].hits(mouseX, mouseY):                 
            blocksTF[index].border='gold'                        
        else:
            blocksTF[index].border='black'

def onMousePress(mouseX, mouseY):
    if mainPage.visible==True:
        mainMenuActions(mouseX, mouseY)
    elif postQuiz.visible==True:
        postQuizActions(mouseX, mouseY)
    elif retryPage.visible==False and questionCountDisplay.visible==True:
        answerSelection(mouseX,mouseY)
    else:
        pass

### Main Page (opening screen)
app.background = 'midnightBlue'
title = Label("EH Genetics Quiz", 200, 50, size=30, bold=True, fill='lightCyan')
menuShape = Rect(100, 139, 200, 176, fill='cornflowerBlue', border='black')
menu = Label("Main Menu", 200, 168, size=25, fill='midnightBlue', bold=True)
startQuiz = Label("1. Start Quiz ", 200, 205, size=20, fill='midnightBlue')
startQuiz.left = 128
viewAttempts = Label("2. View attempts", 200, 245, size=20, fill='midnightBlue')
viewAttempts.left = 128
quit1 = Label("3. Quit", 200, 285, size=20, fill='midnightBlue')
quit1.left=128
instructions1 = Label("Please select (click on) one of the actions below.", 200, 100, size=17, fill='cornflowerBlue')
mainPage = Group(title, menuShape, menu, startQuiz, viewAttempts, quit1, instructions1)

### Score
scoreDisplay = Label("Score: ", 180, 350, size=20, fill='gold')
score = Label(0, 200, 350, size=20, fill='gold')
score.left=215
scoreGroup = Group(scoreDisplay, score)
scoreGroup.centerX=200

### View Attempts Page
viewAttemptsShape = Rect(15,55,370,300, fill=None, border='gold', visible=False)
quizAttempts = []
attemptDisplay = []
viewAttemptsHeader = Label("Previous Attempts", 200, 30, size=25, bold=True, visible=False, fill='lightCyan')
pressBackspace = Label("Press backspace to go back.", 200, 375, size=15, visible=False, fill='lightCyan')

### General Quiz Page
quizTitle = Label("Genetics Quiz", 200, 40, size=22, bold=True, visible=False, fill='lightCyan')
questionCount = Label(1, 200, 380, size=15, visible=False, fill='lightCyan')
questionCount.right= 340
questionDisplay = Label("", 200, 112, size=21, fill='lightCyan')
questionCountDisplay = Label(" / 10", 200, 380, size=15, visible=False, fill='lightCyan')
questionCountDisplay.right=374

### Correct Page
pointsDisplay=Label('', 200, 210, size=20)
correct = Group(Rect(0, 0, 400, 400, fill='forestGreen'), Label("Correct!", 200, 170, size=50), pointsDisplay, Label("Press enter to continue.", 200, 270, size=18), visible=False)

### Incorrect Page
incorrect =  Group(Rect(0, 0, 400, 400, fill=rgb(210, 4, 45)),
Label("Incorrect!", 200, 170, size=50), 
Label("Press enter to continue.", 200, 240, size=18), visible=False)

### Retry Questions Page
retryAttempt = Label('', 100, 100, fill=None, visible=False)
retryQuestions = []
retryInfo = Label("Retry some questions for extra points!", 200, 185, size=20, fill='lightCyan')
retryInstructions = Label("Press enter to continue", 200, 215, size=15, fill='cornflowerBlue')
retryPage=Group(retryInfo, retryInstructions,visible=False)

### Multiple Choice (MC) Questions Page
blockA = Rect(25, 170, 350, 40, fill='cornflowerBlue', border='black', opacity=90)
blockB = Rect(25, 220, 350, 40, fill='cadetBlue', border='black', opacity=90)
blockC = Rect(25, 270, 350, 40, fill='steelBlue', border='black', opacity=90)
blockD = Rect(25, 320, 350, 40, fill='royalBlue', border='black', opacity=90)
answerA = Label("", 200, 190, size=18, fill='white')
answerB = Label("", 200, 240, size=18, fill='white')
answerC = Label("", 200, 290, size=18, fill='white')
answerD = Label("", 200, 340, size=18, fill='white') 
blocksGroupedMC = Group(blockA, blockB, blockC, blockD, visible=False)
blocksListMC = [blockA, blockB, blockC, blockD]
textGroupedMC = Group(answerA, answerB, answerC, answerD, visible=False)

### True or False (TF) Questions Page
blockT = Circle(105,255,85, fill='green', border='black')
TrueOption = Label("True", 105, 255, size=30)
blockF = Circle(295,255,85, fill=rgb(210, 4, 45), border='black')
FalseOption = Label("False", 295, 255, size=30)
TrueOrFalsePage = Group(blockT, blockF, TrueOption, FalseOption, visible=False)
blocksTF = [blockT, blockF]

### Genetics Quiz Questions
# MC options (for first 5 questions)
geneticOptions1 = ["A change in the DNA sequence", "Something that makes you stronger","A repeating unit of DNA",  "The order of the bases in DNA"]
geneticOptions2 = ["Dextrose", "Diatase", "Dextrin", "Deoxyribose"]
geneticOptions3 = [3, 4, 5, 6]
geneticOptions4 = ["Double Helix", "Spiral", "Ladder", "None of the above"]
geneticOptions5 = ["The backbone of DNA", "The chemical bond between the bases", "The building block of nucleic acids", "A nitrogenous base"]
# Quiz Questions
geneticsQ1 = ["1. What is a mutation?", blockA, geneticOptions1, "MC"]
geneticsQ2 = ["2. What is the sugar in DNA called?", blockD, geneticOptions2, "MC"]
geneticsQ3 = ["3. How many bases are there in DNA?", blockB, geneticOptions3, "MC"]
geneticsQ4 = ["4. What is the shape of DNA?", blockA, geneticOptions4, "MC"]
geneticsQ5 = ["5. What's a nucleotide?", blockC, geneticOptions5, "MC"]
geneticsQ6 = ["6. The base uracil is present in DNA.", blockF, "N/A", "True/False"]
geneticsQ7 = ["7. Colour blindness is a sex-linked trait.", blockT, "N/A", "True/False"]
geneticsQ8 = ["8. DNA is read to make proteins.", blockF, "N/A", "True/False"]
geneticsQ9 = ["9. Mendeleev is the father of genetics.", blockF, "N/A", "True/False"]
geneticsQ10 = ["10. Pink carnations show co-dominance.", blockF, "N/A", "True/False"]
questionsList = [geneticsQ1, geneticsQ2, geneticsQ3, geneticsQ4, geneticsQ5, geneticsQ6, geneticsQ7, geneticsQ8, geneticsQ9, geneticsQ10]
answersList = ["A change in the DNA sequence", "Deoxyribose", 4, "Double Helix", "The building block of nucleic acids", "False", "True", "False", "False", "False"]

### Post-Quiz Page
congrats = Label("Congratulations!", 200, 100, fill='gold', size=18, visible=False, bold=True)
quizComplete = Label("You've completed the quiz.", 200, 127.5, fill='cornflowerBlue', size=16, visible=False)
postQuizInstructions = Label("Please select (click on) one of the following actions.", 200, 155, fill='cornflowerBlue', size=15, visible=False)
postQuizShape = Rect(110, 185, 180, 150, fill='cornflowerBlue', visible=False, border='black')
redoQuiz = Label("1. Redo Quiz", 200, 215, size=20)
viewAnswers = Label("2. View Answers", 200, 245, size=20)
mainMenu = Label("3. Main Menu", 200, 275, size=20)
quit = Label("4. Quit", 200, 305, size=20)
redoQuiz.left = 130
viewAnswers.left = 130
mainMenu.left = 130
quit.left = 130
percent = Label("%", 100, 200, fill='gold', size=20, visible=False)
percent.left=score.centerX + 20
postQuiz = Group(percent, quizComplete, congrats, postQuizInstructions, postQuizShape, redoQuiz, viewAnswers, mainMenu, quit, visible=False)
postQuiz.centerX = 200
postQuiz.centerY = 200
percent.centerY=350

### View Answers Page
viewAnswersHeader = Label("Answers", 200, 30, size=22, bold=True, visible=False, fill='lightCyan')
lineGroup = Group(Line(0, 54, 400, 54, fill='gold', lineWidth=1, dashes=True), Line(0, 362, 400, 362, fill='gold', lineWidth=1, dashes=True), visible=False)
viewAnswerDisplay = []
for i in range(10):
    viewAnswerDisplay.append (Label(questionsList[i][0]+" "+str(answersList[i]), 200, 75+i*30, size=14, fill='lightCyan', visible=False))

cmu_graphics.run()