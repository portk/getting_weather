import numpy as np
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import datetime

def record(day):
    time1=day+'0000'
    time2=day+'2300'
    url = 'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm3.php?tm1='+time1+'&tm2='+time2+'&stn=156&help=1&authKey=개인API_Key'
    html=urlopen(url)
    bs = soup(html.read(), 'html.parser')
    date_list = []
    temp_list = []
    wind_list = []
    pa_list = []
    wd_list = []
    for i in str(bs).split('\n')[:-1]:
        if '#' not in i:
            date_list.append(i.split()[0])
            temp_list.append(i.split()[11])
            wind_list.append(i.split()[3])
            pa_list.append(i.split()[7])
            wd_list.append(i.split()[15])
    data = (
        {
            "일시":date_list,
            "온도":temp_list,
            "풍량":wind_list,
            "기압":pa_list,
            "강수량":wd_list
        }
    )
    df = pd.DataFrame(data)
    df = df.astype({"온도":'float','풍량':'float','기압':'float','강수량':'float'})
    data1=pd.Series(df.iloc[0,0][0:8], index=['날짜'])
    data2=df.iloc[:,1:3].mean().round(2)
    data3=pd.Series(df.iloc[::3,3].mean().round(2), index=['일평균기압'])
    data4=[]
    for i in  df.iloc[:,4]:
        if i > 0:
            data4.append(i)
    data4 = pd.Series(np.sum(data4), index=['총강수량']).round(2)
    daydf=pd.DataFrame(pd.concat([data1,data2,data3,data4])).T
    daydf = daydf.astype({'온도':float,'풍량':float,'일평균기압':float,'총강수량':float})
    try:
        ds=pd.read_csv("/content/drive/MyDrive/Colab_Notebooks/weather.csv").iloc[:,1:]
    except:
        ds=pd.DataFrame()
    daydf2=pd.concat([ds,daydf], ignore_index=True)
    daydf2.to_csv("/content/drive/MyDrive/Colab_Notebooks/weather.csv")

#날짜구하기
from datetime import datetime, timedelta
a = datetime.strptime('18/12/23', '%d/%m/%y')
b = datetime.strptime('19/02/24', '%d/%m/%y')
dates=[(a + timedelta(days=i)).strftime("%Y%m%d") for i in range((b-a).days+1)]

for i in dates:
    day = str(i)
    print(i,'일자 자료 정리중 입니다.')
    record(day)
