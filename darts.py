std_in = input('What is the standard deviation of your dart throws to be, in mm? Type None for automatic list ')  # my standard deviation in mm
if std_in != 'None':
    std = [float(std_in)]
else:
    std = [100,75,50,40,30,20,10]
if len(std) ==1 and  std[0]<4:
    print(f"Chosen standard deviation of {std[0]} is too small so has been set to 4mm. Just aim for T20.")
    std[0] = 4
#############################
import numpy as np
import matplotlib.pyplot as plt
import collections
figsca = 14  #size for saving figs
figsize = ((figsca,figsca))
plt.rc("font",**{"size":20})
plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
plt.rc('text', usetex=True)
cols = ['r','b','g','purple','c','orange','brown']
#############################

r_Ibull,r_Obull,r_IT,r_OT,r_ID,r_OD = 6.35,16,99,107,162,170# all in mm
Ordering = [20,1,18,4,13,6,10,15,2,17,3,19,7,16,8,11,14,9,12,5]
iterations = 50000 #10000 is good here

def main():
    plt.figure(figsize=figsize)
    plot_board(plt)
    for i_s,my_std in enumerate(std):
        resolution = my_std/10 # divide into squares of the side lenght, mm
        xran = np.arange(-r_OD,r_OD+resolution,resolution)
        if resolution > 2: resolution = 2
        print(f'Calculating the best place to aim for a player with a standard deviation of {my_std}mm: resolution {resolution}mm')
        results,xs,ys = collections.defaultdict(list),[],[]
        for ix,x in enumerate(xran):
            for y in xran:
                if x**2 + y**2 > r_OD**2: continue
                av = generate_av_score(x,y,my_std)
                results['pos'].append(f'{x}_{y}')
                results['score'].append(av)
            progbar(ix+1,len(xran))
        T20av = generate_av_score(0,r_IT+4,my_std)
        best = max(results['score'])
        print(f'For {iterations} darts thrown with a standard deviation of {my_std}mm, the best average score per dart is {best}')
        print(f'For this skill level, aiming at T20 would give you {T20av} {100*(best-T20av)/best:.1f}% worse')
        for i,el in enumerate(results['score']):
            if el == best:
                xs.append(float(results['pos'][i].split('_')[0]))
                ys.append(float(results['pos'][i].split('_')[1]))
        plot_results(xs,ys,plt,my_std,i_s)
    plt.legend(frameon=True,loc='lower left',bbox_to_anchor=(0.7,0.9),ncol=2)
    plt.savefig(f'plots/Std_{my_std}mm_iters_{iterations}.pdf')
    plt.close()
    return()

def generate_av_score(x,y,my_std):
    xy = np.random.normal(loc=(x,y),scale=my_std,size=(iterations,2)) # returns list iterations long, with [x,y] for each
    av = 0
    for i_it in xy:
        score = get_score(i_it[0],i_it[1])
        av += score
    return(av/iterations)

def plot_results(xs,ys,plt,my_std,i_s):
    for i in range(len(xs)):
        plt.errorbar(xs[i],ys[i],fmt='x',color=cols[i_s],label =f'{std[i_s]}mm')
        circ = plt.Circle((xs[i],ys[i]),my_std,color=cols[i_s],fill=False)
        plt.gca().add_patch(circ)
    return()

def plot_board(plt): # draws board
    x,y = collections.defaultdict(list),collections.defaultdict(list)
    for x_i in np.arange(-r_OD,r_OD+0.1,0.1):
        for rad in [r_Ibull,r_Obull,r_IT,r_OT,r_ID,r_OD]:
            if x_i**2 <= rad**2:
                x[f'{rad}'].append(x_i)
                y[f'{rad}'].append(np.sqrt(rad**2-x_i**2))
        for theta in np.arange(-9*np.pi/20,11*np.pi/20,np.pi/10):
            r2 = x_i**2 +(x_i*np.tan(theta))**2
            if r2 >= r_Obull**2 and r2 <= (r_OD*1.1)**2:
                x[f'{theta}{int(np.sign(x_i))}'].append(x_i)
                y[f'{theta}{int(np.sign(x_i))}'].append(x_i*np.tan(theta))
    for rad in [r_Ibull,r_Obull,r_IT,r_OT,r_ID,r_OD]:
        plt.plot(x[f'{rad}']+x[f'{rad}'][::-1]+[x[f'{rad}'][0]],y[f'{rad}']+list(-np.array(y[f'{rad}'][::-1]))+[y[f'{rad}'][0]],color='k',linestyle='-')
    for theta in np.arange(-9*np.pi/20,11*np.pi/20,np.pi/10):
        plt.plot(x[f'{theta}-1'],y[f'{theta}-1']+list(),color='k',linestyle='-')
        plt.plot(x[f'{theta}1'],y[f'{theta}1'],color='k',linestyle='-')
    for i in range(20):
        theta, r = (np.pi/2 - i*np.pi/10)%(2*np.pi), r_OD*1.05
        plt.text(r*np.cos(theta),r*np.sin(theta),f'{Ordering[i]}',fontsize=20,ha='center',va='center')        
    return()


def get_score(x,y):
    r,theta = get_r_theta(x,y)
    if r > r_OD:
        return(0)
    if r < r_Ibull:
        return(50)
    if r < r_Obull:
        return(25)
    score = get_number(theta)
    if r_IT <= r < r_OT:
        return(score*3)
    if r_ID <= r < r_OD:
        return(score*2)
    return(score)

def get_number(theta):
    if theta <= -19*np.pi/20 or theta >=19*np.pi/20:
        return(Ordering[15]) # deals with case where whe have branch cut
    for i in range(20):
        top,bot = np.pi - i*np.pi/10 + np.pi/20, np.pi - i*np.pi/10 - np.pi/20
        if min([bot,top]) <= theta < max([bot,top]):
            return(Ordering[(i-5)%20])


def get_r_theta(x,y): #we want theta in range(pi to -pi)
    if x == 0:
        if y<0:
            return(abs(y),-np.pi/2)
        else:
            return(abs(y),np.pi/2)
    r,theta = np.sqrt(x**2 + y**2),np.arctan(y/x)
    if x < 0:
        if y <0:
            theta -= np.pi
        else:
            theta += np.pi
    return(r,theta)

def progbar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total:
        print()
    return()

main()
