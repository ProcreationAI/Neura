from web3 import Web3
import json
from web3.types import Wei
from web3.contract import Contract
import requests

from utils.bypass import create_tls_payload
from utils.constants import *

class OpenSea():

    def __init__(self, rpc: str, privkey: str):
        
        self.client = Web3(Web3.HTTPProvider(rpc))

        self.privkey = privkey
        self.pubkey = self.client.eth.account.privateKeyToAccount(privkey).address

        self.gas_fee = 0

    @staticmethod
    def _get_collection_contract(symbol) -> str | None:
        
        try:
            
            res = requests.get(f"https://api.opensea.io/collection/{symbol}?search[sortAscending]=true&search[sortBy]=PRICE&search[toggles][0]=BUY_NOW").json()

            return res["collection"]["primary_asset_contracts"][0]["address"]
        
        except:
            
            return None
    
    @staticmethod
    def get_listed_nfts(symbol: str, min_eth: int | float, max_eth: int | float, filters: list = None) -> list | None:

        params = {
            "id": "AssetSearchQuery",
            "query": "query AssetSearchQuery(\n  $categories: [CollectionSlug!]\n  $chains: [ChainScalar!]\n  $collection: CollectionSlug\n  $collectionQuery: String\n  $collectionSortBy: CollectionSort\n  $collections: [CollectionSlug!]\n  $count: Int\n  $cursor: String\n  $identity: IdentityInputType\n  $includeHiddenCollections: Boolean\n  $numericTraits: [TraitRangeType!]\n  $paymentAssets: [PaymentAssetSymbol!]\n  $priceFilter: PriceFilterType\n  $query: String\n  $resultModel: SearchResultModel\n  $showContextMenu: Boolean = false\n  $shouldShowQuantity: Boolean = false\n  $sortAscending: Boolean\n  $sortBy: SearchSortBy\n  $stringTraits: [TraitInputType!]\n  $toggles: [SearchToggle!]\n  $creator: IdentityInputType\n  $assetOwner: IdentityInputType\n  $isPrivate: Boolean\n  $safelistRequestStatuses: [SafelistRequestStatus!]\n) {\n  query {\n    ...AssetSearch_data_2hBjZ1\n  }\n}\n\nfragment AssetCardAnnotations_assetBundle on AssetBundleType {\n  assetCount\n}\n\nfragment AssetCardAnnotations_asset_3Aax2O on AssetType {\n  assetContract {\n    chain\n    id\n  }\n  decimals\n  ownedQuantity(identity: $identity) @include(if: $shouldShowQuantity)\n  relayId\n  favoritesCount\n  isDelisted\n  isFavorite\n  isFrozen\n  hasUnlockableContent\n  ...AssetCardBuyNow_data\n  orderData {\n    bestAsk {\n      orderType\n      relayId\n      maker {\n        address\n        id\n      }\n    }\n  }\n  ...AssetContextMenu_data_3z4lq0 @include(if: $showContextMenu)\n}\n\nfragment AssetCardBuyNow_data on AssetType {\n  tokenId\n  relayId\n  assetContract {\n    address\n    chain\n    id\n  }\n  collection {\n    slug\n    id\n  }\n  orderData {\n    bestAsk {\n      relayId\n      decimals\n      paymentAssetQuantity {\n        asset {\n          usdSpotPrice\n          decimals\n          id\n        }\n        quantity\n        id\n      }\n    }\n  }\n}\n\nfragment AssetCardContent_asset on AssetType {\n  relayId\n  name\n  ...AssetMedia_asset\n  assetContract {\n    address\n    chain\n    openseaVersion\n    id\n  }\n  tokenId\n  collection {\n    slug\n    id\n  }\n  isDelisted\n}\n\nfragment AssetCardContent_assetBundle on AssetBundleType {\n  assetQuantities(first: 18) {\n    edges {\n      node {\n        asset {\n          relayId\n          ...AssetMedia_asset\n          id\n        }\n        id\n      }\n    }\n  }\n}\n\nfragment AssetCardFooter_assetBundle on AssetBundleType {\n  ...AssetCardAnnotations_assetBundle\n  name\n  assetCount\n  assetQuantities(first: 18) {\n    edges {\n      node {\n        asset {\n          collection {\n            name\n            relayId\n            slug\n            isVerified\n            ...collection_url\n            id\n          }\n          id\n        }\n        id\n      }\n    }\n  }\n  assetEventData {\n    lastSale {\n      unitPriceQuantity {\n        ...AssetQuantity_data\n        id\n      }\n    }\n  }\n  orderData {\n    bestBid {\n      orderType\n      paymentAssetQuantity {\n        quantity\n        ...AssetQuantity_data\n        id\n      }\n    }\n    bestAsk {\n      maker {\n        address\n        id\n      }\n      closedAt\n      orderType\n      dutchAuctionFinalPrice\n      openedAt\n      priceFnEndedAt\n      quantity\n      decimals\n      paymentAssetQuantity {\n        quantity\n        ...AssetQuantity_data\n        id\n      }\n    }\n  }\n}\n\nfragment AssetCardFooter_asset_3Aax2O on AssetType {\n  ...AssetCardAnnotations_asset_3Aax2O\n  name\n  tokenId\n  collection {\n    slug\n    name\n    isVerified\n    ...collection_url\n    id\n  }\n  isDelisted\n  assetContract {\n    address\n    chain\n    openseaVersion\n    id\n  }\n  assetEventData {\n    lastSale {\n      unitPriceQuantity {\n        ...AssetQuantity_data\n        id\n      }\n    }\n  }\n  orderData {\n    bestBid {\n      orderType\n      paymentAssetQuantity {\n        quantity\n        ...AssetQuantity_data\n        id\n      }\n    }\n    bestAsk {\n      maker {\n        address\n        id\n      }\n      closedAt\n      orderType\n      dutchAuctionFinalPrice\n      openedAt\n      priceFnEndedAt\n      quantity\n      decimals\n      paymentAssetQuantity {\n        quantity\n        ...AssetQuantity_data\n        id\n      }\n    }\n  }\n}\n\nfragment AssetContextMenu_data_3z4lq0 on AssetType {\n  ...asset_edit_url\n  ...asset_url\n  ...itemEvents_data\n  relayId\n  isDelisted\n  isEditable {\n    value\n    reason\n  }\n  isListable\n  ownership(identity: {}) {\n    isPrivate\n    quantity\n  }\n  creator {\n    address\n    id\n  }\n  collection {\n    isAuthorizedEditor\n    id\n  }\n  imageUrl\n  ownedQuantity(identity: {})\n}\n\nfragment AssetMedia_asset on AssetType {\n  animationUrl\n  backgroundColor\n  collection {\n    displayData {\n      cardDisplayStyle\n    }\n    id\n  }\n  isDelisted\n  imageUrl\n  displayImageUrl\n}\n\nfragment AssetQuantity_data on AssetQuantityType {\n  asset {\n    ...Price_data\n    id\n  }\n  quantity\n}\n\nfragment AssetSearchFilter_data_3KTzFc on Query {\n  ...CollectionFilter_data_2qccfC\n  collection(collection: $collection) {\n    numericTraits {\n      key\n      value {\n        max\n        min\n      }\n      ...NumericTraitFilter_data\n    }\n    stringTraits {\n      key\n      ...StringTraitFilter_data\n    }\n    defaultChain {\n      identifier\n    }\n    id\n  }\n  ...PaymentFilter_data_2YoIWt\n}\n\nfragment AssetSearchList_data_3Aax2O on SearchResultType {\n  asset {\n    assetContract {\n      address\n      chain\n      id\n    }\n    collection {\n      isVerified\n      relayId\n      id\n    }\n    relayId\n    tokenId\n    ...AssetSelectionItem_data\n    ...asset_url\n    id\n  }\n  assetBundle {\n    relayId\n    id\n  }\n  ...Asset_data_3Aax2O\n}\n\nfragment AssetSearch_data_2hBjZ1 on Query {\n  ...AssetSearchFilter_data_3KTzFc\n  ...SearchPills_data_2Kg4Sq\n  search(after: $cursor, chains: $chains, categories: $categories, collections: $collections, first: $count, identity: $identity, numericTraits: $numericTraits, paymentAssets: $paymentAssets, priceFilter: $priceFilter, querystring: $query, resultType: $resultModel, sortAscending: $sortAscending, sortBy: $sortBy, stringTraits: $stringTraits, toggles: $toggles, creator: $creator, isPrivate: $isPrivate, safelistRequestStatuses: $safelistRequestStatuses) {\n    edges {\n      node {\n        ...AssetSearchList_data_3Aax2O\n        __typename\n      }\n      cursor\n    }\n    totalCount\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n}\n\nfragment AssetSelectionItem_data on AssetType {\n  backgroundColor\n  collection {\n    displayData {\n      cardDisplayStyle\n    }\n    imageUrl\n    id\n  }\n  imageUrl\n  name\n  relayId\n}\n\nfragment Asset_data_3Aax2O on SearchResultType {\n  asset {\n    relayId\n    isDelisted\n    ...AssetCardContent_asset\n    ...AssetCardFooter_asset_3Aax2O\n    ...AssetMedia_asset\n    ...asset_url\n    ...itemEvents_data\n    orderData {\n      bestAsk {\n        paymentAssetQuantity {\n          quantityInEth\n          id\n        }\n      }\n    }\n    id\n  }\n  assetBundle {\n    relayId\n    ...bundle_url\n    ...AssetCardContent_assetBundle\n    ...AssetCardFooter_assetBundle\n    orderData {\n      bestAsk {\n        paymentAssetQuantity {\n          quantityInEth\n          id\n        }\n      }\n    }\n    id\n  }\n}\n\nfragment CollectionFilter_data_2qccfC on Query {\n  selectedCollections: collections(first: 25, collections: $collections, includeHidden: true) {\n    edges {\n      node {\n        assetCount\n        imageUrl\n        name\n        slug\n        isVerified\n        id\n      }\n    }\n  }\n  collections(assetOwner: $assetOwner, assetCreator: $creator, onlyPrivateAssets: $isPrivate, chains: $chains, first: 100, includeHidden: $includeHiddenCollections, parents: $categories, query: $collectionQuery, sortBy: $collectionSortBy) {\n    edges {\n      node {\n        assetCount\n        imageUrl\n        name\n        slug\n        isVerified\n        id\n        __typename\n      }\n      cursor\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n}\n\nfragment CollectionModalContent_data on CollectionType {\n  description\n  imageUrl\n  name\n  slug\n}\n\nfragment NumericTraitFilter_data on NumericTraitTypePair {\n  key\n  value {\n    max\n    min\n  }\n}\n\nfragment PaymentFilter_data_2YoIWt on Query {\n  paymentAssets(first: 10) {\n    edges {\n      node {\n        symbol\n        relayId\n        id\n        __typename\n      }\n      cursor\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n  PaymentFilter_collection: collection(collection: $collection) {\n    paymentAssets {\n      symbol\n      relayId\n      id\n    }\n    id\n  }\n}\n\nfragment Price_data on AssetType {\n  decimals\n  imageUrl\n  symbol\n  usdSpotPrice\n  assetContract {\n    blockExplorerLink\n    chain\n    id\n  }\n}\n\nfragment SearchPills_data_2Kg4Sq on Query {\n  selectedCollections: collections(first: 25, collections: $collections, includeHidden: true) {\n    edges {\n      node {\n        imageUrl\n        name\n        slug\n        ...CollectionModalContent_data\n        id\n      }\n    }\n  }\n}\n\nfragment StringTraitFilter_data on StringTraitType {\n  counts {\n    count\n    value\n  }\n  key\n}\n\nfragment asset_edit_url on AssetType {\n  assetContract {\n    address\n    chain\n    id\n  }\n  tokenId\n  collection {\n    slug\n    id\n  }\n}\n\nfragment asset_url on AssetType {\n  assetContract {\n    address\n    chain\n    id\n  }\n  tokenId\n}\n\nfragment bundle_url on AssetBundleType {\n  slug\n}\n\nfragment collection_url on CollectionType {\n  slug\n}\n\nfragment itemEvents_data on AssetType {\n  assetContract {\n    address\n    chain\n    id\n  }\n  tokenId\n}\n",
            "variables": {
                "categories": None,
                "chains": None,
                "collection": symbol,
                "collectionQuery": None,
                "collectionSortBy": "SEVEN_DAY_VOLUME",
                "collections": [symbol],
                "count": 1,
                "cursor": None,
                "identity": None,
                "includeHiddenCollections": None,
                "numericTraits": None,
                "paymentAssets": None,
                "priceFilter": {
                    "symbol": "ETH",
                    "max": max_eth,
                    "min": min_eth
                },
                "query": "",
                "resultModel": "ASSETS",
                "showContextMenu": True,
                "shouldShowQuantity": False,
                "sortAscending": False,
                "sortBy": "LISTING_DATE",
                "stringTraits": filters,
                "toggles": ["BUY_NOW"],
                "creator": None,
                "assetOwner": None,
                "isPrivate": None,
                "safelistRequestStatuses": None
            }
        }
        
        headers = {
            'authority': 'api.opensea.io',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
            'content-type': 'application/json',
            'accept': '*/*',
            'x-signed-query': '68a9ee13e282478180ad3d72fc295ebe41c5c449f0621e2ab51a7c43fd811fde',
            'x-api-key': '2f6f419a083c46de9d83ce3dbe7db601',
            'sec-ch-ua-platform': '"macOS"',
            'origin': 'https://opensea.io',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://opensea.io/',
            'accept-language': 'es-ES,es;q=0.9',
        }
        
        try:

            payload = create_tls_payload(
                url="https://api.opensea.io/graphql/",
                method="POST",
                headers=headers,
                params=params
            )
            
            res = requests.post(
                "http://127.0.0.1:3000",
                json=payload,
                timeout=3
            ).json()
            
            if res["statusCode"] == 200:
                
                res = json.loads(res["body"])
                
                if res["data"]["query"]["search"]["edges"]:

                    return res["data"]["query"]["search"]["edges"]

        except:

            pass

        return None

    def buy_nft(self, symbol: str, token_id: str, price: int) -> str | None:

        am_data = self._get_atomic_match(symbol, token_id)

        if not am_data:

            return None
        
        am_data[0] = [self.client.toChecksumAddress(i) for i in am_data[0]]
        am_data[1] = [int(i) for i in am_data[1]]

        contract = self._get_contract_details()
        
        if not contract:

            return None

        contract_encoded = self._get_contract_fn(contract, am_data)
        
        if not contract_encoded:

            return None

        transaction_params = {
            "nonce": self.client.eth.getTransactionCount(self.pubkey),
            "to": EthereumContracts.OS_CONTRACT,
            "value": Wei(price),
            "data": contract_encoded,
            "chainId": self.client.eth.chain_id,
            'from': self.pubkey
        }
        
        gas_limit = self._estimate_gas(tx_params=transaction_params)
        
        transaction_params["gas"] = gas_limit
        transaction_params["maxFeePerGas"] = self.client.toWei(self.gas_fee, 'gwei')
        transaction_params["maxPriorityFeePerGas"] = self.client.toWei(self.gas_fee, 'gwei')
        
        try:
            
            signed_transaction = self.client.eth.account.sign_transaction(transaction_params, self.privkey)

            tx_hash = self.client.eth.send_raw_transaction(signed_transaction.rawTransaction)

            return tx_hash
        
        except:
                        
            return None
        

    def _get_contract_details(self) -> Contract | None:

        try:

            contract_abi = requests.get(
                f"http://api.etherscan.io/api?module=contract&action=getabi&address={EthereumContracts.OS_CONTRACT}&format=raw&apikey=GZNB2MR1UP4J1R8R3FIQMVKTYW5S9RTSTP").json()

            contract = self.client.eth.contract(EthereumContracts.OS_CONTRACT, abi=contract_abi)

            return contract

        except:

            return None

    @staticmethod
    def _get_contract_fn(contract: Contract, args):

        try:
            
            return contract.encodeABI(fn_name="atomicMatch_", args=args)

        except:
            
            return None

    def _estimate_gas(self, tx_params: dict):
        
        while True:
            
            try:
                
                estimated_gas = self.client.eth.estimate_gas(transaction=tx_params)

                return estimated_gas

            except ValueError as e:
                
                if 'insufficient funds' in str(e):
                    
                    return None
                
                else:
                    
                    return 150000

    
    def _get_atomic_match(self, symbol: str, token_id: int) -> str | None:

        try:
            
            contract = self.client.toChecksumAddress(self._get_collection_contract(symbol=symbol))
            
            payload = {
                'asset_contract_address': contract,
                'token_id': token_id,
                'buyer':  self.pubkey
            }

            headers = {
                "api-key": Keys.OS_API_KEY
            }

            res = requests.post(
                "https://valkyriesolution.herokuapp.com/api/atomicmatch",
                json=payload,
                headers=headers
            )

            if res.status_code == 200:

                return json.loads(res.text)

        except:

            pass

        return None


if __name__ == "__main__":
    
    OpenSea()