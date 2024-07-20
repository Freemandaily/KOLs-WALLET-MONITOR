# This program tracks the wallet of a cyrpto trader onchain
# It notifies whenever a transction is made by the wallet or token is transfered in the wallet


from web3 import *
import time,sys,os
import requests,json
from matic_class import maticWork

def setUpWallet():
    try:
        with open('KOLWallets.txt','r') as file:
            if file:
                 pass
    except:
         print('Paste the address you want to monitor, type x to stop')
         time.sleep(2)
         while True:
              address = input('Paste Address\n')
              if address == 'x':
                   break
              else:
                   try:
                        address = Web3.to_checksum_address(address)
                        with open('KOLWallets.txt','a') as file:
                            file.write(address+'\n')
                            continue
                   except:
                        print('Address Not Valid,Type x to exit or paste a valid address')
                        continue
    
    print('SETUP IS COMPLETED')


def setupTelegram():
        try:
            with open('KEY-TOKEN-ID','r') as file:
                loadData = json.load(file)
                botToken = loadData['BOT-TOKEN']
                chatId = loadData['CHAT-ID']
                key = loadData['ETHER-KEY']
            return botToken,chatId,key
        except:
            explorer_key = input('Please paste your Etherscan Explorer Api-key\n')
            time.sleep(2)
            print('Please set Your one time Telegram bot token and chatId\n')
            time.sleep(3)
            token = input('What is your Telegram Bot-Token\n')
            time.sleep(2)
            chatId = input('What is your ChatId\n')
            time.sleep(2)

            data = {'BOT-TOKEN':token,'CHAT-ID':chatId,'ETHER-KEY': explorer_key}
            with open('KEY-TOKEN-ID','w') as file:
                loadData = json.dump(data,file,indent=10) 
            return token,chatId,explorer_key
             
        
token,chatId,key = setupTelegram()
setUpWallet()

processor = maticWork(token,chatId,key)
processor.hashFetcher()
tracking = True

while tracking:
    print('Mointoring Wisdom On Ethereum')
    processor.Monitoring()
    if processor.offChain >= 11 :
        processor.off_chain()
        processor.offChain = 0
    print(processor.offChain)
    # Checking the chain every 15 minutes
    time.sleep(300)


              
          

