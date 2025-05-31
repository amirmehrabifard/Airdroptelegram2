from web3 import Web3
import os

bsc_rpc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc_rpc))

token_contract_address = Web3.to_checksum_address("0xd5baB4C1b92176f9690c0d2771EDbF18b73b8181")
airdrop_wallet_address = Web3.to_checksum_address("0xd5F168CFa6a68C21d7849171D6Aa5DDc9307E544")
private_key = os.getenv("PRIVATE_KEY")

erc20_abi = [
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    }
]

token_contract = web3.eth.contract(address=token_contract_address, abi=erc20_abi)

def send_tokens(to_address, amount):
    try:
        to_checksum = Web3.to_checksum_address(to_address)
        decimals = 18
        amount_wei = int(amount * 10 ** decimals)

        nonce = web3.eth.get_transaction_count(airdrop_wallet_address)
        txn = token_contract.functions.transfer(to_checksum, amount_wei).build_transaction({
            'chainId': 56,
            'gas': 100000,
            'gasPrice': web3.to_wei('5', 'gwei'),
            'nonce': nonce
        })

        signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return web3.to_hex(tx_hash)
    except Exception as e:
        print(f"Error sending tokens: {e}")
        return None
