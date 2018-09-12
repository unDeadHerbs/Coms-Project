import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import csv

letter = ''

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Motion Sensor Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Motion Sensor Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        #create letter identifier for data spreadsheet
        def LetterToVector(letter):
            v=[0]*26
            v[ord(letter)-ord("a")]=1
            return v
        a1 = LetterToVector("a")
        b1 = LetterToVector("b")
        c1 = LetterToVector("c")
        d1 = LetterToVector("d")
        e1 = LetterToVector("e")
        f1 = LetterToVector("f")
        g1 = LetterToVector("g")
        h1 = LetterToVector("h")
        i1 = LetterToVector("i")
        j1 = LetterToVector("j")
        k1 = LetterToVector("k")
        l1 = LetterToVector("l")
        m1 = LetterToVector("m")
        n1 = LetterToVector("n")
        o1 = LetterToVector("o")
        p1 = LetterToVector("p")
        q1 = LetterToVector("q")
        r1 = LetterToVector("r")
        s1 = LetterToVector("s")
        t1 = LetterToVector("t")
        u1 = LetterToVector("u")
        v1 = LetterToVector("v")
        w1 = LetterToVector("w")
        x1 = LetterToVector("x")
        y1 = LetterToVector("y")
        z1 = LetterToVector("z")


        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            print "  %s, id %d, positionx: %s, positiony: %s, positionz: %s" % (
                handType, hand.id, hand.palm_position.x, hand.palm_position.y, hand.palm_position.z)

            # Get the hand's normal vector, direction, and position
            normal = hand.palm_normal
            direction = hand.direction
            hand_center = hand.palm_position

            #create data list
            data =[]
        
            #open csv file to write to
            with open('data.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',')

                # Get fingers
                for finger in hand.fingers:
                    print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                        self.finger_names[finger.type],
                        finger.id,
                        finger.length,
                        finger.width)

                    # Get bones
                    for b in range(0, 4):
                        bone = finger.bone(b)
                        #subtract bone vector from palm vector
                        vectorx = bone.next_joint.x - hand_center.x
                        vectory = bone.next_joint.y - hand_center.y
                        vectorz = bone.next_joint.z - hand_center.z

                        #printing for our use
                        print "      Bone: %s, vectorx: %s, vectory: %s, vectorz: %s" % (
                            self.bone_names[bone.type],
                            vectorx,
                            vectory,
                            vectorz)

                        #add new vectors to data list
                        data.append(vectorx)
                        data.append(vectory)
                        data.append(vectorz)

                #adds the letter list to the end of the data list
                print "letter equals: %s" % (letter)
                if (letter == 'a\r'):
                    data.extend(a1)
                elif (letter == 'b\r'):
                    data.extend(b1)
                elif (letter == 'c\r'):
                    data.extend(c1)
                elif (letter == 'd\r'):
                    data.extend(d1)
                elif (letter == 'e\r'):
                    data.extend(e1)
                elif (letter == 'f\r'):
                    data.extend(f1)
                elif (letter == 'g\r'):
                    data.extend(g1)
                elif (letter == 'h\r'):
                    data.extend(h1)
                elif (letter == 'i\r'):
                    data.extend(i1)
                elif (letter == 'j\r'):
                    data.extend(j1)
                elif (letter == 'k\r'):
                    data.extend(k1)
                elif (letter == 'l\r'):
                    data.extend(l1)
                elif (letter == 'm\r'):
                    data.extend(m1)
                elif (letter == 'n\r'):
                    data.extend(n1)
                elif (letter == 'o\r'):
                    data.extend(o1)
                elif (letter == 'p\r'):
                    data.extend(p1)
                elif (letter == 'q\r'):
                    data.extend(q1)
                elif (letter == 'r\r'):
                    data.extend(r1)
                elif (letter == 's\r'):
                    data.extend(s1)
                elif (letter == 't\r'):
                    data.extend(t1)
                elif (letter == 'u\r'):
                    data.extend(u1)
                elif (letter == 'v\r'):
                    data.extend(v1)
                elif (letter == 'w\r'):
                    data.extend(w1)
                elif (letter == 'x\r'):
                    data.extend(x1)
                elif (letter == 'y\r'):
                    data.extend(y1)
                elif (letter == 'z\r'):
                    data.extend(z1)
                else:
                    print "Character is undefined."
                    



                print "     Data: %s" % (data)   
                writer.writerow(data)
                    
    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
    
def start():
    # Takes in starting inputs
    global letter
    letter = str(raw_input("Input letter:"))
    print (letter, type(letter))
    raw_input("Press enter to start.")

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    start()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
