(this["webpackJsonpcandy-machine-mint"] = this["webpackJsonpcandy-machine-mint"] || []).push([[0], {
    132: function(e, n, t) {
        "use strict";
        (function(e) {
            t.d(n, "a", (function() {
                return h
            }
            )),
            t.d(n, "b", (function() {
                return b
            }
            ));
            var i = t(2)
              , o = t(5)
              , r = t(48)
              , a = t(169)
              , c = t(92)
              , s = t(4)
              , l = t(133)
              , d = t(38)
              , u = null;
            Object(a.a)();
            var p = "4tF8wHEecosodqxnmY9jKuEpzSh4X7hZ5Xg6ZkDtyXw2"
              , h = (Object({
                NODE_ENV: "production",
                PUBLIC_URL: "",
                WDS_SOCKET_HOST: void 0,
                WDS_SOCKET_PATH: void 0,
                WDS_SOCKET_PORT: void 0,
                FAST_REFRESH: !0,
                REACT_APP_PRESALE_PRICE: "0",
                REACT_APP_WHITELIST_KEY: "4sekL4Fd8c2bGfsmsCMxVyZnuTkxXWiuAc7VzycDutZH",
                REACT_APP_MINT_UUID: "940dd753-e5c8-4820-92e4-2a0ff41df1fd",
                REACT_APP_PRICE: "2000000000",
                REACT_APP_INDEX_CAP: "5555",
                REACT_APP_CONFIG_KEY: "4tF8wHEecosodqxnmY9jKuEpzSh4X7hZ5Xg6ZkDtyXw2",
                REACT_APP_SOLANA_RPC: "https://twilight-young-forest.solana-mainnet.quiknode.pro/",
                REACT_APP_CANDY_MACHINE_ID: "G6V8noWyidN9R568KKCVsTDYkYXURHANG91Rkj5WbXYP",
                REACT_APP_CONFIG_TIMEOUT: "30",
                REACT_APP_CANDY_START_DATE: "1657126800.0",
                REACT_APP_INDEX_KEY: "FP4xvEg1mExTUpYrswHWkSz33SjgQiVx7b88e1fiAcJX",
                REACT_APP_SOLANA_NETWORK: "mainnet-beta",
                REACT_APP_SOLANA_VLAWMZ_RPC_HOST: "https://twilight-young-forest.solana-mainnet.quiknode.pro/",
                REACT_APP_PRIMARY_WALLET: "Fyw74FzQ53JZ6HKaLN6rR2VGznjgifScP2PmtoYXrgpw",
                REACT_APP_PDA_BUFFER: "1139"
            }).REACT_APP_TOKEN_NAME && Object({
                NODE_ENV: "production",
                PUBLIC_URL: "",
                WDS_SOCKET_HOST: void 0,
                WDS_SOCKET_PATH: void 0,
                WDS_SOCKET_PORT: void 0,
                FAST_REFRESH: !0,
                REACT_APP_PRESALE_PRICE: "0",
                REACT_APP_WHITELIST_KEY: "4sekL4Fd8c2bGfsmsCMxVyZnuTkxXWiuAc7VzycDutZH",
                REACT_APP_MINT_UUID: "940dd753-e5c8-4820-92e4-2a0ff41df1fd",
                REACT_APP_PRICE: "2000000000",
                REACT_APP_INDEX_CAP: "5555",
                REACT_APP_CONFIG_KEY: "4tF8wHEecosodqxnmY9jKuEpzSh4X7hZ5Xg6ZkDtyXw2",
                REACT_APP_SOLANA_RPC: "https://twilight-young-forest.solana-mainnet.quiknode.pro/",
                REACT_APP_CANDY_MACHINE_ID: "G6V8noWyidN9R568KKCVsTDYkYXURHANG91Rkj5WbXYP",
                REACT_APP_CONFIG_TIMEOUT: "30",
                REACT_APP_CANDY_START_DATE: "1657126800.0",
                REACT_APP_INDEX_KEY: "FP4xvEg1mExTUpYrswHWkSz33SjgQiVx7b88e1fiAcJX",
                REACT_APP_SOLANA_NETWORK: "mainnet-beta",
                REACT_APP_SOLANA_VLAWMZ_RPC_HOST: "https://twilight-young-forest.solana-mainnet.quiknode.pro/",
                REACT_APP_PRIMARY_WALLET: "Fyw74FzQ53JZ6HKaLN6rR2VGznjgifScP2PmtoYXrgpw",
                REACT_APP_PDA_BUFFER: "1139"
            }).REACT_APP_TOKEN_NAME,
            function() {
                var e = Object(o.a)(Object(i.a)().mark((function e(n) {
                    var t, a, c, u, h, m, b, g, x, f, _, y;
                    return Object(i.a)().wrap((function(e) {
                        for (; ; )
                            switch (e.prev = e.next) {
                            case 0:
                                return e.next = 2,
                                n.getAccountInfo(new s.PublicKey(p));
                            case 2:
                                return t = e.sent,
                                a = r.deserializeUnchecked(l.b, l.a, t.data),
                                c = function() {
                                    var e = Object(o.a)(Object(i.a)().mark((function e() {
                                        var t, o;
                                        return Object(i.a)().wrap((function(e) {
                                            for (; ; )
                                                switch (e.prev = e.next) {
                                                case 0:
                                                    return t = new s.PublicKey(a.index_key),
                                                    e.next = 3,
                                                    n.getAccountInfo(t);
                                                case 3:
                                                    if (null !== (o = e.sent)) {
                                                        e.next = 6;
                                                        break
                                                    }
                                                    return e.abrupt("return", 0);
                                                case 6:
                                                    return e.abrupt("return", (o.data[1] << 8) + o.data[0]);
                                                case 7:
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
                                }(),
                                u = +a.index_cap,
                                e.next = 8,
                                c();
                            case 8:
                                return h = e.sent,
                                m = u - h,
                                b = Math.floor(Date.now() / 1e3),
                                g = a.staging,
                                x = g.reverse().find((function(e) {
                                    return b > e.time
                                }
                                )),
                                f = g.length - 1 - g.reverse().findIndex((function(e) {
                                    return b > e.time
                                }
                                )),
                                _ = x ? g[f + 1] : g[0],
                                a.pda_buf.and(new d(255)).toNumber(),
                                y = {
                                    pda_buf: +a.pda_buf,
                                    index_cap: +a.index_cap,
                                    items_left: m,
                                    index_key: a.index_key,
                                    primary_wallet: a.primary_wallet,
                                    config_key: p,
                                    timeout: a.ctimeout,
                                    price: (null === x || void 0 === x ? void 0 : x.price) || (null === _ || void 0 === _ ? void 0 : _.price),
                                    token_option: 1,
                                    public: void 0 !== x && null === (null === _ || void 0 === _ ? void 0 : _.white_list) ? _.time : 0,
                                    presale: void 0 === x && null !== (null === _ || void 0 === _ ? void 0 : _.white_list) ? _.time : 0,
                                    presalePrice: (null === x || void 0 === x ? void 0 : x.price) || (null === _ || void 0 === _ ? void 0 : _.price),
                                    isSoldOut: 0 === m,
                                    isActive: void 0 !== x && m > 0,
                                    isPresale: void 0 !== x && null !== (null === x || void 0 === x ? void 0 : x.white_list),
                                    our_wallet: a.our_wallet,
                                    second_wl: a.second_wl,
                                    col_mint: a.collection_key,
                                    stages: g,
                                    active_stage: x,
                                    next_stage: _,
                                    dutch_time: a.dutch_time,
                                    dutch_price: a.dutch_price
                                },
                                console.log(x, _),
                                console.log(y),
                                e.abrupt("return", y);
                            case 20:
                            case "end":
                                return e.stop()
                            }
                    }
                    ), e)
                }
                )));
                return function(n) {
                    return e.apply(this, arguments)
                }
            }())
              , m = new s.PublicKey("mnKzuL9RMtR6GeSHBfDpnQaefcMsiw7waoTSduKNiXM")
              , b = function() {
                var n = Object(o.a)(Object(i.a)().mark((function n(t, o, r, a, l) {
                    var d, p, h, b, g, x, f, _, y, w, v, j, k, O, A, P, S, T, E, C, R, K, N, W, M, z, I, D, F, L, B, U, H, Y, X, V, G, Z, q, J, Q, $, ee, ne, te, ie, oe, re, ae, ce, se, le, de, ue, pe, he, me, be, ge, xe, fe;
                    return Object(i.a)().wrap((function(n) {
                        for (; ; )
                            switch (n.prev = n.next) {
                            case 0:
                                return fe = function(e) {
                                    return e
                                }
                                ,
                                u = t.publicKey.toBuffer(),
                                d = new s.Connection("https://twilight-young-forest.solana-mainnet.quiknode.pro/"),
                                p = new s.PublicKey("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"),
                                h = new s.PublicKey("miniYQHyKbyrPBftpouZJVo4S1SkoYJoKngtfiJB9yq"),
                                b = new s.PublicKey("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"),
                                g = s.Keypair.generate(),
                                n.next = 9,
                                s.PublicKey.findProgramAddress([u, c.a.toBuffer(), g.publicKey.toBuffer()], b);
                            case 9:
                                return x = n.sent[0],
                                n.next = 12,
                                s.PublicKey.findProgramAddress([new Uint8Array([109, 101, 116, 97, 100, 97, 116, 97]), p.toBuffer(), g.publicKey.toBuffer()], p);
                            case 12:
                                return f = n.sent[0],
                                n.next = 15,
                                s.PublicKey.findProgramAddress([new Uint8Array([255 & a.pda_buf, (65280 & a.pda_buf) >> 8]), new Uint8Array([97, 117, 116, 104]), h.toBuffer()], h);
                            case 15:
                                return _ = n.sent[0],
                                y = new s.PublicKey("11111111111111111111111111111111"),
                                w = new s.PublicKey("SysvarRent111111111111111111111111111111111"),
                                n.next = 20,
                                s.PublicKey.findProgramAddress([new Uint8Array([255 & a.pda_buf, (65280 & a.pda_buf) >> 8]), u, h.toBuffer()], h);
                            case 20:
                                return v = n.sent[0],
                                n.next = 23,
                                s.PublicKey.findProgramAddress([new Uint8Array([108, 116, 105, 109, 101]), u, h.toBuffer()], h);
                            case 23:
                                return j = n.sent[0],
                                n.next = 26,
                                s.PublicKey.findProgramAddress([new Uint8Array([109, 101, 116, 97, 100, 97, 116, 97]), p.toBuffer(), g.publicKey.toBuffer(), new Uint8Array([101, 100, 105, 116, 105, 111, 110])], p);
                            case 26:
                                return k = n.sent[0],
                                O = new s.PublicKey(a.primary_wallet),
                                A = new s.PublicKey(a.index_key),
                                P = new s.PublicKey(a.active_stage.white_list || s.Keypair.generate().publicKey),
                                S = new s.PublicKey(a.config_key),
                                T = new s.PublicKey(a.dao_wallet || "7FHzVCP9eX6zmZjw3qwvmdDMhSvCkLxipQatAqhtbVBf"),
                                E = new s.PublicKey(a.our_wallet || m),
                                C = new s.PublicKey("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"),
                                R = new s.PublicKey("Gdq32GtxXRr9t3BScA6VdtKZ7TFu62d6HBhrNFMZNto9"),
                                void 0 !== a.token_mint_account && a.token_mint_account && (C = new s.PublicKey(a.token_mint_account)),
                                void 0 !== a.token_recip_account && a.token_recip_account && (R = new s.PublicKey(a.token_recip_account)),
                                n.next = 39,
                                s.PublicKey.findProgramAddress([u, c.a.toBuffer(), C.toBuffer()], b);
                            case 39:
                                return K = n.sent[0],
                                N = new s.PublicKey(a.col_mint),
                                n.next = 43,
                                s.PublicKey.findProgramAddress([new Uint8Array([109, 101, 116, 97, 100, 97, 116, 97]), p.toBuffer(), N.toBuffer()], p);
                            case 43:
                                return W = n.sent[0],
                                n.next = 46,
                                s.PublicKey.findProgramAddress([new Uint8Array([109, 101, 116, 97, 100, 97, 116, 97]), p.toBuffer(), N.toBuffer(), new Uint8Array([101, 100, 105, 116, 105, 111, 110])], p);
                            case 46:
                                return M = n.sent[0],
                                Date.now() / 1e3 >= a.public || a.isActive && !a.isPresale ? 127 : 0,
                                z = {
                                    pubkey: t.publicKey,
                                    isSigner: !0,
                                    isWritable: !0
                                },
                                I = {
                                    pubkey: S,
                                    isSigner: !1,
                                    isWritable: !0
                                },
                                D = {
                                    pubkey: O,
                                    isSigner: !1,
                                    isWritable: !0
                                },
                                F = {
                                    pubkey: E,
                                    isSigner: !1,
                                    isWritable: !0
                                },
                                L = {
                                    pubkey: A,
                                    isSigner: !1,
                                    isWritable: !0
                                },
                                B = {
                                    pubkey: P,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                U = {
                                    pubkey: x,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                H = {
                                    pubkey: y,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                Y = {
                                    pubkey: f,
                                    isSigner: !1,
                                    isWritable: !0
                                },
                                X = {
                                    pubkey: g.publicKey,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                V = {
                                    pubkey: p,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                G = {
                                    pubkey: w,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                Z = {
                                    pubkey: new s.PublicKey("Sysvar1nstructions1111111111111111111111111"),
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                q = {
                                    pubkey: c.a,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                J = {
                                    pubkey: v,
                                    isSigner: !1,
                                    isWritable: !0
                                },
                                Q = {
                                    pubkey: j,
                                    isSigner: !1,
                                    isWritable: !0
                                },
                                $ = {
                                    pubkey: k,
                                    isSigner: !1,
                                    isWritable: !0
                                },
                                ee = {
                                    pubkey: T,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                ne = {
                                    pubkey: C,
                                    isSigner: !1,
                                    isWritable: 2 === (2 & l)
                                },
                                te = {
                                    pubkey: K,
                                    isSigner: !1,
                                    isWritable: 2 === (2 & l)
                                },
                                ie = {
                                    pubkey: R,
                                    isSigner: !1,
                                    isWritable: 2 === (2 & l)
                                },
                                oe = {
                                    pubkey: N,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                re = {
                                    pubkey: M,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                ae = {
                                    pubkey: W,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                ce = {
                                    pubkey: _,
                                    isSigner: !1,
                                    isWritable: !0
                                },
                                se = new s.TransactionInstruction({
                                    keys: [{
                                        pubkey: t.publicKey,
                                        isSigner: !0,
                                        isWritable: !0
                                    }, {
                                        pubkey: g.publicKey,
                                        isSigner: !0,
                                        isWritable: !0
                                    }, {
                                        pubkey: x,
                                        isSigner: !1,
                                        isWritable: !0
                                    }, {
                                        pubkey: c.a,
                                        isSigner: !1,
                                        isWritable: !1
                                    }, {
                                        pubkey: b,
                                        isSigner: !1,
                                        isWritable: !1
                                    }, {
                                        pubkey: y,
                                        isSigner: !1,
                                        isWritable: !1
                                    }, {
                                        pubkey: w,
                                        isSigner: !1,
                                        isWritable: !1
                                    }],
                                    programId: h,
                                    data: e.from(new Uint8Array([100]))
                                }),
                                le = new s.TransactionInstruction({
                                    keys: fe([z, I, D, F, L, B, U, H, Y, X, V, G, Z, q, J, Q, $, ee, ne, te, ie, oe, re, ae, ce]),
                                    programId: h,
                                    data: e.from(new Uint8Array([10, l]))
                                }),
                                de = new s.TransactionInstruction({
                                    keys: [],
                                    programId: h,
                                    data: e.from(new Uint8Array([250]))
                                }),
                                (ue = new s.Transaction).add(new s.TransactionInstruction({
                                    keys: [],
                                    programId: new s.PublicKey("ComputeBudget111111111111111111111111111111"),
                                    data: e.from(new Uint8Array([0, 48, 87, 5, 0, 0, 0, 0, 0]))
                                })),
                                ue.add(se, le, de),
                                n.next = 55,
                                d.getRecentBlockhash();
                            case 55:
                                return pe = n.sent.blockhash,
                                ue.recentBlockhash = pe,
                                ue.feePayer = t.publicKey,
                                ue.sign(g),
                                n.prev = 59,
                                r(!0),
                                n.next = 63,
                                t.signTransaction(ue);
                            case 63:
                                return he = n.sent,
                                n.next = 66,
                                Object(s.sendAndConfirmRawTransaction)(d, he.serialize(), {
                                    commitment: "processed",
                                    skipPreflight: !0
                                });
                            case 66:
                                return me = n.sent,
                                console.log(me),
                                n.next = 70,
                                d.getConfirmedTransaction(me, "confirmed");
                            case 70:
                                be = n.sent,
                                ge = be.meta.logMessages.join("").indexOf("timeout") > -1,
                                o(ge ? {
                                    open: !0,
                                    message: "There is a ".concat(a.timeout, " second delay between mints!"),
                                    severity: "error"
                                } : {
                                    open: !0,
                                    message: "Mint Successful!",
                                    severity: "success"
                                }),
                                n.next = 80;
                                break;
                            case 75:
                                n.prev = 75,
                                n.t0 = n.catch(59),
                                xe = "Unknown error occurred. Your transaction wasn't confirmed.",
                                void 0 !== n.t0.logs && (xe = n.t0.logs[n.t0.logs.length - 3].split(" ").splice(2).join(" ")).indexOf("0x1") > -1 && (xe = "Not enough Solana."),
                                o({
                                    open: !0,
                                    message: xe,
                                    severity: "error"
                                });
                            case 80:
                                return n.prev = 80,
                                r(!1),
                                n.finish(80);
                            case 83:
                            case "end":
                                return n.stop()
                            }
                    }
                    ), n, null, [[59, 75, 80, 83]])
                }
                )));
                return function(e, t, i, o, r) {
                    return n.apply(this, arguments)
                }
            }()
        }
        ).call(this, t(14).Buffer)
    },
    133: function(e, n, t) {
        "use strict";
        t.d(n, "a", (function() {
            return s
        }
        )),
        t.d(n, "b", (function() {
            return l
        }
        ));
        var i = t(19)
          , o = t(7)
          , r = t(8)
          , a = t(38)
          , c = Object(o.a)((function e(n) {
            Object(r.a)(this, e),
            this.time = void 0,
            this.price = void 0,
            this.name = void 0,
            this.per_wallet = void 0,
            this.pay_type = void 0,
            this.white_list = void 0,
            this.token_mint = void 0,
            this.token_recip = void 0,
            this.token_allotment = void 0,
            this.token_decimals = void 0,
            this.token_price = void 0,
            this.token_name = void 0,
            this.time = n.time,
            this.price = n.price,
            this.name = n.name,
            this.pay_type = n.pay_type || 1,
            this.per_wallet = n.per_wallet,
            this.white_list = n.white_list || null,
            this.token_mint = n.token_mint || null,
            this.token_recip = n.token_recip || null,
            this.token_decimals = n.token_decimals || null,
            this.token_price = n.token_price || null,
            this.token_name = n.token_name || null,
            this.token_allotment = n.token_allotment || null
        }
        ))
          , s = Object(o.a)((function e(n) {
            Object(r.a)(this, e),
            this.our_cut = void 0,
            this.sname = void 0,
            this.symbol = void 0,
            this.per_wallet = void 0,
            this.pda_buf = void 0,
            this.uri = void 0,
            this.index_cap = void 0,
            this.auth_pda = void 0,
            this.index_key = void 0,
            this.ctimeout = void 0,
            this.primary_wallet = void 0,
            this.sfbp = void 0,
            this.secondary_wl_index = void 0,
            this.collection_key = void 0,
            this.creator_1 = void 0,
            this.creator_1_cut = void 0,
            this.shuffle = void 0,
            this.hash = void 0,
            this.breed = void 0,
            this.breed_time = void 0,
            this.custom = void 0,
            this.skip_time = void 0,
            this.staging = void 0,
            this.collection_name = void 0,
            this.config_seed = void 0,
            this.creator_2 = void 0,
            this.creator_3 = void 0,
            this.creator_4 = void 0,
            this.creator_2_cut = void 0,
            this.creator_3_cut = void 0,
            this.creator_4_cut = void 0,
            this.update_auth = void 0,
            this.our_wallet = void 0,
            this.second_wl = void 0,
            this.dutch_price = void 0,
            this.dutch_time = void 0,
            this.our_cut = n.our_cut,
            this.sname = n.sname,
            this.symbol = n.symbol,
            this.per_wallet = n.per_wallet,
            this.pda_buf = new a(n.pda_buf,10),
            this.uri = n.uri,
            this.index_cap = n.index_cap,
            this.auth_pda = n.auth_pda,
            this.index_key = n.index_key,
            this.primary_wallet = n.primary_wallet,
            this.sfbp = n.sfbp,
            this.secondary_wl_index = n.secondary_wl_index,
            this.collection_key = n.collection_key,
            this.creator_1 = n.creator_1,
            this.creator_1_cut = n.creator_1_cut,
            this.shuffle = n.shuffle,
            this.hash = n.hash,
            this.breed = n.breed || 0,
            this.breed_time = n.breed_time || 0,
            this.custom = n.custom || 0,
            this.skip_time = n.skip_time >= 1 ? 1 : 0,
            this.dutch_price = n.dutch_price,
            this.dutch_time = n.dutch_time,
            this.collection_name = n.collection_name,
            this.ctimeout = n.ctimeout,
            this.config_seed = new a(n.config_seed,10),
            this.creator_2 = (null === n || void 0 === n ? void 0 : n.creator_2) || null,
            this.creator_3 = (null === n || void 0 === n ? void 0 : n.creator_3) || null,
            this.creator_4 = (null === n || void 0 === n ? void 0 : n.creator_4) || null,
            this.creator_2_cut = (null === n || void 0 === n ? void 0 : n.creator_2_cut) || null,
            this.creator_3_cut = (null === n || void 0 === n ? void 0 : n.creator_3_cut) || null,
            this.creator_4_cut = (null === n || void 0 === n ? void 0 : n.creator_4_cut) || null,
            this.update_auth = (null === n || void 0 === n ? void 0 : n.update_auth) || null,
            this.our_wallet = n.our_wallet || "mnKzuL9RMtR6GeSHBfDpnQaefcMsiw7waoTSduKNiXM",
            this.second_wl = (null === n || void 0 === n ? void 0 : n.second_wl) || null,
            this.staging = [];
            var t, o = Object(i.a)(n.staging);
            try {
                for (o.s(); !(t = o.n()).done; ) {
                    var s, l = t.value, d = new c({
                        time: l.time,
                        price: new a(l.price,10),
                        name: l.name,
                        per_wallet: l.per_wallet,
                        pay_type: null !== (s = l.pay_type) && void 0 !== s ? s : 1,
                        token_allotment: l.token_allotment || null,
                        token_name: l.token_name || null,
                        token_mint: l.token_mint || null,
                        token_recip: l.token_recip || null,
                        token_decimals: l.token_decimals || null,
                        token_price: l.token_price || null,
                        white_list: l.white_list || ""
                    });
                    this.staging.push(d)
                }
            } catch (u) {
                o.e(u)
            } finally {
                o.f()
            }
        }
        ))
          , l = new Map([[c, {
            kind: "struct",
            fields: [["time", "u32"], ["price", "u64"], ["name", "string"], ["per_wallet", "u8"], ["pay_type", "u8"], ["token_allotment", {
                kind: "option",
                type: "u16"
            }], ["token_mint", {
                kind: "option",
                type: "pubkeyAsString"
            }], ["token_recip", {
                kind: "option",
                type: "pubkeyAsString"
            }], ["token_decimals", {
                kind: "option",
                type: "u8"
            }], ["token_price", {
                kind: "option",
                type: "u64"
            }], ["token_name", {
                kind: "option",
                type: "string"
            }], ["white_list", {
                kind: "option",
                type: "pubkeyAsString"
            }]]
        }], [s, {
            kind: "struct",
            fields: [["our_cut", "string"], ["sname", "string"], ["symbol", "string"], ["pda_buf", "u64"], ["uri", "string"], ["index_cap", "u16"], ["auth_pda", "pubkeyAsString"], ["index_key", "pubkeyAsString"], ["ctimeout", "u16"], ["config_seed", "u64"], ["primary_wallet", "pubkeyAsString"], ["sfbp", "u16"], ["secondary_wl_index", "u16"], ["collection_key", "pubkeyAsString"], ["creator_1", "pubkeyAsString"], ["creator_1_cut", "u8"], ["shuffle", "u8"], ["hash", "u8"], ["breed", "u8"], ["breed_time", "u32"], ["custom", "u16"], ["skip_time", "u8"], ["our_wallet", "pubkeyAsString"], ["staging", [c]], ["collection_name", "string"], ["creator_2", {
                kind: "option",
                type: "pubkeyAsString"
            }], ["creator_2_cut", {
                kind: "option",
                type: "u8"
            }], ["creator_3", {
                kind: "option",
                type: "pubkeyAsString"
            }], ["creator_3_cut", {
                kind: "option",
                type: "u8"
            }], ["creator_4", {
                kind: "option",
                type: "pubkeyAsString"
            }], ["creator_4_cut", {
                kind: "option",
                type: "u8"
            }], ["update_auth", {
                kind: "option",
                type: "pubkeyAsString"
            }], ["second_wl", {
                kind: "option",
                type: "string"
            }], ["dutch_price", {
                kind: "option",
                type: "u64"
            }], ["dutch_time", {
                kind: "option",
                type: "u16"
            }]]
        }]])
    },
    169: function(e, n, t) {
        "use strict";
        t.d(n, "a", (function() {
            return s
        }
        ));
        var i = t(4)
          , o = t(113)
          , r = t.n(o)
          , a = t(48)
          , c = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
          , s = function() {
            a.BinaryReader.prototype.readPubkey = function() {
                var e = this.readFixedArray(32);
                return new i.PublicKey(e)
            }
            ,
            a.BinaryWriter.prototype.writePubkey = function(e) {
                this.writeFixedArray(e.toBuffer())
            }
            ,
            a.BinaryReader.prototype.readPubkeyAsString = function() {
                var e = this.readFixedArray(32);
                return r()(c).encode(e)
            }
            ,
            a.BinaryWriter.prototype.writePubkeyAsString = function(e) {
                this.writeFixedArray(r()(c).decode(e))
            }
        }
    },
    190: function(e, n, t) {},
    191: function(e, n) {},
    192: function(e, n) {},
    217: function(e, n) {},
    218: function(e, n) {},
    249: function(e, n, t) {},
    250: function(e, n, t) {
        "use strict";
        t.r(n);
        var i, o, r, a, c, s, l, d, u, p, h, m, b, g, x, f, _, y = t(1), w = t.n(y), v = t(25), j = t.n(v), k = (t(190),
        t(91)), O = t(29), A = t(30), P = (A.a.a(i || (i = Object(O.a)(["\n  font: bold 14px Arial;\n  text-decoration: none;\n  padding: 8px 24px 8px 24px;\n  width: 150px;\n  background-color: black;\n  color: white;\n  text-align: center;\n  border-radius: 5px;\n"]))),
        A.a.h2(o || (o = Object(O.a)(["\n  fontFamily: verdana;\n"])))), S = A.a.p(r || (r = Object(O.a)(["\n  fontFamily: verdana;\n"]))), T = A.a.div(a || (a = Object(O.a)(["\n  display: flex;\n  width: 100%;\n  height: 100%;\n  min-height: 100vh;\n  position: relative;\n  @media (max-width: 600px) {\n    min-height: 100vh;\n  }\n"]))), E = A.a.div(c || (c = Object(O.a)(["\n  text-align: center;\n  padding-top: 40px;\n  @media (max-width: 1600px) {\n    padding-top: 30px;\n  }\n  img {\n    margin: 0;\n  }\n"]))), C = (A.a.div(s || (s = Object(O.a)(["\n  position: relative;\n  margin-bottom: 50px;\n  @media (max-width: 1600px) {\n    margin-bottom: 30px;\n  }\n  @media (max-width: 600px) {\n    width: 100%;\n  }\n  .NormalClock {\n    width: 600px;\n    @media (max-width: 1600px) {\n      width: 500px;\n    }\n    @media (max-width: 1440px) {\n      width: 450px;\n    }\n    @media (max-width: 600px) {\n      width: 100%;\n    }\n    .NormalUnitContainer {\n      background: #fff;\n      @media (max-width: 600px) {\n        width: 100px;\n        height: auto;\n      }\n      @media (max-width: 420px) {\n        width: 80px;\n      }\n      .NormalupperCard {\n        span {\n          font-size: 60px;\n          font-family: url('https://fonts.googleapis.com/css2?family=Outfit:wght@200&display=swap');\n          color: rgb(17, 35, 53);\n          font-weight: 500;\n          line-height: 1;\n          text-align: center;\n          letter-spacing: 0.025em;\n          @media (max-width: 1600px) {\n            font-size: 36px;\n            line-height: 46px;\n          }\n          @media (max-width: 600px) {\n            font-size: 30px;\n            line-height: 36px;\n          }\n        }\n      }\n      .NormallowerCard {\n        span {\n          font-size: 60px;\n          font-family: url('https://fonts.googleapis.com/css2?family=Outfit:wght@200&display=swap');\n          color: rgb(17, 35, 53);\n          font-weight: 500;\n          line-height: 1;\n          text-align: center;\n          letter-spacing: 0.025em;\n          @media (max-width: 1600px) {\n            font-size: 36px;\n            line-height: 46px;\n          }\n          @media (max-width: 600px) {\n            font-size: 30px;\n            line-height: 36px;\n          }\n        }\n      }\n      .NormalCard {\n        span {\n          font-size: 60px;\n          font-family: url('https://fonts.googleapis.com/css2?family=Outfit:wght@200&display=swap');\n          color: rgb(17, 35, 53);\n          font-weight: 500;\n          line-height: 1;\n          text-align: center;\n          letter-spacing: 0.025em;\n          @media (max-width: 1600px) {\n            font-size: 36px;\n            line-height: 46px;\n          }\n          @media (max-width: 600px) {\n            font-size: 30px;\n            line-height: 36px;\n          }\n        }\n      }\n      .digitLabel {\n        font-size: 14px;\n        font-family: url('https://fonts.googleapis.com/css2?family=Outfit:wght@200&display=swap');\n        color: #889bb7;\n        text-transform: uppercase;\n        text-align: center;\n        font-weight: 500;\n        letter-spacing: 2px;\n        @media (max-width: 1600px) {\n          margin-top: 5px;\n        }\n        @media (max-width: 600px) {\n          letter-spacing: 1px;\n        }\n        @media (max-width: 420px) {\n          font-size: 12px;\n        }\n      }\n    }\n  }\n"]))),
        A.a.div(l || (l = Object(O.a)(["\n  display: flex;\n  max-width: 100%;\n  margin-top: 40px;\n  z-index: 2;\n  margin-bottom: 10px;\n  @media (max-width: 1440px) {\n    margin-top: 30px;\n  }\n  @media (max-width: 600px) {\n    flex-direction: column;\n    width: 100%;\n  }\n\n  @media (max-width: 575px) {\n    flex-direction: column;\n    align-items: center;\n    margin-bottom: 0px;\n    button {\n      width: 100%;\n    }\n  }\n  form {\n    margin-bottom: 10px;\n  }\n  > div {\n    @media (max-width: 600px) {\n      width: 100%;\n    }\n  }\n  form {\n    margin-top: 0;\n    margin-bottom: 0;\n    @media (max-width: 600px) {\n      margin-top: 0;\n      margin-bottom: 0;\n    }\n  }\n  .field-wrapper {\n    @media (max-width: 600px) {\n      width: 100%;\n    }\n    input {\n      background-color: rgb(245, 245, 245);\n      border: transparent;\n      height: 48px;\n      border-radius: 3px;\n      padding-left: 30px;\n      width: 316px;\n      @media (max-width: 600px) {\n        width: 100%;\n        text-align: center;\n      }\n      &::placeholder {\n        font-size: 15px;\n        font-family: url('https://fonts.googleapis.com/css2?family=Outfit:wght@200&display=swap');\n        color: rgb(142, 147, 154);\n      }\n      &:focus {\n        outline: none;\n      }\n    }\n  }\n  button {\n    margin-left: 20px;\n    border-radius: 3px !important;\n    background-color: rgb(51, 51, 51) !important;\n    padding: 13px 33px 15px 34px;\n    height: 48px;\n    transition: all 0.35s ease;\n    background-image: none;\n    &:hover {\n      box-shadow: rgba(51, 51, 51, 0.57) 0px 12px 24px -10px !important;\n    }\n    .btn-text {\n      padding: 4px 0 0;\n    }\n    @media (max-width: 600px) {\n      margin-left: 0;\n      margin-top: 15px;\n    }\n  }\n"]))),
        A.a.div(d || (d = Object(O.a)(["\n  position: relative;\n  padding-bottom: 40px;\n  @media (max-width: 1600px) {\n    padding-bottom: 30px;\n  }\n\n  .social_profiles {\n    justify-content: center;\n    .social_profile_item {\n      border-radius: 50%;\n      background-color: rgb(239, 245, 249);\n      width: 46px;\n      height: 46px;\n      display: flex;\n      justify-content: center;\n      align-items: center;\n      transition: all 0.5s ease;\n      cursor: pointer;\n      @media (max-width: 1440px) {\n        width: 36px;\n        height: 36px;\n      }\n      a {\n        color: rgb(17, 35, 53);\n        font-size: 17px;\n        @media (max-width: 1440px) {\n          font-size: 14px;\n        }\n      }\n      &:hover {\n        background-color: rgb(17, 35, 53);\n        a {\n          color: #fff;\n        }\n      }\n    }\n  }\n  p {\n    margin-top: 30px;\n    font-size: 16px;\n    font-family: url('https://fonts.googleapis.com/css2?family=Outfit:wght@200&display=swap');\n    color: rgb(142, 147, 154);\n    line-height: 1.6;\n    display: flex;\n    justify-content: center;\n    align-items: center;\n    margin-bottom: 0;\n    @media (max-width: 1600px) {\n      margin-top: 15px;\n      font-size: 14px;\n    }\n    @media (max-width: 1440px) {\n      margin-top: 15px;\n    }\n    @media (max-width: 600px) {\n      margin-top: 15px;\n    }\n  }\n"]))),
        A.a.section(u || (u = Object(O.a)(["\n  position: relative;\n  width: 70%;\n  background-image: url(", ");\n  background-size: cover;\n  background-position: top center;\n  order: 1;\n  @media (max-width: 1099px) {\n    width: 100%;\n    position: absolute;\n    top: 0;\n    left: 0;\n    height: 100%;\n    opacity: 0;\n    pointer-events: none;\n  }\n  @media (max-width: 600px) {\n    width: 100%;\n    position: relative;\n    display: none;\n  }\n  img {\n    width: 100%;\n    height: 100%;\n    object-fit: cover;\n    margin-bottom: 0;\n  }\n"])), (function(e) {
            return null === e || void 0 === e ? void 0 : e.image
        }
        ))), R = A.a.section(p || (p = Object(O.a)(["\n  background: ", ";\n  width: 55%;\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  flex-direction: column;\n  order: 2;\n\n  @media (max-width: 1099px) {\n    width: 100%;\n  }\n  .mainContainer {\n    display: flex;\n    justify-content: center;\n    align-items: center;\n    width: 100%;\n    @media (max-width: 600px) {\n      width: 85%;\n    }\n  }\n"])), (function(e) {
            return null === e || void 0 === e ? void 0 : e.background_color
        }
        )), K = A.a.div(h || (h = Object(O.a)(["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n  position: relative;\n  padding: 60px 0;\n  width: 100%;\n  height: 80vh;\n  @media (max-width: 1099px) {\n    margin-left: 15px;\n    margin-right: 15px;\n    min-height: calc(100vh - 300px);\n  }\n  .mainContainer {\n    z-index: 99;\n    position: relative;\n  }\n  h2 {\n    font-size: 48px;\n    font-family: url('https://fonts.googleapis.com/css2?family=Outfit:wght@200&display=swap');\n    color: ", ";\n    line-height: 1.4;\n    text-align: center;\n    max-width: 640px;\n    font-weight: 500;\n    margin-bottom: 20px;\n    @media (max-width: 1600px) {\n      font-size: 36px;\n      max-width: 480px;\n      margin-bottom: 15px;\n    }\n    @media (max-width: 768px) {\n      font-size: 30px;\n      line-height: 1.5;\n      max-width: 430px;\n    }\n    @media (max-width: 480px) {\n      font-size: 24px;\n      line-height: 1.5;\n      max-width: 100%;\n    }\n  }\n  p {\n    font-size: 18px;\n    font-family: url('https://fonts.googleapis.com/css2?family=Outfit:wght@200&display=swap');\n    font-weight: 400;\n    color: ", ";\n    line-height: 1.941;\n    text-align: center;\n    max-width: 480px;\n    @media (max-width: 1600px) {\n      font-size: 16px;\n    }\n    @media (max-width: 768px) {\n      font-size: 16px;\n    }\n    @media (max-width: 480px) {\n      font-size: 15px;\n      max-width: 100%;\n      margin-bottom: 0;\n    }\n  }\n"])), (function(e) {
            return null === e || void 0 === e ? void 0 : e.color
        }
        ), (function(e) {
            return null === e || void 0 === e ? void 0 : e.color
        }
        )), N = t(13), W = t(2), M = t(5), z = t(15), I = t(293), D = t(301), F = t(287), L = t(299), B = t(4), U = t(162), H = t(118), Y = t(132), X = t(291), V = t(288), G = t(170), Z = t(283), q = t(306), J = t(12), Q = Object(Z.a)((function(e) {
            return Object(q.a)({
                root: {
                    display: "flex",
                    maxHeight: "2rem",
                    padding: e.spacing(0),
                    "& > *": {
                        margin: e.spacing(.5),
                        marginRight: 0,
                        width: e.spacing(6),
                        height: e.spacing(6),
                        display: "flex",
                        flexDirection: "column",
                        alignContent: "center",
                        alignItems: "center",
                        justifyContent: "center",
                        background: "#384457",
                        color: "white",
                        borderRadius: 5,
                        fontSize: 10
                    }
                },
                done: {
                    display: "flex",
                    margin: e.spacing(1),
                    marginRight: 0,
                    padding: e.spacing(1),
                    flexDirection: "column",
                    alignContent: "center",
                    alignItems: "center",
                    maxHeight: "2rem",
                    justifyContent: "center",
                    background: "#384457",
                    color: "white",
                    borderRadius: 5,
                    fontWeight: "bold",
                    fontSize: 18
                },
                item: {
                    fontWeight: "bold",
                    fontSize: 18
                }
            })
        }
        )), $ = function(e) {
            var n = e.date
              , t = e.status
              , i = e.style
              , o = e.onComplete
              , r = Q();
            return n ? Object(J.jsx)(G.a, {
                date: n,
                onComplete: o,
                renderer: function(e) {
                    var n = e.days
                      , o = e.hours
                      , a = e.minutes
                      , c = e.seconds;
                    return o += 24 * n,
                    e.completed ? t ? Object(J.jsx)("span", {
                        className: r.done,
                        children: t
                    }) : null : Object(J.jsxs)("div", {
                        className: r.root,
                        style: i,
                        children: [Object(J.jsxs)(F.a, {
                            elevation: 0,
                            children: [Object(J.jsx)("span", {
                                className: r.item,
                                children: o < 10 ? "0".concat(o) : o
                            }), Object(J.jsx)("span", {
                                children: "hrs"
                            })]
                        }), Object(J.jsxs)(F.a, {
                            elevation: 0,
                            children: [Object(J.jsx)("span", {
                                className: r.item,
                                children: a < 10 ? "0".concat(a) : a
                            }), Object(J.jsx)("span", {
                                children: "mins"
                            })]
                        }), Object(J.jsxs)(F.a, {
                            elevation: 0,
                            children: [Object(J.jsx)("span", {
                                className: r.item,
                                children: c < 10 ? "0".concat(c) : c
                            }), Object(J.jsx)("span", {
                                children: "secs"
                            })]
                        })]
                    })
                }
            }) : null
        }, ee = (A.a.div(m || (m = Object(O.a)(["\n  margin-right: 16px;\n"]))),
        function(e) {
            var n, t, i, o, r = e.configState, a = Object(y.useState)(!1), c = Object(z.a)(a, 2), s = c[0], l = c[1], d = Object(y.useState)(0), u = Object(z.a)(d, 2), p = (u[0],
            u[1],
            Object(y.useState)(0)), h = Object(z.a)(p, 2), m = h[0], b = h[1], g = Object(y.useState)(0), x = Object(z.a)(g, 2), f = x[0], _ = x[1], w = Object(y.useState)(0), v = Object(z.a)(w, 2), j = v[0], k = v[1];
            console.log(r);
            var O = Number(null === r || void 0 === r || null === (n = r.active_stage) || void 0 === n ? void 0 : n.time)
              , A = Number(null === r || void 0 === r || null === (t = r.active_stage) || void 0 === t ? void 0 : t.price) / Math.pow(10, 9)
              , P = Number(null === r || void 0 === r ? void 0 : r.dutch_time)
              , S = Number(null === r || void 0 === r ? void 0 : r.dutch_price) / Math.pow(10, 9)
              , T = Number(null === r || void 0 === r || null === (i = r.active_stage) || void 0 === i ? void 0 : i.token_price) / Math.pow(10, 9)
              , E = "DUTCH" === (null === r || void 0 === r || null === (o = r.active_stage) || void 0 === o ? void 0 : o.token_name)
              , C = function() {
                var e = Math.floor(Number(Date.now()) / 1e3)
                  , n = e >= O;
                l(n);
                var t = Math.floor((e - O) / P)
                  , i = n ? Math.max(A - t * S, T) : A;
                console.log("price", i),
                console.log("priceStep", S),
                console.log("priceStep", T);
                var o = n ? Math.max(i - S, T) : A - S;
                console.log("price", i),
                console.log("next price", o),
                b(parseFloat(i.toFixed(2))),
                _(parseFloat(o.toFixed(2))),
                k(O + (t + 1) * P - e)
            };
            Object(y.useEffect)((function() {
                var e;
                return C(),
                e = setInterval((function() {
                    k((function(e) {
                        return e - 1
                    }
                    ))
                }
                ), 1e3),
                function() {
                    return clearInterval(e)
                }
            }
            ), []),
            Object(y.useEffect)((function() {
                j < 0 && C()
            }
            ), [j]);
            var R = String(j % 60).padStart(2, "0")
              , K = String(Math.floor(j / 60)).padStart(2, "0");
            return E ? Object(J.jsx)(X.a, {
                container: !0,
                direction: "row",
                justifyContent: "center",
                wrap: "nowrap",
                children: Object(J.jsxs)(X.a, {
                    container: !0,
                    direction: "row",
                    wrap: "nowrap",
                    children: [Object(J.jsxs)(X.a, {
                        container: !0,
                        direction: "column",
                        children: ["Price", Object(J.jsxs)(V.a, {
                            variant: "h6",
                            color: "textPrimary",
                            style: {
                                fontWeight: "bold"
                            },
                            children: ["\u25ce ", m]
                        })]
                    }), Object(J.jsxs)(X.a, {
                        container: !0,
                        direction: "column",
                        children: ["Interval", Object(J.jsx)(V.a, {
                            variant: "h6",
                            color: "textPrimary",
                            style: {
                                fontWeight: "bold"
                            },
                            children: s ? "".concat(K, ":").concat(R) : "Pending"
                        })]
                    }), Object(J.jsxs)(X.a, {
                        container: !0,
                        direction: "column",
                        children: ["Next Price", Object(J.jsxs)(V.a, {
                            variant: "h6",
                            color: "textPrimary",
                            style: {
                                fontWeight: "bold"
                            },
                            children: ["\u25ce ", f]
                        })]
                    })]
                })
            }) : Object(J.jsx)(X.a, {
                container: !0,
                direction: "row",
                justifyContent: "center",
                wrap: "nowrap",
                children: Object(J.jsx)(X.a, {
                    container: !0,
                    direction: "row",
                    wrap: "nowrap",
                    children: Object(J.jsx)($, {
                        date: new Date(1e3 * (null === r || void 0 === r ? void 0 : r.presale)),
                        style: {
                            justifyContent: "flex-end"
                        },
                        status: null !== r && void 0 !== r && r.isSoldOut ? "COMPLETED" : null !== r && void 0 !== r && r.isPresale ? "PRESALE" : null !== r && void 0 !== r && r.isActive ? "LIVE" : ""
                    })
                })
            })
        }
        ), ne = t(285), te = t(292), ie = Object(A.a)(ne.a)(b || (b = Object(O.a)(["\n  width: 100%;\n  height: 60px;\n  margin-top: 10px;\n  margin-bottom: 5px;\n  background: linear-gradient(180deg, #604ae5 0%, #813eee 100%);\n  color: rgba(230, 230, 230, 0);\n  font-size: 16px;\n  font-weight: bold;\n"]))), oe = Object(A.a)(ne.a)(g || (g = Object(O.a)(["\n  width: 100%;\n  height: 60px;\n  margin-top: 10px;\n  margin-bottom: 5px;\n  background: linear-gradient(0deg, #604ae5 0%, #813eee 100%);\n  color: rgba(230, 230, 230, 0);\n  font-size: 16px;\n  font-weight: bold;\n"]))), re = function(e) {
            var n = e.onMint
              , t = e.configState
              , i = e.isMinting
              , o = e.mintType
              , r = e.mintText;
            return !0 === e.reverse ? Object(J.jsx)(oe, {
                disabled: (null === t || void 0 === t ? void 0 : t.isSoldOut) || i || !(null !== t && void 0 !== t && t.isActive),
                onClick: Object(M.a)(Object(W.a)().mark((function e() {
                    return Object(W.a)().wrap((function(e) {
                        for (; ; )
                            switch (e.prev = e.next) {
                            case 0:
                                return e.next = 2,
                                n(o);
                            case 2:
                            case "end":
                                return e.stop()
                            }
                    }
                    ), e)
                }
                ))),
                children: null !== t && void 0 !== t && t.isSoldOut ? "SOLD OUT" : i ? Object(J.jsx)(te.a, {}) : r ? "MINT (" + r + ")" : "MINT"
            }) : Object(J.jsx)(ie, {
                disabled: (null === t || void 0 === t ? void 0 : t.isSoldOut) || i || !(null !== t && void 0 !== t && t.isActive),
                onClick: Object(M.a)(Object(W.a)().mark((function e() {
                    return Object(W.a)().wrap((function(e) {
                        for (; ; )
                            switch (e.prev = e.next) {
                            case 0:
                                return e.next = 2,
                                n(o);
                            case 2:
                            case "end":
                                return e.stop()
                            }
                    }
                    ), e)
                }
                ))),
                children: null !== t && void 0 !== t && t.isSoldOut ? "SOLD OUT" : i ? Object(J.jsx)(te.a, {}) : r ? "MINT (" + r + ")" : "MINT"
            })
        }, ae = Object(A.a)(H.a)(x || (x = Object(O.a)(["\n  width: 100%;\n  height: 60px;\n  margin-top: 10px;\n  margin-bottom: 5px;\n  background: linear-gradient(180deg, #604ae5 0%, #813eee 100%);\n  color: white;\n  font-size: 16px;\n  font-weight: bold;\n"]))), ce = A.a.div(f || (f = Object(O.a)([""]))), se = function(e) {
            var n, t = Object(y.useState)(!1), i = Object(z.a)(t, 2), o = i[0], r = i[1], a = Object(y.useState)(), c = Object(z.a)(a, 2), s = c[0], l = c[1], d = Object(y.useState)({
                open: !1,
                message: "",
                severity: void 0
            }), u = Object(z.a)(d, 2), p = u[0], h = u[1], m = Object(U.b)(), b = Object(y.useRef)(0), g = Object(y.useMemo)((function() {
                if (m && m.publicKey && m.signAllTransactions && m.signTransaction)
                    return {
                        publicKey: m.publicKey,
                        signAllTransactions: m.signAllTransactions,
                        signTransaction: m.signTransaction
                    }
            }
            ), [m]), x = Object(y.useCallback)(Object(M.a)(Object(W.a)().mark((function n() {
                var t;
                return Object(W.a)().wrap((function(n) {
                    for (; ; )
                        switch (n.prev = n.next) {
                        case 0:
                            if (g) {
                                n.next = 2;
                                break
                            }
                            return n.abrupt("return");
                        case 2:
                            return n.next = 4,
                            Object(Y.a)(e.connection);
                        case 4:
                            t = n.sent,
                            l(t);
                        case 6:
                        case "end":
                            return n.stop()
                        }
                }
                ), n)
            }
            ))), [g, e.connection]), f = Object(y.useCallback)(function() {
                var e = Object(M.a)(Object(W.a)().mark((function e(n) {
                    return Object(W.a)().wrap((function(e) {
                        for (; ; )
                            switch (e.prev = e.next) {
                            case 0:
                                if (!(m.connected && m.publicKey && s)) {
                                    e.next = 3;
                                    break
                                }
                                return e.next = 3,
                                Object(Y.b)(m, h, r, s, n);
                            case 3:
                            case "end":
                                return e.stop()
                            }
                    }
                    ), e)
                }
                )));
                return function(n) {
                    return e.apply(this, arguments)
                }
            }(), [m, s]);
            Object(y.useEffect)((function() {
                return x(),
                b.current = setInterval((function() {
                    x()
                }
                ), 3e4),
                function() {
                    clearTimeout(b.current)
                }
            }
            ), [g, e.connection, b, x]);
            var _ = 0;
            return s && (_ = s.isPresale ? s.presalePrice : s.price),
            Object(J.jsxs)(I.a, {
                style: {
                    marginTop: 25
                },
                children: [Object(J.jsx)(I.a, {
                    maxWidth: "xs",
                    style: {
                        position: "relative"
                    },
                    children: Object(J.jsx)(F.a, {
                        style: {
                            padding: 24,
                            backgroundColor: "#151A1F",
                            borderRadius: 6
                        },
                        children: m.connected ? s && Object(J.jsxs)(J.Fragment, {
                            children: [Object(J.jsx)(ee, {
                                configState: s
                            }), Object(J.jsx)(ce, {
                                children: 3 === s.token_option ? Object(J.jsxs)(J.Fragment, {
                                    children: [Object(J.jsx)(re, {
                                        configState: s,
                                        isMinting: o,
                                        onMint: f,
                                        mintText: "\u25ce " + (_ / B.LAMPORTS_PER_SOL).toFixed(3),
                                        mintType: 1
                                    }), Object(J.jsx)("p", {}), Object(J.jsx)(re, {
                                        configState: s,
                                        isMinting: o,
                                        onMint: f,
                                        mintText: s.token_price + " $" + s.token_name,
                                        mintType: 2,
                                        reverse: !0
                                    })]
                                }) : Object(J.jsx)(re, {
                                    configState: s,
                                    isMinting: o,
                                    onMint: f,
                                    mintType: s.token_option || 1,
                                    mintText: "DUTCH" == (null === s || void 0 === s || null === (n = s.active_stage) || void 0 === n ? void 0 : n.token_name) ? "" : 1 === s.token_option ? "\u25ce " + (_ / B.LAMPORTS_PER_SOL).toFixed(3) : 2 === s.token_option ? s.token_price + " $" + s.token_name : "\u25ce " + (_ / B.LAMPORTS_PER_SOL).toFixed(3) + " AND " + s.token_price + " $" + s.token_name
                                })
                            })]
                        }) : Object(J.jsx)(ae, {
                            children: "Connect Wallet"
                        })
                    })
                }), Object(J.jsx)(D.a, {
                    open: p.open,
                    autoHideDuration: 6e3,
                    onClose: function() {
                        return h(Object(N.a)(Object(N.a)({}, p), {}, {
                            open: !1
                        }))
                    },
                    children: Object(J.jsx)(L.a, {
                        onClose: function() {
                            return h(Object(N.a)(Object(N.a)({}, p), {}, {
                                open: !1
                            }))
                        },
                        severity: p.severity,
                        children: p.message
                    })
                })]
            })
        }, le = A.a.div(_ || (_ = Object(O.a)(["\n  @font-face {\n    font-family: 'Outfit';\n    font-style: normal;\n    font-weight: 400;\n    src: url(", ");\n  }\n  max-width: 1200px;\n  margin: 0 auto;\n  width: 85%;\n  @media (min-width: 601px) {\n    width: 90%;\n  }\n  @media (min-width: 993px) {\n    width: 80%;\n  }\n"])), "https://fonts.googleapis.com/css2?family=Outfit:wght@200&display=swap"), de = t.p + "static/media/transparent_powered_by.7b3d567e.png", ue = t(302), pe = t(303), he = t(304), me = t(296), be = t(297), ge = t(305), xe = t(300), fe = t(172), _e = t(298), ye = t.p + "static/media/Background.7655f58b.png", we = Object(fe.a)({
            palette: {
                type: "dark"
            }
        }), ve = "mainnet-beta", je = "https://twilight-young-forest.solana-mainnet.quiknode.pro/", ke = new k.b.Connection(je), Oe = function() {
            var e = Object(y.useMemo)((function() {
                return Object(B.clusterApiUrl)(ve)
            }
            ), [])
              , n = Object(y.useMemo)((function() {
                return [Object(ue.a)(), Object(pe.a)(), Object(he.a)(), Object(me.a)({
                    network: ve
                }), Object(be.a)({
                    network: ve
                })]
            }
            ), []);
            return Object(J.jsx)(_e.a, {
                theme: we,
                children: Object(J.jsxs)(T, {
                    children: [Object(J.jsx)(R, {
                        background_color: "#000",
                        children: Object(J.jsx)(le, {
                            className: "mainContainer",
                            children: Object(J.jsxs)(K, {
                                color: "#fff",
                                children: [Object(J.jsx)(P, {
                                    children: "HYPE: Primates Embassy"
                                }), Object(J.jsx)(S, {
                                    children: "The Embassy is made up of 5,555 young primates. We are professional investors and builders with fresh ideas that will revolutionize the NFT ecosystem in both a rising and falling market, providing passive income to holders."
                                }), Object(J.jsx)(S, {
                                    children: "Dutch Auction will hit a floor of \u25ce2"
                                }), Object(J.jsx)(ge.a, {
                                    endpoint: e,
                                    children: Object(J.jsx)(xe.a, {
                                        wallets: n,
                                        autoConnect: !0,
                                        children: Object(J.jsx)(H.b, {
                                            children: Object(J.jsx)(se, {
                                                connection: ke,
                                                rpcHost: je
                                            })
                                        })
                                    })
                                }), Object(J.jsx)("a", {
                                    href: "https://monkelabs.io/",
                                    target: "_blank",
                                    rel: "noreferrer",
                                    children: Object(J.jsx)(E, {
                                        children: Object(J.jsx)("img", {
                                            src: de,
                                            alt: "logo",
                                            height: "45px"
                                        })
                                    })
                                })]
                            })
                        })
                    }), Object(J.jsx)(C, {
                        image: ye
                    })]
                })
            })
        }, Ae = function(e) {
            e && e instanceof Function && t.e(3).then(t.bind(null, 307)).then((function(n) {
                var t = n.getCLS
                  , i = n.getFID
                  , o = n.getFCP
                  , r = n.getLCP
                  , a = n.getTTFB;
                t(e),
                i(e),
                o(e),
                r(e),
                a(e)
            }
            ))
        };
        t(249);
        j.a.render(Object(J.jsx)(w.a.StrictMode, {
            children: Object(J.jsx)(Oe, {})
        }), document.getElementById("root")),
        Ae()
    }
}, [[250, 1, 2]]]);
