print ("Deploying Letter Of Credit Smart Contract")
import time
import json
import web3
from eth_account import Account
from web3.auto import w3
from web3.providers.websocket import WebsocketProvider
from web3 import Web3
from solc import compile_standard
with open("LetterOfCredit.sol") as contract:
 contractText=contract.read()
with open(".pk") as pkfile:
 privateKey=pkfile.read()
with open(".infura") as infurafile:
 infuraKey=infurafile.read()

# Solidity source code
compiled_sol = compile_standard({
     "language": "Solidity",
     "sources": {
         "LetterOfCredit.sol": {
             "content": contractText
         }
     },
     "settings":
         {
             "outputSelection": {
                 "*": {
                     "*": [
                         "metadata", "evm.bytecode"
                         , "evm.bytecode.sourceMap"
                     ]
                 }
             }
         }
})
bytecode = compiled_sol['contracts']['LetterOfCredit.sol']['LetterOfCredit']['evm']['bytecode']['object']
abi = json.loads(compiled_sol['contracts']['LetterOfCredit.sol']['LetterOfCredit']['metadata'])['output']['abi']
W3 = Web3(WebsocketProvider('wss://rinkeby.infura.io/ws/v3/%s'%infuraKey))
account1=Account.from_key(privateKey);
address1=account1.address
LetterOfCredit = W3.eth.contract(abi=abi, bytecode=bytecode)
nonce = W3.eth.getTransactionCount(address1)
print(nonce)


# Submit the transaction that deploys the contract
tx_dict = LetterOfCredit.constructor().buildTransaction({
'chainId': 4,
'gas': 1400000,
'gasPrice': w3.toWei('40', 'gwei'),
'nonce': nonce,
'from':address1
})
signed_txn = W3.eth.account.sign_transaction(tx_dict, private_key=privateKey)
print(signed_txn)
print("Deploying the Smart Contract")
result = W3.eth.sendRawTransaction(signed_txn.rawTransaction)
print(result)
print('########################')
tx_receipt = None

count = 0
while tx_receipt is None and (count < 100):
  time.sleep(1)
  try:
    tx_receipt = W3.eth.getTransactionReceipt(result)
  except:
    print('.')

if tx_receipt is None:
  print (" {'status': 'failed', 'error': 'timeout'} ")
#diagnostics
#print (tx_receipt)
print("Contract address is:",tx_receipt.contractAddress)
# 0x10f49f5cD8D3396EFdfcc9AE9f748e56DF1e2dE6

letter_of_credit = W3.eth.contract(
  address=tx_receipt.contractAddress,
  abi=abi
)
print("Parties involved in the LetterOfCredit Smart Contract")
print(letter_of_credit.functions.letter().call())
nonce = W3.eth.getTransactionCount(address1)
tx_dict = letter_of_credit.functions.setLetter('Letter of Credit - 10565195: APPROVED').buildTransaction({
  'chainId': 4,
  'gas': 1400000,
  'gasPrice': w3.toWei('40', 'gwei'),
  'nonce': nonce,
  'from':address1
})

signed_txn = W3.eth.account.sign_transaction(tx_dict, private_key=privateKey)
result = W3.eth.sendRawTransaction(signed_txn.rawTransaction)
tx_receipt = None

count = 0
while tx_receipt is None and (count < 100):
  time.sleep(1)
  try:
    tx_receipt = W3.eth.getTransactionReceipt(result)
  except:
    print('.')

if tx_receipt is None:
  print (" {'status': 'failed', 'error': 'timeout'} ")

tx_hash = letter_of_credit.functions.setLetter('Letter of Credit - 10565195: DECLINED').transact({"from":account1.address})
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("Output from letter")
print(letter_of_credit.functions.letter().call({"from":account1.address}))
# 'Letter of Credit - 10565195: DECLINED'
