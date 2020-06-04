#/usr/bin/python3
import json
import time
import base64
import os
from algosdk import algod
from algosdk import mnemonic
from algosdk import transaction
from algosdk import encoding
from algosdk import account as account_algosdk

# utility to connect to node
def connect_to_network():
    algod_address = "http://127.0.0.1:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)
    return algod_client

# utility for waiting on a transaction confirmation
def wait_for_confirmation( algod_client, txid ):
    while True:
        txinfo = algod_client.pending_transaction_info(txid)
        if txinfo.get('round') and txinfo.get('round') > 0:
            print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('round')))
            break
        else:
            print("Waiting for confirmation...")
            algod_client.status_after_block(algod_client.status().get('lastRound') +1)

# group transactions           
def group_transactions() :

    # recover a account  
    # private_key, account = account_algosdk.generate_account()
    passphrase1 = "faint fog unfair treat enemy disagree host merit bulb lizard client proof aspect cruise vital lion gate victory planet grace weird food phrase absent marriage"
    private_key = mnemonic.to_private_key(passphrase1)
    account = account_algosdk.address_from_private_key(private_key)
    print("My address: {}".format(account))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))

    # connect to node
    acl = connect_to_network()

    # get suggested parameters
    params = acl.suggested_params()
    gen = params["genesisID"]
    gh = params["genesishashb64"]
    last_round = params["lastRound"]
    fee = params["fee"]
    amount = 1000

    input("Press smt when you have fill {0}".format(account))
    # create transaction1
    txn1 = transaction.PaymentTxn(account, fee, last_round, last_round+100, gh, account, amount)
    txid = txn1.get_txid()


    # create transaction2
    # Configure fields for creating the asset.
    data = {
        "sender": account,
        "fee": fee,
        "first": last_round,
        "last": last_round+10,
        "gh": gh,
        "total": 1, # share = 1 / total 
        "decimals": 0,
        "default_frozen": False,
        "unit_name": "MWMCPR", # CC, RL, RH
        "asset_name": "IPxxxxxxx", # IP - base/name number?  - 32 bytes
        "manager": account,
        "reserve": account,
        "freeze": account,
        "clawback": account,
        # Two ways here
        "url": "ciaociaociaociaociaociaociaociao", # 1) if less than 32 bytes of information
        #"metadata_hash" : "ciaociaociaociaociaociaociaociao",
        # "metadata_hash" : txid[:32], # 2) if more than 32 bytes: 52 hash txid of a previous transaction where in Note
        # "url": txid[32:], # there are all the informations 
        "flat_fee": True
    }
    txn2 = transaction.AssetConfigTxn(**data)

    # get group id and assign it to transactions
    gid = transaction.calculate_group_id([txn1, txn2])
    txn1.group = gid
    txn2.group = gid

    # sign transaction1
    stxn1 = txn1.sign(private_key)

    # sign transaction2
    stxn2 = txn2.sign(private_key)

    signedGroup =  []
    signedGroup.append(stxn1)
    signedGroup.append(stxn2)

    # send them over network
    sent = acl.send_transactions(signedGroup)
    # print txid
    print(sent)

    # wait for confirmation
    wait_for_confirmation( acl, sent) 

# Test Runs     
group_transactions()