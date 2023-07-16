from brownie import accounts, network, config
from dotenv import load_dotenv
import eth_utils

load_dotenv()

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["mainnet-fork", "ganache-local", "development"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallets"]["from_key"])
    return None


def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")

    return initializer.encode_input(*args)


def upgrade(
    account,
    proxy,
    new_implementation_address,
    proxy_admin_contract=None,
    initializer=None,
    *args
):
    transaction = None
    if proxy_admin_contract:
        if initializer:
            encode_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encode_function_call,
                {"from": account},
            )
        else:
            transaction = proxy_admin_contract.upgrade(proxy.address,new_implementation_address,{"from":account})
    else:    
        if initializer:
            encode_function_call = encode_function_data(initializer, *args)
            transaction = proxy.upgradeToAndCall(new_implementation_address,encode_function_call,{"from":account})
        else:
            transaction =proxy.upgradeTo(new_implementation_address,{"from":account})
    return transaction