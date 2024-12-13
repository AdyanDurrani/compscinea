import cv2 as cv
import apriltag
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True



nut_id = 10
bridge_id = 11
scale_len = 25

# setup the detector
detector = apriltag.Detector()

#Recieves a videocapture from camera 0
cap = cv.VideoCapture(0)

#Tabs for the song
song = [[0,3,5,0,3,6,5,0,3,5,3,0],["E","E","E","E","E","E","E","E","E","E","E","E"]]
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
    #reads cam
    ret, image = cap.read()
    #image = cv.imread(cv.samples.findFile("guitarfixed.jpg"))
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
        distance = dist_of_fret(distancex, song[0][n])


        #Draws a circle on the correct fret
        image = cv.circle(image,(int(locationbridge[0]+distance+30), int(locationbridge[1])), 5, (0,255,255), -1)

        #Adds text saying which fret to play
        image = cv.putText(image, f'fret: {song[0][n]}', (0,30), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv.LINE_AA)
	    #Adds text saying which string to play
        image = cv.putText(image, f'string: {song[1][n]}', (0,60), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv.LINE_AA)

    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button.collidepoint(mouse_pos):
                print("Booty cheeks")
                n+=1
    

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("Orange")

    # RENDER YOUR GAME HERE
    button = pygame.Rect(50,50,50,50)
    pygame.draw.rect(screen, "Red", button)
    # flip() the display to put your work on screen
    pygame.display.flip()

    mouse_pos = pygame.mouse.get_pos()

    #image = cv.flip(image,1)

    #Displays the camera feed
    cv.imshow('Result', image)


    clock.tick(60)  # limits FPS to 60

#stops recieving cam feed
cap.release()
#closes all windows
cv.destroyAllWindows()
