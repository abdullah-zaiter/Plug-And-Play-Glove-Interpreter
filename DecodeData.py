from HandReading import HandReading
import csv
import os
import pickle
import glob

FULL_BUFFER_SIZE = 1902
OBJECT_SIZE = 36
INPUT_FILENAME = "./data.csv"

def partition(array, sliceSize):
    division = len(array) / sliceSize
    if (not division.is_integer()):
        raise ValueError("Data file does not contain a valid quantitiy of bytes for a whole number of reading objects")
    return [array[sliceSize * i:sliceSize * (i + 1)] for i in range(round(division))]

def fromFileToReadingsList(filename):
    csvLen = 0
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csvLen = sum(1 for row in csv_reader)
        csv_file.close()

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        bytesData = bytearray()
        for i,sublist in enumerate(csv_reader):
            for j,item in enumerate(sublist):
                if not(i == csvLen-1 and (j == len(sublist)-1)):
                    bytesData += (bytes([int(item)]))     
    byteObjects = partition(bytesData, OBJECT_SIZE)
    readings = list()
    for byteobject in byteObjects:
        reading = HandReading()
        reading.timestamp = int.from_bytes(byteobject[0:4], "little", signed = False)
        currentByte = 4
        for imu in reading.imus:
            imu.accel.append(int(byteobject[currentByte]))
            currentByte+=1
            imu.accel.append(int(byteobject[currentByte]))
            currentByte+=1
            imu.accel.append(int(byteobject[currentByte]))
            currentByte+=1
            imu.gyro.append(int(byteobject[currentByte]))
            currentByte+=1
            imu.gyro.append(int(byteobject[currentByte]))
            currentByte+=1
            imu.gyro.append(int(byteobject[currentByte]))
            currentByte+=1
        readings.append(reading)
        del reading
    return readings
    
def writeObject(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    readings = fromFileToReadingsList(INPUT_FILENAME)
    writeObject(readings[:int(FULL_BUFFER_SIZE/2)],'1.pkl')
    writeObject(readings[-int(FULL_BUFFER_SIZE/2):],'2.pkl')
    pass
