"""Provides the `AccountClient` class."""

import base64
from dataclasses import dataclass
from base58 import b58encode
from typing import Any, Optional, Dict, List

from construct import Container
from solana.keypair import Keypair
from solana.system_program import create_account, CreateAccountParams
from solana.transaction import TransactionInstruction
from solana.publickey import PublicKey
from solana.rpc.types import MemcmpOpts

from anchorpy.coder.common import _account_size
from anchorpy.coder.accounts import (
    ACCOUNT_DISCRIMINATOR_SIZE,
    _account_discriminator,
)
from anchorpy.coder.coder import Coder
from anchorpy.error import AccountDoesNotExistError, AccountInvalidDiscriminator
from anchorpy.idl import Idl, _IdlTypeDef
from anchorpy.provider import Provider
from anchorpy.utils.rpc import get_multiple_accounts


def _build_account(
    idl: Idl,
    coder: Coder,
    program_id: PublicKey,
    provider: Provider,
) -> Dict[str, "AccountClient"]:
    """Generate the `.account` namespace.

    Args:
        idl: The parsed Idl object.
        coder: The program's coder object.
        program_id: The program ID.
        provider: The Provider instance.

    Returns:
        Mapping of account name to `AccountClient` instance.
    """
    accounts_fns = {}
    for idl_account in idl.accounts:
        account_client = AccountClient(idl, idl_account, coder, program_id, provider)
        accounts_fns[idl_account.name] = account_client
    return accounts_fns


@dataclass
class ProgramAccount:
    """Deserialized account owned by a program."""

    public_key: PublicKey
    account: Container


class AccountClient(object):
    """Provides methods for fetching and creating accounts."""

    def __init__(
        self,
        idl: Idl,
        idl_account: _IdlTypeDef,
        coder: Coder,
        program_id: PublicKey,
        provider: Provider,
    ):
        """Init.

        Args:
            idl: the parsed IDL object.
            idl_account: the account definition from the IDL.
            coder: The program's Coder object.
            program_id: the program ID.
            provider: The Provider object for the Program.
        """
        self._idl_account = idl_account
        self._program_id = program_id
        self._provider = provider
        self._coder = coder
        self._size = ACCOUNT_DISCRIMINATOR_SIZE + _account_size(idl, idl_account)

    async def fetch_custom(account, address: PublicKey) -> Container[Any]:
        """Return a deserialized account.

        Args:
            address: The address of the account to fetch.

        Raises:
            AccountDoesNotExistError: If the account doesn't exist.
            AccountInvalidDiscriminator: If the discriminator doesn't match the IDL.
        """
        account_info = await account._provider.connection.get_account_info(
            address,
            encoding="base64",
        )
        if not account_info["result"]["value"]:
            raise AccountDoesNotExistError(f"Account {address} does not exist")
        data = base64.b64decode(account_info["result"]["value"]["data"][0])
            
        return account._coder.accounts.decode(data)

    async def fetch_multiple(
        self, addresses: List[PublicKey], batch_size: int = 300
    ) -> list[Optional[Container[Any]]]:
        """Return multiple deserialized accounts.

        Accounts not found or with wrong discriminator are returned as None.

        Args:
            addresses: The addresses of the accounts to fetch.
            batch_size: The number of `getMultipleAccounts` objects to send
                in each HTTP request.
        """
        accounts = await get_multiple_accounts(
            self._provider.connection,
            addresses,
            batch_size=batch_size,
        )
        discriminator = _account_discriminator(self._idl_account.name)
        result: list[Optional[Container[Any]]] = []
        for account in accounts:
            if account is None:
                result.append(None)
            elif discriminator == account.account.data[:8]:
                result.append(self._coder.accounts.decode(account.account.data))
            else:
                result.append(None)
        return result

    async def create_instruction(
        self,
        signer: Keypair,
        size_override: int = 0,
    ) -> TransactionInstruction:
        """Return an instruction for creating this account.

        Args:
            signer: [description]
            size_override: Optional override for the account size. Defaults to 0.

        Returns:
            The instruction to create the account.
        """
        space = size_override if size_override else self._size
        mbre_resp = (
            await self._provider.connection.get_minimum_balance_for_rent_exemption(
                space
            )
        )
        return create_account(
            CreateAccountParams(
                from_pubkey=self._provider.wallet.public_key,
                new_account_pubkey=signer.public_key,
                space=space,
                lamports=mbre_resp["result"],
                program_id=self._program_id,
            )
        )

    async def all(
        self,
        buffer: Optional[bytes] = None,
        memcmp_opts: Optional[list[MemcmpOpts]] = None,
        data_size: Optional[int] = None,
    ) -> list[ProgramAccount]:
        """Return all instances of this account type for the program.

        Args:
            buffer: bytes filter to append to the discriminator.
            memcmp_opts: Options to compare a provided series of bytes with program
                account data at a particular offset.
            data_size: Option to compare the program account data length with the
                provided data size.
        """
        all_accounts = []
        discriminator = _account_discriminator(self._idl_account.name)
        to_encode = discriminator if buffer is None else discriminator + buffer
        bytes_arg = b58encode(to_encode).decode("ascii")
        base_memcmp_opt = MemcmpOpts(
            offset=0,
            bytes=bytes_arg,
        )
        extra_memcmpm_opts = [] if memcmp_opts is None else memcmp_opts
        full_memcmp_opts = [base_memcmp_opt] + extra_memcmpm_opts
        resp = await self._provider.connection.get_program_accounts(
            self._program_id,
            encoding="base64",
            commitment=self.provider.connection._commitment,  # noqa: WPS437
            data_size=data_size,
            memcmp_opts=full_memcmp_opts,
        )
        for r in resp["result"]:
            account_data = r["account"]["data"][0]
            account_data = base64.b64decode(account_data)
            all_accounts.append(
                ProgramAccount(
                    public_key=PublicKey(r["pubkey"]),
                    account=self._coder.accounts.decode(account_data),
                ),
            )
        return all_accounts

    @property
    def size(self) -> int:
        """Return the number of bytes in this account."""
        return self._size

    @property
    def program_id(self) -> PublicKey:
        """Return the program ID owning all accounts."""
        return self._program_id

    @property
    def provider(self) -> Provider:
        """Return the client's wallet and network provider."""
        return self._provider

    @property
    def coder(self) -> Coder:
        """Return the coder."""
        return self._coder
