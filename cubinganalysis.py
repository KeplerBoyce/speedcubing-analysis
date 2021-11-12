import csv
import matplotlib.pyplot as plt
import numpy as np
import statistics as stats
from scipy.optimize import curve_fit
import os.path

solves = list()#video analysis data
responses = list()#survey responses
algnums = {#dict for how many algs are in each algset
    '2GLL - AS' : 12,
    '2GLL - H' : 8,
    '2GLL - L' : 12,
    '2GLL - Pi' : 12,
    '2GLL - S' : 12,
    '2GLL - T' : 12,
    '2GLL - U' : 12,
    'CLL' : 40,
    'CLS' : 104,
    'CMLL' : 40,
    'COLL - AS (Antisune)' : 6,
    'COLL - H (Doublesune)' : 4,
    'COLL - L (Bowtie)' : 6,
    'COLL - Pi (Bruno)' : 6,
    'COLL - S (Sune)' : 6,
    'COLL - T (Chameleon)' : 6,
    'COLL - U (Headlights)' : 6,
    'CPEOLL' : 15,
    'CPLS' : 32,
    'Corner preserving Edge OLL' : 3,
    'ELL' : 29,
    'ELS' : 21,
    'EOLL (non-corner-preserving - the edge part of 2-look OLL)' : 3,
    'EOLR' : 62,
    'EPLL (PLL for edges' : 4,
    'HLS' : 432,
    'Line (1LLL set)' : 48,
    'Magic Wondeful' : 18,
    'OCLL (the corners part of 2-look OLL)' : 7,
    'OLL' : 57,
    'oll' : 57,
    'OLLCP' : 171,
    'PLL' : 21,
    'SV' : 27,
    'TLSE' : 95,
    'TTLL' : 72,
    'Tripod' : 104,
    'tripod' : 104,
    'VHLS' : 32,
    'VLS' : 216,
    'WV' : 27,
    'ZBLL - AS' : 72,
    'ZBLL - H' : 40,
    'ZBLL - L' : 72,
    'ZBLL - Pi' : 72,
    'ZBLL - S' : 72,
    'ZBLL - T' : 72,
    'ZBLL - U' : 72,
    'ZBLS' : 302,
    'ZZLL' : 160,
    'anti-PLL' : 21,
    'pure oll' : 57
}

current_dir = os.getcwd()
final_dir = os.path.join(current_dir, r'graphs')
if not os.path.exists(final_dir):
   os.makedirs(final_dir)

#video analysis data
with open('Video Analysis.tsv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    
    for num, row in enumerate(spamreader):
        if num == 0:
            continue
            
        solve = []
        
        for i in range(2, 26):
            if row[i] == '':
                solve.append(-1)
            else:
                solve.append(float(row[i]))
            
        print(num, solve)
        
        solves.append(solve)
        
    print('Printed solve data from video analysis.')
    
    solves_by_var = list()
    for q in range(24):
        this_var = list()
        for i, arr in enumerate(solves):
            this_var.append(arr[q])
        solves_by_var.append(this_var)
    
    #lists for graph data
    solvetimes = list(solves_by_var[0])
    solvetimes2 = list(solves_by_var[0])
    
    crossfrac = list(solves_by_var[1])
    f2lfrac = list(solves_by_var[2])
    lastlayerfrac = list(solves_by_var[3])
    
    pausefrac = list(solves_by_var[4])
    
    tps = list(solves_by_var[5])
    tps2 = list(solves_by_var[5])
    etps = list(solves_by_var[6])
    
    regrips = list(solves_by_var[7])
    rotations = list(solves_by_var[8])
    tilts = list(solves_by_var[9])
    aufs = list(solves_by_var[10])
    
    crossmoves = list(solves_by_var[11])
    f2lmoves = list(solves_by_var[12])
    lastlayermoves = list(solves_by_var[13])
    totalmoves = [a + b + c for a, b, c in zip(crossmoves, f2lmoves, lastlayermoves)]
    
    crosspauses = list(solves_by_var[14])
    ctofpauses = list(solves_by_var[15])
    f2lpauses = list(solves_by_var[16])
    lastlayerpauses = list(solves_by_var[17])
    
    crosstps = list(solves_by_var[18])
    f2ltps = list(solves_by_var[19])
    lastlayertps = list(solves_by_var[20])
    
    crosspausefrac = list(solves_by_var[21])
    f2lpausefrac = list(solves_by_var[22])
    lastlayerpausefrac = list(solves_by_var[23])
    
    #removing blank elements marked by -1s
    while -1 in pausefrac:
        ind = pausefrac.index(-1)
        del pausefrac[ind]
        del solvetimes2[ind]
        del tps2[ind]
        del etps[ind]
        del crosspauses[ind]
        del ctofpauses[ind]
        del f2lpauses[ind]
        del lastlayerpauses[ind]
        del crosspausefrac[ind]
        del f2lpausefrac[ind]
        del lastlayerpausefrac[ind]
    
    #x range for lines of best fit
    x = np.linspace(0, 40, 100)
    
    #graph for fraction of solve time spent in each step
    plt.figure(0)
    plt.xlim(5, 35)
    plt.ylim(0, 0.7)
    
    plt.title("Fraction of solve spent in each step vs. solve time")
    plt.xlabel('Solve time (s)')
    plt.ylabel('Fraction of solve time')
    
    plt.scatter(solvetimes, crossfrac, s=5)
    plt.scatter(solvetimes, f2lfrac, s=5)
    plt.scatter(solvetimes, lastlayerfrac, s=5)
    
    f1 = np.poly1d(np.polyfit(solvetimes, crossfrac, 1))
    f2 = np.poly1d(np.polyfit(solvetimes, f2lfrac, 1))
    f3 = np.poly1d(np.polyfit(solvetimes, lastlayerfrac, 1))
    
    plt.plot(x, f1(x), label='Cross')
    plt.plot(x, f2(x), label='F2L')
    plt.plot(x, f3(x), label='Last layer')
    
    plt.legend()
    plt.minorticks_on()
    plt.grid(which='major', alpha=0.6)
    plt.grid(which='minor', alpha=0.3)
    plt.savefig('graphs\Fraction of solve spent in each step vs solve time.png', dpi=400)
    
    #graph for fraction of solve time spent pausing
    plt.figure(1)
    plt.xlim(5, 35)
    plt.ylim(0.2, 0.7)
    
    plt.title("Fraction of solve spent pausing vs. solve time")
    plt.xlabel('Solve time (s)')
    plt.ylabel('Fraction of solve time')
        
    plt.scatter(solvetimes2, pausefrac, s=5)
    
    f4 = np.poly1d(np.polyfit(solvetimes2, pausefrac, 1))
        
    plt.plot(x, f4(x))
    
    plt.minorticks_on()
    plt.grid(which='major', alpha=0.6)
    plt.grid(which='minor', alpha=0.3)
    plt.savefig('graphs\Fraction of solve spent pausing vs solve time.png', dpi=400)
    
    #graph for overall tps and etps
    plt.figure(2)
    plt.xlim(5, 35)
    plt.ylim(0, 12)
    
    plt.title("Overall TPS vs. solve time")
    plt.xlabel('Solve time (s)')
    plt.ylabel('Turns per second')
        
    plt.scatter(solvetimes, tps, s=5)
    plt.scatter(solvetimes2, etps, s=5)
    
    f5 = np.poly1d(np.polyfit(solvetimes, tps, 1))
    f6 = np.poly1d(np.polyfit(solvetimes2, etps, 1))
        
    plt.plot(x, f5(x), label='TPS')   
    plt.plot(x, f6(x), label='TPS (pauses ignored)')
    
    plt.legend()
    plt.minorticks_on()
    plt.grid(which='major', alpha=0.6)
    plt.grid(which='minor', alpha=0.3)
    plt.savefig('graphs\Overall TPS vs solve time.png', dpi=400)
    
    #graph for number of regrips, rotations, tilts, and AUFs
    plt.figure(3)
    plt.xlim(5, 35)
    plt.ylim(-1, 40)
    
    plt.title("Regrips, rotations, tilts, and AUFs vs. solve time")
    plt.xlabel('Solve time (s)')
    plt.ylabel('Count')
    
    plt.scatter(solvetimes, regrips, s=5)
    plt.scatter(solvetimes, rotations, s=5)
    plt.scatter(solvetimes, tilts, s=5)
    plt.scatter(solvetimes, aufs, s=5)
    
    f7 = np.poly1d(np.polyfit(solvetimes, regrips, 1))
    f8 = np.poly1d(np.polyfit(solvetimes, rotations, 1))
    f9 = np.poly1d(np.polyfit(solvetimes, tilts, 1))
    f10 = np.poly1d(np.polyfit(solvetimes, aufs, 1))
    
    plt.plot(x, f7(x), label='Regrips')
    plt.plot(x, f8(x), label='Rotations')
    plt.plot(x, f9(x), label='Tilts')
    plt.plot(x, f10(x), label='AUFs')
    
    plt.legend()
    plt.minorticks_on()
    plt.grid(which='major', alpha=0.6)
    plt.grid(which='minor', alpha=0.3)
    plt.savefig('graphs\Regrips rotations tilts and AUFs vs solve time.png', dpi=400)
    
    #graph for move counts
    plt.figure(4)
    plt.xlim(5, 35)
    plt.ylim(0, 100)
    
    plt.title("Move counts for each step vs. solve time")
    plt.xlabel('Solve time (s)')
    plt.ylabel('Move count')
    
    plt.scatter(solvetimes, crossmoves, s=5)
    plt.scatter(solvetimes, f2lmoves, s=5)
    plt.scatter(solvetimes, lastlayermoves, s=5)
    plt.scatter(solvetimes, totalmoves, s=5)
    
    f11 = np.poly1d(np.polyfit(solvetimes, crossmoves, 1))
    f12 = np.poly1d(np.polyfit(solvetimes, f2lmoves, 1))
    f13 = np.poly1d(np.polyfit(solvetimes, lastlayermoves, 1))
    f14 = np.poly1d(np.polyfit(solvetimes, totalmoves, 1))
    
    plt.plot(x, f11(x), label='Cross')
    plt.plot(x, f12(x), label='F2L')
    plt.plot(x, f13(x), label='Last layer')
    plt.plot(x, f14(x), label='Total')
    
    plt.legend()
    plt.minorticks_on()
    plt.grid(which='major', alpha=0.6)
    plt.grid(which='minor', alpha=0.3)
    plt.savefig('graphs\Move counts for each step vs solve time.png', dpi=400)
    
    #graph for pauses for each step
    plt.figure(5)
    plt.xlim(5, 35)
    plt.ylim(-0.25, 8)
    
    plt.title("Pause times for each step vs. solve time")
    plt.xlabel('Solve time (s)')
    plt.ylabel('Total pause time (s)')
    
    plt.scatter(solvetimes2, crosspauses, s=5)
    plt.scatter(solvetimes2, f2lpauses, s=5)
    plt.scatter(solvetimes2, lastlayerpauses, s=5)
    plt.scatter(solvetimes2, ctofpauses, s=5)
    
    f15 = np.poly1d(np.polyfit(solvetimes2, crosspauses, 1))
    f16 = np.poly1d(np.polyfit(solvetimes2, ctofpauses, 1))
    f17 = np.poly1d(np.polyfit(solvetimes2, f2lpauses, 1))
    f18 = np.poly1d(np.polyfit(solvetimes2, lastlayerpauses, 1))
    
    plt.plot(x, f15(x), label='Cross')
    plt.plot(x, f16(x), label='F2L')
    plt.plot(x, f17(x), label='Last layer')
    plt.plot(x, f18(x), label='Cross to F2L transition')
    
    plt.legend()
    plt.minorticks_on()
    plt.grid(which='major', alpha=0.6)
    plt.grid(which='minor', alpha=0.3)
    plt.savefig('graphs\Pause times for each step vs solve time.png', dpi=400)
    
    #graph for tps for each step
    plt.figure(6)
    plt.xlim(5, 35)
    plt.ylim(0, 10)
    
    plt.title("TPS for each step vs. solve time")
    plt.xlabel('Solve time (s)')
    plt.ylabel('Turns per second')
    
    plt.scatter(solvetimes, crosstps, s=5)
    plt.scatter(solvetimes, f2ltps, s=5)
    plt.scatter(solvetimes, lastlayertps, s=5)
    
    f19 = np.poly1d(np.polyfit(solvetimes, crosstps, 1))
    f20 = np.poly1d(np.polyfit(solvetimes, f2ltps, 1))
    f21 = np.poly1d(np.polyfit(solvetimes, lastlayertps, 1))
    
    plt.plot(x, f19(x), label='Cross')
    plt.plot(x, f20(x), label='F2L')
    plt.plot(x, f21(x), label='Last layer')
    
    plt.legend()
    plt.minorticks_on()
    plt.grid(which='major', alpha=0.6)
    plt.grid(which='minor', alpha=0.3)
    plt.savefig('graphs\TPS for each step vs solve time.png', dpi=400)
    
    #graph for pause fractions for each step
    plt.figure(7)
    plt.xlim(5, 35)
    plt.ylim(-0.025, 0.8)
    
    plt.title("Fraction of each step spent pausing vs. solve time")
    plt.xlabel('Solve time (s)')
    plt.ylabel('Fraction of step time')
    
    plt.scatter(solvetimes2, crosspausefrac, s=5)
    plt.scatter(solvetimes2, f2lpausefrac, s=5)
    plt.scatter(solvetimes2, lastlayerpausefrac, s=5)
    
    f22 = np.poly1d(np.polyfit(solvetimes2, crosspausefrac, 1))
    f23 = np.poly1d(np.polyfit(solvetimes2, f2lpausefrac, 1))
    f24 = np.poly1d(np.polyfit(solvetimes2, lastlayerpausefrac, 1))
    
    plt.plot(x, f22(x), label='Cross')
    plt.plot(x, f23(x), label='F2L')
    plt.plot(x, f24(x), label='Last layer')
    
    plt.legend()
    plt.minorticks_on()
    plt.grid(which='major', alpha=0.6)
    plt.grid(which='minor', alpha=0.3)
    plt.savefig('graphs\Fraction of each step spent pausing vs solve time.png', dpi=400)
    
    #graph for pause fraction vs. TPS
    plt.figure(8)
    plt.xlim(1, 9)
    plt.ylim(0.1, 0.7)
    
    plt.title("Fraction of solve spent pausing vs. TPS")
    plt.xlabel('Turns per second')
    plt.ylabel('Fraction of solve time')
    
    plt.scatter(tps2, pausefrac, s=5)
    
    f25 = np.poly1d(np.polyfit(tps2, pausefrac, 1))
    
    plt.plot(x, f25(x))
    
    plt.legend()
    plt.minorticks_on()
    plt.grid(which='major', alpha=0.6)
    plt.grid(which='minor', alpha=0.3)
    plt.savefig('graphs\Fraction of solve spent pausing vs TPS.png', dpi=400)

#reddit survey data
with open('Mega Survey.tsv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    next(spamreader)
    
    num_responses = 0
    num_valid = 0
    
    for num, row in enumerate(spamreader, start=1):
        response = []
        response_valid = True
        
        for i in range(6):
            if len(row[i]) > 0:
                if i in range(2, 6) and ':' in row[i]:
                    tmp = row[i].split(':')
                    secs = int(tmp[0])*60 + float(tmp[1])
                    if secs < 500:
                        response.append(secs)
                    else:
                        response.append(-1.0)
                        response_valid = False
                else:
                    response.append(float(row[i]))
            else:
                response.append(-1.0)
                response_valid = False
                
        if (response[2] > response[3] or
            response[3] > response[4] or
            response[4] > response[5]):
            response_valid = False
        
        tempalgs = 0;
        for alg in row[6].split(','):
            if alg.strip() in algnums:
                tempalgs += algnums[alg.strip()]
        if tempalgs == 0 or tempalgs > 300:
            response.append(-1.0)
            response_valid = False
        else:
            response.append(tempalgs)
            
        print(num, response, response_valid)
        
        num_responses += 1
        if response_valid:
            responses.append(response)
            num_valid += 1

    print('Printed responses from Reddit survey.')    
    print(f'{num_responses} responses, {num_valid} were '
          f'valid ({round(100*num_valid/num_responses,1)}%).')
          
    responses_by_q = list()
    for q in range(7):
        this_question = list()
        for i, arr in enumerate(responses):
            this_question.append(arr[q])
        responses_by_q.append(this_question)
    
    #lists for graph data
    cubingmonths = list(responses_by_q[0])
    speedcubingmonths = list(responses_by_q[1])
    pbsingle = list(responses_by_q[2])
    ao5 = list(responses_by_q[3])
    ao12 = list(responses_by_q[4])
    ao100 = list(responses_by_q[5])
    algsknown = list(responses_by_q[6])
    
    #x range for lines of best fit
    x = np.linspace(0, 1000, 10000)
    
    #for exponential fit
    def func1(x, a, b, c, d):
        return a*np.exp(-c*(x-b))+d
        
    #for linear fit through origin
    def func2(x, a):
        return a * x
    
    #graph for ao100 vs. months of speedcubing
    plt.figure(9)
    plt.xlim(0, 84)
    plt.ylim(0, 60)
    
    plt.title("Ao100 vs. months of speedcubing")
    plt.xlabel('Months')
    plt.ylabel('Ao100 (s)')
    
    plt.scatter(speedcubingmonths, ao100, s=1)
    
    popt1, pcov1 = curve_fit(func1, speedcubingmonths, ao100, [7, 9, 0.1, 18])
    
    plt.plot(x, func1(x, *popt1))
    
    plt.minorticks_on()
    plt.grid(which='major', alpha=0.6)
    plt.grid(which='minor', alpha=0.3)
    plt.savefig('graphs\Ao100 vs months of speedcubing.png', dpi=400)
    
    #graph for ao100 vs. number of algs known
    plt.figure(10)
    plt.xlim(0, 300)
    plt.ylim(0, 60)
    
    plt.title("Ao100 vs. number of algorithms known")
    plt.xlabel('Number of algorithms known')
    plt.ylabel('Ao100 (s)')
    
    plt.scatter(algsknown, ao100, s=1)
    
    popt2, pcov2 = curve_fit(func1, algsknown, ao100, [1, 250, 0.01, 10])
    
    plt.plot(x, func1(x, *popt2))
    
    plt.minorticks_on()
    plt.grid(which='major', alpha=0.6)
    plt.grid(which='minor', alpha=0.3)
    plt.savefig('graphs\Ao100 vs number of algorithms known.png', dpi=400)
    
    #graph for pb single, ao5, and ao12 vs ao100
    plt.figure(11)
    plt.xlim(0, 60)
    plt.ylim(0, 60)
    
    plt.title("PB single, Ao5, and Ao12 vs. Ao100")
    plt.xlabel('Ao100 (s)')
    plt.ylabel('Time (s)')
    
    plt.scatter(ao100, pbsingle, s=1)
    plt.scatter(ao100, ao5, s=1)
    plt.scatter(ao100, ao12, s=1)
    
    popt3, pcov3 = curve_fit(func2, ao100, pbsingle)
    popt4, pcov4 = curve_fit(func2, ao100, ao5)
    popt5, pcov5 = curve_fit(func2, ao100, ao12)
    
    plt.plot(x, func2(x, *popt3), label='PB single')
    plt.plot(x, func2(x, *popt4), label='Average of 5')
    plt.plot(x, func2(x, *popt5), label='Average of 12')
    
    plt.legend()
    plt.minorticks_on()
    plt.grid(which='major', alpha=0.6)
    plt.grid(which='minor', alpha=0.3)
    plt.savefig('graphs\PB single Ao5 and Ao12 vs Ao100.png', dpi=400)
    
    plt.show()

print('Exported graphs as PNGs.')
