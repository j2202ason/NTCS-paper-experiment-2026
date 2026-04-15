import ntcs_main
from ntcs_main import *
from dataStatis_main import *
from dataclean import *

curpath=os.path.join(os.getcwd(),"./experiments")   # path of experiments data store
ntcs_main.dskey="DEEPSEEK_API_KEY"    # set deepseek api key

def ifCleanData(fpath):
    if input('''
    select a mode:
    1: create a new experiment.The datum in experiments folder will be delete, and create a new experiment
    2: append. The datum in experiments will be preserve, and new experiment\'s data will append the end of last experiment.
    It should be noted that procedures such as clustering and visualization were performed on all data. 
    \n>''')=='1':
        clean(fpath)
    return 0


if __name__ == "__main__":
    visual_configure=1  # if visual_configure=1 then statistic data and visualize data,else no statistic and no visualize

    lstCase = [0] #, 1, 2, 3, 4]  # Configure a list of case indices
    turns=1 #10  # The experiment will be conducted for 10 runs.

    ifCleanData(curpath) # create a new of append

    run_experiment(lstCase,turns,curpath)  # run experiment
    if visual_configure==1:
        tmcode = datetime.datetime.now().strftime("%Y%m%d%M%S")
        statis(lstCase,curpath,tmcode)  # statistic and visualize if visual_configure=1


