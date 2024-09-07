
import re
import pandas as pd
import MetaTrader5 as mt
#mt.initialize()
import time
def parsetext(TeleMSG):
    #prices=re.findall(r'[\d]+[.][\d]+', str(context.split('\n')))
    #price_patterns=re.compile(r'\d\d\d+.\d+|\d\d+.\d\d\d|\d.\d\d\d+|\d.\d\d+|\d\d.\d+|\d\d\d\d+')
    try: 
        TelMSG=TeleMSG.upper()
        stop_loss=re.compile("(SL|STOPLOSS|STOP\\s*LOSS|STOP|SUGERIDO|Stopp Loss auf|Stop Loss :round_pushpin::)\\s*(-|:|\\..)?\\s*(@|at|#|_)?\\s*([0-9,.]+)")
        sl_match=stop_loss.findall(TelMSG)
        if ',' in sl_match[-1][-1]:
            stop_loss=sl_match[-1][-1].replace(',','.')
        else:
            stop_loss=sl_match[-1][-1]
        try:   
            entry=re.compile("\\s*(BUY|SELL|NOW|RECOMENDED|OPEN|ENTRY|💎|Einstieg: Jetzt! \\()\\s*([a-z,#]*)?\\s*(LIMIT|STOP)?\\s*([a-z,#]*)?\\s*(PRICE|AGAIN|ENTRY|NOW|\\()?\\s*([a-z,#]*)?\\s*(@|at\\s*cmp|:|_)?\\s*([a-z,#]*)?\\s*([0-9,.]+)")
            entry_match=entry.findall(TelMSG)
            if ',' in entry_match[-1][-1]:
                entry=entry_match[-1][-1].replace(',','.')
            else:
                entry=entry_match[-1][-1]
        except:
            entry=0
        if 'SELL STOP' in TelMSG or 'SELLSTOP' in TelMSG:
            trade='SELL STOP'
        elif 'SELL LIMIT' in TelMSG or 'SELLLIMIT' in TelMSG:
            trade='SELL LIMIT'
        elif 'SELL' in TelMSG or 'SHORT' in TelMSG:
                trade='SELL MARKET'
        elif 'BUY STOP' in TelMSG or 'BUYSTOP' in TelMSG:
            trade='BUY STOP'
        elif 'BUY LIMIT' in TelMSG or 'BUYLIMIT' in TelMSG:
            trade='BUY LIMIT'
        elif 'BUY' in TelMSG or 'LONG' in TelMSG:
            trade='BUY MARKET'
        
        pairs=['EURUSD','USOIL','GBPUSD','EURGBP','USDCAD','NZDUSD','AUDUSD','AUDCAD','AUDCHF','AUDGBP','AUDNZD','NZDCAD',
                    'CADCHF','EURCAD','EURCHF','EURAUD','GBPAUD','GBPNZD','GBPCAD','USDCHF','GBPCHF','NZDCHF',
                    'EURNZD','US30','SPX','S&P500','AUS200','SPY','US500','DE30','FR40','HK50','STOXX50','USTEC',
                    'AUDJPY','GBPJPY','CADJPY','CHFJPY','EURJPY','NZDJPY','USDJPY','XAUUSD']
        if 'gold' in TelMSG:
            symbol='XAUUSD'
        elif '/' in TelMSG:
            TelMSG=TelMSG.replace('/','')
            pattern=re.compile('|'.join(pairs),re.IGNORECASE).search(TelMSG)
            symbol=pattern.group()
            #symbol=symbol.upper()
        else:
            pattern=re.compile('|'.join(pairs),re.IGNORECASE).search(TelMSG)
            symbol=pattern.group()
            #symbol=symbol.upper()
    
        price_patterns=re.compile("(TP\\s*[1-4]*|TARGET\\s*[1-4]*|TAKE\\s*PROFIT\\s*[1-4]*|TP\\s*bitte\\s*auf)\\s*(-|:|=|\\..)?\\s*(@|at|#)?\\s*([0-9,.]+)")
        match=price_patterns.findall(TelMSG)
        if len(match)==1:
            TP1=match[0][-1]
            return (symbol,trade,stop_loss,entry,TP1)
        elif len(match) ==2:
            TP1=match[0][-1]
            TP2=match[1][-1]
            return (symbol,trade,stop_loss,entry,TP1,TP2)
        elif len(match) == 3:
            TP1=match[0][-1]
            TP2=match[1][-1]
            TP3=match[2][-1]
            return (symbol,trade,stop_loss,entry,TP1,TP2,TP3)
        elif len(match) == 4:
            TP1=match[0][-1]
            TP2=match[1][-1]
            TP3=match[2][-1]
            TP4=match[3][-1]
            return (symbol,trade,stop_loss,entry,TP1,TP2,TP3,TP4)
        else:
            TP1=match[0][-1]
            TP2=match[1][-1]
            TP3=match[2][-1] 
            TP4=match[3][-1]
            TP5=match[4][-1]  
            return (symbol,trade,stop_loss,entry,TP1,TP2,TP3,TP4,TP5)
    except BaseException:
        return 0        
    

def tradeExecution(symbol,volume,trade,SL,TP,ENTRY):
    if trade=='BUY STOP':
        request={
        'action':mt.TRADE_ACTION_PENDING,
        'symbol':symbol,
        'volume':volume,
        'type':mt.ORDER_TYPE_BUY_STOP,#or mt.ORDER_TYPE_BUY, for buy
        'price':ENTRY,
        'sl':SL,#float
        'tp':TP,#float
        'deviation':20,#integer, slippage
        'magic':7629765,#integer, ticket no, or id
        'comment':'python script open',
        'type_time':mt.ORDER_TIME_GTC,#valid until you cancel it
        'type_filling':mt.ORDER_FILLING_RETURN,#the max size will be taken if the volume is big
        }
        order=mt.order_send(request)
        return order

    elif trade=='BUY LIMIT':
        request={
        'action':mt.TRADE_ACTION_PENDING,
        'symbol':symbol,
        'volume':volume,
        'type':mt.ORDER_TYPE_BUY_LIMIT,#or mt.ORDER_TYPE_BUY, for buy
        'price':ENTRY,
        'sl':SL,#float
        'tp':TP,#float
        'deviation':20,#integer, slippage
        'magic':55,#integer, ticket no, or id
        'comment':'python script open',
        'type_time':mt.ORDER_TIME_GTC,#valid until you cancel it
        'type_filling':mt.ORDER_FILLING_RETURN,#the max size will be taken if the volume is big
        }
        order=mt.order_send(request)
        return order 
    elif trade=='SELL STOP':
        request={
        'action':mt.TRADE_ACTION_PENDING,
        'symbol':symbol,
        'volume':volume,
        'type':mt.ORDER_TYPE_SELL_STOP,#or mt.ORDER_TYPE_BUY, for buy
        'price':ENTRY,
        'sl':SL,#float
        'tp':TP,#float
        'deviation':20,#integer, slippage
        'magic':7629765,#integer, ticket no, or id
        'comment':'python script open',
        'type_time':mt.ORDER_TIME_GTC,#valid until you cancel it
        'type_filling':mt.ORDER_FILLING_RETURN,#the max size will be taken if the volume is big
        }
        order=mt.order_send(request)
        return order
    elif trade=='SELL LIMIT':
        request={
        'action':mt.TRADE_ACTION_PENDING,
        'symbol':symbol,
        'volume':volume,
        'type':mt.ORDER_TYPE_SELL_LIMIT,#or mt.ORDER_TYPE_BUY, for buy
        'price':ENTRY,
        'sl':SL,#float
        'tp':TP,#float
        'deviation':20,#integer, slippage
        'magic':5,#integer, ticket no, or id
        'comment':'python script open',
        'type_time':mt.ORDER_TIME_GTC,#valid until you cancel it
        'type_filling':mt.ORDER_FILLING_RETURN,#the max size will be taken if the volume is big
        }
        order=mt.order_send(request)
        return order

def MarketExecution(symbol,volume,trade,SL,TP):
    if trade=='SELL MARKET':
        request={
        'action':mt.TRADE_ACTION_DEAL,
        'symbol':symbol,
        'volume':volume,
        'type':mt.ORDER_TYPE_SELL,#or mt.ORDER_TYPE_BUY, for buy
        'price':mt.symbol_info_tick(symbol).ask,
        'sl':SL,#float
        'tp':TP,#float
        'deviation':5,#integer, slippage
        'magic':5,#integer, ticket no, or id
        'comment':'python script open',
        'type_time':mt.ORDER_TIME_GTC,#valid until you cancel it
        'type_filling':mt.ORDER_FILLING_IOC,#the max size will be taken if the volume is big
        }
        order=mt.order_send(request)
        return order
    elif trade=='BUY MARKET':
        request={
        'action':mt.TRADE_ACTION_DEAL,
        'symbol':symbol,
        'volume':volume,
        'type':mt.ORDER_TYPE_BUY,#or mt.ORDER_TYPE_BUY, for buy
        'price':mt.symbol_info_tick(symbol).bid,
        'sl':SL,#float
        'tp':TP,#float
        'deviation':20,#integer, slippage
        'magic':7629765,#integer, ticket no, or id
        'comment':'python script open',
        'type_time':mt.ORDER_TIME_GTC,#valid until you cancel it
        'type_filling':mt.ORDER_FILLING_IOC,#the max size will be taken if the volume is big
        }
        order=mt.order_send(request)
        return order


def parserepltext(repltext):
    rtext=repltext.lower()
    #prices=re.findall(r'[\d]+[.][\d]+', str(rtext.split('\n')))
    price_patterns=re.compile(r'\d\d\d+.\d+|\d\d+.\d\d\d|\d.\d\d\d+|\d\d.\d+|\d\d\d\d+')
    prices=price_patterns.findall(rtext)
    if prices:
        prices=prices
    else:
        prices=[0]
    closes=['close','take']
    pattern1=re.compile('|'.join(closes),re.IGNORECASE).search(rtext)
    if pattern1:
        if 'partial' in rtext:
            trade='close partial'
        elif 'half' in rtext:
            trade='close partial'
        else:
            trade='close fully'
            
    updates=['adjust','move','update']
    pattern2=re.compile('|'.join(updates),re.IGNORECASE).search(rtext)
    if pattern2:
        if 'sl' in rtext and 'tp' in rtext or 'stop' in rtext and 'target' in rtext:
            trade='adjust sltp'
        elif 'sl' in rtext or 'stop' in rtext:
            trade='adjust sl'
        elif 'tp' in rtext or 'target' in rtext:
            trade='adjust tp'
    cancels=['cancel','remove','delete']
    pattern2=re.compile('|'.join(cancels),re.IGNORECASE).search(rtext)
    if pattern2:
        trade='cancel'
    return (trade,prices)

def removeOrder(PositionID):
    request={
        'action':mt.TRADE_ACTION_REMOVE,
        'order':PositionID,#you give the order id here
        }
    order=mt.order_send(request)
    return order

def AdjustSLTP(PositionID,SL,TP):
    request={
        'action':mt.TRADE_ACTION_SLTP,
        'position':PositionID,
        'sl':SL,#float
        'tp':TP,#float
    
        }
    order=mt.order_send(request)
    return order

def closeFully(PositionID):
    tposition=mt.positions_get(ticket=PositionID)[0]
    request={
        'action':mt.TRADE_ACTION_DEAL,
        'symbol':tposition.symbol,
        'volume':tposition.volume,
        'type':mt.ORDER_TYPE_BUY if tposition.type==1 else mt.ORDER_TYPE_SELL,
        'position':tposition.ticket,
        'price':mt.symbol_info_tick(tposition.symbol).ask if tposition.type==0 else mt.symbol_info_tick(tposition.symbol).bid,
        'sl':0.0,#float
        'tp':0.0,#float
        'deviation':10,#integer, slippage
        'magic':7629765,#integer, ticket no, or id
        'comment':'python script open',
        'type_time':mt.ORDER_TIME_GTC,
        'type_filling':mt.ORDER_FILLING_IOC,
        
        }

    order=mt.order_send(request)
    return order

def closePartials(PositionID):
    tposition=mt.positions_get(ticket=PositionID)[0]
    if tposition.volume>0.01:
        volume=round(tposition.volume/2,ndigits=2)
    else:
        volume=tposition.volume
    request={
        'action':mt.TRADE_ACTION_DEAL,
        'symbol':tposition.symbol,
        'volume':volume,
        'type':mt.ORDER_TYPE_BUY if tposition.type==1 else mt.ORDER_TYPE_SELL,
        'position':tposition.ticket,
        'price':mt.symbol_info_tick(tposition.symbol).ask if tposition.type==0 else mt.symbol_info_tick(tposition.symbol).bid,
        'sl':0.0,#float
        'tp':0.0,#float
        'deviation':20,#integer, slippage
        'magic':7629765,#integer, ticket no, or id
        'comment':'python script open',
        'type_time':mt.ORDER_TIME_GTC,
        'type_filling':mt.ORDER_FILLING_IOC,
        }
    order=mt.order_send(request)
    return order


def breakeven_pos(pos_ticket):
    tposition=mt.positions_get(ticket=pos_ticket)[0]
    print(tposition)
    open_price=tposition.price_open
    curr_price=tposition.price_current
    
    request={
        'action':mt.TRADE_ACTION_SLTP,
        'position':pos_ticket,
        'sl':open_price,#float
        'tp':tposition.tp,#float
       
        }
    
    order=mt.order_send(request)

def close_custom(PositionID,percent):
    tposition=mt.positions_get(ticket=PositionID)[0]
    percent=float(percent)
    volume = percent
    request={
        'action':mt.TRADE_ACTION_DEAL,
        'symbol':tposition.symbol,
        'volume':volume,
        'type':mt.ORDER_TYPE_BUY if tposition.type==1 else mt.ORDER_TYPE_SELL,
        'position':tposition.ticket,
        'price':mt.symbol_info_tick(tposition.symbol).ask if tposition.type==0 else mt.symbol_info_tick(tposition.symbol).bid,
        'sl':0.0,#float
        'tp':0.0,#float
        'deviation':20,#integer, slippage
        'magic':7629765,#integer, ticket no, or id
        'comment':'python script open',
        'type_time':mt.ORDER_TIME_GTC,
        'type_filling':mt.ORDER_FILLING_IOC,
        }
    order=mt.order_send(request)
    return order

def close_one_lot(PositionID):
    tposition=mt.positions_get(ticket=PositionID)[0]
    if tposition.volume>0.01:
        volume = float(1)
    else:
        volume=tposition.volume
    request={
        'action':mt.TRADE_ACTION_DEAL,
        'symbol':tposition.symbol,
        'volume':volume,
        'type':mt.ORDER_TYPE_BUY if tposition.type==1 else mt.ORDER_TYPE_SELL,
        'position':tposition.ticket,
        'price':mt.symbol_info_tick(tposition.symbol).ask if tposition.type==0 else mt.symbol_info_tick(tposition.symbol).bid,
        'sl':0.0,#float
        'tp':0.0,#float
        'deviation':20,#integer, slippage
        'magic':7629765,#integer, ticket no, or id
        'comment':'python script open',
        'type_time':mt.ORDER_TIME_GTC,
        'type_filling':mt.ORDER_FILLING_IOC,
        }
    order=mt.order_send(request)
    return order
def close_point_fifty_lot(PositionID):
    tposition=mt.positions_get(ticket=PositionID)[0]
    if tposition.volume>0.01:
        volume = 0.5
    else:
        volume=tposition.volume
    request={
        'action':mt.TRADE_ACTION_DEAL,
        'symbol':tposition.symbol,
        'volume':volume,
        'type':mt.ORDER_TYPE_BUY if tposition.type==1 else mt.ORDER_TYPE_SELL,
        'position':tposition.ticket,
        'price':mt.symbol_info_tick(tposition.symbol).ask if tposition.type==0 else mt.symbol_info_tick(tposition.symbol).bid,
        'sl':0.0,#float
        'tp':0.0,#float
        'deviation':20,#integer, slippage
        'magic':7629765,#integer, ticket no, or id
        'comment':'python script open',
        'type_time':mt.ORDER_TIME_GTC,
        'type_filling':mt.ORDER_FILLING_IOC,
        }
    order=mt.order_send(request)
    return order
def close_point_ten_lot(PositionID):
    tposition=mt.positions_get(ticket=PositionID)[0]
    if tposition.volume>0.01:
        volume = 0.1
    else:
        volume=tposition.volume
    request={
        'action':mt.TRADE_ACTION_DEAL,
        'symbol':tposition.symbol,
        'volume':volume,
        'type':mt.ORDER_TYPE_BUY if tposition.type==1 else mt.ORDER_TYPE_SELL,
        'position':tposition.ticket,
        'price':mt.symbol_info_tick(tposition.symbol).ask if tposition.type==0 else mt.symbol_info_tick(tposition.symbol).bid,
        'sl':0.0,#float
        'tp':0.0,#float
        'deviation':20,#integer, slippage
        'magic':7629765,#integer, ticket no, or id
        'comment':'python script open',
        'type_time':mt.ORDER_TIME_GTC,
        'type_filling':mt.ORDER_FILLING_IOC,
        }
    order=mt.order_send(request)
    return order
def close_point_five_lot(PositionID):
    tposition=mt.positions_get(ticket=PositionID)[0]
    if tposition.volume>0.01:
        volume = 0.05
    else:
        volume=tposition.volume
    request={
        'action':mt.TRADE_ACTION_DEAL,
        'symbol':tposition.symbol,
        'volume':volume,
        'type':mt.ORDER_TYPE_BUY if tposition.type==1 else mt.ORDER_TYPE_SELL,
        'position':tposition.ticket,
        'price':mt.symbol_info_tick(tposition.symbol).ask if tposition.type==0 else mt.symbol_info_tick(tposition.symbol).bid,
        'sl':0.0,#float
        'tp':0.0,#float
        'deviation':20,#integer, slippage
        'magic':7629765,#integer, ticket no, or id
        'comment':'python script open',
        'type_time':mt.ORDER_TIME_GTC,
        'type_filling':mt.ORDER_FILLING_IOC,
        }
    order=mt.order_send(request)
    return order
def close_point_one_lot(PositionID):
    tposition=mt.positions_get(ticket=PositionID)[0]
    if tposition.volume>0.01:
        volume = 0.01
    else:
        volume=tposition.volume
    request={
        'action':mt.TRADE_ACTION_DEAL,
        'symbol':tposition.symbol,
        'volume':volume,
        'type':mt.ORDER_TYPE_BUY if tposition.type==1 else mt.ORDER_TYPE_SELL,
        'position':tposition.ticket,
        'price':mt.symbol_info_tick(tposition.symbol).ask if tposition.type==0 else mt.symbol_info_tick(tposition.symbol).bid,
        'sl':0.0,#float
        'tp':0.0,#float
        'deviation':20,#integer, slippage
        'magic':7629765,#integer, ticket no, or id
        'comment':'python script open',
        'type_time':mt.ORDER_TIME_GTC,
        'type_filling':mt.ORDER_FILLING_IOC,
        }
    order=mt.order_send(request)
    return order

def update(ticket,new_sl,new_tp):
     request = {
                'action': mt.TRADE_ACTION_SLTP,
                'position': ticket,
                'sl': float(new_sl),
                'tp':float(new_tp),
                    }
    
     result = mt.order_send(request)
     return result

def TrailFunc(fx_default,fx_trail,fx_max_dist,ind_default,ind_trail,ind_max_dist):
    MAX_DIST_SL = fx_max_dist  # Max distance between current price and SL, otherwise SL will update
    TRAIL_AMOUNT =fx_trail  # Amount by how much SL updates
    DEFAULT_SL = fx_default  # If position has no SL, set a default SL
    INDEX_DEFAULT_SL= ind_default
    INDEX_TRAIL_AMOUNT= ind_trail
    INDEX_MAX_DIST_SL= ind_max_dist


    indices=['US30','SPX','S&P500','AUS200','SPY','US500','DE30','FR40','HK50','STOXX50','USTEC']
    five_digit_pairs=['EURUSD','GBPUSD','EURGBP','USDCAD','NZDUSD','AUDUSD','AUDCAD','AUDCHF','AUDGBP','AUDNZD','NZDCAD',
                  'CADCHF','EURCAD','EURCHF','EURAUD','GBPAUD','GBPNZD','GBPCAD','USDCHF','GBPCHF','NZDCHF',
                  'EURNZD']
    three_digit_pairs=['AUDJPY','GBPJPY','CADJPY','CHFJPY','EURJPY','NZDJPY','USDJPY']
    while True:
        tposition=mt.positions_get()
        for position in tposition:
            open_price=position.price_open
            curr_price=position.price_current
            ticket=position.ticket
            if position.type==0:        
                OPEN_CUR_PRICE_DIST=curr_price-open_price
                SL_CUR_PRICE_DIST=curr_price-position.sl
            else:
                OPEN_CUR_PRICE_DIST=open_price-curr_price
                SL_CUR_PRICE_DIST=position.sl-curr_price
    
            if position.symbol in indices:
                #giving default sl to indices
                if position.sl==0.0:
                    if position.type==0:
                        new_sl=open_price-INDEX_DEFAULT_SL
                        new_tp=position.tp
                        update(ticket,new_sl, new_tp)
                    else:
                        new_sl=open_price+INDEX_DEFAULT_SL
                        new_tp=position.tp
                        update(ticket,new_sl, new_tp)
                else:
                    #trail stop loss
                    if OPEN_CUR_PRICE_DIST>INDEX_DEFAULT_SL and SL_CUR_PRICE_DIST>INDEX_MAX_DIST_SL:
                        if SL_CUR_PRICE_DIST>INDEX_DEFAULT_SL:
                            if position.type==0:
                                new_sl=position.sl+INDEX_TRAIL_AMOUNT
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                            else:
                                new_sl=position.sl-INDEX_TRAIL_AMOUNT
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                           
                        else:
                            if position.type==0:
                                new_sl=open_price+1
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                            else:
                                new_sl=open_price-1
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                    
            elif position.symbol=='XAUUSD':
                #giving default sl to indices
                if position.sl==0.0:
                    if position.type==0:
                        new_sl=open_price-abs(round(DEFAULT_SL/5))
                        new_tp=position.tp
                        update(ticket,new_sl, new_tp)
                    else:
                        new_sl=open_price+abs(round(DEFAULT_SL/5))
                        new_tp=position.tp
                        update(ticket,new_sl, new_tp)
                else:
                     if OPEN_CUR_PRICE_DIST>abs(round(DEFAULT_SL/5)) and SL_CUR_PRICE_DIST>abs(round(MAX_DIST_SL/5)):
                        if SL_CUR_PRICE_DIST>abs(round(DEFAULT_SL/5)):
                            if position.type==0:
                                new_sl=position.sl+abs(round(TRAIL_AMOUNT/5))
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                            else:
                               new_sl=position.sl-abs(round(TRAIL_AMOUNT/5))
                               new_tp=position.tp
                               update(ticket,new_sl, new_tp)
                            
                        else:
                            if position.type==0:
                                new_sl=open_price+0.2
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                            else:
                                new_sl=open_price-0.2
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
               
            elif position.symbol in five_digit_pairs:
                if position.sl==0.0:
                          multiplier=0.0001
                          if position.type==0:
                              new_sl=open_price-(DEFAULT_SL*multiplier)
                              new_tp=position.tp
                              update(ticket,new_sl, new_tp)
                          else:
                                new_sl=open_price+(DEFAULT_SL*multiplier)
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                else:
                    multiplier=0.0001
                    if OPEN_CUR_PRICE_DIST>(DEFAULT_SL*multiplier) and SL_CUR_PRICE_DIST>(MAX_DIST_SL*multiplier):
                        if SL_CUR_PRICE_DIST>(DEFAULT_SL*multiplier):    
                            if position.type==0:
                               new_sl=position.sl+(TRAIL_AMOUNT*multiplier)
                               new_tp=position.tp
                               update(ticket,new_sl, new_tp)
                            else:
                               new_sl=position.sl-(TRAIL_AMOUNT*multiplier)
                               new_tp=position.tp
                               update(ticket,new_sl, new_tp)
                        else:
                            if position.type==0:
                                new_sl=open_price+0.00007
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                            else:
                                new_sl=open_price-0.00007
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
            elif position.symbol in three_digit_pairs:
                multiplier=0.01
                if position.sl==0.0:
                    if position.type==0:
                        new_sl=open_price-(DEFAULT_SL*multiplier)
                        new_tp=position.tp
                        update(ticket,new_sl, new_tp)
                    else:
                        new_sl=open_price+(DEFAULT_SL*multiplier)
                        new_tp=position.tp
                        update(ticket,new_sl, new_tp)
                       
                else:
                    multiplier=0.01
                    if OPEN_CUR_PRICE_DIST>(DEFAULT_SL*multiplier) and SL_CUR_PRICE_DIST>(MAX_DIST_SL*multiplier):
                        if SL_CUR_PRICE_DIST>(DEFAULT_SL*multiplier):    
                            if position.type==0:
                               new_sl=position.sl+(TRAIL_AMOUNT*multiplier)
                               new_tp=position.tp
                               update(ticket,new_sl, new_tp)
                            else:
                               new_sl=position.sl-(TRAIL_AMOUNT*multiplier)
                               new_tp=position.tp
                               update(ticket,new_sl, new_tp)
                        else:
                            if position.type==0:
                                new_sl=open_price+0.007
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                            else:
                                new_sl=open_price-0.007
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                        
                        
        time.sleep(1.5)