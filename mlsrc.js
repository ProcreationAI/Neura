(this["webpackJsonpcandy-machine-mint"] = this["webpackJsonpcandy-machine-mint"] || []).push([[0], {
    134: function(e, n, t) {
        "use strict";
        (function(e) {
            t.d(n, "a", (function() {
                return h
            }
            )),
            t.d(n, "b", (function() {
                return m
            }
            ));
            var i = t(2)
              , a = t(5)
              , r = t(49)
              , o = t(179)
              , s = t(93)
              , c = t(4)
              , d = t(135)
              , l = t(38)
              , u = null;
            Object(o.a)();
            var p = "9bEaH3dJytiUBcPtZ8cJ3bTTvLb9v88qVkBhSDBybHkx"
              , h = (Object({
                NODE_ENV: "production",
                PUBLIC_URL: "",
                WDS_SOCKET_HOST: void 0,
                WDS_SOCKET_PATH: void 0,
                WDS_SOCKET_PORT: void 0,
                FAST_REFRESH: !0,
                REACT_APP_PRESALE_PRICE: "0",
                REACT_APP_WHITELIST_KEY: "",
                REACT_APP_MINT_UUID: "569dafe0-3e5a-4bc6-b069-f4d9f368cdfc",
                REACT_APP_PRICE: "2000000000",
                REACT_APP_INDEX_CAP: "5000",
                REACT_APP_CONFIG_KEY: "9bEaH3dJytiUBcPtZ8cJ3bTTvLb9v88qVkBhSDBybHkx",
                REACT_APP_SOLANA_RPC: "https://twilight-young-forest.solana-mainnet.quiknode.pro/",
                REACT_APP_CANDY_MACHINE_ID: "G6V8noWyidN9R568KKCVsTDYkYXURHANG91Rkj5WbXYP",
                REACT_APP_CONFIG_TIMEOUT: "30",
                REACT_APP_CANDY_START_DATE: "1657314000.0",
                REACT_APP_INDEX_KEY: "Cg6ScJm2hM4jMMLaXa9cum8WVip4wr9dkvrhyHATc72h",
                REACT_APP_SOLANA_NETWORK: "mainnet-beta",
                REACT_APP_SOLANA_VLAWMZ_RPC_HOST: "https://twilight-young-forest.solana-mainnet.quiknode.pro/",
                REACT_APP_PRIMARY_WALLET: "21ycfBeaHKvaT6xDawR74wv5CYH9i8rftd6S3GQ2TZK4",
                REACT_APP_PDA_BUFFER: "1019"
            }).REACT_APP_TOKEN_NAME && Object({
                NODE_ENV: "production",
                PUBLIC_URL: "",
                WDS_SOCKET_HOST: void 0,
                WDS_SOCKET_PATH: void 0,
                WDS_SOCKET_PORT: void 0,
                FAST_REFRESH: !0,
                REACT_APP_PRESALE_PRICE: "0",
                REACT_APP_WHITELIST_KEY: "",
                REACT_APP_MINT_UUID: "569dafe0-3e5a-4bc6-b069-f4d9f368cdfc",
                REACT_APP_PRICE: "2000000000",
                REACT_APP_INDEX_CAP: "5000",
                REACT_APP_CONFIG_KEY: "9bEaH3dJytiUBcPtZ8cJ3bTTvLb9v88qVkBhSDBybHkx",
                REACT_APP_SOLANA_RPC: "https://twilight-young-forest.solana-mainnet.quiknode.pro/",
                REACT_APP_CANDY_MACHINE_ID: "G6V8noWyidN9R568KKCVsTDYkYXURHANG91Rkj5WbXYP",
                REACT_APP_CONFIG_TIMEOUT: "30",
                REACT_APP_CANDY_START_DATE: "1657314000.0",
                REACT_APP_INDEX_KEY: "Cg6ScJm2hM4jMMLaXa9cum8WVip4wr9dkvrhyHATc72h",
                REACT_APP_SOLANA_NETWORK: "mainnet-beta",
                REACT_APP_SOLANA_VLAWMZ_RPC_HOST: "https://twilight-young-forest.solana-mainnet.quiknode.pro/",
                REACT_APP_PRIMARY_WALLET: "21ycfBeaHKvaT6xDawR74wv5CYH9i8rftd6S3GQ2TZK4",
                REACT_APP_PDA_BUFFER: "1019"
            }).REACT_APP_TOKEN_NAME,
            function() {
                var e = Object(a.a)(Object(i.a)().mark((function e(n) {
                    var t, o, s, u, h, b, m, _, x, f, g, y;
                    return Object(i.a)().wrap((function(e) {
                        for (; ; )
                            switch (e.prev = e.next) {
                            case 0:
                                return e.next = 2,
                                n.getAccountInfo(new c.PublicKey(p));
                            case 2:
                                return t = e.sent,
                                o = r.deserializeUnchecked(d.b, d.a, t.data),
                                s = function() {
                                    var e = Object(a.a)(Object(i.a)().mark((function e() {
                                        var t, a;
                                        return Object(i.a)().wrap((function(e) {
                                            for (; ; )
                                                switch (e.prev = e.next) {
                                                case 0:
                                                    return t = new c.PublicKey(o.index_key),
                                                    e.next = 3,
                                                    n.getAccountInfo(t);
                                                case 3:
                                                    if (null !== (a = e.sent)) {
                                                        e.next = 6;
                                                        break
                                                    }
                                                    return e.abrupt("return", 0);
                                                case 6:
                                                    return e.abrupt("return", (a.data[1] << 8) + a.data[0]);
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
                                u = +o.index_cap,
                                e.next = 8,
                                s();
                            case 8:
                                return h = e.sent,
                                b = u - h,
                                m = Math.floor(Date.now() / 1e3),
                                _ = o.staging,
                                x = _.reverse().find((function(e) {
                                    return m > e.time
                                }
                                )),
                                f = _.length - 1 - _.reverse().findIndex((function(e) {
                                    return m > e.time
                                }
                                )),
                                g = x ? _[f + 1] : _[0],
                                o.pda_buf.and(new l(255)).toNumber(),
                                y = {
                                    pda_buf: +o.pda_buf,
                                    index_cap: +o.index_cap,
                                    items_left: b,
                                    index_key: o.index_key,
                                    primary_wallet: o.primary_wallet,
                                    config_key: p,
                                    timeout: o.ctimeout,
                                    price: (null === x || void 0 === x ? void 0 : x.price) || (null === g || void 0 === g ? void 0 : g.price),
                                    token_option: 1,
                                    public: void 0 !== x && null === (null === g || void 0 === g ? void 0 : g.white_list) ? g.time : 0,
                                    presale: void 0 === x && null !== (null === g || void 0 === g ? void 0 : g.white_list) ? g.time : 0,
                                    presalePrice: (null === x || void 0 === x ? void 0 : x.price) || (null === g || void 0 === g ? void 0 : g.price),
                                    isSoldOut: 0 === b,
                                    isActive: void 0 !== x && b > 0,
                                    isPresale: void 0 !== x && null !== (null === x || void 0 === x ? void 0 : x.white_list),
                                    our_wallet: o.our_wallet,
                                    second_wl: o.second_wl,
                                    col_mint: o.collection_key,
                                    stages: _,
                                    active_stage: x,
                                    next_stage: g,
                                    dutch_time: o.dutch_time,
                                    dutch_price: o.dutch_price
                                },
                                e.abrupt("return", y);
                            case 18:
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
              , b = new c.PublicKey("mnKzuL9RMtR6GeSHBfDpnQaefcMsiw7waoTSduKNiXM")
              , m = function() {
                var n = Object(a.a)(Object(i.a)().mark((function n(t, a, r, o, d) {
                    var l, p, h, m, _, x, f, g, y, w, v, k, j, O, A, P, S, T, C, E, R, K, W, N, M, I, B, L, D, z, U, H, F, Y, G, q, V, X, Z, J, Q, $, ee, ne, te, ie, ae, re, oe, se, ce, de, le, ue, pe, he, be, me, _e, xe, fe;
                    return Object(i.a)().wrap((function(n) {
                        for (; ; )
                            switch (n.prev = n.next) {
                            case 0:
                                return fe = function(e) {
                                    return e
                                }
                                ,
                                u = t.publicKey.toBuffer(),
                                l = new c.Connection("https://twilight-young-forest.solana-mainnet.quiknode.pro/"),
                                p = new c.PublicKey("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"),
                                h = new c.PublicKey("minwAEdewYNqagUwzrVBUGWuo277eeSMwEwj76agxYd"),
                                m = new c.PublicKey("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"),
                                _ = c.Keypair.generate(),
                                n.next = 9,
                                c.PublicKey.findProgramAddress([u, s.a.toBuffer(), _.publicKey.toBuffer()], m);
                            case 9:
                                return x = n.sent[0],
                                n.next = 12,
                                c.PublicKey.findProgramAddress([new Uint8Array([109, 101, 116, 97, 100, 97, 116, 97]), p.toBuffer(), _.publicKey.toBuffer()], p);
                            case 12:
                                return f = n.sent[0],
                                n.next = 15,
                                c.PublicKey.findProgramAddress([new Uint8Array([255 & o.pda_buf, (65280 & o.pda_buf) >> 8]), new Uint8Array([97, 117, 116, 104]), h.toBuffer()], h);
                            case 15:
                                return g = n.sent[0],
                                y = new c.PublicKey("11111111111111111111111111111111"),
                                w = new c.PublicKey("SysvarRent111111111111111111111111111111111"),
                                n.next = 20,
                                c.PublicKey.findProgramAddress([new Uint8Array([255 & o.pda_buf, (65280 & o.pda_buf) >> 8]), u, h.toBuffer()], h);
                            case 20:
                                return v = n.sent[0],
                                n.next = 23,
                                c.PublicKey.findProgramAddress([new Uint8Array([108, 116, 105, 109, 101]), u, h.toBuffer()], h);
                            case 23:
                                return k = n.sent[0],
                                n.next = 26,
                                c.PublicKey.findProgramAddress([new Uint8Array([109, 101, 116, 97, 100, 97, 116, 97]), p.toBuffer(), _.publicKey.toBuffer(), new Uint8Array([101, 100, 105, 116, 105, 111, 110])], p);
                            case 26:
                                return j = n.sent[0],
                                O = new c.PublicKey(o.primary_wallet),
                                A = new c.PublicKey(o.index_key),
                                P = new c.PublicKey(o.active_stage.white_list || c.Keypair.generate().publicKey),
                                S = new c.PublicKey(o.config_key),
                                T = new c.PublicKey(o.dao_wallet || "7FHzVCP9eX6zmZjw3qwvmdDMhSvCkLxipQatAqhtbVBf"),
                                C = new c.PublicKey(o.our_wallet || b),
                                E = new c.PublicKey("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"),
                                R = new c.PublicKey("Gdq32GtxXRr9t3BScA6VdtKZ7TFu62d6HBhrNFMZNto9"),
                                void 0 !== o.token_mint_account && o.token_mint_account && (E = new c.PublicKey(o.token_mint_account)),
                                void 0 !== o.token_recip_account && o.token_recip_account && (R = new c.PublicKey(o.token_recip_account)),
                                n.next = 39,
                                c.PublicKey.findProgramAddress([u, s.a.toBuffer(), E.toBuffer()], m);
                            case 39:
                                return K = n.sent[0],
                                W = new c.PublicKey(o.col_mint),
                                n.next = 43,
                                c.PublicKey.findProgramAddress([new Uint8Array([109, 101, 116, 97, 100, 97, 116, 97]), p.toBuffer(), W.toBuffer()], p);
                            case 43:
                                return N = n.sent[0],
                                n.next = 46,
                                c.PublicKey.findProgramAddress([new Uint8Array([109, 101, 116, 97, 100, 97, 116, 97]), p.toBuffer(), W.toBuffer(), new Uint8Array([101, 100, 105, 116, 105, 111, 110])], p);
                            case 46:
                                return M = n.sent[0],
                                Date.now() / 1e3 >= o.public || o.isActive && !o.isPresale ? 127 : 0,
                                I = {
                                    pubkey: t.publicKey,
                                    isSigner: !0,
                                    isWritable: !0
                                },
                                B = {
                                    pubkey: S,
                                    isSigner: !1,
                                    isWritable: !0
                                },
                                L = {
                                    pubkey: O,
                                    isSigner: !1,
                                    isWritable: !0
                                },
                                D = {
                                    pubkey: C,
                                    isSigner: !1,
                                    isWritable: !0
                                },
                                z = {
                                    pubkey: A,
                                    isSigner: !1,
                                    isWritable: !0
                                },
                                U = {
                                    pubkey: P,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                H = {
                                    pubkey: x,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                F = {
                                    pubkey: y,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                Y = {
                                    pubkey: f,
                                    isSigner: !1,
                                    isWritable: !0
                                },
                                G = {
                                    pubkey: _.publicKey,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                q = {
                                    pubkey: p,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                V = {
                                    pubkey: w,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                X = {
                                    pubkey: new c.PublicKey("Sysvar1nstructions1111111111111111111111111"),
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                Z = {
                                    pubkey: s.a,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                J = {
                                    pubkey: v,
                                    isSigner: !1,
                                    isWritable: !0
                                },
                                Q = {
                                    pubkey: k,
                                    isSigner: !1,
                                    isWritable: !0
                                },
                                $ = {
                                    pubkey: j,
                                    isSigner: !1,
                                    isWritable: !0
                                },
                                ee = {
                                    pubkey: T,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                ne = {
                                    pubkey: E,
                                    isSigner: !1,
                                    isWritable: 2 === (2 & d)
                                },
                                te = {
                                    pubkey: K,
                                    isSigner: !1,
                                    isWritable: 2 === (2 & d)
                                },
                                ie = {
                                    pubkey: R,
                                    isSigner: !1,
                                    isWritable: 2 === (2 & d)
                                },
                                ae = {
                                    pubkey: W,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                re = {
                                    pubkey: M,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                oe = {
                                    pubkey: N,
                                    isSigner: !1,
                                    isWritable: !1
                                },
                                se = {
                                    pubkey: g,
                                    isSigner: !1,
                                    isWritable: !0
                                },
                                ce = new c.TransactionInstruction({
                                    keys: [{
                                        pubkey: t.publicKey,
                                        isSigner: !0,
                                        isWritable: !0
                                    }, {
                                        pubkey: _.publicKey,
                                        isSigner: !0,
                                        isWritable: !0
                                    }, {
                                        pubkey: x,
                                        isSigner: !1,
                                        isWritable: !0
                                    }, {
                                        pubkey: s.a,
                                        isSigner: !1,
                                        isWritable: !1
                                    }, {
                                        pubkey: m,
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
                                de = new c.TransactionInstruction({
                                    keys: fe([I, B, L, D, z, U, H, F, Y, G, q, V, X, Z, J, Q, $, ee, ne, te, ie, ae, re, oe, se]),
                                    programId: h,
                                    data: e.from(new Uint8Array([10, d]))
                                }),
                                le = new c.TransactionInstruction({
                                    keys: [],
                                    programId: h,
                                    data: e.from(new Uint8Array([250]))
                                }),
                                (ue = new c.Transaction).add(new c.TransactionInstruction({
                                    keys: [],
                                    programId: new c.PublicKey("ComputeBudget111111111111111111111111111111"),
                                    data: e.from(new Uint8Array([0, 48, 87, 5, 0, 0, 0, 0, 0]))
                                })),
                                ue.add(ce, de, le),
                                n.next = 55,
                                l.getRecentBlockhash();
                            case 55:
                                return pe = n.sent.blockhash,
                                ue.recentBlockhash = pe,
                                ue.feePayer = t.publicKey,
                                ue.sign(_),
                                n.prev = 59,
                                r(!0),
                                n.next = 63,
                                t.signTransaction(ue);
                            case 63:
                                return he = n.sent,
                                n.next = 66,
                                Object(c.sendAndConfirmRawTransaction)(l, he.serialize(), {
                                    commitment: "processed"
                                });
                            case 66:
                                return be = n.sent,
                                console.log(be),
                                n.next = 70,
                                l.getConfirmedTransaction(be, "confirmed");
                            case 70:
                                me = n.sent,
                                _e = me.meta.logMessages.join("").indexOf("timeout") > -1,
                                a(_e ? {
                                    open: !0,
                                    message: "There is a ".concat(o.timeout, " second delay between mints!"),
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
                                xe = "Your transaction wasn't confirmed in 30 seconds. Please check your wallet",
                                void 0 !== n.t0.logs && (xe = n.t0.logs[n.t0.logs.length - 3].split(" ").splice(2).join(" ")).indexOf("0x1") > -1 && (xe = "Not enough Solana."),
                                a({
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
                return function(e, t, i, a, r) {
                    return n.apply(this, arguments)
                }
            }()
        }
        ).call(this, t(13).Buffer)
    },
    135: function(e, n, t) {
        "use strict";
        t.d(n, "a", (function() {
            return c
        }
        )),
        t.d(n, "b", (function() {
            return d
        }
        ));
        var i = t(19)
          , a = t(7)
          , r = t(8)
          , o = t(38)
          , s = Object(a.a)((function e(n) {
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
          , c = Object(a.a)((function e(n) {
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
            this.pda_buf = new o(n.pda_buf,10),
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
            this.config_seed = new o(n.config_seed,10),
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
            var t, a = Object(i.a)(n.staging);
            try {
                for (a.s(); !(t = a.n()).done; ) {
                    var c, d = t.value, l = new s({
                        time: d.time,
                        price: new o(d.price,10),
                        name: d.name,
                        per_wallet: d.per_wallet,
                        pay_type: null !== (c = d.pay_type) && void 0 !== c ? c : 1,
                        token_allotment: d.token_allotment || null,
                        token_name: d.token_name || null,
                        token_mint: d.token_mint || null,
                        token_recip: d.token_recip || null,
                        token_decimals: d.token_decimals || null,
                        token_price: d.token_price || null,
                        white_list: d.white_list || ""
                    });
                    this.staging.push(l)
                }
            } catch (u) {
                a.e(u)
            } finally {
                a.f()
            }
        }
        ))
          , d = new Map([[s, {
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
        }], [c, {
            kind: "struct",
            fields: [["our_cut", "string"], ["sname", "string"], ["symbol", "string"], ["pda_buf", "u64"], ["uri", "string"], ["index_cap", "u16"], ["auth_pda", "pubkeyAsString"], ["index_key", "pubkeyAsString"], ["ctimeout", "u16"], ["config_seed", "u64"], ["primary_wallet", "pubkeyAsString"], ["sfbp", "u16"], ["secondary_wl_index", "u16"], ["collection_key", "pubkeyAsString"], ["creator_1", "pubkeyAsString"], ["creator_1_cut", "u8"], ["shuffle", "u8"], ["hash", "u8"], ["breed", "u8"], ["breed_time", "u32"], ["custom", "u16"], ["skip_time", "u8"], ["our_wallet", "pubkeyAsString"], ["staging", [s]], ["collection_name", "string"], ["creator_2", {
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
    179: function(e, n, t) {
        "use strict";
        t.d(n, "a", (function() {
            return c
        }
        ));
        var i = t(4)
          , a = t(114)
          , r = t.n(a)
          , o = t(49)
          , s = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
          , c = function() {
            o.BinaryReader.prototype.readPubkey = function() {
                var e = this.readFixedArray(32);
                return new i.PublicKey(e)
            }
            ,
            o.BinaryWriter.prototype.writePubkey = function(e) {
                this.writeFixedArray(e.toBuffer())
            }
            ,
            o.BinaryReader.prototype.readPubkeyAsString = function() {
                var e = this.readFixedArray(32);
                return r()(s).encode(e)
            }
            ,
            o.BinaryWriter.prototype.writePubkeyAsString = function(e) {
                this.writeFixedArray(r()(s).decode(e))
            }
        }
    },
    201: function(e, n, t) {},
    202: function(e, n) {},
    203: function(e, n) {},
    228: function(e, n) {},
    229: function(e, n) {},
    278: function(e, n, t) {},
    279: function(e, n, t) {
        "use strict";
        t.r(n);
        var i, a, r, o, s, c, d, l, u, p, h, b, m, _, x, f, g, y = t(1), w = t.n(y), v = t(25), k = t.n(v), j = t(15), O = (t(201),
        t(76)), A = t(29), P = t(30), S = (P.a.a(i || (i = Object(A.a)(["\n  font: bold 14px Arial;\n  text-decoration: none;\n  padding: 8px 24px 8px 24px;\n  width: 150px;\n  background-color: black;\n  color: white;\n  text-align: center;\n  border-radius: 5px;\n"]))),
        P.a.h2(a || (a = Object(A.a)(["\n  fontFamily: verdana;\n"])))), T = P.a.p(r || (r = Object(A.a)(["\n  fontFamily: verdana;\n"]))), C = P.a.div(o || (o = Object(A.a)(["\n  display: flex;\n  width: 100%;\n  height: 100%;\n  min-height: 100vh;\n  position: relative;\n  @media (max-width: 600px) {\n    min-height: 100vh;\n  }\n"]))), E = P.a.div(s || (s = Object(A.a)(["\n  text-align: center;\n  padding-top: 40px;\n  @media (max-width: 1600px) {\n    padding-top: 30px;\n  }\n  img {\n    margin: 0;\n  }\n"]))), R = (P.a.div(c || (c = Object(A.a)(["\n  position: relative;\n  margin-bottom: 50px;\n  @media (max-width: 1600px) {\n    margin-bottom: 30px;\n  }\n  @media (max-width: 600px) {\n    width: 100%;\n  }\n  .NormalClock {\n    width: 600px;\n    @media (max-width: 1600px) {\n      width: 500px;\n    }\n    @media (max-width: 1440px) {\n      width: 450px;\n    }\n    @media (max-width: 600px) {\n      width: 100%;\n    }\n    .NormalUnitContainer {\n      background: #fff;\n      @media (max-width: 600px) {\n        width: 100px;\n        height: auto;\n      }\n      @media (max-width: 420px) {\n        width: 80px;\n      }\n      .NormalupperCard {\n        span {\n          font-size: 60px;\n          font-family: url('https://fonts.googleapis.com/css2?family=Outfit:wght@200&display=swap');\n          color: rgb(17, 35, 53);\n          font-weight: 500;\n          line-height: 1;\n          text-align: center;\n          letter-spacing: 0.025em;\n          @media (max-width: 1600px) {\n            font-size: 36px;\n            line-height: 46px;\n          }\n          @media (max-width: 600px) {\n            font-size: 30px;\n            line-height: 36px;\n          }\n        }\n      }\n      .NormallowerCard {\n        span {\n          font-size: 60px;\n          font-family: url('https://fonts.googleapis.com/css2?family=Outfit:wght@200&display=swap');\n          color: rgb(17, 35, 53);\n          font-weight: 500;\n          line-height: 1;\n          text-align: center;\n          letter-spacing: 0.025em;\n          @media (max-width: 1600px) {\n            font-size: 36px;\n            line-height: 46px;\n          }\n          @media (max-width: 600px) {\n            font-size: 30px;\n            line-height: 36px;\n          }\n        }\n      }\n      .NormalCard {\n        span {\n          font-size: 60px;\n          font-family: url('https://fonts.googleapis.com/css2?family=Outfit:wght@200&display=swap');\n          color: rgb(17, 35, 53);\n          font-weight: 500;\n          line-height: 1;\n          text-align: center;\n          letter-spacing: 0.025em;\n          @media (max-width: 1600px) {\n            font-size: 36px;\n            line-height: 46px;\n          }\n          @media (max-width: 600px) {\n            font-size: 30px;\n            line-height: 36px;\n          }\n        }\n      }\n      .digitLabel {\n        font-size: 14px;\n        font-family: url('https://fonts.googleapis.com/css2?family=Outfit:wght@200&display=swap');\n        color: #889bb7;\n        text-transform: uppercase;\n        text-align: center;\n        font-weight: 500;\n        letter-spacing: 2px;\n        @media (max-width: 1600px) {\n          margin-top: 5px;\n        }\n        @media (max-width: 600px) {\n          letter-spacing: 1px;\n        }\n        @media (max-width: 420px) {\n          font-size: 12px;\n        }\n      }\n    }\n  }\n"]))),
        P.a.div(d || (d = Object(A.a)(["\n  display: flex;\n  max-width: 100%;\n  margin-top: 40px;\n  z-index: 2;\n  margin-bottom: 10px;\n  @media (max-width: 1440px) {\n    margin-top: 30px;\n  }\n  @media (max-width: 600px) {\n    flex-direction: column;\n    width: 100%;\n  }\n\n  @media (max-width: 575px) {\n    flex-direction: column;\n    align-items: center;\n    margin-bottom: 0px;\n    button {\n      width: 100%;\n    }\n  }\n  form {\n    margin-bottom: 10px;\n  }\n  > div {\n    @media (max-width: 600px) {\n      width: 100%;\n    }\n  }\n  form {\n    margin-top: 0;\n    margin-bottom: 0;\n    @media (max-width: 600px) {\n      margin-top: 0;\n      margin-bottom: 0;\n    }\n  }\n  .field-wrapper {\n    @media (max-width: 600px) {\n      width: 100%;\n    }\n    input {\n      background-color: rgb(245, 245, 245);\n      border: transparent;\n      height: 48px;\n      border-radius: 3px;\n      padding-left: 30px;\n      width: 316px;\n      @media (max-width: 600px) {\n        width: 100%;\n        text-align: center;\n      }\n      &::placeholder {\n        font-size: 15px;\n        font-family: url('https://fonts.googleapis.com/css2?family=Outfit:wght@200&display=swap');\n        color: rgb(142, 147, 154);\n      }\n      &:focus {\n        outline: none;\n      }\n    }\n  }\n  button {\n    margin-left: 20px;\n    border-radius: 3px !important;\n    background-color: rgb(51, 51, 51) !important;\n    padding: 13px 33px 15px 34px;\n    height: 48px;\n    transition: all 0.35s ease;\n    background-image: none;\n    &:hover {\n      box-shadow: rgba(51, 51, 51, 0.57) 0px 12px 24px -10px !important;\n    }\n    .btn-text {\n      padding: 4px 0 0;\n    }\n    @media (max-width: 600px) {\n      margin-left: 0;\n      margin-top: 15px;\n    }\n  }\n"]))),
        P.a.div(l || (l = Object(A.a)(["\n  position: relative;\n  padding-bottom: 40px;\n  @media (max-width: 1600px) {\n    padding-bottom: 30px;\n  }\n\n  .social_profiles {\n    justify-content: center;\n    .social_profile_item {\n      border-radius: 50%;\n      background-color: rgb(239, 245, 249);\n      width: 46px;\n      height: 46px;\n      display: flex;\n      justify-content: center;\n      align-items: center;\n      transition: all 0.5s ease;\n      cursor: pointer;\n      @media (max-width: 1440px) {\n        width: 36px;\n        height: 36px;\n      }\n      a {\n        color: rgb(17, 35, 53);\n        font-size: 17px;\n        @media (max-width: 1440px) {\n          font-size: 14px;\n        }\n      }\n      &:hover {\n        background-color: rgb(17, 35, 53);\n        a {\n          color: #fff;\n        }\n      }\n    }\n  }\n  p {\n    margin-top: 30px;\n    font-size: 16px;\n    font-family: url('https://fonts.googleapis.com/css2?family=Outfit:wght@200&display=swap');\n    color: rgb(142, 147, 154);\n    line-height: 1.6;\n    display: flex;\n    justify-content: center;\n    align-items: center;\n    margin-bottom: 0;\n    @media (max-width: 1600px) {\n      margin-top: 15px;\n      font-size: 14px;\n    }\n    @media (max-width: 1440px) {\n      margin-top: 15px;\n    }\n    @media (max-width: 600px) {\n      margin-top: 15px;\n    }\n  }\n"]))),
        P.a.section(u || (u = Object(A.a)(["\n  position: relative;\n  width: 70%;\n  background-image: url(", ");\n  background-size: cover;\n  background-position: top center;\n  order: 1;\n  @media (max-width: 1099px) {\n    width: 100%;\n    position: absolute;\n    top: 0;\n    left: 0;\n    height: 100%;\n    opacity: 0;\n    pointer-events: none;\n  }\n  @media (max-width: 600px) {\n    width: 100%;\n    position: relative;\n    display: none;\n  }\n  img {\n    width: 100%;\n    height: 100%;\n    object-fit: cover;\n    margin-bottom: 0;\n  }\n"])), (function(e) {
            return null === e || void 0 === e ? void 0 : e.image
        }
        ))), K = P.a.section(p || (p = Object(A.a)(["\n  background: ", ";\n  width: 55%;\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  flex-direction: column;\n  order: 2;\n\n  @media (max-width: 1099px) {\n    width: 100%;\n  }\n  .mainContainer {\n    display: flex;\n    justify-content: center;\n    align-items: center;\n    width: 100%;\n    @media (max-width: 600px) {\n      width: 85%;\n    }\n  }\n"])), (function(e) {
            return null === e || void 0 === e ? void 0 : e.background_color
        }
        )), W = P.a.div(h || (h = Object(A.a)(["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n  position: relative;\n  padding: 60px 0;\n  width: 100%;\n  height: 80vh;\n  @media (max-width: 1099px) {\n    margin-left: 15px;\n    margin-right: 15px;\n    min-height: calc(100vh - 300px);\n  }\n  .mainContainer {\n    z-index: 99;\n    position: relative;\n  }\n  h2 {\n    font-size: 48px;\n    font-family: url('https://fonts.googleapis.com/css2?family=Outfit:wght@200&display=swap');\n    color: ", ";\n    line-height: 1.4;\n    text-align: center;\n    max-width: 640px;\n    font-weight: 500;\n    margin-bottom: 20px;\n    @media (max-width: 1600px) {\n      font-size: 36px;\n      max-width: 480px;\n      margin-bottom: 15px;\n    }\n    @media (max-width: 768px) {\n      font-size: 30px;\n      line-height: 1.5;\n      max-width: 430px;\n    }\n    @media (max-width: 480px) {\n      font-size: 24px;\n      line-height: 1.5;\n      max-width: 100%;\n    }\n  }\n  p {\n    font-size: 18px;\n    font-family: url('https://fonts.googleapis.com/css2?family=Outfit:wght@200&display=swap');\n    font-weight: 400;\n    color: ", ";\n    line-height: 1.941;\n    text-align: center;\n    max-width: 480px;\n    @media (max-width: 1600px) {\n      font-size: 16px;\n    }\n    @media (max-width: 768px) {\n      font-size: 16px;\n    }\n    @media (max-width: 480px) {\n      font-size: 15px;\n      max-width: 100%;\n      margin-bottom: 0;\n    }\n  }\n"])), (function(e) {
            return null === e || void 0 === e ? void 0 : e.color
        }
        ), (function(e) {
            return null === e || void 0 === e ? void 0 : e.color
        }
        )), N = t(12), M = t(2), I = t(5), B = t(322), L = t(330), D = t(316), z = t(328), U = t(4), H = t(172), F = t(119), Y = t(134), G = t(320), q = t(317), V = t(180), X = t(312), Z = t(335), J = t(14), Q = Object(X.a)((function(e) {
            return Object(Z.a)({
                root: {
                    display: "flex",
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
              , a = e.onComplete
              , r = Q();
            return n ? Object(J.jsx)(V.a, {
                date: n,
                onComplete: a,
                renderer: function(e) {
                    var n = e.days
                      , a = e.hours
                      , o = e.minutes
                      , s = e.seconds;
                    return a += 24 * n,
                    e.completed ? t ? Object(J.jsx)("span", {
                        className: r.done,
                        children: t
                    }) : null : Object(J.jsxs)("div", {
                        className: r.root,
                        style: i,
                        children: [Object(J.jsxs)(D.a, {
                            elevation: 0,
                            children: [Object(J.jsx)("span", {
                                className: r.item,
                                children: a < 10 ? "0".concat(a) : a
                            }), Object(J.jsx)("span", {
                                children: "hrs"
                            })]
                        }), Object(J.jsxs)(D.a, {
                            elevation: 0,
                            children: [Object(J.jsx)("span", {
                                className: r.item,
                                children: o < 10 ? "0".concat(o) : o
                            }), Object(J.jsx)("span", {
                                children: "mins"
                            })]
                        }), Object(J.jsxs)(D.a, {
                            elevation: 0,
                            children: [Object(J.jsx)("span", {
                                className: r.item,
                                children: s < 10 ? "0".concat(s) : s
                            }), Object(J.jsx)("span", {
                                children: "secs"
                            })]
                        })]
                    })
                }
            }) : null
        }, ee = P.a.div(b || (b = Object(A.a)(["\n  margin-right: 16px;\n"]))), ne = function(e) {
            var n = e.configState;
            return Object(J.jsx)(G.a, {
                container: !0,
                direction: "row",
                justifyContent: "center",
                wrap: "nowrap",
                children: Object(J.jsxs)(G.a, {
                    container: !0,
                    direction: "row",
                    wrap: "nowrap",
                    children: [n && Object(J.jsx)(G.a, {
                        container: !0,
                        direction: "row",
                        wrap: "nowrap",
                        children: Object(J.jsxs)(ee, {
                            children: ["Remaining", Object(J.jsx)(q.a, {
                                variant: "h6",
                                color: "textPrimary",
                                style: {
                                    fontWeight: "bold"
                                },
                                children: "".concat(null === n || void 0 === n ? void 0 : n.items_left)
                            })]
                        })
                    }), Object(J.jsx)($, {
                        date: new Date(1e3 * (null === n || void 0 === n ? void 0 : n.presale)),
                        style: {
                            justifyContent: "flex-end"
                        },
                        status: null !== n && void 0 !== n && n.isSoldOut ? "COMPLETED" : null !== n && void 0 !== n && n.isPresale ? "PRESALE" : null !== n && void 0 !== n && n.isActive ? "LIVE" : ""
                    })]
                })
            })
        }, te = t(314), ie = t(321), ae = Object(P.a)(te.a)(m || (m = Object(A.a)(["\n  width: 100%;\n  height: 60px;\n  margin-top: 10px;\n  margin-bottom: 5px;\n  background: linear-gradient(180deg, #604ae5 0%, #813eee 100%);\n  color: rgba(230, 230, 230, 0);\n  font-size: 16px;\n  font-weight: bold;\n"]))), re = Object(P.a)(te.a)(_ || (_ = Object(A.a)(["\n  width: 100%;\n  height: 60px;\n  margin-top: 10px;\n  margin-bottom: 5px;\n  background: linear-gradient(0deg, #604ae5 0%, #813eee 100%);\n  color: rgba(230, 230, 230, 0);\n  font-size: 16px;\n  font-weight: bold;\n"]))), oe = function(e) {
            var n = e.onMint
              , t = e.configState
              , i = e.isMinting
              , a = e.mintType
              , r = e.whiteListed
              , o = e.mintText
              , s = e.reverse
              , c = (t.active_stage || t.next_stage).white_list
              , d = c && !r
              , l = (null === t || void 0 === t ? void 0 : t.isSoldOut) || i || !(null !== t && void 0 !== t && t.isActive) || c && d;
            return !0 === s ? Object(J.jsx)(re, {
                disabled: l,
                onClick: Object(I.a)(Object(M.a)().mark((function e() {
                    return Object(M.a)().wrap((function(e) {
                        for (; ; )
                            switch (e.prev = e.next) {
                            case 0:
                                return e.next = 2,
                                n(a);
                            case 2:
                            case "end":
                                return e.stop()
                            }
                    }
                    ), e)
                }
                ))),
                children: c && d ? "Wallet not Whitelisted" : null !== t && void 0 !== t && t.isSoldOut ? "SOLD OUT" : i ? Object(J.jsx)(ie.a, {}) : o ? "MINT (" + o + ")" : "MINT"
            }) : Object(J.jsx)(ae, {
                disabled: l,
                onClick: Object(I.a)(Object(M.a)().mark((function e() {
                    return Object(M.a)().wrap((function(e) {
                        for (; ; )
                            switch (e.prev = e.next) {
                            case 0:
                                return e.next = 2,
                                n(a);
                            case 2:
                            case "end":
                                return e.stop()
                            }
                    }
                    ), e)
                }
                ))),
                children: c && d ? "Wallet not Whitelisted" : null !== t && void 0 !== t && t.isSoldOut ? "SOLD OUT" : i ? Object(J.jsx)(ie.a, {}) : o ? "MINT (" + o + ")" : "MINT"
            })
        }, se = Object(P.a)(F.a)(x || (x = Object(A.a)(["\n  width: 100%;\n  height: 60px;\n  margin-top: 10px;\n  margin-bottom: 5px;\n  background: linear-gradient(180deg, #604ae5 0%, #813eee 100%);\n  color: white;\n  font-size: 16px;\n  font-weight: bold;\n"]))), ce = P.a.div(f || (f = Object(A.a)([""]))), de = function(e) {
            var n = Object(y.useState)(!1)
              , t = Object(j.a)(n, 2)
              , i = t[0]
              , a = t[1]
              , r = Object(y.useState)()
              , o = Object(j.a)(r, 2)
              , s = o[0]
              , c = o[1]
              , d = Object(y.useState)({
                open: !1,
                message: "",
                severity: void 0
            })
              , l = Object(j.a)(d, 2)
              , u = l[0]
              , p = l[1]
              , h = Object(y.useState)(!1)
              , b = Object(j.a)(h, 2)
              , m = b[0]
              , _ = b[1]
              , x = Object(H.b)()
              , f = Object(y.useRef)(0)
              , g = Object(y.useMemo)((function() {
                if (x && x.publicKey && x.signAllTransactions && x.signTransaction)
                    return {
                        publicKey: x.publicKey,
                        signAllTransactions: x.signAllTransactions,
                        signTransaction: x.signTransaction
                    }
            }
            ), [x])
              , w = Object(y.useCallback)(Object(I.a)(Object(M.a)().mark((function n() {
                var t, i, a, r, o, s;
                return Object(M.a)().wrap((function(n) {
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
                            if (t = n.sent,
                            !(i = t.active_stage || t.next_stage) || !i.white_list) {
                                n.next = 21;
                                break
                            }
                            return n.next = 9,
                            e.connection.getAccountInfo(new O.b.PublicKey(i.white_list));
                        case 9:
                            a = n.sent,
                            r = x.publicKey.toBytes().slice(0, 9).join(""),
                            _(!1),
                            o = 0,
                            s = a.data.length;
                        case 13:
                            if (!(o < s)) {
                                n.next = 21;
                                break
                            }
                            if (a.data.slice(o, o + 9).join("") !== r) {
                                n.next = 18;
                                break
                            }
                            return _(!0),
                            n.abrupt("break", 21);
                        case 18:
                            o += 10,
                            n.next = 13;
                            break;
                        case 21:
                            c(t);
                        case 22:
                        case "end":
                            return n.stop()
                        }
                }
                ), n)
            }
            ))), [g, e.connection])
              , v = Object(y.useCallback)(function() {
                var e = Object(I.a)(Object(M.a)().mark((function e(n) {
                    return Object(M.a)().wrap((function(e) {
                        for (; ; )
                            switch (e.prev = e.next) {
                            case 0:
                                if (!(x.connected && x.publicKey && s)) {
                                    e.next = 3;
                                    break
                                }
                                return e.next = 3,
                                Object(Y.b)(x, p, a, s, n);
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
            }(), [x, s]);
            Object(y.useEffect)((function() {
                return w(),
                f.current = setInterval((function() {
                    w()
                }
                ), 3e4),
                function() {
                    clearTimeout(f.current)
                }
            }
            ), [g, e.connection, f, w]);
            var k = 0;
            return s && (k = s.isPresale ? s.presalePrice : s.price),
            Object(J.jsxs)(B.a, {
                style: {
                    marginTop: 25
                },
                children: [Object(J.jsx)(B.a, {
                    maxWidth: "xs",
                    style: {
                        position: "relative"
                    },
                    children: Object(J.jsx)(D.a, {
                        style: {
                            padding: 24,
                            backgroundColor: "#151A1F",
                            borderRadius: 6
                        },
                        children: x.connected ? s && Object(J.jsxs)(J.Fragment, {
                            children: [Object(J.jsx)(ne, {
                                configState: s
                            }), Object(J.jsx)(ce, {
                                children: 3 === s.token_option ? Object(J.jsxs)(J.Fragment, {
                                    children: [Object(J.jsx)(oe, {
                                        configState: s,
                                        isMinting: i,
                                        onMint: v,
                                        whiteListed: m,
                                        mintText: "\u25ce " + (k / U.LAMPORTS_PER_SOL).toFixed(3),
                                        mintType: 1
                                    }), Object(J.jsx)("p", {}), Object(J.jsx)(oe, {
                                        configState: s,
                                        isMinting: i,
                                        onMint: v,
                                        whiteListed: m,
                                        mintText: s.token_price + " $" + s.token_name,
                                        mintType: 2,
                                        reverse: !0
                                    })]
                                }) : Object(J.jsx)(oe, {
                                    configState: s,
                                    isMinting: i,
                                    onMint: v,
                                    whiteListed: m,
                                    mintType: s.token_option || 1,
                                    mintText: 1 === s.token_option ? "\u25ce " + (k / U.LAMPORTS_PER_SOL).toFixed(3) : 2 === s.token_option ? s.token_price + " $" + s.token_name : "\u25ce " + (k / U.LAMPORTS_PER_SOL).toFixed(3) + " AND " + s.token_price + " $" + s.token_name
                                })
                            })]
                        }) : Object(J.jsx)(se, {
                            children: "Connect Wallet"
                        })
                    })
                }), Object(J.jsx)(L.a, {
                    open: u.open,
                    autoHideDuration: 6e3,
                    onClose: function() {
                        return p(Object(N.a)(Object(N.a)({}, u), {}, {
                            open: !1
                        }))
                    },
                    children: Object(J.jsx)(z.a, {
                        onClose: function() {
                            return p(Object(N.a)(Object(N.a)({}, u), {}, {
                                open: !1
                            }))
                        },
                        severity: u.severity,
                        children: u.message
                    })
                })]
            })
        }, le = P.a.div(g || (g = Object(A.a)(["\n  @font-face {\n    font-family: 'Outfit';\n    font-style: normal;\n    font-weight: 400;\n    src: url(", ");\n  }\n  max-width: 1200px;\n  margin: 0 auto;\n  width: 85%;\n  @media (min-width: 601px) {\n    width: 90%;\n  }\n  @media (min-width: 993px) {\n    width: 80%;\n  }\n"])), "https://fonts.googleapis.com/css2?family=Outfit:wght@200&display=swap"), ue = t.p + "static/media/transparent_powered_by.7b3d567e.png", pe = t(331), he = t(332), be = t(333), me = t(325), _e = t(326), xe = t(334), fe = t(329), ge = t(183), ye = t(327), we = t(181), ve = t.n(we), ke = Object(ge.a)({
            palette: {
                type: "dark"
            }
        }), je = "mainnet-beta", Oe = "https://twilight-young-forest.solana-mainnet.quiknode.pro/", Ae = new O.b.Connection(Oe), Pe = function() {
            var e = Object(y.useMemo)((function() {
                return Object(U.clusterApiUrl)(je)
            }
            ), [])
              , n = Object(y.useMemo)((function() {
                return [Object(pe.a)(), Object(he.a)(), Object(be.a)(), Object(me.a)({
                    network: je
                }), Object(_e.a)({
                    network: je
                })]
            }
            ), [])
              , t = Object(y.useState)()
              , i = Object(j.a)(t, 2)
              , a = i[0]
              , r = i[1];
            return Object(y.useEffect)((function() {
                ve.a.get("https://monkelabs.io/api/candy-machine-data/569dafe0-3e5a-4bc6-b069-f4d9f368cdfc").then((function(e) {
                    r(e.data)
                }
                ))
            }
            ), []),
            Object(J.jsx)(ye.a, {
                theme: ke,
                children: Object(J.jsxs)(C, {
                    children: [Object(J.jsx)(K, {
                        background_color: a ? a.background_color : "#fff",
                        children: Object(J.jsx)(le, {
                            className: "mainContainer",
                            children: Object(J.jsxs)(W, {
                                color: a ? a.color : "#000",
                                children: [Object(J.jsx)(S, {
                                    children: null === a || void 0 === a ? void 0 : a.mint_header
                                }), Object(J.jsx)(T, {
                                    children: null === a || void 0 === a ? void 0 : a.description
                                }), Object(J.jsx)(xe.a, {
                                    endpoint: e,
                                    children: Object(J.jsx)(fe.a, {
                                        wallets: n,
                                        autoConnect: !0,
                                        children: Object(J.jsx)(F.b, {
                                            children: Object(J.jsx)(de, {
                                                connection: Ae,
                                                rpcHost: Oe
                                            })
                                        })
                                    })
                                }), Object(J.jsx)("a", {
                                    href: "https://monkelabs.io/",
                                    target: "_blank",
                                    rel: "noreferrer",
                                    children: Object(J.jsx)(E, {
                                        children: Object(J.jsx)("img", {
                                            src: ue,
                                            alt: "logo",
                                            height: "45px"
                                        })
                                    })
                                })]
                            })
                        })
                    }), Object(J.jsx)(R, {
                        image: a ? a.mint_image : ""
                    })]
                })
            })
        }, Se = function(e) {
            e && e instanceof Function && t.e(3).then(t.bind(null, 336)).then((function(n) {
                var t = n.getCLS
                  , i = n.getFID
                  , a = n.getFCP
                  , r = n.getLCP
                  , o = n.getTTFB;
                t(e),
                i(e),
                a(e),
                r(e),
                o(e)
            }
            ))
        };
        t(278);
        k.a.render(Object(J.jsx)(w.a.StrictMode, {
            children: Object(J.jsx)(Pe, {})
        }), document.getElementById("root")),
        Se()
    }
}, [[279, 1, 2]]]);
