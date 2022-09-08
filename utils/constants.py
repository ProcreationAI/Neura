import sys
from pathlib import Path


class Custom():
    
    FP_MONITOR_POLLING = 5

class SolanaEndpoints():
    
    MAINNET_RPC = "https://api.mainnet-beta.solana.com"
    DEVNET_RPC = "https://api.devnet.solana.com"
    
class Bot():
    
    VERSION = "0.21.3.0"
    USER_OS = sys.platform

class Discord():
    
    SUCCESS_WH = "https://discord.com/api/webhooks/997906580395786280/ZHbcYl0pjjf7yOpq0ExwOdsksrGj5LZQZ4mQckQ8hgqD1J3SdcViEz833TxOL2dxufgt"
    EMBED_COLOR = 0x6436CB
    EMBED_FOOTER_IMG = "https://cdn.discordapp.com/attachments/921022038074871879/981234960121856110/logo2.png"
    EMBED_FOOTER_TXT = "Neura - " + Bot.VERSION
    
class Keys():
    
    TLS_KEY = "oLZxFnte8n5UL6ERJqBjH7tJk37jVh503RP5IIt0"
    HELHEIM_API_KEY = ""
    OS_API_KEY = ""
    

class Paths():
    
    TLS_PATH = str(Path("bin/TLS").resolve()) if sys.platform == "darwin" else str(Path("bin/TLS.exe").resolve())
    NEURA_API_PATH = "https://neura-api.herokuapp.com/"
    
class SolanaPrograms():
    
    CMV2_PROGRAM = "cndy3Z4yapfJBmL3ShUp5exZKqR3z33thTzeNMm2gRZ"
    ME_PROGRAM = "CMZYPASGWeTz7RNGHaRJfCq2XQ5pYK6nDvVQxzkH51zb"
    LMN_PROGRAM = "ArAA6CZC123yMJLUe4uisBEgvfuw2WEvex9iFmFCYiXv"
    ML_PROGRAM = "minwAEdewYNqagUwzrVBUGWuo277eeSMwEwj76agxYd"
    BF_PROGRAM = "BFCMkgg9eFSv54HKJZFD5RMG8kNR5eMAEWnAtfRTPCjU"
    EA_PROGRAM = "EXBuYPNgBUXMTsjCbezENRUtFQzjUNZxvPGTd11Pznk5"

class EthereumContracts():
    
    OS_CONTRACT = ""
    
class IDLs():
    
    LMN_IDL = {
    "version": "0.1.0",
    "name": "nft_candy_machine",
    "instructions": [
        {
            "name": "bulkWithdraw",
            "accounts": [
                {
                    "name": "candyMachine",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "bulkOwner",
                    "isMut": True,
                    "isSigner": True
                },
                {
                    "name": "bulk",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "systemProgram",
                    "isMut": False,
                    "isSigner": False
                }
            ],
            "args": []
        },
        {
            "name": "mintBulk",
            "accounts": [
                {
                    "name": "candyMachine",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "receiver",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "payer",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "wallet",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "wallet2",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "metadata",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "mint",
                    "isMut": True,
                    "isSigner": True
                },
                {
                    "name": "associated",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "masterEdition",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "totalMints",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "associatedTokenProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "tokenMetadataProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "tokenProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "systemProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "rent",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "clock",
                    "isMut": False,
                    "isSigner": False
                }
            ],
            "args": [
                {
                    "name": "proof",
                    "type": {
                        "option": {
                            "vec": {
                                "array": [
                                    "u8",
                                    32
                                ]
                            }
                        }
                    }
                },
                {
                    "name": "expect",
                    "type": "u64"
                }
            ]
        },
        {
            "name": "mintEmbed",
            "accounts": [
                {
                    "name": "candyMachine",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "payer",
                    "isMut": True,
                    "isSigner": True
                },
                {
                    "name": "wallet",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "wallet2",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "metadata",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "mint",
                    "isMut": True,
                    "isSigner": True
                },
                {
                    "name": "associated",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "masterEdition",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "totalMints",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "associatedTokenProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "tokenMetadataProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "tokenProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "systemProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "rent",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "clock",
                    "isMut": False,
                    "isSigner": False
                }
            ],
            "args": [
                {
                    "name": "proof",
                    "type": {
                        "option": {
                            "vec": {
                                "array": [
                                    "u8",
                                    32
                                ]
                            }
                        }
                    }
                },
                {
                    "name": "expect",
                    "type": "u64"
                }
            ]
        },
        {
            "name": "mintEe",
            "accounts": [
                {
                    "name": "candyMachine",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "payer",
                    "isMut": True,
                    "isSigner": True
                },
                {
                    "name": "wallet",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "wallet2",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "metadata",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "mint",
                    "isMut": True,
                    "isSigner": True
                },
                {
                    "name": "associated",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "masterEdition",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "totalMints",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "associatedTokenProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "tokenMetadataProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "tokenProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "systemProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "rent",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "clock",
                    "isMut": False,
                    "isSigner": False
                }
            ],
            "args": [
                {
                    "name": "proof",
                    "type": {
                        "option": {
                            "vec": {
                                "array": [
                                    "u8",
                                    32
                                ]
                            }
                        }
                    }
                },
                {
                    "name": "expect",
                    "type": "u64"
                }
            ]
        },
        {
            "name": "mintV4",
            "accounts": [
                {
                    "name": "candyMachine",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "payer",
                    "isMut": True,
                    "isSigner": True
                },
                {
                    "name": "wallet",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "wallet2",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "metadata",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "mint",
                    "isMut": True,
                    "isSigner": True
                },
                {
                    "name": "associated",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "masterEdition",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "totalMints",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "associatedTokenProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "tokenMetadataProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "tokenProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "systemProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "rent",
                    "isMut": False,
                    "isSigner": False
                }
            ],
            "args": [
                {
                    "name": "proof",
                    "type": {
                        "vec": {
                            "array": [
                                "u8",
                                32
                            ]
                        }
                    }
                },
                {
                    "name": "expect",
                    "type": "u64"
                }
            ]
        },
        {
            "name": "mintV2",
            "accounts": [
                {
                    "name": "candyMachine",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "payer",
                    "isMut": True,
                    "isSigner": True
                },
                {
                    "name": "candyMachineCreator",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "wallet",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "wallet2",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "metadata",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "mint",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "masterEdition",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "totalMints",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "tokenMetadataProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "tokenProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "systemProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "rent",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "clock",
                    "isMut": False,
                    "isSigner": False
                }
            ],
            "args": [
                {
                    "name": "creatorBump",
                    "type": "u8"
                },
                {
                    "name": "totalMintsBump",
                    "type": "u8"
                },
                {
                    "name": "proof",
                    "type": {
                        "option": {
                            "vec": {
                                "array": [
                                    "u8",
                                    32
                                ]
                            }
                        }
                    }
                }
            ]
        },
        {
            "name": "editCmV2",
            "accounts": [
                {
                    "name": "authority",
                    "isMut": False,
                    "isSigner": True
                },
                {
                    "name": "candyMachine",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "clock",
                    "isMut": False,
                    "isSigner": False
                }
            ],
            "args": [
                {
                    "name": "data",
                    "type": {
                        "defined": "CandyMachineDataV2"
                    }
                }
            ]
        },
        {
            "name": "editCmV3",
            "accounts": [
                {
                    "name": "authority",
                    "isMut": False,
                    "isSigner": True
                },
                {
                    "name": "candyMachine",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "clock",
                    "isMut": False,
                    "isSigner": False
                }
            ],
            "args": [
                {
                    "name": "data",
                    "type": {
                        "defined": "CandyMachineDataV2"
                    }
                }
            ]
        },
        {
            "name": "editCmV4",
            "accounts": [
                {
                    "name": "authority",
                    "isMut": False,
                    "isSigner": True
                },
                {
                    "name": "candyMachine",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "clock",
                    "isMut": False,
                    "isSigner": False
                }
            ],
            "args": [
                {
                    "name": "data",
                    "type": {
                        "defined": "CandyMachineDataV2"
                    }
                }
            ]
        },
        {
            "name": "reveal",
            "accounts": [
                {
                    "name": "candyMachine",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "metadata",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "tokenMetadataProgram",
                    "isMut": False,
                    "isSigner": False
                }
            ],
            "args": []
        },
        {
            "name": "allowUnfreeze",
            "accounts": [
                {
                    "name": "authority",
                    "isMut": False,
                    "isSigner": True
                },
                {
                    "name": "candyMachine",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "clock",
                    "isMut": False,
                    "isSigner": False
                }
            ],
            "args": []
        },
        {
            "name": "allowReveal",
            "accounts": [
                {
                    "name": "authority",
                    "isMut": False,
                    "isSigner": True
                },
                {
                    "name": "candyMachine",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "clock",
                    "isMut": False,
                    "isSigner": False
                }
            ],
            "args": [
                {
                    "name": "newUri",
                    "type": "string"
                }
            ]
        },
        {
            "name": "burnSupply",
            "accounts": [
                {
                    "name": "authority",
                    "isMut": False,
                    "isSigner": True
                },
                {
                    "name": "candyMachine",
                    "isMut": True,
                    "isSigner": False
                }
            ],
            "args": [
                {
                    "name": "percentToBurn",
                    "type": "u8"
                }
            ]
        },
        {
            "name": "burnSupplyV2",
            "accounts": [
                {
                    "name": "authority",
                    "isMut": False,
                    "isSigner": True
                },
                {
                    "name": "candyMachine",
                    "isMut": True,
                    "isSigner": False
                }
            ],
            "args": [
                {
                    "name": "percentToBurn",
                    "type": "u8"
                }
            ]
        },
        {
            "name": "burnSupplyV3",
            "accounts": [
                {
                    "name": "authority",
                    "isMut": False,
                    "isSigner": True
                },
                {
                    "name": "candyMachine",
                    "isMut": True,
                    "isSigner": False
                }
            ],
            "args": [
                {
                    "name": "percentToBurn",
                    "type": "u8"
                }
            ]
        },
        {
            "name": "thaw",
            "accounts": [
                {
                    "name": "candyMachine",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "mint",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "associated",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "metadata",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "masterEdition",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "tokenMetadataProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "tokenProgram",
                    "isMut": False,
                    "isSigner": False
                }
            ],
            "args": []
        },
        {
            "name": "initCmV4",
            "accounts": [
                {
                    "name": "candyMachine",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "wallet",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "authority",
                    "isMut": False,
                    "isSigner": True
                },
                {
                    "name": "payer",
                    "isMut": True,
                    "isSigner": True
                },
                {
                    "name": "systemProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "rent",
                    "isMut": False,
                    "isSigner": False
                }
            ],
            "args": [
                {
                    "name": "data",
                    "type": {
                        "defined": "CandyMachineDataV2"
                    }
                },
                {
                    "name": "seed",
                    "type": "publicKey"
                },
                {
                    "name": "thawDate",
                    "type": {
                        "option": "i64"
                    }
                }
            ]
        },
        {
            "name": "initCmV3",
            "accounts": [
                {
                    "name": "candyMachine",
                    "isMut": True,
                    "isSigner": False
                },
                {
                    "name": "wallet",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "authority",
                    "isMut": False,
                    "isSigner": True
                },
                {
                    "name": "payer",
                    "isMut": True,
                    "isSigner": True
                },
                {
                    "name": "systemProgram",
                    "isMut": False,
                    "isSigner": False
                },
                {
                    "name": "rent",
                    "isMut": False,
                    "isSigner": False
                }
            ],
            "args": [
                {
                    "name": "data",
                    "type": {
                        "defined": "CandyMachineDataV2"
                    }
                },
                {
                    "name": "seed",
                    "type": "publicKey"
                }
            ]
        },
        {
            "name": "setWhitelist",
            "accounts": [
                {
                    "name": "authority",
                    "isMut": False,
                    "isSigner": True
                },
                {
                    "name": "candyMachine",
                    "isMut": True,
                    "isSigner": False
                }
            ],
            "args": [
                {
                    "name": "wl",
                    "type": {
                        "option": {
                            "defined": "WhitelistV2"
                        }
                    }
                }
            ]
        }
    ],
    "accounts": [
        {
            "name": "Whitelist",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "authority",
                        "type": "publicKey"
                    },
                    {
                        "name": "candyMachine",
                        "type": "publicKey"
                    },
                    {
                        "name": "merkleRoot",
                        "type": {
                            "option": {
                                "array": [
                                    "u8",
                                    32
                                ]
                            }
                        }
                    }
                ]
            }
        },
        {
            "name": "CandyMachine",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "authority",
                        "type": "publicKey"
                    },
                    {
                        "name": "wallet",
                        "type": "publicKey"
                    },
                    {
                        "name": "tokenMint",
                        "type": {
                            "option": "publicKey"
                        }
                    },
                    {
                        "name": "config",
                        "type": "publicKey"
                    },
                    {
                        "name": "data",
                        "type": {
                            "defined": "CandyMachineData"
                        }
                    },
                    {
                        "name": "itemsRedeemed",
                        "type": "u64"
                    },
                    {
                        "name": "bump",
                        "type": "u8"
                    }
                ]
            }
        },
        {
            "name": "CandyMachineV2",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "authority",
                        "type": "publicKey"
                    },
                    {
                        "name": "wallet",
                        "type": "publicKey"
                    },
                    {
                        "name": "itemsRedeemed",
                        "type": "u64"
                    },
                    {
                        "name": "data",
                        "type": {
                            "defined": "CandyMachineDataV2"
                        }
                    }
                ]
            }
        },
        {
            "name": "CandyMachineV3",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "seed",
                        "type": "publicKey"
                    },
                    {
                        "name": "bump",
                        "type": "u8"
                    },
                    {
                        "name": "authority",
                        "type": "publicKey"
                    },
                    {
                        "name": "wallet",
                        "type": "publicKey"
                    },
                    {
                        "name": "itemsRedeemed",
                        "type": "u64"
                    },
                    {
                        "name": "data",
                        "type": {
                            "defined": "CandyMachineDataV2"
                        }
                    }
                ]
            }
        },
        {
            "name": "CandyMachineV4",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "seed",
                        "type": "publicKey"
                    },
                    {
                        "name": "bump",
                        "type": "u8"
                    },
                    {
                        "name": "authority",
                        "type": "publicKey"
                    },
                    {
                        "name": "wallet",
                        "type": "publicKey"
                    },
                    {
                        "name": "itemsRedeemed",
                        "type": "u64"
                    },
                    {
                        "name": "data",
                        "type": {
                            "defined": "CandyMachineDataV2"
                        }
                    },
                    {
                        "name": "thawDate",
                        "type": {
                            "option": "i64"
                        }
                    },
                    {
                        "name": "allowThaw",
                        "type": "bool"
                    },
                    {
                        "name": "revealedUri",
                        "type": {
                            "option": "string"
                        }
                    }
                ]
            }
        },
        {
            "name": "TotalMints",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "total",
                        "type": "u32"
                    }
                ]
            }
        }
    ],
    "types": [
        {
            "name": "CandyMachineDataV2",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "price",
                        "type": "u64"
                    },
                    {
                        "name": "itemsAvailable",
                        "type": "u64"
                    },
                    {
                        "name": "goLiveDate",
                        "type": "i64"
                    },
                    {
                        "name": "symbol",
                        "type": "string"
                    },
                    {
                        "name": "sellerFeeBasisPoints",
                        "type": "u16"
                    },
                    {
                        "name": "creators",
                        "type": {
                            "vec": {
                                "defined": "Creator"
                            }
                        }
                    },
                    {
                        "name": "isMutable",
                        "type": "bool"
                    },
                    {
                        "name": "retainAuthority",
                        "type": "bool"
                    },
                    {
                        "name": "baseUrl",
                        "type": "string"
                    },
                    {
                        "name": "mintsPerUser",
                        "type": {
                            "option": "u32"
                        }
                    },
                    {
                        "name": "whitelist",
                        "type": {
                            "option": {
                                "defined": "WhitelistV2"
                            }
                        }
                    }
                ]
            }
        },
        {
            "name": "WhitelistV2",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "merkleRoot",
                        "type": {
                            "array": [
                                "u8",
                                32
                            ]
                        }
                    },
                    {
                        "name": "mintsPerUser",
                        "type": {
                            "option": "u32"
                        }
                    },
                    {
                        "name": "goLiveDate",
                        "type": "i64"
                    },
                    {
                        "name": "price",
                        "type": {
                            "option": "u64"
                        }
                    }
                ]
            }
        },
        {
            "name": "CandyMachineData",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "uuid",
                        "type": "string"
                    },
                    {
                        "name": "price",
                        "type": "u64"
                    },
                    {
                        "name": "itemsAvailable",
                        "type": "u64"
                    },
                    {
                        "name": "goLiveDate",
                        "type": {
                            "option": "i64"
                        }
                    }
                ]
            }
        },
        {
            "name": "Creator",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "address",
                        "type": "publicKey"
                    },
                    {
                        "name": "verified",
                        "type": "bool"
                    },
                    {
                        "name": "share",
                        "type": "u8"
                    }
                ]
            }
        },
        {
            "name": "ErrorCode",
            "type": {
                "kind": "enum",
                "variants": [
                    {
                        "name": "IncorrectOwner"
                    },
                    {
                        "name": "Uninitialized"
                    },
                    {
                        "name": "MintMismatch"
                    },
                    {
                        "name": "IndexGreaterThanLength"
                    },
                    {
                        "name": "ConfigMustHaveAtleastOneEntry"
                    },
                    {
                        "name": "NumericalOverflowError"
                    },
                    {
                        "name": "TooManyCreators"
                    },
                    {
                        "name": "UuidMustBeExactly6Length"
                    },
                    {
                        "name": "NotEnoughTokens"
                    },
                    {
                        "name": "NotEnoughSOL"
                    },
                    {
                        "name": "TokenTransferFailed"
                    },
                    {
                        "name": "CandyMachineEmpty"
                    },
                    {
                        "name": "CandyMachineNotLiveYet"
                    },
                    {
                        "name": "ConfigLineMismatch"
                    },
                    {
                        "name": "WhitelistExists"
                    },
                    {
                        "name": "WhiteListMissing"
                    },
                    {
                        "name": "WrongWhitelist"
                    },
                    {
                        "name": "NotWhitelisted"
                    },
                    {
                        "name": "InvalidFraction"
                    },
                    {
                        "name": "BumpMissing"
                    },
                    {
                        "name": "PriceViolation"
                    },
                    {
                        "name": "NotThawable"
                    }
                ]
            }
        }
    ]
}
    
    
    