#!/usr/bin/python3

import plotly
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime 

def Scatter_Plot2(df,colour,x_axis,y_axis,mode,display,fill,filename):  
    cat_list = df[colour].unique()
    cat_list = sorted(cat_list) #, reverse=True)
    year = ''
    if filename == 'distance' or filename == 'elevation_gain':
        year = '_' + str(datetime.now().year)
        cat_list.remove('UNCLAIMED')
    
    data=[]
    for item in cat_list:
        x=df.loc[df[colour] == item][x_axis]
        y=df.loc[df[colour] == item][y_axis]
        
        try:
        	friend_colour = '#'+str(friend_df.loc[friend_df['name'] == item,'colour'].values[0])
        except:
        	friend_colour = '#646464'
         
        latest_y = int(y[y.index[-1]])
        if filename == 'distance' or filename == 'elevation_gain':
            try:
                item = str(df.loc[df[colour] == item, 'sport'].values[-1]) + item
            except:
                pass
            item = format(latest_y, '04d') + ' ' + item

        trace = go.Scatter(
            x=x,
            y=y,
            name=item,
            mode=mode,
            fill=fill,
            fillcolor = friend_colour,
            line=dict(color = friend_colour)
        )
        if (filename == 'distance' or filename == 'elevation_gain') and len(data) != 0:
            for i in range(len(data)):
                dis = data[i]['y'][data[i]['y'].index[-1]]
                if latest_y > dis:
                  data.insert(i, trace)
                  break
            else:
                data.append(trace) 
        else:
            data.append(trace) 
    
    layout = go.Layout( 
        xaxis = {'title': x_axis },
        yaxis = {'title': display},
        legend = {'x': 100}
    )

    fig = go.Figure(data=data, layout=layout)
    
    plotly.offline.plot(fig, filename=filename+'_plot' + year + '.html',auto_open=False)
    return

def Bar_Plot(df,colour,x_axis,y_axis,mode,display,fill,filename):  
    
    
    df = df.sort_values([y_axis], ascending=False)
    df['colour'] = '#' + df['colour'].astype(str)
    x=df[colour]
    y=df[y_axis]

    colour = df['colour']
    
    
    
    data=[]
    
    
    trace = go.Bar(
        x=x,
        y=y,
        #name=item,
        #mode=mode,
        #fill=fill,
        marker=dict(color=colour),
        #fillcolor = '#646464',
        #line=dict(color = friend_colour)
       
        )
    data.append(trace) 
    
    layout = go.Layout( 
        xaxis = {'title': x_axis},
        yaxis = {'title': y_axis},
        legend = {'x': 100}
      
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=filename+'_plot.html',auto_open=False)
    return

friend_df = pd.read_csv('friend_colour_new.csv',index_col=False)

#line graph of segments over time:
df = pd.read_csv('segmentcountovertime.csv')
Scatter_Plot2(df,'name','date','count','lines','count','','segments_over_time')

#stacked graph of segments over time:
df_cumsum = df.groupby(by=['date','name']).max().groupby(level=[0]).cumsum()['count']
df_cumsum = df_cumsum.unstack().fillna(0).stack()
df_cumsum = df_cumsum.reset_index()
df_cumsum.rename(columns={0: 'count'}, inplace=True)
Scatter_Plot2(df_cumsum,'name','date','count','lines','count','tozeroy','stacked')

#bar graph of current segment count snapshot:
df_snapshot = pd.read_csv('segmentcount.csv')
Bar_Plot(df_snapshot,'name','date','count','lines','count','tozeroy','segment_count_snapshot')

#bar graph of current segment count snapshot for this year:
df_snapshot_this_year = pd.read_csv('segmentcount_this_year.csv')
Bar_Plot(df_snapshot_this_year,'name','date','count','lines','count','tozeroy','segment_count_snapshot_this_year')

year = str(datetime.now().year)

#distance list graph:
#line graph of segments over time:
df_distance = pd.read_csv('distance_' + year + '.csv')
Scatter_Plot2(df_distance,'name','datetime','distance','lines','Distance(km)','','distance')

#distance list graph:
#line graph of segments over time:
df_elevation_gain = pd.read_csv('elevation_gain_' + year + '.csv')
Scatter_Plot2(df_elevation_gain,'name','datetime','elevation gain','lines','Elevation Gain(meter)','','elevation_gain')
