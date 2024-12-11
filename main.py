import cv2 as cv
import apriltag

nut_id = 10
bridge_id = 11
scale_len = 25

# setup the detector
detector = apriltag.Detector()

#Recieves a videocapture from camera 0
cap = cv.VideoCapture(0)

#Tabs for the song
song = [0,3,5,0,3,6,5,0,3,5,3,0]
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

#Main loop
while True:
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
        distance = dist_of_fret(distancex, song[n])


        #Draws a circle on the correct fret
        image = cv.circle(image,(int(locationbridge[0]+distance+30), int(locationbridge[1])), 5, (0,255,255), -1)



    
    #image = cv.flip(image,1)

    #Displays the camera feed
    cv.imshow('Result', image)

    #exits when keyboard "q" is pressed
    if cv.waitKey(0) == ord("q"):
        break
    #advances the song if keyboard "a" is pressed
    elif cv.waitKey() == ord("a"):
        n+=1
    

#stops recieving cam feed
cap.release()
#closes all windows
cv.destroyAllWindows()
