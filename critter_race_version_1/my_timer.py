import schedule
import time, sys, os
import subprocess

num_gens = 0
keep_running = True
max_gens = 10
times_program_run = 0

def job():
    global num_gens
    global keep_running
    global max_gens
    global times_program_run
    num_gens += 1
    print("num_gens: {}".format(num_gens))
    if num_gens > max_gens:
        schedule.clear()
        keep_running = False
        print("******* PROGRAM RUN {} TIMES ********".format(times_program_run))
    else:
        times_program_run += 1
        pid = subprocess.Popen([sys.executable, "doodling_tkinter.py"])
        print("****** PROGRAM RUN {} TIMES *********".format(times_program_run))
        #subprocess.run(["ls", "-l"])

print("Max gens: {}".format(max_gens))
schedule.every(18).seconds.do(job)

while keep_running:
    schedule.run_pending()
    time.sleep(1)

# if __name__ == "__main__":
#     program_name = os.path.basename(__file__)
#     if len(sys.argv) == 1:
#         print("{} needs one argument. Here are the options:")
#         print("")
#         print("Number of genertions:")
#         print("> {} 10".format(program_name))
#         sys.exit()
#     try:
#         max_gens = int(sys.argv[1])
#     except:
#         print("The max number of generations needs to be an integer.")
#         print("Here is the input give: {}".format(sys.argv[1]))
