
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
import csv
#from functools import reduce
import numpy as np
import sys
from threading import Thread
import MetaTrader5 as mt5
from PyQt5.uic import loadUi
import asyncio
from PyQt5.QtWidgets import QDialog, QApplication, QWidget,QMainWindow
from sklearn import exceptions
from telethon import TelegramClient, events, sync, client, utils
import phonenumbers
from PyQt5.QtCore import QThread, QObject, pyqtSignal
import sqlite3
from functions import *
import datetime as dt
import config
api_id = config.api_id
api_hash = config.api_hash

client = TelegramClient('gui/session', api_id, api_hash)    
client.connect()
conn=sqlite3.connect('gui/employee.db')
c=conn.cursor()
#create table
def users_table():
    c.execute('''
            CREATE TABLE users(
              Server   text,
              LoginID text,
              Password  text,
              Suffix   text,
              Symbol text
                )
            ''')
def defaults_table():
    c.execute('''
            CREATE TABLE defaults(
              fxvolume   integer,
              fxslippage integer,
              fxsl  integer,
              indexvolume   integer,
              indexslippage integer,
              indexsl integer,
              comvolume integer,
              comslippage integer,
              comsl integer
                )
            ''')
    c.execute("INSERT INTO defaults VALUES(:fxvol,:fxslip,:fxsl,:indexvol,:indexslip,:indexsl,:comvol,:comslip,:comsl)",
            {'fxvol':0.01,'fxslip':0.01,'fxsl':0.01,'indexvol':0.01,'indexslip':0.01,'indexsl':0.01 ,'comvol':0.01 ,'comslip': 0.01,'comsl':0.01 })
    conn.commit()
def symbol_volume():
    c.execute('''
            CREATE TABLE symbol_volume(
              symbol   text,
              volume integer
                )
            ''')
def symbols_table():
    c.execute('''
            CREATE TABLE exclude_symbol(
              symbol   text
                )
            ''')

def Trailer_table():
    print('its trailer')
    c.execute('''
            CREATE TABLE trailer(
              fxdef   integer,
              fxtrail integer,
              fxdistance  integer,
              fxcus   integer,
              inddef   integer,
              indtrail integer,
              inddistance  integer,
              indcus   integer,
              comdef   integer,
              comtrail integer,
              comdistance  integer,
              comcus   integer
                )
            ''')
    print('trailer created')


try:
    Trailer_table()
    users_table()
    defaults_table()
    
except:
    pass

with open("gui/telmsg.csv","a",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    # First write the headers
    writer.writerow(['FirstMSG','FirstmsgID','Firstmsgchat_title','chat_id','repltext','replid'])
liast=[]
liast.append([0,1,2,3,4])
executed_trades=pd.DataFrame(liast)
executed_trades.columns=['AccountID','MessageID','PositionID','SL','TP']
class trail_sl(QObject):
    def __init__(self):
        super().__init__()
    def trail_starter(self):
        QApplication.sendPostedEvents()
        mt5.initialize()
        conn=sqlite3.connect('gui/employee.db')
        c=conn.cursor()
        c.execute('SELECT * FROM trailer')
        data=c.fetchall()
        print(data)
        print(data[0])
        fx_default = int(data[0][0])
        fx_trail = int(data[0][1])
        fx_max_dist = int(data[0][2])
        ind_default = int(data[0][4])
        ind_trail = int(data[0][5])
        ind_max_dist = int(data[0][6])
        TrailFunc(fx_default,fx_trail,fx_max_dist,ind_default,ind_trail,ind_max_dist)
        QApplication.processEvents()
    def Tp_starter(self):
        c.execute('SELECT * FROM trailer')
        data=c.fetchall()

class start_copying(QObject):

    def __init__(self,client):
        super().__init__()
        self.client=client
    def start_event(self):
        try:
            QApplication.sendPostedEvents()
            asyncio.run(self.main())
            QApplication.processEvents()
        except BaseException as e: #sqlite3.OperationalError or ValueError:
            print('hey stop',e)
            pass

    async def main(self):
        QApplication.sendPostedEvents()
        self.client.connect
        await self.client.disconnect()
        api_id = config.api_id
        api_hash = config.api_hash
        conn=sqlite3.connect('gui/employee.db')
        c=conn.cursor()
        async with TelegramClient('gui/session', api_id, api_hash) as client:
            username= await client.get_me()
            print(utils.get_display_name(username))
            with open('gui/alljang.csv', "r") as f:
                reader = csv.reader(f, delimiter=",",lineterminator="\n")
                for row in reader:
                    channelha = row
            @client.on(events.NewMessage(chats=channelha))
            async def my_event_handler(event):
                print('event is triggered')
                with open("gui/telmsg.csv","a",encoding='UTF-8') as f:
                    writer = csv.writer(f,delimiter=",",lineterminator="\n")    
                    try:
                        if event.is_reply:
                            print('its reply')
                            repl=await event.get_reply_message()
                            base_text=repl.raw_text
                            base_text_id=repl.id 
                            reply_msg=event.raw_text
                            reply_msg_id=event.id
                            chat_from = event.chat if event.chat else (await event.get_chat()) # telegram MAY not send the chat enity
                            chat_title = chat_from.title
                            chat_id=chat_from.id

                            writer.writerow([base_text,base_text_id,chat_title,chat_id,reply_msg,reply_msg_id]) 
                            mt5.initialize()
                            account_info=mt5.account_info()
                            loggedIn=account_info.login
                           
                            trade,prices=parserepltext(reply_msg)
                            print(trade,prices)
                            filt=executed_trades[(executed_trades['AccountID']==loggedIn) & (executed_trades['MessageID']==base_text_id)]
                            pos_ticket = int(filt['PositionID'].values[0])
                            #pos_ticket=int(executed_trades.loc[filt,'PositionID'].values[0])
                            pos_sl=filt['SL'].values[0]
                            pos_tp=filt['TP'].values[0]

                            if trade=='adjust sltp':
                                if mt.positions_get(ticket=pos_ticket)[0].type==0:
                                    new_sl=min(prices)
                                    new_tp=max(prices)
                                else:
                                    new_sl=max(prices)
                                    new_tp=min(prices)
                                AdjustSLTP(pos_ticket,float(new_sl),float(new_tp))
                                print(new_sl,new_tp)
                            elif trade=='adjust sl':
                                new_sl=prices[0]
                                AdjustSLTP(pos_ticket,float(new_sl),float(pos_tp))
                                print(new_sl,pos_tp)
                            elif trade=='adjust tp':
                                new_tp=prices[0]
                                AdjustSLTP(pos_ticket,float(pos_sl),float(new_tp))
                                print(new_tp,pos_sl)
                            elif trade=='cancel':
                                removeOrder(pos_ticket)
                            elif trade=='close partial':
                                closePartials(pos_ticket)
                            elif trade=='close fully':
                                closeFully(pos_ticket)
                                print(pos_ticket)
                            c.execute(f'SELECT * FROM users')
                            data=c.fetchall()
                            for mt in data:
                                server=mt[0]
                                logins=int(mt[1])
                                if logins == loggedIn:
                                    continue
                                password=mt[2]
                                print(logins)
                                mt5.login(logins,password,server)
                                print('do1')
                                mt5.initialize()
                                account_info=mt5.account_info()
                                loggedIn=account_info.login
                                filt=executed_trades[(executed_trades['AccountID']==loggedIn) & (executed_trades['MessageID']==base_text_id)]
                                pos_ticket = int(filt['PositionID'].values[0])
                                #pos_ticket=int(executed_trades.loc[filt,'PositionID'].values[0])
                                pos_sl=filt['SL'].values[0]
                                pos_tp=filt['TP'].values[0]

                                if trade=='adjust sltp':
                                    if mt.positions_get(ticket=pos_ticket)[0].type==0:
                                        new_sl=min(prices)
                                        new_tp=max(prices)
                                    else:
                                        new_sl=max(prices)
                                        new_tp=min(prices)
                                    AdjustSLTP(pos_ticket,float(new_sl),float(new_tp))
                                    print(new_sl,new_tp)
                                elif trade=='adjust sl':
                                    new_sl=prices[0]
                                    AdjustSLTP(pos_ticket,float(new_sl),float(pos_tp))
                                    print(new_sl,pos_tp)
                                elif trade=='adjust tp':
                                    new_tp=prices[0]
                                    AdjustSLTP(pos_ticket,float(pos_sl),float(new_tp))
                                    print(new_tp,pos_sl)
                                elif trade=='cancel':
                                    removeOrder(pos_ticket)
                                elif trade=='close partial':
                                    closePartials(pos_ticket)
                                elif trade=='close fully':
                                    closeFully(pos_ticket)
                                    print(pos_ticket)

                        else:
                            chat_from = event.chat if event.chat else (await event.get_chat()) # telegram MAY not send the chat enity
                            chat_title = chat_from.title
                            chat_id=chat_from.id
                            base_text=event.raw_text
                            base_text_id=event.id
                            writer.writerow([base_text,base_text_id,chat_title,chat_id]) 
                            #analyzing the telegram text and getting sl,tp,...
                            #symbol,trade,SL,TP,ENTRY=parsetext(base_text)
                            symbol, trade, SL, ENTRY,*TPS = parsetext(base_text)
                            TP=TPS[-1]
                            print(SL,TP,ENTRY)
                            if trade=='SELL MARKET' or trade=='BUY MARKET':
                                try:
                                    mt5.initialize()
                                    account_info=mt5.account_info()
                                    loggedIn=account_info.login
                                    c.execute(f'SELECT * FROM users WHERE LoginID == {loggedIn}')
                                    data=c.fetchall()
                                    for mt in data:
                                        first_symbol=symbol
                                        server=mt[0]
                                        logins=int(mt[1])
                                        password=mt[2]
                                        suffix=mt[3]
                                        mt5.login(logins,password,server)
                                        if suffix:
                                            first_symbol=first_symbol +suffix
                                        else:
                                            first_symbol=first_symbol
                                        mt5.symbol_select(first_symbol,True)
                                        result=MarketExecution(first_symbol,0.2,trade,float(SL),float(TP))
                                        
                                        executed_trades.loc[len(executed_trades)]=[logins,base_text_id,result.order,SL,TP]
                                        print(executed_trades,symbol,SL,TP)
                                finally:
                                    c.execute('SELECT * FROM users')
                                    data=c.fetchall()
                                    for mt in data:
                                        second_symbol=symbol
                                        server=mt[0]
                                        logins=int(mt[1])
                                        password=mt[2]
                                        suffix=mt[3]
                                        if logins == int(loggedIn):
                                            continue
                                            
                                        else:
                                            server=mt[0]
                                            logins=int(mt[1])
                                            password=mt[2]
                                            suffix=mt[3]
                                            mt5.login(logins,password,server)
                                            if len(suffix) !=0:
                                                second_symbol=second_symbol + suffix
                                            else:
                                                second_symbol=second_symbol
                                            mt5.initialize()
                                            mt5.symbol_select(second_symbol,True)
                                            result=MarketExecution(second_symbol,0.3,trade,float(SL),float(TP))
                                            executed_trades.loc[len(executed_trades)]=[logins,base_text_id,result.order,SL,TP]
                                            print(executed_trades,symbol,SL,TP)
                                            #print(symbol,trade,SL,TP,ENTRY)
                            else:
                                try:
                                    mt5.initialize()
                                    account_info=mt5.account_info()
                                    loggedIn=account_info.login
                                    c.execute(f'SELECT * FROM users WHERE LoginID == {loggedIn}')
                                    data=c.fetchall()
                                    for mt in data:
                                        first_symbol=symbol
                                        server=mt[0]
                                        logins=int(mt[1])
                                        password=mt[2]
                                        suffix=mt[3]
                                        mt5.login(logins,password,server)
                                        if suffix:
                                            first_symbol=first_symbol +suffix
                                        else:
                                            first_symbol=first_symbol
                                        mt5.symbol_select(first_symbol,True)
                                        result=tradeExecution(first_symbol,0.3,trade,float(SL),float(TP),float(ENTRY))
                                        executed_trades.loc[len(executed_trades)]=[logins,base_text_id,result.order,SL,TP]
                                        
                                finally:
                                    c.execute('SELECT * FROM users')
                                    data=c.fetchall()
                                    for mt in data:
                                        second_symbol=symbol
                                        server=mt[0]
                                        logins=int(mt[1])
                                        password=mt[2]
                                        suffix=mt[3]
                                        if logins == int(loggedIn):
                                            continue
                                            
                                        else:
                                            server=mt[0]
                                            logins=int(mt[1])
                                            password=mt[2]
                                            suffix=mt[3]
                                            mt5.login(logins,password,server)
                                            if len(suffix) !=0:
                                                second_symbol=second_symbol + suffix
                                            else:
                                                second_symbol=second_symbol
                                            mt5.initialize()
                                            mt5.symbol_select(second_symbol,True)
                                            result=tradeExecution(second_symbol,0.3,trade,float(SL),float(TP),float(ENTRY))
                                            print('this is not logged in')
                                            executed_trades.loc[len(executed_trades)]=[logins,base_text_id,result.order,SL,TP]
                                            print(executed_trades,symbol,SL,TP)
                    except BaseException:
                        print('Message is not a trade')
                
            #await client.disconnect()
            try:
                await client.run_until_disconnected()
            finally:
                 client.disconnect()
            QApplication.sendPostedEvents()


class welcomescreen(QDialog):
    def __init__(self,client):
        super(welcomescreen, self).__init__()
        self.client=client
        loadUi('gui/welcomescreen.ui',self)
        
        #to add a func to the login button
        if client.is_user_authorized():
            if client.get_me():
                self.login.clicked.connect(self.home_page)

        else:
            self.login.clicked.connect(self.gotologin)
    def home_page(self):
        home=home_page(client)
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotologin(self):
        login=LoginScreen(self.client)
        widget.addWidget(login)
        #make the index of the screen, we change the screen by giving its index
        widget.setCurrentIndex(widget.currentIndex()+1)

class LoginScreen(QDialog):
    def __init__(self,client):
        super(LoginScreen, self).__init__()
        loadUi('gui/loginpage.ui',self)
     
        self.login.clicked.connect( self.loginfunction)
        
    #with this func we get the typed text inside the linedit
    def loginfunction(self):
        
        phone_number= self.phonefield.text()
        if len(phone_number) ==0:
            self.error.setText('Please enter your Phone!')
        elif len(phone_number)>0:
            phone=phonenumbers.parse(phone_number)
            if phonenumbers.is_valid_number(phone):
                    print('phone is valid')
                    #self.phonefield.clear()
                    if not client.is_user_authorized():
                        client.send_code_request(phone_number)
                        codelogin= tele_code(phone_number,client)
                        widget.addWidget(codelogin)
                        #make the index of the screen, we change the screen by giving its index
                        widget.setCurrentIndex(widget.currentIndex()+1)
                        #client.sign_in(phone_number, telegramCode)
                    
            else:
                self.error.setText('Please put a valid Phone Number! code, +93, +91')
    

class tele_code(QDialog):
    def __init__(self,phone_number,client):
        super(tele_code, self).__init__()
        self.phone_number=phone_number
        loadUi('gui/codepage.ui',self)
        #to add a func to the login button
        self.login.clicked.connect(self.logintelegram)
    
    def logintelegram(self):
        try:
            self.logged_in=client.sign_in(self.phone_number, self.phonefield.text())
            if self.logged_in:
                if client.get_me():
                    home=home_page(client)
                    widget.addWidget(home)
                    widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            self.error.setText('Please put the correct Code!')
        #print('user',self.logged_in)

class home_page(QMainWindow):

    def __init__(self,client):
        super(home_page,self).__init__()
        loadUi('gui/mainpage.ui',self)
        self.client=client
        self.widget=self.stackedWidget
        self.widget.setCurrentWidget(self.home)
        username=self.client.get_me()
        username=utils.get_display_name(username)
        self.usernamebtn.setText(f'Telegram Username: {username}')
        self.channelsbtn.clicked.connect(self.channels_page)
        self.mt5btn.clicked.connect(self.mt5_page)
        self.defaultsbtn.clicked.connect(self.defaults_page)
        self.homebtn.clicked.connect(self.home_page)
        self.magicbtn.clicked.connect(self.magic_page)
        self.mtanalyticsbtn.clicked.connect(self.analytics_page)
        self.trailingbtn.clicked.connect(self.trailer_page)
    ######################### Analytics page ###################################
    def trailer_page(self):
        self.widget.setCurrentWidget(self.stop_loss)
        self.trailing_save.clicked.connect(self.save_trailers)
        self.start_trailing.clicked.connect(self.start_trailing_func)
    def start_trailing_func(self):
        if self.radiotrailer.isChecked():
            self.trailer_start  = trail_sl()
            self.objThread3 = QThread(parent=self)
            self.trailer_start.moveToThread(self.objThread3)
            self.objThread3.started.connect(self.trailer_start.trail_starter)
            self.objThread3.start()
            self.start_trailing.setText('Trail Started')
            print('did start trailing')
        elif self.radiotp.isChecked():
            print('its tps')
            #start_tp_trailing()

        else:
            print('choose one of them')
    def save_trailers(self):
        fx_default = self.fx_default.text()
        fx_trailer =  self.fx_trailer.text()
        fx_distance = self.fx_distance.text()
        fx_cus = self.fx_cus.text()
        ind_default = self.ind_default.text()
        ind_trailer =  self.ind_trailer.text()
        ind_distance = self.ind_distance.text()
        ind_cus = self.ind_cus.text()
        com_default = self.com_default.text()
        com_trailer =  self.com_trailer.text()
        com_distance = self.com_distance.text()
        com_cus = self.com_cus.text()
        c.execute('SELECT * FROM trailer')
        data=c.fetchall()
        if len(data)==0:
            c.execute("""INSERT INTO trailer VALUES(:fxd,:fxt,:fxdist,:fxc,
                    :indd,:indt,:inddist,:indc,:comd,:comt,:comdist,:comc)""",
                    {'fxd':fx_default,'fxt':fx_trailer,'fxdist':fx_distance,'fxc':fx_cus,
                    'indd':ind_default,'indt':ind_trailer,'inddist':ind_distance,'indc':ind_cus,
                    'comd':com_default,'comt':com_trailer,'comdist':com_distance,'comc':com_cus})
            conn.commit()
        else:
            c.execute('''
                    UPDATE trailer SET fxdef=:fxd,fxtrail=:fxt,fxdistance=:fxdist,fxcus=:fxc,
                    inddef=:indd,indtrail=:indt,inddistance=:inddist,indcus=:indc,
                    comdef=:comd,comtrail=:comt,comdistance=:comdist,comcus=:comc
                    ''',
                    {'fxd':fx_default,'fxt':fx_trailer,'fxdist':fx_distance,'fxc':fx_cus,
                    'indd':ind_default,'indt':ind_trailer,'inddist':ind_distance,'indc':ind_cus,
                    'comd':com_default,'comt':com_trailer,'comdist':com_distance,'comc':com_cus
                    })
            conn.commit()
            c.execute('SELECT * FROM trailer')
            data=c.fetchall()
            print(data)
        self.fx_default.clear()
        self.fx_trailer.clear()
        self.fx_distance.clear()
        self.fx_cus.clear()
        self.ind_default.clear()
        self.ind_trailer.clear()
        self.ind_distance.clear()
        self.ind_cus.clear()
        self.com_default.clear()
        self.com_trailer.clear()
        self.com_distance.clear()
        self.com_cus.clear()   
    def analytics_page(self):
        self.widget.setCurrentWidget(self.analytica)
        self.showmtbtn.clicked.connect(self.mt_analytics)
    def mt_analytics(self):
        mt5.initialize()
        account_info=mt5.account_info()
        login_number=account_info.login
        balance=account_info.balance
        equity=account_info.equity
        floating_profit = account_info.profit

        start_date=self.startdate.dateTime().toPyDateTime()
        upto_date=self.uptodate.dateTime().toPyDateTime()
        total_sent=mt5.history_orders_total(start_date, upto_date)
        total_executed=mt5.history_deals_total(start_date, upto_date)
        all_executed_trades=mt5.history_deals_get(start_date,upto_date)
        profits = []
        commissions = []
        losses = []
        for trade in all_executed_trades:
            if trade.profit !=0.0:
                if trade.profit >0:
                     profits.append(trade.profit)
                else:
                    losses.append(trade.profit)
            else:
                commissions.append(trade.commission)      

        #total_commission = reduce(lambda x,y: x+y,commissions)
        total_commission = sum(commissions)

        if len(profits) > 0:
            max_profit = np.max(profits)

        if len(profits) > 0:    
            average_profit = np.mean(profits)

        if len(losses) > 0:
            average_loss = np.mean(losses)

        if len(losses) > 0:
            max_loss = np.min(losses)
            
        if len(profits) > 0 and len(losses) > 0:
            over_all_profit= sum(profits) - (abs(abs(sum(losses))+abs(total_commission)))

        else:
            if len(profits) ==0:
                over_all_profit= abs(sum(losses))+abs(total_commission)
                #over_all_profit = ('-'+over_all_profit)
                print('boom here')
            else:
                over_all_profit = sum(profits)

        self.analyticslist.addItem(f'LoginID:                         {login_number} ')
        self.analyticslist.addItem(f'Current Balance:                 {balance} ')
        self.analyticslist.addItem(f'Current Equity:                  {login_number} ')
        self.analyticslist.addItem(f'Total Orders Sent:                {total_sent} ')
        self.analyticslist.addItem(f'Total Executed Orders:              {total_executed} ')
        self.analyticslist.addItem(f'Max Profit:                         {max_profit} ')
        self.analyticslist.addItem(f'Average Win:                        {average_profit} ')
        self.analyticslist.addItem(f'Max Loss:                           {max_loss} ')
        self.analyticslist.addItem(f'Average Loss:                        {average_loss} ')
        self.analyticslist.addItem(f'Overall Profit:                       {over_all_profit} ')
        self.analyticslist.addItem(f'Commissions Paid:                        {total_commission} ')
        self.analyticslist.addItem(f'Floating Profit/Loss:                       {floating_profit} ')
        self.analyticslist.addItem(f'-----------------------------------------------')
    ##########################################################################

    def magic_page(self):
        self.widget.setCurrentWidget(self.magickeys)
        self.showtrades.clicked.connect(self.show_trades)
        self.refreshtrades.clicked.connect(self.refresh_trades)
        self.editTPsl.clicked.connect(self.edit_tp_sl)
        self.saveTPsl.clicked.connect(self.save_tp_sl)
        self.closeAll.clicked.connect(self.close_current_pos)
        self.closeHalf.clicked.connect(self.close_half)
        self.close_customlot.clicked.connect(self.close_custom)
        self.closeLot.clicked.connect(self.close_lot)
        self.close_fifty.clicked.connect(self.close_point_fifty)
        self.close_ten.clicked.connect(self.close_point_ten)
        self.close_five.clicked.connect(self.close_point_five)
        self.close_one.clicked.connect(self.close_point_one)
        self.breakeven.clicked.connect(self.breakeven_def)
    def breakeven_def(self):
        self.magic_errors.clear()
        items = self.tradeslist.selectedItems()
        if items:
            for i in range(len(items)):
                self.edit_ID=self.tradeslist.selectedItems()[i].text().split(':')
                self.edit_ID=int(self.edit_ID[2].split(' ')[1])
                result=breakeven_pos(self.edit_ID)
                self.show_trades()
            
    def close_point_one(self):
        self.magic_errors.clear()
        try:
            items = self.tradeslist.selectedItems()
            if items:
                for i in range(len(items)):
                    self.edit_ID=self.tradeslist.selectedItems()[i].text().split(':')
                    self.edit_ID=int(self.edit_ID[2].split(' ')[1])
                    result=close_point_one_lot(self.edit_ID)
                    self.show_trades()
                   
        except BaseException:
            self.magic_errors.setText('| Please select positionID row!')
            self.show_trades()
    def close_point_five(self):
        self.magic_errors.clear()
        try:
            items = self.tradeslist.selectedItems()
            if items:
                for i in range(len(items)):
                    self.edit_ID=self.tradeslist.selectedItems()[i].text().split(':')
                    self.edit_ID=int(self.edit_ID[2].split(' ')[1])
                    result=close_point_five_lot(self.edit_ID)
                    self.show_trades()
        except BaseException:
            self.magic_errors.setText('| Please select positionID row!') 
            self.show_trades()  
    def close_point_ten(self):
        self.magic_errors.clear()
        try:
            items = self.tradeslist.selectedItems()
            if items:
                for i in range(len(items)):
                    self.edit_ID=self.tradeslist.selectedItems()[i].text().split(':')
                    self.edit_ID=int(self.edit_ID[2].split(' ')[1])
                    close_point_ten_lot(self.edit_ID)
                    self.show_trades()
        except BaseException:
            self.magic_errors.setText('| Please select positionID row!')
            self.show_trades()
    def close_point_fifty(self):
        self.magic_errors.clear()
        try:
            items = self.tradeslist.selectedItems()
            if items:
                for i in range(len(items)):
                    self.edit_ID=self.tradeslist.selectedItems()[i].text().split(':')
                    self.edit_ID=int(self.edit_ID[2].split(' ')[1])
                    close_point_fifty_lot(self.edit_ID)
                    self.show_trades()
        except BaseException:
            self.magic_errors.setText('| Please select positionID row!')
            self.show_trades()
    def close_lot(self):
        self.magic_errors.clear()
        try:
            items = self.tradeslist.selectedItems()
            if items:
                for i in range(len(items)):
                    self.edit_ID=self.tradeslist.selectedItems()[i].text().split(':')
                    self.edit_ID=int(self.edit_ID[2].split(' ')[1])
                    close_one_lot(self.edit_ID)
                    self.show_trades()
        except BaseException:
            self.magic_errors.setText('| Please select positionID row!')
            self.show_trades()
    def close_custom(self):
        self.magic_errors.clear()
        items = self.tradeslist.selectedItems()
        try:
            if items:
                for i in range(len(items)):
                    self.edit_ID=self.tradeslist.selectedItems()[i].text().split(':')
                    self.edit_ID=int(self.edit_ID[2].split(' ')[1])
                    positions=mt5.positions_get(ticket=int(self.edit_ID))[0]
                    #self.custompcEntry.setText(str(positions.volume))
                    percent=self.customEntry.text()
                    if percent:
                        close_custom(self.edit_ID,percent)
                        self.show_trades()
        except BaseException:
            self.magic_errors.setText('| Please select positionID row!')
            self.show_trades()
    def close_half(self):
        self.magic_errors.clear()
        try:
            items = self.tradeslist.selectedItems()
            if items:
                for i in range(len(items)):
                    self.edit_ID=self.tradeslist.selectedItems()[i].text().split(':')
                    self.edit_ID=int(self.edit_ID[2].split(' ')[1])
                    closePartials(self.edit_ID)
                    self.show_trades()
        except BaseException:
            self.magic_errors.setText('| Please select positionID row!')
            self.show_trades()
    def close_current_pos(self):
        self.magic_errors.clear()
        try:
            items = self.tradeslist.selectedItems()
            if items:
                for i in range(len(items)):
                    self.edit_ID=self.tradeslist.selectedItems()[i].text().split(':')
                    self.edit_ID=int(self.edit_ID[2].split(' ')[1])
                    closeFully(self.edit_ID)
                    self.show_trades()
        except BaseException:
            self.magic_errors.setText('| Please select positionID row!')
            self.show_trades()
    def save_tp_sl(self):
        try:
            tp=self.tpentry.text()
            sl=self.slentry.text()
            ticket=self.edit_ID
            AdjustSLTP(int(ticket),float(sl),float(tp))
        except BaseException:
            self.magic_errors.setText('| Check if Fields are empty!')
    def edit_tp_sl(self):
        try:
            items = self.tradeslist.selectedItems()
            if items:
                for i in range(len(items)):
                    self.edit_ID=self.tradeslist.selectedItems()[i].text().split(':')
                    self.edit_ID=self.edit_ID[2].split(' ')[1]
                    positions=mt5.positions_get(ticket=int(self.edit_ID))[0]
                    self.tpentry.setText(str(positions.tp))
                    self.slentry.setText(str(positions.sl))
                    self.volentry.setText(str(positions.volume))
                    self.volentry.setEnabled(False)
                    self.profitentry.setText(str(positions.profit))
                    self.profitentry.setEnabled(False)
                    self.curentry.setText(str(positions.price_current))
                    self.curentry.setEnabled(False)
        except BaseException:
            self.magic_errors.setText('| Please select the PositionID row!')
    def refresh_trades(self):
        self.magic_errors.clear()
        self.magic_errors.clear()
        mt5.initialize()
        try:
            positions=mt5.positions_get()
            for position in positions:
                ticket=position.ticket
                if ticket not in self.pos:
                    profit=position.profit
                    sl=position.sl
                    tp=position.tp
                    volume=position.volume
                    pos_type= 'Buy' if position.type==1 else "Sell"
                    cur_price=position.price_current
                    open_price=position.price_open
                    symbol=position.symbol
                    self.tradeslist.addItem(f'Symbol: {symbol}                                                                 PositionID: {ticket}   ')
                    self.tradeslist.addItem(f'Profit/Loss: {profit}                SL: {sl}           TP: {tp}                     Type: {pos_type}')
                    self.tradeslist.addItem(f'Volume:{volume}                            Current_Price: {cur_price}            Opened_Price: {open_price}')
                    self.tradeslist.addItem(f'-----------------------------------------------')
                    self.pos.append(ticket)
        except:
            pass
    def show_trades(self):
        self.tradeslist.clear()
        mt5.initialize()
        self.pos=[]
        positions=mt5.positions_get()
        if not positions:
            self.magic_errors.setText('| Currently there is no positions ')
        else:
            for position in positions:
                ticket=position.ticket
                profit=position.profit
                sl=position.sl
                tp=position.tp
                volume = position.volume
                pos_type= 'Buy' if position.type==1 else "Sell"
                cur_price=position.price_current
                open_price=position.price_open
                symbol=position.symbol
                self.tradeslist.addItem(f'Symbol: {symbol}                                                                 PositionID: {ticket}   ')
                self.tradeslist.addItem(f'Profit/Loss: {profit}                SL: {sl}           TP: {tp}                     Type: {pos_type}')
                self.tradeslist.addItem(f'Volume:{volume}                            Current_Price: {cur_price}            Opened_Price: {open_price}')
                self.tradeslist.addItem(f'-----------------------------------------------')
                self.pos.append(ticket)
            self.showtrades.setEnabled(False)
    ########################### HOME_PAGE ##########################
    def home_page(self):
        self.widget.setCurrentWidget(self.home)
        self.startbtn.clicked.connect(self.start_copy)
        self.refreshbtn.clicked.connect(self.refresher)
    def refresher(self):
        print('hey')
        self.widget.setCurrentWidget(self.magickeys)

    def start_copy(self):
        self.start_copier  = start_copying(client)
        self.objThread1 = QThread(parent=self)
        self.start_copier.moveToThread(self.objThread1)
        self.objThread1.started.connect(self.start_copier.start_event)
        self.objThread1.start()
        self.startbtn.setText('Copy Started')
        self.startbtn.setEnabled(False)
        self.channelsbtn.setEnabled(False)
   
    ########################### DEFAULTS_PAGE #######################
    def defaults_page(self):
        self.widget.setCurrentWidget(self.defaults)
        self.defaultsavebtn.clicked.connect(self.save_defaults)
        self.symbolsavebtn.clicked.connect(self.save_symbol_vol)
        self.exsavebtn.clicked.connect(self.exclude_symbols)
        self.insavebtn.clicked.connect(self.include_symbols)
    def exclude_symbols(self):
        symbol=self.exentry.text()
        c.execute("DELETE FROM symbols WHERE symbol ={}".format(symbol))
        conn.commit()
    def include_symbols(self):
        symbol=self.inentry.text()
        c.execute("INSERT INTO symbols VALUES(:symbo)",
                {'symbo':symbol})
        conn.commit()
    def save_symbol_vol(self):
        symbol=self.symbolentry.text()
        volume=self.symbolvolume.text()
        symbol_volume()
        c.execute('SELECT * FROM symbol_volume')
        data=c.fetchall()
        if len(data)==0:
            c.execute("INSERT INTO symbol_volume VALUES(:symbo,:vol)",
                {'symbo':symbol ,'vol': volume })
            conn.commit()
        else:
            c.execute('update')
    def save_defaults(self):
        fxvolume=self.fxvolume.text()
        fxslippage=self.fxslippage.text()
        fxsl=self.fxsl.text()

        indexvolume=self.indexvolume.text()
        indexslippage=self.indexslippage.text()
        indexsl=self.indexsl.text()

        comvolume=self.comvolume.text()
        comslippage=self.comslippage.text()
        comsl=self.comsl.text()
        c.execute('''
                  UPDATE defaults SET fxvolume=:fxvol,fxslippage=:fxslip,fxsl=:fxsl,indexvolume=:indexvol,
                  indexslippage=:indexslip,indexsl=:indexsl,comvolume=:comvol,comslippage=:comslip,comsl=:comsl
                  ''',
                  {'fxvol':fxvolume,'fxslip':fxslippage,'fxsl':fxsl,'indexvol':indexvolume,'indexslip':indexslippage,'indexsl':indexsl,
                  'comvol':comvolume,'comslip':comslippage,'comsl':comsl})
        conn.commit()
        c.execute('SELECT * FROM defaults')
        data=c.fetchall()
        print(data)
    ########################### MT5_PAGE   ######################    
    def mt5_page(self):
        self.widget.setCurrentWidget(self.mt)
        self.mtaddbtn.clicked.connect(self.line_data)
        self.mtshow.clicked.connect(self.show_accounts)
        self.mtlogin.clicked.connect(self.login_accounts)
        self.mtdelete.clicked.connect(self.delete_accounts)
    def login_accounts(self):
        mt5.initialize()
        items = self.mtlist.selectedItems()
        for i in range(len(items)):
            self.ID=self.mtlist.selectedItems()[i].text().split(':')
            c.execute('SELECT * FROM users WHERE LoginID ={}'.format(self.ID[1]))
            print(self.ID[1])
            data=c.fetchall()
            print(data)
            for mt in data:
                print(mt)
                server=mt[0]
                logins=int(mt[1])
                password=mt[2]
                mt5.login(logins,password,server)
        QApplication.sendPostedEvents()

    def delete_accounts(self):
        items = self.mtlist.selectedItems()
        for i in range(len(items)):
            self.ID=self.mtlist.selectedItems()[i].text().split(':')
            self.ID = self.ID[1]
            print(self.ID)
            c.execute("DELETE FROM users WHERE LoginID ={}".format(self.ID))
            conn.commit()  
            self.show_accounts()
            #self.error.setText('please select the ID row!')
    def show_accounts(self):
        self.mtlist.clear()
        c.execute("SELECT * FROM users")
        data=c.fetchall()
        for mt in data:
            #self.mtlist.addItem(str(mt))
            self.mtlist.addItem(str(f'server : {mt[0]}'))
            self.mtlist.addItem(str(f'ID : {mt[1]}'))
            self.mtlist.addItem(str(f'Suffix : {mt[3]}'))
            self.mtlist.addItem(str(f'Symbols : {mt[4]}'))
            self.mtlist.addItem(str('............................. '))
    def line_data(self):
        
        mtserver=self.mtserver.text()
        if not mtserver:
            self.serverError.setText('* Required')
        mtid=self.mtid.text()
        if not mtid:
            self.idError.setText('* Required')
        mtpass=self.mtpassword.text()
        if not mtpass:
            self.passError.setText('* Required')
        mtsuffix=self.mtsuffix.text()
        mtsymbol=self.mtsymbols.text()
        try:
            int(mtid)
            self.idError.setText('')
            if mtserver and mtpass and mtid:
                c.execute("INSERT INTO users VALUES(:server,:login,:pass,:suffix,:symbol)",{'server':mtserver,'login':mtid,'pass':mtpass,'suffix':mtsuffix,'symbol':mtsymbol})
                conn.commit()
            self.mtserver.clear()
            self.mtid.clear()
            self.mtpassword.clear()
            self.mtsuffix.clear()
            self.mtsymbols.clear()
        except ValueError:
            self.idError.setText('Wrong ID')

    ################################ CHANNELS_PAGE  ####################################
    def channels_page(self):
        self.widget.setCurrentWidget(self.channels)
        self.list1.clear()
        
        #channels=client.get_dialogs()
        for dialog in client.iter_dialogs():
            if not dialog.is_user :
            #if not dialog.is_group and dialog.is_channel:
                self.list1.addItem(dialog.name)
            #print(channel.name)
        try:
            with open('gui/alljang.csv', "r") as f:
                reader = csv.reader(f, delimiter=",",lineterminator="\n")
                self.list2.clear()
                for row in reader:    
                    for i in row:
                        self.list2.addItem(str(i))
        except:
            pass 
        self.addbtn.clicked.connect(self.add_item)
        #self.list1.itemClicked.connect(self.do_print)
        self.removebtn.clicked.connect(self.remove_item)
        self.savebtn.clicked.connect(self.save_item)
    def add_item(self):
        self.error.setText('')  
        items = self.list1.selectedItems()
        for i in range(len(items)):
            itemsTextList =  [str(self.list2.item(i).text()) for i in range(self.list2.count())]
            if self.list1.selectedItems()[i].text() in itemsTextList:
                self.error.setText('--> Duplicates not allowed!')
                continue
            else:
                
                self.list2.addItem(str(self.list1.selectedItems()[i].text()))
               
    def remove_item(self):
        self.list2.takeItem(self.list2.currentRow())
    def save_item(self):
        itemsTextList =  [str(self.list2.item(i).text()) for i in range(self.list2.count())]        
        
        with open("gui/alljang.csv","w",encoding='UTF-8') as f:
            writer = csv.writer(f,delimiter=",",lineterminator="\n")
            writer.writerow(itemsTextList) 
        
        print('done')
    #######################################################################
    


app=QApplication(sys.argv)
#app.setWindowTitle('Telegram TO MT5 Copier')
welcome=welcomescreen(client)

widget = QtWidgets.QStackedWidget()
widget.setWindowTitle('Telegram To MT5 Copier')
widget.setMinimumHeight(620)
widget.setMinimumWidth(1000)
widget.addWidget(welcome)
widget.show()

try:
    sys.exit(app.exec())
except:
    print('there is a problem')

