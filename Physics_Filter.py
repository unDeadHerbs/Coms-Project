#!/usr/bin/python3

"""Filters out and cleans up suspicious/noisy data from a stream."""

import time
import Leap
import itertools
import numpy

#TODO:
# - [x] test out how tuples work or ask murray
#   Tuples act the same as C++ vectors for the most part (they have some extra features)
#   For an example
#   >>> tup = ("cat", "hat", "bat")
#   >>> x,y,z = tup
#   >>> print(y)
#   'hat'
#   >>> for v in tup:
#   ...     print("it's a",v)
#   ...
#   "it's a cat"
#   "it's a hat"
#   "it's a bat"
#   # end example
# - [ ] ask murray a lot of questions about python in general
# - [x] ensure that we're saving actual values rather than pointers from the Leap to ensure data isn't lost
#   Generaly python dosen't have pointers and values, it has a diffrent divide.
#   We don't have to wory about it until it dose something wrong, then we'll get some code for deep copying.
# - [ ] fix possible syntax errors
# - [ ] clean up code
#   I'm going to let you change the code over more to pure maths before I make any comments here.
#   The general jist of it is, you're making a function that takes a frame and
#           validates it, some persistant variables are expected.
#   But working on the maths is more important than the code at the moment.
#           (Also we don't have any sample data to test with yet.)
# - [ ] finish up Kalman Filter Implementation
# - [ ] feed it data and plot to see if it works the way we want it to
# - [ ] stop thinking in terms of C++

class PhysicsFilter:
    
    def getVar(self, dataset):
        return sqrt(numpy.apply_over_axes(numpy.std,dataset))
    
    # NOTE:
    # sample data to get process variance and sensor variance of position, velocity, and acceleration
    # keep her hand as still as she can get -sensor variance
    # get her to spell her name -process variance
    
    def getCovarxva(self, positionData, velocityData, accelerationData):
        positionCovar = getVar(positionData)
        velocityCovar = getVar(velocityData)
        accelerationCovar = getVar(accelerationData)
        return numpy.diag([positionCovar, velocityCovar, accelerationCovar])
    
    # NOTE:
    # create for process and sensor noise
    
    def getCovarxv(self, positionData, velocityData):
        positionCovar = getVar(positionData)
        velocityCovar = getVar(velocityData)
        return numpy.diag([positionCovar, velocityCovar])
    
    
    def predictxva(self, stateVectors, deltaT): 
        stateVectors = numpy.reshape(stateVectors, (3, 1)) 
        stateTransition = numpy.matrix('1, deltaT, deltaT^2; 0, 1, deltaT; 0, 0, 1') 
        return stateTransition*stateVector
    
    # NOTE: 
    # Must order the stateVector in position, velocity, acceleration for this model 
    # stateVector = [[position],
    #                [velocity],
    #                [acceleration]]
    # stateTransition = [[1, deltaT, deltaT^2],
    #                    [0,      1,   deltaT],
    #                    [0,      0,        1]]
    # Another translation of the maths above
    # stateVector         stateTransition
    # position_k        : position_(k-1) + velocity_(k-1)*deltaT + acceleration_(k-1)*deltaT^2
    # velocity_k        :                  velocity_(k-1)        + acceleration_(k-1)*deltaT
    # acceleration_k    :                                          acceleration_(k-1)
    
    # TODO: 
    # Make this code tuple friendly
    # We might have to initialize the stateTransition as this:
    # stateTransition = [[(1,1,1), (deltaT,deltaT,deltaT), (deltaT^2,deltaT^2,deltaT^2)],
    #                    [(0,0,0), (1,1,1), (deltaT,deltaT,deltaT)],
    #                    [(0,0,0), (0,0,0), (1,1,1)]]
       
    def predictxv(self, stateVectors, deltaT):
        stateVectors = numpy.reshape(stateVectors,(2,1))
        stateTransition = numpy.matrix('1, deltaT; 0, 1')
        return stateTransition*stateVector

    # NOTE: 
    # Must order the stateVector in position and velocity for this model
    # stateVector = [[position],
    #                [velocity]]
    # stateTransition = [[1, deltaT],
    #                    [0,      1]]
    # Another translation of the maths above
    # stateVector         stateTransition
    # position_k        : position_(k-1) + velocity_(k-1)*deltaT
    # velocity_k        :                  velocity_(k-1)
    
    # TODO:
    # Make this code tuple friendly
    
    def updatexva(self, stateVectors, stateCovar, deltaT):
        

    def setPalmOrigin(self, palm_position, dataset):
        for data in dataset:
            dataset = dataset - palm_position
        return dataset
    
    def controlLimit(self, numPoints, threshold):
        
        dataset = numpy.zeros(numPoints)
        
        for data in dataset:                                               #samples data points from Leap Controller
            dataset[data] = controller.frame().hand.palm_velocity          #only evaluates palm_velocity
            
            while(dataset[data]==controller.frame()):                      #wait until next frame
                time.sleep(0.02)
        
        dataset_filtered = itertools.ifilterfalse(NaN, dataset)            #remove data point if NaN
        data_filtered = numpy.array(dataset_filterd)
        
        mean = numpy.apply_over_axes(numpy.mean, data_filtered, (1,2,3))
        stdDev = numpy.apply_over_axes(numpy.std, data_filtered, (1,2,3))
                                                                           #remove possible outliers
        dataset_norm = [(x,y,z) for (x,y,z) in dataset_filtered 
                        if (((x,y,z) > mean - threshold*stdDev) & 
                            ((x,y,z) < mean + threshold*stdDev))]
        
        mean_norm = numpy.apply_over_axes(numpy.mean, data_norm, (1,2,3))  #normalize everything
        stdDev_norm = numpy.apply_over_axes(numpy.std, data_norm, (1,2,3))
        
        controlLimit = mean_norm + threshold*stdDev_norm
        
        return controlLimit
    
        #LOGIC: controlLimit determines the behavior of the palm of the hand as it hovers over the Leap sensors and returns controlLimit
        #       If palm_velocity is less than the controlLimit, the user is hovering her hand over the Leap.
        #       palm_velocity was chosen because it is a value that does not rely on initial position in space or change in time
        #TODO:  correct possible syntax errors. some of the syntax may be incorrect as palm_velocity is a tuple
        #       fine tune threshold. some movements in ASL may accidentally be filtered out if threshold is too low
        #NOTE:  threshold corresponds with z score in statistics. 1.645 corresponds with 95%
        
    def EulFilter(self, controlLimit, previousHand):                      #EulFilter pronounced "Oil Filter"
        
        currentFrame = controller.frame()
        currentHand = frame.hand
        
        if currentHand.is_valid:
            
            if currentHand.palm_velocity < controlLimit:                  #if data seems reasonable, keep it
                previousHand.palm_velocity = currentHand.palm_velocity
                previousHand.timestamp = currentFrame.timestamp
                previousHand.palm_position = currentHand.palm_position
                
                fingers = currentHand.fingers
                
                for finger in fingers:
                    previousHand.finger.tip_position = finger.tip_position
                    previousHand.finger.tip_velocity = finger.tip_velocity
                    
                #add other data points you'd like to keep here
                
                previousHand.is_valid = currentHand.is_valid
                
                return previousHand
            
            elif previousHand.is_valid:                                   #hand is moving erratically and previous data is usable
                
                #extrapolate position using previously measured velocities, assume previously measured velocity remains constant
                
                deltaT = (currentFrame.timestamp - previousHand.timestamp)*0.000001
                #convert from microseconds to seconds because velocity is given as millimeters per second
                
                previousHand.palm_position = previousHand.palm_position + deltaT*previousHand.palm_velocity
                
                fingers = previousHand.fingers
                
                for finger in fingers:
                    finger.tip_position = finger.tip_position + deltaT*finger.tip_velocity
                    
                #add other data points you'd like to update here
                
                return previousHand
            
            else:                                                        #hand is moving erratically and previous data is not usable
                
                #evaluate the good ole fashioned way
                
                index = 0
                
                while(index < 2):
                    
                    while(~controller.frame().hand.is_valid):            #gather some valid frames, this is probably where the hand is
                        time.sleep(0.02)
                        
                    frame[index] = controller.frame()
                    hand[index] = frame[index].hand
                    index += 1
                    
                #average all the frames' data
                previousHand.timestamp = (frame[1].timestamp + frame[0].timestamp + currentFrame.timestamp)/3
                
                #math up the rest of the variables of previousHand, there's probably a better way to do this
                
                previousHand.is_valid = True 
                
                return previousHand
            
        else:                                                            #hand is not on screen, flag as invalid
            previousHand.is_valid = currentHand.is_valid
            
            return previousHand
        
        #LOGIC: filter helps filter out noise and makes educated guesses about hand movement
        #       filter assumes that user is intentionally hovering hand over Leap if palm_velocity is less than controlLimit
        #       filter dampens movement if palm_velocity is greater than controlLimit
        #       if data seems reasonable, keep it. if not, make up some numbers. if there's no hand, data is invalid
        #TODO:  correct possible syntax errors as some values may be tuples
        #       establish a better procedure for invalid cases, something doesn't feel right
        #NOTE:  euler method is considered as it requires only the position and velocity of previous data point to create a prediction
        #       quicker and less memory extensive although not as reliable as there's no true feedback system
        #       from my readings of kalman filter thus far, designing it for this scenario may be similar to euler with a statistics
        
    class previousHand:
        
        def __init__(self):
            self.timestamp
            self.palm_position
            self.is_valid
                
            #aaaaand the rest
                
        #TODO:  make it like the Leap's Hand class. ask murray how this stuff works
    
    class predictedHand:
    
        def __init__(self):
            self.timestamp
            self.palm_position
            self.is_valid
            
            #aaaaand the rest
        
        #TODO:  make it like the Leap's Hand class. ask murray how this stuff works
        
    def StatsFilter(self, numFrames, previousHand):                    #Statistical Filter Implementation
        
        index = 0
        
        while(index < numFrames):                                      #grab a lot of frames
            frame[index] = controller.frame((numFrames - index))
            hand[index] = frame[index].hand
            index += 1
        
        if (sizeof(itertools.ifilterfalse(hand.is_valid, hand[index]) > 0):
        #if one of those frames don't contain a hand, flag as invalid
            previousHand.is_valid = False
            
            return previousHand
            
        else: 
            #average out all the important stuff and save into previousHand
            previousHand.palm_velocity = numpy.apply_over_axis(numpy.mean, hand.palm_velocity, (1,2,3))
            previousHand.palm_position = numpy.apply_over_axis(numpy.mean, hand.palm_position, (1,2,3))
            
            #do this for all the data points
            
            return previousHand
            
        #LOGIC: filter helps filter out noise and approximates hand position for a given time frame
        #       filter assumes that if at any point in the sample time frame the hand is not on screen, it is invalid
        #TODO:  all of the code essentially
        #NOTE:  StatsFilter is memory extensive, requires a lot of calculations and may lag but can potentially be most accurate
            
    def KalFilter(self, currentHand, previousHand, predictedHand):
        
        xk = numpy.matrix('positionk, velocityk')
        transitionMatrix = numpy.matrix('1, deltaT; 0, 1')
            #predict position = previous position + deltaT previous velocity and velocity remains constant
        
        #residuals = abs(predictedHand - currentHand)
        #covariance noise = sqrt(predictedHand.stdDev - currentHand.stdDev)
        #model will be based on x(t) + v(t) or x(t) + x'(t) as only velocity and position is readily available
        
        #k+1 is our predictedHand
        #k is our currentHand or observedHand
        #k-1 is our previousHand
            
            return previousHand, predictedHand
            
        #LOGIC: filter helps filter out noise and approximates hand position for a sample time frame
        #       filter compares predicted outcome with actual outcome then determines kalman filter variables to use in the next iteration
        #TODO:  ask murray if function can return more than 1 variable
        #       figure out how to code all this and do all of the code essentially
        #NOTE:  KalFilter uses the similar logic as Euler method in terms of predicting the outcome
        #       KalFilter differs from EulFilter as it takes feedback into consideration