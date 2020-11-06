import time

class RatActivityCounter():
    def __init__(self, ratid, ratio, rat_label = "unknown"):
        self.ratid = ratid
        self.active_licks = 0
        self.inactive_licks = 0
        self.rewards = 0
        self.touch_counter = 0
        self.next_ratio = ratio
        self.rat_label = rat_label
        self.last_act_licks = {"time":float(time.time()), "scantime":0}
        self.last_inact_licks = {"time":float(time.time()), "scantime":0}
        self.pumptimedout = False


    @staticmethod 
    def update_last_licks(lick_dict, lick_time, scan_time):
        lick_dict["time"] = lick_time
        lick_dict["scantime"] = scan_time
    
    @staticmethod
    def colored_print(ratID, act_count, inact_count, reward_count, timeout):
        print (ratID+ \
            "\x1b[0;32;40m" + \
            ": Active=" + str(act_count)+ \
            "\x1b[0m" + \
            "\x1b[0;33;40m" + \
            " Inactive="+str(inact_count) + \
            "\x1b[0m" + \
            "\x1b[0;32;40m" + \
            " Reward=" +  str(reward_count) + \
            "\x1b[0m" + \
            "\x1b[0;35;40m" + \
            " Timeout: "+ str(timeout) + \
            "\x1b[0m"
            )

    @staticmethod
    def show_data(sessionLength, schedule, lapsed,
                  rat1,rat2,rat_unknown, phase="progress"):
        if schedule == "pr":
            minsLeft = int((sessionLength - (time.time() - rat1.last_act_licks["time"])) / 60)
        else:
            minsLeft = int((sessionLength-lapsed)/60)
        if phase == "final":
            print("{} Session_{}".format())

        print ("\x1b[0;31;40m" + \
                "[" + str(minsLeft) + " min Left]" + \
                "\x1b[0m")

        RatActivityCounter.colored_print(rat1.ratid, rat1.active_licks,
                                         rat1.inactive_licks, rat1.rewards,
                                         rat1.pumptimedout)
        RatActivityCounter.colored_print(rat2.ratid, rat2.active_licks,
                                         rat2.inactive_licks, rat2.rewards,
                                         rat2.pumptimedout)
        RatActivityCounter.colored_print(rat_unknown.ratid, rat_unknown.active_licks,
                                         rat_unknown.inactive_licks, rat_unknown.rewards,
                                         rat_unknown.pumptimedout)

        return time.time() 


    def incr_rewards(self):
        self.rewards = self.rewards + 1

    def incr_active_licks(self):
        self.active_licks = self.active_licks + 1

    def incr_inactive_licks(self):
        self.inactive_licks = self.inactive_licks + 1

    def incr_touch_counter(self):
        self. touch_counter = self.touch_counter + 1

    def reset_touch_counter(self):
        self.touch_counter = 0