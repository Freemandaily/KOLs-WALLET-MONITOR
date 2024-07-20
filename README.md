# KOLs-WALLET-MONITOR
Bot to monitor any Interesting addresses  whenever they make onchain transaction

### Workings
This bot monitors the onchain activities of the specified wallet addresses, it is capable of
- Spoting the wallet transaction
- spoting the Erc20 token transfered to or from the wallet addresses
- Has the ability to skip any spam ERC20 token tranfered into the wallet
- notify the user about interesting transaction/s spotted

### Requirements
- web3.py
- telegram( Get the telegram token and chatId  from the telegram bot-father, there are easier online guide to that)
- Addresses you wish to add

  ### Note
  You all need to setup the bot-token,chatId and the etherscan api key once, you can add more address to the KOLWallets.txt
