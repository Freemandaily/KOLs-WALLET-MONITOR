from unittest import result
from web3 import *
import time,sys,os
import requests,json
import telegram,asyncio
from telegram.constants import ParseMode


print('Updated 6 for Wisdom-Ethereum')
connect = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOU-INFURA-KEY'))

class maticWork:
    def __init__(self) -> None:
        self.EtherKey = 'YOUR-EXPLORER-KEY[ANY EVM EXPLORER]'
        self.offChain = 0
        self.Onchain = []

    def TransactionErrorHandler(self,url):
        print('Handling Error')
        while True:
            time.sleep(5)
            tracking_url = f'{url}&sort=desc&apikey={self.EtherKey}&page=1'
            response = requests.get(tracking_url)
            if response.status_code == 200:
                data = json.load(response.text)
                transactions = data.get('result',[])
                return transactions

    def TransactionsListFetcher(self,address):
        try:
            time.sleep(5)
            tracking_url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={self.EtherKey}&page=1'
            response = requests.get(tracking_url)
            if response.status_code == 200:
                data = json.loads(response.text)
                transactions = data.get('result',[])
                return transactions
            else:
                url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}'
                return self.TransactionErrorHandler(url)
        except Exception as e:
            time.sleep(5)
            tracking_url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={self.EtherKey}&page=1'
            response = requests.get(tracking_url)
            if response.status_code == 200:
                data = json.loads(response.text)
                transactions = data.get('result',[])
                return transactions
            else:
                url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}'
                return self.TransactionErrorHandler(url)
            

    def ERC20TransactionListFetcher(self,address):
        try:
            time.sleep(5)
            tracking_url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={address}&sort=desc&apikey={self.EtherKey}&page=1"
            response = requests.get(tracking_url)
            if response.status_code == 200:
                data = json.loads(response.text)
                transactions = data.get('result',[])
                return transactions
            else:
                url = f'https://api.etherscan.io/api?module=account&action=tokentx&address={address}'
                return self.TransactionErrorHandler(url)
        except Exception as e:
            time.sleep(5)
            tracking_url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={address}&sort=desc&apikey={self.EtherKey}&page=1"
            response = requests.get(tracking_url)
            if response.status_code == 200:
                data = json.loads(response.text)
                transactions = data.get('result',[])
                return transactions
            else:
                url = f'https://api.etherscan.io/api?module=account&action=tokentx&address={address}'
                return self.TransactionErrorHandler(url)

    def SinglHashDumper(self,address,hash):
        print('Dumping A Single Hash')
        with open(address[:6]+'.txt','r') as hashFile:
            hashData = json.load(hashFile)
            hashes = hashData['hashes']
            hashes.append(hash)
        with open(address[:6]+'.txt','w') as hashFile:
              json.dump(hashData,hashFile,indent=10)


    def HashDumper(self,address):
        print('Dumping Hashes')
        individualHases = []
        NormalWalletTransactions = self.TransactionsListFetcher(address)
        ERC20Transactions = self.ERC20TransactionListFetcher(address)
        for transaction in NormalWalletTransactions:
            individualHases.append(transaction['hash'])
        for transaction in ERC20Transactions:
            individualHases.append(transaction['hash'])
        hashData = {'address': address,'hashes': individualHases}
        with open(address[:6] +'.txt','w') as hashFile:
            #print('About To Dump Hashes')
            json.dump(hashData,hashFile,indent=10)

    def trackedAddress(self):
        TRACKED_WALLET = []
        with open('KOLWallets.txt','r') as addressFile:
            addresses = addressFile.readlines()
            for address in addresses:
                address =  connect.to_checksum_address(address[:-1])
                TRACKED_WALLET.append(address)
        return TRACKED_WALLET

    def hashFetcher(self):
        print('FETCHING HASHES')
        TRACKED_WALLET = self.trackedAddress()
        for address in TRACKED_WALLET:
            self.HashDumper(address)
            
    def HashLoader(self,address):
        with open(address[:6]+'.txt','r') as hashFile:
            hashData = json.load(hashFile)
            hashes = hashData['hashes']
        return hashes
    
    def Monitoring(self):
        TRACKED_WALLET = self.trackedAddress()
        for address in TRACKED_WALLET:
            NormalWalletTransactions = self.TransactionsListFetcher(address)
            ERC20Transactions = self.ERC20TransactionListFetcher(address)
            PreviousHashes =  self.HashLoader(address)
            self.AnalyzeNormalTransaction(NormalWalletTransactions,PreviousHashes,address)
            self.AnalyzeERC20TransferTransaction(ERC20Transactions,PreviousHashes,address)
            

    def AnalyzeNormalTransaction(self,NormalWalletTransactions,previousHashes,address):
        for transaction in NormalWalletTransactions:
            if transaction['hash'] not in previousHashes:
                self.offChain = 0
                if transaction['input'] == '0x':
                    addressFrom = Web3.to_checksum_address(transaction['from'])
                    addressTo = Web3.to_checksum_address(transaction['to'])
                    value = str(int(transaction['value'])/10**18)+' ETH'
                    hash =  transaction['hash']
                    transactionType = 'ETH TRANSFER'
                    self.Alert(transactionType,hash,From=addressFrom,To=addressTo,Value=value)
                    # Alert
                else:
                    transactionType = 'NORMAL TRANSACTION'
                    hash = transaction['hash']
                    self.Alert(transactionType,hash)
                    # Alert
                self.SinglHashDumper(address,hash)
            else:
                self.offChain += 0.1
                    

    def AnalyzeERC20TransferTransaction(self,ERC20Transactions,previousHashes,address):
        for transaction in ERC20Transactions:
            if transaction['hash'] not in previousHashes:
                self.offChain = 0
                addressFrom = Web3.to_checksum_address(transaction['from'])
                result = self.checkContract(addressFrom)
                if result == b'':
                    addressTo = Web3.to_checksum_address(transaction['to'])
                    value = (int(transaction['value'])/10**int(transaction['tokenDecimal']))
                    tokenName = transaction['tokenName']
                    hash = transaction['hash']
                    transactionType = 'ERC20 TOKEN TRANSFER'
                    # Alert
                    self.Alert(transactionType,hash,From=addressFrom,To=addressTo,Value=value,TokenName=tokenName)
                    self.SinglHashDumper(address,hash)
                    

    def checkContract(self,address):
        address  = Web3.to_checksum_address(address)
        result = connect.eth.get_code(address)
        return result
    

    def Alert(self,TransactionType,hash,**kwargs):
        transactionDetails = [f'{key}: {value}' for key,value in kwargs.items()]
        formatedTransactionDetail = '\n\n'.join(transactionDetails)
        transactionLink = f'https://etherscan.io/tx/{hash}'
        information = 'KOL TRXN SPOTTED\n\n'\
                    f'TRANSACTION TYPE: {TransactionType}\n\n'\
                    f'Hash: <a href="{transactionLink}">VIEW DETAIL</a>\n\n'\
                    f'{formatedTransactionDetail}'
        
        bot_token = 'YOUR-TELEGRAM-BOT-TOKEN'
        chatId = 'YOUR-telegram-chat-id'
        async def main():
            try:
                bot=telegram.Bot(bot_token)
            except:
                bot=telegram.Bot(bot_token)
            async with bot:
                await bot.send_message(text=information,parse_mode=ParseMode.HTML,chat_id=chatId)
        if __name__!='__main__':
            asyncio.run(main())

    
    def off_chain(self):
        chatId = 'YOUR-telegram-chat-id'
        bot_token = 'YOUR-TELEGRAM-BOT-TOKEN'
        async def main():
            try:
                bot=telegram.Bot(bot_token)
            except:
                bot=telegram.Bot(bot_token)
            async with bot:
                await bot.send_message(text=f'KOL IS OFFCHAIN \n\nBOT_STATUS:ACTIVE',
                chat_id=chatId)
        if __name__!='__main__':
            asyncio.run(main())
        
