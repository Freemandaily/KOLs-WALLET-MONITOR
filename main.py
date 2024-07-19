# This program tracks the wallet of a cyrpto trader onchain
# It notifies whenever a transction is made by the wallet or token is transfered in the wallet


from web3 import *
import time,sys,os
import requests,json
from matic_class import maticWork

processor = maticWork()
processor.hashFetcher()
tracking = True

while tracking:
    print('Mointoring Wisdom On Ethereum')
    processor.Monitoring()
    if processor.offChain >= 11 :
        processor.off_chain()
        processor.offChain = 0
    print(processor.offChain)
    time.sleep(10)