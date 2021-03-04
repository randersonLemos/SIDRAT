import seaborn as sb
import matplotlib as mpl
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
plt.style.use('seaborn-talk')

mpl.rcParams['axes.titlesize']  = 18.0
mpl.rcParams['axes.labelsize']  = 18.0
mpl.rcParams['xtick.labelsize'] = 17.0
mpl.rcParams['ytick.labelsize'] = 17.0
mpl.rcParams['legend.fontsize'] = 18.0
mpl.rcParams["legend.title_fontsize"] = 18.0
mpl.rcParams['lines.linewidth'] =  4.0

def save(TrainDataObj, TestDataObj, ClassifierObj, savefig_root):
    trd = TrainDataObj
    ted = TestDataObj
    cl  = ClassifierObj

    fig, axs = plt.subplots(1,2, figsize=(10,8), tight_layout=True)

    title  = 'Tranning with iteration {} data and classification of iteration {} data'.format(trd.iteration, ted.iteration)
    title += '\nTrain data size {}'.format(len(trd.X))
    title += '\nTrain data oversampled size {}'.format(len(trd.Xos))
    title += '\nHit {} over 20 best samples'.format(cl.y['CLASS'].iloc[:20].sum())
    title += '\nThreshold {}'.format(cl.threshold)
    fig.suptitle(title, fontsize=20)

    _x = cl.y['CLASS'].tolist()
    _y = (cl.y['NPV'] / 1000000).tolist()

    axs[0].scatter(_x, _y, s=250)
    axs[0].scatter(_x[:20], _y[:20], s=250)

    axs[0].set_ylabel('NPV [MM$]')
    axs[0].set_xlabel('CLASS')

    axs[0].set_xticks([0,1])
    axs[0].set_xlim([-0.25, 1.25])

    axs[0].yaxis.set_major_locator(ticker.LinearLocator(5))
    axs[0].yaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))

    _x = [0,1]
    value_counts = cl.y['CLASS'].value_counts()
    if len(value_counts) == 2:
        _y = cl.y['CLASS'].value_counts()[_x].tolist()
    else: # Assumundo que tem apenas classe 1
        _y = [0]
        _y = _y + cl.y['CLASS'].value_counts().tolist()

    axs[1].bar(_x, _y)

    axs[1].set_ylabel('Qty')
    axs[1].set_xlabel('CLASS')

    axs[1].set_xticks([0,1])
    axs[1].set_yticks([0, 25, 50 , 75, 100])

    rects = axs[1].patches
    labels = _y

    for rect, label in zip(rects, labels):
        height = rect.get_height()
        axs[1].text(rect.get_x() + rect.get_width() / 2, height / 2, label,
                ha='center', va='center', fontsize=18)

    plt.savefig('{}/it_{}_it_{}'.format(savefig_root, trd.iteration, ted.iteration))
    plt.close()

    trd.save('{}/it_{}_it_{}_train.csv'.format(savefig_root, trd.iteration, ted.iteration))
    ted.y = cl.y
    ted.save('{}/it_{}_it_{}_test.csv'.format(savefig_root, trd.iteration, ted.iteration))


