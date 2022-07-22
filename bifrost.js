(self.webpackChunk_N_E = self.webpackChunk_N_E || []).push([[775], {
    6355: function(e, t, n) {
        (window.__NEXT_P = window.__NEXT_P || []).push(["/mint/[projectSlug]", function() {
            return n(81519)
        }
        ])
    },
    81519: function(e, t, n) {
        "use strict";
        n.r(t),
        n.d(t, {
            default: function() {
                return We
            }
        });
        var i = n(34051)
          , a = n.n(i)
          , s = n(85893)
          , r = n(11163)
          , c = n(33299)
          , o = n(59917)
          , l = n(18077)
          , u = (new o.PublicKey("gravk12G8FF5eaXaXSe4VEC8BhkxQ7ig5AHdeVdPmDF"),
        new o.PublicKey("TBondmkCYxaPCKG4CHYfVTcwQ8on31xnJrPzk8F8WsS"),
        new o.PublicKey("FoRGERiW7odcCBGU1bztZi16osPBHjxharvDathL5eds"),
        new o.PublicKey("HEiMicL2q6G6SQqpHek4xyMXs1jzPCDC71ZwxZLXx43i"))
          , d = new o.PublicKey("BFMGKvziBENLDdpFs3y75d9myFYF9ZqhTyxqet9ohB4N")
          , m = new o.PublicKey("BFCMkgg9eFSv54HKJZFD5RMG8kNR5eMAEWnAtfRTPCjU")
          , p = (new o.PublicKey("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"),
        {
            version: "4.0.0",
            name: "candy_machine",
            instructions: [{
                name: "initializeCandyMachine",
                accounts: [{
                    name: "candyMachine",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "wallet",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "authority",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "payer",
                    isMut: !1,
                    isSigner: !0
                }, {
                    name: "systemProgram",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "rent",
                    isMut: !1,
                    isSigner: !1
                }],
                args: [{
                    name: "data",
                    type: {
                        defined: "CandyMachineData"
                    }
                }]
            }, {
                name: "updateCandyMachine",
                accounts: [{
                    name: "candyMachine",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "authority",
                    isMut: !1,
                    isSigner: !0
                }, {
                    name: "wallet",
                    isMut: !1,
                    isSigner: !1
                }],
                args: [{
                    name: "data",
                    type: {
                        defined: "CandyMachineData"
                    }
                }]
            }, {
                name: "updateAuthority",
                accounts: [{
                    name: "candyMachine",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "authority",
                    isMut: !1,
                    isSigner: !0
                }, {
                    name: "wallet",
                    isMut: !1,
                    isSigner: !1
                }],
                args: [{
                    name: "newAuthority",
                    type: {
                        option: "publicKey"
                    }
                }]
            }, {
                name: "addConfigLines",
                accounts: [{
                    name: "candyMachine",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "authority",
                    isMut: !1,
                    isSigner: !0
                }],
                args: [{
                    name: "index",
                    type: "u32"
                }, {
                    name: "configLines",
                    type: {
                        vec: {
                            defined: "ConfigLine"
                        }
                    }
                }]
            }, {
                name: "setCollection",
                accounts: [{
                    name: "candyMachine",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "authority",
                    isMut: !1,
                    isSigner: !0
                }, {
                    name: "collectionPda",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "payer",
                    isMut: !1,
                    isSigner: !0
                }, {
                    name: "systemProgram",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "rent",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "metadata",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "mint",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "edition",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "collectionAuthorityRecord",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "tokenMetadataProgram",
                    isMut: !1,
                    isSigner: !1
                }],
                args: []
            }, {
                name: "removeCollection",
                accounts: [{
                    name: "candyMachine",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "authority",
                    isMut: !1,
                    isSigner: !0
                }, {
                    name: "collectionPda",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "metadata",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "mint",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "collectionAuthorityRecord",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "tokenMetadataProgram",
                    isMut: !1,
                    isSigner: !1
                }],
                args: []
            }, {
                name: "mintNft",
                accounts: [{
                    name: "candyMachine",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "candyMachineCreator",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "payer",
                    isMut: !1,
                    isSigner: !0
                }, {
                    name: "wallet",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "metadata",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "mint",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "mintAuthority",
                    isMut: !1,
                    isSigner: !0
                }, {
                    name: "updateAuthority",
                    isMut: !1,
                    isSigner: !0
                }, {
                    name: "masterEdition",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "tokenMetadataProgram",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "tokenProgram",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "systemProgram",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "rent",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "clock",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "recentBlockhashes",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "instructionSysvarAccount",
                    isMut: !1,
                    isSigner: !1
                }],
                args: [{
                    name: "creatorBump",
                    type: "u8"
                }]
            }, {
                name: "setCollectionDuringMint",
                accounts: [{
                    name: "candyMachine",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "metadata",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "payer",
                    isMut: !1,
                    isSigner: !0
                }, {
                    name: "collectionPda",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "tokenMetadataProgram",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "instructions",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "collectionMint",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "collectionMetadata",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "collectionMasterEdition",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "authority",
                    isMut: !1,
                    isSigner: !1
                }, {
                    name: "collectionAuthorityRecord",
                    isMut: !1,
                    isSigner: !1
                }],
                args: []
            }, {
                name: "setLockupSettings",
                accounts: [{
                    name: "candyMachine",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "authority",
                    isMut: !1,
                    isSigner: !0
                }, {
                    name: "lockupSettings",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "payer",
                    isMut: !0,
                    isSigner: !0
                }, {
                    name: "systemProgram",
                    isMut: !1,
                    isSigner: !1
                }],
                args: [{
                    name: "lockupType",
                    type: "u8"
                }, {
                    name: "number",
                    type: "i64"
                }]
            }, {
                name: "closeLockupSettings",
                accounts: [{
                    name: "candyMachine",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "authority",
                    isMut: !1,
                    isSigner: !0
                }, {
                    name: "lockupSettings",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "systemProgram",
                    isMut: !1,
                    isSigner: !1
                }],
                args: []
            }, {
                name: "withdrawFunds",
                accounts: [{
                    name: "candyMachine",
                    isMut: !0,
                    isSigner: !1
                }, {
                    name: "authority",
                    isMut: !1,
                    isSigner: !0
                }],
                args: []
            }],
            accounts: [{
                name: "CandyMachine",
                type: {
                    kind: "struct",
                    fields: [{
                        name: "authority",
                        type: "publicKey"
                    }, {
                        name: "wallet",
                        type: "publicKey"
                    }, {
                        name: "tokenMint",
                        type: {
                            option: "publicKey"
                        }
                    }, {
                        name: "itemsRedeemed",
                        type: "u64"
                    }, {
                        name: "data",
                        type: {
                            defined: "CandyMachineData"
                        }
                    }]
                }
            }, {
                name: "CollectionPDA",
                type: {
                    kind: "struct",
                    fields: [{
                        name: "mint",
                        type: "publicKey"
                    }, {
                        name: "candyMachine",
                        type: "publicKey"
                    }]
                }
            }, {
                name: "LockupSettings",
                type: {
                    kind: "struct",
                    fields: [{
                        name: "candyMachine",
                        type: "publicKey"
                    }, {
                        name: "lockupType",
                        type: "u8"
                    }, {
                        name: "number",
                        type: "i64"
                    }]
                }
            }],
            types: [{
                name: "CandyMachineData",
                type: {
                    kind: "struct",
                    fields: [{
                        name: "uuid",
                        type: "string"
                    }, {
                        name: "price",
                        type: "u64"
                    }, {
                        name: "symbol",
                        type: "string"
                    }, {
                        name: "sellerFeeBasisPoints",
                        type: "u16"
                    }, {
                        name: "maxSupply",
                        type: "u64"
                    }, {
                        name: "isMutable",
                        type: "bool"
                    }, {
                        name: "retainAuthority",
                        type: "bool"
                    }, {
                        name: "goLiveDate",
                        type: {
                            option: "i64"
                        }
                    }, {
                        name: "endSettings",
                        type: {
                            option: {
                                defined: "EndSettings"
                            }
                        }
                    }, {
                        name: "creators",
                        type: {
                            vec: {
                                defined: "Creator"
                            }
                        }
                    }, {
                        name: "hiddenSettings",
                        type: {
                            option: {
                                defined: "HiddenSettings"
                            }
                        }
                    }, {
                        name: "whitelistMintSettings",
                        type: {
                            option: {
                                defined: "WhitelistMintSettings"
                            }
                        }
                    }, {
                        name: "itemsAvailable",
                        type: "u64"
                    }, {
                        name: "gatekeeper",
                        type: {
                            option: {
                                defined: "GatekeeperConfig"
                            }
                        }
                    }]
                }
            }, {
                name: "ConfigLine",
                type: {
                    kind: "struct",
                    fields: [{
                        name: "name",
                        type: "string"
                    }, {
                        name: "uri",
                        type: "string"
                    }]
                }
            }, {
                name: "EndSettings",
                type: {
                    kind: "struct",
                    fields: [{
                        name: "endSettingType",
                        type: {
                            defined: "EndSettingType"
                        }
                    }, {
                        name: "number",
                        type: "u64"
                    }]
                }
            }, {
                name: "Creator",
                type: {
                    kind: "struct",
                    fields: [{
                        name: "address",
                        type: "publicKey"
                    }, {
                        name: "verified",
                        type: "bool"
                    }, {
                        name: "share",
                        type: "u8"
                    }]
                }
            }, {
                name: "HiddenSettings",
                type: {
                    kind: "struct",
                    fields: [{
                        name: "name",
                        type: "string"
                    }, {
                        name: "uri",
                        type: "string"
                    }, {
                        name: "hash",
                        type: {
                            array: ["u8", 32]
                        }
                    }]
                }
            }, {
                name: "WhitelistMintSettings",
                type: {
                    kind: "struct",
                    fields: [{
                        name: "mode",
                        type: {
                            defined: "WhitelistMintMode"
                        }
                    }, {
                        name: "mint",
                        type: "publicKey"
                    }, {
                        name: "presale",
                        type: "bool"
                    }, {
                        name: "discountPrice",
                        type: {
                            option: "u64"
                        }
                    }]
                }
            }, {
                name: "GatekeeperConfig",
                type: {
                    kind: "struct",
                    fields: [{
                        name: "gatekeeperNetwork",
                        type: "publicKey"
                    }, {
                        name: "expireOnUse",
                        type: "bool"
                    }]
                }
            }, {
                name: "EndSettingType",
                type: {
                    kind: "enum",
                    variants: [{
                        name: "Date"
                    }, {
                        name: "Amount"
                    }]
                }
            }, {
                name: "LockupType",
                type: {
                    kind: "enum",
                    variants: [{
                        name: "Expiration"
                    }, {
                        name: "Duration"
                    }]
                }
            }, {
                name: "WhitelistMintMode",
                type: {
                    kind: "enum",
                    variants: [{
                        name: "BurnEveryTime"
                    }, {
                        name: "NeverBurn"
                    }]
                }
            }],
            errors: [{
                code: 6e3,
                name: "IncorrectOwner",
                msg: "Account does not have correct owner!"
            }, {
                code: 6001,
                name: "Uninitialized",
                msg: "Account is not initialized!"
            }, {
                code: 6002,
                name: "MintMismatch",
                msg: "Mint Mismatch!"
            }, {
                code: 6003,
                name: "IndexGreaterThanLength",
                msg: "Index greater than length!"
            }, {
                code: 6004,
                name: "NumericalOverflowError",
                msg: "Numerical overflow error!"
            }, {
                code: 6005,
                name: "TooManyCreators",
                msg: "Can only provide up to 4 creators to candy machine (because candy machine is one)!"
            }, {
                code: 6006,
                name: "UuidMustBeExactly6Length",
                msg: "Uuid must be exactly of 6 length"
            }, {
                code: 6007,
                name: "NotEnoughTokens",
                msg: "Not enough tokens to pay for this minting"
            }, {
                code: 6008,
                name: "NotEnoughSOL",
                msg: "Not enough SOL to pay for this minting"
            }, {
                code: 6009,
                name: "TokenTransferFailed",
                msg: "Token transfer failed"
            }, {
                code: 6010,
                name: "CandyMachineEmpty",
                msg: "Candy machine is empty!"
            }, {
                code: 6011,
                name: "CandyMachineNotLive",
                msg: "Candy machine is not live!"
            }, {
                code: 6012,
                name: "HiddenSettingsConfigsDoNotHaveConfigLines",
                msg: "Configs that are using hidden uris do not have config lines, they have a single hash representing hashed order"
            }, {
                code: 6013,
                name: "CannotChangeNumberOfLines",
                msg: "Cannot change number of lines unless is a hidden config"
            }, {
                code: 6014,
                name: "DerivedKeyInvalid",
                msg: "Derived key invalid"
            }, {
                code: 6015,
                name: "PublicKeyMismatch",
                msg: "Public key mismatch"
            }, {
                code: 6016,
                name: "NoWhitelistToken",
                msg: "No whitelist token present"
            }, {
                code: 6017,
                name: "TokenBurnFailed",
                msg: "Token burn failed"
            }, {
                code: 6018,
                name: "GatewayAppMissing",
                msg: "Missing gateway app when required"
            }, {
                code: 6019,
                name: "GatewayTokenMissing",
                msg: "Missing gateway token when required"
            }, {
                code: 6020,
                name: "GatewayTokenExpireTimeInvalid",
                msg: "Invalid gateway token expire time"
            }, {
                code: 6021,
                name: "NetworkExpireFeatureMissing",
                msg: "Missing gateway network expire feature when required"
            }, {
                code: 6022,
                name: "CannotFindUsableConfigLine",
                msg: "Unable to find an unused config line near your random number index"
            }, {
                code: 6023,
                name: "InvalidString",
                msg: "Invalid string"
            }, {
                code: 6024,
                name: "SuspiciousTransaction",
                msg: "Suspicious transaction detected"
            }, {
                code: 6025,
                name: "CannotSwitchToHiddenSettings",
                msg: "Cannot Switch to Hidden Settings after items available is greater than 0"
            }, {
                code: 6026,
                name: "IncorrectSlotHashesPubkey",
                msg: "Incorrect SlotHashes PubKey"
            }, {
                code: 6027,
                name: "IncorrectCollectionAuthority",
                msg: "Incorrect collection NFT authority"
            }, {
                code: 6028,
                name: "MismatchedCollectionPDA",
                msg: "Collection PDA address is invalid"
            }, {
                code: 6029,
                name: "MismatchedCollectionMint",
                msg: "Provided mint account doesn't match collection PDA mint"
            }, {
                code: 6030,
                name: "SlotHashesEmpty",
                msg: "Slot hashes Sysvar is empty"
            }, {
                code: 6031,
                name: "MetadataAccountMustBeEmpty",
                msg: "The metadata account has data in it, and this must be empty to mint a new NFT"
            }, {
                code: 6032,
                name: "MissingSetCollectionDuringMint",
                msg: "Missing set collection during mint IX for Candy Machine with collection set"
            }, {
                code: 6033,
                name: "NoChangingCollectionDuringMint",
                msg: "Can't change collection settings after items have begun to be minted"
            }, {
                code: 6034,
                name: "CandyCollectionRequiresRetainAuthority",
                msg: "Retain authority must be true for Candy Machines with a collection set"
            }, {
                code: 6035,
                name: "InvalidCandyMachineAuthority",
                msg: "Invalid candy machine authority"
            }, {
                code: 6036,
                name: "InvalidLockupType",
                msg: "Lockup settings lockup type is invalid"
            }, {
                code: 6037,
                name: "LockupSettingsAccountMissing",
                msg: "Lockup settings account missing"
            }, {
                code: 6038,
                name: "LockupSettingsAccountInvalid",
                msg: "Lockup settings account invalid"
            }, {
                code: 6039,
                name: "LockupSettingsMissingAccounts",
                msg: "Lockup settings missing accounts"
            }, {
                code: 6040,
                name: "LockupSettingsMissingTokenManager",
                msg: "Lockup settings missing token manager"
            }, {
                code: 6041,
                name: "LockupSettingsMissingTokenManagerTokenAccount",
                msg: "Lockup settings missing token managertoken account"
            }, {
                code: 6042,
                name: "LockupSettingsMissingMintCounter",
                msg: "Lockup settings missing mint counter"
            }, {
                code: 6043,
                name: "LockupSettingsMissingRecipientTokenAccount",
                msg: "Lockup settings missing recipient token account"
            }, {
                code: 6044,
                name: "LockupSettingsMissingTimeInvalidator",
                msg: "Lockup settings missing time invalidator"
            }, {
                code: 6045,
                name: "LockupSettingsMissingTimeInvalidatorProgram",
                msg: "Lockup settings missing time invalidator program"
            }, {
                code: 6046,
                name: "LockupSettingsInvalidTimeInvalidatorProgram",
                msg: "Lockup settings invalid time invalidator program"
            }, {
                code: 6047,
                name: "LockupSettingsMissingTokenManagerProgram",
                msg: "Lockup settings missing token manager program"
            }, {
                code: 6048,
                name: "LockupSettingsInvalidTokenManagerProgram",
                msg: "Lockup settings invalid token manager program"
            }]
        })
          , h = n(43029);
        function g(e, t, n, i, a, s, r) {
            try {
                var c = e[s](r)
                  , o = c.value
            } catch (l) {
                return void n(l)
            }
            c.done ? t(o) : Promise.resolve(o).then(i, a)
        }
        function x(e) {
            return function() {
                var t = this
                  , n = arguments;
                return new Promise((function(i, a) {
                    var s = e.apply(t, n);
                    function r(e) {
                        g(s, i, a, r, c, "next", e)
                    }
                    function c(e) {
                        g(s, i, a, r, c, "throw", e)
                    }
                    r(void 0)
                }
                ))
            }
        }
        var f = "/api/solana"
          , y = function(e) {
            return x(a().mark((function t() {
                return a().wrap((function(t) {
                    for (; ; )
                        switch (t.prev = t.next) {
                        case 0:
                            return t.abrupt("return", fetch("".concat(f, "/bonding-price?tokenBondingKey=").concat(e)).then((function(e) {
                                return e.json()
                            }
                            )));
                        case 1:
                        case "end":
                            return t.stop()
                        }
                }
                ), t)
            }
            )))()
        }
          , v = function(e, t) {
            return x(a().mark((function n() {
                return a().wrap((function(n) {
                    for (; ; )
                        switch (n.prev = n.next) {
                        case 0:
                            return n.abrupt("return", fetch("".concat(f, "/bonding-info?mint=").concat(e, "&index=").concat(t || 0)).then((function(e) {
                                return e.json()
                            }
                            )));
                        case 1:
                        case "end":
                            return n.stop()
                        }
                }
                ), n)
            }
            )))()
        }
          , N = function(e) {
            return x(a().mark((function t() {
                return a().wrap((function(t) {
                    for (; ; )
                        switch (t.prev = t.next) {
                        case 0:
                            return t.abrupt("return", fetch("/api/solana/send-transaction", {
                                method: "POST",
                                body: JSON.stringify(e)
                            }).then((function(e) {
                                return e.json()
                            }
                            )));
                        case 1:
                        case "end":
                            return t.stop()
                        }
                }
                ), t)
            }
            )))()
        }
          , b = n(48764).Buffer;
        function S(e, t) {
            (null == t || t > e.length) && (t = e.length);
            for (var n = 0, i = new Array(t); n < t; n++)
                i[n] = e[n];
            return i
        }
        function T(e, t, n, i, a, s, r) {
            try {
                var c = e[s](r)
                  , o = c.value
            } catch (l) {
                return void n(l)
            }
            c.done ? t(o) : Promise.resolve(o).then(i, a)
        }
        function E(e) {
            return function() {
                var t = this
                  , n = arguments;
                return new Promise((function(i, a) {
                    var s = e.apply(t, n);
                    function r(e) {
                        T(s, i, a, r, c, "next", e)
                    }
                    function c(e) {
                        T(s, i, a, r, c, "throw", e)
                    }
                    r(void 0)
                }
                ))
            }
        }
        function w(e) {
            return function(e) {
                if (Array.isArray(e))
                    return S(e)
            }(e) || function(e) {
                if ("undefined" !== typeof Symbol && null != e[Symbol.iterator] || null != e["@@iterator"])
                    return Array.from(e)
            }(e) || function(e, t) {
                if (!e)
                    return;
                if ("string" === typeof e)
                    return S(e, t);
                var n = Object.prototype.toString.call(e).slice(8, -1);
                "Object" === n && e.constructor && (n = e.constructor.name);
                if ("Map" === n || "Set" === n)
                    return Array.from(n);
                if ("Arguments" === n || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))
                    return S(e, t)
            }(e) || function() {
                throw new TypeError("Invalid attempt to spread non-iterable instance.\\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
            }()
        }
        var j = new l.rV.PublicKey("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
          , A = (function() {
            var e = E(a().mark((function e(t, n) {
                return a().wrap((function(e) {
                    for (; ; )
                        switch (e.prev = e.next) {
                        case 0:
                            return e.next = 2,
                            l.rV.PublicKey.findProgramAddress([n.toBuffer(), h.H_.toBuffer(), t.toBuffer()], j);
                        case 2:
                            return e.abrupt("return", e.sent);
                        case 3:
                        case "end":
                            return e.stop()
                        }
                }
                ), e)
            }
            )))
        }(),
        function() {
            var e = E(a().mark((function e(t) {
                return a().wrap((function(e) {
                    for (; ; )
                        switch (e.prev = e.next) {
                        case 0:
                            return e.next = 2,
                            l.rV.PublicKey.findProgramAddress([t.toBuffer(), b.from("expire")], u);
                        case 2:
                            return e.abrupt("return", e.sent);
                        case 3:
                        case "end":
                            return e.stop()
                        }
                }
                ), e)
            }
            )))
        }(),
        function() {
            var e = E(a().mark((function e(t, n) {
                return a().wrap((function(e) {
                    for (; ; )
                        switch (e.prev = e.next) {
                        case 0:
                            return e.next = 2,
                            l.rV.PublicKey.findProgramAddress([t.toBuffer(), b.from("gateway"), b.from([0, 0, 0, 0, 0, 0, 0, 0]), n.toBuffer()], u);
                        case 2:
                            return e.abrupt("return", e.sent);
                        case 3:
                        case "end":
                            return e.stop()
                        }
                }
                ), e)
            }
            )))
        }(),
        function() {
            var e = E(a().mark((function e(t, n, i) {
                var s, r, c, u, d, h = arguments;
                return a().wrap((function(e) {
                    for (; ; )
                        switch (e.prev = e.next) {
                        case 0:
                            return s = h.length > 3 && void 0 !== h[3] ? h[3] : "",
                            r = new l.zt(i,t,{
                                preflightCommitment: "processed"
                            }),
                            c = new l.$r(p,m,r),
                            e.next = 5,
                            fetch("".concat(s, "/api/solana/cm-state?id=").concat(n)).then((function(e) {
                                return e.json()
                            }
                            ));
                        case 5:
                            return u = e.sent,
                            (d = u.state).tokenMint = d.tokenMint && new o.PublicKey(d.tokenMint),
                            d.treasury = d.treasury && new o.PublicKey(d.treasury),
                            d.treasury = d.treasury && new o.PublicKey(d.treasury),
                            d.gatekeeper && (d.gatekeeper.gatekeeperNetwork = new o.PublicKey(d.gatekeeper.gatekeeperNetwork)),
                            e.abrupt("return", {
                                id: n,
                                program: c,
                                state: d
                            });
                        case 12:
                        case "end":
                            return e.stop()
                        }
                }
                ), e)
            }
            )));
            return function(t, n, i) {
                return e.apply(this, arguments)
            }
        }())
          , O = function() {
            var e = E(a().mark((function e(t, n, i) {
                var s, r, c, u, m, p, h, g, x, f, y, v, S, T, E, j, A, O, R, M, I, k, L, C, P = arguments;
                return a().wrap((function(e) {
                    for (; ; )
                        switch (e.prev = e.next) {
                        case 0:
                            s = P.length > 3 && void 0 !== P[3] ? P[3] : 1,
                            r = P.length > 4 ? P[4] : void 0,
                            c = [],
                            u = 0;
                        case 3:
                            if (!(u < s)) {
                                e.next = 22;
                                break
                            }
                            return p = l.rV.Keypair.generate(),
                            h = "/api/solana/mint-info?",
                            g = new URLSearchParams({
                                id: n.id.toBase58(),
                                payer: i.toBase58(),
                                mint: p.publicKey.toBase58()
                            }),
                            r && Object.keys(r).length > 0 && (g.set("tokenBonding", r.tokenBonding.toBase58()),
                            g.set("maxPrice", r.maxPrice.toString())),
                            e.next = 11,
                            fetch(h + g.toString()).then((function(e) {
                                return e.json()
                            }
                            ));
                        case 11:
                            if (x = e.sent,
                            f = x.success,
                            y = x.txs,
                            v = x.message,
                            f) {
                                e.next = 17;
                                break
                            }
                            throw new Error(v);
                        case 17:
                            S = y.map((function(e, t) {
                                var n = o.Transaction.from(b.from(e, "base64"));
                                return console.log(n),
                                t === y.length - 1 && (n.setSigners(i, p.publicKey, d),
                                n.partialSign(p)),
                                n
                            }
                            )),
                            (m = c).push.apply(m, w(S));
                        case 19:
                            u++,
                            e.next = 3;
                            break;
                        case 22:
                            return e.next = 24,
                            t.wallet.signAllTransactions(c);
                        case 24:
                            if (T = e.sent.map((function(e) {
                                return e.serialize({
                                    requireAllSignatures: !1
                                }).toString("base64")
                            }
                            )),
                            !r) {
                                e.next = 32;
                                break
                            }
                            return e.next = 28,
                            N(T);
                        case 28:
                            if ((E = e.sent).success) {
                                e.next = 31;
                                break
                            }
                            return e.abrupt("return", {
                                status: "ERROR",
                                message: E.error || "An error occured"
                            });
                        case 31:
                            return e.abrupt("return", {
                                status: "SUCCESS",
                                message: "Successfully minted 1 item. \n p.s. it's Bifrost, not Bitfrost."
                            });
                        case 32:
                            j = 0,
                            A = "",
                            O = !0,
                            R = !1,
                            M = void 0,
                            e.prev = 35,
                            I = T[Symbol.iterator]();
                        case 37:
                            if (O = (k = I.next()).done) {
                                e.next = 51;
                                break
                            }
                            return L = k.value,
                            e.next = 41,
                            N([L]);
                        case 41:
                            if (!(C = e.sent).success) {
                                e.next = 46;
                                break
                            }
                            j++,
                            e.next = 48;
                            break;
                        case 46:
                            return A = C.error || "An error occured",
                            e.abrupt("break", 51);
                        case 48:
                            O = !0,
                            e.next = 37;
                            break;
                        case 51:
                            e.next = 57;
                            break;
                        case 53:
                            e.prev = 53,
                            e.t0 = e.catch(35),
                            R = !0,
                            M = e.t0;
                        case 57:
                            e.prev = 57,
                            e.prev = 58,
                            O || null == I.return || I.return();
                        case 60:
                            if (e.prev = 60,
                            !R) {
                                e.next = 63;
                                break
                            }
                            throw M;
                        case 63:
                            return e.finish(60);
                        case 64:
                            return e.finish(57);
                        case 65:
                            if (console.log("aaa", s, j),
                            j) {
                                e.next = 68;
                                break
                            }
                            return e.abrupt("return", {
                                status: "ERROR",
                                message: A
                            });
                        case 68:
                            if (s === j) {
                                e.next = 70;
                                break
                            }
                            return e.abrupt("return", {
                                status: "INFO",
                                message: "Successfully minted ".concat(j, " item").concat(s > 1 ? "s" : "", ". ").concat(s - j, " item").concat(s > 1 ? "s" : "", " failed: ").concat(A)
                            });
                        case 70:
                            return e.abrupt("return", {
                                status: "SUCCESS",
                                message: "Successfully minted ".concat(j, " item").concat(s > 1 ? "s" : "", ". \n p.s. it's Bifrost, not Bitfrost.")
                            });
                        case 71:
                        case "end":
                            return e.stop()
                        }
                }
                ), e, null, [[35, 53, 57, 65], [58, , 60, 64]])
            }
            )));
            return function(t, n, i) {
                return e.apply(this, arguments)
            }
        }()
          , R = n(67294)
          , M = n(1485);
        function I(e, t, n, i, a, s, r) {
            try {
                var c = e[s](r)
                  , o = c.value
            } catch (l) {
                return void n(l)
            }
            c.done ? t(o) : Promise.resolve(o).then(i, a)
        }
        function k(e, t, n, i) {
            var s, r = (0,
            R.useState)(), c = r[0], u = r[1], d = (0,
            R.useState)(!1), m = d[0], p = d[1], h = (0,
            R.useMemo)((function() {
                return t || new l.w5(o.Keypair.generate())
            }
            ), [t]), g = (0,
            R.useCallback)((s = a().mark((function e() {
                var t, s, r, c;
                return a().wrap((function(e) {
                    for (; ; )
                        switch (e.prev = e.next) {
                        case 0:
                            if (h) {
                                e.next = 2;
                                break
                            }
                            return e.abrupt("return", console.log("[INFO]: Wallet is not connected"));
                        case 2:
                            if (p(!0),
                            !n) {
                                e.next = 20;
                                break
                            }
                            return e.prev = 4,
                            e.next = 8,
                            A(h, n, i);
                        case 8:
                            null === (r = e.sent) || void 0 === r || r.state.goLiveDate,
                            (new Date).getTime(),
                            (null === (t = null === r || void 0 === r ? void 0 : r.state.endSettings) || void 0 === t ? void 0 : t.endSettingType.date) && (r.state.endSettings.number,
                            (new Date).getTime()),
                            (null === (s = null === r || void 0 === r ? void 0 : r.state.endSettings) || void 0 === s ? void 0 : s.endSettingType.amount) && (c = Math.min(r.state.endSettings.number, r.state.itemsAvailable),
                            r.state.itemsRedeemed > c && (r.state.isSoldOut = !0)),
                            r.state.isSoldOut,
                            u(r),
                            e.next = 20;
                            break;
                        case 16:
                            e.prev = 16,
                            e.t0 = e.catch(4),
                            console.log("There was a problem fetching Candy Machine state"),
                            console.log(e.t0);
                        case 20:
                            p(!1);
                        case 21:
                        case "end":
                            return e.stop()
                        }
                }
                ), e, null, [[4, 16]])
            }
            )),
            function() {
                var e = this
                  , t = arguments;
                return new Promise((function(n, i) {
                    var a = s.apply(e, t);
                    function r(e) {
                        I(a, n, i, r, c, "next", e)
                    }
                    function c(e) {
                        I(a, n, i, r, c, "throw", e)
                    }
                    r(void 0)
                }
                ))
            }
            ), [h, n, i, null === e || void 0 === e ? void 0 : e.user.sub]);
            return (0,
            R.useEffect)((function() {
                var t;
                (null === e || void 0 === e || null === (t = e.user) || void 0 === t ? void 0 : t.sub) && !m && (console.log("Fetching candy machine state"),
                g())
            }
            ), [null === e || void 0 === e ? void 0 : e.user.sub, n]),
            (0,
            M.Yz)((function() {
                e && (console.log("Refreshing candy machine state"),
                g())
            }
            ), 1e4),
            {
                loading: m,
                candyMachine: c
            }
        }
        var L = n(76535);
        function C(e, t, n, i, a, s, r) {
            try {
                var c = e[s](r)
                  , o = c.value
            } catch (l) {
                return void n(l)
            }
            c.done ? t(o) : Promise.resolve(o).then(i, a)
        }
        function P(e) {
            return function() {
                var t = this
                  , n = arguments;
                return new Promise((function(i, a) {
                    var s = e.apply(t, n);
                    function r(e) {
                        C(s, i, a, r, c, "next", e)
                    }
                    function c(e) {
                        C(s, i, a, r, c, "throw", e)
                    }
                    r(void 0)
                }
                ))
            }
        }
        var D = "/api/project"
          , F = function(e) {
            return P(a().mark((function t() {
                var n, i;
                return a().wrap((function(t) {
                    for (; ; )
                        switch (t.prev = t.next) {
                        case 0:
                            return t.next = 2,
                            fetch("".concat(D, "/info/").concat(e));
                        case 2:
                            return n = t.sent,
                            t.next = 5,
                            n.json();
                        case 5:
                            return i = t.sent,
                            t.abrupt("return", i.data);
                        case 7:
                        case "end":
                            return t.stop()
                        }
                }
                ), t)
            }
            )))()
        }
          , B = function(e, t) {
            return P(a().mark((function n() {
                var i;
                return a().wrap((function(n) {
                    for (; ; )
                        switch (n.prev = n.next) {
                        case 0:
                            return n.next = 2,
                            fetch("".concat(D, "/").concat(e, "/gateway/token/issue"), {
                                method: "POST",
                                body: JSON.stringify({
                                    recipient: t
                                })
                            });
                        case 2:
                            return i = n.sent,
                            n.abrupt("return", i.json());
                        case 4:
                        case "end":
                            return n.stop()
                        }
                }
                ), n)
            }
            )))()
        };
        function H(e, t, n, i, a, s, r) {
            try {
                var c = e[s](r)
                  , o = c.value
            } catch (l) {
                return void n(l)
            }
            c.done ? t(o) : Promise.resolve(o).then(i, a)
        }
        var K = function(e, t) {
            var n, i = (0,
            R.useState)(!1), s = i[0], r = i[1], c = (0,
            R.useState)(), o = c[0], l = c[1], u = (0,
            R.useState)(), d = u[0], m = u[1], p = (0,
            R.useCallback)((n = a().mark((function t() {
                var n, i;
                return a().wrap((function(t) {
                    for (; ; )
                        switch (t.prev = t.next) {
                        case 0:
                            if (e) {
                                t.next = 2;
                                break
                            }
                            return t.abrupt("return", console.log("[INFO]: No projectSlug defined"));
                        case 2:
                            return t.prev = 2,
                            r(!0),
                            t.next = 6,
                            F(e);
                        case 6:
                            n = t.sent,
                            i = n.mintPhases.find((function(e) {
                                return e.isActive && new Date(e.startDate) < new Date && new Date(e.endDate) > new Date
                            }
                            )),
                            r(!1),
                            l(n),
                            m(i),
                            t.next = 16;
                            break;
                        case 13:
                            t.prev = 13,
                            t.t0 = t.catch(2),
                            console.log("error", t.t0);
                        case 16:
                        case "end":
                            return t.stop()
                        }
                }
                ), t, null, [[2, 13]])
            }
            )),
            function() {
                var e = this
                  , t = arguments;
                return new Promise((function(i, a) {
                    var s = n.apply(e, t);
                    function r(e) {
                        H(s, i, a, r, c, "next", e)
                    }
                    function c(e) {
                        H(s, i, a, r, c, "throw", e)
                    }
                    r(void 0)
                }
                ))
            }
            ), [e, t]);
            return (0,
            M.Yz)((function() {
                console.log("Refreshing Project"),
                p()
            }
            ), 1e4),
            (0,
            R.useEffect)((function() {
                e && p()
            }
            ), [e, p]),
            {
                loading: s,
                project: o,
                activePhase: d
            }
        };
        function U() {
            for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
                t[n] = arguments[n];
            return t.filter(Boolean).join(" ")
        }
        var Y = n(68171)
          , G = n(11355)
          , W = n(37763)
          , V = n(41664)
          , _ = n.n(V);
        function z(e, t, n, i, a, s, r) {
            try {
                var c = e[s](r)
                  , o = c.value
            } catch (l) {
                return void n(l)
            }
            c.done ? t(o) : Promise.resolve(o).then(i, a)
        }
        var Z = function() {
            var e, t = (0,
            R.useState)(!1), n = t[0], i = t[1], s = (0,
            R.useState)(), r = s[0], c = s[1], o = (0,
            R.useCallback)((e = a().mark((function e() {
                var t, n;
                return a().wrap((function(e) {
                    for (; ; )
                        switch (e.prev = e.next) {
                        case 0:
                            return e.prev = 0,
                            i(!0),
                            e.next = 4,
                            fetch("https://api.solanart.io/get_solana_tps");
                        case 4:
                            return t = e.sent,
                            e.next = 7,
                            t.json();
                        case 7:
                            n = e.sent,
                            i(!1),
                            c(n.tps),
                            e.next = 15;
                            break;
                        case 12:
                            e.prev = 12,
                            e.t0 = e.catch(0),
                            console.log("Error Fetching TPS", e.t0);
                        case 15:
                        case "end":
                            return e.stop()
                        }
                }
                ), e, null, [[0, 12]])
            }
            )),
            function() {
                var t = this
                  , n = arguments;
                return new Promise((function(i, a) {
                    var s = e.apply(t, n);
                    function r(e) {
                        z(s, i, a, r, c, "next", e)
                    }
                    function c(e) {
                        z(s, i, a, r, c, "throw", e)
                    }
                    r(void 0)
                }
                ))
            }
            ), []);
            return (0,
            M.Yz)((function() {
                console.log("Refreshing TPS"),
                o()
            }
            ), 1e4),
            {
                loading: n,
                tps: r
            }
        }
          , q = n(24762);
        function $() {
            var e = Z().tps;
            return (0,
            s.jsx)(s.Fragment, {
                children: e && (0,
                s.jsxs)("div", {
                    className: "border px-3 py-1 text-sm rounded-md border-gray-700 ".concat(e < 1500 && "hover:cursor-pointer"),
                    "data-tip": "",
                    "data-for": "tps-tip",
                    children: [(0,
                    s.jsxs)("div", {
                        className: "flex sm:flex-col items-center",
                        children: [(0,
                        s.jsx)("div", {
                            className: "flex items-center",
                            children: (0,
                            s.jsx)("p", {
                                className: "text-white",
                                children: "Solana"
                            })
                        }), (0,
                        s.jsx)("div", {
                            className: "flex pl-2 sm:pl-0",
                            children: (0,
                            s.jsxs)("p", {
                                className: e > 1500 ? "text-greenc" : "text-red-500",
                                children: [e, " TPS"]
                            })
                        })]
                    }), e < 1500 && (0,
                    s.jsx)(q.Z, {
                        id: "tps-tip",
                        type: "light",
                        effect: "solid",
                        place: "bottom",
                        getContent: function() {
                            return (0,
                            s.jsx)("div", {
                                className: "bg-white px-4 py-2 rounded-md",
                                children: (0,
                                s.jsxs)("p", {
                                    className: "text-grayc",
                                    children: ["Due to the Solana network is currently experiencing a limited capacity of ~", e, " transactions per second. ", (0,
                                    s.jsx)("br", {}), " ", "This may result in your transactions failing, if this happens, please try again."]
                                })
                            })
                        }
                    })]
                })
            })
        }
        function X(e) {
            var t = e.session;
            return (0,
            s.jsx)(s.Fragment, {
                children: (0,
                s.jsx)("section", {
                    className: "relative",
                    children: (0,
                    s.jsxs)("div", {
                        className: "flex md:flex-row flex-col md:justify-between justify-center sm:gap-8 gap-4 items-center",
                        children: [(0,
                        s.jsxs)("div", {
                            className: "flex-1 flex w-full xs:justify-between xs:flex-row flex-col gap-4 items-center",
                            children: [(0,
                            s.jsx)(_(), {
                                href: "/",
                                children: (0,
                                s.jsx)("img", {
                                    src: "/imgs/logo.svg",
                                    alt: "Bifrost",
                                    className: "cursor-pointer h-10 object-contain object-left"
                                })
                            }), (0,
                            s.jsx)($, {})]
                        }), (0,
                        s.jsxs)("div", {
                            className: "flex gap-4 items-center",
                            children: [t ? (0,
                            s.jsxs)(Y.v, {
                                as: "div",
                                className: "relative inline-block text-left",
                                children: [(0,
                                s.jsx)("div", {
                                    children: (0,
                                    s.jsxs)(Y.v.Button, {
                                        className: "bg-bluec2 flex items-center gap-4 px-4 py-2 rounded ",
                                        children: [(0,
                                        s.jsx)("img", {
                                            src: "/imgs/discord.svg",
                                            alt: "Discord"
                                        }), (0,
                                        s.jsx)("span", {
                                            className: "text-white",
                                            children: t.user.name
                                        }), (0,
                                        s.jsx)("img", {
                                            className: "hidden sm:visible",
                                            src: "/imgs/arrow-down.svg",
                                            alt: "Down"
                                        })]
                                    })
                                }), (0,
                                s.jsx)(G.u, {
                                    as: R.Fragment,
                                    children: (0,
                                    s.jsx)(Y.v.Items, {
                                        className: "origin-top-right absolute right-0 mt-2 p-2 w-36 rounded-lg shadow-lg bg-neutral-700 focus:outline-none",
                                        children: (0,
                                        s.jsx)(Y.v.Item, {
                                            children: function(e) {
                                                var t = e.active;
                                                return (0,
                                                s.jsx)("button", {
                                                    type: "button",
                                                    className: U(t ? "bg-slate-800" : "", "block w-full p-1 rounded-md text-lg text-white text-center"),
                                                    onClick: function() {
                                                        return (0,
                                                        c.signOut)({
                                                            redirect: !1
                                                        })
                                                    },
                                                    children: "Logout"
                                                })
                                            }
                                        })
                                    })
                                })]
                            }) : null, (0,
                            s.jsx)(W.aD, {
                                className: "!bg-bluec2"
                            })]
                        })]
                    })
                })
            })
        }
        var J = function() {
            return (0,
            s.jsxs)("div", {
                className: "flex flex-col gap-8 md:items-start items-center",
                children: [(0,
                s.jsx)("div", {
                    className: "animate-pulse max-w-md rounded-3xl md:p-6 shadow-lg bg-grayc lg:w-96 lg:h-96 w-64 h-64"
                }), (0,
                s.jsx)("div", {
                    className: "animate-pulse w-full h-16 rounded-xl shadow-lg bg-grayc"
                }), (0,
                s.jsx)("div", {
                    className: "animate-pulse w-full h-8 rounded-xl shadow-lg bg-grayc"
                }), (0,
                s.jsx)("div", {
                    className: "animate-pulse w-full h-8 rounded-xl shadow-lg bg-grayc"
                }), (0,
                s.jsx)("div", {
                    className: "animate-pulse w-full h-8 rounded-xl shadow-lg bg-grayc"
                }), (0,
                s.jsx)("div", {
                    className: "animate-pulse w-full h-8 rounded-xl shadow-lg bg-grayc"
                })]
            })
        };
        function Q(e) {
            var t = e.project;
            return t ? (0,
            s.jsxs)("div", {
                className: "flex flex-col md:items-start items-center",
                children: [(0,
                s.jsx)("h1", {
                    className: "text-white md:text-4xl text-3xl mb-4 text-center futura-bold md:hidden block",
                    children: t.name
                }), (0,
                s.jsx)("div", {
                    className: "md:max-w-full max-w-md rounded-3xl md:pt-6 shadow-lg w-full",
                    children: (0,
                    s.jsx)("img", {
                        src: t.avatar,
                        alt: "Avatar",
                        className: "rounded-3xl"
                    })
                }), (0,
                s.jsxs)("div", {
                    className: "flex md:gap-4 gap-8 md:justify-start justify-center mt-8",
                    children: [(0,
                    s.jsx)("div", {
                        className: "flex items-center",
                        children: (0,
                        s.jsx)("a", {
                            href: t.url,
                            target: "_blank",
                            rel: "noreferrer",
                            children: (0,
                            s.jsx)("img", {
                                src: "/imgs/world.svg",
                                className: "w-6 h-6",
                                alt: "Website"
                            })
                        })
                    }), (0,
                    s.jsx)("a", {
                        href: t.twitter,
                        target: "_blank",
                        rel: "noreferrer",
                        children: (0,
                        s.jsx)("img", {
                            src: "/imgs/twitter.svg",
                            alt: "Twitter"
                        })
                    }), (0,
                    s.jsx)("a", {
                        href: t.discord,
                        target: "_blank",
                        rel: "noreferrer",
                        children: (0,
                        s.jsx)("img", {
                            src: "/imgs/discord.svg",
                            alt: "Discord"
                        })
                    })]
                }), (0,
                s.jsxs)("div", {
                    className: "w-full flex items-center justify-center gap-4 mt-8",
                    children: [(0,
                    s.jsx)("div", {
                        className: "flex grow md:border-r-2 h-20 items-center border-gray-800",
                        children: (0,
                        s.jsx)("h1", {
                            className: "text-white md:text-4xl sm:text-3xl text-2xl futura-bold md:flex hidden mr-4",
                            children: t.name
                        })
                    }), (0,
                    s.jsxs)("div", {
                        className: "flex flex-col md:text-left text-center md:border-none border-y border-gray-800 flex-none w-full md:w-28 py-2 ",
                        children: [(0,
                        s.jsx)("p", {
                            className: "gradient-text text-4xl futura-bold text-center ",
                            children: t.supply
                        }), (0,
                        s.jsx)("p", {
                            className: "text-white text-center ",
                            children: "TOTAL ITEMS"
                        })]
                    })]
                }), (0,
                s.jsx)("div", {
                    className: "w-full border mt-4 border-gray-800 hidden md:block"
                }), (0,
                s.jsx)("p", {
                    className: "text-white md:text-xl text-2xl mt-8",
                    children: t.description
                })]
            }) : (0,
            s.jsx)(J, {})
        }
        function ee(e) {
            var t = e.isLoading;
            return (0,
            s.jsx)("div", {
                className: "w-full md:rounded-3xl md:p-12 p-4 md:shadow-lg md:bg-grayc text-center mt-5 ".concat(t && "animate-pulse"),
                children: (0,
                s.jsxs)("div", {
                    className: "".concat(t && "invisible"),
                    children: [(0,
                    s.jsx)("img", {
                        src: "/imgs/bifrost2.png",
                        alt: "Bifrost",
                        className: "mx-auto my-12 md:block hidden"
                    }), (0,
                    s.jsx)("h1", {
                        className: "text-white text-3xl futura-bold",
                        children: "Log in with Discord to mint"
                    }), (0,
                    s.jsxs)("button", {
                        type: "button",
                        className: "bg-bluec2 futura-bold flex items-center justify-center gap-4 w-48 py-2 mx-auto my-8 rounded",
                        onClick: function() {
                            return (0,
                            c.signIn)("discord")
                        },
                        children: [(0,
                        s.jsx)("img", {
                            src: "/imgs/discord.svg",
                            alt: "Discord"
                        }), (0,
                        s.jsx)("span", {
                            className: "text-white",
                            children: "Login"
                        })]
                    }), (0,
                    s.jsx)(W.aD, {
                        className: "!bg-bluec2 w-48 md:!hidden flex mx-auto justify-center"
                    })]
                })
            })
        }
        function te(e) {
            var t = e.setTab
              , n = e.tab
              , i = e.isDynamicPricing;
            return (0,
            s.jsx)("div", {
                className: "flex overflow-auto mb-6 -mx-4 sm:-mx-6",
                children: (0,
                s.jsx)("div", {
                    className: "flex-none min-w-full px-4 sm:px-6",
                    children: (0,
                    s.jsxs)("ul", {
                        className: "border-b border-grayc space-x-6 flex whitespace-nowrap",
                        children: [(0,
                        s.jsx)("li", {
                            children: (0,
                            s.jsx)("h2", {
                                className: "flex text-xl leading-6 py-3 px-4 border-b-4 -mb-px text-white \n                          ".concat("MINT" === n ? "border-blue-500" : "border-transparent", "\n                          hover:border-blue-500 cursor-pointer"),
                                onClick: function() {
                                    return t("MINT")
                                },
                                children: "Mint"
                            })
                        }), (0,
                        s.jsx)("li", {
                            children: (0,
                            s.jsx)("button", {
                                children: (0,
                                s.jsx)("h2", {
                                    className: "flex text-xl leading-6 py-3 px-4 border-b-4 -mb-px text-white \n                          ".concat("CHART" === n ? "border-blue-500" : "border-transparent", "\n                          ").concat(!i && "opacity-40 cursor-default", "\n                          ").concat(i && "hover:border-blue-500", " cursor-pointer"),
                                    onClick: function() {
                                        return i && t("CHART")
                                    },
                                    children: "Price Chart"
                                })
                            })
                        })]
                    })
                })
            })
        }
        var ne = function(e) {
            return e && ("STRATA_FORGE" === e.phaseType || "STRATA_SOL" === e.phaseType)
        }
          , ie = function(e) {
            return "STRATA_FORGE" === e.phaseType ? "/imgs/forge.png" : "GATEKEEPER_SOL" === e.phaseType ? "/imgs/gold.png" : "STRATA_SOL" === e.phaseType ? "/imgs/silver.png" : ""
        }
          , ae = n(30381)
          , se = n.n(ae)
          , re = function(e) {
            var t = new Date(e).getTime()
              , n = (0,
            R.useState)(t - (new Date).getTime())
              , i = n[0]
              , a = n[1];
            return (0,
            R.useEffect)((function() {
                var e = setInterval((function() {
                    a(t - (new Date).getTime())
                }
                ), 1e3);
                return function() {
                    return clearInterval(e)
                }
            }
            ), [t]),
            ce(i)
        }
          , ce = function(e) {
            var t = ""
              , n = se().duration(e);
            return n.days() && (t += n.days() + "d "),
            n.hours() && (t += n.hours() + "h "),
            n.minutes() && (t += n.minutes() + "m "),
            n.seconds() && (t += n.seconds() + "s"),
            [t, e]
        };
        function oe(e, t) {
            (null == t || t > e.length) && (t = e.length);
            for (var n = 0, i = new Array(t); n < t; n++)
                i[n] = e[n];
            return i
        }
        function le(e, t) {
            return function(e) {
                if (Array.isArray(e))
                    return e
            }(e) || function(e, t) {
                var n = null == e ? null : "undefined" !== typeof Symbol && e[Symbol.iterator] || e["@@iterator"];
                if (null != n) {
                    var i, a, s = [], r = !0, c = !1;
                    try {
                        for (n = n.call(e); !(r = (i = n.next()).done) && (s.push(i.value),
                        !t || s.length !== t); r = !0)
                            ;
                    } catch (o) {
                        c = !0,
                        a = o
                    } finally {
                        try {
                            r || null == n.return || n.return()
                        } finally {
                            if (c)
                                throw a
                        }
                    }
                    return s
                }
            }(e, t) || function(e, t) {
                if (!e)
                    return;
                if ("string" === typeof e)
                    return oe(e, t);
                var n = Object.prototype.toString.call(e).slice(8, -1);
                "Object" === n && e.constructor && (n = e.constructor.name);
                if ("Map" === n || "Set" === n)
                    return Array.from(n);
                if ("Arguments" === n || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))
                    return oe(e, t)
            }(e, t) || function() {
                throw new TypeError("Invalid attempt to destructure non-iterable instance.\\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
            }()
        }
        function ue(e) {
            var t, n, i = e.phase, a = e.isPastPhase, r = e.isActivePhase, c = le(re(null !== (t = i.startDate) && void 0 !== t ? t : new Date), 2), o = c[0], l = c[1], u = le(re(null !== (n = i.endDate) && void 0 !== n ? n : new Date), 2), d = u[0], m = u[1];
            return (0,
            s.jsx)(s.Fragment, {
                children: r ? (0,
                s.jsx)("div", {
                    children: (0,
                    s.jsxs)("div", {
                        className: "flex gap-2 items-center text-sm",
                        children: [m > 0 && (0,
                        s.jsxs)("p", {
                            className: "text-bluec mr-1 hidden sm:block",
                            children: ["Ends in ", d]
                        }), (0,
                        s.jsx)("p", {
                            className: "text-white text-sm",
                            children: "Live"
                        }), (0,
                        s.jsx)("div", {
                            className: "w-3 h-3 rounded-lg bg-greenc"
                        })]
                    })
                }) : a || m < 0 ? (0,
                s.jsx)("div", {
                    children: (0,
                    s.jsxs)("div", {
                        className: "flex gap-2 items-center",
                        children: [(0,
                        s.jsx)("span", {
                            className: "text-white text-sm",
                            children: "Ended"
                        }), (0,
                        s.jsx)("div", {
                            className: "w-3 h-3 rounded-lg bg-gray-500"
                        })]
                    })
                }) : (0,
                s.jsx)(s.Fragment, {
                    children: l > 0 ? (0,
                    s.jsxs)("span", {
                        className: "text-bluec text-sm",
                        children: ["Starts in ", o]
                    }) : (0,
                    s.jsx)("div", {
                        children: (0,
                        s.jsxs)("div", {
                            className: "flex gap-2 items-center",
                            children: [(0,
                            s.jsx)("span", {
                                className: "text-white text-sm",
                                children: "Activating..."
                            }), (0,
                            s.jsx)("div", {
                                className: "w-3 h-3 rounded-lg bg-orange-500"
                            })]
                        })
                    })
                })
            })
        }
        var de = n(38264)
          , me = n(68715)
          , pe = n(19965);
        function he(e) {
            e.project;
            var t = e.livePrice
              , n = e.phase
              , i = e.isActivePhase
              , a = (0,
            R.useMemo)((function() {
                return new Date(n.endDate) < new Date
            }
            ), [n])
              , r = (0,
            R.useMemo)((function() {
                return function(e, t) {
                    return "GATEKEEPER_SOL" === e.phaseType ? e.isActive && t ? t.toFixed(2) + " SOL" : e.price.toFixed(2) + " SOL" : "STRATA_SOL" === e.phaseType ? e.isActive && t ? t.toFixed(4) + " SOL" : e.price.toFixed(2) + " SOL" : "STRATA_FORGE" === e.phaseType ? e.isActive && t ? t.toFixed(4) + " FORGE" : e.price.toFixed(2) + " FORGE" : "-"
                }(n, t)
            }
            ), [t, n, i]);
            return (0,
            s.jsxs)(s.Fragment, {
                children: [(0,
                s.jsx)("div", {
                    className: "".concat(i && "w-full rounded-2xl shadow-lg bg-gradient-to-r from-orange-400 via-purple-600 to-blue-200 p-0.5"),
                    children: (0,
                    s.jsxs)("div", {
                        className: "w-full rounded-2xl flex gap-6 px-6 py-3 shadow-lg bg-grayc2 ".concat(!i && "opacity-50"),
                        children: [(0,
                        s.jsx)("div", {
                            className: "w-16 md:block hidden",
                            children: (0,
                            s.jsx)("img", {
                                src: ie(n),
                                alt: "Public",
                                className: "object-contain object-top"
                            })
                        }), (0,
                        s.jsxs)("div", {
                            className: "flex-1",
                            children: [(0,
                            s.jsxs)("div", {
                                className: "flex justify-between mb-2",
                                children: [(0,
                                s.jsxs)("div", {
                                    className: "flex flex-col gap-4",
                                    children: [(0,
                                    s.jsx)("div", {
                                        className: "w-16 md:hidden block",
                                        children: (0,
                                        s.jsx)("img", {
                                            src: ie(n),
                                            alt: "Public",
                                            className: "object-contain object-top"
                                        })
                                    }), ne(n) ? (0,
                                    s.jsxs)("div", {
                                        className: "flex gap-2 items-center",
                                        children: [(0,
                                        s.jsx)("span", {
                                            className: "text-white text-sm",
                                            children: "Dynamic pricing"
                                        }), (0,
                                        s.jsx)(de.Z, {
                                            className: "h-5 w-5 text-white cursor-pointer",
                                            "data-tip": "",
                                            "data-for": "pricing-tip"
                                        })]
                                    }) : (0,
                                    s.jsx)("div", {
                                        className: "flex gap-2 items-center text-sm",
                                        children: (0,
                                        s.jsx)("span", {
                                            className: n.userMintLimit ? "text-greenc" : "text-red-600",
                                            children: n.userMintLimit ? (0,
                                            s.jsxs)("div", {
                                                className: "flex items-center",
                                                children: [(0,
                                                s.jsx)(me.Z, {
                                                    className: "h-4 w-4 mr-1",
                                                    "aria-hidden": "true"
                                                }), (0,
                                                s.jsxs)("span", {
                                                    children: ["Whitelisted \xb7 Limit: ", n.userMintLimit, " items"]
                                                })]
                                            }) : (0,
                                            s.jsxs)("div", {
                                                className: "flex items-center text-red-600",
                                                children: [(0,
                                                s.jsx)(pe.Z, {
                                                    className: "h-4 w-4 mr-1",
                                                    "aria-hidden": "true"
                                                }), (0,
                                                s.jsx)("span", {
                                                    children: "Not Whitelisted"
                                                })]
                                            })
                                        })
                                    })]
                                }), (0,
                                s.jsx)(ue, {
                                    phase: n,
                                    isPastPhase: a,
                                    isActivePhase: i
                                })]
                            }), (0,
                            s.jsxs)("div", {
                                className: "flex justify-between mb-1 xs:flex-row flex-col",
                                children: [(0,
                                s.jsx)("span", {
                                    className: "text-white text-xl",
                                    children: n.name
                                }), (0,
                                s.jsxs)("div", {
                                    className: "text-white flex items-center",
                                    children: [(0,
                                    s.jsx)("span", {
                                        className: "text-lg pr-2",
                                        children: "GATEKEEPER_SOL" === n.phaseType ? "Price" : i ? "Current Price" : "Starting Price"
                                    }), t ? (0,
                                    s.jsx)("span", {
                                        className: "text-xl futura-bold",
                                        children: r
                                    }) : (0,
                                    s.jsx)("div", {
                                        className: "animate-pulse rounded-xl bg-slate-200 w-12 h-4"
                                    })]
                                })]
                            }), (0,
                            s.jsxs)("div", {
                                className: "flex justify-between mt-3 align-middle items-center",
                                children: [(0,
                                s.jsx)("span", {
                                    className: "px-2 py-0.5 bg-gray-700 rounded-lg text-greenc text-sm",
                                    children: i ? "MINTING" : a ? "FINISHED" : "UPCOMING"
                                }), (0,
                                s.jsx)("span", {
                                    className: i ? "text-greenc text-sm" : "text-indigo-300 text-sm",
                                    children: (0,
                                    s.jsx)("p", {
                                        className: "text-right",
                                        children: n.isLastPhase ? (0,
                                        s.jsx)("span", {
                                            children: "No phase limit"
                                        }) : ne(n) ? (0,
                                        s.jsxs)("span", {
                                            children: [n.phaseMintLimit, " items"]
                                        }) : (0,
                                        s.jsxs)(s.Fragment, {
                                            children: [(0,
                                            s.jsxs)("span", {
                                                children: [n.whitelistSpots, " Whitelisted"]
                                            }), " ", (0,
                                            s.jsxs)("span", {
                                                children: ["\xb7 ", n.phaseMintLimit, " items"]
                                            }), " ", n.rule && n.rule.properties && n.rule.properties.roles && (0,
                                            s.jsxs)("span", {
                                                className: "block sm:inline-flex",
                                                children: [(0,
                                                s.jsx)("span", {
                                                    className: "hidden sm:inline-block sm:mr-1",
                                                    children: "\xb7"
                                                }), 1 === n.rule.properties.roles.length ? "".concat(n.rule.properties.roles[0].mintLimit, " per\n                                user") : "Variable limit"]
                                            })]
                                        })
                                    })
                                })]
                            })]
                        })]
                    })
                }), (0,
                s.jsx)(q.Z, {
                    id: "pricing-tip",
                    type: "light",
                    effect: "solid",
                    getContent: function() {
                        return (0,
                        s.jsx)("div", {
                            className: "bg-white px-4 py-2 rounded-md",
                            children: (0,
                            s.jsx)("p", {
                                className: "text-grayc w-96",
                                children: "Mint price starts at a set price and gradually increases as users mint and demand rises. Once the price reaches a ceiling, it begins to drop until it finds a floor. This process repeats itself until a fair mint price is found."
                            })
                        })
                    }
                })]
            })
        }
        var ge = n(74931);
        function xe(e, t, n, i, a, s, r) {
            try {
                var c = e[s](r)
                  , o = c.value
            } catch (l) {
                return void n(l)
            }
            c.done ? t(o) : Promise.resolve(o).then(i, a)
        }
        function fe(e) {
            return function() {
                var t = this
                  , n = arguments;
                return new Promise((function(i, a) {
                    var s = e.apply(t, n);
                    function r(e) {
                        xe(s, i, a, r, c, "next", e)
                    }
                    function c(e) {
                        xe(s, i, a, r, c, "throw", e)
                    }
                    r(void 0)
                }
                ))
            }
        }
        var ye = function(e) {
            var t = e.candyMachine
              , n = e.project
              , i = e.tokenBondingKey
              , r = e.isWhitelisted
              , c = e.slippage
              , o = e.mintPrice
              , u = e.activePhase
              , d = (0,
            L.Os)()
              , m = (0,
            L.zs)()
              , p = (0,
            L.Rc)().connection
              , h = (0,
            W.hB)().setVisible
              , g = (0,
            R.useState)(!1)
              , x = g[0]
              , f = g[1]
              , y = (0,
            R.useState)(1)
              , v = y[0]
              , N = y[1]
              , b = (0,
            R.useMemo)((function() {
                var e, n;
                return (null === (e = t.state.endSettings) || void 0 === e ? void 0 : e.number) ? (null === (n = t.state.endSettings) || void 0 === n ? void 0 : n.number) - t.state.itemsRedeemed === 0 : 0 === t.state.itemsAvailable
            }
            ), [t])
              , S = d.connected && (!t || !o || b || x || !u)
              , T = function() {
                var e = fe(a().mark((function e() {
                    var t;
                    return a().wrap((function(e) {
                        for (; ; )
                            switch (e.prev = e.next) {
                            case 0:
                                if (d.publicKey) {
                                    e.next = 2;
                                    break
                                }
                                return e.abrupt("return", {
                                    isTokenIssued: !1,
                                    message: "Wallet is not connected"
                                });
                            case 2:
                                return e.next = 4,
                                B(n._id, d.publicKey.toBase58());
                            case 4:
                                if (!(t = e.sent).data || !t.data.isAllowed) {
                                    e.next = 7;
                                    break
                                }
                                return e.abrupt("return", {
                                    isTokenIssued: !0,
                                    message: t.message
                                });
                            case 7:
                                return e.abrupt("return", {
                                    isTokenIssued: !1,
                                    message: t.message || t.error
                                });
                            case 8:
                            case "end":
                                return e.stop()
                            }
                    }
                    ), e)
                }
                )));
                return function() {
                    return e.apply(this, arguments)
                }
            }()
              , E = function(e) {
                if (!u || !u.rule.properties || !u.userMintLimit)
                    return N(1);
                var t = parseInt(e);
                return isNaN(t) || t < 1 ? N(1) : t > 10 && u.userMintLimit > 10 ? N(10) : t > u.userMintLimit ? N(u.userMintLimit) : void N(t)
            }
              , w = function() {
                var e = fe(a().mark((function e() {
                    var n, s, u, g, x, y, N, b, E;
                    return a().wrap((function(e) {
                        for (; ; )
                            switch (e.prev = e.next) {
                            case 0:
                                if (d.connected) {
                                    e.next = 2;
                                    break
                                }
                                return e.abrupt("return", h(!0));
                            case 2:
                                if (d.publicKey && m) {
                                    e.next = 4;
                                    break
                                }
                                return e.abrupt("return", d.connect());
                            case 4:
                                if (!S && d.publicKey && o) {
                                    e.next = 6;
                                    break
                                }
                                return e.abrupt("return", console.log("[INFO]: Disabled"));
                            case 6:
                                if (n = new l.zt(p,m,{
                                    preflightCommitment: "processed"
                                }),
                                f(!0),
                                s = ge.Am.loading("Minting..."),
                                e.prev = 9,
                                !i || !m) {
                                    e.next = 18;
                                    break
                                }
                                return u = {
                                    tokenBonding: i,
                                    maxPrice: o * (1 + Number(c) / 100)
                                },
                                e.next = 14,
                                O(n, t, d.publicKey, 1, u);
                            case 14:
                                "ERROR" === (g = e.sent).status ? ge.Am.error(g.message, {
                                    id: s,
                                    duration: 1e4
                                }) : "SUCCESS" !== g.status && "INFO" !== g.status || ge.Am.success(g.message, {
                                    id: s,
                                    duration: 3e4
                                }),
                                e.next = 36;
                                break;
                            case 18:
                                if (r) {
                                    e.next = 21;
                                    break
                                }
                                return f(!1),
                                e.abrupt("return", ge.Am.error("User is not whitelisted.", {
                                    id: s
                                }));
                            case 21:
                                return ge.Am.loading("Whitelisting wallet, please wait.", {
                                    id: s
                                }),
                                e.next = 24,
                                T();
                            case 24:
                                if (x = e.sent,
                                y = x.isTokenIssued,
                                N = x.message,
                                !y) {
                                    e.next = 35;
                                    break
                                }
                                return ge.Am.loading("Minting ".concat(v, " item").concat(v > 1 ? "s" : "", "..."), {
                                    id: s
                                }),
                                e.next = 31,
                                O(n, t, d.publicKey, v);
                            case 31:
                                "ERROR" === (b = e.sent).status ? ge.Am.error(b.message, {
                                    id: s,
                                    duration: 1e4
                                }) : "SUCCESS" !== b.status && "INFO" !== b.status || ge.Am.success(b.message, {
                                    id: s,
                                    duration: 3e4
                                }),
                                e.next = 36;
                                break;
                            case 35:
                                ge.Am.error(N, {
                                    id: s
                                });
                            case 36:
                                e.next = 43;
                                break;
                            case 38:
                                e.prev = 38,
                                e.t0 = e.catch(9),
                                E = e.t0.message,
                                ge.Am.error(E, {
                                    duration: 1e4,
                                    id: s
                                }),
                                console.log("error", e.t0);
                            case 43:
                                f(!1);
                            case 44:
                            case "end":
                                return e.stop()
                            }
                    }
                    ), e, null, [[9, 38]])
                }
                )));
                return function() {
                    return e.apply(this, arguments)
                }
            }();
            return (0,
            s.jsxs)("div", {
                className: "flex gap-2",
                children: [u && !ne(u) && (0,
                s.jsxs)("div", {
                    className: "flex flex-row border rounded relative bg-transparent w-24  border-bluec ".concat(S && "opacity-40"),
                    children: [(0,
                    s.jsx)("button", {
                        onClick: function() {
                            return E(v - 1)
                        },
                        className: "bg-grayc2 text-gray-300  ".concat(S ? "cursor-default" : "hover:text-gray-400 hover:bg-gray-800", " h-full w-20 rounded-l-md cursor-pointer outline-none"),
                        disabled: S,
                        children: (0,
                        s.jsx)("span", {
                            className: "m-auto text-2xl font-thin",
                            children: "\u2212"
                        })
                    }), (0,
                    s.jsx)("input", {
                        type: "number",
                        className: "focus:outline-none text-center w-full bg-grayc2 font-semibold text-2xl hover:text-gray-100 focus:text-gray-100 md:text-basecursor-default flex items-center text-gray-300 outline-none",
                        name: "custom-input-number",
                        value: v,
                        onChange: function(e) {
                            return E(e.target.value)
                        },
                        onBlur: function() {
                            return isNaN(v) || v < 1 ? N(1) : v > 10 ? N(10) : void 0
                        },
                        disabled: S
                    }), (0,
                    s.jsx)("button", {
                        onClick: function() {
                            return E(v + 1)
                        },
                        disabled: S,
                        className: "bg-grayc2 text-gray-300  ".concat(S ? "cursor-default" : "hover:text-gray-400 hover:bg-gray-800", " h-full w-20 rounded-r-md cursor-pointer outline-none"),
                        children: (0,
                        s.jsx)("span", {
                            className: "m-auto text-2xl font-thin",
                            children: "+"
                        })
                    })]
                }), (0,
                s.jsx)("button", {
                    type: "button",
                    className: "inline-flex items-center px-4 py-4 justify-center w-full text-2xl futura-bold rounded-md text-white\n         ".concat(S ? "cursor-not-allowed opacity-40" : "cursor-pointer"),
                    style: {
                        background: "linear-gradient(90deg, #2D5BFF -20%, #3E8AFC 35%, #2400FF 105%)"
                    },
                    disabled: !1,
                    onClick: fe(a().mark((function e() {
                        return a().wrap((function(e) {
                            for (; ; )
                                switch (e.prev = e.next) {
                                case 0:
                                    return e.next = 2,
                                    w();
                                case 2:
                                case "end":
                                    return e.stop()
                                }
                        }
                        ), e)
                    }
                    ))),
                    children: d.connected ? o ? b ? "PHASE SOLD OUT" : u ? "MINT" : "NO ACTIVE PHASE" : "LOADING" : "Select Wallet"
                })]
            })
        };
        function ve(e) {
            e.project;
            var t = e.currentSupply
              , n = e.totalSupply;
            return (0,
            s.jsxs)("div", {
                className: "mt-2",
                children: [(0,
                s.jsxs)("div", {
                    className: "flex justify-between text-lg",
                    children: [(0,
                    s.jsx)("span", {
                        className: "text-greenc",
                        children: "Total Minted"
                    }), (0,
                    s.jsxs)("span", {
                        className: "text-greenc",
                        children: ["(", t, "/", n, ")"]
                    })]
                }), (0,
                s.jsxs)("div", {
                    className: "w-full h-8 bg-grayc2 my-2 rounded-lg relative",
                    children: [(0,
                    s.jsxs)("div", {
                        className: "relative",
                        children: [(0,
                        s.jsx)("div", {
                            className: "h-9 rounded-lg absolute z-20",
                            style: {
                                background: "linear-gradient(90deg, #29FFE5 4.49%, rgba(41, 255, 229, 0.14) 92.22%)",
                                width: n ? Math.min(t / n * 100) + "%" : "0%"
                            }
                        }), (0,
                        s.jsx)("div", {
                            className: "h-9 rounded-lg bg-gray-700/50 absolute w-full z-0"
                        })]
                    }), (0,
                    s.jsxs)("p", {
                        className: "text-greenc absolute inset-0 text-center leading-9 text-xl",
                        children: [n ? Math.min(t / n * 100).toFixed(0) : "0", "%"]
                    })]
                }), (0,
                s.jsx)(q.Z, {
                    type: "light",
                    effect: "float",
                    border: !1
                })]
            })
        }
        var Ne = n(56363)
          , be = n(5506);
        function Se(e) {
            var t = e.isModalOpen
              , n = e.toggleModal;
            return (0,
            s.jsx)(G.u.Root, {
                show: t,
                as: R.Fragment,
                children: (0,
                s.jsxs)(Ne.V, {
                    open: t,
                    onClose: function() {
                        return n()
                    },
                    className: "relative z-50",
                    children: [(0,
                    s.jsx)(G.u.Child, {
                        as: R.Fragment,
                        enter: "ease-out duration-300",
                        enterFrom: "opacity-0",
                        enterTo: "opacity-100",
                        leave: "ease-in duration-200",
                        leaveFrom: "opacity-100",
                        leaveTo: "opacity-0",
                        children: (0,
                        s.jsx)("div", {
                            className: "fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
                        })
                    }), (0,
                    s.jsx)("div", {
                        className: "fixed inset-0 flex items-center justify-center p-4 overflow-y-auto",
                        children: (0,
                        s.jsx)(G.u.Child, {
                            as: R.Fragment,
                            enter: "ease-out duration-300",
                            enterFrom: "opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95",
                            enterTo: "opacity-100 translate-y-0 sm:scale-100",
                            leave: "ease-in duration-200",
                            leaveFrom: "opacity-100 translate-y-0 sm:scale-100",
                            leaveTo: "opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95",
                            children: (0,
                            s.jsxs)(Ne.V.Panel, {
                                className: "mx-auto max-w-lg w-full bg-application rounded-md h-2/3 overflow-y-auto no-scrollbar border-8 border-application",
                                children: [(0,
                                s.jsx)("div", {
                                    className: "hidden sm:block absolute top-0 right-0 pt-4 pr-4",
                                    children: (0,
                                    s.jsxs)("button", {
                                        type: "button",
                                        className: "bg-transparent rounded-md text-gray-400 hover:text-gray-100",
                                        onClick: function() {
                                            return n()
                                        },
                                        children: [(0,
                                        s.jsx)("span", {
                                            className: "sr-only",
                                            children: "Close"
                                        }), (0,
                                        s.jsx)(be.Z, {
                                            className: "h-6 w-6",
                                            "aria-hidden": "true"
                                        })]
                                    })
                                }), (0,
                                s.jsxs)("div", {
                                    className: "flex justify-center items-center mt-4",
                                    children: [(0,
                                    s.jsx)("img", {
                                        src: "/imgs/Gem.png",
                                        className: "w-20 h-auto",
                                        alt: "Logo"
                                    }), (0,
                                    s.jsx)("p", {
                                        className: "gradient-text text-3xl futura-bold pb-4 mt-2 -ml-4",
                                        children: "BIFROST"
                                    })]
                                }), (0,
                                s.jsx)("div", {
                                    className: "py-4 px-6 lg:px-8 text-white text-center text-2xl ",
                                    children: "Terms of Service"
                                }), (0,
                                s.jsxs)("div", {
                                    className: "pt-2 pb-6 px-6 lg:px-8 text-white text-sm ",
                                    children: [(0,
                                    s.jsx)("p", {
                                        className: "mb-2",
                                        children: "Disclaimers"
                                    }), (0,
                                    s.jsxs)("div", {
                                        className: "mr-2",
                                        children: [(0,
                                        s.jsx)("p", {
                                            children: "OUR ACCESS TO AND USE OF THE SERVICE IS AT YOUR OWN RISK. YOU UNDERSTAND AND AGREE THAT THE SERVICE IS PROVIDED ON AN \u201cAS IS\u201d AND \u201cAS AVAILABLE\u201d BASIS AND BLOCKSMITH LABS EXPRESSLY DISCLAIMS WARRANTIES OR CONDITIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED. BLOCKSMITH LABS (AND ITS SUPPLIERS) MAKE NO WARRANTY OR REPRESENTATION AND DISCLAIM ALL RESPONSIBILITY FOR WHETHER THE SERVICE: (A) WILL MEET YOUR REQUIREMENTS; (B) WILL BE AVAILABLE ON AN UNINTERRUPTED, TIMELY, SECURE, OR ERROR-FREE BASIS; OR (C) WILL BE ACCURATE, RELIABLE, COMPLETE, LEGAL, OR SAFE. BLOCKSMITH LABS DISCLAIMS ALL OTHER WARRANTIES OR CONDITIONS, EXPRESS OR IMPLIED, INCLUDING, WITHOUT LIMITATION, IMPLIED WARRANTIES OR CONDITIONS OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. BLOCKSMITH LABS WILL NOT BE LIABLE FOR ANY LOSS OF ANY KIND FROM ANY ACTION TAKEN OR TAKEN IN RELIANCE ON MATERIAL OR INFORMATION, CONTAINED ON THE SERVICE. WHILE BLOCKSMITH LABS ATTEMPTS TO MAKE YOUR ACCESS TO AND USE OF THE SERVICE SAFE, BLOCKSMITH LABS CANNOT AND DOES NOT REPRESENT OR WARRANT THAT THE SERVICE, CONTENT, CONTENT LINKED TO OR ASSOCIATED WITH ANY NFTS, OR ANY NFTS YOU INTERACT WITH USING OUR SERVICE OR OUR SERVICE PROVIDERS\u2019 SERVERS ARE FREE OF VIRUSES OR OTHER HARMFUL COMPONENTS. WE CANNOT GUARANTEE THE SECURITY OF ANY DATA THAT YOU DISCLOSE ONLINE. NO ADVICE OR INFORMATION, WHETHER ORAL OR OBTAINED FROM THE BLOCKSMITH LABS PARTIES OR THROUGH THE SERVICE, WILL CREATE ANY WARRANTY OR REPRESENTATION NOT EXPRESSLY MADE HEREIN. YOU ACCEPT THE INHERENT SECURITY RISKS OF PROVIDING INFORMATION AND DEALING ONLINE OVER THE INTERNET AND WILL NOT HOLD BLOCKSMITH LABS RESPONSIBLE FOR ANY BREACH OF SECURITY."
                                        }), (0,
                                        s.jsx)("p", {
                                            className: "mt-2",
                                            children: "WE WILL NOT BE RESPONSIBLE OR LIABLE TO YOU FOR ANY LOSS AND TAKE NO RESPONSIBILITY FOR, AND WILL NOT BE LIABLE TO YOU FOR, ANY USE OF NFTS, CONTENT, AND/OR CONTENT LINKED TO OR ASSOCIATED WITH NFTS, INCLUDING BUT NOT LIMITED TO ANY LOSSES, DAMAGES, OR CLAIMS ARISING FROM: (A) USER ERROR, INCORRECTLY CONSTRUCTED TRANSACTIONS, OR MISTYPED ADDRESSES; (B) SERVER FAILURE OR DATA LOSS; (C) UNAUTHORIZED ACCESS OR USE; (D) ANY UNAUTHORIZED THIRD-PARTY ACTIVITIES, INCLUDING WITHOUT LIMITATION THE USE OF VIRUSES, PHISHING, BRUTEFORCING OR OTHER MEANS OF ATTACK AGAINST THE SERVICE OR NFTS.NFTS EXIST ONLY BY VIRTUE OF THE OWNERSHIP RECORD MAINTAINED IN THE ASSOCIATED BLOCKCHAIN (E.G., SOLANA NETWORK). ANY TRANSFERS OR SALES OCCUR ON THE ASSOCIATED BLOCKCHAIN (E.G., SOLANA). BLOCKSMITH LABS AND/OR ANY OTHER BLOCKSMITH LABS PARTY CANNOT EFFECT OR OTHERWISE CONTROL THE TRANSFER OF TITLE OR RIGHT IN ANY NFTS OR UNDERLYING OR ASSOCIATED CONTENT OR ITEMS.NO BLOCKSMITH LABS PARTY IS RESPONSIBLE OR LIABLE FOR ANY SUSTAINED LOSSES OR INJURY DUE TO VULNERABILITY OR ANY KIND OF FAILURE, ABNORMAL BEHAVIOR OF SOFTWARE (E.G., WALLET, SMART CONTRACT), BLOCKCHAINS OR ANY OTHER FEATURES OF THE NFTS. NO BLOCKSMITH LABS PARTY IS RESPONSIBLE FOR LOSSES OR INJURY DUE TO LATE REPORTS BY DEVELOPERS OR REPRESENTATIVES (OR NO REPORT AT ALL) OF ANY ISSUES WITH THE BLOCKCHAIN SUPPORTING THE NFTS, INCLUDING FORKS, TECHNICAL NODE ISSUES OR ANY OTHER ISSUES HAVING LOSSES OR INJURY AS A RESULT. Some jurisdictions do not allow the exclusion of implied warranties in contracts with consumers, so the above exclusion may not apply to you."
                                        })]
                                    }), (0,
                                    s.jsxs)("div", {
                                        className: "mt-6",
                                        children: [(0,
                                        s.jsx)("p", {
                                            children: "Assumption of Risk"
                                        }), (0,
                                        s.jsxs)("div", {
                                            className: "mr-2 mt-4",
                                            children: [(0,
                                            s.jsx)("p", {
                                                children: "You accept and acknowledge:"
                                            }), (0,
                                            s.jsxs)("ul", {
                                                className: "mr-5 mt-3",
                                                children: [(0,
                                                s.jsx)("li", {
                                                    className: "mt-1",
                                                    children: "\u2022 The value of an NFTs is subjective. Prices of NFTs are subject to volatility and fluctuations in the price of cryptocurrency can also materially and adversely affect NFT prices. You acknowledge that you fully understand this subjectivity and volatility and that you may lose money."
                                                }), (0,
                                                s.jsx)("li", {
                                                    className: "mt-1",
                                                    children: "\u2022 A lack of use or public interest in the creation and development of distributed ecosystems could negatively impact the development of those ecosystems and related applications, and could therefore also negatively impact the potential utility of NFTs."
                                                }), (0,
                                                s.jsx)("li", {
                                                    className: "mt-1",
                                                    children: "\u2022 The regulatory regime governing blockchain technologies, non-fungible tokens, cryptocurrency, and other crypto-based items is uncertain, and new regulations or policies may materially adversely affect the development of the Service and the utility of NFTs."
                                                }), (0,
                                                s.jsx)("li", {
                                                    className: "mt-1",
                                                    children: "\u2022 You are solely responsible for determining what, if any, taxes apply to your transactions. BLOCKSMITH LABS is not responsible for determining the taxes that apply to your NFTs."
                                                }), (0,
                                                s.jsx)("li", {
                                                    className: "mt-1",
                                                    children: "\u2022 There are risks associated with purchasing items associated with content created by third parties through peer-to-peer transactions, including but not limited to, the risk of purchasing counterfeit items, mislabeled items, items that are vulnerable to metadata decay, items on smart contracts with bugs, and items that may become untransferable. You represent and warrant that you have done sufficient research before making any decisions to sell, obtain, transfer, or otherwise interact with any NFTs or accounts/collections."
                                                }), (0,
                                                s.jsx)("li", {
                                                    className: "mt-1",
                                                    children: "\u2022 We do not control the public blockchains that you are interacting with and we do not control certain smart contracts and protocols that may be integral to your ability to complete transactions on these public blockchains. Additionally, blockchain transactions are irreversible and BLOCKSMITH LABS has no ability to reverse any transactions on the blockchain."
                                                }), (0,
                                                s.jsx)("li", {
                                                    className: "mt-1",
                                                    children: "\u2022 There are risks associated with using Internet and blockchain based products, including, but not limited to, the risk associated with hardware, software, and Internet connections, the risk of malicious software introduction, and the risk that third parties may obtain unauthorized access to your third-party wallet or Account. You accept and acknowledge that BLOCKSMITH LABS will not be responsible for any communication failures, disruptions, errors, distortions or delays you may experience when using the Service or any Blockchain network, however caused."
                                                })]
                                            })]
                                        })]
                                    })]
                                })]
                            })
                        })
                    })]
                })
            })
        }
        function Te(e) {
            var t = e.project
              , n = e.activePhase
              , i = e.candyMachine
              , a = e.tokenBonding
              , r = e.livePrice
              , c = (0,
            R.useState)(!1)
              , o = c[0]
              , l = c[1]
              , u = (0,
            R.useState)(!1)
              , d = u[0]
              , m = u[1]
              , p = (0,
            R.useState)("5")
              , h = p[0]
              , g = p[1];
            return (0,
            s.jsxs)(s.Fragment, {
                children: [(0,
                s.jsxs)("div", {
                    className: "flex md:flex-col flex-col-reverse xlg:gap-8 gap-4",
                    children: [(0,
                    s.jsx)("div", {
                        className: "flex flex-col gap-6",
                        children: t.mintPhases.map((function(e) {
                            return (0,
                            s.jsx)(he, {
                                project: t,
                                phase: e,
                                candyMachine: i,
                                livePrice: r,
                                isActivePhase: n && e._id === n._id
                            }, e._id)
                        }
                        ))
                    }), (0,
                    s.jsxs)("div", {
                        className: "flex flex-col w-full rounded-2xl md:px-16 md:py-8 p-4 shadow-lg bg-grayc2 gap-4 mt-3",
                        children: [(0,
                        s.jsx)(ve, {
                            project: t,
                            totalSupply: i.state.itemsAvailable,
                            currentSupply: i.state.itemsRedeemed
                        }), (0,
                        s.jsx)(ye, {
                            candyMachine: i,
                            project: t,
                            tokenBondingKey: null === a || void 0 === a ? void 0 : a.publicKey,
                            isWhitelisted: !!(null === n || void 0 === n ? void 0 : n.userMintLimit),
                            slippage: h || "0",
                            mintPrice: r,
                            activePhase: n
                        }), (0,
                        s.jsxs)("div", {
                            className: "w-full",
                            children: [n && "GATEKEEPER_SOL" !== (null === n || void 0 === n ? void 0 : n.phaseType) && (0,
                            s.jsxs)("div", {
                                className: "flex pb-2 justify-center gap-2 text-white cursor-pointer",
                                onClick: function() {
                                    m(!d)
                                },
                                children: ["Advanced Settings", (0,
                                s.jsx)("img", {
                                    src: "/imgs/arrow-down.svg",
                                    alt: "Down"
                                })]
                            }), d && n && "GATEKEEPER_SOL" !== (null === n || void 0 === n ? void 0 : n.phaseType) && (0,
                            s.jsxs)("div", {
                                children: [(0,
                                s.jsxs)("div", {
                                    className: "w-36 flex p-2 rounded border-2 border-gray-600 mx-auto",
                                    children: [(0,
                                    s.jsx)("span", {
                                        className: "text-gray-600 mr-2",
                                        children: "Slippage"
                                    }), (0,
                                    s.jsx)("input", {
                                        type: "text",
                                        className: "bg-gray-700 rounded-sm text-white text-right w-12 focus-none mr-0.5 px-1",
                                        value: h,
                                        onChange: function(e) {
                                            var t;
                                            ("" === (t = e.target.value) || /^[0-9\b]+$/.test(t)) && g(t)
                                        }
                                    }), (0,
                                    s.jsx)("span", {
                                        className: "text-white",
                                        children: "%"
                                    })]
                                }), (0,
                                s.jsx)("p", {
                                    className: "text-center text-gray-500 py-4",
                                    children: "Your transaction will fail if the price changes unfavorably more than this percentage"
                                })]
                            })]
                        })]
                    }), (0,
                    s.jsxs)("div", {
                        className: "rounded-2xl bg-grayc2 md:px-8 md:py-6 py-4 px-4",
                        children: [(0,
                        s.jsxs)("div", {
                            className: "flex items-center",
                            children: [(0,
                            s.jsx)(de.Z, {
                                className: "h-5 w-5 text-white",
                                "aria-hidden": "true"
                            }), (0,
                            s.jsx)("p", {
                                className: "text-white ml-2",
                                children: "Disclaimers"
                            })]
                        }), (0,
                        s.jsxs)("ul", {
                            className: "text-white text-sm mt-2 list-none",
                            children: [(0,
                            s.jsxs)("li", {
                                className: "mt-3",
                                children: ["By clicking Mint button, you agree our", " ", (0,
                                s.jsx)("span", {
                                    onClick: function() {
                                        return l(!0)
                                    },
                                    className: "text-indigo-400 cursor-pointer",
                                    children: "Terms of Service"
                                }), "."]
                            }), (0,
                            s.jsx)("li", {
                                className: "mt-2",
                                children: "Mint attempts after the collection is sold out will be taxed with 0.01 SOL botting fee."
                            }), t.premintAmount > 0 && (0,
                            s.jsxs)("li", {
                                className: "mt-2",
                                children: [t.premintAmount, " items will be allocated for the project team and will be minted before the first phase."]
                            }), t.isFreezed && (0,
                            s.jsxs)("li", {
                                className: "mt-2",
                                children: ["Your items will be freezed and cannot be transferred until the sale is closed or ", "it's", " sold out."]
                            })]
                        })]
                    }), (0,
                    s.jsxs)("div", {
                        className: "text-center w-full lg:px-24 md:block hidden",
                        children: [(0,
                        s.jsx)("h1", {
                            className: "text-white py-2",
                            children: "How does dynamic pricing work?"
                        }), (0,
                        s.jsx)("p", {
                            className: "text-light",
                            children: "Mint price starts at a set price and gradually increases as users mint and demand rises. Once the price reaches a ceiling, it begins to drop until it finds a floor. This process repeats itself until a fair mint price is found."
                        })]
                    })]
                }), (0,
                s.jsx)(Se, {
                    isModalOpen: o,
                    toggleModal: function() {
                        l(!o)
                    }
                })]
            })
        }
        var Ee = n(98340)
          , we = n(55850)
          , je = n(29009)
          , Ae = n(90088)
          , Oe = n(14888)
          , Re = n(75358)
          , Me = n(83235)
          , Ie = function(e) {
            var t = e.bondingInfo
              , n = e.activePhase;
            return (0,
            s.jsx)("div", {
                className: "my-8",
                children: (0,
                s.jsx)(je.h, {
                    width: "100%",
                    height: 200,
                    children: (0,
                    s.jsxs)(Ae.T, {
                        height: 200,
                        data: t,
                        margin: {
                            top: 0,
                            right: 30,
                            left: 0,
                            bottom: 0
                        },
                        children: [(0,
                        s.jsx)(Oe.u, {
                            content: function(e) {
                                if (!e.active || !e.payload)
                                    return null;
                                var i = e.payload[0].value.toFixed(2) + ("STRATA_FORGE" === (null === n || void 0 === n ? void 0 : n.phaseType) ? " FORGE" : " SOL")
                                  , a = se()(t[e.label].time).format("lll");
                                return (0,
                                s.jsxs)("div", {
                                    className: "bg-white text-light p-3 rounded-xl text-xs",
                                    children: [(0,
                                    s.jsxs)("p", {
                                        className: "label",
                                        children: ["Price: ", i]
                                    }), (0,
                                    s.jsxs)("p", {
                                        className: "label",
                                        children: ["Time: ", a]
                                    })]
                                })
                            }
                        }), (0,
                        s.jsx)(Re.B, {
                            dataKey: "price",
                            name: "Price",
                            type: "number"
                        }), (0,
                        s.jsx)(Me.u, {
                            type: "monotone",
                            dataKey: "price",
                            stroke: "#3FD5FD",
                            fill: "#163443",
                            strokeWidth: "2",
                            dot: !1,
                            className: "border border-slate-600"
                        })]
                    })
                })
            })
        }
          , ke = function(e) {
            var t = e.bondingInfo
              , n = e.activePhase
              , i = e.loadTokenBonding
              , a = e.setLoadTokenBonding
              , r = (0,
            R.useMemo)((function() {
                return t.slice().reverse().slice(0, 10)
            }
            ), [t]);
            return (0,
            s.jsxs)("div", {
                children: [(0,
                s.jsxs)("div", {
                    className: "flex items-center gap-2 py-4",
                    children: [(0,
                    s.jsx)("h4", {
                        className: "text-white text-2xl flex-1",
                        children: "Recent Transactions"
                    }), (0,
                    s.jsx)("div", {
                        className: "flex gap-2 items-center",
                        children: (0,
                        s.jsxs)("button", {
                            onClick: function() {
                                return a(!0)
                            },
                            type: "button",
                            className: "text-white bg-blue-700 hover:bg-blue-800 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 inline-flex items-center",
                            children: [i && (0,
                            s.jsxs)("svg", {
                                role: "status",
                                className: "inline w-4 h-4 mr-3 text-white animate-spin",
                                viewBox: "0 0 100 101",
                                fill: "none",
                                xmlns: "http://www.w3.org/2000/svg",
                                children: [(0,
                                s.jsx)("path", {
                                    d: "M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z",
                                    fill: "#E5E7EB"
                                }), (0,
                                s.jsx)("path", {
                                    d: "M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z",
                                    fill: "currentColor"
                                })]
                            }), i ? "Loading..." : "Reload"]
                        })
                    })]
                }), (0,
                s.jsxs)("table", {
                    className: "table-fixed w-full",
                    children: [(0,
                    s.jsx)("thead", {
                        children: (0,
                        s.jsxs)("tr", {
                            className: "border-b border-slate-600 text-white",
                            children: [(0,
                            s.jsx)("th", {
                                className: "text-left py-4",
                                children: "Time"
                            }), (0,
                            s.jsx)("th", {
                                className: "text-left py-4",
                                children: "Volume"
                            }), (0,
                            s.jsx)("th", {
                                className: "text-left py-4",
                                children: "Price"
                            })]
                        })
                    }), (0,
                    s.jsx)("tbody", {
                        children: r.map((function(e) {
                            return (0,
                            s.jsxs)("tr", {
                                className: "border-b border-slate-600 text-gray-400",
                                children: [(0,
                                s.jsx)("td", {
                                    className: "text-left py-4",
                                    children: se()(e.time).format("lll")
                                }), (0,
                                s.jsx)("td", {
                                    className: "text-left py-4",
                                    children: "1"
                                }), (0,
                                s.jsx)("td", {
                                    className: "text-left py-4",
                                    children: e.price.toFixed(4) + ("STRATA_FORGE" === (null === n || void 0 === n ? void 0 : n.phaseType) ? " FORGE" : " SOL")
                                })]
                            }, e.time)
                        }
                        ))
                    })]
                })]
            })
        };
        function Le() {
            var e, t, n = (e = ["\n  query GetBondingChanges(\n    $address: PublicKey!\n    $startUnixTime: NaiveDateTime!\n    $stopUnixTime: NaiveDateTime!\n    $limit: Int!\n    $offset: Int!\n  ) {\n    enrichedBondingChanges(\n      address: $address\n      startUnixTime: $startUnixTime\n      stopUnixTime: $stopUnixTime\n      limit: $limit\n      offset: $offset\n    ) {\n      reserveChange\n      supplyChange\n      insertTs\n    }\n  }\n"],
            t || (t = e.slice(0)),
            Object.freeze(Object.defineProperties(e, {
                raw: {
                    value: Object.freeze(t)
                }
            })));
            return Le = function() {
                return n
            }
            ,
            n
        }
        function Ce() {
            return (new Date).valueOf() / 1e3
        }
        var Pe = (0,
        Ee.Ps)(Le())
          , De = function(e) {
            var t, n = e.tokenBonding, i = e.activePhase, a = (0,
            R.useState)(Ce()), r = a[0], c = a[1], o = (0,
            R.useState)(!0), l = o[0], u = o[1], d = null === n || void 0 === n ? void 0 : n.baseMint, m = null === n || void 0 === n ? void 0 : n.targetMint, p = (0,
            we.a)(Pe, {
                fetchPolicy: "no-cache",
                nextFetchPolicy: "no-cache",
                variables: {
                    address: n.publicKey,
                    startUnixTime: Math.max(r - 31536e3, (null === n || void 0 === n || null === (t = n.goLiveUnixTime) || void 0 === t ? void 0 : t.toNumber()) || 0),
                    stopUnixTime: r,
                    offset: 0,
                    limit: 1e3
                }
            }), h = p.data, g = (void 0 === h ? {} : h).enrichedBondingChanges, x = (p.error,
            p.loading,
            p.refetch,
            (0,
            R.useMemo)((function() {
                return g && d && m ? g.map((function(e) {
                    return {
                        time: 1e3 * e.insertTs,
                        price: Math.abs(Number(e.reserveChange) / Number(e.supplyChange)) / Math.pow(10, 9)
                    }
                }
                )).filter((function(e) {
                    return NaN !== e.price && e.price !== 1 / 0
                }
                )).sort((function(e, t) {
                    return e.time - t.time
                }
                )) : []
            }
            ), [g, d, m, l]));
            return (0,
            R.useEffect)((function() {
                l && c(Ce())
            }
            ), [l]),
            (0,
            R.useEffect)((function() {
                u(!1)
            }
            ), [x]),
            (0,
            s.jsxs)(s.Fragment, {
                children: [(0,
                s.jsx)(Ie, {
                    bondingInfo: x,
                    activePhase: i
                }), (0,
                s.jsx)(ke, {
                    bondingInfo: x,
                    activePhase: i,
                    loadTokenBonding: l,
                    setLoadTokenBonding: u
                })]
            })
        }
          , Fe = function() {
            return (0,
            s.jsxs)("div", {
                className: "flex flex-col gap-8 md:items-start items-center",
                children: [(0,
                s.jsx)("div", {
                    className: "animate-pulse rounded-3xl bg-grayc w-full h-36"
                }), (0,
                s.jsx)("div", {
                    className: "animate-pulse rounded-3xl bg-grayc w-full h-36"
                }), (0,
                s.jsx)("div", {
                    className: "animate-pulse rounded-3xl bg-grayc w-full h-36"
                }), (0,
                s.jsx)("div", {
                    className: "animate-pulse rounded-3xl bg-grayc w-full h-36"
                })]
            })
        };
        function Be(e) {
            var t = e.project
              , n = e.activePhase
              , i = e.candyMachine
              , a = e.livePrice
              , r = e.tokenBonding
              , c = (e.session,
            (0,
            R.useState)("MINT"))
              , o = c[0]
              , l = c[1]
              , u = (0,
            R.useMemo)((function() {
                return ne(n)
            }
            ), [n]);
            return (0,
            s.jsxs)("div", {
                id: "tab-selector",
                children: [(0,
                s.jsx)(te, {
                    setTab: l,
                    tab: o,
                    isDynamicPricing: u
                }), (0,
                s.jsx)("div", {
                    id: "project-content",
                    className: "MINT" === o ? "block" : "hidden",
                    children: t && i ? (0,
                    s.jsx)(Te, {
                        project: t,
                        activePhase: n,
                        candyMachine: i,
                        livePrice: a,
                        tokenBonding: r
                    }) : (0,
                    s.jsx)(Fe, {})
                }), r && (0,
                s.jsx)("div", {
                    id: "chart-content",
                    className: "CHART" === o ? "block" : "hidden",
                    children: (0,
                    s.jsx)(De, {
                        tokenBonding: r,
                        activePhase: n
                    })
                })]
            })
        }
        function He(e, t, n, i, a, s, r) {
            try {
                var c = e[s](r)
                  , o = c.value
            } catch (l) {
                return void n(l)
            }
            c.done ? t(o) : Promise.resolve(o).then(i, a)
        }
        function Ke(e, t) {
            var n = (0,
            R.useState)()
              , i = n[0]
              , s = n[1]
              , r = function() {
                var e, n = (e = a().mark((function e() {
                    var n;
                    return a().wrap((function(e) {
                        for (; ; )
                            switch (e.prev = e.next) {
                            case 0:
                                if (t) {
                                    e.next = 2;
                                    break
                                }
                                return e.abrupt("return", s(void 0));
                            case 2:
                                return e.next = 4,
                                y(t);
                            case 4:
                                n = e.sent,
                                s(n.price);
                            case 6:
                            case "end":
                                return e.stop()
                            }
                    }
                    ), e)
                }
                )),
                function() {
                    var t = this
                      , n = arguments;
                    return new Promise((function(i, a) {
                        var s = e.apply(t, n);
                        function r(e) {
                            He(s, i, a, r, c, "next", e)
                        }
                        function c(e) {
                            He(s, i, a, r, c, "throw", e)
                        }
                        r(void 0)
                    }
                    ))
                }
                );
                return function() {
                    return n.apply(this, arguments)
                }
            }();
            return (0,
            M.Yz)((function() {
                t && e && (console.log("Refreshing price for ".concat(null === t || void 0 === t ? void 0 : t.toBase58())),
                r())
            }
            ), 3e3),
            {
                price: i || 0
            }
        }
        function Ue(e, t, n, i, a, s, r) {
            try {
                var c = e[s](r)
                  , o = c.value
            } catch (l) {
                return void n(l)
            }
            c.done ? t(o) : Promise.resolve(o).then(i, a)
        }
        function Ye(e, t, n) {
            var i = (0,
            R.useState)()
              , s = i[0]
              , r = i[1]
              , c = function() {
                var e, i = (e = a().mark((function e() {
                    var i, s;
                    return a().wrap((function(e) {
                        for (; ; )
                            switch (e.prev = e.next) {
                            case 0:
                                if (t) {
                                    e.next = 2;
                                    break
                                }
                                return e.abrupt("return", r(void 0));
                            case 2:
                                return e.next = 4,
                                v(t, n);
                            case 4:
                                i = e.sent,
                                (s = i.tokenBonding) && (s.goLiveUnixTime = new l.BN(s.goLiveUnixTime),
                                s.baseMint = new o.PublicKey(s.baseMint),
                                s.baseStorage = new o.PublicKey(s.baseStorage),
                                s.targetMint = new o.PublicKey(s.targetMint),
                                s.publicKey = new o.PublicKey(s.publicKey)),
                                r(s);
                            case 8:
                            case "end":
                                return e.stop()
                            }
                    }
                    ), e)
                }
                )),
                function() {
                    var t = this
                      , n = arguments;
                    return new Promise((function(i, a) {
                        var s = e.apply(t, n);
                        function r(e) {
                            Ue(s, i, a, r, c, "next", e)
                        }
                        function c(e) {
                            Ue(s, i, a, r, c, "throw", e)
                        }
                        r(void 0)
                    }
                    ))
                }
                );
                return function() {
                    return i.apply(this, arguments)
                }
            }();
            return (0,
            R.useEffect)((function() {
                e && (console.log("Refreshing token bonding"),
                c())
            }
            ), [t, e]),
            {
                tokenBonding: s
            }
        }
        function Ge(e, t, n, i, a, s, r) {
            try {
                var c = e[s](r)
                  , o = c.value
            } catch (l) {
                return void n(l)
            }
            c.done ? t(o) : Promise.resolve(o).then(i, a)
        }
        function We() {
            var e = (0,
            c.useSession)()
              , t = e.data
              , n = e.status;
            t && t.error && (0,
            c.signOut)({
                redirect: !1
            });
            var i = (0,
            L.Rc)().connection
              , l = (0,
            L.zs)()
              , u = (0,
            r.useRouter)().query.projectSlug
              , d = K(u, t && t.sub).project
              , m = function() {
                var e, t = (e = a().mark((function e() {
                    var t;
                    return a().wrap((function(e) {
                        for (; ; )
                            switch (e.prev = e.next) {
                            case 0:
                                if (t = window.solana,
                                !((null === l || void 0 === l ? void 0 : l.publicKey) && t._publicKey && t.isPhantom && (null === l || void 0 === l ? void 0 : l.publicKey.toBase58()) !== t._publicKey.toBase58())) {
                                    e.next = 4;
                                    break
                                }
                                return e.next = 4,
                                t.disconnect();
                            case 4:
                            case "end":
                                return e.stop()
                            }
                    }
                    ), e)
                }
                )),
                function() {
                    var t = this
                      , n = arguments;
                    return new Promise((function(i, a) {
                        var s = e.apply(t, n);
                        function r(e) {
                            Ge(s, i, a, r, c, "next", e)
                        }
                        function c(e) {
                            Ge(s, i, a, r, c, "throw", e)
                        }
                        r(void 0)
                    }
                    ))
                }
                );
                return function() {
                    return t.apply(this, arguments)
                }
            }();
            (0,
            M.Yz)((function() {
                m()
            }
            ), 200);
            var p = d && d.mintPhases.find((function(e) {
                return e.isActive && new Date(e.startDate) < new Date && new Date(e.endDate) > new Date
            }
            ))
              , h = (0,
            R.useMemo)((function() {
                return d && d.candyMachineId ? new o.PublicKey(d.candyMachineId) : void 0
            }
            ), [d])
              , g = k(t, l, h, i).candyMachine
              , x = Ye(t, null === g || void 0 === g ? void 0 : g.state.tokenMint).tokenBonding
              , f = Ke(t, null === x || void 0 === x ? void 0 : x.publicKey)
              , y = (0,
            R.useMemo)((function() {
                return ne(p) ? f.price : (null === g || void 0 === g ? void 0 : g.state.price) && (null === g || void 0 === g ? void 0 : g.state.price) / o.LAMPORTS_PER_SOL
            }
            ), [g, f, p, t]);
            return (0,
            s.jsxs)("div", {
                className: "sm:p-8 p-4",
                children: [(0,
                s.jsx)(X, {
                    session: t
                }), (0,
                s.jsx)("div", {
                    className: "lg:container mx-auto md:my-4 my-0 md:p-0 sm:p-8 p-4",
                    children: (0,
                    s.jsxs)("div", {
                        className: "flex gap-6 md:flex-row flex-col justify-evenly my-12",
                        children: [(0,
                        s.jsx)("div", {
                            className: "md:w-2/5 w-full",
                            children: (0,
                            s.jsx)(Q, {
                                project: d
                            })
                        }), (0,
                        s.jsx)("div", {
                            className: "md:w-540 w-full",
                            children: t && d && "authenticated" === n ? (0,
                            s.jsx)(Be, {
                                project: d,
                                activePhase: p,
                                candyMachine: g,
                                tokenBonding: x,
                                livePrice: y,
                                session: t
                            }) : (0,
                            s.jsx)(ee, {
                                isLoading: "loading" === n || !d
                            })
                        })]
                    })
                })]
            })
        }
    },
    15365: function() {}
}, function(e) {
    e.O(0, [655, 885, 735, 870, 17, 133, 22, 774, 888, 179], (function() {
        return t = 6355,
        e(e.s = t);
        var t
    }
    ));
    var t = e.O();
    _N_E = t
}
]);
