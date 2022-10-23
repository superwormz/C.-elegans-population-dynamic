
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import math
import copy

# constant, don't change
STAGES = ['Eggs'] * 10 + ['L1'] * 9 + ['L2'] * 8 + ['L3'] * 5 + ['L4'] * 8 + ['Adult'] * 200
FOOD_CONSUMPTION_BY_AGE  = [0] * 10 + [1] * 9 + [2] * 8 + [4] * 5 + [8] * 8 + [16] * 200  

def get_transform_matrix(max_age):
    # we use the 
    # - first $max_age for population per age and then
    # - food
    # - maybe something else in the future?
    n_rows_cols = (
        max_age + 
        1 # food
    ) 
    food_idx = max_age
    m = pd.DataFrame([[0]*n_rows_cols]*n_rows_cols, index=STAGES + ["Food"], columns=STAGES + ["Food"]) # $n_rows_cols x $n_rows_cols matrix
    # aging
    for i in range(max_age):
        m.iloc[i+1, i] = 1
    # laying eggs
    m.iloc[0, 47:49] = 1
    m.iloc[0, 49:51] = 2
    m.iloc[0, 51:53] = 3
    m.iloc[0, 53:55] = 4
    m.iloc[0, 55:57] = 5
    m.iloc[0, 57:59] = 6
    m.iloc[0, 59:61] = 7
    m.iloc[0, 61:63] = 8
    m.iloc[0, 63:66] = 7
    m.iloc[0, 66:70] = 6
    m.iloc[0, 70:73] = 5
    m.iloc[0, 73:76] = 4
    m.iloc[0, 76:80] = 3
    m.iloc[0, 80:85] = 2
    m.iloc[0, 85:89] = 1
    # consuming food
    for age, food_consumption in enumerate(FOOD_CONSUMPTION_BY_AGE):
        m.iloc[food_idx, age] = -food_consumption
    # food stays
    m.iloc[food_idx, food_idx] = 1
    return m

def get_initial_vector(initial_population, max_age, initial_food):
    # we use the 
    # - first $max_age for population per age and then
    # - food
    # - maybe something else in the future?
    n_rows_cols = (
        max_age + 
        1 # food
    ) 
    food_idx = max_age
    v = pd.Series([0] * n_rows_cols, index=STAGES + ["Food"])
    for age, population in initial_population.items():
        assert age < max_age
        assert population >= 0
        v[age] = population
    v.iloc[food_idx] = initial_food
    return v

def v_to_pct(v):
    sum_by_stage = v.groupby(level=0, sort=False).sum().drop(['Eggs', 'Food'])
    pct_by_stage = sum_by_stage.divide(sum_by_stage.sum()) * 100
    return pct_by_stage

def plot_v_over_time(v_over_time, filename):
    # fig_v_over_time = plt.subplot()
    # fig_v_over_time.set_size_inches(20,8)
    # fig_v_over_time.bar(v_over_time, v_over_time.loc['L1'], color= '#b9db57')

    fig_v_over_time, ax_v_over_time = plt.subplots()
    fig_v_over_time.set_size_inches(20,8)
    prev = None
    # colors = {'L1':'#b9db57','L2':'#56db94','L3':'#5684da','L4':'#ca58c8','A':'#da4953'}
    # c = prev['Name'].apply(lambda x: colors[x])
    for stage in (v_over_time.columns):
        ax_v_over_time.bar((v_over_time.index), v_over_time.loc[:, stage], label=stage, bottom=prev)
        if prev is None:
            prev = v_over_time.loc[:, stage]
        else:
            prev += v_over_time.loc[:, stage]
    fig_v_over_time.legend()
    fig_v_over_time.savefig(filename, edgecolor='black', dpi=400,  bbox_inches='tight')


def simulate(initial_v, transform_m, max_hours):
    v = initial_v
    food_exhaution_v = None
    v_over_time = [v_to_pct(v)]
    hours_done = -1
    for i in range(max_hours):
        v = transform_m.dot(v)
        food_left = v.iloc[-1]
        if food_left < 0 and food_exhaution_v is None:
            # only record the first food exhaustion
            food_exhaution_v = v
            hours_done = i
        v_over_time.append(v_to_pct(v))
    # exhaution
    pct_by_stage = v_to_pct(food_exhaution_v)
    # end of exhaustion
    v_over_time = pd.DataFrame(v_over_time)
    return (pct_by_stage, hours_done, v_over_time)

def main():
    ## make sure STAGES & FOOD_CONSUMPTION_BY_AGE are of correct length
    assert len(STAGES) == len(FOOD_CONSUMPTION_BY_AGE), f"STAGES length {len(STAGES)}, FOOD_CONSUMPTION_BY_AGE length {len(FOOD_CONSUMPTION_BY_AGE)}, should be the same"
    for age, food in enumerate(FOOD_CONSUMPTION_BY_AGE):
        assert food >= 0, f"food cconsumption should be non-negative, age {age} consumes {food}"
    populations = [1, 3, 10, 50, 200]
    foods = [10**7, 5*10**7, 10**8]

    fig = plt.figure(tight_layout=True)
    fig.suptitle('Population structure when starvation begins', fontsize=24, fontweight='bold')
    fig.set_size_inches(20,12)
    gs = gridspec.GridSpec(len(foods), len(populations), wspace = 0.25, hspace = 0.35)

    max_age = len(STAGES)
    max_simulation_hours = 200
    
    for i, population in enumerate([1, 3, 10, 50, 200]):
        for j, initial_food in enumerate([10**7, 5*10**7, 10**8]):
            init_population = {39: population}
            v = get_initial_vector(init_population, max_age, initial_food)
            transform = get_transform_matrix(max_age)
            v, finish_hours, v_over_time = simulate(v, transform, max_simulation_hours)

            # subplot
            ax = fig.add_subplot(gs[j, i])
            p1 = ax.bar(range(len(v)), v, tick_label=v.index, color = ['#b9db57','#56db94','#5684da','#ca58c8','#da4953'])
            ax.bar_label(p1, fmt='%.1f')
            ax.grid(axis='y', linestyle = '--')
            ax.set_xlabel('Stage')
            ax.set(ylim=(0,100))
            for axis in ['top','bottom','left','right']:
                ax.spines[axis].set_linewidth(1.5)

            if i == 0:
                ax.set_ylabel(f"Percentage (%)", fontsize=14)
                #ax.set_ylabel(f"Food: " + format(int(initial_food), ',') + " units\n Percentage (%)", fontsize=14)
            if j == 0:
                ax.set_title(f"founder = {population}\n{finish_hours} hours")
            else:
                ax.set_title(f"{finish_hours} hours")
            # end of subplot

            # plotting v over time 
    plot_v_over_time(v_over_time, f"v_over_{max_simulation_hours}.jpg")
            
    fig.savefig('founders_food_matrix', format = 'tif', edgecolor='black', dpi=400,  bbox_inches='tight')
    
if __name__ == "__main__":
    main()
