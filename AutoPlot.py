'''
This program aims to replace Origin to plot the figure
'''
#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def plotter(file_name, export_path):
    # Import the exp data
    data = np.genfromtxt(file_name, delimiter=',')
    Temp = data[:, 2]  # the 3-rd, Temp [K]
    MagneticField = data[:, 3]  # the 4-th
    Moment = data[:, 4]  # the 5-th, moment [emu]

    ## Data filtering
    mask = ~np.isnan(MagneticField) & ~np.isinf(MagneticField)
    MagneticField = MagneticField[mask]
    mask = ~np.isnan(Moment) & ~np.isinf(Moment)
    Moment = Moment[mask]

    # Define the group size
    group_size = 430

    num_groups_mf = len(MagneticField) // group_size + (1 if len(MagneticField) % group_size > 0 else 0)
    num_groups_mm = len(Moment) // group_size + (1 if len(Moment) % group_size > 0 else 0)

    # use array_split to split the data
    mf_groups = np.array_split(MagneticField, num_groups_mf)
    mm_groups = np.array_split(Moment, num_groups_mm)

    # 转换temp列，将温度四舍五入到最近的5K
    Temp = (Temp / 5).round() * 5
    num_Temp = num_groups_mf
    Temp_groups = np.array_split(Temp, num_Temp)
    Templen = len(Temp)
    # for i in range(Templen):
    # Temp_groups_i = Temp_groups[i]

    """
    Initial Plot(OG scatter)
    """
    # plt.figure(1)
    # plt.scatter(mf_groups[1], mm_groups[1], label='first', s=2)
    # plt.legend()
    # plt.xlabel('Magnetic Field')
    # plt.ylabel('Moment')
    """
    Optional 
    """
    # ## Curve fit for the whole data
    # plt.figure(2)
    # coefficients = np.polyfit(mf_groups[1], mm_groups[1], 1)
    # slope, intercept = coefficients
    # print("slope = ", slope, "intercept = ", intercept)

    # fit_line = slope * mm_groups[1] + intercept

    # plt.plot(mf_groups[1], fit_line, color='red', label='linear fit')
    # plt.legend()

    ## Final operation
    plt.figure(3)
    mf_groups_1 = mf_groups[1]
    mm_groups_1 = mm_groups[1]

    min_indices = np.argsort(mf_groups_1)[:3]
    min_values = mf_groups_1[min_indices]

    coefficients = np.polyfit(mf_groups_1[min_indices], mm_groups_1[min_indices], 1)
    slope, intercept = coefficients
    corrected_moment = mm_groups_1 - (slope * mf_groups_1)
    plt.scatter(mf_groups_1, mm_groups_1, label='OG', s=2)
    plt.plot(mf_groups_1, corrected_moment, color='blue', label='linear fit')
    plt.xlabel('Magnetic Field')
    plt.ylabel('Moment')
    plt.legend()
    # plt.show()

    #%%

    for i in range(len(mf_groups)):
        tmp_idx = Temp[(i + 1) * 430]
        plt.figure(i + 1)  # 为每个数据组创建一个新的figure
        mf_groups_i = mf_groups[i]
        mm_groups_i = mm_groups[i]
        min_indices = np.argsort(mf_groups_i)[:3]

        coefficients = np.polyfit(mf_groups_i[min_indices], mm_groups_i[min_indices], 1)
        slope, intercept = coefficients
        corrected_moment = mm_groups_i - (slope * mf_groups_i)
        plt.scatter(mf_groups_i, mm_groups_i, label=f'Group {i + 1} Original', s=2)
        plt.plot(mf_groups_i, corrected_moment, color='blue', label='Linear Fit')
        plt.xlabel('Magnetic Field')
        plt.ylabel('Corrected Moment')
        plt.title(f'{tmp_idx}K')
        plt.legend()
        picture_name = export_path + "/" + str(tmp_idx) + "K.png"
        plt.savefig(picture_name)

        # plt.show()

    #%%
