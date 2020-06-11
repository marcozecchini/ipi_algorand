#/usr/bin/python3
import json
import time
import base64
import os
from encode import *
from util import *
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
    return txinfo


def setup_acl():
    # connect to node
    acl = connect_to_network()
    return acl

def setup_cmo():
    private_key, account = account_algosdk.generate_account()
    # passphrase1 = "faint fog unfair treat enemy disagree host merit bulb lizard client proof aspect cruise vital lion gate victory planet grace weird food phrase absent marriage"
    # private_key = mnemonic.to_private_key(passphrase1)
    # account = account_algosdk.address_from_private_key(private_key)
    print("CMO address: {}".format(account))
    print("CMO passphrase: {}".format(mnemonic.from_private_key(private_key)))
    return  account, private_key

def create_ipi_name(account, private_key):
    # get suggested parameters
    params = acl.suggested_params()
    gen = params["genesisID"]
    gh = params["genesishashb64"]
    last_round = params["lastRound"]
    fee = params["fee"]


    # create transaction
    # Configure fields for creating the asset.
    data = {
        "sender": account,
        "fee": fee,
        "first": last_round,
        "last": last_round+100,
        "gh": gh,
        "total": 1,  
        "decimals": 0,
        "default_frozen": False,
        "unit_name": "41161231", # ipi_name_number
        "asset_name": "IPI:I-001450581-6;N;PA", # IPI:<ipi_base_number>;<IPI_type>;<name_type> - base/name number?  - 32 bytes
        "manager": account,
        "reserve": account,
        "freeze": account,
        "clawback": account,
        "url": "Mario Rossi", # IPI_name
        "flat_fee": True
    }
    txn = transaction.AssetConfigTxn(**data)

    # sign transaction
    stxn = txn.sign(private_key)

    # send them over network
    sent = acl.send_transaction(stxn)
    # print txid
    # print(sent)

    # wait for confirmation
    txinfo = wait_for_confirmation( acl, sent) 
    asset_id = txinfo["txresults"]["createdasset"]

    return asset_id

# create ipi record          
def create_succint_ipi_record(IPI_id, cc, rl, rh, from_date, to_date, share, territories, account, private_key) : 

    # get suggested parameters
    params = acl.suggested_params()
    gen = params["genesisID"]
    gh = params["genesishashb64"]
    last_round = params["lastRound"]
    fee = params["fee"]

    # create transaction2
    # Configure fields for creating the asset.
    data = {
        "sender": account,
        "fee": fee,
        "first": last_round,
        "last": last_round+100,
        "gh": gh,
        "total": int(( 1 / share ) * 100), # (1 / share)*100 = total 
        "decimals": 0,
        "default_frozen": False,
        "unit_name": cc+rl+rh, # CC, RL, RH
        "asset_name": IPI_id, # IP - base/name number?  - 32 bytes
        "manager": account,
        "reserve": account,
        "freeze": account,
        "clawback": account,
        "url" : from_date+"-"+to_date,
        "metadata_hash" : countrytovector(country_list, territories).encode(),
        "flat_fee": True
    }

    if "WO" in territories: 
        del data["metadata_hash"]
    if "ZW" in territories:
        data["url"] = data["url"] + "-ZW"

    txn = transaction.AssetConfigTxn(**data)

    # sign transaction
    stxn = txn.sign(private_key)

    # send them over network
    sent = acl.send_transaction(stxn)
    # print txid
    # print(sent)

    # wait for confirmation
    txinfo = wait_for_confirmation( acl, sent) 
    asset_id = txinfo["txresults"]["createdasset"]

    asset_info = acl.asset_info(asset_id)
    # print(json.dumps(asset_info, indent=4))
    return asset_id

def create_external_ipi_record(account, private_key, url):
    # get suggested parameters
    params = acl.suggested_params()
    gen = params["genesisID"]
    gh = params["genesishashb64"]
    last_round = params["lastRound"]
    fee = params["fee"]

    # create transaction2
    # Configure fields for creating the asset.
    data = {
        "sender": account,
        "fee": fee,
        "first": last_round,
        "last": last_round+100,
        "gh": gh,
        "total": 1, 
        "decimals": 0,
        "default_frozen": False,
        "unit_name": "IPIs", # CC, RL, RH
        "asset_name": "IPI_external", # IP - base/name number?  - 32 bytes
        "manager": account,
        "reserve": account,
        "freeze": account,
        "clawback": account,
        "url" : "https://bit.ly/37hQKQa",
        "flat_fee": True
    }

    txn = transaction.AssetConfigTxn(**data)

    # sign transaction
    stxn = txn.sign(private_key)

    # send them over network
    sent = acl.send_transaction(stxn)
    # print txid
    # print(sent)

    # wait for confirmation
    txinfo = wait_for_confirmation( acl, sent) 
    asset_id = txinfo["txresults"]["createdasset"]

    asset_info = acl.asset_info(asset_id)
    # print(json.dumps(asset_info, indent=4))
    return asset_id


def transfer_ipi(asset_id, to_account, account, private_key, opt_in=False) : # how do I pass territory string

    # get suggested parameters
    params = acl.suggested_params()
    gen = params["genesisID"]
    gh = params["genesishashb64"]
    last_round = params["lastRound"]
    fee = params["fee"]

    # create transaction2
    # Configure fields for creating the asset.
    # send 10 
    data = {
        "sender": account,
        "fee": fee,
        "first": last_round,
        "last": last_round+100,
        "gh": gh,
        "receiver": to_account,
        "amt": 1 if opt_in==False else 0,
        "index": asset_id,
        "flat_fee": True
    }
    print("Asset Transfer")
    txn = transaction.AssetTransferTxn(**data)
    stxn = txn.sign(private_key)
    txid = acl.send_transaction(stxn, headers={'content-type': 'application/x-binary'})
    print(txid)

    # wait for confirmation
    txinfo = wait_for_confirmation( acl, txid) 

    # todo add asset_id return


acl = setup_acl()

# create cmo account 
cmo_account, cmo_private_key = setup_cmo()
cmo_list = [cmo_account]


# create rightholder account
private_key, account = account_algosdk.generate_account()
print("Rh address: {}".format(account))
print("Rh passphrase: {}".format(mnemonic.from_private_key(private_key)))


input("Press smt when you have filled the accounts")

# create IPI names & identifier
asset_id_ipi = create_ipi_name(account, private_key)
asset_info_ipi = acl.asset_info(asset_id_ipi)
# print(json.dumps(asset_info_ipi, indent=4))

# create ipi record. Two types: 1) external 2) on-chain
ipi_record_id = create_external_ipi_record(account, private_key, "https://bit.ly/37hQKQa")
ipi_record_id2 = create_succint_ipi_record(asset_info_ipi["unitname"], cclasses_list[1], roles_list[1], rights_list[1], "2000", "2050", 100, ["IT"], account, private_key)


print("Here is how IPI records look like in chain ...")
print_ipi_on_chain_structure(acl, account, asset_id_ipi)

# record 1
## optin cmo
transfer_ipi(ipi_record_id, cmo_account, cmo_account, cmo_private_key, opt_in=True)

## transfer to cmo
transfer_ipi(ipi_record_id, cmo_account, account, private_key)

# record 2
## optin cmo
transfer_ipi(ipi_record_id2, cmo_account, cmo_account, cmo_private_key, opt_in=True)

## transfer to cmo
transfer_ipi(ipi_record_id2, cmo_account, account, private_key)

print_ipi_records(acl, cmo_list, account)
