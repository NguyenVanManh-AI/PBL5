with open("thamdu2.csv", "r+") as f:
    myDataList = f.readlines()
    print(myDataList)
    nameList = []
    timeList = []
    for line in myDataList:
        entry = line.split(",")
        nameList.append(entry[0])
        timeList.append(entry[1])
    print(nameList)
    print(timeList)