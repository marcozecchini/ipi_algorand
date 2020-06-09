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


def print_ipi_records(account, asset_id_ipi): # todo modifica con stampa di json come in documento
    account_info = acl.account_info(account)
    for asset in account_info["assets"]:
        print("\n------------------------------------------------")
        ipi_record = acl.asset_info(int(asset))
        print(json.dumps(ipi_record, indent=4))
        if int(asset_id_ipi) == int(asset):
            continue
        elif "metadatahash" not in ipi_record.keys():
            print("\nWhole World")
        else:
            char_vector = base64.b64decode(ipi_record["metadatahash"]).decode()
            res = "\n"+vectortocountry(country_list, char_vector)
            if ("ZW" in ipi_record["url"]):
                res += ",ZW"
            print(res)
        print("Amount: {0}".format(account_info["assets"][asset]["amount"]))
        print("------------------------------------------------\n")

def print_created_assets(account):
    account_info = acl.account_info(account)
    print(json.dumps(account_info["thisassettotal"], indent=4))

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
    # print(sent)

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

    input("Press smt when you have fill {0}".format(account))

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



# create cmo account  
acl, cmo_account, cmo_private_key = setup_acl()

# create rightholder account
private_key, account = account_algosdk.generate_account()
print("Rh address: {}".format(account))
print("Rh passphrase: {}".format(mnemonic.from_private_key(private_key)))

# create IPI names & identifier
asset_id_ipi = create_ipi_name(account, private_key)
asset_info_ipi = acl.asset_info(asset_id_ipi)
# print(json.dumps(asset_info_ipi, indent=4))

# create ipi record
ipi_record_id = create_succint_ipi_record(asset_info_ipi["unitname"], cclasses_list[0], roles_list[0], rights_list[0], "2000", "2050", 100, ["WO"], account, private_key)
ipi_record_id2 = create_succint_ipi_record(asset_info_ipi["unitname"], cclasses_list[1], roles_list[1], rights_list[1], "2000", "2050", 100, ["IT"], account, private_key)

print_ipi_records(account, asset_id_ipi)

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

print_ipi_records(cmo_account, asset_id_ipi)
