import numpy as np
import random
randomlist = []

inputs = input().split(" ")
M = int(inputs[0])                                      #number of rooms
enterRate = float(inputs[1])                            #patients entering rate    is poisson with lambda
AvgTiredTime = float(inputs[2])
receptionRate = float(inputs[3])                        #poisson with moo
doctorsinRoomRate = [[] for k in range(M)]              #rates of doctors in each room starting room number zero
for i in range(M):
    rates = input().split(" ")

    for j in range(len(rates)):
        doctorsinRoomRate[i].append([j])


        try:
            int(rates[j])
        except ValueError:
            doctorsinRoomRate[i][j].append(float(rates[j]))
        else:
            doctorsinRoomRate[i][j].append(int(rates[j]))
        doctorsinRoomRate[i][j].append(0)


###########***********      handling patients       **********#############
number_of_patients = 5000
patients_data = [[] for i in range(number_of_patients)]
r = np.random.poisson(receptionRate, number_of_patients)
s = np.random.poisson(enterRate, number_of_patients)
t = np.random.exponential(AvgTiredTime, number_of_patients)

randomlist = []
for k in range(0,number_of_patients//10):
    n = random.randint(0, number_of_patients)
    randomlist.append(n)

for i in range(number_of_patients):
    patients_data[i].append(s[i])
    patients_data[i].append(0)

patients_data = sorted(patients_data)

for h in randomlist:
    patients_data[h].pop()
    patients_data[h].append(1)
patients_data = sorted(patients_data)
#zero if has covid, 1 if doesn't have it.
for o in range(len(patients_data)):
    patients_data[o].append(r[o])  #burst time in reception
    patients_data[o].append(o)
    patients_data[o].append(t[o])  # tired time
    patients_data[o].append(0)


#since now, in patients_data we have time of enterence and covid positivity or negetivity and it's sorted based on its priority


###########***********      Handling Reception  & ROOM Queue      **********#############
RoomQ = [[] for a in range(M)]
counter = [[0] for m in range(M)]
def HOSP_reserve(patienc_D):
    start_time = []
    tmp = []
    exit_time = []
    Returned_patients = []
    S_time = 0
    for i in range(len(patienc_D)):
        AVG_line = 0
        ArrivedQ = []
        notArrivedQ = []
        for j in range(len(patienc_D)):
            if(patienc_D[j][0] <= S_time and patienc_D[j][5] == 0):
                tmp.extend([patienc_D[j][0], patienc_D[j][1], patienc_D[j][2], patienc_D[j][3], patienc_D[j][4]])
                ArrivedQ.append(tmp)
                tmp = []
            elif (patienc_D[j][5] == 0):
                tmp.extend([patienc_D[j][0], patienc_D[j][1], patienc_D[j][2], patienc_D[j][3], patienc_D[j][4]])
                notArrivedQ.append(tmp)
                tmp = []
        if (len(ArrivedQ) != 0) :
            AVG_line += len(ArrivedQ)
            ArrivedQ.sort(key=lambda x:x[1], reverse=True)
            S_time_temp = S_time
            S_time_temp = S_time_temp + ArrivedQ[0][2]
            e_time_temp = S_time_temp
            if (S_time - ArrivedQ[0][0] > ArrivedQ[0][4]):
                for z in range(len(patienc_D)):
                    if(patienc_D[z][3] == ArrivedQ[0][3]):
                        break
                patienc_D[z][5] = -1

                Returned_patients.append(ArrivedQ[0])
                ArrivedQ.pop(0)
                patienc_D.pop(z)
            else:


                start_time.append(S_time)
                S_time = S_time + ArrivedQ[0][2]
                e_time = S_time
                exit_time.append(e_time)
                for k in range(len(patienc_D)):
                    if(patienc_D[k][3] == ArrivedQ[0][3]):
                        break
                patienc_D[k][5] = 1
                patienc_D[k].append(e_time)

        elif(len(ArrivedQ) == 0):
            if(S_time < notArrivedQ[0][0]):
                S_time = notArrivedQ[0][0]
                start_time.append(S_time)
                S_time = S_time + notArrivedQ[0][2]
                e_time = S_time
                exit_time.append(e_time)
                for indx in range(len(patienc_D)):
                    if patienc_D[indx][3] == notArrivedQ[0][3]:
                        break
                patienc_D[indx][5] = 1
                patienc_D[indx].append(e_time)

    return start_time, exit_time, Returned_patients, AVG_line
print("first list of patients")
First_list_of_patients = patients_data
print(First_list_of_patients)
reception_output = HOSP_reserve(patients_data)
AVG_line_reception = reception_output[3]
print("start time")
print(reception_output[0])

print("End time")
print(reception_output[1])

print("Returned patients ")
print(reception_output[2])

sorted(patients_data, key=lambda x:x[6])

print("Waiting time in reception: (reception process included)")
waiting_time_reception_1 = []
waiting_time_reception_2 = []   #to not include reception process
for e in range(len(reception_output[0])):
    waiting_time_reception_1.append(reception_output[1][e] - patients_data[e][0])
    waiting_time_reception_2.append(reception_output[0][e] - patients_data[e][0])

print(waiting_time_reception_1)
print("Waiting time in reception: (reception process not included)")
print(waiting_time_reception_2)

print("patience left after reception process in order of end time")
print(patients_data)



def rooms_occupied(DC_InRoom, T):
    assign_room = 0
    for i in DC_InRoom:
      if(len(RoomQ[DC_InRoom.index(i)]) == 0):
        for j in i:
            if j[2] <= T:
                return False, DC_InRoom.index(i), i.index(j), j     #which room, Which doctor, the doctor
      else:
          assign_room = FindshortestQ(DC_InRoom)


    return True, assign_room





# This func returns the room with shortest line (actually what it returns is an index of the room)
def FindshortestQ(ilist):
    num = 0
    if(len(ilist) >= 2):
        for k in range(1, len(ilist)):
            if len(ilist[k]) < len(ilist[num]):
                num = k
    return num


print("Rooms situation with its doctor")
print(doctorsinRoomRate)



AVG_line_EXP = [[0] for h in range(M)]
# what are the inputs and outputs?     input: patience data[arrival time, priority, burst_time in reservation, number_id, Tired_time, state, endtime]
# input: the doctors in room [[] which is every room] now in each room :[doc_id, rate, end_time of previous work]
def HOSP_EXP(patients_AftRsv, DoctorsInRoom):

    start_time = []
    tmp = []
    exit_time = []
    Returned_patients2 = []
    S_time = 0
    E_time = 0
    patients_AfEXP = []
    for i in range (len(patients_AftRsv)):
       out = rooms_occupied(doctorsinRoomRate, patients_AftRsv[i][6])

       if(out[0] == True):
        RoomQ[out[1]].append(patients_AftRsv[i])
        AVG_line_EXP[out[1]][0] += len(RoomQ[out[1]])
        RoomQ[out[1]].sort(key=lambda x: x[ 1 ], reverse=True)
        counter[out[1]][0] += 1
        v = doctorsinRoomRate[out[1]][0][2]
        assigened_doc = doctorsinRoomRate[out[1]][0]
        for k in range(1, len(DoctorsInRoom[out[1]])):
                if(doctorsinRoomRate[out[1]][k][2]) < v:
                    v = doctorsinRoomRate[out[1]][k][2]
                    assigened_doc = doctorsinRoomRate[out[1]][k]
        if(RoomQ[out[1]][0][6] > v):
            end_time_AfterEXP = RoomQ[out[1]][0][6] + assigened_doc[2]
            RoomQ[out[1]][0].append(end_time_AfterEXP)
            patients_AfEXP.append(RoomQ[out[1]][0])
            RoomQ[out[1]].pop(0)
        else:
            end_time_AfterEXP = v + assigened_doc[2]
            RoomQ[out[1]][0].append(end_time_AfterEXP)
            patients_AfEXP.append(RoomQ[out[1]][0])
            RoomQ[out[1]].pop(0)







       else:
            doctor = out[3]
            doc_speed = doctor[1]
            doctor[2] = 0
            S_time = patients_AftRsv[i][6]
            start_time.append(S_time)
            S_time = S_time + doc_speed
            E_time = S_time
            exit_time.append(E_time)
            patients_AftRsv[i][5] = 2
            patients_AftRsv[i].append(E_time)
            doctor[2] = E_time
            patients_AfEXP.append(patients_AftRsv[i])
    return patients_AfEXP


# HOSP_EXP(patients_data, doctorsinRoomRate)
patients_afterall = HOSP_EXP(patients_data, doctorsinRoomRate)
print("After all the patients, with the end time in the last index")
print(patients_afterall)








#implementing questions:

#question one

def AvgTimeInSystem(patients):
    covid_count = 0
    nottest_count = 0
    overal = 0
    covid_positive = 0
    not_tested = 0
    for i in patients:
        overal += i[7] - i[0]
        if i[1] == 1:
            covid_count += 1
            covid_positive += i[7] - i[0]
        else:
            nottest_count += 1
            not_tested += i[7] - i[0]
    overal = overal/len(patients_afterall)
    covid_positive = covid_positive/covid_count
    not_tested = not_tested/nottest_count
    return overal, covid_positive, not_tested

#question 2
def AvgWaitingTimeInLine():
    covid_count = 0
    nottest_count = 0
    covid_inline = 0
    overal = 0
    not_covid_inline = 0
    for i in range(len(patients_data)):
        if patients_data[i][1] == 1:
            covid_inline += waiting_time_reception_2[i]
            overal += waiting_time_reception_2[i]
            covid_count += 1
        else:
            not_covid_inline += waiting_time_reception_2[i]
            nottest_count += 1
            overal += waiting_time_reception_2[i]
    overal = overal / len(patients_data)
    covid_inline = covid_inline/covid_count
    not_covid_inline = not_covid_inline/nottest_count
    return overal, covid_inline, not_covid_inline


#Question3
def AvgPeopleTired():
    AVG = number_of_patients - len(patients_afterall)
    return AVG

def AVGLINE():
    AVG_rec = AVG_line_reception

    return AVG_rec, AVG_line_EXP


#Q1

AVG_output = AvgTimeInSystem(patients_afterall)
print("AVG SYS overall")
print(AVG_output[0])
print("AVG SYS covid+")
print(AVG_output[1])
print("AVG SYS not tested")
print(AVG_output[2])

#Q2
AVGTIMEINLINE = AvgWaitingTimeInLine()
print("average time overall in line")
print(AVGTIMEINLINE[0])

print("average time covid+ in line")
print(AVGTIMEINLINE[1])
print("average time notcovid in line")
print(AVGTIMEINLINE[2])

#Q3
print("Average people leaving system")
print(AvgPeopleTired())

print("AVGAVG length of line in reception")
print(AVGLINE()[0])
print("AVGAVG length of line in rooms")
print(AVGLINE()[1][0][0]/M)

import matplotlib.pyplot as plt

X0 = []
X1 = []
for patient in patients_afterall:
    if(patient[1] == 0):
        X0.append(patient[6] - patient[0] - patient[2])
    else:
        X1.append(patient[6] - patient[0] - patient[2])
plt.hist(X0)
plt.show()
plt.hist(X1)
plt.show()

X0 = []
X1 = []
for patient in patients_afterall:
    if(patient[1] == 0):
        X0.append(patient[6] - patient[0])
    else:
        X1.append(patient[6] - patient[0])
plt.hist(X0)
plt.show()
plt.hist(X1)
plt.show()

X0 = []
X1 = []
for patient in patients_afterall:
    if(patient[1] == 0):
        X0.append(patient[7] - patient[0])
    else:
        X1.append(patient[7] - patient[0])
plt.hist(X0)
plt.show()
plt.hist(X1)
plt.show()

X = []
for patient in patients_afterall:
    X.append(patient[1])
plt.hist(X)

X0 = []
X1 = []
X2 = []
for patient in patients_afterall:
    X2.append(patient[6] - patient[0] - patient[2])
    if(patient[1] == 0):
        X0.append(patient[6] - patient[0] - patient[2])
    else:
        X1.append(patient[6] - patient[0] - patient[2])
plt.hist(X0)
plt.show()
plt.hist(X1)
plt.show()
plt.hist(X2)
plt.show()
