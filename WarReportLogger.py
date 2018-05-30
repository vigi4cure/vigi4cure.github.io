#!/usr/bin/python3.4

import datetime
import operator
import numpy as np
import pandas as pd
from mm_bot import *
from collections import defaultdict


def main_logger(df2, df1, timeframe = None):
    now = datetime.datetime.now()

    #don't understand the following block of code:
    ne = (df1 != df2).any(1)
    ne_stacked = (df1 != df2).stack()
    changed = ne_stacked[ne_stacked]
    difference_locations = np.where(df1 != df2)
    changed_from = df1.values[difference_locations]
    changed_to = df2.values[difference_locations]
    changed_df = pd.DataFrame({'from': changed_from, 'to': changed_to}, index=changed.index)

    changed_df2 = changed_df.unstack()
    # its making some sort of multi-index array but I can't figure out how to slice or work with the data.  Un stack atleast gets
    # it back into a form I can work with but this seems very inefficient, need to figure out how to work with multi-index df
    # print(changed_df2)

    bot = 'Strava-bot'
    icon = 'http://vigi4cure.github.io/bot.png'
    # init('shtest003', '61r88z7o9tn6tph1sypfim3joy', '1hrzxecjjfgbfxdfcch8mhb45y')
    if len(changed_df2) == 0:
        # init('Warlords', '61r88z7o9tn6tph1sypfim3joy', '1hrzxecjjfgbfxdfcch8mhb45y')
        # postmessage('no change', icon, bot)
        print('no change')
        return

    changed_from2 = changed_df2['from']['type']
    changed_to2 = changed_df2['to']['type']

    df_changed_from = pd.DataFrame(changed_from2)
    df_changed_from = df_changed_from[df_changed_from.type.notnull()]

    df_changed_to = pd.DataFrame(changed_to2)
    df_changed_to = df_changed_to[df_changed_to.type.notnull()]


    war_report_dict = {}
    winner_loser_segment_dict = {}
    for x in df_changed_to['type'].unique():

        personcount = defaultdict(int)
        person_segment_list = defaultdict(list)

        for y in df_changed_to[df_changed_to['type'] == x].index:

            #don't get why the output here is a numpy array:
            beatperson_array = df_changed_from[df_changed_from.index == y].values[0]

            #converting to string:
            beatperson_string = str(beatperson_array[0])

            personcount[beatperson_string] += 1
            person_segment_list[beatperson_string].append(y)

        war_report_dict[x] = personcount
        winner_loser_segment_dict[x] = person_segment_list


    if timeframe is None:
        logfile=open('warlog.csv', 'a+')
        title = 'Strava Segment Leaderboards **(All Time)**\n'
    else:
        logfile=open('warlog_' + timeframe + '.csv', 'a+')
        title = 'Strava Segment Leaderboards **(' + timeframe + ')**\n'

    for warlord in war_report_dict:
        for victim in sorted(war_report_dict[warlord].items(), key=operator.itemgetter(1), reverse=True):
            territory = 'territory' if victim[1] == 1 else 'territories'
            action = ' conquered ' + str(victim[1]) + ' ' + territory + ' from ' + victim[0]
            if victim[0] == 'UNCLAIMED':
                action = ' claimed ' + str(victim[1]) + ' unowned ' + territory

            msg = warlord + action
            print(msg)

            title += msg
            for id in winner_loser_segment_dict[warlord][victim[0]]:
                title += ' [{id}](http://strava.com/segments/{id})'.format(id=id)
            title += '\n'

            segment_IDs = ' '.join(map(str, winner_loser_segment_dict[warlord][victim[0]]))
            line = str(now) + ',' + warlord + action + ',' + segment_IDs
            logfile.write(line + '\n')
    logfile.close()

    init('Warlords', '61r88z7o9tn6tph1sypfim3joy', '1hrzxecjjfgbfxdfcch8mhb45y')
    postmessage(title, icon, bot)

if __name__ == "__main__":
  main()







