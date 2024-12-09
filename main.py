import cv2 as cv
import apriltag

nut_id = 10
bridge_id = 11

# setup the detector
detector = apriltag.Detector()

#Recieves a videocapture from camera 0
cap = cv.VideoCapture(0)



def get_tag_distance(nut, bridge):
    #Checks if the tags exist
    if bridge and nut:
    #Loads tag coordinates into variables
        locationnut = nut.corners[0]
        locationbridge = bridge.corners[1]
        #Distance is calculated using pythagerous theorum 
        distance = (((locationnut[0] - locationbridge[0]) ** 2) + (locationnut[1] -locationbridge[1]) ** 2) ** 0.5
        return (locationnut[0],locationnut[1]), (locationbridge[0], locationbridge[1]), distance

    else:
        return None


#Checks if the camera can be opened
if not cap.isOpened():
    print("Camera not being read")
    exit()

#Main loop
while True:
    #reads cam
    ret, image = cap.read()
    image = cv.imread(cv.samples.findFile("guitar.jpg"))
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

        l1,l2,distance = (get_tag_distance(nutmarker, bridgemarker))
        
        cv.line(image,(int(l1[0]),int(l1[1])),(int(l2[0]), int(l2[1])),(255,0,0),5)

    
    image = cv.flip(image,1)

    #Displays the camera feed
    cv.imshow('Result', image)

    #exits when keyboard "q" is pressed
    if cv.waitKey(1) == ord("q"):
        break

#stops recieving cam feed
cap.release()
#closes all windows
cv.destroyAllWindows()
