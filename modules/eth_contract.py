from web3 import Web3
import requests


class EthContract():


    def __init__(self, contract_adress, function, amount, price, gas, cancel, task, name, privkey, wallet_address, rpc):

        self.web3 = Web3(Web3.HTTPProvider(rpc))
        self.name = name
        self.contract_adress = contract_adress
        self.function = function
        self.parameters = [amount]
        self.price = price
        self.gas = gas
        self.privkey = privkey
        self.wallet_address = wallet_address
        self.task = task
        self.cancel = cancel

        self._terminate = None

    def _get_abi(self):

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36"
        }

        payload = {
            "module": "contract",
            "action": "getabi",
            "address": self.contract_adress,
            "apikey": "Q597826139TAGNYGWCZZZM8FIIBWJFEN17"
        }

        try:
            
            res = requests.get("https://api.etherscan.io/api",params=payload, headers=headers).json()
            
            return res["result"] if res["status"] == "1" else None
        
        except:
            
            return None
   

    def send_transaction(self):


        self.contract = self.web3.eth.contract(address=self.contract_adress, abi=self.contract_abi)

        raw_tx = {
            'nonce': self.web3.eth.get_transaction_count(self.wallet_address),
            'from': self.wallet_address,
            'to': self.contract_adress,
            'gasPrice': self.web3.toWei(self.gas, 'gwei'),
            'value': self.web3.toWei(self.price, "ether"),
            'data': self.contract.encodeABI(fn_name=self.function, args=self.parameters),
            'gas': self.web3.eth.estimateGas({
                'nonce': self.web3.eth.get_transaction_count(self.wallet_address),
                'from': self.wallet_address,
                'to': self.contract_adress,
                'gasPrice': self.web3.toWei(self.gas, 'gwei'),
                'value': self.web3.toWei(self.price, "ether"),
                'data': self.contract.encodeABI(fn_name=self.function, args=self.parameters),
            })
        }

        signed_txn = self.web3.eth.account.sign_transaction(raw_tx, private_key=self.privkey)
        
        try:
        
            self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            tx_hash = signed_txn.hash.hex()

            return tx_hash
        
        except:
            
            return None

    def cancel_transaction(self):

        raw_tx = {
            'nonce': self.web3.eth.get_transaction_count(self.wallet_address),
            'from': self.wallet_address,
            'to': self.wallet_address,
            'gasPrice': self.web3.toWei(self.gas+self.gas*0.2, 'gwei'),
            'value': 0,
            'gas': self.web3.eth.estimateGas({
                'nonce': self.web3.eth.get_transaction_count(self.wallet_address),
                'from': self.wallet_address,
                'to': self.wallet_address,
                'gasPrice': self.web3.toWei(self.gas+self.gas*0.2, 'gwei'),
                'value': 0,
            })
        }

        signed_txn = self.web3.eth.account.sign_transaction(raw_tx, private_key=self.privkey)
        
        try:
                
            self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            tx_hash = signed_txn.hash.hex()

            return tx_hash
        
        except:
            
            return None


if __name__ == "__main__":

    EthContract()
