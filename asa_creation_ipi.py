#/usr/bin/python3
import json
import time
import base64
import os
from encode import *
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
    # recover a account  
    private_key, account = account_algosdk.generate_account()
    # passphrase1 = "faint fog unfair treat enemy disagree host merit bulb lizard client proof aspect cruise vital lion gate victory planet grace weird food phrase absent marriage"
    # private_key = mnemonic.to_private_key(passphrase1)
    # account = account_algosdk.address_from_private_key(private_key)
    print("CMO address: {}".format(account))
    print("CMO passphrase: {}".format(mnemonic.from_private_key(private_key)))

    # connect to node
    acl = connect_to_network()
    return acl, account, private_key

def create_ipi_name(account, private_key):
    # get suggested parameters
    params = acl.suggested_params()
    gen = params["genesisID"]
    gh = params["genesishashb64"]
    last_round = params["lastRound"]
    fee = params["fee"]

    input("Press smt when you have fill {0}".format(account))

    # create transaction
    # Configure fields for creating the asset.
    data = {
        "sender": account,
        "fee": fee,
        "first": last_round,
        "last": last_round+100,
        "gh": gh,
        "total": 1, # (1 / share)*100 = total 
        "decimals": 0,
        "default_frozen": False,
        "unit_name": "MarioRos", # CC, RL, RH
        "asset_name": "I-001450581-6;41161231;N", # IP - base/name number?  - 32 bytes
        "manager": account,
        "reserve": account,
        "freeze": account,
        "clawback": account,
        "flat_fee": True
    }
    txn = transaction.AssetConfigTxn(**data)

    # sign transaction
    stxn = txn.sign(private_key)

    # send them over network
    sent = acl.send_transaction(stxn)
    # print txid
    print(sent)

    # wait for confirmation
    txinfo = wait_for_confirmation( acl, sent) 
    asset_id = txinfo["txresults"]["createdasset"]

    return asset_id

# create ipi record          
def create_succint_ipi_record(IPI_id, cc, rl, rh, from_date, to_date, share, territories, account, private_key) : # how do I pass territory string

    # get suggested parameters
    params = acl.suggested_params()
    gen = params["genesisID"]
    gh = params["genesishashb64"]
    last_round = params["lastRound"]
    fee = params["fee"]

    input("Press smt when you have fill {0}".format(account))

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
    print(sent)

    # wait for confirmation
    txinfo = wait_for_confirmation( acl, sent) 
    asset_id = txinfo["txresults"]["createdasset"]

    asset_info = acl.asset_info(asset_id)
    print(json.dumps(asset_info, indent=4))
    return asset_info



# create cmo account  
acl, cmo_account, cmo_private_key = setup_acl()

# create rightholder account
private_key, account = account_algosdk.generate_account()
print("Rh address: {}".format(account))
print("Rh passphrase: {}".format(mnemonic.from_private_key(private_key)))

# create IPI names & identifier
asset_id_ipi = create_ipi_name(account, private_key)
asset_info_ipi = acl.asset_info(asset_id_ipi)
print(json.dumps(asset_info_ipi, indent=4))

# create ipi record
ipi_record = create_succint_ipi_record(asset_info_ipi["unitname"], cclasses_list[0], roles_list[0], rights_list[0], "2000", "2050", 100, ["WO"], account, private_key)

if "metadatahash" not in ipi_record.keys():
    print("Whole World")
else:
    char_vector = base64.b64decode(ipi_record["metadatahash"]).decode()
    res = vectortocountry(country_list, char_vector)
    if ("ZW" in ipi_record["url"]):
        res += ",ZW"
    print(res)

# # todo per PoC:
# * vedi account balance e printa le scelte
# * gestisci __main__ e sys.argv elaborato per gestire i record