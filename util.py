import json
import base64
from encode import *

def print_ipi_on_chain_structure(acl, account, asset_id_ipi): # todo modifica con stampa di json come in documento
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

def get_ipi_records(acl, cmo_list, account): 
    account_info = acl.account_info(account)
    asset_ipi = {}
    asset_ipi_id = 0
    res = []
    for asset in account_info["assets"]:
        record = acl.asset_info(int(asset))
        territory = "World"
        if "IPI:" in record["assetname"]:
            asset_ipi = record
            asset_ipi_id = int(asset)
            continue
        if "IPI_external" in record["assetname"]:
            temp = {"External IPIs" : record["url"]}
            res.append(temp)
            continue
        if "metadatahash" in record.keys():
            char_vector = base64.b64decode(record["metadatahash"]).decode()
            territory = vectortocountry(country_list, char_vector)
            if ("ZW" in record["url"]):
                territory += ",ZW"
        temp_values = asset_ipi["assetname"][4:].split(";")
        owning = get_collecting_society(acl, cmo_list, asset)
        if record["total"] == 1:
            temp = {"IP_Name": asset_ipi["url"], "Name_type" : temp_values[2], "CC": record["unitname"][0:2], "RL": record["unitname"][2:4], 
                "RH": record["unitname"][4:6], "IP_type": temp_values[1], "IP_base_number": temp_values[0], "IP_name_number": asset_ipi["unitname"], 
                "date_from": record["url"].split("-")[0], "date_to": record["url"].split("-")[1], "Territory": territory, "Collecting_society" : owning[0],
                "Share" : 100 } 
            res.append(temp)
        else:
            for owner in owning:
                info = acl.account_info(owner)
                owned = info["assets"][asset]["amount"]
                temp = {"IP_Name": asset_ipi["url"], "Name_type" : temp_values[2], "CC": record["unitname"][0:2], "RL": record["unitname"][2:4], 
                "RH": record["unitname"][4:6], "IP_type": temp_values[1], "IP_base_number": temp_values[0], "IP_name_number": asset_ipi["unitname"], 
                "date_from": record["url"].split(":")[0], "date_to": record["url"].split(":")[1], "Territory": territory, "Collecting_society" : owner,
                "Share" : (record["total"]/owned)*100 } 
                res.append(temp)
    return res


def print_ipi_records(acl, cmo_list, account):
    res = get_ipi_records(acl, cmo_list, account)
    print("\n---------------------------------")
    print("IPI records of account", account)
    print("---------------------------------")

    for elem in res:
        print(json.dumps(elem, indent=4))

    print("---------------------------------")


def get_collecting_society(acl, cmo_list, asset_id):
    res = []
    for cmo in cmo_list:
        account_info = acl.account_info(cmo)
        if str(asset_id) in account_info["assets"]:
            res.append(cmo)
    return res


def print_created_assets(acl, account):
    account_info = acl.account_info(account)
    print(json.dumps(account_info["thisassettotal"], indent=4))