
import pandas as pd
import copy
import warnings
warnings.filterwarnings("ignore", category=FutureWarning) 

food_hour_list = []

#from plotnine import *

founders_n = 1
hours = 200
food_on_plate = 10000000

def worm_at_25():
# Create a schedule for worm development at 25C
    df1 = pd.DataFrame({'Stages_name': [], 'Stages_detail': [], 'Numbers': [], 'Progeny/hour': []})
    temp = []
    for i in range(0,10):
        temp.append({"Stages_name": "Egg", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
    
    for i in range(10,19):
        temp.append({"Stages_name": "L1", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(19,27):
        temp.append({"Stages_name": "L2", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(27,32):
        temp.append({"Stages_name": "L3", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(32,40):
        temp.append({"Stages_name": "L4", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(40,47):
        temp.append({"Stages_name": "A_nf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(47,89):
        temp.append({"Stages_name": "A_f", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(89,240):
        temp.append({"Stages_name": "A_pf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    df1 = pd.DataFrame(temp)
    # Filling egg laying schedule
    # total number of eggs at 25C = 170
    for i in range(47,49):
        df1.iloc[i,3] = 1
    for i in range(49,51):
        df1.iloc[i,3] = 2
    for i in range(51,53):
        df1.iloc[i,3] = 3
    for i in range(53,55):
        df1.iloc[i,3] = 4
    for i in range(55,57):
        df1.iloc[i,3] = 5
    for i in range(57,59):
        df1.iloc[i,3] = 6
    for i in range(59,61):
        df1.iloc[i,3] = 7
    for i in range(61,63):
        df1.iloc[i,3] = 8
    for i in range(63,66):
        df1.iloc[i,3] = 7
    for i in range(66,70):
        df1.iloc[i,3] = 6
    for i in range(70,73):
        df1.iloc[i,3] = 5
    for i in range(73,76):
        df1.iloc[i,3] = 4
    for i in range(76,80):
        df1.iloc[i,3] = 3
    for i in range(80,85):
        df1.iloc[i,3] = 2
    for i in range(85,89):
        df1.iloc[i,3] = 1
    
    return df1

df1 = worm_at_25()

res = pd.DataFrame({'t': [], 'Eggs': [], 'L1': [], 'L2': [], 'L3': [], 
                    'L4': [], 'A': [], 'YA': [], 'PA': []})

##### initialize

# put the number of L4 founders
df1.iloc[39,2] = founders_n

##### Run first simulation 
df_list = {}
for t in range(1, hours):
    for step in range(239, 0, -1):
       df1.iloc[step, 2] = df1.iloc[step-1, 2]
       df1.iloc[step-1, 2] = 0
    df1.iloc[0, 2] = (df1.iloc[47:89, 2]*df1.iloc[47:89, 3]).sum() 
    
    df_list['t_'+str(t)] = df1
    r = []
    r.append( t )    # t
    r.append( df1.loc[df1['Stages_name']=='Eggs', 'Numbers'].sum())   # Eggs 
    r.append( df1.loc[df1['Stages_name']=='L1', 'Numbers'].sum() )   # L1
    r.append( df1.loc[df1['Stages_name']=='L2', 'Numbers'].sum() )   # L2
    r.append( df1.loc[df1['Stages_name']=='L3', 'Numbers'].sum() )   # L3
    r.append( df1.loc[df1['Stages_name']=='L4', 'Numbers'].sum() )   # L4
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f')|(df1['Stages_name']=='A_pf'), 'Numbers'].sum() )  # A
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f'), 'Numbers'].sum() )   # YA
    r.append( df1.loc[(df1['Stages_name']=='A_pf'), 'Numbers'].sum() ) #PA
    res = res.append(pd.Series(r, index=['t', 'Eggs', 'L1', 'L2', 'L3', 'L4', 'A', 'YA', 'PA']), ignore_index=True)


#sum column
sum_all = pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
sum_all['Total_number'] = sum_all[sum_list].sum(axis=1)


#find food consumption 
food= pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
#set food intake ratio 1, 2, 4, 8, 16
food_cons_stage = [1, 0, 1, 2, 4, 8, 16, 1, 1]
food_cons = food.mul(food_cons_stage, axis= 1)
food_cons['food_consum'] = food_cons[sum_list].sum(axis=1)
food_cons['food_consum_acu'] = food_cons['food_consum'].cumsum()
food_cons_total = food_cons.loc[food_cons['food_consum_acu'] > food_on_plate]
food_cons_total_1 = food_cons_total['t'].head(1)
food_hour = int(food_cons_total_1)
food_hour_list.append(int(food_hour))

food_dist = sum_all[food_hour-1:food_hour]

y_starved = int(food_dist['Total_number'])

sum_great_dis = food_dist


distribution = pd.DataFrame.copy(res)
for t in range(hours-2, 0, -1):
    distribution.iloc[t] -= distribution.iloc[t-1]
    distribution['t'] = res['t']

sum_dist = pd.DataFrame.copy(distribution)
sum_dist['Total_number'] = sum_dist[sum_list].sum(axis=1)
sum_dist = sum_dist.drop(sum_list, axis=1)




from plotnine import ggplot
from plotnine import geom_bar, aes


######################################################################################
# without eggs / with larve + adults
res_plot_a = res[[ 't', 'L1', 'L2', 'L3', 'L4', 'A']]
res_plot_a_sum = copy.deepcopy(res_plot_a)
res_plot_a_sum['sum'] = res_plot_a_sum[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
res_plot_a_sum = res_plot_a_sum.loc[:,"L1":"A"].div(res_plot_a_sum["sum"], axis=0)
res_plot_a_sum['t'] = res_plot_a['t']


sum_great_dis_sum = copy.deepcopy(sum_great_dis)
sum_great_dis_sum['sum'] = sum_great_dis[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
sum_great_dis_sum = sum_great_dis_sum.loc[:, "L1":"A"].div(sum_great_dis_sum["sum"],axis=0) * 100
sum_great_dis_sum['t'] = sum_great_dis['t']

res_plot_a_sum2 = pd.melt(res_plot_a, id_vars="t")
res_plot_a_sum_plot = pd.melt(res_plot_a_sum, id_vars="t")
sum_great_dis_plot = pd.melt(sum_great_dis_sum, id_vars="t")

print(sum_great_dis_plot.to_string())


# Stacked
import matplotlib.pyplot as plt
import plotnine as p9
from matplotlib import gridspec
from plotnine import data
from mizani.formatters import scientific_format

p1 = (p9.ggplot(sum_great_dis_plot, aes(fill='variable', y= 'value', x= ['L1', 'L2', 'L3', 'L4', 'A' ]))
    + p9.scale_x_discrete(limits= ('L1', 'L2', 'L3', 'L4', 'A'))
    + p9.geom_bar(position="stack", stat="identity")
    + p9.ylim(0,100)
    + p9.geom_text(mapping=aes(label='value'), format_string='{:.1f}', va="bottom")
    + p9.theme_linedraw())

df1 = df1.iloc[0:0]
res = res.iloc[0:0]



founders_n = 3
hours = 200
food_on_plate = 10000000

def worm_at_25():
# Create a schedule for worm development at 25C
    df1 = pd.DataFrame({'Stages_name': [], 'Stages_detail': [], 'Numbers': [], 'Progeny/hour': []})
    temp = []
    for i in range(0,10):
        temp.append({"Stages_name": "Egg", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
    
    for i in range(10,19):
        temp.append({"Stages_name": "L1", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(19,27):
        temp.append({"Stages_name": "L2", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(27,32):
        temp.append({"Stages_name": "L3", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(32,40):
        temp.append({"Stages_name": "L4", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(40,47):
        temp.append({"Stages_name": "A_nf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(47,89):
        temp.append({"Stages_name": "A_f", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(89,240):
        temp.append({"Stages_name": "A_pf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    df1 = pd.DataFrame(temp)
    # Filling egg laying schedule
    # total number of eggs at 25C = 170
    for i in range(47,49):
        df1.iloc[i,3] = 1
    for i in range(49,51):
        df1.iloc[i,3] = 2
    for i in range(51,53):
        df1.iloc[i,3] = 3
    for i in range(53,55):
        df1.iloc[i,3] = 4
    for i in range(55,57):
        df1.iloc[i,3] = 5
    for i in range(57,59):
        df1.iloc[i,3] = 6
    for i in range(59,61):
        df1.iloc[i,3] = 7
    for i in range(61,63):
        df1.iloc[i,3] = 8
    for i in range(63,66):
        df1.iloc[i,3] = 7
    for i in range(66,70):
        df1.iloc[i,3] = 6
    for i in range(70,73):
        df1.iloc[i,3] = 5
    for i in range(73,76):
        df1.iloc[i,3] = 4
    for i in range(76,80):
        df1.iloc[i,3] = 3
    for i in range(80,85):
        df1.iloc[i,3] = 2
    for i in range(85,89):
        df1.iloc[i,3] = 1
    
    return df1

df1 = worm_at_25()

res = pd.DataFrame({'t': [], 'Eggs': [], 'L1': [], 'L2': [], 'L3': [], 
                    'L4': [], 'A': [], 'YA': [], 'PA': []})

##### initialize

# put the number of L4 founders
df1.iloc[39,2] = founders_n

##### Run first simulation 
df_list = {}
for t in range(1, hours):
    for step in range(239, 0, -1):
       df1.iloc[step, 2] = df1.iloc[step-1, 2]
       df1.iloc[step-1, 2] = 0
    df1.iloc[0, 2] = (df1.iloc[47:89, 2]*df1.iloc[47:89, 3]).sum() 
    
    df_list['t_'+str(t)] = df1
    r = []
    r.append( t )    # t
    r.append( df1.loc[df1['Stages_name']=='Eggs', 'Numbers'].sum())   # Eggs 
    r.append( df1.loc[df1['Stages_name']=='L1', 'Numbers'].sum() )   # L1
    r.append( df1.loc[df1['Stages_name']=='L2', 'Numbers'].sum() )   # L2
    r.append( df1.loc[df1['Stages_name']=='L3', 'Numbers'].sum() )   # L3
    r.append( df1.loc[df1['Stages_name']=='L4', 'Numbers'].sum() )   # L4
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f')|(df1['Stages_name']=='A_pf'), 'Numbers'].sum() )  # A
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f'), 'Numbers'].sum() )   # YA
    r.append( df1.loc[(df1['Stages_name']=='A_pf'), 'Numbers'].sum() ) #PA
    res = res.append(pd.Series(r, index=['t', 'Eggs', 'L1', 'L2', 'L3', 'L4', 'A', 'YA', 'PA']), ignore_index=True)


#sum column
sum_all = pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
sum_all['Total_number'] = sum_all[sum_list].sum(axis=1)


#find food consumption 
food= pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
#set food intake ratio 1, 2, 4, 8, 16
food_cons_stage = [1, 0, 1, 2, 4, 8, 16, 1, 1]
food_cons = food.mul(food_cons_stage, axis= 1)
food_cons['food_consum'] = food_cons[sum_list].sum(axis=1)
food_cons['food_consum_acu'] = food_cons['food_consum'].cumsum()
food_cons_total = food_cons.loc[food_cons['food_consum_acu'] > food_on_plate]
food_cons_total_1 = food_cons_total['t'].head(1)
food_hour = int(food_cons_total_1)
food_hour_list.append(int(food_hour))

food_dist = sum_all[food_hour-1:food_hour]

y_starved = int(food_dist['Total_number'])

sum_great_dis = food_dist


distribution = pd.DataFrame.copy(res)
for t in range(hours-2, 0, -1):
    distribution.iloc[t] -= distribution.iloc[t-1]
    distribution['t'] = res['t']

sum_dist = pd.DataFrame.copy(distribution)
sum_dist['Total_number'] = sum_dist[sum_list].sum(axis=1)
sum_dist = sum_dist.drop(sum_list, axis=1)




from plotnine import ggplot
from plotnine import geom_bar, aes


######################################################################################
# without eggs / with larve + adults
res_plot_a = res[[ 't', 'L1', 'L2', 'L3', 'L4', 'A']]
res_plot_a_sum = copy.deepcopy(res_plot_a)
res_plot_a_sum['sum'] = res_plot_a_sum[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
res_plot_a_sum = res_plot_a_sum.loc[:,"L1":"A"].div(res_plot_a_sum["sum"], axis=0)
res_plot_a_sum['t'] = res_plot_a['t']


sum_great_dis_sum = copy.deepcopy(sum_great_dis)
sum_great_dis_sum['sum'] = sum_great_dis[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
sum_great_dis_sum = sum_great_dis_sum.loc[:, "L1":"A"].div(sum_great_dis_sum["sum"],axis=0) * 100
sum_great_dis_sum['t'] = sum_great_dis['t']

res_plot_a_sum2 = pd.melt(res_plot_a, id_vars="t")
res_plot_a_sum_plot = pd.melt(res_plot_a_sum, id_vars="t")
sum_great_dis_plot = pd.melt(sum_great_dis_sum, id_vars="t")
print(sum_great_dis_plot)


# Stacked
import matplotlib.pyplot as plt
import plotnine as p9
from matplotlib import gridspec
from plotnine import data
from mizani.formatters import scientific_format

p2 = (p9.ggplot(sum_great_dis_plot, aes(fill='variable', y= 'value', x= ['L1', 'L2', 'L3', 'L4', 'A' ]))
    + p9.scale_x_discrete(limits= ('L1', 'L2', 'L3', 'L4', 'A'))
    + p9.geom_bar(position="stack", stat="identity")
    + p9.ylim(0,100)
    + p9.geom_text(mapping=aes(label='value'), format_string='{:.1f}', va="bottom")
    + p9.theme_linedraw())

df1 = df1.iloc[0:0]
res = res.iloc[0:0]

founders_n = 10
hours = 200
food_on_plate = 10000000

def worm_at_25():
# Create a schedule for worm development at 25C
    df1 = pd.DataFrame({'Stages_name': [], 'Stages_detail': [], 'Numbers': [], 'Progeny/hour': []})
    temp = []
    for i in range(0,10):
        temp.append({"Stages_name": "Egg", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
    
    for i in range(10,19):
        temp.append({"Stages_name": "L1", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(19,27):
        temp.append({"Stages_name": "L2", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(27,32):
        temp.append({"Stages_name": "L3", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(32,40):
        temp.append({"Stages_name": "L4", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(40,47):
        temp.append({"Stages_name": "A_nf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(47,89):
        temp.append({"Stages_name": "A_f", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(89,240):
        temp.append({"Stages_name": "A_pf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    df1 = pd.DataFrame(temp)
    # Filling egg laying schedule
    # total number of eggs at 25C = 170
    for i in range(47,49):
        df1.iloc[i,3] = 1
    for i in range(49,51):
        df1.iloc[i,3] = 2
    for i in range(51,53):
        df1.iloc[i,3] = 3
    for i in range(53,55):
        df1.iloc[i,3] = 4
    for i in range(55,57):
        df1.iloc[i,3] = 5
    for i in range(57,59):
        df1.iloc[i,3] = 6
    for i in range(59,61):
        df1.iloc[i,3] = 7
    for i in range(61,63):
        df1.iloc[i,3] = 8
    for i in range(63,66):
        df1.iloc[i,3] = 7
    for i in range(66,70):
        df1.iloc[i,3] = 6
    for i in range(70,73):
        df1.iloc[i,3] = 5
    for i in range(73,76):
        df1.iloc[i,3] = 4
    for i in range(76,80):
        df1.iloc[i,3] = 3
    for i in range(80,85):
        df1.iloc[i,3] = 2
    for i in range(85,89):
        df1.iloc[i,3] = 1
    
    return df1

df1 = worm_at_25()

res = pd.DataFrame({'t': [], 'Eggs': [], 'L1': [], 'L2': [], 'L3': [], 
                    'L4': [], 'A': [], 'YA': [], 'PA': []})

##### initialize

# put the number of L4 founders
df1.iloc[39,2] = founders_n

##### Run first simulation 
df_list = {}
for t in range(1, hours):
    for step in range(239, 0, -1):
       df1.iloc[step, 2] = df1.iloc[step-1, 2]
       df1.iloc[step-1, 2] = 0
    df1.iloc[0, 2] = (df1.iloc[47:89, 2]*df1.iloc[47:89, 3]).sum() 
    
    df_list['t_'+str(t)] = df1
    r = []
    r.append( t )    # t
    r.append( df1.loc[df1['Stages_name']=='Eggs', 'Numbers'].sum())   # Eggs 
    r.append( df1.loc[df1['Stages_name']=='L1', 'Numbers'].sum() )   # L1
    r.append( df1.loc[df1['Stages_name']=='L2', 'Numbers'].sum() )   # L2
    r.append( df1.loc[df1['Stages_name']=='L3', 'Numbers'].sum() )   # L3
    r.append( df1.loc[df1['Stages_name']=='L4', 'Numbers'].sum() )   # L4
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f')|(df1['Stages_name']=='A_pf'), 'Numbers'].sum() )  # A
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f'), 'Numbers'].sum() )   # YA
    r.append( df1.loc[(df1['Stages_name']=='A_pf'), 'Numbers'].sum() ) #PA
    res = res.append(pd.Series(r, index=['t', 'Eggs', 'L1', 'L2', 'L3', 'L4', 'A', 'YA', 'PA']), ignore_index=True)


#sum column
sum_all = pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
sum_all['Total_number'] = sum_all[sum_list].sum(axis=1)


#find food consumption 
food= pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
#set food intake ratio 1, 2, 4, 8, 16
food_cons_stage = [1, 0, 1, 2, 4, 8, 16, 1, 1]
food_cons = food.mul(food_cons_stage, axis= 1)
food_cons['food_consum'] = food_cons[sum_list].sum(axis=1)
food_cons['food_consum_acu'] = food_cons['food_consum'].cumsum()
food_cons_total = food_cons.loc[food_cons['food_consum_acu'] > food_on_plate]
food_cons_total_1 = food_cons_total['t'].head(1)
food_hour = int(food_cons_total_1)
food_hour_list.append(int(food_hour))

food_dist = sum_all[food_hour-1:food_hour]

y_starved = int(food_dist['Total_number'])

sum_great_dis = food_dist


distribution = pd.DataFrame.copy(res)
for t in range(hours-2, 0, -1):
    distribution.iloc[t] -= distribution.iloc[t-1]
    distribution['t'] = res['t']

sum_dist = pd.DataFrame.copy(distribution)
sum_dist['Total_number'] = sum_dist[sum_list].sum(axis=1)
sum_dist = sum_dist.drop(sum_list, axis=1)




from plotnine import ggplot
from plotnine import geom_bar, aes


######################################################################################
# without eggs / with larve + adults
res_plot_a = res[[ 't', 'L1', 'L2', 'L3', 'L4', 'A']]
res_plot_a_sum = copy.deepcopy(res_plot_a)
res_plot_a_sum['sum'] = res_plot_a_sum[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
res_plot_a_sum = res_plot_a_sum.loc[:,"L1":"A"].div(res_plot_a_sum["sum"], axis=0)
res_plot_a_sum['t'] = res_plot_a['t']


sum_great_dis_sum = copy.deepcopy(sum_great_dis)
sum_great_dis_sum['sum'] = sum_great_dis[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
sum_great_dis_sum = sum_great_dis_sum.loc[:, "L1":"A"].div(sum_great_dis_sum["sum"],axis=0) * 100
sum_great_dis_sum['t'] = sum_great_dis['t']

res_plot_a_sum2 = pd.melt(res_plot_a, id_vars="t")
res_plot_a_sum_plot = pd.melt(res_plot_a_sum, id_vars="t")
sum_great_dis_plot = pd.melt(sum_great_dis_sum, id_vars="t")
print(sum_great_dis_plot)


# Stacked
import matplotlib.pyplot as plt
import plotnine as p9
from matplotlib import gridspec
from plotnine import data
from mizani.formatters import scientific_format

p3 = (p9.ggplot(sum_great_dis_plot, aes(fill='variable', y= 'value', x= ['L1', 'L2', 'L3', 'L4', 'A' ]))
    + p9.scale_x_discrete(limits= ('L1', 'L2', 'L3', 'L4', 'A'))
    + p9.geom_bar(position="stack", stat="identity")
    + p9.ylim(0,100)
    + p9.geom_text(mapping=aes(label='value'), format_string='{:.1f}', va="bottom")
    + p9.theme_linedraw())

df1 = df1.iloc[0:0]
res = res.iloc[0:0]

founders_n = 50
hours = 200
food_on_plate = 10000000

def worm_at_25():
# Create a schedule for worm development at 25C
    df1 = pd.DataFrame({'Stages_name': [], 'Stages_detail': [], 'Numbers': [], 'Progeny/hour': []})
    temp = []
    for i in range(0,10):
        temp.append({"Stages_name": "Egg", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
    
    for i in range(10,19):
        temp.append({"Stages_name": "L1", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(19,27):
        temp.append({"Stages_name": "L2", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(27,32):
        temp.append({"Stages_name": "L3", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(32,40):
        temp.append({"Stages_name": "L4", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(40,47):
        temp.append({"Stages_name": "A_nf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(47,89):
        temp.append({"Stages_name": "A_f", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(89,240):
        temp.append({"Stages_name": "A_pf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    df1 = pd.DataFrame(temp)
    # Filling egg laying schedule
    # total number of eggs at 25C = 170
    for i in range(47,49):
        df1.iloc[i,3] = 1
    for i in range(49,51):
        df1.iloc[i,3] = 2
    for i in range(51,53):
        df1.iloc[i,3] = 3
    for i in range(53,55):
        df1.iloc[i,3] = 4
    for i in range(55,57):
        df1.iloc[i,3] = 5
    for i in range(57,59):
        df1.iloc[i,3] = 6
    for i in range(59,61):
        df1.iloc[i,3] = 7
    for i in range(61,63):
        df1.iloc[i,3] = 8
    for i in range(63,66):
        df1.iloc[i,3] = 7
    for i in range(66,70):
        df1.iloc[i,3] = 6
    for i in range(70,73):
        df1.iloc[i,3] = 5
    for i in range(73,76):
        df1.iloc[i,3] = 4
    for i in range(76,80):
        df1.iloc[i,3] = 3
    for i in range(80,85):
        df1.iloc[i,3] = 2
    for i in range(85,89):
        df1.iloc[i,3] = 1
    
    return df1

df1 = worm_at_25()

res = pd.DataFrame({'t': [], 'Eggs': [], 'L1': [], 'L2': [], 'L3': [], 
                    'L4': [], 'A': [], 'YA': [], 'PA': []})

##### initialize

# put the number of L4 founders
df1.iloc[39,2] = founders_n

##### Run first simulation 
df_list = {}
for t in range(1, hours):
    for step in range(239, 0, -1):
       df1.iloc[step, 2] = df1.iloc[step-1, 2]
       df1.iloc[step-1, 2] = 0
    df1.iloc[0, 2] = (df1.iloc[47:89, 2]*df1.iloc[47:89, 3]).sum() 
    
    df_list['t_'+str(t)] = df1
    r = []
    r.append( t )    # t
    r.append( df1.loc[df1['Stages_name']=='Eggs', 'Numbers'].sum())   # Eggs 
    r.append( df1.loc[df1['Stages_name']=='L1', 'Numbers'].sum() )   # L1
    r.append( df1.loc[df1['Stages_name']=='L2', 'Numbers'].sum() )   # L2
    r.append( df1.loc[df1['Stages_name']=='L3', 'Numbers'].sum() )   # L3
    r.append( df1.loc[df1['Stages_name']=='L4', 'Numbers'].sum() )   # L4
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f')|(df1['Stages_name']=='A_pf'), 'Numbers'].sum() )  # A
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f'), 'Numbers'].sum() )   # YA
    r.append( df1.loc[(df1['Stages_name']=='A_pf'), 'Numbers'].sum() ) #PA
    res = res.append(pd.Series(r, index=['t', 'Eggs', 'L1', 'L2', 'L3', 'L4', 'A', 'YA', 'PA']), ignore_index=True)


#sum column
sum_all = pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
sum_all['Total_number'] = sum_all[sum_list].sum(axis=1)


#find food consumption 
food= pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
#set food intake ratio 1, 2, 4, 8, 16
food_cons_stage = [1, 0, 1, 2, 4, 8, 16, 1, 1]
food_cons = food.mul(food_cons_stage, axis= 1)
food_cons['food_consum'] = food_cons[sum_list].sum(axis=1)
food_cons['food_consum_acu'] = food_cons['food_consum'].cumsum()
food_cons_total = food_cons.loc[food_cons['food_consum_acu'] > food_on_plate]
food_cons_total_1 = food_cons_total['t'].head(1)
food_hour = int(food_cons_total_1)
food_hour_list.append(int(food_hour))

food_dist = sum_all[food_hour-1:food_hour]

y_starved = int(food_dist['Total_number'])

sum_great_dis = food_dist


distribution = pd.DataFrame.copy(res)
for t in range(hours-2, 0, -1):
    distribution.iloc[t] -= distribution.iloc[t-1]
    distribution['t'] = res['t']

sum_dist = pd.DataFrame.copy(distribution)
sum_dist['Total_number'] = sum_dist[sum_list].sum(axis=1)
sum_dist = sum_dist.drop(sum_list, axis=1)




from plotnine import ggplot
from plotnine import geom_bar, aes


######################################################################################
# without eggs / with larve + adults
res_plot_a = res[[ 't', 'L1', 'L2', 'L3', 'L4', 'A']]
res_plot_a_sum = copy.deepcopy(res_plot_a)
res_plot_a_sum['sum'] = res_plot_a_sum[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
res_plot_a_sum = res_plot_a_sum.loc[:,"L1":"A"].div(res_plot_a_sum["sum"], axis=0)
res_plot_a_sum['t'] = res_plot_a['t']


sum_great_dis_sum = copy.deepcopy(sum_great_dis)
sum_great_dis_sum['sum'] = sum_great_dis[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
sum_great_dis_sum = sum_great_dis_sum.loc[:, "L1":"A"].div(sum_great_dis_sum["sum"],axis=0) * 100
sum_great_dis_sum['t'] = sum_great_dis['t']

res_plot_a_sum2 = pd.melt(res_plot_a, id_vars="t")
res_plot_a_sum_plot = pd.melt(res_plot_a_sum, id_vars="t")
sum_great_dis_plot = pd.melt(sum_great_dis_sum, id_vars="t")
print(sum_great_dis_plot)


# Stacked
import matplotlib.pyplot as plt
import plotnine as p9
from matplotlib import gridspec
from plotnine import data
from mizani.formatters import scientific_format

p4 = (p9.ggplot(sum_great_dis_plot, aes(fill='variable', y= 'value', x= ['L1', 'L2', 'L3', 'L4', 'A' ]))
    + p9.scale_x_discrete(limits= ('L1', 'L2', 'L3', 'L4', 'A'))
    + p9.geom_bar(position="stack", stat="identity")
    + p9.ylim(0,100)
    + p9.geom_text(mapping=aes(label='value'), format_string='{:.1f}', va="bottom")
    + p9.theme_linedraw())

df1 = df1.iloc[0:0]
res = res.iloc[0:0]

founders_n = 200
hours = 200
food_on_plate = 10000000

def worm_at_25():
# Create a schedule for worm development at 25C
    df1 = pd.DataFrame({'Stages_name': [], 'Stages_detail': [], 'Numbers': [], 'Progeny/hour': []})
    temp = []
    for i in range(0,10):
        temp.append({"Stages_name": "Egg", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
    
    for i in range(10,19):
        temp.append({"Stages_name": "L1", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(19,27):
        temp.append({"Stages_name": "L2", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(27,32):
        temp.append({"Stages_name": "L3", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(32,40):
        temp.append({"Stages_name": "L4", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(40,47):
        temp.append({"Stages_name": "A_nf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(47,89):
        temp.append({"Stages_name": "A_f", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(89,240):
        temp.append({"Stages_name": "A_pf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    df1 = pd.DataFrame(temp)
    # Filling egg laying schedule
    # total number of eggs at 25C = 170
    for i in range(47,49):
        df1.iloc[i,3] = 1
    for i in range(49,51):
        df1.iloc[i,3] = 2
    for i in range(51,53):
        df1.iloc[i,3] = 3
    for i in range(53,55):
        df1.iloc[i,3] = 4
    for i in range(55,57):
        df1.iloc[i,3] = 5
    for i in range(57,59):
        df1.iloc[i,3] = 6
    for i in range(59,61):
        df1.iloc[i,3] = 7
    for i in range(61,63):
        df1.iloc[i,3] = 8
    for i in range(63,66):
        df1.iloc[i,3] = 7
    for i in range(66,70):
        df1.iloc[i,3] = 6
    for i in range(70,73):
        df1.iloc[i,3] = 5
    for i in range(73,76):
        df1.iloc[i,3] = 4
    for i in range(76,80):
        df1.iloc[i,3] = 3
    for i in range(80,85):
        df1.iloc[i,3] = 2
    for i in range(85,89):
        df1.iloc[i,3] = 1
    
    return df1

df1 = worm_at_25()

res = pd.DataFrame({'t': [], 'Eggs': [], 'L1': [], 'L2': [], 'L3': [], 
                    'L4': [], 'A': [], 'YA': [], 'PA': []})

##### initialize

# put the number of L4 founders
df1.iloc[39,2] = founders_n

##### Run first simulation 
df_list = {}
for t in range(1, hours):
    for step in range(239, 0, -1):
       df1.iloc[step, 2] = df1.iloc[step-1, 2]
       df1.iloc[step-1, 2] = 0
    df1.iloc[0, 2] = (df1.iloc[47:89, 2]*df1.iloc[47:89, 3]).sum() 
    
    df_list['t_'+str(t)] = df1
    r = []
    r.append( t )    # t
    r.append( df1.loc[df1['Stages_name']=='Eggs', 'Numbers'].sum())   # Eggs 
    r.append( df1.loc[df1['Stages_name']=='L1', 'Numbers'].sum() )   # L1
    r.append( df1.loc[df1['Stages_name']=='L2', 'Numbers'].sum() )   # L2
    r.append( df1.loc[df1['Stages_name']=='L3', 'Numbers'].sum() )   # L3
    r.append( df1.loc[df1['Stages_name']=='L4', 'Numbers'].sum() )   # L4
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f')|(df1['Stages_name']=='A_pf'), 'Numbers'].sum() )  # A
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f'), 'Numbers'].sum() )   # YA
    r.append( df1.loc[(df1['Stages_name']=='A_pf'), 'Numbers'].sum() ) #PA
    res = res.append(pd.Series(r, index=['t', 'Eggs', 'L1', 'L2', 'L3', 'L4', 'A', 'YA', 'PA']), ignore_index=True)


#sum column
sum_all = pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
sum_all['Total_number'] = sum_all[sum_list].sum(axis=1)


#find food consumption 
food= pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
#set food intake ratio 1, 2, 4, 8, 16
food_cons_stage = [1, 0, 1, 2, 4, 8, 16, 1, 1]
food_cons = food.mul(food_cons_stage, axis= 1)
food_cons['food_consum'] = food_cons[sum_list].sum(axis=1)
food_cons['food_consum_acu'] = food_cons['food_consum'].cumsum()
food_cons_total = food_cons.loc[food_cons['food_consum_acu'] > food_on_plate]
food_cons_total_1 = food_cons_total['t'].head(1)
food_hour = int(food_cons_total_1)
food_hour_list.append(int(food_hour))

food_dist = sum_all[food_hour-1:food_hour]

y_starved = int(food_dist['Total_number'])

sum_great_dis = food_dist


distribution = pd.DataFrame.copy(res)
for t in range(hours-2, 0, -1):
    distribution.iloc[t] -= distribution.iloc[t-1]
    distribution['t'] = res['t']

sum_dist = pd.DataFrame.copy(distribution)
sum_dist['Total_number'] = sum_dist[sum_list].sum(axis=1)
sum_dist = sum_dist.drop(sum_list, axis=1)




from plotnine import ggplot
from plotnine import geom_bar, aes


######################################################################################
# without eggs / with larve + adults
res_plot_a = res[[ 't', 'L1', 'L2', 'L3', 'L4', 'A']]
res_plot_a_sum = copy.deepcopy(res_plot_a)
res_plot_a_sum['sum'] = res_plot_a_sum[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
res_plot_a_sum = res_plot_a_sum.loc[:,"L1":"A"].div(res_plot_a_sum["sum"], axis=0)
res_plot_a_sum['t'] = res_plot_a['t']


sum_great_dis_sum = copy.deepcopy(sum_great_dis)
sum_great_dis_sum['sum'] = sum_great_dis[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
sum_great_dis_sum = sum_great_dis_sum.loc[:, "L1":"A"].div(sum_great_dis_sum["sum"],axis=0) * 100
sum_great_dis_sum['t'] = sum_great_dis['t']

res_plot_a_sum2 = pd.melt(res_plot_a, id_vars="t")
res_plot_a_sum_plot = pd.melt(res_plot_a_sum, id_vars="t")
sum_great_dis_plot = pd.melt(sum_great_dis_sum, id_vars="t")
print(sum_great_dis_plot)


# Stacked
import matplotlib.pyplot as plt
import plotnine as p9
from matplotlib import gridspec
from plotnine import data
from mizani.formatters import scientific_format

p5 = (p9.ggplot(sum_great_dis_plot, aes(fill='variable', y= 'value', x= ['L1', 'L2', 'L3', 'L4', 'A' ]))
    + p9.scale_x_discrete(limits= ('L1', 'L2', 'L3', 'L4', 'A'))
    + p9.geom_bar(position="stack", stat="identity")
    + p9.ylim(0,100)
    + p9.geom_text(mapping=aes(label='value'), format_string='{:.1f}', va="bottom")
    + p9.theme_linedraw())

df1 = df1.iloc[0:0]
res = res.iloc[0:0]


founders_n = 1
hours = 200
food_on_plate = 50000000

def worm_at_25():
# Create a schedule for worm development at 25C
    df1 = pd.DataFrame({'Stages_name': [], 'Stages_detail': [], 'Numbers': [], 'Progeny/hour': []})
    temp = []
    for i in range(0,10):
        temp.append({"Stages_name": "Egg", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
    
    for i in range(10,19):
        temp.append({"Stages_name": "L1", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(19,27):
        temp.append({"Stages_name": "L2", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(27,32):
        temp.append({"Stages_name": "L3", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(32,40):
        temp.append({"Stages_name": "L4", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(40,47):
        temp.append({"Stages_name": "A_nf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(47,89):
        temp.append({"Stages_name": "A_f", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(89,240):
        temp.append({"Stages_name": "A_pf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    df1 = pd.DataFrame(temp)
    # Filling egg laying schedule
    # total number of eggs at 25C = 170
    for i in range(47,49):
        df1.iloc[i,3] = 1
    for i in range(49,51):
        df1.iloc[i,3] = 2
    for i in range(51,53):
        df1.iloc[i,3] = 3
    for i in range(53,55):
        df1.iloc[i,3] = 4
    for i in range(55,57):
        df1.iloc[i,3] = 5
    for i in range(57,59):
        df1.iloc[i,3] = 6
    for i in range(59,61):
        df1.iloc[i,3] = 7
    for i in range(61,63):
        df1.iloc[i,3] = 8
    for i in range(63,66):
        df1.iloc[i,3] = 7
    for i in range(66,70):
        df1.iloc[i,3] = 6
    for i in range(70,73):
        df1.iloc[i,3] = 5
    for i in range(73,76):
        df1.iloc[i,3] = 4
    for i in range(76,80):
        df1.iloc[i,3] = 3
    for i in range(80,85):
        df1.iloc[i,3] = 2
    for i in range(85,89):
        df1.iloc[i,3] = 1
    
    return df1

df1 = worm_at_25()

res = pd.DataFrame({'t': [], 'Eggs': [], 'L1': [], 'L2': [], 'L3': [], 
                    'L4': [], 'A': [], 'YA': [], 'PA': []})

##### initialize

# put the number of L4 founders
df1.iloc[39,2] = founders_n

##### Run first simulation 
df_list = {}
for t in range(1, hours):
    for step in range(239, 0, -1):
       df1.iloc[step, 2] = df1.iloc[step-1, 2]
       df1.iloc[step-1, 2] = 0
    df1.iloc[0, 2] = (df1.iloc[47:89, 2]*df1.iloc[47:89, 3]).sum() 
    
    df_list['t_'+str(t)] = df1
    r = []
    r.append( t )    # t
    r.append( df1.loc[df1['Stages_name']=='Eggs', 'Numbers'].sum())   # Eggs 
    r.append( df1.loc[df1['Stages_name']=='L1', 'Numbers'].sum() )   # L1
    r.append( df1.loc[df1['Stages_name']=='L2', 'Numbers'].sum() )   # L2
    r.append( df1.loc[df1['Stages_name']=='L3', 'Numbers'].sum() )   # L3
    r.append( df1.loc[df1['Stages_name']=='L4', 'Numbers'].sum() )   # L4
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f')|(df1['Stages_name']=='A_pf'), 'Numbers'].sum() )  # A
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f'), 'Numbers'].sum() )   # YA
    r.append( df1.loc[(df1['Stages_name']=='A_pf'), 'Numbers'].sum() ) #PA
    res = res.append(pd.Series(r, index=['t', 'Eggs', 'L1', 'L2', 'L3', 'L4', 'A', 'YA', 'PA']), ignore_index=True)


#sum column
sum_all = pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
sum_all['Total_number'] = sum_all[sum_list].sum(axis=1)


#find food consumption 
food= pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
#set food intake ratio 1, 2, 4, 8, 16
food_cons_stage = [1, 0, 1, 2, 4, 8, 16, 1, 1]
food_cons = food.mul(food_cons_stage, axis= 1)
food_cons['food_consum'] = food_cons[sum_list].sum(axis=1)
food_cons['food_consum_acu'] = food_cons['food_consum'].cumsum()
food_cons_total = food_cons.loc[food_cons['food_consum_acu'] > food_on_plate]
food_cons_total_1 = food_cons_total['t'].head(1)
food_hour = int(food_cons_total_1)
food_hour_list.append(int(food_hour))

food_dist = sum_all[food_hour-1:food_hour]

y_starved = int(food_dist['Total_number'])

sum_great_dis = food_dist


distribution = pd.DataFrame.copy(res)
for t in range(hours-2, 0, -1):
    distribution.iloc[t] -= distribution.iloc[t-1]
    distribution['t'] = res['t']

sum_dist = pd.DataFrame.copy(distribution)
sum_dist['Total_number'] = sum_dist[sum_list].sum(axis=1)
sum_dist = sum_dist.drop(sum_list, axis=1)




from plotnine import ggplot
from plotnine import geom_bar, aes


######################################################################################
# without eggs / with larve + adults
res_plot_a = res[[ 't', 'L1', 'L2', 'L3', 'L4', 'A']]
res_plot_a_sum = copy.deepcopy(res_plot_a)
res_plot_a_sum['sum'] = res_plot_a_sum[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
res_plot_a_sum = res_plot_a_sum.loc[:,"L1":"A"].div(res_plot_a_sum["sum"], axis=0)
res_plot_a_sum['t'] = res_plot_a['t']


sum_great_dis_sum = copy.deepcopy(sum_great_dis)
sum_great_dis_sum['sum'] = sum_great_dis[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
sum_great_dis_sum = sum_great_dis_sum.loc[:, "L1":"A"].div(sum_great_dis_sum["sum"],axis=0) * 100
sum_great_dis_sum['t'] = sum_great_dis['t']

res_plot_a_sum2 = pd.melt(res_plot_a, id_vars="t")
res_plot_a_sum_plot = pd.melt(res_plot_a_sum, id_vars="t")
sum_great_dis_plot = pd.melt(sum_great_dis_sum, id_vars="t")
print(sum_great_dis_plot)


# Stacked
import matplotlib.pyplot as plt
import plotnine as p9
from matplotlib import gridspec
from plotnine import data
from mizani.formatters import scientific_format

p6 = (p9.ggplot(sum_great_dis_plot, aes(fill='variable', y= 'value', x= ['L1', 'L2', 'L3', 'L4', 'A' ]))
    + p9.scale_x_discrete(limits= ('L1', 'L2', 'L3', 'L4', 'A'))
    + p9.geom_bar(position="stack", stat="identity")
    + p9.ylim(0,100)
    + p9.geom_text(mapping=aes(label='value'), format_string='{:.1f}', va="bottom")
    + p9.theme_linedraw())

df1 = df1.iloc[0:0]
res = res.iloc[0:0]



founders_n = 3
hours = 200
food_on_plate = 50000000

def worm_at_25():
# Create a schedule for worm development at 25C
    df1 = pd.DataFrame({'Stages_name': [], 'Stages_detail': [], 'Numbers': [], 'Progeny/hour': []})
    temp = []
    for i in range(0,10):
        temp.append({"Stages_name": "Egg", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
    
    for i in range(10,19):
        temp.append({"Stages_name": "L1", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(19,27):
        temp.append({"Stages_name": "L2", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(27,32):
        temp.append({"Stages_name": "L3", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(32,40):
        temp.append({"Stages_name": "L4", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(40,47):
        temp.append({"Stages_name": "A_nf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(47,89):
        temp.append({"Stages_name": "A_f", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(89,240):
        temp.append({"Stages_name": "A_pf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    df1 = pd.DataFrame(temp)
    # Filling egg laying schedule
    # total number of eggs at 25C = 170
    for i in range(47,49):
        df1.iloc[i,3] = 1
    for i in range(49,51):
        df1.iloc[i,3] = 2
    for i in range(51,53):
        df1.iloc[i,3] = 3
    for i in range(53,55):
        df1.iloc[i,3] = 4
    for i in range(55,57):
        df1.iloc[i,3] = 5
    for i in range(57,59):
        df1.iloc[i,3] = 6
    for i in range(59,61):
        df1.iloc[i,3] = 7
    for i in range(61,63):
        df1.iloc[i,3] = 8
    for i in range(63,66):
        df1.iloc[i,3] = 7
    for i in range(66,70):
        df1.iloc[i,3] = 6
    for i in range(70,73):
        df1.iloc[i,3] = 5
    for i in range(73,76):
        df1.iloc[i,3] = 4
    for i in range(76,80):
        df1.iloc[i,3] = 3
    for i in range(80,85):
        df1.iloc[i,3] = 2
    for i in range(85,89):
        df1.iloc[i,3] = 1
    
    return df1

df1 = worm_at_25()

res = pd.DataFrame({'t': [], 'Eggs': [], 'L1': [], 'L2': [], 'L3': [], 
                    'L4': [], 'A': [], 'YA': [], 'PA': []})

##### initialize

# put the number of L4 founders
df1.iloc[39,2] = founders_n

##### Run first simulation 
df_list = {}
for t in range(1, hours):
    for step in range(239, 0, -1):
       df1.iloc[step, 2] = df1.iloc[step-1, 2]
       df1.iloc[step-1, 2] = 0
    df1.iloc[0, 2] = (df1.iloc[47:89, 2]*df1.iloc[47:89, 3]).sum() 
    
    df_list['t_'+str(t)] = df1
    r = []
    r.append( t )    # t
    r.append( df1.loc[df1['Stages_name']=='Eggs', 'Numbers'].sum())   # Eggs 
    r.append( df1.loc[df1['Stages_name']=='L1', 'Numbers'].sum() )   # L1
    r.append( df1.loc[df1['Stages_name']=='L2', 'Numbers'].sum() )   # L2
    r.append( df1.loc[df1['Stages_name']=='L3', 'Numbers'].sum() )   # L3
    r.append( df1.loc[df1['Stages_name']=='L4', 'Numbers'].sum() )   # L4
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f')|(df1['Stages_name']=='A_pf'), 'Numbers'].sum() )  # A
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f'), 'Numbers'].sum() )   # YA
    r.append( df1.loc[(df1['Stages_name']=='A_pf'), 'Numbers'].sum() ) #PA
    res = res.append(pd.Series(r, index=['t', 'Eggs', 'L1', 'L2', 'L3', 'L4', 'A', 'YA', 'PA']), ignore_index=True)


#sum column
sum_all = pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
sum_all['Total_number'] = sum_all[sum_list].sum(axis=1)


#find food consumption 
food= pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
#set food intake ratio 1, 2, 4, 8, 16
food_cons_stage = [1, 0, 1, 2, 4, 8, 16, 1, 1]
food_cons = food.mul(food_cons_stage, axis= 1)
food_cons['food_consum'] = food_cons[sum_list].sum(axis=1)
food_cons['food_consum_acu'] = food_cons['food_consum'].cumsum()
food_cons_total = food_cons.loc[food_cons['food_consum_acu'] > food_on_plate]
food_cons_total_1 = food_cons_total['t'].head(1)
food_hour = int(food_cons_total_1)
food_hour_list.append(int(food_hour))

food_dist = sum_all[food_hour-1:food_hour]

y_starved = int(food_dist['Total_number'])

sum_great_dis = food_dist


distribution = pd.DataFrame.copy(res)
for t in range(hours-2, 0, -1):
    distribution.iloc[t] -= distribution.iloc[t-1]
    distribution['t'] = res['t']

sum_dist = pd.DataFrame.copy(distribution)
sum_dist['Total_number'] = sum_dist[sum_list].sum(axis=1)
sum_dist = sum_dist.drop(sum_list, axis=1)




from plotnine import ggplot
from plotnine import geom_bar, aes


######################################################################################
# without eggs / with larve + adults
res_plot_a = res[[ 't', 'L1', 'L2', 'L3', 'L4', 'A']]
res_plot_a_sum = copy.deepcopy(res_plot_a)
res_plot_a_sum['sum'] = res_plot_a_sum[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
res_plot_a_sum = res_plot_a_sum.loc[:,"L1":"A"].div(res_plot_a_sum["sum"], axis=0)
res_plot_a_sum['t'] = res_plot_a['t']


sum_great_dis_sum = copy.deepcopy(sum_great_dis)
sum_great_dis_sum['sum'] = sum_great_dis[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
sum_great_dis_sum = sum_great_dis_sum.loc[:, "L1":"A"].div(sum_great_dis_sum["sum"],axis=0) * 100
sum_great_dis_sum['t'] = sum_great_dis['t']

res_plot_a_sum2 = pd.melt(res_plot_a, id_vars="t")
res_plot_a_sum_plot = pd.melt(res_plot_a_sum, id_vars="t")
sum_great_dis_plot = pd.melt(sum_great_dis_sum, id_vars="t")
print(sum_great_dis_plot)


# Stacked
import matplotlib.pyplot as plt
import plotnine as p9
from matplotlib import gridspec
from plotnine import data
from mizani.formatters import scientific_format

p7 = (p9.ggplot(sum_great_dis_plot, aes(fill='variable', y= 'value', x= ['L1', 'L2', 'L3', 'L4', 'A' ]))
    + p9.scale_x_discrete(limits= ('L1', 'L2', 'L3', 'L4', 'A'))
    + p9.geom_bar(position="stack", stat="identity")
    + p9.ylim(0,100)
    + p9.geom_text(mapping=aes(label='value'), format_string='{:.1f}', va="bottom")
    + p9.theme_linedraw())

df1 = df1.iloc[0:0]
res = res.iloc[0:0]

founders_n = 10
hours = 200
food_on_plate = 50000000

def worm_at_25():
# Create a schedule for worm development at 25C
    df1 = pd.DataFrame({'Stages_name': [], 'Stages_detail': [], 'Numbers': [], 'Progeny/hour': []})
    temp = []
    for i in range(0,10):
        temp.append({"Stages_name": "Egg", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
    
    for i in range(10,19):
        temp.append({"Stages_name": "L1", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(19,27):
        temp.append({"Stages_name": "L2", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(27,32):
        temp.append({"Stages_name": "L3", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(32,40):
        temp.append({"Stages_name": "L4", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(40,47):
        temp.append({"Stages_name": "A_nf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(47,89):
        temp.append({"Stages_name": "A_f", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(89,240):
        temp.append({"Stages_name": "A_pf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    df1 = pd.DataFrame(temp)
    # Filling egg laying schedule
    # total number of eggs at 25C = 170
    for i in range(47,49):
        df1.iloc[i,3] = 1
    for i in range(49,51):
        df1.iloc[i,3] = 2
    for i in range(51,53):
        df1.iloc[i,3] = 3
    for i in range(53,55):
        df1.iloc[i,3] = 4
    for i in range(55,57):
        df1.iloc[i,3] = 5
    for i in range(57,59):
        df1.iloc[i,3] = 6
    for i in range(59,61):
        df1.iloc[i,3] = 7
    for i in range(61,63):
        df1.iloc[i,3] = 8
    for i in range(63,66):
        df1.iloc[i,3] = 7
    for i in range(66,70):
        df1.iloc[i,3] = 6
    for i in range(70,73):
        df1.iloc[i,3] = 5
    for i in range(73,76):
        df1.iloc[i,3] = 4
    for i in range(76,80):
        df1.iloc[i,3] = 3
    for i in range(80,85):
        df1.iloc[i,3] = 2
    for i in range(85,89):
        df1.iloc[i,3] = 1
    
    return df1

df1 = worm_at_25()

res = pd.DataFrame({'t': [], 'Eggs': [], 'L1': [], 'L2': [], 'L3': [], 
                    'L4': [], 'A': [], 'YA': [], 'PA': []})

##### initialize

# put the number of L4 founders
df1.iloc[39,2] = founders_n

##### Run first simulation 
df_list = {}
for t in range(1, hours):
    for step in range(239, 0, -1):
       df1.iloc[step, 2] = df1.iloc[step-1, 2]
       df1.iloc[step-1, 2] = 0
    df1.iloc[0, 2] = (df1.iloc[47:89, 2]*df1.iloc[47:89, 3]).sum() 
    
    df_list['t_'+str(t)] = df1
    r = []
    r.append( t )    # t
    r.append( df1.loc[df1['Stages_name']=='Eggs', 'Numbers'].sum())   # Eggs 
    r.append( df1.loc[df1['Stages_name']=='L1', 'Numbers'].sum() )   # L1
    r.append( df1.loc[df1['Stages_name']=='L2', 'Numbers'].sum() )   # L2
    r.append( df1.loc[df1['Stages_name']=='L3', 'Numbers'].sum() )   # L3
    r.append( df1.loc[df1['Stages_name']=='L4', 'Numbers'].sum() )   # L4
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f')|(df1['Stages_name']=='A_pf'), 'Numbers'].sum() )  # A
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f'), 'Numbers'].sum() )   # YA
    r.append( df1.loc[(df1['Stages_name']=='A_pf'), 'Numbers'].sum() ) #PA
    res = res.append(pd.Series(r, index=['t', 'Eggs', 'L1', 'L2', 'L3', 'L4', 'A', 'YA', 'PA']), ignore_index=True)


#sum column
sum_all = pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
sum_all['Total_number'] = sum_all[sum_list].sum(axis=1)


#find food consumption 
food= pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
#set food intake ratio 1, 2, 4, 8, 16
food_cons_stage = [1, 0, 1, 2, 4, 8, 16, 1, 1]
food_cons = food.mul(food_cons_stage, axis= 1)
food_cons['food_consum'] = food_cons[sum_list].sum(axis=1)
food_cons['food_consum_acu'] = food_cons['food_consum'].cumsum()
food_cons_total = food_cons.loc[food_cons['food_consum_acu'] > food_on_plate]
food_cons_total_1 = food_cons_total['t'].head(1)
food_hour = int(food_cons_total_1)
food_hour_list.append(int(food_hour))

food_dist = sum_all[food_hour-1:food_hour]

y_starved = int(food_dist['Total_number'])

sum_great_dis = food_dist


distribution = pd.DataFrame.copy(res)
for t in range(hours-2, 0, -1):
    distribution.iloc[t] -= distribution.iloc[t-1]
    distribution['t'] = res['t']

sum_dist = pd.DataFrame.copy(distribution)
sum_dist['Total_number'] = sum_dist[sum_list].sum(axis=1)
sum_dist = sum_dist.drop(sum_list, axis=1)




from plotnine import ggplot
from plotnine import geom_bar, aes


######################################################################################
# without eggs / with larve + adults
res_plot_a = res[[ 't', 'L1', 'L2', 'L3', 'L4', 'A']]
res_plot_a_sum = copy.deepcopy(res_plot_a)
res_plot_a_sum['sum'] = res_plot_a_sum[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
res_plot_a_sum = res_plot_a_sum.loc[:,"L1":"A"].div(res_plot_a_sum["sum"], axis=0)
res_plot_a_sum['t'] = res_plot_a['t']


sum_great_dis_sum = copy.deepcopy(sum_great_dis)
sum_great_dis_sum['sum'] = sum_great_dis[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
sum_great_dis_sum = sum_great_dis_sum.loc[:, "L1":"A"].div(sum_great_dis_sum["sum"],axis=0) * 100
sum_great_dis_sum['t'] = sum_great_dis['t']

res_plot_a_sum2 = pd.melt(res_plot_a, id_vars="t")
res_plot_a_sum_plot = pd.melt(res_plot_a_sum, id_vars="t")
sum_great_dis_plot = pd.melt(sum_great_dis_sum, id_vars="t")
print(sum_great_dis_plot)


# Stacked
import matplotlib.pyplot as plt
import plotnine as p9
from matplotlib import gridspec
from plotnine import data
from mizani.formatters import scientific_format

p8 = (p9.ggplot(sum_great_dis_plot, aes(fill='variable', y= 'value', x= ['L1', 'L2', 'L3', 'L4', 'A' ]))
    + p9.scale_x_discrete(limits= ('L1', 'L2', 'L3', 'L4', 'A'))
    + p9.geom_bar(position="stack", stat="identity")
    + p9.ylim(0,100)
    + p9.geom_text(mapping=aes(label='value'), format_string='{:.1f}', va="bottom")
    + p9.theme_linedraw())

df1 = df1.iloc[0:0]
res = res.iloc[0:0]

founders_n = 50
hours = 200
food_on_plate = 50000000

def worm_at_25():
# Create a schedule for worm development at 25C
    df1 = pd.DataFrame({'Stages_name': [], 'Stages_detail': [], 'Numbers': [], 'Progeny/hour': []})
    temp = []
    for i in range(0,10):
        temp.append({"Stages_name": "Egg", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
    
    for i in range(10,19):
        temp.append({"Stages_name": "L1", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(19,27):
        temp.append({"Stages_name": "L2", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(27,32):
        temp.append({"Stages_name": "L3", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(32,40):
        temp.append({"Stages_name": "L4", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(40,47):
        temp.append({"Stages_name": "A_nf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(47,89):
        temp.append({"Stages_name": "A_f", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(89,240):
        temp.append({"Stages_name": "A_pf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    df1 = pd.DataFrame(temp)
    # Filling egg laying schedule
    # total number of eggs at 25C = 170
    for i in range(47,49):
        df1.iloc[i,3] = 1
    for i in range(49,51):
        df1.iloc[i,3] = 2
    for i in range(51,53):
        df1.iloc[i,3] = 3
    for i in range(53,55):
        df1.iloc[i,3] = 4
    for i in range(55,57):
        df1.iloc[i,3] = 5
    for i in range(57,59):
        df1.iloc[i,3] = 6
    for i in range(59,61):
        df1.iloc[i,3] = 7
    for i in range(61,63):
        df1.iloc[i,3] = 8
    for i in range(63,66):
        df1.iloc[i,3] = 7
    for i in range(66,70):
        df1.iloc[i,3] = 6
    for i in range(70,73):
        df1.iloc[i,3] = 5
    for i in range(73,76):
        df1.iloc[i,3] = 4
    for i in range(76,80):
        df1.iloc[i,3] = 3
    for i in range(80,85):
        df1.iloc[i,3] = 2
    for i in range(85,89):
        df1.iloc[i,3] = 1
    
    return df1

df1 = worm_at_25()

res = pd.DataFrame({'t': [], 'Eggs': [], 'L1': [], 'L2': [], 'L3': [], 
                    'L4': [], 'A': [], 'YA': [], 'PA': []})

##### initialize

# put the number of L4 founders
df1.iloc[39,2] = founders_n

##### Run first simulation 
df_list = {}
for t in range(1, hours):
    for step in range(239, 0, -1):
       df1.iloc[step, 2] = df1.iloc[step-1, 2]
       df1.iloc[step-1, 2] = 0
    df1.iloc[0, 2] = (df1.iloc[47:89, 2]*df1.iloc[47:89, 3]).sum() 
    
    df_list['t_'+str(t)] = df1
    r = []
    r.append( t )    # t
    r.append( df1.loc[df1['Stages_name']=='Eggs', 'Numbers'].sum())   # Eggs 
    r.append( df1.loc[df1['Stages_name']=='L1', 'Numbers'].sum() )   # L1
    r.append( df1.loc[df1['Stages_name']=='L2', 'Numbers'].sum() )   # L2
    r.append( df1.loc[df1['Stages_name']=='L3', 'Numbers'].sum() )   # L3
    r.append( df1.loc[df1['Stages_name']=='L4', 'Numbers'].sum() )   # L4
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f')|(df1['Stages_name']=='A_pf'), 'Numbers'].sum() )  # A
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f'), 'Numbers'].sum() )   # YA
    r.append( df1.loc[(df1['Stages_name']=='A_pf'), 'Numbers'].sum() ) #PA
    res = res.append(pd.Series(r, index=['t', 'Eggs', 'L1', 'L2', 'L3', 'L4', 'A', 'YA', 'PA']), ignore_index=True)


#sum column
sum_all = pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
sum_all['Total_number'] = sum_all[sum_list].sum(axis=1)


#find food consumption 
food= pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
#set food intake ratio 1, 2, 4, 8, 16
food_cons_stage = [1, 0, 1, 2, 4, 8, 16, 1, 1]
food_cons = food.mul(food_cons_stage, axis= 1)
food_cons['food_consum'] = food_cons[sum_list].sum(axis=1)
food_cons['food_consum_acu'] = food_cons['food_consum'].cumsum()
food_cons_total = food_cons.loc[food_cons['food_consum_acu'] > food_on_plate]
food_cons_total_1 = food_cons_total['t'].head(1)
food_hour = int(food_cons_total_1)
food_hour_list.append(int(food_hour))

food_dist = sum_all[food_hour-1:food_hour]

y_starved = int(food_dist['Total_number'])

sum_great_dis = food_dist


distribution = pd.DataFrame.copy(res)
for t in range(hours-2, 0, -1):
    distribution.iloc[t] -= distribution.iloc[t-1]
    distribution['t'] = res['t']

sum_dist = pd.DataFrame.copy(distribution)
sum_dist['Total_number'] = sum_dist[sum_list].sum(axis=1)
sum_dist = sum_dist.drop(sum_list, axis=1)




from plotnine import ggplot
from plotnine import geom_bar, aes


######################################################################################
# without eggs / with larve + adults
res_plot_a = res[[ 't', 'L1', 'L2', 'L3', 'L4', 'A']]
res_plot_a_sum = copy.deepcopy(res_plot_a)
res_plot_a_sum['sum'] = res_plot_a_sum[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
res_plot_a_sum = res_plot_a_sum.loc[:,"L1":"A"].div(res_plot_a_sum["sum"], axis=0)
res_plot_a_sum['t'] = res_plot_a['t']


sum_great_dis_sum = copy.deepcopy(sum_great_dis)
sum_great_dis_sum['sum'] = sum_great_dis[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
sum_great_dis_sum = sum_great_dis_sum.loc[:, "L1":"A"].div(sum_great_dis_sum["sum"],axis=0) * 100
sum_great_dis_sum['t'] = sum_great_dis['t']

res_plot_a_sum2 = pd.melt(res_plot_a, id_vars="t")
res_plot_a_sum_plot = pd.melt(res_plot_a_sum, id_vars="t")
sum_great_dis_plot = pd.melt(sum_great_dis_sum, id_vars="t")
print(sum_great_dis_plot)


# Stacked
import matplotlib.pyplot as plt
import plotnine as p9
from matplotlib import gridspec
from plotnine import data
from mizani.formatters import scientific_format

p9a = (p9.ggplot(sum_great_dis_plot, aes(fill='variable', y= 'value', x= ['L1', 'L2', 'L3', 'L4', 'A' ]))
    + p9.scale_x_discrete(limits= ('L1', 'L2', 'L3', 'L4', 'A'))
    + p9.geom_bar(position="stack", stat="identity")
    + p9.ylim(0,100)
    + p9.geom_text(mapping=aes(label='value'), format_string='{:.1f}', va="bottom")
    + p9.theme_linedraw())

df1 = df1.iloc[0:0]
res = res.iloc[0:0]

founders_n = 200
hours = 200
food_on_plate = 50000000

def worm_at_25():
# Create a schedule for worm development at 25C
    df1 = pd.DataFrame({'Stages_name': [], 'Stages_detail': [], 'Numbers': [], 'Progeny/hour': []})
    temp = []
    for i in range(0,10):
        temp.append({"Stages_name": "Egg", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
    
    for i in range(10,19):
        temp.append({"Stages_name": "L1", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(19,27):
        temp.append({"Stages_name": "L2", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(27,32):
        temp.append({"Stages_name": "L3", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(32,40):
        temp.append({"Stages_name": "L4", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(40,47):
        temp.append({"Stages_name": "A_nf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(47,89):
        temp.append({"Stages_name": "A_f", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(89,240):
        temp.append({"Stages_name": "A_pf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    df1 = pd.DataFrame(temp)
    # Filling egg laying schedule
    # total number of eggs at 25C = 170
    for i in range(47,49):
        df1.iloc[i,3] = 1
    for i in range(49,51):
        df1.iloc[i,3] = 2
    for i in range(51,53):
        df1.iloc[i,3] = 3
    for i in range(53,55):
        df1.iloc[i,3] = 4
    for i in range(55,57):
        df1.iloc[i,3] = 5
    for i in range(57,59):
        df1.iloc[i,3] = 6
    for i in range(59,61):
        df1.iloc[i,3] = 7
    for i in range(61,63):
        df1.iloc[i,3] = 8
    for i in range(63,66):
        df1.iloc[i,3] = 7
    for i in range(66,70):
        df1.iloc[i,3] = 6
    for i in range(70,73):
        df1.iloc[i,3] = 5
    for i in range(73,76):
        df1.iloc[i,3] = 4
    for i in range(76,80):
        df1.iloc[i,3] = 3
    for i in range(80,85):
        df1.iloc[i,3] = 2
    for i in range(85,89):
        df1.iloc[i,3] = 1
    
    return df1

df1 = worm_at_25()

res = pd.DataFrame({'t': [], 'Eggs': [], 'L1': [], 'L2': [], 'L3': [], 
                    'L4': [], 'A': [], 'YA': [], 'PA': []})

##### initialize

# put the number of L4 founders
df1.iloc[39,2] = founders_n

##### Run first simulation 
df_list = {}
for t in range(1, hours):
    for step in range(239, 0, -1):
       df1.iloc[step, 2] = df1.iloc[step-1, 2]
       df1.iloc[step-1, 2] = 0
    df1.iloc[0, 2] = (df1.iloc[47:89, 2]*df1.iloc[47:89, 3]).sum() 
    
    df_list['t_'+str(t)] = df1
    r = []
    r.append( t )    # t
    r.append( df1.loc[df1['Stages_name']=='Eggs', 'Numbers'].sum())   # Eggs 
    r.append( df1.loc[df1['Stages_name']=='L1', 'Numbers'].sum() )   # L1
    r.append( df1.loc[df1['Stages_name']=='L2', 'Numbers'].sum() )   # L2
    r.append( df1.loc[df1['Stages_name']=='L3', 'Numbers'].sum() )   # L3
    r.append( df1.loc[df1['Stages_name']=='L4', 'Numbers'].sum() )   # L4
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f')|(df1['Stages_name']=='A_pf'), 'Numbers'].sum() )  # A
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f'), 'Numbers'].sum() )   # YA
    r.append( df1.loc[(df1['Stages_name']=='A_pf'), 'Numbers'].sum() ) #PA
    res = res.append(pd.Series(r, index=['t', 'Eggs', 'L1', 'L2', 'L3', 'L4', 'A', 'YA', 'PA']), ignore_index=True)


#sum column
sum_all = pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
sum_all['Total_number'] = sum_all[sum_list].sum(axis=1)


#find food consumption 
food= pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
#set food intake ratio 1, 2, 4, 8, 16
food_cons_stage = [1, 0, 1, 2, 4, 8, 16, 1, 1]
food_cons = food.mul(food_cons_stage, axis= 1)
food_cons['food_consum'] = food_cons[sum_list].sum(axis=1)
food_cons['food_consum_acu'] = food_cons['food_consum'].cumsum()
food_cons_total = food_cons.loc[food_cons['food_consum_acu'] > food_on_plate]
food_cons_total_1 = food_cons_total['t'].head(1)
food_hour = int(food_cons_total_1)
food_hour_list.append(int(food_hour))

food_dist = sum_all[food_hour-1:food_hour]

y_starved = int(food_dist['Total_number'])

sum_great_dis = food_dist


distribution = pd.DataFrame.copy(res)
for t in range(hours-2, 0, -1):
    distribution.iloc[t] -= distribution.iloc[t-1]
    distribution['t'] = res['t']

sum_dist = pd.DataFrame.copy(distribution)
sum_dist['Total_number'] = sum_dist[sum_list].sum(axis=1)
sum_dist = sum_dist.drop(sum_list, axis=1)




from plotnine import ggplot
from plotnine import geom_bar, aes


######################################################################################
# without eggs / with larve + adults
res_plot_a = res[[ 't', 'L1', 'L2', 'L3', 'L4', 'A']]
res_plot_a_sum = copy.deepcopy(res_plot_a)
res_plot_a_sum['sum'] = res_plot_a_sum[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
res_plot_a_sum = res_plot_a_sum.loc[:,"L1":"A"].div(res_plot_a_sum["sum"], axis=0)
res_plot_a_sum['t'] = res_plot_a['t']


sum_great_dis_sum = copy.deepcopy(sum_great_dis)
sum_great_dis_sum['sum'] = sum_great_dis[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
sum_great_dis_sum = sum_great_dis_sum.loc[:, "L1":"A"].div(sum_great_dis_sum["sum"],axis=0) * 100
sum_great_dis_sum['t'] = sum_great_dis['t']

res_plot_a_sum2 = pd.melt(res_plot_a, id_vars="t")
res_plot_a_sum_plot = pd.melt(res_plot_a_sum, id_vars="t")
sum_great_dis_plot = pd.melt(sum_great_dis_sum, id_vars="t")
print(sum_great_dis_plot)


# Stacked
import matplotlib.pyplot as plt
import plotnine as p9
from matplotlib import gridspec
from plotnine import data
from mizani.formatters import scientific_format

p10 = (p9.ggplot(sum_great_dis_plot, aes(fill='variable', y= 'value', x= ['L1', 'L2', 'L3', 'L4', 'A' ]))
    + p9.scale_x_discrete(limits= ('L1', 'L2', 'L3', 'L4', 'A'))
    + p9.geom_bar(position="stack", stat="identity")
    + p9.ylim(0,100)
    + p9.geom_text(mapping=aes(label='value'), format_string='{:.1f}', va="bottom")
    + p9.theme_linedraw())

df1 = df1.iloc[0:0]
res = res.iloc[0:0]


founders_n = 1
hours = 200
food_on_plate = 100000000

def worm_at_25():
# Create a schedule for worm development at 25C
    df1 = pd.DataFrame({'Stages_name': [], 'Stages_detail': [], 'Numbers': [], 'Progeny/hour': []})
    temp = []
    for i in range(0,10):
        temp.append({"Stages_name": "Egg", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
    
    for i in range(10,19):
        temp.append({"Stages_name": "L1", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(19,27):
        temp.append({"Stages_name": "L2", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(27,32):
        temp.append({"Stages_name": "L3", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(32,40):
        temp.append({"Stages_name": "L4", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(40,47):
        temp.append({"Stages_name": "A_nf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(47,89):
        temp.append({"Stages_name": "A_f", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(89,240):
        temp.append({"Stages_name": "A_pf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    df1 = pd.DataFrame(temp)
    # Filling egg laying schedule
    # total number of eggs at 25C = 170
    for i in range(47,49):
        df1.iloc[i,3] = 1
    for i in range(49,51):
        df1.iloc[i,3] = 2
    for i in range(51,53):
        df1.iloc[i,3] = 3
    for i in range(53,55):
        df1.iloc[i,3] = 4
    for i in range(55,57):
        df1.iloc[i,3] = 5
    for i in range(57,59):
        df1.iloc[i,3] = 6
    for i in range(59,61):
        df1.iloc[i,3] = 7
    for i in range(61,63):
        df1.iloc[i,3] = 8
    for i in range(63,66):
        df1.iloc[i,3] = 7
    for i in range(66,70):
        df1.iloc[i,3] = 6
    for i in range(70,73):
        df1.iloc[i,3] = 5
    for i in range(73,76):
        df1.iloc[i,3] = 4
    for i in range(76,80):
        df1.iloc[i,3] = 3
    for i in range(80,85):
        df1.iloc[i,3] = 2
    for i in range(85,89):
        df1.iloc[i,3] = 1
    
    return df1

df1 = worm_at_25()

res = pd.DataFrame({'t': [], 'Eggs': [], 'L1': [], 'L2': [], 'L3': [], 
                    'L4': [], 'A': [], 'YA': [], 'PA': []})

##### initialize

# put the number of L4 founders
df1.iloc[39,2] = founders_n

##### Run first simulation 
df_list = {}
for t in range(1, hours):
    for step in range(239, 0, -1):
       df1.iloc[step, 2] = df1.iloc[step-1, 2]
       df1.iloc[step-1, 2] = 0
    df1.iloc[0, 2] = (df1.iloc[47:89, 2]*df1.iloc[47:89, 3]).sum() 
    
    df_list['t_'+str(t)] = df1
    r = []
    r.append( t )    # t
    r.append( df1.loc[df1['Stages_name']=='Eggs', 'Numbers'].sum())   # Eggs 
    r.append( df1.loc[df1['Stages_name']=='L1', 'Numbers'].sum() )   # L1
    r.append( df1.loc[df1['Stages_name']=='L2', 'Numbers'].sum() )   # L2
    r.append( df1.loc[df1['Stages_name']=='L3', 'Numbers'].sum() )   # L3
    r.append( df1.loc[df1['Stages_name']=='L4', 'Numbers'].sum() )   # L4
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f')|(df1['Stages_name']=='A_pf'), 'Numbers'].sum() )  # A
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f'), 'Numbers'].sum() )   # YA
    r.append( df1.loc[(df1['Stages_name']=='A_pf'), 'Numbers'].sum() ) #PA
    res = res.append(pd.Series(r, index=['t', 'Eggs', 'L1', 'L2', 'L3', 'L4', 'A', 'YA', 'PA']), ignore_index=True)


#sum column
sum_all = pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
sum_all['Total_number'] = sum_all[sum_list].sum(axis=1)


#find food consumption 
food= pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
#set food intake ratio 1, 2, 4, 8, 16
food_cons_stage = [1, 0, 1, 2, 4, 8, 16, 1, 1]
food_cons = food.mul(food_cons_stage, axis= 1)
food_cons['food_consum'] = food_cons[sum_list].sum(axis=1)
food_cons['food_consum_acu'] = food_cons['food_consum'].cumsum()
food_cons_total = food_cons.loc[food_cons['food_consum_acu'] > food_on_plate]
food_cons_total_1 = food_cons_total['t'].head(1)
food_hour = int(food_cons_total_1)
food_hour_list.append(int(food_hour))

food_dist = sum_all[food_hour-1:food_hour]

y_starved = int(food_dist['Total_number'])

sum_great_dis = food_dist


distribution = pd.DataFrame.copy(res)
for t in range(hours-2, 0, -1):
    distribution.iloc[t] -= distribution.iloc[t-1]
    distribution['t'] = res['t']

sum_dist = pd.DataFrame.copy(distribution)
sum_dist['Total_number'] = sum_dist[sum_list].sum(axis=1)
sum_dist = sum_dist.drop(sum_list, axis=1)




from plotnine import ggplot
from plotnine import geom_bar, aes


######################################################################################
# without eggs / with larve + adults
res_plot_a = res[[ 't', 'L1', 'L2', 'L3', 'L4', 'A']]
res_plot_a_sum = copy.deepcopy(res_plot_a)
res_plot_a_sum['sum'] = res_plot_a_sum[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
res_plot_a_sum = res_plot_a_sum.loc[:,"L1":"A"].div(res_plot_a_sum["sum"], axis=0)
res_plot_a_sum['t'] = res_plot_a['t']


sum_great_dis_sum = copy.deepcopy(sum_great_dis)
sum_great_dis_sum['sum'] = sum_great_dis[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
sum_great_dis_sum = sum_great_dis_sum.loc[:, "L1":"A"].div(sum_great_dis_sum["sum"],axis=0) * 100
sum_great_dis_sum['t'] = sum_great_dis['t']

res_plot_a_sum2 = pd.melt(res_plot_a, id_vars="t")
res_plot_a_sum_plot = pd.melt(res_plot_a_sum, id_vars="t")
sum_great_dis_plot = pd.melt(sum_great_dis_sum, id_vars="t")
print(sum_great_dis_plot)


# Stacked
import matplotlib.pyplot as plt
import plotnine as p9
from matplotlib import gridspec
from plotnine import data
from mizani.formatters import scientific_format

p11 = (p9.ggplot(sum_great_dis_plot, aes(fill='variable', y= 'value', x= ['L1', 'L2', 'L3', 'L4', 'A' ]))
    + p9.scale_x_discrete(limits= ('L1', 'L2', 'L3', 'L4', 'A'))
    + p9.geom_bar(position="stack", stat="identity")
    + p9.ylim(0,100)
    + p9.geom_text(mapping=aes(label='value'), format_string='{:.1f}', va="bottom")
    + p9.theme_linedraw())

df1 = df1.iloc[0:0]
res = res.iloc[0:0]



founders_n = 3
hours = 200
food_on_plate = 100000000

def worm_at_25():
# Create a schedule for worm development at 25C
    df1 = pd.DataFrame({'Stages_name': [], 'Stages_detail': [], 'Numbers': [], 'Progeny/hour': []})
    temp = []
    for i in range(0,10):
        temp.append({"Stages_name": "Egg", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
    
    for i in range(10,19):
        temp.append({"Stages_name": "L1", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(19,27):
        temp.append({"Stages_name": "L2", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(27,32):
        temp.append({"Stages_name": "L3", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(32,40):
        temp.append({"Stages_name": "L4", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(40,47):
        temp.append({"Stages_name": "A_nf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(47,89):
        temp.append({"Stages_name": "A_f", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(89,240):
        temp.append({"Stages_name": "A_pf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    df1 = pd.DataFrame(temp)
    # Filling egg laying schedule
    # total number of eggs at 25C = 170
    for i in range(47,49):
        df1.iloc[i,3] = 1
    for i in range(49,51):
        df1.iloc[i,3] = 2
    for i in range(51,53):
        df1.iloc[i,3] = 3
    for i in range(53,55):
        df1.iloc[i,3] = 4
    for i in range(55,57):
        df1.iloc[i,3] = 5
    for i in range(57,59):
        df1.iloc[i,3] = 6
    for i in range(59,61):
        df1.iloc[i,3] = 7
    for i in range(61,63):
        df1.iloc[i,3] = 8
    for i in range(63,66):
        df1.iloc[i,3] = 7
    for i in range(66,70):
        df1.iloc[i,3] = 6
    for i in range(70,73):
        df1.iloc[i,3] = 5
    for i in range(73,76):
        df1.iloc[i,3] = 4
    for i in range(76,80):
        df1.iloc[i,3] = 3
    for i in range(80,85):
        df1.iloc[i,3] = 2
    for i in range(85,89):
        df1.iloc[i,3] = 1
    
    return df1

df1 = worm_at_25()

res = pd.DataFrame({'t': [], 'Eggs': [], 'L1': [], 'L2': [], 'L3': [], 
                    'L4': [], 'A': [], 'YA': [], 'PA': []})

##### initialize

# put the number of L4 founders
df1.iloc[39,2] = founders_n

##### Run first simulation 
df_list = {}
for t in range(1, hours):
    for step in range(239, 0, -1):
       df1.iloc[step, 2] = df1.iloc[step-1, 2]
       df1.iloc[step-1, 2] = 0
    df1.iloc[0, 2] = (df1.iloc[47:89, 2]*df1.iloc[47:89, 3]).sum() 
    
    df_list['t_'+str(t)] = df1
    r = []
    r.append( t )    # t
    r.append( df1.loc[df1['Stages_name']=='Eggs', 'Numbers'].sum())   # Eggs 
    r.append( df1.loc[df1['Stages_name']=='L1', 'Numbers'].sum() )   # L1
    r.append( df1.loc[df1['Stages_name']=='L2', 'Numbers'].sum() )   # L2
    r.append( df1.loc[df1['Stages_name']=='L3', 'Numbers'].sum() )   # L3
    r.append( df1.loc[df1['Stages_name']=='L4', 'Numbers'].sum() )   # L4
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f')|(df1['Stages_name']=='A_pf'), 'Numbers'].sum() )  # A
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f'), 'Numbers'].sum() )   # YA
    r.append( df1.loc[(df1['Stages_name']=='A_pf'), 'Numbers'].sum() ) #PA
    res = res.append(pd.Series(r, index=['t', 'Eggs', 'L1', 'L2', 'L3', 'L4', 'A', 'YA', 'PA']), ignore_index=True)


#sum column
sum_all = pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
sum_all['Total_number'] = sum_all[sum_list].sum(axis=1)


#find food consumption 
food= pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
#set food intake ratio 1, 2, 4, 8, 16
food_cons_stage = [1, 0, 1, 2, 4, 8, 16, 1, 1]
food_cons = food.mul(food_cons_stage, axis= 1)
food_cons['food_consum'] = food_cons[sum_list].sum(axis=1)
food_cons['food_consum_acu'] = food_cons['food_consum'].cumsum()
food_cons_total = food_cons.loc[food_cons['food_consum_acu'] > food_on_plate]
food_cons_total_1 = food_cons_total['t'].head(1)
food_hour = int(food_cons_total_1)
food_hour_list.append(int(food_hour))

food_dist = sum_all[food_hour-1:food_hour]

y_starved = int(food_dist['Total_number'])

sum_great_dis = food_dist


distribution = pd.DataFrame.copy(res)
for t in range(hours-2, 0, -1):
    distribution.iloc[t] -= distribution.iloc[t-1]
    distribution['t'] = res['t']

sum_dist = pd.DataFrame.copy(distribution)
sum_dist['Total_number'] = sum_dist[sum_list].sum(axis=1)
sum_dist = sum_dist.drop(sum_list, axis=1)




from plotnine import ggplot
from plotnine import geom_bar, aes


######################################################################################
# without eggs / with larve + adults
res_plot_a = res[[ 't', 'L1', 'L2', 'L3', 'L4', 'A']]
res_plot_a_sum = copy.deepcopy(res_plot_a)
res_plot_a_sum['sum'] = res_plot_a_sum[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
res_plot_a_sum = res_plot_a_sum.loc[:,"L1":"A"].div(res_plot_a_sum["sum"], axis=0)
res_plot_a_sum['t'] = res_plot_a['t']


sum_great_dis_sum = copy.deepcopy(sum_great_dis)
sum_great_dis_sum['sum'] = sum_great_dis[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
sum_great_dis_sum = sum_great_dis_sum.loc[:, "L1":"A"].div(sum_great_dis_sum["sum"],axis=0) * 100
sum_great_dis_sum['t'] = sum_great_dis['t']

res_plot_a_sum2 = pd.melt(res_plot_a, id_vars="t")
res_plot_a_sum_plot = pd.melt(res_plot_a_sum, id_vars="t")
sum_great_dis_plot = pd.melt(sum_great_dis_sum, id_vars="t")
print(sum_great_dis_plot)


# Stacked
import matplotlib.pyplot as plt
import plotnine as p9
from matplotlib import gridspec
from plotnine import data
from mizani.formatters import scientific_format

p12 = (p9.ggplot(sum_great_dis_plot, aes(fill='variable', y= 'value', x= ['L1', 'L2', 'L3', 'L4', 'A' ]))
    + p9.scale_x_discrete(limits= ('L1', 'L2', 'L3', 'L4', 'A'))
    + p9.geom_bar(position="stack", stat="identity")
    + p9.ylim(0,100)
    + p9.geom_text(mapping=aes(label='value'), format_string='{:.1f}', va="bottom")
    + p9.theme_linedraw())

df1 = df1.iloc[0:0]
res = res.iloc[0:0]

founders_n = 10
hours = 200
food_on_plate = 100000000

def worm_at_25():
# Create a schedule for worm development at 25C
    df1 = pd.DataFrame({'Stages_name': [], 'Stages_detail': [], 'Numbers': [], 'Progeny/hour': []})
    temp = []
    for i in range(0,10):
        temp.append({"Stages_name": "Egg", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
    
    for i in range(10,19):
        temp.append({"Stages_name": "L1", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(19,27):
        temp.append({"Stages_name": "L2", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(27,32):
        temp.append({"Stages_name": "L3", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(32,40):
        temp.append({"Stages_name": "L4", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(40,47):
        temp.append({"Stages_name": "A_nf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(47,89):
        temp.append({"Stages_name": "A_f", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(89,240):
        temp.append({"Stages_name": "A_pf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    df1 = pd.DataFrame(temp)
    # Filling egg laying schedule
    # total number of eggs at 25C = 170
    for i in range(47,49):
        df1.iloc[i,3] = 1
    for i in range(49,51):
        df1.iloc[i,3] = 2
    for i in range(51,53):
        df1.iloc[i,3] = 3
    for i in range(53,55):
        df1.iloc[i,3] = 4
    for i in range(55,57):
        df1.iloc[i,3] = 5
    for i in range(57,59):
        df1.iloc[i,3] = 6
    for i in range(59,61):
        df1.iloc[i,3] = 7
    for i in range(61,63):
        df1.iloc[i,3] = 8
    for i in range(63,66):
        df1.iloc[i,3] = 7
    for i in range(66,70):
        df1.iloc[i,3] = 6
    for i in range(70,73):
        df1.iloc[i,3] = 5
    for i in range(73,76):
        df1.iloc[i,3] = 4
    for i in range(76,80):
        df1.iloc[i,3] = 3
    for i in range(80,85):
        df1.iloc[i,3] = 2
    for i in range(85,89):
        df1.iloc[i,3] = 1
    
    return df1

df1 = worm_at_25()

res = pd.DataFrame({'t': [], 'Eggs': [], 'L1': [], 'L2': [], 'L3': [], 
                    'L4': [], 'A': [], 'YA': [], 'PA': []})

##### initialize

# put the number of L4 founders
df1.iloc[39,2] = founders_n

##### Run first simulation 
df_list = {}
for t in range(1, hours):
    for step in range(239, 0, -1):
       df1.iloc[step, 2] = df1.iloc[step-1, 2]
       df1.iloc[step-1, 2] = 0
    df1.iloc[0, 2] = (df1.iloc[47:89, 2]*df1.iloc[47:89, 3]).sum() 
    
    df_list['t_'+str(t)] = df1
    r = []
    r.append( t )    # t
    r.append( df1.loc[df1['Stages_name']=='Eggs', 'Numbers'].sum())   # Eggs 
    r.append( df1.loc[df1['Stages_name']=='L1', 'Numbers'].sum() )   # L1
    r.append( df1.loc[df1['Stages_name']=='L2', 'Numbers'].sum() )   # L2
    r.append( df1.loc[df1['Stages_name']=='L3', 'Numbers'].sum() )   # L3
    r.append( df1.loc[df1['Stages_name']=='L4', 'Numbers'].sum() )   # L4
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f')|(df1['Stages_name']=='A_pf'), 'Numbers'].sum() )  # A
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f'), 'Numbers'].sum() )   # YA
    r.append( df1.loc[(df1['Stages_name']=='A_pf'), 'Numbers'].sum() ) #PA
    res = res.append(pd.Series(r, index=['t', 'Eggs', 'L1', 'L2', 'L3', 'L4', 'A', 'YA', 'PA']), ignore_index=True)


#sum column
sum_all = pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
sum_all['Total_number'] = sum_all[sum_list].sum(axis=1)


#find food consumption 
food= pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
#set food intake ratio 1, 2, 4, 8, 16
food_cons_stage = [1, 0, 1, 2, 4, 8, 16, 1, 1]
food_cons = food.mul(food_cons_stage, axis= 1)
food_cons['food_consum'] = food_cons[sum_list].sum(axis=1)
food_cons['food_consum_acu'] = food_cons['food_consum'].cumsum()
food_cons_total = food_cons.loc[food_cons['food_consum_acu'] > food_on_plate]
food_cons_total_1 = food_cons_total['t'].head(1)
food_hour = int(food_cons_total_1)
food_hour_list.append(int(food_hour))

food_dist = sum_all[food_hour-1:food_hour]

y_starved = int(food_dist['Total_number'])

sum_great_dis = food_dist


distribution = pd.DataFrame.copy(res)
for t in range(hours-2, 0, -1):
    distribution.iloc[t] -= distribution.iloc[t-1]
    distribution['t'] = res['t']

sum_dist = pd.DataFrame.copy(distribution)
sum_dist['Total_number'] = sum_dist[sum_list].sum(axis=1)
sum_dist = sum_dist.drop(sum_list, axis=1)




from plotnine import ggplot
from plotnine import geom_bar, aes


######################################################################################
# without eggs / with larve + adults
res_plot_a = res[[ 't', 'L1', 'L2', 'L3', 'L4', 'A']]
res_plot_a_sum = copy.deepcopy(res_plot_a)
res_plot_a_sum['sum'] = res_plot_a_sum[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
res_plot_a_sum = res_plot_a_sum.loc[:,"L1":"A"].div(res_plot_a_sum["sum"], axis=0)
res_plot_a_sum['t'] = res_plot_a['t']


sum_great_dis_sum = copy.deepcopy(sum_great_dis)
sum_great_dis_sum['sum'] = sum_great_dis[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
sum_great_dis_sum = sum_great_dis_sum.loc[:, "L1":"A"].div(sum_great_dis_sum["sum"],axis=0) * 100
sum_great_dis_sum['t'] = sum_great_dis['t']

res_plot_a_sum2 = pd.melt(res_plot_a, id_vars="t")
res_plot_a_sum_plot = pd.melt(res_plot_a_sum, id_vars="t")
sum_great_dis_plot = pd.melt(sum_great_dis_sum, id_vars="t")
print(sum_great_dis_plot)


# Stacked
import matplotlib.pyplot as plt
import plotnine as p9
from matplotlib import gridspec
from plotnine import data
from mizani.formatters import scientific_format

p13 = (p9.ggplot(sum_great_dis_plot, aes(fill='variable', y= 'value', x= ['L1', 'L2', 'L3', 'L4', 'A' ]))
    + p9.scale_x_discrete(limits= ('L1', 'L2', 'L3', 'L4', 'A'))
    + p9.geom_bar(position="stack", stat="identity")
    + p9.ylim(0,100)
    + p9.geom_text(mapping=aes(label='value'), format_string='{:.1f}', va="bottom")
    + p9.theme_linedraw())

df1 = df1.iloc[0:0]
res = res.iloc[0:0]

founders_n = 50
hours = 200
food_on_plate = 100000000

def worm_at_25():
# Create a schedule for worm development at 25C
    df1 = pd.DataFrame({'Stages_name': [], 'Stages_detail': [], 'Numbers': [], 'Progeny/hour': []})
    temp = []
    for i in range(0,10):
        temp.append({"Stages_name": "Egg", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
    
    for i in range(10,19):
        temp.append({"Stages_name": "L1", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(19,27):
        temp.append({"Stages_name": "L2", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(27,32):
        temp.append({"Stages_name": "L3", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(32,40):
        temp.append({"Stages_name": "L4", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(40,47):
        temp.append({"Stages_name": "A_nf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(47,89):
        temp.append({"Stages_name": "A_f", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(89,240):
        temp.append({"Stages_name": "A_pf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    df1 = pd.DataFrame(temp)
    # Filling egg laying schedule
    # total number of eggs at 25C = 170
    for i in range(47,49):
        df1.iloc[i,3] = 1
    for i in range(49,51):
        df1.iloc[i,3] = 2
    for i in range(51,53):
        df1.iloc[i,3] = 3
    for i in range(53,55):
        df1.iloc[i,3] = 4
    for i in range(55,57):
        df1.iloc[i,3] = 5
    for i in range(57,59):
        df1.iloc[i,3] = 6
    for i in range(59,61):
        df1.iloc[i,3] = 7
    for i in range(61,63):
        df1.iloc[i,3] = 8
    for i in range(63,66):
        df1.iloc[i,3] = 7
    for i in range(66,70):
        df1.iloc[i,3] = 6
    for i in range(70,73):
        df1.iloc[i,3] = 5
    for i in range(73,76):
        df1.iloc[i,3] = 4
    for i in range(76,80):
        df1.iloc[i,3] = 3
    for i in range(80,85):
        df1.iloc[i,3] = 2
    for i in range(85,89):
        df1.iloc[i,3] = 1
    
    return df1

df1 = worm_at_25()

res = pd.DataFrame({'t': [], 'Eggs': [], 'L1': [], 'L2': [], 'L3': [], 
                    'L4': [], 'A': [], 'YA': [], 'PA': []})

##### initialize

# put the number of L4 founders
df1.iloc[39,2] = founders_n

##### Run first simulation 
df_list = {}
for t in range(1, hours):
    for step in range(239, 0, -1):
       df1.iloc[step, 2] = df1.iloc[step-1, 2]
       df1.iloc[step-1, 2] = 0
    df1.iloc[0, 2] = (df1.iloc[47:89, 2]*df1.iloc[47:89, 3]).sum() 
    
    df_list['t_'+str(t)] = df1
    r = []
    r.append( t )    # t
    r.append( df1.loc[df1['Stages_name']=='Eggs', 'Numbers'].sum())   # Eggs 
    r.append( df1.loc[df1['Stages_name']=='L1', 'Numbers'].sum() )   # L1
    r.append( df1.loc[df1['Stages_name']=='L2', 'Numbers'].sum() )   # L2
    r.append( df1.loc[df1['Stages_name']=='L3', 'Numbers'].sum() )   # L3
    r.append( df1.loc[df1['Stages_name']=='L4', 'Numbers'].sum() )   # L4
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f')|(df1['Stages_name']=='A_pf'), 'Numbers'].sum() )  # A
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f'), 'Numbers'].sum() )   # YA
    r.append( df1.loc[(df1['Stages_name']=='A_pf'), 'Numbers'].sum() ) #PA
    res = res.append(pd.Series(r, index=['t', 'Eggs', 'L1', 'L2', 'L3', 'L4', 'A', 'YA', 'PA']), ignore_index=True)


#sum column
sum_all = pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
sum_all['Total_number'] = sum_all[sum_list].sum(axis=1)


#find food consumption 
food= pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
#set food intake ratio 1, 2, 4, 8, 16
food_cons_stage = [1, 0, 1, 2, 4, 8, 16, 1, 1]
food_cons = food.mul(food_cons_stage, axis= 1)
food_cons['food_consum'] = food_cons[sum_list].sum(axis=1)
food_cons['food_consum_acu'] = food_cons['food_consum'].cumsum()
food_cons_total = food_cons.loc[food_cons['food_consum_acu'] > food_on_plate]
food_cons_total_1 = food_cons_total['t'].head(1)
food_hour = int(food_cons_total_1)
food_hour_list.append(int(food_hour))

food_dist = sum_all[food_hour-1:food_hour]

y_starved = int(food_dist['Total_number'])

sum_great_dis = food_dist


distribution = pd.DataFrame.copy(res)
for t in range(hours-2, 0, -1):
    distribution.iloc[t] -= distribution.iloc[t-1]
    distribution['t'] = res['t']

sum_dist = pd.DataFrame.copy(distribution)
sum_dist['Total_number'] = sum_dist[sum_list].sum(axis=1)
sum_dist = sum_dist.drop(sum_list, axis=1)




from plotnine import ggplot
from plotnine import geom_bar, aes


######################################################################################
# without eggs / with larve + adults
res_plot_a = res[[ 't', 'L1', 'L2', 'L3', 'L4', 'A']]
res_plot_a_sum = copy.deepcopy(res_plot_a)
res_plot_a_sum['sum'] = res_plot_a_sum[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
res_plot_a_sum = res_plot_a_sum.loc[:,"L1":"A"].div(res_plot_a_sum["sum"], axis=0)
res_plot_a_sum['t'] = res_plot_a['t']


sum_great_dis_sum = copy.deepcopy(sum_great_dis)
sum_great_dis_sum['sum'] = sum_great_dis[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
sum_great_dis_sum = sum_great_dis_sum.loc[:, "L1":"A"].div(sum_great_dis_sum["sum"],axis=0) * 100
sum_great_dis_sum['t'] = sum_great_dis['t']

res_plot_a_sum2 = pd.melt(res_plot_a, id_vars="t")
res_plot_a_sum_plot = pd.melt(res_plot_a_sum, id_vars="t")
sum_great_dis_plot = pd.melt(sum_great_dis_sum, id_vars="t")
print(sum_great_dis_plot)


# Stacked
import matplotlib.pyplot as plt
import plotnine as p9
from matplotlib import gridspec
from plotnine import data
from mizani.formatters import scientific_format

p14 = (p9.ggplot(sum_great_dis_plot, aes(fill='variable', y= 'value', x= ['L1', 'L2', 'L3', 'L4', 'A' ]))
    + p9.scale_x_discrete(limits= ('L1', 'L2', 'L3', 'L4', 'A'))
    + p9.geom_bar(position="stack", stat="identity")
    + p9.ylim(0,100)
    + p9.geom_text(mapping=aes(label='value'), format_string='{:.1f}', va="bottom")
    + p9.theme_linedraw())

df1 = df1.iloc[0:0]
res = res.iloc[0:0]

founders_n = 200
hours = 200
food_on_plate = 100000000

def worm_at_25():
# Create a schedule for worm development at 25C
    df1 = pd.DataFrame({'Stages_name': [], 'Stages_detail': [], 'Numbers': [], 'Progeny/hour': []})
    temp = []
    for i in range(0,10):
        temp.append({"Stages_name": "Egg", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
    
    for i in range(10,19):
        temp.append({"Stages_name": "L1", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(19,27):
        temp.append({"Stages_name": "L2", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(27,32):
        temp.append({"Stages_name": "L3", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(32,40):
        temp.append({"Stages_name": "L4", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(40,47):
        temp.append({"Stages_name": "A_nf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(47,89):
        temp.append({"Stages_name": "A_f", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    for i in range(89,240):
        temp.append({"Stages_name": "A_pf", "Stages_detail": i, "Numbers": 0, "Progeny/hour": 0})
        
    df1 = pd.DataFrame(temp)
    # Filling egg laying schedule
    # total number of eggs at 25C = 170
    for i in range(47,49):
        df1.iloc[i,3] = 1
    for i in range(49,51):
        df1.iloc[i,3] = 2
    for i in range(51,53):
        df1.iloc[i,3] = 3
    for i in range(53,55):
        df1.iloc[i,3] = 4
    for i in range(55,57):
        df1.iloc[i,3] = 5
    for i in range(57,59):
        df1.iloc[i,3] = 6
    for i in range(59,61):
        df1.iloc[i,3] = 7
    for i in range(61,63):
        df1.iloc[i,3] = 8
    for i in range(63,66):
        df1.iloc[i,3] = 7
    for i in range(66,70):
        df1.iloc[i,3] = 6
    for i in range(70,73):
        df1.iloc[i,3] = 5
    for i in range(73,76):
        df1.iloc[i,3] = 4
    for i in range(76,80):
        df1.iloc[i,3] = 3
    for i in range(80,85):
        df1.iloc[i,3] = 2
    for i in range(85,89):
        df1.iloc[i,3] = 1
    
    return df1

df1 = worm_at_25()

res = pd.DataFrame({'t': [], 'Eggs': [], 'L1': [], 'L2': [], 'L3': [], 
                    'L4': [], 'A': [], 'YA': [], 'PA': []})

##### initialize

# put the number of L4 founders
df1.iloc[39,2] = founders_n

##### Run first simulation 
df_list = {}
for t in range(1, hours):
    for step in range(239, 0, -1):
       df1.iloc[step, 2] = df1.iloc[step-1, 2]
       df1.iloc[step-1, 2] = 0
    df1.iloc[0, 2] = (df1.iloc[47:89, 2]*df1.iloc[47:89, 3]).sum() 
    
    df_list['t_'+str(t)] = df1
    r = []
    r.append( t )    # t
    r.append( df1.loc[df1['Stages_name']=='Eggs', 'Numbers'].sum())   # Eggs 
    r.append( df1.loc[df1['Stages_name']=='L1', 'Numbers'].sum() )   # L1
    r.append( df1.loc[df1['Stages_name']=='L2', 'Numbers'].sum() )   # L2
    r.append( df1.loc[df1['Stages_name']=='L3', 'Numbers'].sum() )   # L3
    r.append( df1.loc[df1['Stages_name']=='L4', 'Numbers'].sum() )   # L4
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f')|(df1['Stages_name']=='A_pf'), 'Numbers'].sum() )  # A
    r.append( df1.loc[(df1['Stages_name']=='A_nf')|(df1['Stages_name']=='A_f'), 'Numbers'].sum() )   # YA
    r.append( df1.loc[(df1['Stages_name']=='A_pf'), 'Numbers'].sum() ) #PA
    res = res.append(pd.Series(r, index=['t', 'Eggs', 'L1', 'L2', 'L3', 'L4', 'A', 'YA', 'PA']), ignore_index=True)


#sum column
sum_all = pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
sum_all['Total_number'] = sum_all[sum_list].sum(axis=1)


#find food consumption 
food= pd.DataFrame.copy(res)
sum_list = ['L1', 'L2', 'L3', 'L4', 'A']
#set food intake ratio 1, 2, 4, 8, 16
food_cons_stage = [1, 0, 1, 2, 4, 8, 16, 1, 1]
food_cons = food.mul(food_cons_stage, axis= 1)
food_cons['food_consum'] = food_cons[sum_list].sum(axis=1)
food_cons['food_consum_acu'] = food_cons['food_consum'].cumsum()
food_cons_total = food_cons.loc[food_cons['food_consum_acu'] > food_on_plate]
food_cons_total_1 = food_cons_total['t'].head(1)
food_hour = int(food_cons_total_1)

food_hour_list.append(int(food_hour))

food_dist = sum_all[food_hour-1:food_hour]

y_starved = int(food_dist['Total_number'])

sum_great_dis = food_dist


distribution = pd.DataFrame.copy(res)
for t in range(hours-2, 0, -1):
    distribution.iloc[t] -= distribution.iloc[t-1]
    distribution['t'] = res['t']

sum_dist = pd.DataFrame.copy(distribution)
sum_dist['Total_number'] = sum_dist[sum_list].sum(axis=1)
sum_dist = sum_dist.drop(sum_list, axis=1)




from plotnine import ggplot
from plotnine import geom_bar, aes


######################################################################################
# without eggs / with larve + adults
res_plot_a = res[[ 't', 'L1', 'L2', 'L3', 'L4', 'A']]
res_plot_a_sum = copy.deepcopy(res_plot_a)
res_plot_a_sum['sum'] = res_plot_a_sum[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
res_plot_a_sum = res_plot_a_sum.loc[:,"L1":"A"].div(res_plot_a_sum["sum"], axis=0)
res_plot_a_sum['t'] = res_plot_a['t']


sum_great_dis_sum = copy.deepcopy(sum_great_dis)
sum_great_dis_sum['sum'] = sum_great_dis[['L1', 'L2', 'L3', 'L4', 'A']].sum(axis=1)
sum_great_dis_sum = sum_great_dis_sum.loc[:, "L1":"A"].div(sum_great_dis_sum["sum"],axis=0) * 100
sum_great_dis_sum['t'] = sum_great_dis['t']

res_plot_a_sum2 = pd.melt(res_plot_a, id_vars="t")
res_plot_a_sum_plot = pd.melt(res_plot_a_sum, id_vars="t")
sum_great_dis_plot = pd.melt(sum_great_dis_sum, id_vars="t")
print(sum_great_dis_plot)


# Stacked
import matplotlib.pyplot as plt
import plotnine as p9
from matplotlib import gridspec
from plotnine import data
from mizani.formatters import scientific_format

p15 = (p9.ggplot(sum_great_dis_plot, aes(fill='variable', y= 'value', x= ['L1', 'L2', 'L3', 'L4', 'A' ]))
    + p9.scale_x_discrete(limits= ('L1', 'L2', 'L3', 'L4', 'A'))
    + p9.geom_bar(position="stack", stat="identity")
    + p9.ylim(0,100)
    + p9.geom_text(mapping=aes(label='value'), format_string='{:.1f}', va="bottom")
    + p9.theme_linedraw())

df1 = df1.iloc[0:0]
res = res.iloc[0:0]


founders_n = 1
hours = 200
food_on_plate = 100000000





    
fig = (p9.ggplot()+p9.geom_blank(data=data.diamonds)).draw()

# Create gridspec for adding subpanels to the blank figure
gs = gridspec.GridSpec(3,5, wspace = 0.25, hspace = 0.4)
# ax1 = fig.add_subplot(gs[0,0])
# ax1.set_xlabel('Hours')
# ax1.set_ylabel('Counts')
# ax1.set_title('Population structure: counts')

# ax2 = fig.add_subplot(gs[0,1])
# ax2.set_xlabel('Hours')
# ax2.set_ylabel('Counts')
# ax2.set_title('Population structure: changes')

# ax3 = fig.add_subplot(gs[0,2])
# ax3.set_xlabel('Hours')
# ax3.set_ylabel('Share')
# ax3.set_title('Population structure: share')

# ax4 = fig.add_subplot(gs[1,0])
# ax4.set_xlabel('Hours')
# ax4.set_ylabel('Counts')
# ax4.set_title('After ' + str(food_hour_list[]) + ' hour, \n total number of '  + str(y_starved) + ' worms \ncomsumed all food on the plate.')

# ax5 = fig.add_subplot(gs[1,1])
# ax5.set_xlabel('Hours')
# ax5.set_ylabel('Counts')
# ax5.set_title('Population structure: changes')

ax1 = fig.add_subplot(gs[0,0])
ax1.set_xlabel('Stage')
#ax1.title.set_text('Founder = 1')
ax1.set_ylabel('Food: 10,000,000 unit')
ax1.set_title('Founder = 1 \n' + str(food_hour_list[0]) + ' hour')

ax2 = fig.add_subplot(gs[0,1])
ax2.set_xlabel('Stage')
#ax2.title.set_text('Founder = 3')
#ax2.set_ylabel('Percentage of whole population (%)')
ax2.set_title('Founder = 3 \n' + str(food_hour_list[1]) + ' hour')

ax3 = fig.add_subplot(gs[0,2])
ax3.set_xlabel('Stage')
#ax3.title.set_text('Founder = 10')
#ax3.set_ylabel('Percentage of whole population (%)')
ax3.set_title('Founder = 10 \n' + str(food_hour_list[2]) + ' hour')

ax4 = fig.add_subplot(gs[0,3])
ax4.set_xlabel('Stage')
#ax4.title.set_text('Founder = 50')
#ax4.set_ylabel('Percentage of whole population (%)')
ax4.set_title('Founder = 50 \n' + str(food_hour_list[3]) + ' hour')

ax5 = fig.add_subplot(gs[0,4])
ax5.set_xlabel('Stage')
#ax5.title.set_text('Founder = 200')
#ax5.set_ylabel('Percentage of whole population (%)')
ax5.set_title('Founder = 200 \n' + str(food_hour_list[4]) + ' hour')

ax11 = fig.add_subplot(gs[1,0])
ax11.set_xlabel('Stage')
ax11.set_ylabel('Food: 50,000,000')
ax11.set_title(str(food_hour_list[5]) + ' hour')

ax12 = fig.add_subplot(gs[1,1])
ax12.set_xlabel('Stage')
#ax12.set_ylabel('Percentage of whole population (%)')
ax12.set_title(str(food_hour_list[6]) + ' hour')

ax13 = fig.add_subplot(gs[1,2])
ax13.set_xlabel('Stage')
#ax13.set_ylabel('Percentage of whole population (%)')
ax13.set_title(str(food_hour_list[7]) + ' hour')

ax14 = fig.add_subplot(gs[1,3])
ax14.set_xlabel('Stage')
#ax14.set_ylabel('Percentage of whole population (%)')
ax14.set_title(str(food_hour_list[8]) + ' hour')

ax15 = fig.add_subplot(gs[1,4])
ax15.set_xlabel('Stage')
#ax15.set_ylabel('Percentage of whole population (%)')
ax15.set_title(str(food_hour_list[9]) + ' hour')

ax21 = fig.add_subplot(gs[2,0])
ax21.set_xlabel('Stage')
ax21.set_ylabel('Food: 100,000,000 unit')
ax21.set_title(str(food_hour_list[10]) + ' hour')

ax22 = fig.add_subplot(gs[2,1])
ax22.set_xlabel('Stage')
#ax22.set_ylabel('Percentage of whole population (%)')
ax22.set_title(str(food_hour_list[11]) + ' hour')

ax23 = fig.add_subplot(gs[2,2])
ax23.set_xlabel('Stage')
#ax23.set_ylabel('Percentage of whole population (%)')
ax23.set_title(str(food_hour_list[12]) + ' hour')

ax24 = fig.add_subplot(gs[2,3])
ax24.set_xlabel('Stage')
#ax24.set_ylabel('Percentage of whole population (%)')
ax24.set_title(str(food_hour_list[13]) + ' hour')

ax25 = fig.add_subplot(gs[2,4])
ax25.set_xlabel('Stage')
#ax25.set_ylabel('Percentage of whole population (%)')
ax25.set_title(str(food_hour_list[14]) + ' hour')




# Add subplots to the figure
_ = p1._draw_using_figure(fig, [ax1])
_ = p2._draw_using_figure(fig, [ax2])
_ = p3._draw_using_figure(fig, [ax3])
_ = p4._draw_using_figure(fig, [ax4])
_ = p5._draw_using_figure(fig, [ax5])
_ = p6._draw_using_figure(fig, [ax11])
_ = p7._draw_using_figure(fig, [ax12])
_ = p8._draw_using_figure(fig, [ax13])
_ = p9a._draw_using_figure(fig, [ax14])
_ = p10._draw_using_figure(fig, [ax15])
_ = p11._draw_using_figure(fig, [ax21])
_ = p12._draw_using_figure(fig, [ax22])
_ = p13._draw_using_figure(fig, [ax23])
_ = p14._draw_using_figure(fig, [ax24])
_ = p15._draw_using_figure(fig, [ax25])



fig.suptitle('Population structure (%) when starvation begins' , fontsize=16)


fig.set_size_inches(60,10)
fig.show()


plt.savefig('founder_X_food.jpeg', edgecolor='black', dpi=1000,  bbox_inches='tight')#,facecolor='black', transparent=True)

print("finish")
