import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dir_files = '../Dataset/'
col_labels = [
    'Dev_ID',
    'Acc_X',
    'Acc_Y',
    'Acc_Z',
    'Gyr_X',
    'Gyr_Y',
    'Gyr_Z',
    'Mag_X',
    'Mag_Y',
    'Mag_Z',
    'Timestamp',
    'Act_Label'
]

act_labels = [
    'Stand',
    'Sit',
    'Sit_Talk',
    'Walk',
    'Walk_Talk',
    'Climb_Stair',
    'Climb_Stair_talk',
    'Stand_Sit',
    'Sit_Stand',
    'Stand_Sit_Talk',
    'Sit_Stand_Talk',
    'Stand_Walk',
    'Walk_Stand',
    'Stand_Climb_Stairs_Talk',
    'Climb_Stairs_Walk',
    'Climb_Stairs_Talk_Walk_Talk'
]

modules_labels = [
    'Acc_Dens',
    'Gyr_Dens',
    'Mag_Dens'
]

k_values = [
    3
]

def read_file(id=0, dev=2):
    file_path = dir_files + 'part' + str(id) + '/part' + str(id) + 'dev' + str(dev) + '.csv'

    csv_file = open(file_path)
    csv_reader = csv.reader(csv_file, delimiter=',')
    data_np = np.array(list(csv_reader)).astype(float)

    data = pd.DataFrame(data_np)
    data.columns = col_labels
    
    return [data,data_np]
    

[data,data_np] = read_file()
data

def calc_mod(data, n_act=16):
    acc = list()
    gyr = list()
    mag = list()

    for act in range(1, n_act+1):
        activity = data.loc[data['Act_Label'] == act]

        df_acc = pd.DataFrame(np.sqrt((activity['Acc_X']**2 + activity['Acc_Y']**2 + activity['Acc_Z']**2)))
        df_acc.columns=[act]
        acc.append(df_acc)

        df_gyr = pd.DataFrame(np.sqrt((activity['Gyr_X']**2 + activity['Gyr_Y']**2 + activity['Gyr_Z']**2)))
        df_gyr.columns=[act]
        gyr.append(df_gyr)

        df_mag = pd.DataFrame(np.sqrt((activity['Mag_X']**2 + activity['Mag_Y']**2 + activity['Mag_Z']**2)))
        df_mag.columns=[act]
        mag.append(df_mag)
    
    acc = pd.concat(acc)
    gyr = pd.concat(gyr)
    mag = pd.concat(mag)

    return [acc,gyr,mag]

[acc,gyr,mag] = calc_mod(data)

def getDensity(vector,i):
    quart = vector[i].quantile([0.25,0.75])
    iqr = quart[0.75] - quart[0.25]
    lim = [quart[0.25] - iqr, quart[0.75] + iqr]

    values = vector.loc[(vector[i] < lim[0]) | (vector[i] > lim[1]),[i]]
    
    return values.shape[0] / vector.shape[0] * 100


def plotBoxplot(acc,gyr,mag,n_act=16):
    density = [[],[],[]]

    for i in range(1,n_act+1):
        dens_acc = getDensity(acc, i)
        density[0].append(dens_acc)

        dens_gyr = getDensity(gyr, i)
        density[1].append(dens_gyr)

        dens_mag = getDensity(mag, i)
        density[2].append(dens_mag)

        # plt.figure()
        # col = [n for n in range(i,min(i+3,n_act+1))]
        # for j in col:
        # acc.boxplot(column=col)

    for i in range(len(density)):
        density[i] = pd.DataFrame(density[i])
        density[i].columns = [modules_labels[i]]
        
    density = pd.concat(density,axis=1)

    # plt.figure()
    # acc.boxplot()

    # plt.figure()
    # gyr.boxplot()
    
    # plt.figure()
    # mag.boxplot()
    
    return density
density = plotBoxplot(acc,gyr,mag)
density

def zscore(vector,k):
    z = (vector - vector.mean()) / vector.std()
    
    out = z.loc[(z < -k) | (z > k)]
    not_out = z.loc[(z >= -k) & (z <= k)]

    return [out.index,not_out.index]

def outliersZscore(vector,data,vec_name,acts=[1]):
    n_outliers = list() 
        
    for k in k_values:
        k_out = list()
        for act in acts:
            [out_pos,not_out_pos] = zscore(vector[act],k)

            k_out.append(out_pos.shape[0])

            out = data.iloc[out_pos]
            not_out = data.iloc[not_out_pos]
            
            threedee = plt.figure().gca(projection='3d')
            threedee.scatter(not_out[vec_name+'_X'],not_out[vec_name+'_Y'],not_out[vec_name+'_Z'],c='blue',label='Not Outliers')
            threedee.scatter(out[vec_name+'_X'],out[vec_name+'_Y'],out[vec_name+'_Z'],c='red',label='Ouliers')
            title = vec_name + ' Act=' + str(act) + ' k=' + str(k)
            plt.title(title)
            threedee.legend()
            plt.show()
        
        df = pd.DataFrame(k_out)
        df.columns = [vec_name + ' ' + str(k)]
        df.index = acts
        n_outliers.append(df)

    n_outliers = pd.concat(n_outliers,axis=1)
    return n_outliers
    
acts = [1]
out_acc = outliersZscore(acc,data,'Acc',acts)
# out_gyr = outliersZscore(gyr,data,'Gyr',acts)
# out_mag = outliersZscore(mag,data,'Mag',acts)

# out = pd.concat([out_acc,out_gyr,out_mag],axis=1)
out_acc