from web3 import Web3
import requests
import csv
import time
from threading import Thread
from rich.console import Console

from utils.helpers import *

console = Console(highlight=False, log_path=False)

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
        
    def run_task(self):

        if self._get_abi():

            if self._send_transaction():

                while True:

                    if self._terminate is None:

                        self._monitor_task()

                    else:

                        return self._terminate

        else:

            return self._terminate

    def _get_abi(self):

        try:

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36"
            }

            payload = {
                "module": "contract",
                "action": "getabi",
                "address": self.contract_adress,
                "apikey": "Q597826139TAGNYGWCZZZM8FIIBWJFEN17"
            }

            res = requests.get("https://api.etherscan.io/api",
                               params=payload, headers=headers).json()

            if res["status"] == "1":

                self.contract_abi = res["result"]

                return True
        except:

            pass

        return None

    def _send_transaction(self):

        i = 0

        while i < 10:

            try:

                self.contract = self.web3.eth.contract(
                    address=self.contract_adress, abi=self.contract_abi)

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

                signed_txn = self.web3.eth.account.sign_transaction(
                    raw_tx, private_key=self.privkey)
                self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
                self.tx_hash = signed_txn.hash.hex()

                console.print(
                    logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ 1/1 ] [GAS ~ {:<6}][/] [yellow]Sent mint tx with {} gas[/]\n".format(self.name, self.gas, self.gas)), end="")

                Thread(target=self._wait_for_send_tx, daemon=True).start()

                return True

            except:

                console.print(
                    logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ 1/1 ] [GAS ~ {:<6}][/] [yellow]Error while sending mint tx, retrying...[/]\n".format(self.name, self.gas)), end="")

                i += 1
                

        return False

    def _cancel_transaction(self):

        i = 0

        while i < 10:

            try:
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

                signed_txn = self.web3.eth.account.sign_transaction(
                    raw_tx, private_key=self.privkey)
                self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
                self.tx_hash = signed_txn.hash.hex()

                console.print(
                    logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ 1/1 ] [GAS ~ {:<6}][/] [yellow]Sent cancelation tx with {} gas[/]\n".format(self.name, self.gas, self.gas + self.gas*0.2)), end="")

                Thread(target=self._wait_for_cancel_tx, daemon=True).start()

                return True

            except:

                console.print(
                    logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ 1/1 ] [GAS ~ {:<6}][/] [yellow]Error while sending cancel tx, retrying...[/]\n".format(self.name, self.gas)), end="")

                i += 1

        return False

    def _wait_for_send_tx(self):

        i = 0

        while i < 10:

            console.print(
                logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ 1/1 ] [GAS ~ {:<6}][/] [yellow]Waiting for tx confirmation...[/]\n".format(self.name, self.gas)), end="")

            try:

                receipt = self.web3.eth.wait_for_transaction_receipt(
                    self.tx_hash)

                if receipt["status"] == 1:

                    console.print(
                        logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ 1/1 ] [GAS ~ {:<6}][/] [green]Mint successful with tx: {}[/]\n".format(self.name, self.gas, self.tx_hash)), end="")

                    self._terminate = True

                else:

                    console.print(
                        logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ 1/1 ] [GAS ~ {:<6}][/] [red]Mint failed[/]\n".format(self.name, self.gas)), end="")

                    self._terminate = False

                return

            except:

                console.print(
                    logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ 1/1 ] [GAS ~ {:<6}][/] [yellow]Confirmation timed out, retrying...[/]\n".format(self.name, self.gas)), end="")

                i += 1

        self._terminate = False

    def _wait_for_cancel_tx(self):

        i = 0

        while i < 10:

            console.print(
                logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ 1/1 ] [GAS ~ {:<6}][/] [yellow]Waiting for tx cancelation...[/]\n".format(self.name, self.gas)), end="")

            try:

                receipt = self.web3.eth.wait_for_transaction_receipt(
                    self.tx_hash)

                if receipt["status"] == 1:

                    console.print(
                        logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ 1/1 ] [GAS ~ {:<6}][/] [green]Cancelation successful[/]\n".format(self.name, self.gas)), end="")

                else:

                    console.print(
                        logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ 1/1 ] [GAS ~ {:<6}][/] [red]Cancelation failed[/]\n".format(self.name, self.gas)), end="")

                self._terminate = False

                return

            except:

                console.print(
                    logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ 1/1 ] [GAS ~ {:<6}][/] [yellow]Cancelation timed out, retrying...[/]\n".format(self.name, self.gas)), end="")

                i += 1

        self._terminate = False

    def _monitor_task(self):

        try:

            with open('eth-wallets.csv', 'r') as f:

                reader = csv.DictReader(f)

                task_id = 1

                for wallet in reader:

                    if task_id == self.task:

                        if float(wallet["gas"]) > self.gas:

                            self.gas = float(wallet['gas'])

                            console.print(
                                logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ 1/1 ] [GAS ~ {:<6}][/] [yellow]Speeding up transaction...[/]\n".format(self.name, self.gas)), end="")

                            self._send_transaction()

                            return

                        if int(wallet["cancel"]) != self.cancel:

                            self.cancel = int(wallet['cancel'])

                            console.print(
                                logger("[BOT] [cyan][WALLET ~ {:<10}] [TASK ~ 1/1 ] [GAS ~ {:<6}][/] [yellow]Canceling transaction...[/]\n".format(self.name, self.gas)), end="")

                            self._cancel_transaction()

                            return

                    task_id += 1

        except:
            pass

        time.sleep(0.5)


if __name__ == "__main__":

    EthContract()
