# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 18:46:52 2019

@author: 43739
"""

import pandas as pd

class Order_Book():
    # initialize the class
    def __init__(self):        
        self.order_book_bid=pd.DataFrame(columns=['Shares','Price','Nanoseconds','Timestamp'])
        self.order_book_ask=pd.DataFrame(columns=['Shares','Price','Nanoseconds','Timestamp'])
        self.cur_time=0
    # update order book
    def update(self, information):
                
        def information_to_order_book(information):
            switcher = {       
                'A': Add_Order_Message_OB(information),         
                'F': Add_Order_MPID_Attribution_Message_OB(information),  
                'E': Order_Executed_Message_OB(information), 
                'C': Order_Executed_With_Price_Message_OB(information),         
                'X': Order_Cancel_Message_OB(information),         
                'D': Order_Delete_Message_OB(information), 
                'U': Order_Replace_Message_OB(information),           
#                'P': Trade_Message_Non_Cross_OB(information),    
#                looks like this part will product negative shares
            } 
            return switcher.get(information['Message_Type'], None) 
        #  
        def Add_Order_Message_OB(information):
            #to enable the switcher
            if not information['Message_Type']=='A':
                return 0   
            #buy/sale    
            if information['Buy_Sell_Indicator']=='S':
                self.order_book_ask.loc[information['Order_Reference_Number']]=[information['Shares'],information['Price'],information['Timestamp'].Nanoseconds,information['Timestamp']]
            else:
                self.order_book_bid.loc[information['Order_Reference_Number']]=[information['Shares'],information['Price'],information['Timestamp'].Nanoseconds,information['Timestamp']]
        
        def Add_Order_MPID_Attribution_Message_OB(information):
            #to enable the switcher
            if not information['Message_Type']=='F':
                return 0   
            #buy/sale    
            if information['Buy_Sell_Indicator']=='S':
                self.order_book_ask.loc[information['Order_Reference_Number']]=[information['Shares'],information['Price'],information['Timestamp'].Nanoseconds,information['Timestamp']]
            else:
                self.order_book_bid.loc[information['Order_Reference_Number']]=[information['Shares'],information['Price'],information['Timestamp'].Nanoseconds,information['Timestamp']]
        
        def Order_Executed_Message_OB(information):
            #to enable the switcher
            if not information['Message_Type']=='E':
                return 0   
            #buy/sale 
            if information['Order_Reference_Number'] in self.order_book_ask.index:
                origin_shares=self.order_book_ask.loc[information['Order_Reference_Number'],'Shares']
                new_shares=origin_shares-information['Executed_Shares']
                if new_shares: 
                #partly exercised               
                    self.order_book_ask.loc[information['Order_Reference_Number'],'Shares']=new_shares
                    self.order_book_ask.loc[information['Order_Reference_Number'],'Nanoseconds']=information['Timestamp'].Nanoseconds               
                    self.order_book_ask.loc[information['Order_Reference_Number'],'Timestamp']=information['Timestamp']              
                else:
                #fully exercised 
                    self.order_book_ask.drop([information['Order_Reference_Number']],inplace=True)
        
            elif information['Order_Reference_Number'] in self.order_book_bid.index:
                origin_shares=self.order_book_bid.loc[information['Order_Reference_Number'],'Shares']
                new_shares=origin_shares-information['Executed_Shares']
                if new_shares: 
                #partly exercised               
                    self.order_book_bid.loc[information['Order_Reference_Number'],'Shares']=new_shares
                    self.order_book_bid.loc[information['Order_Reference_Number'],'Nanoseconds']=information['Timestamp'].Nanoseconds               
                    self.order_book_bid.loc[information['Order_Reference_Number'],'Timestamp']=information['Timestamp']              
                else:
                #fully exercised 
                    self.order_book_bid.drop([information['Order_Reference_Number']],inplace=True)
                   
            else:
                print('Order not found!!!',information['Message_Type'],information['Order_Reference_Number'])
        
        def Order_Executed_With_Price_Message_OB(information):
            #to enable the switcher
            if not information['Message_Type']=='C':
                return 0   
            #buy/sale 
            if information['Order_Reference_Number'] in self.order_book_ask.index:
                origin_shares=self.order_book_ask.loc[information['Order_Reference_Number'],'Shares']
                new_shares=origin_shares-information['Executed_Shares']
                if new_shares: 
                #partly exercised               
                    self.order_book_ask.loc[information['Order_Reference_Number'],'Shares']=new_shares
                    self.order_book_ask.loc[information['Order_Reference_Number'],'Price']=information['Execution_Price']
                    self.order_book_ask.loc[information['Order_Reference_Number'],'Nanoseconds']=information['Timestamp'].Nanoseconds               
                    self.order_book_ask.loc[information['Order_Reference_Number'],'Timestamp']=information['Timestamp']              
                else:
                #fully exercised 
                    self.order_book_ask.drop([information['Order_Reference_Number']],inplace=True)
        
            elif information['Order_Reference_Number'] in self.order_book_bid.index:
                origin_shares=self.order_book_bid.loc[information['Order_Reference_Number'],'Shares']
                new_shares=origin_shares-information['Executed_Shares']
                if new_shares: 
                #partly exercised               
                    self.order_book_bid.loc[information['Order_Reference_Number'],'Shares']=new_shares
                    self.order_book_bid.loc[information['Order_Reference_Number'],'Price']=information['Execution_Price']
                    self.order_book_bid.loc[information['Order_Reference_Number'],'Nanoseconds']=information['Timestamp'].Nanoseconds               
                    self.order_book_bid.loc[information['Order_Reference_Number'],'Timestamp']=information['Timestamp']              
                else:
                #fully exercised 
                    self.order_book_bid.drop([information['Order_Reference_Number']],inplace=True)
                   
            else:
                print('Order not found!!!',information['Message_Type'],information['Order_Reference_Number'])
        
        def Order_Cancel_Message_OB(information):
            #to enable the switcher
            if not information['Message_Type']=='X':
                return 0  
            #buy/sale 
            if information['Order_Reference_Number'] in self.order_book_ask.index:
                origin_shares=self.order_book_ask.loc[information['Order_Reference_Number'],'Shares']
                new_shares=origin_shares-information['Cancelled_Shares']
                if new_shares: 
                #partly exercised               
                    self.order_book_ask.loc[information['Order_Reference_Number'],'Shares']=new_shares
                    self.order_book_ask.loc[information['Order_Reference_Number'],'Nanoseconds']=information['Timestamp'].Nanoseconds               
                    self.order_book_ask.loc[information['Order_Reference_Number'],'Timestamp']=information['Timestamp']              
                else:
                #fully exercised 
                    self.order_book_ask.drop([information['Order_Reference_Number']],inplace=True)
        
            elif information['Order_Reference_Number'] in self.order_book_bid.index:
                origin_shares=self.order_book_bid.loc[information['Order_Reference_Number'],'Shares']
                new_shares=origin_shares-information['Cancelled_Shares']
                if new_shares: 
                #partly exercised               
                    self.order_book_bid.loc[information['Order_Reference_Number'],'Shares']=new_shares
                    self.order_book_bid.loc[information['Order_Reference_Number'],'Nanoseconds']=information['Timestamp'].Nanoseconds               
                    self.order_book_bid.loc[information['Order_Reference_Number'],'Timestamp']=information['Timestamp']              
                else:
                #fully exercised 
                    self.order_book_bid.drop([information['Order_Reference_Number']],inplace=True)
                   
            else:
                print('Order not found!!!',information['Message_Type'],information['Order_Reference_Number'])
        
        def Order_Delete_Message_OB(information):
            #to enable the switcher
            if not information['Message_Type']=='D':
                return 0
            #buy/sale 
            if information['Order_Reference_Number'] in self.order_book_ask.index:
                    self.order_book_ask.drop([information['Order_Reference_Number']],inplace=True)
            elif information['Order_Reference_Number'] in self.order_book_bid.index:
                    self.order_book_bid.drop([information['Order_Reference_Number']],inplace=True)          
            else:
                print('Order not found!!!',information['Message_Type'],information['Order_Reference_Number'])
        
        def Order_Replace_Message_OB(information):
            #to enable the switcher
            if not information['Message_Type']=='U':
                return 0
            #buy/sale 
            if information['Original_Order_Reference_Number'] in self.order_book_ask.index:
                    #delete
                    self.order_book_ask.drop([information['Original_Order_Reference_Number']],inplace=True)
                    #add
                    self.order_book_ask.loc[information['New_Order_Reference_Number']]=[information['Shares'],information['Price'],information['Timestamp'].Nanoseconds,information['Timestamp']]
            elif information['Original_Order_Reference_Number'] in self.order_book_bid.index:
                    #delete
                    self.order_book_bid.drop([information['Original_Order_Reference_Number']],inplace=True) 
                    #add
                    self.order_book_bid.loc[information['New_Order_Reference_Number']]=[information['Shares'],information['Price'],information['Timestamp'].Nanoseconds,information['Timestamp']]
            else:
                print('Order not found!!!',information['Message_Type'],information['Original_Order_Reference_Number'])
        
        def Trade_Message_Non_Cross_OB(information):
            #we can't use reference number so we need to mtch price
            #to enable the switcher
            if not information['Message_Type']=='P':
                return 0
            #buy/sale 
            if information['Price'] in set(self.order_book_ask['Price']):
                Order_Reference_Number=self.order_book_ask[self.order_book_ask['Price']==information['Price']].index[0]
                origin_shares=self.order_book_ask.loc[Order_Reference_Number,'Shares']
                new_shares=origin_shares-information['Shares']
                if new_shares: 
                #partly exercised               
                    self.order_book_ask.loc[Order_Reference_Number,'Shares']=new_shares
                    self.order_book_ask.loc[Order_Reference_Number,'Nanoseconds']=information['Timestamp'].Nanoseconds               
                    self.order_book_ask.loc[Order_Reference_Number,'Timestamp']=information['Timestamp']              
                else:
                #fully exercised 
                    self.order_book_ask.drop([Order_Reference_Number])
        
            elif information['Price'] in set(self.order_book_bid['Price']):
                Order_Reference_Number=self.order_book_bid[self.order_book_bid['Price']==information['Price']].index[0]
                origin_shares=self.order_book_bid.loc[Order_Reference_Number,'Shares']
                new_shares=origin_shares-information['Shares']
                if new_shares: 
                #partly exercised               
                    self.order_book_bid.loc[Order_Reference_Number,'Shares']=new_shares
                    self.order_book_bid.loc[Order_Reference_Number,'Nanoseconds']=information['Timestamp'].Nanoseconds               
                    self.order_book_bid.loc[Order_Reference_Number,'Timestamp']=information['Timestamp']              
                else:
                #fully exercised 
                    self.order_book_bid.drop([Order_Reference_Number])
                   
            else:
#                print('Order not found!!!',information['Message_Type'],information['Order_Reference_Number']) 
                print(information['Price'],information['Shares'])    
    
        information_to_order_book(information)