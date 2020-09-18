import parselmouth
import math

def calcJitter(soundPath,fromTime,toTime,shortestPeriod, longestPeriod, maximumPeriodFactor):
    sound = parselmouth.Sound(soundPath)
    pitch = sound.to_pitch()
    pulses = parselmouth.praat.call([sound, pitch],"To PointProcess (cc)")
    n_pulse = parselmouth.praat.call(pulses, "Get number of points")
    numOfPulsesUse = n_pulse
    SumT = 0 

    for i in range(2,n_pulse - 1):
        Ti = parselmouth.praat.call(pulses,"Get time from index", i - 1)
        Ti1 = parselmouth.praat.call(pulses,"Get time from index", i)
        Ti2= parselmouth.praat.call(pulses,"Get time from index", i + 1)

        dT1 = Ti1 - Ti  #duration of interval at point i - 1 
        dT2 = Ti2 - Ti1 #duration of interval at point i
        
        if ((dT1) > shortestPeriod and (dT1) < longestPeriod) and ((dT1/dT2)<maximumPeriodFactor and (dT2/dT1)<maximumPeriodFactor):
                SumT = SumT + dT1 
        else:
            numOfPulsesUse = numOfPulsesUse - 1
        if numOfPulsesUse < 2:
            return 'Undefined'

    jitLocalAbs = calJitLocalAbs(soundPath,fromTime,toTime,shortestPeriod,longestPeriod,maximumPeriodFactor)
    meanPeriod = SumT/numOfPulsesUse
        
    jitLocal = (jitLocalAbs/meanPeriod)*100
    
    return jitLocal

def calJitLocalAbs(soundPath,fromTime,toTime,shortestPeriod, longestPeriod, maximumPeriodFactor):
    sound = parselmouth.Sound(soundPath)
    pitch = sound.to_pitch()
    pulses = parselmouth.praat.call([sound, pitch],"To PointProcess (cc)")
    n_pulse = parselmouth.praat.call(pulses, "Get number of points")
    numOfPulsesUse = n_pulse
    SumS = 0

    for i in range(2,n_pulse - 1):
        Ti = parselmouth.praat.call(pulses,"Get time from index", i - 1)
        Ti1 = parselmouth.praat.call(pulses,"Get time from index", i)
        Ti2= parselmouth.praat.call(pulses,"Get time from index", i + 1)

        dT1 = Ti1 - Ti
        dT2 = Ti2 - Ti1
        
        if ((dT1) > shortestPeriod and (dT1) < longestPeriod) and ((dT1/dT2)<maximumPeriodFactor and (dT2/dT1)<maximumPeriodFactor):
                if ((dT2) > 0.001 and (dT2) < 0.02):
                        SumS = SumS + abs(dT2 - dT1)
        else:
                numOfPulsesUse = numOfPulsesUse - 1

        if numOfPulsesUse < 2:
            return 'undefined'

    jitLocalAbs = SumS/(numOfPulsesUse-1)
        
    return jitLocalAbs

def calJitDDP(soundPath,fromTime,toTime,shortestPeriod, longestPeriod, maximumPeriodFactor):
    sound = parselmouth.Sound(soundPath)
    pitch = sound.to_pitch()
    pulses = parselmouth.praat.call([sound, pitch],"To PointProcess (cc)")
    n_pulse = parselmouth.praat.call(pulses, "Get number of points")
    numOfPulsesUse = n_pulse
    SumDDP = 0
    Sum = 0

    for i in range(2,n_pulse - 2):
        Ti = parselmouth.praat.call(pulses,"Get time from index", i - 1)
        Ti1 = parselmouth.praat.call(pulses,"Get time from index", i)
        Ti2= parselmouth.praat.call(pulses,"Get time from index", i + 1)
        Ti3= parselmouth.praat.call(pulses,"Get time from index", i + 2)

        dT1 = Ti1 - Ti
        dT2 = Ti2 - Ti1
        dT3 = Ti3 - Ti2

        Sum = Sum + dT1
        SumDDP = SumDDP + abs((dT3 - dT2) - (dT2 - dT1))


    absDDP = SumDDP/(numOfPulsesUse - 2)
    meanPeriod = Sum/numOfPulsesUse    

    jitDDP = absDDP/meanPeriod

    return jitDDP

def calJitppq5(soundPath,fromTime,toTime,shortestPeriod, longestPeriod, maximumPeriodFactor):
    sound = parselmouth.Sound(soundPath)
    pitch = sound.to_pitch()
    pulses = parselmouth.praat.call([sound, pitch],"To PointProcess (cc)")
    n_pulse = parselmouth.praat.call(pulses, "Get number of points")
    numOfPulsesUse = n_pulse
    Sumppq5 = 0
    Sum = 0

    for i in range(1,n_pulse - 5):  
        Ti = parselmouth.praat.call(pulses,"Get time from index", i)
        Ti1= parselmouth.praat.call(pulses,"Get time from index", i + 1)
        Ti2= parselmouth.praat.call(pulses,"Get time from index", i + 2)
        Ti3= parselmouth.praat.call(pulses,"Get time from index", i + 3)
        Ti4= parselmouth.praat.call(pulses,"Get time from index", i + 4)
        Ti5= parselmouth.praat.call(pulses,"Get time from index", i + 5)

        dT1 = Ti1 - Ti
        dT2 = Ti2 - Ti1
        dT3 = Ti3 - Ti2
        dT4 = Ti4 - Ti3
        dT5 = Ti5 - Ti4

        Sum = Sum + dT1
        Sumppq5 = Sumppq5 + abs(dT3 - (dT1 + dT2 + dT3 + dT4 + dT5)/5)

    absPPQ5 = Sumppq5/(numOfPulsesUse - 4)
    meanPeriod = Sum/numOfPulsesUse

    jitppq5 = absPPQ5/meanPeriod
    return jitppq5

def calJitRAP(soundPath,fromTime,toTime,shortestPeriod, longestPeriod, maximumPeriodFactor):
    sound = parselmouth.Sound(soundPath)
    pitch = sound.to_pitch()
    pulses = parselmouth.praat.call([sound, pitch],"To PointProcess (cc)")
    n_pulse = parselmouth.praat.call(pulses, "Get number of points")
    numOfPulsesUse = n_pulse
    SumAP = 0
    Sum = 0

    for i in range(2,n_pulse - 2):
        Ti = parselmouth.praat.call(pulses,"Get time from index", i - 1)
        Ti1 = parselmouth.praat.call(pulses,"Get time from index", i)
        Ti2= parselmouth.praat.call(pulses,"Get time from index", i + 1)
        Ti3= parselmouth.praat.call(pulses,"Get time from index", i + 2)

        dT1 = Ti1 - Ti
        dT2 = Ti2 - Ti1
        dT3 = Ti3 - Ti2

        Sum = Sum + dT1
        SumAP = SumAP + abs(dT2 - (dT1+dT2+ dT3)/3)

    absAP = SumAP/(numOfPulsesUse - 2)
    meanPeriod = Sum/numOfPulsesUse
   
    JitRAP = absAP/meanPeriod
    return JitRAP



def calcShimmerLocal(soundPath,fromTime,toTime,shortestPeriod,longestPeriod,maximumPeriodFactor,maximunAmplitudeFactor):
    sound = parselmouth.Sound(soundPath)
    pitch = sound.to_pitch()
    pulses = parselmouth.praat.call([sound, pitch],"To PointProcess (cc)")
    n_pulse = parselmouth.praat.call(pulses, "Get number of points")
    SumA = 0
    SumA1 = 0

    for i in range( 2, n_pulse):
        Ti = parselmouth.praat.call(pulses,"Get time from index", i - 1)
        Ti1 = parselmouth.praat.call(pulses,"Get time from index", i)
        Ti2 = parselmouth.praat.call(pulses,"Get time from index", i + 1)
        Aimax = parselmouth.praat.call(sound,"Get maximum...",Ti,Ti1,"Sinc70")
        Aimin = parselmouth.praat.call(sound,"Get minimum...",Ti,Ti1,"Sinc70") 
        Ai1max = parselmouth.praat.call(sound,"Get maximum...",Ti1,Ti2,"Sinc70")
        Ai1min = parselmouth.praat.call(sound,"Get minimum...",Ti1,Ti2,"Sinc70")
        Ai = 0
        Ai1 = 0 
        if(abs(Aimin)> Aimax):
                Ai = abs(Aimin)
        else:
                Ai = Aimax
        if(abs(Ai1min)>Aimax):
                Ai1 = abs(Ai1min)
        else:
                Ai1 = Ai1max
        SumA = SumA + abs(Ai - Ai1)
        SumA1 = SumA1 + Ai
        
    AvgSumA = SumA/(n_pulse - 1)
    AvgSumA1 = SumA1/n_pulse
    shimLocal = (AvgSumA/AvgSumA1)*100   
    return shimLocal

def calcShimmerLocaldb(soundPath,fromTime,toTime,shortestPeriod,longestPeriod,maximumPeriodFactor,maximunAmplitudeFactor):
    sound = parselmouth.Sound(soundPath)
    pitch = sound.to_pitch()
    pulses = parselmouth.praat.call([sound, pitch],"To PointProcess (cc)")
    n_pulse = parselmouth.praat.call(pulses, "Get number of points")
    ShdB = 0
    for i in range( 2, n_pulse - 1):
        Ti = parselmouth.praat.call(pulses,"Get time from index", i - 1)
        Ti1 = parselmouth.praat.call(pulses,"Get time from index", i)
        Ti2 = parselmouth.praat.call(pulses,"Get time from index", i + 1)
        Aimax = parselmouth.praat.call(sound,"Get maximum...",Ti,Ti1,"Sinc70")
        Aimin = parselmouth.praat.call(sound,"Get minimum...",Ti,Ti1,"Sinc70") 
        Ai1max = parselmouth.praat.call(sound,"Get maximum...",Ti1,Ti2,"Sinc70")
        Ai1min = parselmouth.praat.call(sound,"Get minimum...",Ti1,Ti2,"Sinc70")
        Ai = 0
        Ai1 = 0 
        
        if(abs(Aimin)> Aimax):
                Ai = abs(Aimin)
        else:
                Ai = Aimax
        if(abs(Ai1min)>Aimax):
                Ai1 = abs(Ai1min)
        else:
                Ai1 = Ai1max
        Avg = abs(Ai1/Ai)
        loga = math.log(Avg)        
        ShdB = ShdB + abs(20*loga)

    ShdB = ShdB/(n_pulse - 1)
    return ShdB

def calcShimmerAPQ3(soundPath,fromTime,toTime,shortestPeriod,longestPeriod,maximumPeriodFactor,maximunAmplitudeFactor):
    sound = parselmouth.Sound(soundPath)
    pitch = sound.to_pitch()
    pulses = parselmouth.praat.call([sound, pitch],"To PointProcess (cc)")
    n_pulse = parselmouth.praat.call(pulses, "Get number of points")
    numOfPulses = n_pulse
    SumAPQ3 = 0
    Sum = 0


    for i in range( 1, n_pulse - 3):
        Ti = parselmouth.praat.call(pulses,"Get time from index", i)
        Ti1 = parselmouth.praat.call(pulses,"Get time from index", i + 1)
        Ti2 = parselmouth.praat.call(pulses,"Get time from index", i + 2)
        Ti3 = parselmouth.praat.call(pulses,"Get time from index", i + 3)

        Aimax = parselmouth.praat.call(sound,"Get maximum...",Ti,Ti1,"Sinc70")
        Aimin = parselmouth.praat.call(sound,"Get minimum...",Ti,Ti1,"Sinc70") 
        Ai1max = parselmouth.praat.call(sound,"Get maximum...",Ti1,Ti2,"Sinc70")
        Ai1min = parselmouth.praat.call(sound,"Get minimum...",Ti1,Ti2,"Sinc70")
        Ai2max = parselmouth.praat.call(sound,"Get maximum...",Ti2,Ti3,"Sinc70")
        Ai2min = parselmouth.praat.call(sound,"Get minimum...",Ti2,Ti3,"Sinc70")

        Ai = Aimax
        Ai1 = Ai1max
        Ai2 = Ai2max

        SumAPQ3 = SumAPQ3 + abs(Ai1 - (Ai + Ai1 + Ai2)/3)
        Sum = Sum + Ai

    APQ3 = SumAPQ3/(numOfPulses - 1)
    meanPeriod = Sum/numOfPulses    

    ShAPQ3 = (APQ3/meanPeriod)*100
    return ShAPQ3

def calcShimmerAPQ5(soundPath,fromTime,toTime,shortestPeriod,longestPeriod,maximumPeriodFactor,maximunAmplitudeFactor):
    sound = parselmouth.Sound(soundPath)
    pitch = sound.to_pitch()
    pulses = parselmouth.praat.call([sound, pitch],"To PointProcess (cc)")
    n_pulse = parselmouth.praat.call(pulses, "Get number of points")
    numOfPulses = n_pulse
    SumAPQ5 = 0
    Sum = 0


    for i in range( 1, n_pulse - 5):
        Ti = parselmouth.praat.call(pulses,"Get time from index", i)
        Ti1 = parselmouth.praat.call(pulses,"Get time from index", i + 1)
        Ti2 = parselmouth.praat.call(pulses,"Get time from index", i + 2)
        Ti3 = parselmouth.praat.call(pulses,"Get time from index", i + 3)
        Ti4 = parselmouth.praat.call(pulses,"Get time from index", i + 4)
        Ti5 = parselmouth.praat.call(pulses,"Get time from index", i + 5)

        Aimax = parselmouth.praat.call(sound,"Get maximum...",Ti,Ti1,"Sinc70")
        Aimin = parselmouth.praat.call(sound,"Get minimum...",Ti,Ti1,"Sinc70") 
        Ai1max = parselmouth.praat.call(sound,"Get maximum...",Ti1,Ti2,"Sinc70")
        Ai1min = parselmouth.praat.call(sound,"Get minimum...",Ti1,Ti2,"Sinc70")
        Ai2max = parselmouth.praat.call(sound,"Get maximum...",Ti2,Ti3,"Sinc70")
        Ai2min = parselmouth.praat.call(sound,"Get minimum...",Ti2,Ti3,"Sinc70")
        Ai3max = parselmouth.praat.call(sound,"Get maximum...",Ti3,Ti4,"Sinc70")
        Ai3min = parselmouth.praat.call(sound,"Get minimum...",Ti3,Ti4,"Sinc70")
        Ai4max = parselmouth.praat.call(sound,"Get maximum...",Ti4,Ti5,"Sinc70")
        Ai4min = parselmouth.praat.call(sound,"Get minimum...",Ti4,Ti5,"Sinc70")

        Ai = Aimax
        Ai1 = Ai1max
        Ai2 = Ai2max
        Ai3 = Ai3max
        Ai4 = Ai4max

        SumAPQ5 = SumAPQ5 + abs(Ai2 - (Ai + Ai1 + Ai2 + Ai3 + Ai4)/5)
        Sum = Sum + Ai

    APQ5 = SumAPQ5/(numOfPulses - 1)
    meanPeriod = Sum/numOfPulses    

    ShAPQ5 = (APQ5/meanPeriod)*100
    return ShAPQ5

