# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 20:27:57 2019

@author: 43739
"""

import math

def Message_to_Information(data):
    switcher = { 
        'S': System_Event_Message_IN(data), 
        'R': Stock_Related_Messages_IN(data),         
        'H': Stock_Trading_Action_IN(data),         
        'Y': Reg_SHO_Restriction_IN(data), 
        'L': Market_Participant_Position_IN(data),           
        'V': MWCB_Decline_Level_Message_IN(data),         
        'W': MWCB_Status_Message_IN(data),         
        'K': IPO_Quoting_Period_Update_IN(data),         
        'J': LULD_Auction_Collar_IN(data),         
        'h': Operational_Halt_IN(data),         
        'A': Add_Order_Message_IN(data),         
        'F': Add_Order_MPID_Attribution_Message_IN(data),  
        'E': Order_Executed_Message_IN(data), 
        'C': Order_Executed_With_Price_Message_IN(data),         
        'X': Order_Cancel_Message_IN(data),         
        'D': Order_Delete_Message_IN(data), 
        'U': Order_Replace_Message_IN(data),           
        'P': Trade_Message_Non_Cross_IN(data),         
        'Q': Trade_Message_Cross_IN(data),         
        'B': Broken_Trade_Message_IN(data),         
        'I': NOII_Message_IN(data),         
        'N': Retail_Interest_Message_IN(data),         
    } 
    return switcher.get(chr(data[0]), None) 

class NanoTime():
    # initialize the class
    def __init__(self):
        self.Hours = 0
        self.Minutes = 0
        self.Seconds = 0
        self.Nanoseconds=0
    # read data
    def initialize(self, Nanoseconds):
        self.Nanoseconds = Nanoseconds
        self.Hours = math.floor(self.Nanoseconds/(1e9*3600)) 
        self.Minutes = math.floor((self.Nanoseconds-self.Hours*(1e9*3600))/(1e9*60))
        self.Seconds = math.floor((self.Nanoseconds-self.Hours*(1e9*3600)-self.Minutes*(1e9*60))/1e9)

def multi_chr(data):
    return ''.join([chr(x) for x in data])
   
def System_Event_Message_IN(data):
    #to enable the switcher
    if not chr(data[0])=='S':
        return 0
    #decode event code
    Code_to_Event = { 
        'O': 'Start of Messages', 
        'S': 'Start of System hours',         
        'Q': 'Start of Market hours',         
        'M': 'End of Market hours', 
        'E': 'End of System hours',           
        'C': 'End of Messages',                         
    } 
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))
    Event=Code_to_Event.get(chr(data[11]),'nothing')
    #return
    return {'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,
     'Tracking_Number':Tracking_Number,'Timestamp':Timestamp,'Event':Event}


def Stock_Related_Messages_IN(data):
    #to enable the switcher
    if not chr(data[0])=='R':
        return 0
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))
    Stock=multi_chr(data[11:19])
    Market_Category=chr(data[19])
    Financial_Status_Indicator=chr(data[20])
    Round_Lot_Size=int.from_bytes(data[21:25],'big')
    Round_Lots_Only=chr(data[25])
    Issue_Classification=chr(data[26])   
    Issue_Sub_Type=multi_chr(data[27:29])
    Authenticity=chr(data[29])
    Short_Sale_Threshold_Indicator=chr(data[30])
    IPO_Flag=chr(data[31])
    LULD_Reference_Price_Tier=chr(data[32])
    ETP_Flag=chr(data[33])
    ETP_Leverage_Factor=int.from_bytes(data[34:38],'big')
    Inverse_Indicator=chr(data[38])
    #return
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,'Tracking_Number':Tracking_Number,'Timestamp':Timestamp,
           'Stock':Stock,'Market_Category':Market_Category,'Financial_Status_Indicator':Financial_Status_Indicator,
           'Round_Lot_Size':Round_Lot_Size,'Round_Lots_Only':Round_Lots_Only,'Issue_Classification':Issue_Classification,
           'Issue_Sub_Type':Issue_Sub_Type,'Authenticity':Authenticity,'Short_Sale_Threshold_Indicator':Short_Sale_Threshold_Indicator,
           'IPO_Flag':IPO_Flag,'LULD_Reference_Price_Tier':LULD_Reference_Price_Tier,'ETP_Flag':ETP_Flag,
           'ETP_Leverage_Factor':ETP_Leverage_Factor,'Inverse_Indicator':Inverse_Indicator}
    
def Stock_Trading_Action_IN(data):
    #to enable the switcher
    if not chr(data[0])=='H':
        return 0    
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))
    Stock=multi_chr(data[11:19])    
    Trading_State=chr(data[19])
    Reserved=chr(data[20])
    Reason=multi_chr(data[21:25])
    #return
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,'Tracking_Number':Tracking_Number,
       'Timestamp':Timestamp,'Stock':Stock,'Trading_State':Trading_State,'Reserved':Reserved,'Reason':Reason}

def Reg_SHO_Restriction_IN(data):
    #to enable the switcher
    if not chr(data[0])=='Y':
        return 0    
    #information
    Message_Type=chr(data[0])
    Locate_Code=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))
    Stock=multi_chr(data[11:19])  
    Reg_SHO_Action=chr(data[19])
    #return
    return{'Message_Type':Message_Type,'Locate_Code':Locate_Code,'Tracking_Number':Tracking_Number,
           'Timestamp':Timestamp,'Stock':Stock,'Reg_SHO_Action':Reg_SHO_Action}

def Market_Participant_Position_IN(data):
    #to enable the switcher
    if not chr(data[0])=='L':
        return 0    
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))   
    MPID=multi_chr(data[11:15])
    Stock=multi_chr(data[15:23]) 
    Primary_Market_Maker=chr(data[23])
    Market_Maker_Mode=chr(data[24])
    Market_Participant_State=chr(data[25])
    #return
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,'Tracking_Number':Tracking_Number,
           'Timestamp':Timestamp,'MPID':MPID,'Stock':Stock,'Primary_Market_Maker':Primary_Market_Maker,
           'Market_Maker_Mode':Market_Maker_Mode,'Market_Participant_State':Market_Participant_State}

def MWCB_Decline_Level_Message_IN(data):   
    #to enable the switcher
    if not chr(data[0])=='V':
        return 0         
    #information  
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big')) 
    Level1=int.from_bytes(data[11:19],'big')/1e8
    Level2=int.from_bytes(data[19:27],'big')/1e8
    Level3=int.from_bytes(data[27:35],'big')/1e8
    #return
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,'Tracking_Number':Tracking_Number,
           'Timestamp':Timestamp,'Level1':Level1,'Level2':Level2,'Level3':Level3}

def MWCB_Status_Message_IN(data):
    #to enable the switcher
    if not chr(data[0])=='W':
        return 0    
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))
    Breached_Level=chr(data[11])
    #return
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,'Tracking_Number':Tracking_Number,
           'Timestamp':Timestamp,'Breached_Level':Breached_Level}

def IPO_Quoting_Period_Update_IN(data):
    #to enable the switcher
    if not chr(data[0])=='K':
        return 0       
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))
    Stock=multi_chr(data[11:19])
    IPO_Quotation_Release_Time=int.from_bytes(data[19:23],'big')
    IPO_Quotation_Release_Qualifier=chr(data[23])
    IPO_Price=int.from_bytes(data[24:28],'big')/1e4
    #return
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,
           'Tracking_Number':Tracking_Number,'Timestamp':Timestamp,'Stock':Stock,
           'IPO_Quotation_Release_Time':IPO_Quotation_Release_Time,
           'IPO_Quotation_Release_Qualifier':IPO_Quotation_Release_Qualifier,
           'IPO_Price':IPO_Price}

def LULD_Auction_Collar_IN(data):
    #to enable the switcher
    if not chr(data[0])=='J':
        return 0            
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))
    Stock=multi_chr(data[11:19])
    Auction_Collar_Reference_Price=int.from_bytes(data[19:23],'big')/1e4
    Upper_Auction_Collar_Price=int.from_bytes(data[23:27],'big')/1e4
    Lower_Auction_Collar_Price=int.from_bytes(data[27:31],'big')/1e4 
    Auction_Collar_Extension=int.from_bytes(data[31:35],'big')
    #return
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,'Tracking_Number':Tracking_Number,
           'Timestamp':Timestamp,'Stock':Stock,'Auction_Collar_Reference_Price':Auction_Collar_Reference_Price,
           'Upper_Auction_Collar_Price':Upper_Auction_Collar_Price,'Lower_Auction_Collar_Price':Lower_Auction_Collar_Price,
           'Auction_Collar_Extension':Auction_Collar_Extension}
    
def Operational_Halt_IN(data):
    #to enable the switcher
    if not chr(data[0])=='h':
        return 0            
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))
    Stock=multi_chr(data[11:19])
    Market_Code=chr(data[19])
    Operational_Halt_Action=chr(data[20])
    #return
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,'Tracking_Number':Tracking_Number,
           'Timestamp':Timestamp,'Stock':Stock,'Market_Code':Market_Code,
           'Operational_Halt_Action':Operational_Halt_Action} 
      
def Add_Order_Message_IN(data):
    #to enable the switcher
    if not chr(data[0])=='A':
        return 0            
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))
    Order_Reference_Number=int.from_bytes(data[11:19],'big')
    Buy_Sell_Indicator=chr(data[19])
    Shares=int.from_bytes(data[20:24],'big')
    Stock=multi_chr(data[24:32])
    Price=int.from_bytes(data[32:36],'big')/1e4
    #return 
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,'Tracking_Number':Tracking_Number,
           'Timestamp':Timestamp,'Order_Reference_Number':Order_Reference_Number,
           'Buy_Sell_Indicator':Buy_Sell_Indicator,'Shares':Shares,'Stock':Stock,'Price':Price}
    
def Add_Order_MPID_Attribution_Message_IN(data):
    #to enable the switcher
    if not chr(data[0])=='F':
        return 0                
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))
    Order_Reference_Number=int.from_bytes(data[11:19],'big')
    Buy_Sell_Indicator=chr(data[19])
    Shares=int.from_bytes(data[20:24],'big')
    Stock=multi_chr(data[24:32])
    Price=int.from_bytes(data[32:36],'big')/1e4
    Attribution=multi_chr(data[36:40])
    #return 
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,'Tracking_Number':Tracking_Number,
           'Timestamp':Timestamp,'Order_Reference_Number':Order_Reference_Number,
           'Buy_Sell_Indicator':Buy_Sell_Indicator,'Shares':Shares,'Stock':Stock,
           'Price':Price,'Attribution':Attribution}
    
def Order_Executed_Message_IN(data): 
    #to enable the switcher
    if not chr(data[0])=='E':
        return 0                
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))
    Order_Reference_Number=int.from_bytes(data[11:19],'big')
    Executed_Shares=int.from_bytes(data[19:23],'big')
    Match_Number=int.from_bytes(data[23:31],'big')
    #return 
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,
           'Tracking_Number':Tracking_Number,'Timestamp':Timestamp,
           'Order_Reference_Number':Order_Reference_Number,
           'Executed_Shares':Executed_Shares,'Match_Number':Match_Number}

def Order_Executed_With_Price_Message_IN(data):
    #to enable the switcher
    if not chr(data[0])=='C':
        return 0    
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))
    Order_Reference_Number=int.from_bytes(data[11:19],'big')
    Executed_Shares=int.from_bytes(data[19:23],'big')
    Match_Number=int.from_bytes(data[23:31],'big')
    Printable=chr(data[31])
    Execution_Price=int.from_bytes(data[32:36],'big')/1e4
    #return 
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,'Tracking_Number':Tracking_Number,
           'Timestamp':Timestamp,'Order_Reference_Number':Order_Reference_Number,
           'Executed_Shares':Executed_Shares,'Match_Number':Match_Number,'Printable':Printable,
           'Execution_Price':Execution_Price}

def Order_Cancel_Message_IN(data):
    #to enable the switcher
    if not chr(data[0])=='X':
        return 0    
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))
    Order_Reference_Number=int.from_bytes(data[11:19],'big')
    Cancelled_Shares=int.from_bytes(data[19:23],'big')
    #return 
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,'Tracking_Number':Tracking_Number,'Timestamp':Timestamp,
           'Order_Reference_Number':Order_Reference_Number,'Cancelled_Shares':Cancelled_Shares}

def Order_Delete_Message_IN(data):
    #to enable the switcher
    if not chr(data[0])=='D':
        return 0    
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))
    Order_Reference_Number=int.from_bytes(data[11:19],'big')
    #return 
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,'Tracking_Number':Tracking_Number,
           'Timestamp':Timestamp,'Order_Reference_Number':Order_Reference_Number}

def Order_Replace_Message_IN(data):
    #to enable the switcher
    if not chr(data[0])=='U':
        return 0
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))
    Original_Order_Reference_Number=int.from_bytes(data[11:19],'big')
    New_Order_Reference_Number=int.from_bytes(data[19:27],'big')
    Shares=int.from_bytes(data[27:31],'big')
    Price=int.from_bytes(data[31:35],'big')/1e4
    #return 
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,
           'Tracking_Number':Tracking_Number,'Timestamp':Timestamp,
           'Original_Order_Reference_Number':Original_Order_Reference_Number,
           'New_Order_Reference_Number':New_Order_Reference_Number,'Shares':Shares,'Price':Price}

def Trade_Message_Non_Cross_IN(data):
    #to enable the switcher
    if not chr(data[0])=='P':
        return 0    
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))
    Order_Reference_Number=int.from_bytes(data[11:19],'big')
    Buy_Sell_Indicator=chr(data[19])
    Shares=int.from_bytes(data[20:24],'big')
    Stock=multi_chr(data[24:32])
    Price=int.from_bytes(data[32:36],'big')/1e4 
    Match_Number=int.from_bytes(data[36:44],'big')   
    #return 
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,
           'Tracking_Number':Tracking_Number,'Timestamp':Timestamp,
           'Order_Reference_Number':Order_Reference_Number,
           'Buy_Sell_Indicator':Buy_Sell_Indicator,'Shares':Shares,
           'Stock':Stock,'Price':Price,'Match_Number':Match_Number}

def Trade_Message_Cross_IN(data): 
    #to enable the switcher
    if not chr(data[0])=='Q':
        return 0
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))
    Shares=int.from_bytes(data[11:19],'big')
    Stock=multi_chr(data[19:27])
    Cross_Price=int.from_bytes(data[27:31],'big')/1e4 
    Match_Number=int.from_bytes(data[31:39],'big')       
    Cross_Type=chr(data[39])
    #return
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,
           'Tracking_Number':Tracking_Number,'Timestamp':Timestamp,'Shares':Shares,'Stock':Stock,
           'Cross_Price':Cross_Price,'Match_Number':Match_Number,'Cross_Type':Cross_Type}
    
def Broken_Trade_Message_IN(data):
    #to enable the switcher
    if not chr(data[0])=='B':
        return 0
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big'))
    Match_Number=int.from_bytes(data[11:19],'big') 
    #return
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,'Tracking_Number':Tracking_Number,
           'Timestamp':Timestamp,'Match_Number':Match_Number}

def NOII_Message_IN(data): 
    #to enable the switcher
    if not chr(data[0])=='I':
        return 0
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big')) 
    Paired_Shares=int.from_bytes(data[11:19],'big')
    Imbalance_Shares=int.from_bytes(data[19:27],'big')
    Imbalance_Direction=chr(data[27])
    Stock=multi_chr(data[28:36])
    Far_Price=int.from_bytes(data[36:40],'big')/1e4 
    Near_Price=int.from_bytes(data[40:44],'big')/1e4
    Current_Reference_Price=int.from_bytes(data[44:48],'big')/1e4
    Cross_Type=chr(data[48]) 
    Price_Variation_Indicator=chr(data[49])
    #return    
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,'Tracking_Number':Tracking_Number,
           'Timestamp':Timestamp,'Paired_Shares':Paired_Shares,'Imbalance_Shares':Imbalance_Shares,
           'Imbalance_Direction':Imbalance_Direction,'Stock':Stock,'Far_Price':Far_Price,
           'Near_Price':Near_Price,'Current_Reference_Price':Current_Reference_Price,
           'Cross_Type':Cross_Type,'Price_Variation_Indicator':Price_Variation_Indicator}
    
def Retail_Interest_Message_IN(data): 
    #to enable the switcher
    if not chr(data[0])=='N':
        return 0     
    #information
    Message_Type=chr(data[0])
    Stock_Locate=int.from_bytes(data[1:3],'big')
    Tracking_Number=int.from_bytes(data[3:5],'big')
    Timestamp=NanoTime()
    Timestamp.initialize(int.from_bytes(data[5:11],'big')) 
    Stock=multi_chr(data[11:19])
    Interest_Flag=chr(data[19]) 
    #return
    return{'Message_Type':Message_Type,'Stock_Locate':Stock_Locate,'Tracking_Number':Tracking_Number,
           'Timestamp':Timestamp,'Stock':Stock,'Interest_Flag':Interest_Flag}
 
if __name__ == '__main__':
    import os  
    os.chdir('D:\\Nasdaq')
    file=open('10302019.NASDAQ_ITCH50','rb')    
    size=int.from_bytes(file.read(2),'big')
    data=file.read(size)
#    print(chr(data[0]))
    Message_to_Information(data)   
#    list to dict    
#    list1=['Message_Type','Stock_Locate','Tracking_Number','Timestamp','Stock','Trading_State','Reserved','Reason']
#    temp=["'"+x+"':"+x+',' for x in list1]
#    print('return{'+''.join(temp)+'}')
    