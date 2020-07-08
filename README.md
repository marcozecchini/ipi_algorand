# IPI record on Algorand standard asset

We have to represent the following structure:
 *IP_name, Name_type, Creation_class, Role, Right, Collecting_Society,  IP_type, Current_status, IP_base_number, IP_name_number, date_from, date_to, Share, Territory*

```
record = {
    "IP_name": "Mario Rossi",
    "Name_type" : "PA",# Name Type (e.g. Patronym)
    "CC": "MW", # Creation Class (e.g. Musical Work)
    "RL": "MC", # Role (e.g. Musical Creator)
    "RH": "PR", # Right (e.g. Performing Right)
    "Collecting_Society": "SIAE", # Collecting Society (e.g. SIAE)
    "IP_type": "N", # IP Type (e.g. ?)
    "Current_status": 1, # Current Status (e.g. ?)
    "IP_base_number": "I-001450581-6", # IPI BASE NUMBER
    "IP_name_number": "41161231", # IPI NAME NUMBER
    "date_from": 2000,
    "date_to": 2050,
    "Share": 100,
    "Territory": "Italy"
}
```

## 1. Assets based from Right holder to CMO

### To insert a new row in the IPI

* Right holder install an App
* The App generates a couple Sk,Pk of secret and public keys
* **A unique IPI number is associated to Sk,Pk by a suitable verifiable claim in a Self-Sovereign Identity perspective** -> **TODO**
* A CMO is an entity in the chain with its own  Sk_CMO,Pk_CMO
* Through the App, users can fill-up all the necessary fields to register an entity in the IPI. All this information is stored in a private space and signed by the user while the link to this information is stored in an asset. Note that the user remains the manager of the asset and consequently he/she can recall it. 

* The asset is finally transferred to a CMO, that will behave accordingly in a given territory

### To update a row in the IPI

* The user revokes the asset to assign it to a different CMO
* The user can modify the off-chain information and possibly sign the information with its private key

### To view the IPI
Access the assets of the CMOs or of the users

--------------------------------------------------

#### Strengths

* It models the reality
* Accessing the state of an account you have all the information you need and its proof without scanning the whole chain. 
* Possibility to group IPI records
#### Drawbacks
* Such a decentralized solution is too difficult to adopt? (From SIAE point of view)
* Right holders have to manage by themselves the external sources filled with the information
* 1000 asset limitations for CMO

-------------------------------------------

## 2. Alternative solution based on asset (Encoding the IPI record)
Using all the info fields of an Asset you can have all the information you need. 

Note that these are the length of the Asset info fields:
* length(unit_name) <=15 bytes
* length(asset_name) <= 32 bytes 
* length(url) <= 32 bytes 
* length(metadata_hash) == 32 base64 bytes(fixed)

Instead of representing a dense table repeating *IP_Name, IP_base_number, IP_name_number, Name Type* every row that doesn’t change we use a single Asset for representing them.

Then, I create one asset per record IPI that I combine with the asset info fields described previously. For instance, unit_name/asset_name = {CCRLRH} , url = {date interval}, metadata_hash = {binary vector with all the territories}, total = ( 1 / Share ) * 100. 

 In the metadata_hash we can represent all world countries (~ 192) with the following vector:

x = (x0, x1, ..., x192) where xi ={1 if territory i is involved in the IPI record; 0 otherwise} 

It follows the snippet of code where the ASA parameters are specified:
```
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
```


### To insert a new row in the IPI

* The right holder install an App
* The App generates a couple of Sk, Pk of secret and public keys
* **A unique IPI number is associated to Sk,Pk by a suitable verifiable claim in a Self-Sovereign Identity perspective** -> **TODO**
* A CMO is an entity in the chain with its own  Sk_CMO, Pk_CMO
* Through the App, users can fill-up all the necessary fields to register an entity in the IPI. All this information is stored in the asset information fields.
* The asset is finally transferred to a CMO, that will behave accordingly in a given territory

### To update a row in the IPI

The user revokes the asset to assign it to a different CMO
The user destroys the previous asset and it creates, through the App, a new one with the updated information. 

### To view the IPI
Access the assets of the CMOs or of the users

---------------------------------------------

#### Strengths
* It models the reality
* Accessing the state of an account you have all the information you need and its proof without scanning the whole chain. 
* Everything is written in the chain
* Easy to switch to the external references solution (right holder private space pointer in the URL field)

#### Drawbacks
* 1000 asset limitations for CMO
* IPI records can’t be grouped
* To update an IPI record you need to destroy and recreate an asset

----------------------------------------------

A first PoC (running [`asa_creation_ipi.py`](https://github.com/marcozecchini/ipi_algorand/blob/master/asa_creation_ipi.py)) is available here: https://www.youtube.com/watch?v=JAGWgb2maH0
