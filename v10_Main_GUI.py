# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 16:51:20 2019

@author: 43739
"""

from v10_Main_Message_Parser import Message_to_Information
from v10_Main_Information_Parser import Order_Book
from v10_Main_Analysis import Order_Book_Monitor 
import os
import pandas as pd
from tkinter import mainloop,Button,Label,StringVar,Entry
import tkinter as tk

def main():
    Window=tk.Tk()
    Window.title('Order Book v1.0')
    Window.geometry("500x400")
    Label(Window,text='Stock: ').grid(row=0,column=0)
    default_stock=StringVar()
    default_stock.set(r'AAPL')
    stock_input = Entry(Window,textvariable=default_stock)
    stock_input.grid(row=0,column=1,columnspan=3)
    #order book
    #title 
    Label(Window,text='Price').grid(row=1,column=1)
    Label(Window,text='Size').grid(row=1,column=2)
    Label(Window,text='Order').grid(row=1,column=3)
    #ask  
    Label(Window,text='ASK5').grid(row=2,column=0)
    a5p=Label(Window,text='-------')#.grid(row=2,column=1)
    a5s=Label(Window,text='-------')#.grid(row=2,column=2)
    a5o=Label(Window,text='-------')#.grid(row=2,column=3)
    Label(Window,text='ASK4').grid(row=3,column=0)
    a4p=Label(Window,text='-------')#.grid(row=3,column=1)
    a4s=Label(Window,text='-------')#.grid(row=3,column=2)
    a4o=Label(Window,text='-------')#.grid(row=3,column=3)
    Label(Window,text='ASK3').grid(row=4,column=0)
    a3p=Label(Window,text='-------')#.grid(row=4,column=1)
    a3s=Label(Window,text='-------')#.grid(row=4,column=2)
    a3o=Label(Window,text='-------')#.grid(row=4,column=3)
    Label(Window,text='ASK2').grid(row=5,column=0)
    a2p=Label(Window,text='-------')#.grid(row=5,column=1)
    a2s=Label(Window,text='-------')#.grid(row=5,column=2)
    a2o=Label(Window,text='-------')#.grid(row=5,column=3)
    Label(Window,text='ASK1').grid(row=6,column=0)
    a1p=Label(Window,text='-------')#.grid(row=6,column=1)
    a1s=Label(Window,text='-------')#.grid(row=6,column=2)
    a1o=Label(Window,text='-------')#.grid(row=6,column=3)
    
    ask=[[a1p,a1s,a1o],[a2p,a2s,a2o],[a3p,a3s,a3o],[a4p,a4s,a4o],[a5p,a5s,a5o]]
    for i in range(len(ask)):
        for j in range(len(ask[0])):
            ask[i][j].grid(row=(6-i),column=j+1)#assign the location, see the grid part 
    
    
    Label(Window,text='---------------------------------------').grid(row=7,column=0,columnspan=4)
    
    #bid
    Label(Window,text='BID1').grid(row=8,column=0)
    b1p=Label(Window,text='-------')#.grid(row=8,column=1)
    b1s=Label(Window,text='-------')#.grid(row=8,column=2)
    b1o=Label(Window,text='-------')#.grid(row=8,column=3)
    Label(Window,text='BID2').grid(row=9,column=0)
    b2p=Label(Window,text='-------')#.grid(row=9,column=1)
    b2s=Label(Window,text='-------')#.grid(row=9,column=2)
    b2o=Label(Window,text='-------')#.grid(row=9,column=3)
    Label(Window,text='BID3').grid(row=10,column=0)
    b3p=Label(Window,text='-------')#.grid(row=10,column=1)
    b3s=Label(Window,text='-------')#.grid(row=10,column=2)
    b3o=Label(Window,text='-------')#.grid(row=10,column=3)
    Label(Window,text='BID4').grid(row=11,column=0)
    b4p=Label(Window,text='-------')#.grid(row=11,column=1)
    b4s=Label(Window,text='-------')#.grid(row=11,column=2)
    b4o=Label(Window,text='-------')#.grid(row=11,column=3)
    Label(Window,text='BID5').grid(row=12,column=0)
    b5p=Label(Window,text='-------')#.grid(row=12,column=1)
    b5s=Label(Window,text='-------')#.grid(row=12,column=2)
    b5o=Label(Window,text='-------')#.grid(row=12,column=3)
    
    bid=[[b1p,b1s,b1o],[b2p,b2s,b2o],[b3p,b3s,b3o],[b4p,b4s,b4o],[b5p,b5s,b5o]]
    for i in range(len(bid)):
        for j in range(len(bid[0])):
            bid[i][j].grid(row=(8+i),column=j+1)#assign the location, see the grid part 
            
    time=Label(Window,text='--：--：--')#.grid(row=12,column=3)
    time.grid(row=0,column=5)
    
    def Order_Book_Demo():
        os.chdir('D:\\Nasdaq')
        file=open('10302019.NASDAQ_ITCH50','rb')
        book=Order_Book()
        monitor=Order_Book_Monitor()
        #the messages we use for construct order book
        useful={'A', #Add_Order_Message(data),         
                'F', #Add_Order_MPID_Attribution_Message(data),  
                'E', #Order_Executed_Message(data), 
                'C', #Order_Executed_With_Price_Message(data),         
                'X', #Order_Cancel_Message(data),         
                'D', #Order_Delete_Message(data), 
                'U', #Order_Replace_Message(data),           
                'P'} #Trade_Message_Non_Cross(data)
        
        Find_Locate_or_not=False
        information={}
        stock=stock_input.get()
        
        while not('Event' in information.keys() and information['Event']=='End of Messages'):
            #read message one by one
            size=int.from_bytes(file.read(2),'big')
            data=file.read(size)
            information=Message_to_Information(data)
            #find Stock_Locate for the stock we want
            if not Find_Locate_or_not:
                if information['Message_Type']=='R' and information['Stock'].strip()==stock:
                    Stock_Locate=information['Stock_Locate']
                    Find_Locate_or_not=True
                else:
                    pass
            else:
                if information['Message_Type'] in useful and information['Stock_Locate']==Stock_Locate:
                    book.update(information)
                    #group by, count, sum, sort and so on
                    ask_order_book=book.order_book_ask.reset_index().groupby(['Price']).agg({'Shares': ['sum'], 'index': ['count']}).reset_index().sort_values(by=['Price'],ascending=False)
                    bid_order_book=book.order_book_bid.reset_index().groupby(['Price']).agg({'Shares': ['sum'], 'index': ['count']}).reset_index().sort_values(by=['Price'],ascending=False)
                    ask_order_book.columns=['Price','Shares','Orders']
                    bid_order_book.columns=['Price','Shares','Orders']
                    #get latest time
                    sorted_time=sorted((book.order_book_ask['Timestamp'].tolist()+book.order_book_bid['Timestamp'].tolist()),key=lambda x:x.Nanoseconds,reverse=True)
                    if sorted_time:
                        cur_time=sorted_time[0]
                        time['text']=str(cur_time.Hours)+':'+str(cur_time.Minutes)+':'+str(cur_time.Seconds)
                    else:
                        pass
                    #clean the order book
                    for i in range(5):
                        for j in range(3):
                            ask[i][j]['text']='-------'
                            bid[i][j]['text']='-------'    
                    #update order book               
                    for i in range(min(5,len(ask_order_book))):
                        ask[i][0]['text']=ask_order_book.loc[i,'Price']
                        ask[i][1]['text']=ask_order_book.loc[i,'Shares']
                        ask[i][2]['text']=ask_order_book.loc[i,'Orders']
                            
                    for i in range(min(5,len(bid_order_book))):
                        bid[i][0]['text']=bid_order_book.loc[len(bid_order_book)-i-1,'Price']
                        bid[i][1]['text']=bid_order_book.loc[len(bid_order_book)-i-1,'Shares']
                        bid[i][2]['text']=bid_order_book.loc[len(bid_order_book)-i-1,'Orders']
                    
                    #order book monitor
                    ask_data=[[ask[i][j]['text'] for j in range(3)]for i in range(5)]
                    bid_data=[[bid[i][j]['text'] for j in range(3)]for i in range(5)]
                    monitor.update(ask_data,bid_data,cur_time)    
                    Window.update()

        monitor.output()
        history=monitor.level2_data
        history.to_csv(stock+'.csv')
        
        
    Button(Window, text="start demo",command=Order_Book_Demo).grid(row=0,column=4)
    mainloop()    
    
if __name__ == '__main__':
    main()