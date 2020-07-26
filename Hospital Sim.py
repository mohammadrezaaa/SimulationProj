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
        doctorsinRoomRate[ i ][ j ].append("Not busy")
        try:
            int(rates[j])
        except ValueError:
            doctorsinRoomRate[i][j].append(float(rates[j]))
        else:
            doctorsinRoomRate[i][j].append(int(rates[j]))


###########***********      handling patients       **********#############
number_of_patients = 10
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
# patients_data = sorted(patients_data)
#zero if has covid, 1 if doesn't have it.
for o in range(len(patients_data)):
    patients_data[o].append(r[o])  #burst time in reception
    patients_data[o].append(o)
    patients_data[o].append(t[o])  # tired time
    patients_data[o].append(0)


#since now, in patients_data we have time of enterence and covid positivity or negetivity and it's sorted based on its priority

# This func returns the room with shortest line (actually what it returns is an index of the room)
def FindshortestQ(ilist):
    num = 0
    for k in range(1, len(ilist)):
        if len(ilist[k]) < len(ilist[num]):
            num = k
    return num



###########***********      Handling Reception  & ROOM Queue      **********#############
RoomQ = [[] for a in range(M)]

def HOSP_reserve(patienc_D):
    start_time = []
    tmp = []
    exit_time = []
    Returned_patients = []
    S_time = 0
    for i in range(len(patienc_D)):
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

    return start_time, exit_time, Returned_patients
print(patients_data)
reception_output = HOSP_reserve(patients_data)
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
    waiting_time_reception_1.append(reception_output[1][e] - reception_output[0][e])
    waiting_time_reception_2.append(reception_output[0][e] - patients_data[e][0])

print(waiting_time_reception_1)
print("Waiting time in reception: (reception process not included)")
print(waiting_time_reception_2)

print("patience left after reception process in order of end time")
print(patients_data)



def rooms_occupied(DC_InRoom):
    for i in DC_InRoom:
        for j in i:
            if j[1] == 'Not busy':
                return False, DC_InRoom.index(i), i.index(j)
    return True

print(rooms_occupied(doctorsinRoomRate))

def HOSP_EXP(patience_AftRsv, DoctorsInRoom):
    start_time = []
    tmp = []

















