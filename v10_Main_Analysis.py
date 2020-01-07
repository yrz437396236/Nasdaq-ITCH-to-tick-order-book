# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:20:06 2019

@author: 43739
"""
    
import pandas as pd

class Order_Book_Monitor():
    #That's probably as efficient as any, but Pandas/numpy structures are fundamentally
    #not suited for efficiently growing. They work best when they are created with a fixed size 
    #and stay that way. – BrenBarn
    #see the link below
    #https://link.zhihu.com/?target=http%3A//stackoverflow.com/questions/13751926/efficiently-add-single-row-to-pandas-series-or-dataframe%23comment18900162_13751926
    ########################################
    # initialize the class
    def __init__(self):   
        self.a1=[]
        self.a2=[]
        self.a3=[]
        self.a4=[]
        self.a5=[]
        self.b1=[]
        self.b2=[]
        self.b3=[]
        self.b4=[]
        self.b5=[]
        self.time=[]
        self.level2_data=pd.DataFrame()
        
    def update(self,ask_data,bid_data,cur_time):
        #ask_data=[[a1p,a1s,a1o],[a2p,a2s,a2o],[a3p,a3s,a3o],[a4p,a4s,a4o],[a5p,a5s,a5o]]
        #bid_data=[[b1p,b1s,b1o],[b2p,b2s,b2o],[b3p,b3s,b3o],[b4p,b4s,b4o],[b5p,b5s,b5o]]
        self.time.append(cur_time)
        self.a1.append(ask_data[0])
        self.a2.append(ask_data[1])
        self.a3.append(ask_data[2])
        self.a4.append(ask_data[3])
        self.a5.append(ask_data[4])
        self.b1.append(bid_data[0])
        self.b2.append(bid_data[1])
        self.b3.append(bid_data[2])
        self.b4.append(bid_data[3])
        self.b5.append(bid_data[4])           
        
    def output(self):
        self.level2_data=pd.concat([pd.DataFrame([x.Nanoseconds for x in self.time],columns=['Nanoseconds']),
            pd.DataFrame(self.time,columns=['Timestamp']),
            pd.DataFrame(self.a1,columns=['a1p','a1s','a1o']),
            pd.DataFrame(self.a2,columns=['a2p','a2s','a2o']),
            pd.DataFrame(self.a3,columns=['a3p','a3s','a3o']),
            pd.DataFrame(self.a4,columns=['a4p','a4s','a4o']),
            pd.DataFrame(self.a5,columns=['a5p','a5s','a5o']),
            pd.DataFrame(self.b1,columns=['b1p','b1s','b1o']),
            pd.DataFrame(self.b2,columns=['b2p','b2s','b2o']),
            pd.DataFrame(self.b3,columns=['b3p','b3s','b3o']),
            pd.DataFrame(self.b4,columns=['b4p','b4s','b4o']),
            pd.DataFrame(self.b5,columns=['b5p','b5s','b5o'])],axis=1)
    
