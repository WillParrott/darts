import numpy as np
import matplotlib.pyplot as plt
import collections
figsca = 14  #size for saving figs
figsize = ((figsca,figsca))


r_Ibull,r_Obull,r_IT,r_OT,r_ID,r_OD = 6.35,16,99,107,162,170# all in mm
Ordering = [20,1,18,4,13,6,10,15,2,17,3,19,7,16,8,11,14,9,12,5]
resolution = 0.01 # divide into squares of the side lenght, mm, we'll take a box of length 420*420




def main():
    plt.figure(figsize=figsize)
    plot_board(plt)
    plt.show()
    return()


def plot_board(plt): # draws board
    x,y = collections.defaultdict(list),collections.defaultdict(list)
    for x_i in np.arange(-210,210+resolution,resolution):
        for rad in [r_Ibull,r_Obull,r_IT,r_OT,r_ID,r_OD]:
            if x_i**2 <= rad**2:
                x[f'{rad}'].append(x_i)
                y[f'{rad}'].append(np.sqrt(rad**2-x_i**2))
        for theta in np.arange(-9*np.pi/20,11*np.pi/20,np.pi/10):
            r2 = x_i**2 +(x_i*np.tan(theta))**2
            if r2 >= r_Obull**2 and r2 <= (r_OD*1.1)**2:
                x[f'{theta}{np.sign(x_i)}'].append(x_i)
                y[f'{theta}{np.sign(x_i)}'].append(x_i*np.tan(theta))
    for rad in [r_Ibull,r_Obull,r_IT,r_OT,r_ID,r_OD]:
        plt.plot(x[f'{rad}'],y[f'{rad}'],color='k',linestyle='-')
        plt.plot(x[f'{rad}'],-np.array(y[f'{rad}']),color='k',linestyle='-')
    for theta in np.arange(-9*np.pi/20,11*np.pi/20,np.pi/10):
        plt.plot(x[f'{theta}-1.0'],y[f'{theta}-1.0'],color='k',linestyle='-')
        plt.plot(x[f'{theta}1.0'],y[f'{theta}1.0'],color='k',linestyle='-')
    return()


def get_score(x,y):
    r,theta = np.sqrt(x**2 + y**2), np.arctan(y/x)
    if r > r_OD:
        return(0)
    if r < r_Ibull:
        return(50)
    if r < r_Obull:
        return(25)
    
        
    return(score)

main()
