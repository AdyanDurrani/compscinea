import cv2 as cv
import apriltag
import pygame
from urllib.request import urlopen
import numpy as np

def url_to_image(url, readFlag=cv.IMREAD_COLOR):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv.imdecode(image, readFlag)

    # return the image
    return image

cat = url_to_image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9jXOE7IX7YnKW_OZtFe9yo1qEOdfxoP7gsw&s')
# pygame setup
pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
running = True

font = pygame.font.SysFont("copperplategothic", 20, True, True)

cat= cv.resize(cat,(200,300))


nut_id = 10
bridge_id = 11
scale_len = 25

# setup the detector
detector = apriltag.Detector()

#Recieves a videocapture from camera 0
cap = cv.VideoCapture(0)

#Tabs for the song
f = open("songs.txt")

E = "E"
A = "A"
D = "D"
G = "G"
B = "B"
e = "e"

songs= [["Smoke on the Water - Deep Purple", [0,3,5,0,3,6,5,0,3,5,3,0], [E,E,E,E,E,E,E,E,E,E,E,E]],
        ["Buddy Holly - Weezer"], [4,5,4,6,8,6,4,5,4], [e,B,e,e,e,e,B,B]]


#Starting note
n=0

def get_tag_distance(nut, bridge):
    #Checks if the tags exist
    if bridge and nut:
    #Loads tag coordinates into variables
        locationnut = nut.corners[0]
        locationbridge = bridge.corners[1]
        distancex = locationnut[0] - locationbridge[0]
        distancey = locationnut[1] - locationbridge[1]
        return (locationnut[0],locationnut[1]), (locationbridge[0], locationbridge[1]), distancex, distancey

    else:
        return None


def dist_of_fret(scale_len, fret):
	return scale_len / (2 ** (fret/12) )

#Checks if the camera can be opened
if not cap.isOpened():
    print("Camera not being read")
    exit()

running = True

#Main loop
while running:

    mouse_pos = pygame.mouse.get_pos()

    #reads cam
    ret, image = cap.read()
    image = cv.imread(cv.samples.findFile("guitarfixed.jpg"))
    #converts image to greyscale.
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    #Detector looks for April tags in grey image
    detections = detector.detect(gray)


    #Checks if camera is readable
    if not ret:
        print("can not read camera.")
        break
    
    else:
	    # iterate through each tag detected    
        for detect in detections:
            #store top left coordinates
            topleftx = detect.corners[0][0]
            toplefty = detect.corners[0][1]
            #draw a circle at the top left
            image = cv.circle(image,(int(topleftx), int(toplefty)), 20, (0,0,255), -1)

    if len(detections) == 2:
        if detections[0].tag_id == nut_id:
            nutmarker = detections[0]
            bridgemarker = detections[1]
        else:
            nutmarker = detections[1]
            bridgemarker = detections[0]

        locationnut,locationbridge, distancex, distancey = (get_tag_distance(nutmarker, bridgemarker))
       
       #fret number is now the note number of the song
        distance = dist_of_fret(distancex, songs[0][1][n])


        #Draws a circle on the correct fret
        image = cv.circle(image,(int(locationbridge[0]+distance+30), int(locationbridge[1])), 5, (0,255,255), -1)

        #Adds text saying which fret to play
        image = cv.putText(image, f'fret: {songs[0][1][n]}', (0,30), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv.LINE_AA)
	    #Adds text saying which string to play
        image = cv.putText(image, f'string: {songs[0][2][n]}', (0,60), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv.LINE_AA)

    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #If when the mouse is clicked and mouse is in the box run the code
            if next.collidepoint(mouse_pos):
                #Increments the note
                n+=1
                #If the end of the song was reached, loop back
                if n == len(songs[0][1]):
                    n=0

            elif prev.collidepoint(mouse_pos):
                #decrements the note
                n-=1
                #if reversed all the way to the start of the song, keep it there
                if n == -1:
                    n = 0
            


    # fill the screen with a color to wipe away anything from last frame
    screen.fill("Orange")

    #Draws the next button
    next = pygame.Rect(150,50,50,50)

    pygame.draw.rect(screen, "Red", next)
    screen.blit(font.render("Next ->", True, (0,0,0)), (150,50), )

    #Draws the previous button
    prev = pygame.Rect(50,50,75,50)

    pygame.draw.rect(screen, "Red", prev)
    screen.blit(font.render("<- Previous", True, (0,0,0)), (50,50))

    #Change the colour of the button when hovered over
    if prev.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (100,0,0), prev)
        screen.blit(font.render("<- Previous", True, (0,0,0)), (50,50), )    

    elif next.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (100,0,0), next)
        screen.blit(font.render("Next ->", True, (0,0,0)), (150,50), )
    
    #screen.blit(font.render(f"Fret: {songs[0][1][n]}", False, (0,0,0)), (50,200), )
    #screen.blit(font.render(f"String: {songs[0][2][n]}", False, (0,0,0)), (50,200), )


    # flip() the display to put your work on screen
    pygame.display.flip()

    

    #image = cv.flip(image,1)
    #width = image.shape[1]

    #image[0:100, width-100:width] = cat[0:100, 0:100]
    #Displays the camera feed
    cv.imshow('Result', image)



#stops recieving cam feed
cap.release()
#closes all windows
cv.destroyAllWindows()
