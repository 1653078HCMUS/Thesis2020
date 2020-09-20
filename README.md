# Code for thesis 2020

## **1.Bao gồm:**
Source code bao gồm 3 folder:
- Folder Histogram_Calculate list of Jitter chứa code tìm danh sách các jitter trên 1 đoạn âm thanh và vẽ Histogram của đoạn âm thanh đó.
- Folder Principal Component Analysis chứa code vẽ PCA, trong folder này tách ra 2 folder nhỏ là PCA Jitter và PCA Shimmer.
- folder Library for Jitter and Shimmer Calculation chứa code của thư viện tính toán Jitter Shimmer và file script dùng để gọi các hàm tính toán từ thư viện.

## **2.Giải thích:**
##### **a.Vẽ Histogram:**
- j_Histogram là script vẽ ra histogram từ danh sách các Jitter trên 1 đoạn âm thanh được chứa trong 1 file csv.
Code phân loại các khung dữ liệu:
```ruby
features = ['local', 'absolute', 'rap', 'ppq5', 'ddp']
column_name = ['local', 'absolute', 'rap', 'ppq5', 'ddp', 'target']
```
Code đọc từ file csv:
```ruby
data = pd.read_csv(csv_file, names=column_name)
data.plot(kind='bar')
```

##### **b.PCA:**
- Hàm Standardlize:
```ruby
x = StandardScaler().fit_transform(x)
```
- Hàm chuyển 4 cột thành 2 cột:
```ruby
pca = PCA(n_components=2)
#Set number of components for PCA
principalComponents = pca.fit_transform(x)

#Transform data in x to fit into principal component
principalDf = pd.DataFrame(data=principalComponents,
                           columns=['principal component 1', 'principal component 2'])
finalDf = pd.concat([principalDf, data[['target']]], axis=1)
```
- Hàm vẽ Chart
```ruby
fig = plt.figure(figsize=(12, 7))
#Size of figure

ax = fig.add_subplot(1, 1, 1)
#Add number of rows, columns and indexs to figure

ax.set_xlabel('Principal Component 1', fontsize=15)
ax.set_ylabel('Principal Component 2', fontsize=15)
ax.set_title('2 component PCA', fontsize=20)
#Set labels and title for the figure

targets = ['normal', 'patient']
colors = ['g', 'r']
for target, color in zip(targets, colors):
    indicesToKeep = finalDf['target'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1'],
               finalDf.loc[indicesToKeep, 'principal component 2'],
               c=color, s=50)
ax.legend(targets)
#Put target into figure
```
##### **c.Thư viện tính toán:**
- Các hàm thường dùng
```ruby
sound = parselmouth.Sound(soundPath)
#Hàm xử lý file âm thanh từ đường dẫn
pitch = sound.to_pitch()
#Hàm đưa tín hiệu âm thanh về Pitch (một kiểu data của âm thanh biểu diễn dưới dạng mức độ sóng tại 1 điểm thời gian)
pulses = parselmouth.praat.call([sound, pitch],"To PointProcess (cc)")
#Hàm nhằm lấy các pulses của file âm thanh (pulse là ...), 
n_pulse = parselmouth.praat.call(pulses, "Get number of points")
#Hàm lấy các chu kì của file âm thanh
Ti = parselmouth.praat.call(pulses,"Get time from index", i)
#Hàm lấy thời gian tại điểm cho trước (ở đây điểm cho trước là vị trí của Pulse)
```

- Tính Jitter Local
```ruby
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
```
- Tính Jitter Local Absolute
```ruby
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
```
- Tính Jitter RAP
```ruby

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
```
- Tính Jitter PPQ5
```ruby
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
```
- Tính Jitter DDP
```ruby
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
```

- Tính Shimmer Local
```ruby
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
```

- Tính Shimmer DB
```ruby
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
```

- Tính Shimmer APQ3
```ruby
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
```

- Tính Shimmer APQ5
```ruby
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
```
