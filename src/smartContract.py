import json
from web3 import Web3
import torch
import numpy as np


ganache_url = "http://127.0.0.1:7545"


class SmartContract:
  def __init__(self, chunk_num):
    self.chunk_num = chunk_num
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    truffleFile = json.load(open('./build/contracts/Chunk.json'))
    abi = truffleFile['abi']
    bytecode = truffleFile['bytecode']
    contract = web3.eth.contract(bytecode=bytecode, abi=abi)
    tx_hash = contract.constructor().transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    self.contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    print("chunk {} made".format(self.chunk_num))


  def get_chunk(self):
    print("got chunk {}".format(self.chunk_num))
    return self.contract.functions.download_chunk().call()


  def upload_chunk(self, codebook):
    print("uploaded chunk {}".format(self.chunk_num))
    self.contract.functions.upload_book(codebook[:3]).transact()
    for key in codebook[3].keys():
      self.contract.functions.upload_arr(key, codebook[3][key]).transact()
  

# sc = SmartContract(5)
# sc.upload_chunk((1,1,1,[[1,2,3], [2,3,4]]))
# print(sc.get_chunk())

# arr, scale, zero_point = q.chunkQuantization(torch.tensor([-1.2, 1.1, 2.1]))
# upload_chunk(0, arr, scale, zero_point)
# print(get_chunk(0))

# print('Default contract greeting: {}'.format(
#   contract.functions.greet().call()
# ))

# tx_hash = contract.functions.setGreeting('HiHi').transact()

# web3.eth.waitForTransactionReceipt(tx_hash)

# print('Updated contract geeting: {}'.format(
#   contract.functions.greet().call()
# ))