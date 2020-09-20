import calcLibrary

soundPath = "E:\Project\Python calc\Sound Test\ormal1.mp3"
fromTime = 0
toTime = 0
shortestPeriod = 0.001
longestPeriod = 0.02
maximumPeriodFactor = 1.3
maximunAmplitudeFactor = 1.6

#Jitter
jitLocal = calcLibrary.calcJitter(soundPath,fromTime,toTime,shortestPeriod,longestPeriod,maximumPeriodFactor)
jitLocalAbs = calcLibrary.calJitLocalAbs(soundPath,fromTime,toTime,shortestPeriod,longestPeriod,maximumPeriodFactor)
jitRAP = calcLibrary.calJitRAP(soundPath,fromTime,toTime,shortestPeriod,longestPeriod,maximumPeriodFactor)
jitPPQ5 = calcLibrary.calJitppq5(soundPath,fromTime,toTime,shortestPeriod,longestPeriod,maximumPeriodFactor)
jitDDP = calcLibrary.calJitDDP(soundPath,fromTime,toTime,shortestPeriod,longestPeriod,maximumPeriodFactor)

#Shimmer
shimLocal = calcLibrary.calcShimmerLocal(soundPath,fromTime,toTime,shortestPeriod,longestPeriod,maximumPeriodFactor,maximunAmplitudeFactor)
shimDB = calcLibrary.calcShimmerLocaldb(soundPath,fromTime,toTime,shortestPeriod,longestPeriod,maximumPeriodFactor,maximunAmplitudeFactor)
ShimAPQ3 = calcLibrary.calcShimmerAPQ3(soundPath,fromTime,toTime,shortestPeriod,longestPeriod,maximumPeriodFactor,maximunAmplitudeFactor)
ShimAPQ5 = calcLibrary.calcShimmerAPQ5(soundPath,fromTime,toTime,shortestPeriod,longestPeriod,maximumPeriodFactor,maximunAmplitudeFactor)

print('Jitter (Local)=',jitLocal,' %')
print('Jitter (local, absolute) =',jitLocalAbs,' seconds')
print('Jitter (RAP)=',jitRAP,' %')
print('Jitter (PPQ5) =',jitPPQ5,' %')
print('Jitter (DDP)=',jitDDP,' %')
print('Shimmer (local) =',shimLocal,' %')
print('Shimmer (local, dB) =',shimDB,' dB')
print('Shimmer (APQ3) =',ShimAPQ3,' %')
print('Shimmer (APQ5) =',ShimAPQ5,' %')
