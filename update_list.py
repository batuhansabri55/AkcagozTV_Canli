function parser() {
    if (Core.jsParser.thread.isInterrupted()) {
        return;
    }
    consolelog("--------------------Parser Function Start--------------------");
    if (url(["stream.tvcdn.net"], 0x1)) {
        url("http://", "https://");
    }
    consolelog(0x5, url());
    consolelog(0x6, g.getLang());
    consolelog(0x7, sub());
    consolelog(headers());
    try {
        if (headers() == 0x0) {
            try {
                Core.mainUrlForReferer = url();
            } catch (_0x48632d) {}
            headers("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36");
            headers('Referer', baseUrl(url()));
            headers("base", "aHR0cHM6Ly9zZXlpcnR1cmsubmV0L3Jvb3RjaGVjay9hbmRyb2lkLnBocA");
        }
        g.logHeader();
        consolelog("--------------------Parser Function End--------------------");
        if (isPreview() && !url(["https://"], 0x1)) {
            var _0x443f96 = atob(reverseString(fetch(atob(headers('base') + '='))));
            url(_0x443f96 + "sey/back/getImdb.php?id=" + url());
            url(fetch());
            if (url(['|'], 0x1)) {
                url("https://www.youtube.com/watch?v=" + url().split('|')[0x1]);
            } else {
                url("https://imdb.com/title/tt" + url());
                headers('Referer', 'https://imdb.com');
            }
        }
        url("?wfilmizle", '');
        url("?atv", '');
        if (url(["atv.com.tr", "a2tv", "minikago", "minikacocuk", "vavtv.com.tr"], 0x1) && !url([".m3u8"], 0x1)) {
            atv();
        } else {
            if (url(['kanald.com'], 0x1) && !url(['.m3u8'], 0x1)) {
                kanald();
            } else {
                if (url(["startv.com.tr", "ntv.com.tr"], 0x1) && !url([".m3u8"], 0x1) && !url(["womantv"], 0x1)) {
                    startv();
                } else {
                    if (url(['showtv.com', "showturk.com", "showmax.com"], 0x1) && !url([".m3u8"], 0x1)) {
                        showtv();
                    } else {
                        if (url(["nowtv.com"], 0x1) && !url(['.m3u8'], 0x1)) {
                            nowtv();
                        } else {
                            if (url(["tv8.com.tr"], 0x1) && !url(['video-cdn'], 0x1) && !url([".m3u8"], 0x1)) {
                                tv8();
                            } else {
                                if (url(["tlctv", "dmax"], 0x1) && !url([".m3u8"], 0x1)) {
                                    tlc();
                                } else {
                                    if (url(["teve2"], 0x1) && !url(["duhnet"], 0x1) && !url([".m3u8"], 0x1)) {
                                        teve2();
                                    } else {
                                        if (url(["tv360"], 0x1) && !url([".m3u8"], 0x1)) {
                                            tv360();
                                        } else {
                                            if (url(["tvem"], 0x1) && !url(['m3u8'], 0x1) && !url([".m3u8"], 0x1)) {
                                                tvem();
                                            } else {
                                                if (url(["womantv"], 0x1) && !url([".m3u8"], 0x1)) {
                                                    womantv();
                                                } else {
                                                    if (url(["kanal7"], 0x1) && !url(['.m3u8'], 0x1)) {
                                                        kanal7();
                                                    } else {
                                                        if (url(['ucankus'], 0x1) && !url([".m3u8"], 0x1)) {
                                                            ucankus();
                                                        } else {
                                                            if (url(["tele1"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                tele1();
                                                            } else {
                                                                if (url(["kanalb"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                    kanalb();
                                                                } else {
                                                                    if (url(['haberturk'], 0x1) && !url([".m3u8"], 0x1)) {
                                                                        haberturk();
                                                                    } else {
                                                                        if (url(["cnnturk"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                            cnnturk();
                                                                        } else {
                                                                            if (url(["ahaber.com", 'anews.com', 'sabah.com.tr', "aspor.com"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                ahaber();
                                                                            } else {
                                                                                if (url(["bloomberg"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                    bloomberg();
                                                                                } else {
                                                                                    if (url(['yirmidort.tv'], 0x1) && !url(['.m3u8'], 0x1)) {
                                                                                        yirmidort();
                                                                                    } else {
                                                                                        if (url(['beyaztv.com.tr'], 0x1) && !url(['.m3u8'], 0x1)) {
                                                                                            beyaztv();
                                                                                        } else {
                                                                                            if (url(['tvnet.com.tr'], 0x1) && !url(['.m3u8'], 0x1)) {
                                                                                                tvnet();
                                                                                            } else {
                                                                                                if (url(["dha.com.tr"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                                    dha();
                                                                                                } else {
                                                                                                    if (url(["yabantv.com", "koytv.tv"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                                        yabantv();
                                                                                                    } else {
                                                                                                        if (url(["tjk.org"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                                            tjk();
                                                                                                        } else {
                                                                                                            if (url(["dreamturk.com"], 0x1) && !url(['.m3u8'], 0x1)) {
                                                                                                                dreamturk();
                                                                                                            } else {
                                                                                                                if (url(["canlitv.digital"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                                                    canlitvcenter();
                                                                                                                } else {
                                                                                                                    if (url(["istanbuluseyret"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                                                        istanbuluseyret();
                                                                                                                    } else {
                                                                                                                        if (url(["radyodelisi"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                                                            radyodelisi();
                                                                                                                        } else {
                                                                                                                            if (url(["pokitv"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                                                                pokitv();
                                                                                                                            } else {
                                                                                                                                if (url(['filmon'], 0x1) && !url(['m3u8'], 0x1) && !url(['.m3u8'], 0x1)) {
                                                                                                                                    filmon();
                                                                                                                                } else {
                                                                                                                                    if (url(["cnbce"], 0x1) && !url(["m3u8"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                                                                        cnbce();
                                                                                                                                    } else {
                                                                                                                                        if (url(["canlitvulusal"], 0x1) && !url(["m3u8"], 0x1)) {
                                                                                                                                            canlitvulusal();
                                                                                                                                        } else {
                                                                                                                                            if (url(['canlitv.ws'], 0x1) && !url(["m3u8"], 0x1)) {
                                                                                                                                                canlitvws();
                                                                                                                                            } else {
                                                                                                                                                if (url(['yoltv.com'], 0x1) && !url(["m3u8"], 0x1)) {
                                                                                                                                                    yoltv();
                                                                                                                                                } else {
                                                                                                                                                    if (url(["canlitvvolo"], 0x1) && !url(["m3u8"], 0x1)) {
                                                                                                                                                        canlitvvolo();
                                                                                                                                                    } else {
                                                                                                                                                        if (url(["149.255.152.218", "aspx"], 0x1)) {
                                                                                                                                                            myvideoaz();
                                                                                                                                                        } else {
                                                                                                                                                            if (url(["parsatv"], 0x1)) {
                                                                                                                                                                parsatv();
                                                                                                                                                            } else {
                                                                                                                                                                if (url(['halktv.com'], 0x1)) {
                                                                                                                                                                    halktv();
                                                                                                                                                                } else {
                                                                                                                                                                    if (url(["radyohome.com"], 0x1)) {
                                                                                                                                                                        radyohome();
                                                                                                                                                                    } else {
                                                                                                                                                                        if (url(["streamtheworld.com"], 0x1) && !url(["aac"], 0x1)) {
                                                                                                                                                                            streamtheworld();
                                                                                                                                                                        } else {
                                                                                                                                                                            if (url(["canliradyolar"], 0x1) && !url(["mp3"], 0x1)) {
                                                                                                                                                                                canliradyolar();
                                                                                                                                                                            } else {
                                                                                                                                                                                if (url(["onlineradiobox"], 0x1) && !url(['mp3'], 0x1)) {
                                                                                                                                                                                    onlineradiobox();
                                                                                                                                                                                } else {
                                                                                                                                                                                    if (url(["filmmakinesi"], 0x1)) {
                                                                                                                                                                                        filmmakinesi();
                                                                                                                                                                                    } else {
                                                                                                                                                                                        if (url(["asyafilmizlesene"], 0x1)) {
                                                                                                                                                                                            asyafilmizlesene();
                                                                                                                                                                                        } else {
                                                                                                                                                                                            if (url(["filmmodu"], 0x1)) {
                                                                                                                                                                                                filmmodu();
                                                                                                                                                                                            } else {
                                                                                                                                                                                                if (url(["setfilmizle", "hdfilmcehennemiboncuk45"], 0x1)) {
                                                                                                                                                                                                    setfilmizle();
                                                                                                                                                                                                } else {
                                                                                                                                                                                                    if (url(["filmekseni"], 0x1)) {
                                                                                                                                                                                                        filmekseni();
                                                                                                                                                                                                    } else {
                                                                                                                                                                                                        if (url(["sinefil", "selcukflix"], 0x1)) {
                                                                                                                                                                                                            sinefil();
                                                                                                                                                                                                        } else {
                                                                                                                                                                                                            if (url(["kultfilmler"], 0x1)) {
                                                                                                                                                                                                                kultfilmler();
                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                if (url(['filmkovasi'], 0x1)) {
                                                                                                                                                                                                                    filmkovasi();
                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                    if (url(['filmatek'], 0x1)) {
                                                                                                                                                                                                                        filmatek();
                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                        if (url(['movie4k'], 0x1)) {
                                                                                                                                                                                                                            movie4k();
                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                            if (url(["/s.to", "aniworld.to"], 0x1)) {
                                                                                                                                                                                                                                sto();
                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                if (url(["siyahfilmizle"], 0x1)) {
                                                                                                                                                                                                                                    siyahfilmizle();
                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                    if (url(["sinemafilmizle"], 0x1)) {
                                                                                                                                                                                                                                        sinemafilmizle();
                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                        if (url(["123movies"], 0x1)) {
                                                                                                                                                                                                                                            movies123();
                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                            if (url(["wikiflix"], 0x1)) {
                                                                                                                                                                                                                                                wikiflix();
                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                if (url(['hdtoday'], 0x1)) {
                                                                                                                                                                                                                                                    hdtoday();
                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                    if (url(["wfilmizle"], 0x1)) {
                                                                                                                                                                                                                                                        wfilmizle();
                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                        if (url(["sinefy"], 0x1)) {
                                                                                                                                                                                                                                                            sinefy();
                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                            if (url(["fullhdfilmizlesene"], 0x1)) {
                                                                                                                                                                                                                                                                fullhdfilmizlesene();
                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                if (url(['4kfilmizle'], 0x1) && !url(["filmizlemek"], 0x1)) {
                                                                                                                                                                                                                                                                    filmizle4k();
                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                    if (url(['filmizlesene', "mavifilm3"], 0x1)) {
                                                                                                                                                                                                                                                                        url(url().replace('#mavifilm3', ''));
                                                                                                                                                                                                                                                                        consolelog(url());
                                                                                                                                                                                                                                                                        filmizlesene();
                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                        if (url(['jetfilm'], 0x1)) {
                                                                                                                                                                                                                                                                            jetfilm();
                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                            if (url(["mavifilm", "sinemaizle"], 0x1)) {
                                                                                                                                                                                                                                                                                hdfilmce();
                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                if (url(['hdfilmizle'], 0x1)) {
                                                                                                                                                                                                                                                                                    hdfilmcehennemi3();
                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                    if (url(["hdfilmcehennemi"], 0x1)) {
                                                                                                                                                                                                                                                                                        if (url(['syrtrk'], 0x1)) {
                                                                                                                                                                                                                                                                                            hdfilmcehennemi2();
                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                            if (url(["boncuk"], 0x1)) {
                                                                                                                                                                                                                                                                                                hdfilmcehennemi3();
                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                hdfilmcehennemi();
                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                        if (url(["realfilmizle"], 0x1)) {
                                                                                                                                                                                                                                                                                            realfilmizle();
                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                            if (url(['filmmax'], 0x1)) {
                                                                                                                                                                                                                                                                                                filmmax();
                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                if (url(['unutulmazfilmler'], 0x1)) {
                                                                                                                                                                                                                                                                                                    unutulmaz();
                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                    if (url(["sinemadelisi"], 0x1)) {
                                                                                                                                                                                                                                                                                                        sinemadelisi();
                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                        if (url(['sinema.vip'], 0x1) && !url(["/hls"], 0x1)) {
                                                                                                                                                                                                                                                                                                            sinemacx();
                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                            if (url(["superfilmgeldi", "hdsinemax"], 0x1)) {
                                                                                                                                                                                                                                                                                                                superfilmgeldi();
                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                if (url(['vumoox'], 0x1)) {
                                                                                                                                                                                                                                                                                                                    vumoox();
                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                    if (url(['yesmovies'], 0x1)) {
                                                                                                                                                                                                                                                                                                                        yesmovies();
                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                        if (url(['watchomovies'], 0x1)) {
                                                                                                                                                                                                                                                                                                                            watchomovies();
                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                            if (url(['123chill'], 0x1)) {
                                                                                                                                                                                                                                                                                                                                chill123();
                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                if (url(["webteizle"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                    webteizle();
                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                    if (url(["ugurfilm"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                        ugurfilm();
                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                        if (url(["xcine"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                            xcine();
                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                            if (url(['izledayim'], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                filmcidayi();
                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                if (url(['filmizlemek'], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                    filmizlemek();
                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                    if (url(['fullhdfilm'], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                        fullhdfilm();
                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                        if (url(["tafdi"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                            tafdi();
                                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                                            if (url(["filmfav", "sarifilm"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                url(url().replace("#sarifilm", ''));
                                                                                                                                                                                                                                                                                                                                                                filmfav();
                                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                                if (url(["dizilla"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                    yabanci_dizi();
                                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                                    if (url(["dizimom"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                        dizimom();
                                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                                        if (url(['dizimia'], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                            dizimia();
                                                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                                                            if (url(["diziyou"], 0x1) && !url(['.m3u8'], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                diziyou();
                                                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                                                if (url(['dizilab'], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                    dizilab();
                                                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                                                    if (url(["dizitime"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                        dizitime();
                                                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                                                        if (url(["dizibox"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                            dizibox();
                                                                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                                                                            if (url(["yabancidizi"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                yabancidizi();
                                                                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                                                                if (url(["dizipub", "dizist"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                    dizipub();
                                                                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                                                                    if (url(["dizipal"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                        dizipal();
                                                                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                                                                        if (url(["dizirix"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                            dizirix();
                                                                                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                                                                                            if (url(["onlinedizi"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                onlinedizi();
                                                                                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                                                                                if (url(['yabanci-dizi'], 0x1) || url(["roketdizi"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                    yabanci_dizi();
                                                                                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                                                                                    if (url(["diziyo"], 0x1) && !url(["diziyou"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                        diziyo();
                                                                                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                                                                                        if (url(["diziroll"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                            diziroll();
                                                                                                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                                                                                                            if (url(["sezonlukdizi"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                sezonlukdizi();
                                                                                                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                if (url(["diziwatch"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                    diziwatch();
                                                                                                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                    if (url(['diziplus'], 0x1) || url(['dizimag'], 0x1) || url(["diziberlin"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                        diziplus();
                                                                                                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                        if (url(["dizifin"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                            dizifin();
                                                                                                                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                            if (url(["dizikral"], 0x1) || url(["filmhe"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                dizikral();
                                                                                                                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                if (url(["dizifix"], 0x1) || url(["dizilib"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                    dizifix();
                                                                                                                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                    if (url(["koreanturk"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                        koreanturk();
                                                                                                                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                        if (url(["dizigom"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                            dizigom();
                                                                                                                                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                            if (url(["ddizi"], 0x1) && !url(['.mp4'], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                ddizi();
                                                                                                                                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                if (url(["dizimat"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    dizimat();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    if (url(["canlidizi"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                        canlidizi();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                        if (url(["dizipod"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                            dizipod();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                            if (url(["dizibul"], 0x1) || url(['hdnetflix'], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                dizibul();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                if (url(["streamruby"], 0x1) && !url(["m3u8"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    streamruby();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    if (url(['filemoon', "upstream"], 0x1) && !url(["m3u8"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        filemoon();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        if (url(["sibnet"], 0x1) && !url(["m3u8"], 0x1) && !url([".mp4"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            sibnet();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            if (url(["govids"], 0x1) && !url(['redirect'], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                govids();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                if (url(["youtube"], 0x1) && !url(["googlevideo.com/"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    youtube();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    if (url(["vidmoly"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        vidmoly();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        if (url(["contentx", 'playru', "filese", "hotlinger", "//four", "pichive"], 0x1) && !url(["m.php"], 0x0)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            contentx();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            if (url(['ok.ru', "odnok"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                okru();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                if (url(["vidmoxy", "vidrame"], 0x1) && !url(['ok.vidmoxy'], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    vidmoxy();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    if (url(["supervideo", "dropload"], 0x1) && !url(['.m3u8'], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        supervideo();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        if (url(["mixdrop"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            mixdrop();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            if (url(["streamtape"], 0x1) && !url(["get_video"], 0x1) && !url([".mp4"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                streamtape();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                if (url(["voe"], 0x1) && !url(["m3u8"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    voe();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    if (url(["vectorx", "ply.jetv.xyz"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        vectorx();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        if (url(["videoseyred.in"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            videoseyred();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            if (url(["mail.ru"], 0x1) && !url([".mp4"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                mailru();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                if (url(["vimeo"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    vimeo();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    if (url(['streamoupload'], 0x1) && !url(["m3u8"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        streamoupload();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        if (url(["vk.com"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            vkcom();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            if (url(["dood."], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                dood();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                if (url(["vidload."], 0x1) && !url(["m3u8"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    vidload();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    if (url(["puhutv.com"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        puhutv();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        if (url(["dailymotion"], 0x1) && !url(["m3u8"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            dailymotion();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            if (url(['imdb'], 0x1) && !url(['video.media'], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                imdb();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                if (url(['trstx', 'sobreatsesuyp', "chaintwistasherictive"], 0x1) && !url([".txt"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    trstx();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    if (url(["vudeo"], 0x1) && !url([".mp4"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        vudeo();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        if (url(["oneupload"], 0x1) && !url([".mp4"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            oneupload();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            if (url(["vidlop"], 0x1) && !url([".mp4"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                vidlop();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                if (url(['streamplayer'], 0x1) && !url([".mp4"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    streamplayer();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    if (url(["chaturbate"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        chaturbate();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        if (url(["ashemaletube"], 0x1) && !url(['.mp4'], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ashemaletube();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            if (url(['pornhub'], 0x1) && !url([".mp4"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                pornhub();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                if (url(["xvideos"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    xvideos();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    if (url(["thehun"], 0x1) && !url([".m3u8"], 0x1) && !url([".mp4"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        thehun();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        if (url(["youporn"], 0x1) && !url(["/hls/"], 0x1) && !url(["/mp4/"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            youporn();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            if (url(["xnxx"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                xnxx();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                if (url(["xhamster"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    xhamster();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    if (url(["7dak"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        dak7();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        if (url(["hdabla"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            hdabla();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            if (url(['allclassic'], 0x1) && !url([".mp4"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                allclassic();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                if (url(["pornpics"], 0x1) && !url(['.mp4'], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    pornpics();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    if (url(['.aac', "radyotvonline"], 0x1) && !url(["streamtheworld"], 0x1) && !url([".m3u8"], 0x1)) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        g.setMediaType("mp3");
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    try {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        var _0x443f96 = Core.getUrlContentType() + '';
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        consolelog("Content Type: " + _0x443f96);
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        consolelog("Media Type: " + g.getMediaType() + '');
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        if (_0x443f96 == "video/mp2t" || _0x443f96 == "video/x-matroska") {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            g.setMediaType('mp4');
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    } catch (_0x3686a0) {}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    if (isPreview()) {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        g.setReady(true);
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        url(fixUrl(url()));
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        Core.playVideoJS();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                }
                                                                                                                                                                                                                            }
                                                                                                                                                                                                                        }
                                                                                                                                                                                                                    }
                                                                                                                                                                                                                }
                                                                                                                                                                                                            }
                                                                                                                                                                                                        }
                                                                                                                                                                                                    }
                                                                                                                                                                                                }
                                                                                                                                                                                            }
                                                                                                                                                                                        }
                                                                                                                                                                                    }
                                                                                                                                                                                }
                                                                                                                                                                            }
                                                                                                                                                                        }
                                                                                                                                                                    }
                                                                                                                                                                }
                                                                                                                                                            }
                                                                                                                                                        }
                                                                                                                                                    }
                                                                                                                                                }
                                                                                                                                            }
                                                                                                                                        }
                                                                                                                                    }
                                                                                                                                }
                                                                                                                            }
                                                                                                                        }
                                                                                                                    }
                                                                                                                }
                                                                                                            }
                                                                                                        }
                                                                                                    }
                                                                                                }
                                                                                            }
                                                                                        }
                                                                                    }
                                                                                }
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    } catch (_0x1ce057) {
        var _0x52c877 = _0x1ce057.message;
        consolelog("Error: ", _0x52c877);
        errorEncode = encodeURIComponent(_0x52c877);
        try {
            var _0x3f477f = encodeURIComponent("NEW PARSER: " + Core.mainUrlForReferer + ", " + g.getLang());
            fetch("http://rootcheck.tk/sey/back/v2/parser/notifier.php?error=" + errorEncode + "&details=" + _0x3f477f);
        } catch (_0x4fe868) {
            var _0x3f477f = encodeURIComponent("NEW PARSER: " + url() + ", " + g.getLang());
            fetch("http://rootcheck.tk/sey/back/v2/parser/notifier.php?error=" + errorEncode + "&details=" + _0x3f477f);
        }
        if (!isPreview()) {
            if (_0x52c877.includes("Webview")) {
                Core.showOnError("SeÃ§tiÄŸiniz kaynak/alt kaynak cihazÄ±nÄ±z tarafÄ±ndan desteklenmemektedir.");
            } else {
                if (_0x52c877.includes("kapalÄ± olduÄŸundan")) {
                    Core.showOnError(_0x52c877 + '');
                } else {
                    Core.showOnError();
                }
            }
        } else {
            url("empty");
            g.setReady(true);
        }
        return _0x52c877;
    }
}

function ahaber() {
    if (url(["apara"], 0x0)) {
        url("https://securevideotoken.tmgrup.com.tr/webtv/secure?851521&url=http%3A%2F%2Ftrkvz-live.ercdn.net%2Faparahd%2Faparahd.m3u8");
    } else {
        if (url(["ahaber"], 0x0)) {
            url("https://securevideotoken.tmgrup.com.tr/webtv/secure?851521&url=https%3A%2F%2Ftrkvz-live.ercdn.net%2Fahaberhd%2Fahaberhd.m3u8");
        } else {
            if (url(['anews'], 0x0)) {
                url("https://securevideotoken.tmgrup.com.tr/webtv/secure?851521&url=http%3A%2F%2Ftrkvz-live.ercdn.net%2Fanewshd%2Fanewshd.m3u8");
            } else if (url(['aspor'], 0x0)) {
                url("https://securevideotoken.tmgrup.com.tr/webtv/secure?851521&url=http%3A%2F%2Ftrkvz-live.ercdn.net%2Fasporhd%2Fasporhd.m3u8");
            }
        }
    }
    url(fetch().match(/"Url":"(.*?)"/)[0x1]);
    parser();
}

function allclassic() {
    var _0x284ff8 = fetch().match(/function\/0\/(.*?)',/)[0x1];
    var _0xcca4ec = _0x284ff8.split('/')[0x5].substring(0x0, 0x20);
    var _0x455cbf = "76582147925414364366255444386504";
    h = _0xcca4ec.split('');
    _0x455cbf = _0x455cbf.split('');
    for (let _0x370b8d = h.length - 0x1; _0x370b8d >= 0x0; _0x370b8d--) {
        let _0x36b1ac = _0x370b8d;
        for (let _0x18d5ab = _0x370b8d; _0x18d5ab < _0x455cbf.length; _0x18d5ab++) {
            _0x36b1ac += parseInt(_0x455cbf[_0x18d5ab]);
        }
        while (_0x36b1ac >= h.length) {
            _0x36b1ac -= h.length;
        }
        let _0x16945f = '';
        for (let _0x48aaa4 = 0x0; _0x48aaa4 < h.length; _0x48aaa4++) {
            if (_0x48aaa4 === _0x370b8d) {
                _0x16945f += h[_0x36b1ac];
            } else {
                if (_0x48aaa4 === _0x36b1ac) {
                    _0x16945f += h[_0x370b8d];
                } else {
                    _0x16945f += h[_0x48aaa4];
                }
            }
        }
        h = _0x16945f.split('');
    }
    h = h.join('');
    url(_0x284ff8.replace(_0xcca4ec, h));
    parser();
}

function ashemaletube() {
    var _0x361f2d = matchAll(fetch(), /"src":"(.*?)","desc":"(.*?)",/g);
    var _0x2a4463 = {};
    for (let _0x41020f = 0x0; _0x41020f < _0x361f2d.length; _0x41020f++) {
        _0x2a4463[_0x361f2d[_0x41020f][0x2]] = _0x361f2d[_0x41020f][0x1];
    }
    var _0x2ab6c3 = ["360p", '480p', "720p", '1080p', "Alone"];
    var _0x56bc81 = -0x1;
    var _0x5e2c1b = -0x1;
    for (let _0x13f437 = 0x0; _0x13f437 < Object.keys(_0x2a4463).length; _0x13f437++) {
        try {
            var _0x184a8f = Object.keys(_0x2a4463)[_0x13f437];
            var _0x76ab9c = _0x2ab6c3.indexOf(_0x184a8f);
            if (_0x56bc81 < _0x76ab9c) {
                _0x56bc81 = _0x76ab9c;
                _0x5e2c1b = _0x184a8f;
            }
        } catch (_0x1569ce) {}
    }
    if (_0x56bc81 != -0x1) {
        url(fixUrl(_0x2a4463[_0x5e2c1b].replace(/\\/g, '')));
    }
    parser();
}

function asyafilmizlesene() {
    initialUrl = url() + '';
    var _0x518886 = fetch();
    _0x518886 = _0x518886.match(/href="([^"]+)"\s*class="amy-redirect-watch-online".*?Film\s*izle/)[0x1];
    _0x518886 = fetch(_0x518886);
    streamUrls = {};
    try {
        var _0x428760 = matchAll(_0x518886, /data-source="(.*?)">/g);
        consolelog(_0x428760);
        for (let _0x327ec1 = 0x0; _0x327ec1 < _0x428760.length; _0x327ec1++) {
            try {
                var _0x140334 = _0x428760[_0x327ec1][0x1];
                var _0x35937d = _0x140334.split('//')[0x1].split('.')[0x0];
                if (_0x35937d != "listeamed" && _0x35937d != "csst") {
                    streamUrls[_0x35937d] = _0x140334;
                }
            } catch (_0x2ff51e) {}
        }
    } catch (_0x3adb3f) {
        error(_0x3adb3f.message);
    }
    if (!(initialUrl + '').includes('#') && JSON.stringify(streamUrls) != '{}') {
        Core.showAlternatesJS(JSON.stringify(streamUrls));
    } else {
        url((initialUrl + '').split('#')[0x1]);
        parser();
    }
}

function atv() {
    if (url(["canli-yayin"], 0x0)) {
        var _0x3294df = "atv";
        if (url(["minikacocuk"], 0x0)) {
            _0x3294df = "minikago_cocuk";
        } else {
            if (url(["minikago"], 0x0)) {
                _0x3294df = "minikago";
            } else {
                if (url(["a2tv"], 0x0)) {
                    _0x3294df = "a2tv";
                    url("https://www.atv.com.tr/a2tv/canli-yayin");
                }
            }
        }
        headers('Referer', "https://www.atv.com.tr/");
        var _0x4f8a6e = fetch();
        url(_0x4f8a6e.match(/"(https:\/\/i.tmgrup.com.tr\/videojs\/js.*?)"/)[0x1]);
        var _0x5023d4 = "'(https://trkvz.daioncdn.net/" + _0x3294df + '/' + _0x3294df + ".m3u8.*?&app=)(.*?)'";
        consolelog(_0x5023d4);
        var _0x30b9d3 = new RegExp(_0x5023d4);
        var _0x12780b = '';
        var _0x2e05af = '';
        try {
            _0x4f8a6e = fetch().match(_0x30b9d3);
            if (_0x3294df == "a2tv") {
                _0x4f8a6e = '';
            }
            _0x12780b = _0x4f8a6e[0x2];
            _0x2e05af = _0x4f8a6e[0x1];
        } catch (_0x2aaef3) {
            _0x4f8a6e = '';
        }
        if (_0x4f8a6e == '') {
            _0x5023d4 = "\"(https://trkvz.daioncdn.net/" + _0x3294df + '/' + _0x3294df + ".m3u8.*?)" + "\";";
            _0x30b9d3 = new RegExp(_0x5023d4);
            _0x4f8a6e = fetch().match(_0x30b9d3);
            _0x2e05af = _0x4f8a6e[0x1];
            _0x12780b = '';
        }
        url('https://securevideotoken.tmgrup.com.tr/webtv/secure?url=' + encodeURIComponent(_0x2e05af + _0x12780b));
        _0x4f8a6e = fetch();
        url(_0x4f8a6e.match(/.*?Url":"(htt.*?)"/)[0x1]);
    } else {
        try {
            var _0x4f8a6e = fetch();
            var _0xf22cec = (_0x4f8a6e + '').match(/videoid="(.*?)" data-vp="tmdvpcontainer" data-websiteid="(.*?)"/);
            _0xf22cec = 'https://videojs.tmgrup.com.tr/getvideo/' + _0xf22cec[0x2] + '/' + _0xf22cec[0x1];
            _0x4f8a6e = fetch(_0xf22cec);
            var _0x292a6f = _0x4f8a6e.match("\"VideoUrl\":\"([^\"]+)\".*?\"VideoSmilUrl\":\"([^\"]+)\"");
            var _0x12780b = encodeURIComponent(_0x292a6f[0x1]);
            var _0x2e05af = encodeURIComponent(_0x292a6f[0x2]);
            url("https://securevideotoken.tmgrup.com.tr/webtv/secure?url=" + _0x12780b + "&url2=" + _0x2e05af);
            _0xf22cec = fetch();
            json = JSON.parse(_0xf22cec);
            if (json.hasOwnProperty("Url")) {
                url(json.Url);
            } else {
                if (json.hasOwnProperty("Alone")) {
                    url(json.Alone);
                } else {
                    if (json.hasOwnProperty("1080p")) {
                        url(json["1080p"]);
                    } else {
                        if (json.hasOwnProperty('720p')) {
                            url(json["720p"]);
                        } else if (json.hasOwnProperty("480p")) {
                            url(json["480p"]);
                        }
                    }
                }
            }
        } catch (_0x4bb063) {
            error(_0x4bb063.message);
        }
    }
    parser();
}

function beyaztv() {
    url(fetch().match(/videoUrl\s*=\s*"(.*?)"/)[0x1]);
    parser();
}

function bloomberg() {
    url(fetch().match(/ var\s*videoUrl\s*=\s*"(.*?&app.*?)"/)[0x1]);
    parser();
}

function canlidizi() {
    var _0x50cf14 = fetch();
    _0x50cf14 = _0x50cf14.match(/data-wpfc-original-src="(.*?(?:fireplayer|betaplayer).*?)"/)[0x1];
    if (_0x50cf14.includes("fireplayer")) {
        var _0x11955 = _0x50cf14.split('/');
        _0x11955 = _0x11955[_0x11955.length - 0x1];
        var _0x7c37a5 = _0x50cf14 + "?do=getVideo";
        var _0x4ef061 = "hash=" + _0x11955 + "&r=" + baseUrl(url()) + "&s=";
        headers('Content-type', "application/x-www-form-urlencoded; charset=UTF-8");
        headers("x-requested-with", "XMLHttpRequest");
        _0x50cf14 = fetchPost(_0x4ef061, _0x7c37a5);
        _0x50cf14 = JSON.parse(_0x50cf14);
        url(_0x50cf14.videoSources[0x0].file);
    } else {
        if (_0x50cf14.includes("betaplayer")) {
            var _0x560268 = _0x50cf14;
            _0x50cf14 = fetch(_0x50cf14);
            var _0x7c37a5 = _0x50cf14.match(/file\s*:\s*"(.*?betaplayer.*?)"/)[0x1];
            headers("Referer", _0x560268);
            headers("Accept", "*/*");
            url(_0x7c37a5);
            try {
                var _0x435b21 = _0x50cf14.match(/tracks\s*:\s*(\[.*?\]),/)[0x1];
                _0x435b21 = _0x435b21.split('}');
                for (let _0x1b31de = 0x0; _0x1b31de < _0x435b21.length; _0x1b31de++) {
                    if (_0x435b21[_0x1b31de].includes("tur") && _0x435b21[_0x1b31de].includes(".vtt") && !_0x435b21[_0x1b31de].includes('forced')) {
                        sub(baseUrl(url()) + '' + _0x435b21[_0x1b31de].match(/file":\s*"(.*?)"/)[0x1]);
                    }
                }
            } catch (_0x2832a2) {}
        }
    }
    parser();
}

function canliradyolar() {
    var _0x2cd061 = fetch();
    var _0x5bae7d = _0x2cd061.match(/iframe\s*src="(.*?)"\s*name=/)[0x1];
    _0x2cd061 = fetch(_0x5bae7d);
    _0x5bae7d = _0x2cd061.match(/source\s*src="(.*?)"/)[0x1];
    url(_0x5bae7d);
    g.setMediaType("mp3");
    parser();
}

function canlitvcenter() {
    var _0x24050e = fetch();
    _0x24050e = _0x24050e.match(/iframe-player.*?src=[\"'](.*?)[\"']/)[0x1];
    if (_0x24050e.includes("urlcik=")) {
        try {
            _0x24050e = _0x24050e.match(/urlcik=(.*?)&/)[0x1];
            _0x24050e = atob(_0x24050e);
        } catch (_0x22fe13) {}
    }
    _0x24050e = fetch(_0x24050e);
    if (_0x24050e.includes("DM.player")) {
        url("https://dailymotion.com/video/" + _0x24050e.match(/video\\s*:\\s*'(.*?)'/)[0x1]);
    } else {
        if (_0x24050e.includes('youtube.com/embed')) {
            url(_0x24050e.match(/iframe.*?src=[\"'](.*?)(?:\?|[\"'])/)[0x1]);
        } else {
            if (_0x24050e.includes("atob")) {
                url(atob(_0x24050e.match(/atob\("(.*?)"/)[0x1]));
            } else {
                if (_0x24050e.includes("eval(function") || _0x24050e.includes("<script src=\"")) {
                    try {
                        url(_0x24050e.match(/script\s*src=\\"(.*?)\\">/)[0x1]);
                    } catch (_0x36cb40) {
                        url('');
                    }
                    if (url() == '') {
                        url(_0x24050e.match(/<script\s*src=\s*"(https:\/\/play.cdn-canlitv.*?)"/)[0x1]);
                    }
                    _0x24050e = fetch();
                    var _0x5e7e87 = _0x24050e.match(/verianahtar\s*=\s*"(.*?)"/)[0x1];
                    var _0xadab8e = "https:" + _0x24050e.match(/yayincomtr4\s*=\s*"(.*?)"/)[0x1];
                    url(_0xadab8e + _0x5e7e87);
                }
            }
        }
    }
    parser();
}

function canlitvulusal() {
    url("https://canlitvulusal.com/", "https://canlitvulusal3.xyz/live/");
    url("tv-show/", '');
    url("-canli-yayin/", "/index.m3u8");
    url('-', '');
    try {
        fetch();
    } catch (_0x16514b) {
        url("https://canlitvulusal.com/", "https://canlitvulusal3.xyz/live/");
        url('tv-show/', '');
        url("-canli-yayin/", "/index.m3u8");
        url('-', '');
    }
    g.deleteHeader("Referer");
    parser();
}

function canlitvvolo() {
    headers("Referer", url());
    headers("User-Agent", "Cloudflare");
    var _0x45109d = fetch().match(/const data = (.*?);/)[0x1].replace(/\s*/g, '').replace('{', '').replace('}', '').split(',');
    var _0x4090d4 = {};
    for (var _0x3754f6 = 0x0; _0x3754f6 < _0x45109d.length; _0x3754f6++) {
        var _0x549243 = _0x45109d[_0x3754f6].split(':');
        _0x4090d4[_0x549243[0x0]] = _0x549243[0x1].replace(/'/g, '');
    }
    headers('Referer', url());
    headers("X-Requested-With", "XMLHttpRequest");
    headers("Content-Type", "application/json");
    url('https://tv.canlitvvolo.com/Tv/TVShow');
    _0x45109d = fetchPost(JSON.stringify(_0x4090d4));
    var _0x11dc1f = JSON.parse(_0x45109d);
    try {
        url(_0x11dc1f.result.playerBodyEnd.match(/file:'(.*?)'/)[0x1]);
    } catch (_0x17da66) {
        url(_0x11dc1f.result.playerBodyEnd.match(/contentURL"\s*:\s*(.*?)"/)[0x1]);
    }
    parser();
}

function canlitvws() {
    var _0x242d2e = fetch().match(/index.php\?id=(\d+)"/)[0x1];
    var _0x3ab45a = fetch("https://www.canlitv.ws/embed/?id=" + _0x242d2e).match(/file:\s*"(.*?)"/)[0x1];
    url(_0x3ab45a);
    parser();
}

function chaturbate() {
    var _0x355706 = fetch().match(/hls_source\\u0022:\s*\\u0022(.*?)\\u0022/)[0x1].replace(/\\u002D/g, '-');
    url(_0x355706);
    parser();
}

function chill123() {
    headers("Referer", "https://123chill.online/");
    data = fetch();
    try {
        var _0x47b007 = (data + '').match(/iframe\s*id="myFrame"\s*src="(.*?)"/)[0x1];
        data = fetch(_0x47b007);
        var _0x4e333f = (data + '').match(/<iframe.*?src="(.*?)"/)[0x1];
        _0x4e333f = fixUrl(_0x4e333f);
        var _0x5207f6 = baseUrl(_0x4e333f);
        data = fetch(_0x4e333f);
        _0x4e333f = _0x5207f6 + (data + '').match(/src:.*?'(.*?)'/)[0x1];
        var _0x4e0e09 = '';
        while (!_0x4e0e09.startsWith('eqq') && true) {
            data = fetch(_0x4e333f);
            var _0x4e0e09 = (data + '').match(/style="display:none;">\s*(.*?)<\/div>/)[0x1];
            consolelog(_0x4e0e09);
        }
        if (!_0x4e0e09.startsWith('eqq')) {}
        url(replaceCustomChars(_0x4e0e09));
    } catch (_0x419402) {
        error(_0x419402.message);
    }
    parser();
}

function cnbce() {
    try {
        var _0x281a75 = fetchPost('', 'https://www.cnbce.com/api/live-stream/source');
        var _0x1ed38b = JSON.parse(_0x281a75);
        url(_0x1ed38b.source);
    } catch (_0x1ddcb7) {
        error(_0x1ddcb7.message);
    }
    parser('', 0x2, '', false);
}

function cnnturk() {
    var _0x4e44df = JSON.parse(fetch("https://www.cnnturk.com/action/media/" + fetch().match(/data-id="(.*?)"/)[0x1] + "?ad_type=embed-player"));
    url(_0x4e44df.Media.Link.ServiceUrl + '' + _0x4e44df.Media.Link.SecurePath);
    parser();
}

function contentx() {
    if (!url(["filese"], 0x0)) {
        url(fixUrl(url()));
        headers("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7");
        headers("User-Agent", 'cf_clearance=');
        var _0x499e45 = fetch();
        try {
            var _0x2665c2 = matchAll(_0x499e45, /"file"\s*:\s*"(.*?)"\s*,\s*"label"\s*:\s*"(.*?)"/g);
            for (let _0x3e90e6 = 0x0; _0x3e90e6 < _0x2665c2.length; _0x3e90e6++) {
                consolelog(_0x2665c2[_0x3e90e6][0x1]);
                if ((_0x2665c2[_0x3e90e6][0x2].toLowerCase().includes('rk') || _0x2665c2[_0x3e90e6][0x2].toLowerCase().includes('turkish') || _0x2665c2[_0x3e90e6][0x2].toLowerCase().includes('turkish')) && !_0x2665c2[_0x3e90e6][0x1].includes('forced')) {
                    sub(_0x2665c2[_0x3e90e6][0x1].replace(/\\\//g, '/'));
                }
            }
        } catch (_0x307271) {}
        _0x499e45 = _0x499e45.match(/window.openPlayer\((.*?)\)/)[0x1].split(',')[0x0].replace(/'/g, '');
        _0x499e45 = fetch(baseUrl(url()) + "/source2.php?v=" + _0x499e45);
        var _0x3f74b4 = JSON.parse(_0x499e45).playlist;
        url('');
        for (var _0x58264d = 0x0; _0x58264d < _0x3f74b4.length; _0x58264d++) {
            if (g.getLang() == 0x1 && (_0x3f74b4[_0x58264d].sources[0x0].title.includes("TÃ¼rkÃ§e Dublaj") || _0x3f74b4[_0x58264d].sources[0x0].title.includes('Orijinal'))) {
                url(_0x3f74b4[_0x58264d].sources[0x0].file);
            } else {
                if (g.getLang() == 0x0 && (_0x3f74b4[_0x58264d].sources[0x0].title.includes("TÃ¼rkÃ§e AltyazÄ±") || _0x3f74b4[_0x58264d].sources[0x0].title.includes('Orijinal'))) {
                    url(_0x3f74b4[_0x58264d].sources[0x0].file);
                }
            }
        }
        if (url() == '') {
            for (var _0x58264d = 0x0; _0x58264d < _0x3f74b4.length; _0x58264d++) {
                url(_0x3f74b4[_0x58264d].sources[0x0].file);
            }
        }
        if (g.getLang() == 0x0 && Core.mainUrlForReferer.includes('dizilla')) {
            sub('');
        }
        headers("Referer", baseUrl(url()));
        parser();
    }
}

function dailymotion() {
    url("embed/", '');
    url("video", "player/metadata/video");
    var _0x38e437 = fetch();
    var _0x5b6c32 = JSON.parse(_0x38e437);
    url(_0x5b6c32.qualities.auto[0x0].url);
    g.deleteHeader('Referer');
    parser();
}

function dak7() {
    var _0x152433 = matchAll(fetch(), /source\s*src="(.*?)".*?size="(.*?)"/g);
    var _0x573985 = ["240", '360', "480", "720", "1080", "Alone"];
    var _0x32ebf7 = -0x1;
    var _0x2f5b7e = -0x1;
    for (let _0x7da6d0 = 0x0; _0x7da6d0 < _0x152433.length; _0x7da6d0++) {
        try {
            var _0x842eb0 = _0x152433[_0x7da6d0][0x2];
            var _0x56c181 = _0x573985.indexOf(_0x842eb0);
            consolelog(_0x56c181);
            if (_0x32ebf7 < _0x56c181) {
                _0x32ebf7 = _0x56c181;
                _0x2f5b7e = _0x7da6d0;
            }
        } catch (_0x1092fe) {}
    }
    if (_0x32ebf7 != -0x1) {
        url(fixUrl(_0x152433[_0x2f5b7e][0x1].replace(/\\/g, '')));
    }
    parser();
}

function ddizi() {
    headers("Accept", "*/*");
    var _0x11ffe0 = fetch();
    var _0x3813a8 = _0x11ffe0.match(/iframe.*?src="(.*?)"/)[0x1];
    if (!_0x3813a8.startsWith("https")) {
        _0x3813a8 = baseUrl(url()) + '/' + _0x3813a8;
        headers("Referer", _0x3813a8);
        g.deleteHeader('Origin');
        _0x11ffe0 = fetch(_0x3813a8);
        url(_0x11ffe0.match(/file:"(.*?)"/)[0x1].replace(/\\/g, ''));
    } else {
        url(_0x3813a8);
    }
    parser();
}

function dha() {
    url(fetch().match(/src:\s*'(.*?)'/)[0x1].replace(/\\\//g, '/'));
    parser();
}

function dizibox() {
    var _0x5aa97c = url();
    headers("User-Agent", "google");
    var _0x14ba16 = '';
    try {
        _0x14ba16 = fetch();
        _0x14ba16 = _0x14ba16.match(/woca-linkpages-dd selectBox(.*?)\/select/);
    } catch (_0x162491) {
        _0x14ba16 = '';
    }
    var _0x1d7f85 = {};
    try {
        var _0x3a12ee = matchAll(_0x14ba16, /(?:value=["']|href=["'])(.*?)["'].*?>(.*?)</g);
        for (let _0xeeff9e = 0x0; _0xeeff9e < _0x3a12ee.length; _0xeeff9e++) {
            var _0x126506 = _0x3a12ee[_0xeeff9e][0x1];
            var _0x53ba8d = _0x3a12ee[_0xeeff9e][0x2];
            if (_0x53ba8d != '' && _0x53ba8d != "King" && _0x53ba8d != "Play") {
                _0x1d7f85[_0x53ba8d] = _0x126506;
            }
        }
    } catch (_0x2d096a) {
        error(_0x2d096a.message);
    }
    consolelog(JSON.stringify(_0x1d7f85));
    if (!_0x5aa97c.includes('#') && JSON.stringify(_0x1d7f85) != '{}') {
        Core.showAlternatesJS(JSON.stringify(_0x1d7f85));
    } else {
        url(_0x5aa97c.split('#')[0x1]);
        var _0x5dd240 = _0x5aa97c.split('#')[0x2];
        if (_0x5dd240.toLowerCase().includes('pro')) {
            if (!isWebView) {
                error("NO Webview");
            } else {
                getWebViewOwnContentJS(_0x5aa97c, "molystream", "I AM NOT LOOKING", "playSheilaBtn", '', 0x0, false, headers, 0x1);
            }
        } else {
            _0x14ba16 = fetch();
            url(_0x14ba16.match(/frame.*?src="(.*?)".*?webkitallowfullscreen/)[0x1]);
            _0x14ba16 = fetch();
            if (url(["haydi.php"], 0x1)) {
                try {
                    var _0x3a12ee = matchAll(_0x14ba16, /<iframe(.*?)<\/iframe/g);
                    for (let _0x46d88c = 0x0; _0x46d88c < _0x3a12ee.length; _0x46d88c++) {
                        if (!_0x3a12ee[_0x46d88c][0x1].includes("display:")) {
                            url(_0x3a12ee[_0x46d88c][0x1]);
                            break;
                        }
                    }
                    url(url().match(/src=['"](.*?)['"]/)[0x1]);
                } catch (_0x3547fd) {
                    error(_0x3547fd.message);
                }
            } else {
                if (url(["moly.php"], 0x1)) {
                    try {
                        var _0x3a12ee = matchAll(_0x14ba16, /unescape\("(.*?)"\)/g);
                        for (let _0x2e2002 = 0x0; _0x2e2002 < _0x3a12ee.length; _0x2e2002++) {
                            if (!_0x3a12ee[_0x2e2002][0x1].includes('display:')) {
                                url(_0x3a12ee[_0x2e2002][0x1]);
                                break;
                            }
                        }
                        url(decodeURIComponent(url()));
                        url(atob(url()));
                        try {
                            var _0x3a12ee = matchAll(url(), /<iframe(.*?)<\/iframe/g);
                            for (let _0x321aef = 0x0; _0x321aef < _0x3a12ee.length; _0x321aef++) {
                                if (!_0x3a12ee[_0x321aef][0x1].includes('display:')) {
                                    url(_0x3a12ee[_0x321aef][0x1]);
                                    break;
                                }
                            }
                        } catch (_0x228b5d) {
                            error(_0x228b5d.message);
                        }
                        url(url().match(/src=['"](.*?)['"]/)[0x1]);
                    } catch (_0x5629b7) {
                        error(_0x5629b7.message);
                    }
                }
            }
            parser();
        }
    }
}

function dizibul() {
    var _0x26e701 = fetch();
    var _0x286481 = _0x26e701.match(/data-frame="(.*?)"/)[0x1];
    _0x26e701 = fetch(_0x286481);
    _0x26e701 = _0x26e701.match(/bePlayer\('\s*(.*?)'\s*,\s*'(.*?)'\)/);
    var _0x3d442c = _0x26e701[0x1];
    var _0x18e09c = _0x26e701[0x2];
    _0x26e701 = hdmomplayer(_0x3d442c, _0x18e09c);
    consolelog(_0x26e701);
    url(_0x26e701[0x0]);
    headers("Referer", _0x286481);
    headers("Accept", '*/*');
    parser();
}

function dizifin() {
    var _0x653f3 = fetch();
    headers("Referer", url());
    _0x653f3 = _0x653f3.match(/iframe\s*src="(.*?)"/)[0x1];
    var _0x57bd19 = baseUrl(_0x653f3);
    headers("Referer", 'https://dizifin.com/');
    _0x653f3 = fetch(_0x653f3);
    try {
        var _0x206b18 = matchAll(_0x653f3, /"file":"(.*?vtt)"/g);
        for (let _0x2ed504 = 0x0; _0x2ed504 < _0x206b18.length; _0x2ed504++) {
            if (_0x206b18[_0x2ed504][0x1].includes("tur") || _0x206b18[_0x2ed504][0x1].includes('tr')) {}
            sub(_0x206b18[_0x2ed504][0x1].replace(/\\/g, '').replace('..', _0x57bd19));
        }
    } catch (_0x17c0b9) {
        error(_0x17c0b9.message);
    }
    _0x653f3 = _0x653f3.match(/"file":\s*"(.*?)"/)[0x1].replace(/\\x/g, " ");
    var _0x151583 = _0x653f3.split(" ");
    _0x653f3 = '';
    for (var _0xe0267 = 0x0; _0xe0267 < _0x151583.length; _0xe0267++) {
        var _0x26e2c2 = parseInt(_0x151583[_0xe0267], 0x10);
        var _0x536035 = String.fromCharCode(_0x26e2c2);
        _0x653f3 += _0x536035;
    }
    _0x653f3 = _0x653f3.replace('..', _0x57bd19).replace(" ", '').substring(0x1);
    url(_0x653f3);
    parser();
}

function dizifix() {
    var _0x48a3b6 = url();
    var _0x577d01 = fetch();
    var _0x22295f = {};
    try {
        var _0x59b621 = matchAll(_0x577d01, /<a\s*data-frame="(.*?)"/g);
        for (let _0x44c503 = 0x0; _0x44c503 < _0x59b621.length; _0x44c503++) {
            var _0x5886b1 = _0x59b621[_0x44c503][0x1];
            var _0x5d3124 = "Kaynak-" + (_0x44c503 + 0x1);
            _0x22295f[_0x5d3124] = _0x5886b1;
        }
    } catch (_0x56f7d8) {
        error(_0x56f7d8.message);
    }
    if (!_0x48a3b6.includes('#') && JSON.stringify(_0x22295f) != '{}' && _0x22295f.length > 0x1) {
        Core.showAlternatesJS(JSON.stringify(_0x22295f));
    } else {
        if (url(['#'], 0x1)) {
            url(_0x48a3b6.split('#')[0x1]);
        } else {
            url(_0x22295f["Kaynak-1"]);
        }
        headers("Referer", headers("Referer") + '/');
        if (!url(["dovideo"], 0x1) && !url(['videoloji'], 0x1)) {
            parser();
        } else {
            _0x577d01 = fetch();
            var _0x1cea3c = _0x577d01.match(/"file":\s*"(.*?)"/)[0x1].replace(/\\x/g, '');
            url(hex2a(_0x1cea3c).replace('..', baseUrl(url())));
            try {
                var _0x232d67 = matchAll(_0x577d01, /"file":"(.*?)"/g);
                sub('');
                for (var _0x548179 = 0x0; _0x548179 < _0x232d67.length; _0x548179++) {
                    var _0x160c34 = _0x232d67[_0x548179][0x1];
                    if (_0x160c34.includes("tur")) {
                        sub(_0x160c34.replace(/\\/g, '').replace('..', baseUrl(url())));
                    }
                }
                if (sub() == '') {
                    var _0x160c34 = _0x232d67[_0x232d67.length - 0x1][0x1];
                    sub(_0x160c34.replace(/\\/g, '').replace('..', baseUrl(url())));
                }
            } catch (_0x33eed5) {
                sub('');
            }
            parser();
        }
    }
}

function dizigom() {
    var _0x7218db = fetch().match(/"contentUrl"\s*:\s*"(.*?)"/)[0x1].replace(/\\/g, '').replace("https://", "https://play.");
    _0x7218db = fetch(_0x7218db).match(/>(eval\(.*?\))\s*<\/script>/)[0x1];
    _0x7218db = unPack(_0x7218db).split("\n").join('').match(/sources:(\[.*?\])/)[0x1];
    var _0x38cbf0 = JSON.parse(_0x7218db);
    url(_0x38cbf0[0x0].file);
    parser();
}

function dizikral() {
    headers("x-requested-with", "XMLHttpRequest");
    headers("content-type", "application/x-www-form-urlencoded; charset=UTF-8");
    var _0x205ae3 = fetch();
    var _0xfc5966 = _0x205ae3.match(/<iframe\s*src="(.*?)"/)[0x1];
    if (_0xfc5966.includes("videoseyred") || _0xfc5966.includes("vidmoly")) {
        url(_0xfc5966);
        parser();
        return;
    }
    _0x205ae3 = fetch(_0xfc5966);
    _0x205ae3 = _0x205ae3.match(/bePlayer\('\s*(.*?)'\s*,\s*'(.*?)'\)/);
    var _0xb343e5 = _0x205ae3[0x1];
    var _0x2df414 = _0x205ae3[0x2];
    _0x205ae3 = hdmomplayer(_0xb343e5, _0x2df414);
    sub(_0x205ae3[0x1]);
    url(_0x205ae3[0x0]);
    headers("Accept", '*/*');
    headers("Referer", _0xfc5966);
    parser();
}

function dizilab() {
    var _0x2767c2 = url();
    var _0x29db14 = fetch();
    headers("User-Agent", "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36");
    if (_0x29db14.includes("mobilembeds")) {
        _0x29db14 = _0x29db14.match(/mobilembeds(.*?)Sonra/)[0x1];
    } else {
        _0x29db14 = _0x29db14.match(/fa fa-angle-down(.*?)Sonra/)[0x1];
    }
    var _0x494498 = {};
    try {
        var _0x14b2a6 = matchAll(_0x29db14, /loadVideo\('(.*?)'.*?"icon-tr"><\/span>(.*?)\s*<\/a>/g);
        for (let _0x16e9fe = 0x0; _0x16e9fe < _0x14b2a6.length; _0x16e9fe++) {
            var _0x2c67e3 = _0x14b2a6[_0x16e9fe][0x1];
            var _0x4748ab = _0x14b2a6[_0x16e9fe][0x2].split(" ").join('').split("\n").join('').split("\t").join('');
            _0x494498[_0x4748ab] = _0x2c67e3;
        }
    } catch (_0x3a2e84) {
        error(_0x3a2e84.message);
    }
    if (!_0x2767c2.includes('#') && JSON.stringify(_0x494498) != '{}') {
        Core.showAlternatesJS(JSON.stringify(_0x494498));
    } else {
        url(_0x2767c2.split('#')[0x1]);
        var _0x547d2b = _0x2767c2.split('#')[0x2];
        if (_0x547d2b.toLowerCase().includes("vip")) {
            if (!g.isWebView()) {
                error("NO Webview");
            } else {
                getWebViewOwnContentJS(_0x2767c2, "molystream", "I AM NOT LOOKING", "playSheilaBtn", '', 0x0, false, g.getHeadersJSON, 0x1);
            }
        } else {
            url(_0x494498[_0x547d2b]);
            postData = "vid=" + encodeURIComponent(url()) + "&mobil=1&tip=1&type=loadVideo";
            url(baseUrl(_0x2767c2) + "/ajax");
            headers('Referer', _0x2767c2.split('#')[0x0]);
            headers("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
            headers('X-Requested-With', "XMLHttpRequest");
            _0x29db14 = fetchPost(postData + '');
            g.logHeader();
            url(_0x29db14.match(/src=\\"(.*?)"/)[0x1].replace(/\\/g, ''));
            url("https://dizilab.com", baseUrl(_0x2767c2));
            g.deleteHeader("X-Requested-With");
            g.deleteHeader('Content-Type');
            url(_0x29db14.match(/src=\\"(.*?)\\"/)[0x1].split("\\").join(''));
            url("https://dizilab.com", baseUrl(_0x2767c2));
            if (url(["vplayer", "oplayer"], 0x1)) {
                _0x29db14 = fetch();
                _0x29db14 = Core.fetchCFF(url(), g.getHeadersJSON(), "LÃ¼tfen bekleyiniz") + '';
                if (_0x29db14.includes("cff")) {
                    headers('Cookie', _0x29db14.split(';')[0x0] + ';');
                    _0x29db14 = fetch();
                    if (_0x29db14.includes("LÃ¼tfen bekleyiniz")) {
                        var _0x18b489 = 0x0;
                        while (_0x18b489 < 0xa) {
                            _0x29db14 = Core.fetchCFF(url(), g.getHeadersJSON(), "LÃ¼tfen bekleyiniz");
                            if (_0x29db14.includes('cff')) {
                                headers('Cookie', _0x29db14.split(';')[0x0] + ';');
                                _0x29db14 = fetch();
                            }
                            if (!_0x29db14.includes("LÃ¼tfen bekleyiniz")) {
                                break;
                            }
                            _0x18b489++;
                        }
                    }
                }
                url(fetch().match(/src="(.*?)"/)[0x1]);
            }
            g.deleteHeader.Cookie;
            parser();
        }
    }
}

function dizilla() {
    headers('User-Agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0");
    consolelog(headers("User-Agent"));
    headers('Accept', "*/*");
    var _0x45b68c = url();
    try {
        var _0x516778 = fetch();
        var _0x21718d = _0x516778.match(/<iframe.*?src="(.*?)"/)[0x1];
        if (!_0x21718d.startsWith('https')) {
            _0x21718d = "https:" + _0x21718d;
        }
        if (_0x21718d.includes('dizilla.org/vmplayer')) {
            _0x21718d = "https://vidmoly.to/embed-" + _0x21718d.split("\\?vid=")[0x1] + '.html';
        }
        url(_0x21718d);
        parser();
    } catch (_0xf9267d) {
        findSource(_0x45b68c);
        parser();
    }
}

function dizimat() {
    var _0x2c81ea = fetch();
    var _0x209ace = _0x2c81ea.match(/data-frame=["\']?(.*?)["\'\s*]/)[0x1];
    _0x2c81ea = fetch(_0x209ace);
    url(_0x2c81ea.match(/file\s*:\s*"(.*?m3u8.*?)"/)[0x1]);
    try {
        var _0x55f6aa = _0x2c81ea.match(/tracks:\s*(.*?])/)[0x1];
        _0x55f6aa = _0x55f6aa.split('}');
        for (let _0x41f743 = 0x0; _0x41f743 < _0x55f6aa.length; _0x41f743++) {
            if (_0x55f6aa[_0x41f743].includes('Tur') && _0x55f6aa[_0x41f743].includes(".vtt")) {
                sub(baseUrl(url()) + '' + _0x55f6aa[_0x41f743].match(/file:\s*"(.*?)"/)[0x1]);
            }
        }
    } catch (_0x58f79c) {}
    parser();
}

function dizimia() {
    var _0x42671d = url();
    var _0x1d7af5 = fetch();
    var _0x684828 = {};
    if (g.getLang() == 0x0) {
        Core.setLang(0x1);
    } else {
        Core.setLang(0x0);
    }
    try {
        var _0x45f344 = matchAll(_0x1d7af5, /<a class="focus:outline-none"\s*href="(.*?)"\s*title="(.*?)"/g);
        var _0x2730bc = 0x1;
        for (let _0x2f67bb = 0x0; _0x2f67bb < _0x45f344.length; _0x2f67bb++) {
            if (_0x45f344[_0x2f67bb][0x2] != "Fragman") {
                _0x684828[_0x45f344[_0x2f67bb][0x2]] = _0x45f344[_0x2f67bb][0x1];
                _0x2730bc++;
            }
        }
    } catch (_0x2cf3a2) {
        error(_0x2cf3a2.message);
    }
    if (!_0x42671d.includes('#') && JSON.stringify(_0x684828) != '{}') {
        Core.showAlternatesJS(JSON.stringify(_0x684828));
    } else {
        url(_0x42671d.split('#')[0x1]);
        var _0x1d7af5 = fetch();
        var _0x17a349 = _0x1d7af5.match(/<iframe.*?src="(.*?)"/)[0x1];
        if (!_0x17a349.startsWith("https")) {
            _0x17a349 = "https:" + _0x17a349;
        }
        url(_0x17a349);
        parser();
    }
}

function dizimom() {
    var _0x9a129e = url();
    headers("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    headers("User-Agent", "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36");
    headers("X-Requested-With", "XMLHttpRequest");
    headers('sec-ch-ua-mobile', '?1');
    var _0x5d8bf9 = fetch();
    urls = {};
    singleUrl = '';
    try {
        var _0x56edfd = matchAll(_0x5d8bf9, /iframe.*?src="([^\"]+)".*?<\/iframe>/g);
        for (let _0x58ef07 = 0x0; _0x58ef07 < _0x56edfd.length; _0x58ef07++) {
            if (!_0x56edfd[_0x58ef07][0x1].includes("video_onu")) {
                urls[_0x56edfd[_0x58ef07][0x1]] = _0x56edfd[_0x58ef07][0x1];
                singleUrl = _0x56edfd[_0x58ef07][0x1];
            }
        }
    } catch (_0xd1942d) {}
    if (!_0x9a129e.includes('#') && urls.length > 0x1) {
        Core.showAlternatesJS(JSON.stringify(urls));
    } else {
        if (!_0x9a129e.includes('#')) {
            _0x9a129e += '#' + singleUrl;
        }
        var _0x3218e4 = urls[_0x9a129e.split('#')[0x1]].replace('https://hdplayersystem.live/video/', '');
        if (!_0x3218e4.includes("videoseyred.in") && !_0x3218e4.includes("youtube")) {
            if (_0x3218e4.includes("hdmomplayer")) {
                var _0x5d8bf9 = fetch(_0x3218e4);
                _0x5d8bf9 = _0x5d8bf9.match(/bePlayer\('(.*?)',\s*'(.*?)'\)/);
                headers('Referer', _0x3218e4);
                headers("Accept", "*/*");
                headers("Origin", baseUrl(_0x3218e4));
                var _0x57c67d = _0x5d8bf9[0x1];
                var _0xb12b0e = _0x5d8bf9[0x2];
                _0x5d8bf9 = hdmomplayer(_0x57c67d, _0xb12b0e);
                sub(_0x5d8bf9[0x1]);
                url(_0x5d8bf9[0x0]);
            } else {
                if (_0x3218e4.includes("index.php") || _0x3218e4.includes("peacemakerst")) {
                    url(_0x3218e4 + "&do=getVideo");
                } else {
                    url("https://hdplayersystem.live/player/index.php?data=" + _0x3218e4 + "&do=getVideo");
                }
                var _0x5d8bf9 = fetchPost("hash=" + _0x3218e4 + '&r=' + encodeURIComponent(_0x9a129e) + ')');
                var _0x221304 = JSON.parse(_0x5d8bf9);
                if (_0x221304.hasOwnProperty("securedLink")) {
                    url(_0x221304.securedLink.replace(/\\\//g, '/'));
                } else {
                    url(_0x221304.videoSources[0x0].file);
                }
            }
        } else {
            _0x3218e4 = _0x3218e4.replace('https://videoseyred.in/embed/', '').replace("?hideTitle=1", '');
            var _0x5d8bf9 = fetch("https://videoseyred.in/playlist/" + _0x3218e4 + ".json");
            var _0x221304 = JSON.parse(_0x5d8bf9);
            url(_0x221304[0x0].sources[0x0].file);
            var _0x5d012c = _0x221304[0x0].tracks;
            for (var _0x4f0be3 = 0x0; _0x4f0be3 < _0x5d012c.length; _0x4f0be3++) {
                if (_0x5d012c[_0x4f0be3].hasOwnProperty('language')) {
                    if (_0x5d012c[_0x4f0be3].language == "tur") {
                        sub(_0x5d012c[_0x4f0be3].file);
                    }
                }
            }
            headers("Referer", "https://videoseyred.in/");
        }
        parser();
    }
}

function dizipal() {
    headers("User-Agent", "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36");
    var _0x3fc1c8 = fetch();
    url(_0x3fc1c8.match(/data-src="(.*?)"/)[0x1]);
    _0x3fc1c8 = fetch();
    url(_0x3fc1c8.match(/file:"(.*?)"/)[0x1]);
    try {
        var _0x5e0dd3 = matchAll(_0x3fc1c8, /\](http.*?\.vtt)/g);
        for (let _0x23ca45 = 0x0; _0x23ca45 < _0x5e0dd3.length; _0x23ca45++) {
            if (_0x5e0dd3[_0x23ca45][0x1].includes("Turkce") || _0x5e0dd3[_0x23ca45][0x1].includes('tr') || _0x5e0dd3[_0x23ca45][0x1].includes('_tur')) {
                sub(_0x5e0dd3[_0x23ca45][0x1]);
            }
        }
    } catch (_0x388892) {
        sub('');
    }
    parser();
}

function diziplus() {
    var _0x2a606f = '';
    _0x2a606f = fetch();
    var _0x1180a4 = _0x2a606f.match(/data-frame="(.*?)"/)[0x1];
    if (!_0x1180a4.includes("vidmoxy")) {
        _0x2a606f = fetch(_0x1180a4);
        var _0x5735c8 = _0x2a606f.match(/bePlayer\('(.*?)',\s*'(.*?)'\)/);
        var _0x2b8f12 = _0x5735c8[0x1];
        var _0x6612af = _0x5735c8[0x2];
        headers("Referer", _0x1180a4);
        _0x2a606f = hdmomplayer(_0x2b8f12, _0x6612af);
        sub(_0x2a606f[0x1]);
        _0x2a606f = _0x2a606f[0x0];
        headers('Accept', "*/*");
    } else {
        _0x2a606f = _0x1180a4;
    }
    url(_0x2a606f);
    parser();
}

function dizipod() {
    var _0x53d6b3 = '';
    var _0x52716b = baseUrl(url());
    _0x53d6b3 = fetch();
    try {
        var _0x52c0bc = _0x53d6b3.match(/data-post-id="(.*?)"/)[0x1];
        _0x53d6b3 = fetchPost('', _0x52716b + "/wp/wp-admin/admin-ajax.php?action=get_episode_player&post_id=" + _0x52c0bc);
        var _0x5bb5b8 = JSON.parse(_0x53d6b3);
        url(_0x5bb5b8.data.match(/src="(.*?)"/)[0x1]);
        _0x53d6b3 = fetch();
        var _0x1077b3 = _0x53d6b3.match(/text\/javascript">(eval.*?)<\/sc/)[0x1];
        _0x53d6b3 = unPack(_0x1077b3).match(/sources\s*:\s*\[([\s\S]*?)\]/)[0x1];
        _0x5bb5b8 = JSON.parse(_0x53d6b3);
        url(fixUrl(_0x5bb5b8.file));
    } catch (_0x27ad60) {}
    parser();
}

function dizipub() {
    var _0x40a3f7 = url();
    if (g.getLang() == 0x2) {
        Core.setLang(0x1);
    }
    headers("User-Agent", "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36");
    var _0x48cabd = '';
    try {
        var _0x48cabd = fetch();
        _0x48cabd = _0x48cabd.match(/series-alter-active(.*?) <\/ul>/)[0x1];
        var _0x43f7fb = {};
        try {
            var _0x2d1f6d = matchAll(_0x48cabd, /<(?:span class=|a.*?href=)"(.*?)"\s*title="(.*?)"/g);
            for (let _0x4fe311 = 0x0; _0x4fe311 < _0x2d1f6d.length; _0x4fe311++) {
                var _0x427cf6 = _0x2d1f6d[_0x4fe311][0x1];
                var _0xf5c100 = _0x2d1f6d[_0x4fe311][0x2];
                _0x43f7fb[_0xf5c100] = _0x427cf6;
            }
        } catch (_0x402737) {
            error(_0x402737.message);
        }
        if (!_0x40a3f7.includes('#') && JSON.stringify(_0x43f7fb) != '{}') {
            Core.showAlternatesJS(JSON.stringify(_0x43f7fb));
        } else {
            url(_0x40a3f7.split('#')[0x1]);
            try {
                _0x48cabd = fetch();
                url(_0x48cabd.match(/<iframe.*?src="(.*?)".*?allowfullscreen.*?<\/iframe>/)[0x1]);
                url(fixUrl(url()));
            } catch (_0x21b44f) {
                findSource(_0x40a3f7.split('#')[0x0]);
            }
            parser();
        }
    } catch (_0x121b66) {
        findSource(_0x40a3f7.split('#')[0x0]);
        parser();
    }
}

function dizirix() {
    var _0x4481b6 = url();
    headers("User-Agent", "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36");
    if (!_0x4481b6.includes('#')) {
        var _0x153f4e = fetch();
        var _0x39d8c5 = "dublaj";
        if (g.getLang() == 0x1) {
            _0x39d8c5 = "altyazili";
        }
        var _0x2e2c55 = _0x153f4e.match(/var\s*bID\s*=\s*"(\d*)"/)[0x1];
        var _0x54bb22 = 'whichOne=' + _0x39d8c5 + "&bId=" + _0x2e2c55;
        url(baseUrl(url()) + "/ajax/request=getLanguage");
        _0x153f4e = fetchPost(_0x54bb22);
        var _0x3002d0 = {};
        try {
            var _0xbbb0e1 = matchAll(_0x153f4e, /data-code=\\\"(.*?)\\\".*?span>(.*?)</g);
            for (let _0x1d94d1 = 0x0; _0x1d94d1 < _0xbbb0e1.length; _0x1d94d1++) {
                var _0x597a8a = _0xbbb0e1[_0x1d94d1][0x1];
                var _0x54e69b = _0xbbb0e1[_0x1d94d1][0x2];
                _0x3002d0[_0x54e69b] = _0x597a8a;
            }
        } catch (_0x141e1d) {
            error(_0x141e1d.message);
        }
        Core.showAlternatesJS(JSON.stringify(_0x3002d0));
    } else {
        url(_0x4481b6.split('#')[0x1]);
        headers("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
        var _0x153f4e = fetchPost("dataCode=" + url(), baseUrl(_0x4481b6) + "/ajax/request=getFrames");
        _0x153f4e = atob(_0x153f4e);
        url(_0x153f4e.match(/src="(.*?)"/)[0x1]);
        g.deleteHeader("Content-Type");
        if (url(["prixy.php", "source=rix2", "source-yg", "proxy.php"], 0x1)) {
            headers('upgrade-insecure-requests', '1');
            _0x153f4e = fetch();
            url('dummy');
            try {
                url(_0x153f4e.match(/file:"(.*?)"/)[0x1]);
                var _0x2eb5bb = _0x153f4e.match(/"file":.*?"(.*?)"/) || [];
                if (_0x2eb5bb.length > 0x0) {
                    sub(_0x2eb5bb[0x1]);
                }
            } catch (_0x40f504) {
                url(_0x153f4e.match(/Back.*?'(https.*?)'/)[0x1]);
            }
            g.deleteHeader('upgrade-insecure-requests');
            headers("Origin", baseUrl(_0x4481b6));
        }
        parser();
    }
}

function diziroll() {
    var _0x431ffe = fetch();
    _0x431ffe = _0x431ffe.match(/focus\:outline-none"\s*href="(.*?)"\s*title="(.*?)"\s*data-navigo/)[0x1];
    _0x431ffe = fetch(_0x431ffe);
    try {
        var _0x3aa6cf = matchAll(_0x431ffe, /class="player".*?iframe.*?src="(.*?)"/g);
        for (let _0x5471b0 = 0x0; _0x5471b0 < _0x3aa6cf.length; _0x5471b0++) {
            if (!_0x3aa6cf[_0x5471b0][0x1].includes("finema")) {
                url(_0x3aa6cf[_0x5471b0][0x1]);
                break;
            }
        }
    } catch (_0x401e0d) {
        error(_0x401e0d.message);
    }
    if (g.getLang() == 0x2) {
        Core.setLang(0x0);
    }
    url(fixUrl(url()));
    parser();
}

function dizitime() {
    var _0x1d4a3d = url();
    var _0xcbc778 = fetch();
    var _0x15e6b2 = {};
    try {
        var _0x1f5b59 = matchAll(_0xcbc778, /data-name="(.*?)"\s*data-oid="(.*?)"/g);
        for (let _0x27202d = 0x0; _0x27202d < _0x1f5b59.length; _0x27202d++) {
            var _0xf0e4bf = _0x1f5b59[_0x27202d][0x2];
            var _0x1617bb = _0x1f5b59[_0x27202d][0x1];
            if (!_0x15e6b2.hasOwnProperty(_0x1617bb) && !_0x1617bb.toLowerCase().includes("odnok")) {
                _0x15e6b2[_0x1617bb] = _0xf0e4bf;
            }
        }
    } catch (_0x2bd94) {
        error(_0x2bd94.message);
    }
    if (!_0x1d4a3d.includes('#') && JSON.stringify(_0x15e6b2) != '{}') {
        Core.showAlternatesJS(JSON.stringify(_0x15e6b2));
    } else {
        url(_0x1d4a3d.split('#')[0x1]);
        var _0x4af627 = _0x1d4a3d.split('#')[0x2];
        if (_0x4af627.toLowerCase().includes("time")) {
            if (!g.isWebView()) {
                error("NO Webview");
            } else {
                getWebViewOwnContentJS(_0x1d4a3d, 'molystream.org', "I AM NOT LOOKING", "playSheilaBtn", '', 0x0, false, g.getHeadersJSON(), 0x1);
            }
        } else {
            url(_0x15e6b2[_0x4af627]);
            headers("Referer", baseUrl(_0x1d4a3d));
            url(baseUrl(_0x1d4a3d) + '/getvideo/' + url() + '_t');
            url(Core.getRedirectUrlJS(url()));
            parser();
        }
    }
}

function diziwatch() {
    var _0x3e0895 = fetch();
    if (!_0x3e0895.includes("<iframe")) {
        _0x3e0895 = _0x3e0895.toLowerCase();
        var _0x1a424e = _0x3e0895.match(/url\s*:\s*"(http[^"]+php)".*?\'pid\'\s*:\s*(\d+),/);
        _0x3e0895 = fetch(_0x1a424e[0x1] + "?action=playlist&pid=" + _0x1a424e[0x2]).toLowerCase();
        var _0x30c8eb = JSON.parse(_0x3e0895);
        url(_0x30c8eb[0x0].sources[0x0].file);
    } else {
        var _0x1a424e = _0x3e0895.match(/<iframe\s*src="(.*?)".*?allowfullscreen>/)[0x1];
        _0x3e0895 = fetch(_0x1a424e);
        url(_0x3e0895.match(/'\/playlist\/(.*?).json';/)[0x1]);
        _0x3e0895 = fetch("https://videoseyred.in/playlist/" + url() + '.json');
        var _0x45eaf9 = JSON.parse(_0x3e0895);
        url(_0x45eaf9[0x0].sources[0x0].file);
        var _0x84c885 = _0x45eaf9[0x0].tracks;
        for (var _0x59befa = 0x0; _0x59befa < _0x84c885.length; _0x59befa++) {
            if (_0x84c885[_0x59befa].hasOwnProperty("language")) {
                if (_0x84c885[_0x59befa].language == "tur") {
                    sub(_0x84c885[_0x59befa].file);
                }
            }
        }
        headers('Referer', "https://videoseyred.in/");
    }
    parser();
}

function diziyo() {
    headers('User-Agent', "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36");
    var _0x3c8d46 = fetch();
    var _0x278de1 = _0x3c8d46.match(/id="player-option-1"\s*class=".*?"\s*data-type="(.*?)"\s*data-post=".*?"\s*data-nume=".*?"/)[0x1];
    var _0x157534 = _0x3c8d46.match(/id="player-option-1"\s*class=".*?"\s*data-type=".*?"\s*data-post="(.*?)"\s*data-nume=".*?"/)[0x1];
    var _0x3c0888 = _0x3c8d46.match(/id="player-option-1"\s*class=".*?"\s*data-type=".*?"\s*data-post=".*?"\s*data-nume="(.*?)"/)[0x1];
    var _0x54c293 = 'action=doo_player_ajax&post=' + _0x157534 + '&nume=' + _0x3c0888 + '&type=' + _0x278de1;
    _0x3c8d46 = fetchPost(_0x54c293, baseUrl(url()) + "/wp-admin/admin-ajax.php");
    _0x3c8d46 = _0x3c8d46.match(/src='(.*?)'/)[0x1];
    var _0x54a18a = _0x3c8d46.split('/');
    var _0x32c359 = _0x54a18a[_0x54a18a.length - 0x1];
    _0x54c293 = "hash=" + _0x32c359 + "&r=" + baseUrl(url()) + '/';
    headers("X-Requested-With", 'XMLHttpRequest');
    var _0x591e4e = fetchPost(_0x54c293, _0x3c8d46 + "?do=getVideo");
    headers("Referer", _0x3c8d46);
    var _0xa143e4 = JSON.parse(_0x591e4e);
    url(_0xa143e4.videoSources[0x0].file);
    g.deleteHeader("X-Requested-With");
    headers('Accept', '*/*');
    parser();
}

function diziyou() {
    var _0x3f4cf7 = fetch();
    url(_0x3f4cf7.match(/<iframe.*?src="(.*?)"/)[0x1]);
    if (g.getLang() == 0x0) {
        url(url(".html", '_tr.html'));
    }
    var _0x3f4cf7 = fetch();
    sub(_0x3f4cf7.match(/<track\s*src="(.*?)"/)[0x1]);
    url(_0x3f4cf7.match(/<source.*?src="(.*?)"/)[0x1]);
    parser();
}

function dood() {
    url(fixUrl(url()));
    url('.so', ".yt");
    url('.pm', ".yt");
    url('dooood.com', "dood.la");
    var _0x50c333 = fetch().match(/dsplayer\.hotkeys[^']+'([^']+).+?function\s*makePlay.+?return[^?]+([^"]+)/);
    var _0x4290e4 = "https://d0000d.com" + _0x50c333[0x1];
    var _0x13ecce = '';
    for (var _0x44d39b = 0x0; _0x44d39b < 0xa; _0x44d39b++) {
        _0x13ecce += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789".charAt(Math.floor(Math.random() * "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789".length));
    }
    var _0x19b8b8 = new Date().getTime();
    headers('Referer', "https://d0000d.com");
    url(fetch(_0x4290e4) + _0x13ecce + _0x50c333[0x2] + _0x19b8b8 + "#.mp4");
    parser();
}

function dreamturk() {
    var _0x5756c7 = fetch().match(/data-id="(.*?)"/)[0x1];
    url("https://www.dreamturk.com.tr/actions/content/media/" + _0x5756c7);
    var _0x147b75 = JSON.parse(fetch());
    url(_0x147b75.Media.Link.ServiceUrl + _0x147b75.Media.Link.SecurePath);
    parser();
}

function filemoon() {
    data = fetch();
    try {
        data = (data + '').match(/text\/javascript.*?\s*(eval.*?)<\/sc/)[0x1];
    } catch (_0x485c4c) {
        try {
            data = (data + '').match(/<iframe\s*src="(.*?)"/)[0x1];
            headers("Accept-Language", 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7');
            headers("sec-fetch-dest", 'iframe');
            data = fetch(data);
            data = (data + '').match(/text\/javascript.*?(eval.*?)<\/script/)[0x1];
        } catch (_0x49e804) {
            data = fetch();
            data = (data + '').match(/text\/javascript.*?(eval.*?)<\/script/)[0x1];
        }
    }
    url(unPack(data));
    try {
        url(url().match(/file:"(.*?m3u8)"/)[0x1]);
    } catch (_0x59f427) {
        url(url().match(/file\s*:"(.*?)"/)[0x1]);
    }
    parser();
}

function filmatek() {
    var _0x42a5b5 = url();
    var _0x5cabce = 0x1;
    var _0x1054cf = fetch();
    var _0x3aa015 = {};
    try {
        var _0x5b8ac7 = matchAll(_0x1054cf, /(\d+)\.\s*KÄ±sÄ±m/g);
        var _0x135fbc = 0x1;
        for (let _0x952b40 = 0x0; _0x952b40 < _0x5b8ac7.length; _0x952b40++) {
            if (!_0x5b8ac7[_0x952b40][0x1].includes("youtube")) {
                if (_0x42a5b5.includes('#')) {
                    if (_0x5b8ac7[_0x952b40][0x1] == _0x42a5b5.split('#')[0x1]) {
                        _0x5cabce = _0x952b40 + 0x1;
                    }
                }
                _0x3aa015["BÃ¶lÃ¼m " + _0x135fbc] = _0x5b8ac7[_0x952b40][0x1];
                _0x135fbc++;
            }
        }
    } catch (_0x23ab2e) {
        error(_0x23ab2e.message);
    }
    if (!_0x42a5b5.includes('#') && JSON.stringify(_0x3aa015) != '{}') {
        Core.showAlternatesJS(JSON.stringify(_0x3aa015));
    } else {
        if (_0x42a5b5.includes('#')) {
            _0x5cabce = _0x42a5b5.split('#')[0x1];
        }
        var _0x59154b = _0x1054cf.match(/layer_api":"(.*?)","play_aj/)[0x1];
        var _0x413b7e = _0x1054cf.match(/data-post='(\d+)'/)[0x1];
        url(_0x59154b.replace(/\\\//g, '/') + _0x413b7e + "/movie/" + _0x5cabce);
        var _0x1054cf = fetch();
        try {
            var _0x267395 = JSON.parse(_0x1054cf);
            url(_0x267395.embed_url);
            _0x1054cf = fetch();
            url(_0x1054cf.match(/"file"\s*:\s*"(.*?)"/)[0x1].replace(/\\\//g, '/'));
            parser();
        } catch (_0x33975c) {
            error(_0x33975c.message);
        }
    }
}

function filmcidayi() {
    var _0x4f6ec2 = fetch();
    var _0x41ae1e = "movie";
    if (url(["/bolum"], 0x1)) {
        _0x41ae1e = 'tv';
    }
    var _0x441445 = _0x4f6ec2.match(/data-post=[\'"](.*?)[\'"]/)[0x1];
    headers("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    _0x4f6ec2 = fetchPost("action=doo_player_ajax&post=" + _0x441445 + "&nume=1&type=" + _0x41ae1e, baseUrl(url()) + "/wp-admin/admin-ajax.php");
    var _0x10f216 = JSON.parse(_0x4f6ec2).embed_url;
    _0x4f6ec2 = fetchPost(_0x4f6ec2, _0x10f216);
    var _0x398ef7 = _0x4f6ec2.match(/bePlayer\('(.*?)',\s*'(.*?)'\);/)[0x1];
    var _0x559c4b = _0x4f6ec2.match(/bePlayer\('(.*?)',\s*'(.*?)'\);/)[0x2];
    consolelog(_0x559c4b);
    _0x4f6ec2 = getAes(_0x398ef7, _0x559c4b).split("video_location] => ")[0x1].split('==')[0x0] + '==';
    url(_0x4f6ec2);
    g.deleteHeader('Content-Type');
    headers("Referer", _0x10f216);
    headers('Accept', '*/*');
    headers("Origin", "https://hotstream.club");
    parser();
}

function filmekseni() {
    var _0x457a30 = url();
    headers("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    headers("X-Requested-With", "XMLHttpRequest");
    var _0x1ba740 = fetch();
    try {
        _0x1ba740 = _0x1ba740.match("tab-pane active(.*?)</nav>")[0x1];
    } catch (_0x58740e) {
        error('Telif');
    }
    var _0x2aef0e = {};
    try {
        var _0x2ebf8b = matchAll(_0x1ba740, /href="(.*?)">\s*(.*?)\s*<\/a>/g);
        for (let _0x17d6c1 = 0x0; _0x17d6c1 < _0x2ebf8b.length; _0x17d6c1++) {
            _0x2aef0e[_0x2ebf8b[_0x17d6c1][0x2]] = _0x2ebf8b[_0x17d6c1][0x1];
        }
    } catch (_0x1b20c7) {}
    if (!_0x457a30.includes('#')) {
        Core.showAlternatesJS(JSON.stringify(_0x2aef0e));
    } else {
        url(_0x457a30.split('#')[0x1]);
        var _0x1ba740 = fetch();
        url(_0x1ba740.match(/iframe.*?data-src="(.*?)"/)[0x1]);
        if (url(['vidload'], 0x1)) {
            url(fixUrl(url()));
            var _0x4a4fc0 = new Date();
            _0x4a4fc0 = _0x4a4fc0.getTime();
            var _0x45406f = url().split('/')[url().split('/').length - 0x1];
            var _0x1c5bb8 = baseUrl(url());
            url(_0x1c5bb8 + "/ajax/" + _0x45406f + '?' + _0x4a4fc0);
            headers("Referer", _0x1c5bb8);
            var _0x1489ff = fetch(_0x1c5bb8 + '/video.js?' + _0x4a4fc0);
            var _0x35a39b = _0x1489ff.match("window,'(.*?)','.*?','.*?'")[0x1];
            var _0x505d98 = _0x1489ff.match("window,'.*?','(.*?)','.*?'")[0x1];
            headers(_0x35a39b, _0x505d98);
            _0x1ba740 = fetch();
            var _0x15f93b = JSON.parse(_0x1ba740);
            url(_0x15f93b.file + '?' + _0x15f93b.hash);
            url(Core.getRedirectUrlJS(url()));
        } else {
            url(fixUrl(url()));
            _0x1ba740 = fetch();
            url(baseUrl(url()) + _0x1ba740.match(/<source src="(.*?)" type="application\/x-mpegURL">/)[0x1]);
            headers("Referer", _0x457a30);
        }
        parser();
    }
}

function filmfav() {
    var _0x19c1f2 = fetch().match(/<iframe\s*src="(.*?)"/)[0x1];
    var _0x5055a = fetch(_0x19c1f2);
    _0x5055a = _0x5055a.match(/bePlayer\('\s*(.*?)'\s*,\s*'(.*?)'\)/);
    var _0x3db004 = _0x5055a[0x1];
    var _0x9e8da6 = _0x5055a[0x2];
    _0x5055a = hdmomplayer(_0x3db004, _0x9e8da6);
    sub(_0x5055a[0x1]);
    url(_0x5055a[0x0]);
    headers('Referer', _0x19c1f2);
    headers("Accept", '*/*');
    parser();
}

function filmizle4k() {
    var _0x4737aa = fetch(fetch().match(/<p><iframe.*?src="(.*?)".*?/)[0x1]);
    try {
        var _0x5abafc = JSON.parse(_0x4737aa.match(/jwSetup\.tracks\s*=\s*(\[.*?\])/)[0x1]);
        for (let _0x1f6dc6 = 0x0; _0x1f6dc6 < _0x5abafc.length; _0x1f6dc6++) {
            if (_0x5abafc[_0x1f6dc6].hasOwnProperty("label") && _0x5abafc[_0x1f6dc6].label.includes("Ã¼rkÃ§e")) {
                sub(_0x5abafc[_0x1f6dc6].file);
            }
        }
        sub(sub().replace('.vtt', '.srt'));
    } catch (_0x2f2bd3) {}
    url(decryptFor4KIzle(_0x4737aa.match(/"file":\s*av\('(.*?)'\),/)[0x1]));
    parser();
}

function filmizlemek() {
    error("4kfilmizlemek isimli kaynak site kapalÄ± olduÄŸundan oynatÄ±lamÄ±yor.");
    var _0x555f43 = url();
    var _0x4e8db6 = fetch();
    var _0x257229 = {};
    try {
        var _0x320de2 = matchAll(_0x4e8db6, /class="parttab.*?href="(.*?)".*?<\/i>(.*?)</g);
        for (let _0x409720 = 0x0; _0x409720 < _0x320de2.length; _0x409720++) {
            alt = _0x320de2[_0x409720][0x2].trim().replace('HD', '');
            if (!alt.includes("ragman")) {
                _0x257229[alt + _0x409720] = fixUrl(_0x320de2[_0x409720][0x1]);
            }
        }
    } catch (_0x581a2a) {
        error(_0x581a2a.message);
    }
    if (!_0x555f43.includes('#') && JSON.stringify(_0x257229) != '{}') {
        Core.showAlternatesJS(JSON.stringify(_0x257229));
    } else {
        if (_0x555f43.includes('#')) {
            part = _0x555f43.split('#')[0x1];
        }
        consolelog(part);
        _0x4e8db6 = fetch(part);
        url(_0x4e8db6.match(/<iframe.*?src="(.*?)"/)[0x1]);
        parser();
    }
}

function filmizlesene() {
    var _0x30bf9d = url();
    headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36";
    var _0x4a6447 = fetch();
    var _0x41d79d = '';
    if (_0x4a6447.includes("vidcontainer")) {
        _0x41d79d = _0x4a6447.match(/(?:inepisode|bolumler)(.*?)vidcontainer/)[0x1];
    }
    if (_0x41d79d == '' && !_0x30bf9d.includes('#')) {
        _0x4a6447 = _0x4a6447.match(/iframe\s*src="(.*?)"/)[0x1];
        if (_0x4a6447.includes("/ok/")) {
            var _0x4b02f3 = _0x4a6447.split('?v=')[0x1];
            _0x4b02f3 = atob(_0x4b02f3);
            url('https://odnoklassniki.ru/videoembed/' + _0x4b02f3);
        } else {
            url(_0x4a6447);
        }
        parser();
    } else {
        _0x4a6447 = _0x41d79d;
        if (!_0x30bf9d.includes('#')) {
            var _0x11bfba = {};
            try {
                var _0x12b6b2 = matchAll(_0x4a6447, /dil="(.*?)">(.*?)<.*?iframe\s*src="(.*?)"/g);
                for (let _0x53e314 = 0x0; _0x53e314 < _0x12b6b2.length; _0x53e314++) {
                    if (_0x22d122 != "opn" && _0x22d122 != 'up') {
                        var _0x2adc74 = _0x12b6b2[_0x53e314][0x3];
                        var _0x22d122 = _0x12b6b2[_0x53e314][0x2] + ", " + _0x12b6b2[_0x53e314][0x1];
                        _0x11bfba[_0x22d122] = _0x2adc74;
                    }
                }
            } catch (_0x5e1662) {
                error(_0x5e1662.message);
            }
            Core.showAlternatesJS(JSON.stringify(_0x11bfba));
        } else {
            url(_0x30bf9d.split('#')[0x1]);
            if (url(["vidmoly"], 0x1)) {
                url(url().match(/vid=(.*?)$/)[0x1]);
            } else {
                if (url(["mail.ru"], 0x1)) {} else {
                    _0x4a6447 = fetch();
                    _0x4a6447 = _0x4a6447.match(/iframe\s*src=(?:\'|")(.*?)(?:\'|")/)[0x1];
                    if (_0x4a6447.includes("hdplayer") || _0x4a6447.includes("vidmo")) {
                        var _0x24a114 = fetchResponseHeader(url(), g.getHeadersJSON(), 'set-cookie');
                        headers("Cookie", '');
                        try {
                            _0x24a114 = _0x24a114.match(/(PHPS.*?;)/)[0x1];
                            headers("Cookie", _0x24a114 + '');
                            g.logHeader();
                        } catch (_0x582d89) {}
                        _0x24a114 = fetchResponseHeader(_0x4a6447, g.getHeadersJSON(), "set-cookie");
                        headers("Cookie", headers("Cookie") + _0x24a114);
                        _0x4a6447 = fetch(_0x4a6447);
                        g.logHeader();
                        var _0x14d23a = false;
                        _0x4a6447 = _0x4a6447.match(/iframe.*?src\s*=\s*"(.*?)"/)[0x1];
                        if (_0x4a6447.includes("odnoklass")) {
                            url(_0x4a6447);
                            _0x14d23a = true;
                        }
                        if (!_0x4a6447.includes("hdplayer")) {
                            url(_0x4a6447 + '/sheila');
                            g.deleteHeader("Cookie");
                            headers("Referer", _0x4a6447);
                            _0x14d23a = true;
                        }
                    } else {
                        url(_0x4a6447);
                    }
                }
            }
            parser();
        }
    }
}

function filmkovasi() {
    try {
        var _0x5de889 = fetch();
    } catch (_0x5b9867) {
        error("Telif");
    }
    var _0x2a7198 = _0x5de889.match(/iframe.*?src=["']?(.*?)[\s>"']/)[0x1];
    if (!_0x2a7198.includes("trstx") && !_0x2a7198.includes("sobreatsesuyp") && !_0x2a7198.includes("vidrame")) {
        if (g.getLang() == '1') {
            url(url() + '2/');
            var _0x5de889 = fetch();
            _0x2a7198 = _0x5de889.match(/iframe.*?src=["']?(.*?)[\s>"']/)[0x1];
        }
        headers('Referer', _0x2a7198);
        _0x5de889 = fetch(_0x2a7198);
        var _0x5c6173 = baseUrl(_0x2a7198);
        var _0x107224 = _0x5de889.match(/uid":"(.*?)"/)[0x1];
        var _0x8788db = _0x5de889.match(/md5":"(.*?)"/)[0x1];
        var _0x1cdbd5 = _0x5de889.match(/"id":"(.*?)"/)[0x1];
        var _0x4dc691 = _0x5de889.match(/status":"(.*?)"/)[0x1];
        _0x2a7198 = _0x5de889.match(/file:\s*(.*?m3u8.*?),/)[0x1];
        _0x2a7198 = _0x5c6173 + _0x2a7198.replace('`', '').replace('`', '').replace("${video.uid}", _0x107224).replace("${video.id}", _0x1cdbd5).replace("${video.status}", _0x4dc691).replace("${video.md5}", _0x8788db);
        headers("Accept", '*/*');
        headers("accept-language", "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7");
    }
    url(_0x2a7198);
    consolelog(_0x2a7198);
    parser();
}

function filmmakinesi() {
    headers("User-Agent", 'Google');
    try {
        var _0x4daa52 = fetch(fetch().match(/<iframe.*?src="(https:\/\/closeload.filmmakinesi.*?embed.*?)"/)[0x1]);
    } catch (_0x3ae249) {
        if (fetch().toLowerCase().includes("telif haklar")) {
            error("Telif");
        }
    }
    var _0x3e5a8b = "https://closeload." + baseUrl(url(), true);
    try {
        var _0x3e7eb1 = matchAll(_0x4daa52, /<track src="(.*?)"\s*kind="captions"/g);
        for (let _0x361b63 = 0x0; _0x361b63 < _0x3e7eb1.length; _0x361b63++) {
            if (_0x3e7eb1[_0x361b63][0x1].includes('tr')) {
                sub(_0x3e5a8b + '/' + _0x3e7eb1[_0x361b63][0x1]);
                break;
            }
        }
    } catch (_0x134cfa) {}
    _0x4daa52 = _0x4daa52.match(/(eval.*?)<\/script>/)[0x1];
    _0x4daa52 = unPack(_0x4daa52);
    var _0x30285e = _0x4daa52.match(/function\s*(dc_.*?)\(value_parts\)/)[0x1];
    var _0x2ef4c7 = _0x30285e + "\\(.*?\\)\\s*{([\\s\\S]*?)}\\s*func";
    var _0x359fbc = new RegExp(_0x2ef4c7);
    var _0x5419f3 = _0x359fbc.exec(_0x4daa52);
    var _0x2a9053 = "function test(value_parts){" + _0x5419f3[0x1] + '}';
    eval(_0x2a9053);
    _0x2ef4c7 = "=\\s*" + _0x30285e + "\\((.*?)\\)";
    _0x359fbc = new RegExp(_0x2ef4c7);
    _0x5419f3 = _0x359fbc.exec(_0x4daa52);
    var _0x50254e = _0x5419f3[0x1];
    try {
        _0x50254e = JSON.parse(_0x50254e);
    } catch (_0x12933f) {}
    _0x50254e = test(_0x50254e);
    url(_0x50254e);
    headers('Referer', _0x3e5a8b);
    g.setMediaType("mimeType:MPEG-TS");
    parser();
}

function filmmax() {
    var _0x46da27 = fetch();
    var _0x161834 = _0x46da27.match(/iframe.*?src="(.*?)"/)[0x1];
    _0x46da27 = fetch(_0x161834);
    url(_0x46da27.match(/'\/playlist\/(.*?).json';/)[0x1]);
    _0x46da27 = fetch("https://videoseyred.in/playlist/" + url() + ".json");
    var _0x5bfe6a = JSON.parse(_0x46da27);
    url(_0x5bfe6a[0x0].sources[0x0].file);
    var _0xbd27fc = _0x5bfe6a[0x0].tracks;
    for (var _0x2465db = 0x0; _0x2465db < _0xbd27fc.length; _0x2465db++) {
        if (_0xbd27fc[_0x2465db].hasOwnProperty("language")) {
            if (_0xbd27fc[_0x2465db].language == "tur") {
                sub(_0xbd27fc[_0x2465db].file);
            }
        }
    }
    headers("Referer", "https://videoseyred.in/");
    parser();
}

function filmmodu() {
    var _0x3dabde = JSON.parse(fetch());
    if (_0x3dabde.hasOwnProperty("subtitle")) {
        sub(baseUrl(url()) + _0x3dabde.subtitle);
    }
    var _0x3821fe = _0x3dabde.sources;
    _0x3821fe.sort(function(_0x4c7083, _0x3dc83b) {
        return _0x4c7083.label.localeCompare(_0x3dc83b.label);
    });
    url(_0x3821fe[0x0].src);
    parser();
}

function filmon() {
    url(url("https://www.filmon.com/", ''));
    var _0x441b1e = "channel_id=" + url() + "&quality=low";
    headers("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    headers("X-Requested-With", "XMLHttpRequest");
    headers('Cookie', "PHPSESSID=");
    var _0x59a34b = fetchPost(_0x441b1e, "https://www.filmon.com/ajax/getChannelInfo");
    var _0x445a91 = JSON.parse(_0x59a34b);
    url(_0x445a91.serverURL);
    parser();
}

function fullhdfilm() {
    var _0x380b7c = url();
    var _0x1d041d = fetch();
    var _0x430d9d = {};
    try {
        var _0xaa850d = matchAll(_0x1d041d, /id='(\d+)'.*?href=\"#\">(.*?)<\/a><\/li>/g);
        for (let _0x366ad9 = 0x0; _0x366ad9 < _0xaa850d.length; _0x366ad9++) {
            _0x430d9d[_0xaa850d[_0x366ad9][0x2]] = fixUrl(_0xaa850d[_0x366ad9][0x1]);
        }
    } catch (_0x108d75) {
        error(_0x108d75.message);
    }
    if (!_0x380b7c.includes('#') && JSON.stringify(_0x430d9d) != '{}') {
        Core.showAlternatesJS(JSON.stringify(_0x430d9d));
    } else {
        if (_0x380b7c.includes('#')) {
            part = _0x380b7c.split('#')[0x1].replace("https://", '');
        }
        var _0x215607 = "pdata\\['prt_" + part + "'\\]\\s*=\\s*'(.*?)'";
        var _0x47ccd8 = new RegExp(_0x215607);
        var _0x13ab22 = 'PGlmcmFtZSB' + _0x1d041d.match(_0x47ccd8)[0x1];
        var _0x1e0475 = g.base64Decode(_0x13ab22);
        url(_0x1e0475.match(/src=["\\\'](.*?)["\\\']/)[0x1]);
        parser();
    }
}

function fullhdfilmizlesene() {
    var _0x32dc3f = url();
    var _0x253e5b = fetch().match(/var\s*scx\s*=\s*(.*?);/)[0x1];
    var _0x415485 = JSON.parse(_0x253e5b);
    var _0x34523d = 'tr';
    var _0x46a2c2 = {};
    var _0x333d8d = {};
    if (g.getLang() == 0x1) {
        _0x34523d = 'en';
    }
    for (let _0xbe70fa = 0x0; _0xbe70fa < Object.keys(_0x415485).length; _0xbe70fa++) {
        var _0x22cd22 = Object.keys(_0x415485)[_0xbe70fa];
        try {
            _0x333d8d[_0x22cd22] = _0x415485[_0x22cd22].sx.t[0x0].replace(/\\/g, '');
        } catch (_0x2e7a98) {
            _0x333d8d[_0x22cd22] = _0x415485[_0x22cd22].sx.t[_0x34523d].replace(/\\/g, '');
        }
    }
    var _0x3c003a = '';
    for (let _0x2ae480 = 0x0; _0x2ae480 < Object.keys(_0x333d8d).length; _0x2ae480++) {
        var _0x22cd22 = Object.keys(_0x333d8d)[_0x2ae480];
        for (let _0x5c66dd = 0x0; _0x5c66dd < _0x333d8d[_0x22cd22].length; _0x5c66dd++) {
            _0x3c003a += findRealChar(_0x333d8d[_0x22cd22].substring(_0x5c66dd, _0x5c66dd + 0x1));
        }
        _0x46a2c2[_0x22cd22] = atob(_0x3c003a);
    }
    if (!_0x32dc3f.includes('#') && Object.keys(_0x46a2c2).length > 0x1) {
        Core.showAlternatesJS(JSON.stringify(_0x46a2c2));
    } else {
        url(_0x46a2c2[Object.keys(_0x46a2c2)[0x0]]);
        _0x253e5b = fetch();
        try {
            var _0x162524 = JSON.parse(_0x253e5b.match(/jwSetup\.tracks\s*=\s*(\[.*?\])/)[0x1]);
            for (let _0x29d265 = 0x0; _0x29d265 < _0x162524.length; _0x29d265++) {
                if (_0x162524[_0x29d265].hasOwnProperty('label') && _0x162524[_0x29d265].label.includes("Ã¼rkÃ§e")) {
                    sub(_0x162524[_0x29d265].file);
                }
            }
            sub(sub().replace('.vtt', '.srt'));
        } catch (_0x2fefdc) {}
        url(decryptFor4KIzle(_0x253e5b.match(/"file":\s*av\('(.*?)'\),/)[0x1]));
        parser();
    }
}

function govids() {
    var _0x1533f1 = url().split('?')[0x1].split('=');
    var _0x55a777 = _0x1533f1[0x1];
    var _0x1fa75a = _0x1533f1[0x2];
    var _0x150619 = _0x1533f1[0x3];
    var _0x3c6648 = 'i=' + _0x55a777 + '=' + _0x1fa75a + '=' + _0x150619;
    headers('Referer', url());
    headers("sec-ch-ua-platform", "\"Windows\"");
    headers("sec-ch-ua-mobile", '?0');
    url('/embed?', "/embed/get?");
    var _0x520d76 = fetchPost(_0x3c6648);
    try {
        var _0xef6123 = JSON.parse(_0x520d76);
        var _0x31df52 = _0xef6123.Links[0x0];
        _0x31df52 = _0x31df52.split('redirect')[0x1];
        var _0x319435 = "#.mp4";
        if (url(["setplay"], 0x1)) {
            _0x319435 = '';
        }
        url(baseUrl(url()) + '/redirect' + _0x31df52 + _0x319435);
    } catch (_0x3e7cac) {
        url('');
    }
    g.logHeader();
    parser();
}

function haberturk() {
    url(fetch().match(/videoUrl\s*=\s*"(.*?)"/)[0x1]);
    parser();
}

function halktv() {
    url(fetch().match(/videoUrl\s*=\s*"(.*?)"/)[0x1]);
    parser();
}

function hdabla() {
    var _0x34816d = fetch();
    var _0x19c40c = _0x34816d.match(/<iframe\s*src="(.*?)"/)[0x1];
    _0x19c40c = fixUrl(_0x19c40c);
    _0x34816d = fetch(_0x19c40c);
    url(_0x34816d.match(/file\s*:\s*'(.*?)'/)[0x1]);
    headers("Referer", "https://wai.moonfast.site/");
    parser();
}

function hdfilmce() {
    url(url().split('#')[0x0]);
    var _0x2b5364 = fetch();
    var _0x342cbe = _0x2b5364.match(/ilkpartkod\s*=\s*['\"](.*?)['\"]/)[0x1];
    var _0x13bfd5 = atob(_0x342cbe);
    _0x13bfd5 = _0x13bfd5.match(/src=['\"](.*?)['\"]/)[0x1];
    _0x2b5364 = fetch(_0x13bfd5);
    var _0x12a4ed = extractLink(_0x2b5364);
    url(_0x12a4ed);
    headers("Referer", _0x13bfd5);
    parser();
}

function hdfilmcehennemi() {
    var _0x552cbb = url();
    var _0x30d085 = fetch();
    var _0x19733e = '';
    try {
        if (g.getLang() == 0x0) {
            _0x19733e = _0x30d085.match(/videostr(.*?)<\/nav/)[0x1];
        } else {
            _0x19733e = _0x30d085.match(/videosen(.*?)<\/nav/)[0x1];
        }
    } catch (_0x53ea97) {
        _0x19733e = _0x30d085;
    }
    var _0x3fc054 = matchAll(_0x19733e, /nav-link\s*px-3\s*py-1.*?"\s*href="(.*?)"/g);
    var _0x1ea65a = {};
    for (let _0x506f2b = 0x0; _0x506f2b < _0x3fc054.length; _0x506f2b++) {
        _0x1ea65a["Kaynak " + (_0x506f2b + 0x1)] = _0x3fc054[_0x506f2b][0x1];
    }
    if (!_0x552cbb.includes('#') && Object.keys(_0x1ea65a).length > 0x1) {
        Core.showAlternatesJS(JSON.stringify(_0x1ea65a));
    } else {
        url(_0x552cbb.split('#')[0x1]);
        _0x30d085 = fetch();
        try {
            _0x30d085 = _0x30d085.match(/<script>var.*?'(.*?)'/)[0x1].match(/iframe.*?src\s*=\s*(?:"|\')(.*?)(?:"|\')/)[0x1].toLowerCase();
            _0x30d085 = fixUrl(_0x30d085);
            if (_0x30d085.includes("moly")) {
                if (_0x30d085.includes("watch.php")) {
                    url('https://vidmoly.to/embed-' + _0x30d085.split("watch.php")[0x1] + ".html");
                }
            } else {
                if (_0x30d085.includes('odnok') || _0x30d085.includes("ok.ru")) {
                    if (_0x30d085.includes("watch.php")) {
                        url('https://odnoklassniki.ru/videoembed/' + _0x30d085.split('watch.php')[0x1]);
                    }
                } else {
                    if (_0x30d085.includes('up')) {
                        if (_0x30d085.includes('watch.php')) {
                            url('https://uptostream.com/iframe/' + _0x30d085.split("watch.php")[0x1]);
                        }
                    } else {
                        if (_0x30d085.includes("fembed")) {
                            if (_0x30d085.includes('watch.php')) {
                                url("https://www.fembed.net/v/" + _0x30d085.split("watch.php")[0x1]);
                            }
                        }
                    }
                }
            }
        } catch (_0x18dd86) {
            url(_0x30d085.match(/<iframe.*?src\s*=\s*(?:"|\')(.*?)(?:"|\')/)[0x1]);
            url(fixUrl(url()));
            _0x30d085 = fetch(url());
            url(baseUrl(url()) + _0x30d085.match(/<source src="(.*?)" type="application\/x-mpegURL">/)[0x1]);
        }
        parser();
    }
}

function hdfilmcehennemi2() {
    url(url('syrtrk', ''));
    var _0x8833c1 = url();
    headers("User-Agent", "Cloudflare");
    try {
        var _0x2fa084 = fetch();
    } catch (_0x5e1bd4) {
        if (g.isWebView()) {
            Core.saveCookie(url(), "on_dz", "description");
            var _0x2fa084 = Core.pageContent.split("\n").join('');
        } else {
            error('');
        }
    }
    _0x2fa084 = _0x2fa084.match(/<nav\s*class="video-alternatives">(.*?)player-container/)[0x1];
    var _0xb5f03c = {};
    var _0x4f28a2 = '';
    try {
        var _0x223b71 = matchAll(_0x2fa084, /<div\s*class="alternative-links".*?data-lang="(.*?)">/g);
        var _0x39bf18 = _0x2fa084.split("class=\"alternative-links");
        for (let _0x631218 = 0x0; _0x631218 < _0x223b71.length; _0x631218++) {
            _0x2fa084 = _0x39bf18[_0x631218 + 0x1];
            var _0x3621a7 = matchAll(_0x2fa084, /data-video="(.*?)">(.*?)<\/button>/g);
            for (let _0x25f13a = 0x0; _0x25f13a < _0x3621a7.length; _0x25f13a++) {
                var _0x417d87 = _0x3621a7[_0x25f13a][0x2].replace(/ /g, '');
                var _0xe9ce96 = _0x3621a7[_0x25f13a][0x1];
                _0x4f28a2 = _0xe9ce96;
                if (_0x223b71[_0x631218][0x1] == "dual") {
                    _0x417d87 = _0x417d87 + " - AltyazÄ± & Dublaj";
                } else {
                    if (_0x223b71[_0x631218][0x1] == 'tr') {
                        _0x417d87 = _0x417d87 + " - Dublaj";
                    } else {
                        _0x417d87 = _0x417d87 + " - AltyazÄ±";
                    }
                }
                _0xb5f03c[_0x417d87] = _0xe9ce96;
            }
        }
    } catch (_0x3fb1b1) {
        error(_0x3fb1b1.message);
    }
    if (!_0x8833c1.includes('#') && JSON.stringify(_0xb5f03c) != '{}' && Object.keys(_0xb5f03c).length > 0x1) {
        Core.showAlternatesJS(JSON.stringify(_0xb5f03c));
    } else {
        if (_0x8833c1.includes('#')) {
            url(_0x8833c1.split('#')[0x1]);
        } else {
            url(_0x4f28a2);
        }
        headers("X-Requested-With", 'fetch');
        _0x2fa084 = fetch(baseUrl(_0x8833c1) + '/video/' + url() + '/');
        _0x2fa084 = _0x2fa084.match(/<iframe.*?data-src=\\"(.*?)\\"/)[0x1].replace(/\\\//g, '/');
        var _0x4ced7b = [];
        if (_0x2fa084.includes("player")) {
            _0x2fa084 = fetch(_0x2fa084);
            url('eval(' + _0x2fa084.match(/eval\((.*?)\{\}\)\)/)[0x1] + "{}))");
            _0x2fa084 = _0x2fa084.match(/tracks:\s*(.*?\]),/)[0x1];
            _0x4ced7b = [];
            try {
                var _0x3621a7 = matchAll(_0x2fa084, /"file":"(.*?)"/g);
                for (let _0xa3d3 = 0x0; _0xa3d3 < _0x3621a7.length; _0xa3d3++) {
                    var _0x176a15 = '';
                    if (_0x3621a7[_0xa3d3][0x1].includes('Turkish')) {
                        _0x176a15 = 'tr';
                    } else {
                        if (_0x3621a7[_0xa3d3][0x1].includes('English')) {
                            _0x176a15 = 'en';
                        }
                    }
                    if (_0x176a15 != '') {
                        var _0x403920 = _0x3621a7[_0xa3d3][0x1].replace(/\\\//g, '/') + '/';
                        var _0x2ddd61 = {
                            'lang': _0x176a15,
                            'url': baseUrl(_0x8833c1) + _0x403920
                        };
                        _0x4ced7b.push(_0x2ddd61);
                    }
                }
            } catch (_0x48e61a) {}
            _0x2fa084 = unPack(url()).replace("var file_link=\"", '').replace("\";", '');
            url(g.base64Decode(_0x2fa084));
            g.deleteHeader("X-Requested-With");
        } else {
            if (_0x2fa084.includes('video/embed')) {
                headers("Referer", _0x2fa084);
                _0x2fa084 = fetch(_0x2fa084);
                _0x4ced7b = [];
                try {
                    var _0x3621a7 = matchAll(_0x2fa084, /<track\s*src="(.*?\.vtt)".*?label="(.*?)"/g);
                    for (let _0x53255f = 0x0; _0x53255f < _0x3621a7.length; _0x53255f++) {
                        var _0x176a15 = '';
                        if (_0x3621a7[_0x53255f][0x2].includes("Turkish")) {
                            _0x176a15 = 'tr';
                        }
                        if (_0x176a15 != '') {
                            var _0x403920 = _0x3621a7[_0x53255f][0x1].replace(/\\\//g, '/');
                            var _0x2ddd61 = {
                                'lang': _0x176a15,
                                'url': baseUrl(headers.Referer) + _0x403920
                            };
                            _0x4ced7b.push(_0x2ddd61);
                        }
                    }
                } catch (_0xdd397a) {}
                url("eval(" + _0x2fa084.match(/eval\((.*?)\{\}\)\)/)[0x1] + "{}))");
                _0x2fa084 = unPack(url()).replace("var file_link=\"", '');
                url(_0x2fa084.match(/"(aHR0c.*?)"/)[0x1]);
                url(atob(url()));
            }
        }
        sub(JSON.stringify(_0x4ced7b));
        parser();
    }
}

function hdfilmcehennemi3() {
    var _0x585bd8 = url().split("?l=");
    url(_0x585bd8[0x0]);
    var _0x2bafc0 = 'en';
    if (g.getLang() == 0x0 || _0x585bd8[0x1] == '1') {
        _0x2bafc0 = 'tr';
    } else {
        if (g.getLang() == 0x2 || _0x585bd8[0x1] == '2') {
            _0x2bafc0 = "dual";
        }
    }
    headers('User-Agent', "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36");
    var _0x45b81e = matchAll(fetch(), /let\s*parts\s*=\s*(.*?);/g);
    url('');
    if (_0x45b81e.length > 0x0) {
        var _0x189a12 = JSON.parse(_0x45b81e[0x0][0x1]);
        for (var _0xa03880 = 0x0; _0xa03880 < _0x189a12.length; _0xa03880++) {
            if (_0x189a12[_0xa03880].lang == _0x2bafc0) {
                url(_0x189a12[_0xa03880].data.match(/iframe\s*src="(.*?)"/)[0x1]);
                break;
            }
        }
    } else {
        url(_0x45b81e.match(/<iframe\s*src="(.*?)"/)[0x1]);
    }
    parser();
}

function hdtoday() {
    if (!g.isWebView()) {
        error("No Webview");
    }
    var _0x18a6e1 = url().split('#')[0x0];
    headers("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36");
    var _0x3053ff = '';
    if (_0x18a6e1.includes("/movie/")) {
        _0x18a6e1 = _0x18a6e1.replace('/movie/', "/watch-movie/");
    } else {
        if (_0x18a6e1.includes("/tv/")) {
            _0x18a6e1 = _0x18a6e1.replace("/tv/", "/watch-tv/").replace("-full-", "-hd-").replace(".se", '.tv');
            _0x3053ff = _0x18a6e1.split('.')[_0x18a6e1.split('.').length - 0x1];
            _0x3053ff = _0x3053ff.split('/')[0x0];
            var _0x4582ac = fetch(baseUrl(_0x18a6e1) + "/ajax/episode/servers/" + _0x3053ff);
            _0x18a6e1 = _0x18a6e1.replace(_0x3053ff, _0x4582ac.match(/<a data-id="(.*?)"/)[0x1]).split("/sezon")[0x0];
        }
    }
    if (!url().includes('#')) {
        getWebViewOwnContentJS(_0x18a6e1, "==.m3u8", "embed", "jw-icon jw-icon-display jw-button-color jw-reset", '', 0x0, false, g.getHeadersJSON(), 0x2);
    } else {
        var _0x4247a1 = url().split('#')[0x2];
        consolelog('TEst123');
        url(url().split('#')[0x1]);
        if (_0x4247a1.includes("http")) {
            headers("x-requested-with", 'XMLHttpRequest');
            var _0x38069f = _0x4247a1.split('/')[_0x4247a1.split('/').length - 0x1];
            _0x38069f = _0x38069f.split('?')[0x1].split('&')[0x0].replace("id=", '');
            headers('Referer', 'https://hdtodayz.to');
            var _0xf6bfbd = fetch("https://videostr.net/embed-1/v3/e-1/" + _0x38069f + "?z=");
            if (_0xf6bfbd.includes("_is_th")) {
                _0xf6bfbd = _0xf6bfbd.match(/_is_th:(.*?)/)[0x1];
            } else {
                if (_0xf6bfbd.includes("_xy_ws")) {
                    _0xf6bfbd = _0xf6bfbd.match(/window._xy_ws\s*=\s*"(.*?)";/)[0x1];
                } else {
                    if (_0xf6bfbd.includes('_gg_fb')) {
                        _0xf6bfbd = _0xf6bfbd.match(/name="_gg_fb"\s*content="(.*?)"/)[0x1];
                    } else {
                        if (_0xf6bfbd.includes('_lk_db')) {
                            var _0x50615e = _0xf6bfbd.match(/{x:\s*"(.*?)",\s*y:\s*".*?",\s*z:\s*".*?"};/)[0x1];
                            var _0x1fbce7 = _0xf6bfbd.match(/{x:\s*".*?",\s*y:\s*"(.*?)",\s*z:\s*".*?"};/)[0x1];
                            var _0x307788 = _0xf6bfbd.match(/{x:\s*".*?",\s*y:\s*".*?",\s*z:\s*"(.*?)"};/)[0x1];
                            _0xf6bfbd = _0x50615e + _0x1fbce7 + _0x307788;
                        } else {
                            if (_0xf6bfbd.includes("nonce")) {
                                _0xf6bfbd = _0xf6bfbd.match(/nonce="(.*?)"/)[0x1];
                            } else {
                                if (_0xf6bfbd.includes("data-dpi")) {
                                    _0xf6bfbd = _0xf6bfbd.match(/<data-dpi="(.*?)"/)[0x1];
                                }
                            }
                        }
                    }
                }
            }
            _0x4247a1 = _0x4247a1.split('k=')[0x0] + 'k=' + _0xf6bfbd;
            headers("Referer", baseUrl(_0x4247a1) + '/');
            _0xf6bfbd = fetch(_0x4247a1);
            var _0x47de34 = [];
            try {
                var _0x48e6f9 = JSON.parse(_0xf6bfbd);
                var _0x4ef611 = _0x48e6f9.tracks;
                for (var _0x239da3 = 0x0; _0x239da3 < _0x4ef611.length; _0x239da3++) {
                    var _0x4c1f23 = _0x4ef611[_0x239da3];
                    if (_0x4c1f23.hasOwnProperty('label') && _0x4c1f23.hasOwnProperty('file')) {
                        if (_0x4c1f23.label.includes('English') || _0x4c1f23.label.includes('German') || _0x4c1f23.label.includes("Turkish")) {
                            var _0x28e8fc = "Eng";
                            if (_0x4c1f23.label.includes("German")) {
                                _0x28e8fc = 'Ger';
                            } else {
                                if (_0x4c1f23.label.includes("Turkish")) {
                                    _0x28e8fc = "Tur";
                                }
                            }
                            var _0x1fc55e = {
                                'lang': _0x28e8fc,
                                'url': _0x4c1f23.file
                            };
                            _0x47de34.push(_0x1fc55e);
                        }
                    }
                }
            } catch (_0x2a20ee) {}
            var _0x11c57a = '';
            var _0x3401e3 = '';
            var _0x15cffb = '';
            for (var _0x239da3 = 0x0; _0x239da3 < _0x47de34.length; _0x239da3++) {
                if (_0x47de34[_0x239da3].lang == "Tur") {
                    _0x11c57a = _0x47de34[_0x239da3].url;
                } else {
                    if (_0x47de34[_0x239da3].lang == "Eng") {
                        _0x3401e3 = _0x47de34[_0x239da3].url;
                    } else {
                        if (_0x47de34[_0x239da3].lang == "Ger") {
                            _0x15cffb = _0x47de34[_0x239da3].url;
                        }
                    }
                }
            }
            var _0x117846 = [];
            if (_0x11c57a == '') {
                var _0x31890b = '';
                if (_0x3401e3 != '') {
                    _0x31890b = _0x3401e3;
                } else {
                    if (_0x15cffb != '') {
                        _0x31890b = _0x15cffb;
                    }
                }
                if (_0x31890b != '') {
                    headers("forHelper", 'c2V5L3RyYW5zbGF0ZS8');
                    headers("forHelper2", 'Q2V2aXJpQUkuVFIucGhwP3VybD0');
                    var _0x241224 = 'm_';
                    if (_0x3053ff != '') {
                        _0x241224 = 't_';
                    }
                    sub(subHelp(_0x31890b, _0x241224 + 'hd'));
                    if (_0x3401e3 != '') {
                        var _0x4247a1 = {};
                        _0x4247a1.lang = 'en';
                        _0x4247a1.url = _0x3401e3;
                        _0x117846 = JSON.parse(sub());
                        _0x117846.push(_0x4247a1);
                        sub(JSON.stringify(_0x117846));
                    }
                }
            } else {
                sub(_0x11c57a);
            }
            parser();
        }
    }
}

function imdb() {
    url(url() + '/');
    var _0x3b8c21 = fetch().match(/"embedUrl"\s*:\s*"(.*?)"/)[0x1];
    var _0x5031a7 = _0x3b8c21.replace('video/imdb', 'videoembed');
    if (!_0x5031a7.startsWith('https')) {
        _0x5031a7 = "https://imdb.com" + _0x5031a7;
    }
    var _0x5ea813 = fetch(_0x5031a7);
    try {
        var _0xccff39 = matchAll(_0x5ea813, /"videoUrl":"(.*?)"},{"definition":"(.*?)"/);
        if (_0xccff39.length > 0x0) {
            for (var _0x13809f = 0x0; _0x13809f < _0xccff39.length; _0x13809f++) {}
        } else {
            throw Error();
        }
    } catch (_0x5244f2) {
        var _0x13d253 = JSON.parse(_0x5ea813.match(/<script id="__NEXT_DATA__" type="application\/json">(.*?)<\/script>/)[0x1]);
        url(_0x13d253.props.pageProps.videoPlaybackData.video.playbackURLs[0x0].url);
    }
    parser();
}

function istanbuluseyret() {
    var _0x15ccf4 = fetch();
    _0x15ccf4 = _0x15ccf4.match(/"dataProvider":(.*?\}),/)[0x1];
    var _0x4920e7 = JSON.parse(_0x15ccf4);
    url(_0x4920e7.source[0x0].url);
    parser();
}

function sinefil() {
    var _0x8eb3ec = fetch();
    _0x8eb3ec = _0x8eb3ec.match(/secureData\":\"(.*?)\"/)[0x1];
    var _0x5c7be6 = _0x8eb3ec;
    _0x8eb3ec = atob(_0x8eb3ec);
    var _0x578ae8 = _0x8eb3ec;
    try {
        if (!_0x8eb3ec.includes('pichive')) {
            consolelog(_0x5c7be6);
            _0x8eb3ec = getSecureData(_0x5c7be6);
        }
        _0x8eb3ec = JSON.parse(_0x8eb3ec);
        _0x8eb3ec = _0x8eb3ec.RelatedResults.getEpisodeSources.result;
        for (var _0x5cbe46 = 0x0; _0x5cbe46 < _0x8eb3ec.length; _0x5cbe46++) {
            if ((g.getLang() >= 0x1 && url(["yabancidizi"], 0x1) || url(["selcukflix"], 0x1)) && _0x8eb3ec[_0x5cbe46].language_name.includes("Altyaz") || g.getLang() == 0x0 && _0x8eb3ec[_0x5cbe46].language_name.includes('Dublaj')) {
                if (_0x8eb3ec[_0x5cbe46].source_content.includes('pichive') || !_0x8eb3ec[_0x5cbe46].source_content.includes("pichive")) {
                    url(_0x8eb3ec[_0x5cbe46].source_content.match(/src="(.*?)"/)[0x1]);
                    break;
                }
            }
        }
    } catch (_0xdc2d7f) {
        url(_0x578ae8.match(/src=\\"(.*?)\\"/)[0x1]);
    }
    url(fixUrl(url()));
    parser();
}

function jetfilm() {
    var _0x55eb74 = url();
    headers("User-Agent", "cloudflare");
    var _0x5ae2fb = fetch().match(/film_part(.*?)(?:pbgiris|iframe)/)[0x1];
    consolelog(_0x5ae2fb);
    var _0x2d9af3 = matchAll(_0x5ae2fb, /<span>(.*?)<\/span>/g);
    var _0xe4c84c = matchAll(_0x5ae2fb, /href="(.*?)"/g);
    var _0x1a3e4c = {};
    var _0x39b76d = ["vip", "vupload", 'letsupload', "jetplay", "mail", "aparat", "vidmoly", "mixplay", "jetv.xyz", "platin", 'moly', "okru", 'vk', 'jet', 'seg', 'one', "tr-en", 'yx', "trp", "dood", 'fmoon'];
    _0xe4c84c.unshift(['', url()]);
    for (let _0x1f5d1f = 0x0; _0x1f5d1f < _0x2d9af3.length; _0x1f5d1f++) {
        if (_0x39b76d.indexOf((_0x2d9af3[_0x1f5d1f][0x1] + '').toLowerCase()) !== -0x1) {
            _0x1a3e4c[_0x2d9af3[_0x1f5d1f][0x1]] = _0xe4c84c[_0x1f5d1f][0x1];
        }
    }
    if (!_0x55eb74.includes('#') && Object.keys(_0x1a3e4c).length > 0x1) {
        Core.showAlternatesJS(JSON.stringify(_0x1a3e4c));
    } else {
        url(url().split('#')[0x1]);
        _0x5ae2fb = fetch();
        try {
            url(_0x5ae2fb.match(/<iframe.*?data(?:-litespeed|)-src=["|'](.*?)['|"]\s*(?:width|frame|)/)[0x1]);
        } catch (_0x3fddd7) {
            try {
                url(_0x5ae2fb.match(/<iframe.*?data-src="(.*?)"/)[0x1]);
            } catch (_0x556b4f) {
                try {
                    url(_0x5ae2fb.match(/iframe src='(.*?)'/)[0x1]);
                } catch (_0x484130) {
                    url(_0x5ae2fb.match(/class="film_partiframe src='(.*?)'/)[0x1]);
                }
            }
        }
        if (!url(["mixdrop", "videobin", 'upstream', "vidmoly", "ok.ru", "odnoklassniki", "vk.com", "dood", "trstx"], 0x1)) {
            if (url(["jetv.xyz/yx"], 0x1)) {
                var _0x354a26 = "vars=" + url().match(/id=(.*?)$/)[0x1];
                _0x5ae2fb = fetchPost(_0x354a26, "https://jetv.xyz/yx/api.php");
                url(_0x5ae2fb.match(/file:.*?"(.*?)",/)[0x1]);
            } else {
                if (url(["jfvid"], 0x1)) {
                    url("/play/", "/stream/");
                } else {
                    _0x5ae2fb = fetch();
                    if (url(["jtfi"], 0x1)) {
                        try {
                            url(_0x5ae2fb.match(/"hls","file":"(.*?)"/)[0x1].replace(/\\/g, ''));
                        } catch (_0x2cd472) {
                            _0x5ae2fb = matchAll(_0x5ae2fb, /"file":"(.*?)"/g);
                            url(_0x5ae2fb[_0x5ae2fb.length - 0x1][0x1].replace(/\\/g, '') + "#.mp4");
                        }
                        headers('Referer', url());
                        headers('Range', "bytes=0-");
                    } else {
                        if (url(["oneupload", "segavid"], 0x1)) {
                            url(fetch().match(/file:"(.*?)"/)[0x1]);
                        } else {
                            if (url(['jetv.xyz'], 0x1)) {
                                if (_0x5ae2fb.includes("jetESources")) {
                                    var _0x3e3bd3 = {
                                        iv: "987654jetfilmcom",
                                        s: "987654321jetfilm",
                                        ct: _0x5ae2fb.match(/jetESources\s*=\s*"(.*?)";/)[0x1]
                                    };
                                    url(getAes('', JSON.stringify(_0x3e3bd3)));
                                } else {
                                    if (_0x5ae2fb.includes("Contents =")) {
                                        url(url());
                                    } else {
                                        if (_0x5ae2fb.includes("\"label\":")) {
                                            consolelog("label");
                                        } else {
                                            if (_0x5ae2fb.includes("m3u8")) {
                                                consolelog("m3u8");
                                            } else {
                                                if (_0x5ae2fb.includes('src=')) {
                                                    consolelog("src=");
                                                } else {
                                                    consolelog("other");
                                                }
                                            }
                                        }
                                    }
                                }
                            } else {
                                _0x5ae2fb = _0x5ae2fb.match(/"?file"? ?: ?"([^"]+)", ?"(?:type|label)": ?"([^"]+)"/);
                            }
                        }
                    }
                }
            }
        }
        consolelog("Test: " + url());
        url(fixUrl(url()));
        parser();
    }
}

function kanal7() {
    if (url(['canli-izle'], 0x1)) {
        url(fetch().match(/hls:\s*'(.*?)'/)[0x1]);
    } else {
        var _0x54a902 = fetch().match(/<iframe.*?src="(https:\/\/www.izle7.com\/.*?)"/)[0x1];
        _0x54a902 = fetch(_0x54a902).match(/play_video\s*=\s*"(.*?)"/)[0x1];
        url('https://www.dailymotion.com/embed/video/' + _0x54a902);
    }
    parser();
}

function kanalb() {
    url("https://baskentaudiovideo.xyz/LiveApp/streams/" + fetch().match(/\?name=(.*?)"/)[0x1] + ".m3u8");
    parser(url(), 0x1, '', '', false);
}

function kanald() {
    if (url(['canli-yayin'], 0x0)) {
        var _0x568ce1 = fetch();
        url(_0x568ce1.match(/data-url="(.*?)"/)[0x1].replace("https://media.duhnet.tv", ''));
        parser();
    } else {
        var _0x568ce1 = fetch();
        _0x568ce1 = _0x568ce1.match(/"contentUrl":"(.*?)"/)[0x1];
        url(_0x568ce1);
        parser();
    }
}

function koreanturk() {
    var _0xdf3c2f = url();
    var _0x421832 = fetch();
    _0x421832 = matchAll(_0x421832.match(/tab-content icerikler(.*?)text\/css/)[0x1], /id="(.*?)".*?(?:iframe.*?src|a.*?href)="(.*?)"/g);
    streamUrls = {};
    for (let _0x2b1f7f = 0x0; _0x2b1f7f < _0x421832.length; _0x2b1f7f++) {
        if (!_0x421832[_0x2b1f7f][0x1].includes("guard") && !_0x421832[_0x2b1f7f][0x1].includes("mega")) {
            streamUrls[_0x421832[_0x2b1f7f][0x1]] = _0x421832[_0x2b1f7f][0x2];
        }
    }
    if (!_0xdf3c2f.includes('#')) {
        Core.showAlternatesJS(JSON.stringify(streamUrls));
    } else {
        url(url().split('#')[0x1]);
        parser();
    }
}

function kultfilmler() {
    var _0x55abef = url();
    var _0x1ba771 = fetch();
    _0x1ba771 = _0x1ba771.match(/player-control(.*?)button\s*report-button\s*trigger/)[0x1];
    var _0x155769 = {};
    try {
        var _0x284e8c = matchAll(_0x1ba771, /part-name">(.*?)<.*?"part-lang">(.*?)<\/div/g);
        var _0x13dc15 = 0x0;
        for (let _0x482df4 = 0x0; _0x482df4 < _0x284e8c.length; _0x482df4++) {
            var _0x4dfb6f = url();
            if (_0x13dc15 > 0x0) {
                _0x4dfb6f = url() + (_0x13dc15 + 0x1) + '/';
            }
            var _0x4aa30b = 'cc';
            if (g.getLang() == 0x1) {
                _0x4aa30b = 'tr';
            }
            if (_0x284e8c[_0x482df4][0x2].includes(_0x4aa30b) || _0x4aa30b != 0x1 && _0x284e8c[_0x482df4][0x2].length < 0x2) {
                if (!_0x284e8c[_0x482df4][0x1].includes('KULTPlayer')) {
                    _0x155769[_0x284e8c[_0x482df4][0x1]] = _0x4dfb6f;
                }
            }
            _0x13dc15++;
        }
    } catch (_0x178cfe) {
        error(_0x178cfe.message);
    }
    if (!_0x55abef.includes('#') && _0x155769.length > 0x0) {
        Core.showAlternatesJS(JSON.stringify(_0x155769));
    } else {
        if (_0x55abef.includes('#')) {
            url(_0x55abef.split('#')[0x1]);
        } else {
            url(_0x55abef);
        }
        _0x1ba771 = fetch();
        url(_0x1ba771.match(/new ContentManager\(.*?, "(.*?)", 15\);/)[0x1]);
        url(atob(url()));
        url(url().match(/iframe.*?src="(.*?)"/)[0x1]);
        url(fixUrl(url()));
        if (url(["yildizkisafilm"], 0x0)) {
            var _0x9a31b9 = url().split('/')[url().split('/').length - 0x1];
            url('https://yildizkisafilm.org/player/index.php?data=' + _0x9a31b9 + "&do=getVideo");
            var _0x1240c9 = "hash=" + _0x9a31b9 + '&r=';
            headers('X-Requested-With', "XMLHttpRequest");
            try {
                _0x1ba771 = fetch();
                sub(_0x1ba771.match(/var playerjsSubtitle = "\[TÃ¼rkÃ§e\](.*?\.srt)";/)[0x1]);
            } catch (_0x59232d) {
                sub('');
            }
            g.logHeader();
            var _0x4aec55 = fetchPost(_0x1240c9);
            try {
                _0x1240c9 = JSON.parse(_0x4aec55);
                url(_0x1240c9.securedLink);
                parser();
            } catch (_0x45a76b) {
                error(_0x45a76b.message);
            }
        } else {
            parser();
        }
    }
}

function mailru() {
    url(fixUrl(url()));
    var _0x9db150 = matchAll(fetch(), /"video":(.*?),/g);
    var _0x1e0eda = '';
    for (let _0x3a1147 = 0x0; _0x3a1147 < _0x9db150.length; _0x3a1147++) {
        _0x1e0eda = 'https://my.mail.ru' + _0x9db150[_0x3a1147][0x1].split("\"").join('').split('{').join('').split(':').join('').split('metadataUrl').join('').split(" ").join('');
    }
    var _0x3f749e = JSON.parse(fetch(_0x1e0eda)).videos;
    var _0x36fefc = ["360p", "480p", '720p', "1080p", 'Alone'];
    var _0x5c2d4d = -0x1;
    var _0x3be0ad = -0x1;
    for (let _0x4c1663 = 0x0; _0x4c1663 < _0x3f749e.length; _0x4c1663++) {
        try {
            var _0xb1a215 = _0x36fefc.indexOf(_0x3f749e[_0x4c1663].key);
            if (_0x5c2d4d < _0xb1a215) {
                _0x5c2d4d = _0xb1a215;
                _0x3be0ad = _0x4c1663;
            }
        } catch (_0x597785) {}
    }
    if (_0x5c2d4d != -0x1) {
        url(fixUrl(_0x3f749e[_0x3be0ad].url));
    }
    parser();
}

function mixdrop() {
    url(fixUrl(url()));
    var _0x430947 = fetch();
    _0x430947 = unPack(_0x430947.match(/(eval\(function\(p,a,c,k,e,d.*?)<\/script>/)[0x1]);
    var _0x5a0117 = /MDCore.wurl="(.*?)"/;
    if (url(["luluvdo"], 0x1)) {
        _0x5a0117 = /file:"(.*?)"/;
    } else {
        if (url(["streamhub"], 0x1)) {
            _0x5a0117 = /src:"(.*?)"/;
        }
    }
    url(fixUrl(_0x430947.match(_0x5a0117)[0x1]));
    parser();
}

function movies123() {
    if (!g.isWebView()) {
        error("No Webview");
    }
    var _0x38c774 = url().split('#')[0x0];
    headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36";
    var _0x24edff = -0x1;
    getWebViewOwnContentJS(_0x38c774, "site/hls", "I AM NOT LOOKING", 'play-now', '', _0x24edff, false, g.getHeadersJSON, 0x0);
}

function movie4k() {
    var _0x2279ca = url();
    var _0x242fc9 = fetch();
    var _0x54e49e = {};
    try {
        var _0x4861b9 = matchAll(_0x242fc9, /class="tablinks"\s*href="#"\s*data-link="(.*?)">(.*?)</g);
        var _0x10ad32 = 0x1;
        for (let _0xa08266 = 0x0; _0xa08266 < _0x4861b9.length; _0xa08266++) {
            if (!_0x4861b9[_0xa08266][0x2].includes("Player HD") && !_0x4861b9[_0xa08266][0x2].includes("Trailer") && !_0x4861b9[_0xa08266][0x2].includes("Server 4K") && !_0x4861b9[_0xa08266][0x2].includes("Goodstream")) {
                _0x54e49e[_0x4861b9[_0xa08266][0x2]] = _0x4861b9[_0xa08266][0x1];
                _0x10ad32++;
            }
        }
    } catch (_0x5dd8bc) {
        error(_0x5dd8bc.message);
    }
    if (!_0x2279ca.includes('#') && JSON.stringify(_0x54e49e) != '{}') {
        Core.showAlternatesJS(JSON.stringify(_0x54e49e));
    } else {
        url(_0x2279ca.split('#')[0x1]);
        url(fixUrl(url()));
        if (url(["goodstream"], 0x1)) {} else {
            parser();
        }
    }
}

function nowtv() {
    if (url(["canli-yayin"], 0x0)) {
        var _0xd7b817 = fetch();
        var _0x14516d = /(?:videoSrc|daiUrl)\s*:\s*'(.*?)'/;
        url(_0xd7b817.match(_0x14516d)[0x1]);
        parser();
    } else {
        var _0xd7b817 = fetch();
        url(_0xd7b817.match(/'(https:\/\/nowtv-.*?)'/)[0x1]);
        parser();
    }
}

function myvideoaz() {
    url(fetch().match(/application\/x-mpegURL"\s*src="(.*?)"/)[0x1]);
    parser();
}

function okru() {
    url(fixUrl(url()));
    headers('User-Agent', "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0");
    var _0x8e7f90 = url().match(/https?:\/\/(?:www.)?(?:odnoklassniki|ok).ru\/(?:videoembed\/|dk\?cmd=videoPlayerMetadata&mid=)(\d+)/)[0x1];
    var _0x52a23e = JSON.parse(fetchPost("cmd=videoPlayerMetadata&mid=" + _0x8e7f90, "http://www.ok.ru/dk"));
    _0x52a23e = _0x52a23e.videos;
    var _0xf9d021 = ["mobile", "lowest", "low", 'sd', 'hd', "full"];
    var _0xb0485c = -0x1;
    var _0x8dd5a5 = -0x1;
    for (let _0xb66e2 = 0x0; _0xb66e2 < _0x52a23e.length; _0xb66e2++) {
        try {
            var _0x42f453 = _0xf9d021.indexOf(_0x52a23e[_0xb66e2].name);
            if (_0xb0485c < _0x42f453) {
                _0xb0485c = _0x42f453;
                _0x8dd5a5 = _0xb66e2;
            }
        } catch (_0x31db40) {}
    }
    if (_0xb0485c != -0x1) {
        url(_0x52a23e[_0x8dd5a5].url + "#.mp4");
        headers("Referer", "https://odnoklassniki.ru/");
    }
    parser();
}

function oneupload() {
    var _0x13e268 = fetch();
    url(_0x13e268.match(/\[\{file:"(.*?)"/)[0x1]);
    parser();
}

function onlinedizi() {
    var _0xd123bc = url();
    var _0x16319e = "episode-buttons";
    if (url(["/film/"], 0x1)) {
        _0x16319e = 'active';
        if (!url(["izle"], 0x1)) {
            url(url() + '/turkce-altyazi-izle');
        }
    }
    headers("User-Agent", "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36");
    var _0x78755 = fetch();
    try {
        _0x78755 = _0x78755.match(/Alternatif(.*?)episode-buttons/)[0x1];
    } catch (_0x1ea145) {}
    var _0x4c89a2 = {};
    try {
        var _0x3b6403 = matchAll(_0x78755, /href="(.*?)".*?>(.*?)</g);
        for (let _0x1c23f9 = 0x0; _0x1c23f9 < _0x3b6403.length; _0x1c23f9++) {
            var _0x4bbe7e = _0x3b6403[_0x1c23f9][0x1];
            var _0x16a5e2 = _0x3b6403[_0x1c23f9][0x2];
            _0x4c89a2[_0x16a5e2] = _0x4bbe7e;
        }
    } catch (_0x32b6c0) {
        error(_0x32b6c0.message);
    }
    if (Object.keys(_0x4c89a2).length == 0x0 || Object.keys(_0x4c89a2).length > 0x8) {
        error("Onlinedizi 1371");
    }
    if (!_0xd123bc.includes('#') && JSON.stringify(_0x4c89a2) != '{}') {
        Core.showAlternatesJS(JSON.stringify(_0x4c89a2));
    } else {
        url(_0xd123bc.split('#')[0x1]);
        _0x78755 = fetch();
        url(_0x78755.match(/iframe\s*src="(.*?)"/)[0x1]);
        if (!url().startsWith("http")) {
            url(baseUrl(_0xd123bc) + url());
        }
        _0x78755 = fetch();
        var _0x538259 = _0x78755.match(/ifsrc = "(.*?)"/)[0x1];
        if (!_0x538259.startsWith("http")) {
            _0x538259 = baseUrl(url()) + _0x538259;
        }
        url(Core.getRedirectUrlJS(_0x538259));
        if (url() == '') {
            error("Onlinedizi 1393");
        } else {
            if (url(["gdplayer"], 0x1)) {
                _0x78755 = fetch();
                url('https:' + _0x78755.match(/(\/\/gdplayer.org\/api\/.*?)"/)[0x1]);
                _0x78755 = fetch();
                try {
                    var _0x20c2fd = JSON.parse(_0x78755);
                    url(_0x20c2fd.sources[0x0].file);
                } catch (_0x452e95) {
                    error(_0x452e95.message);
                }
            } else {
                if (url(["fscdn.xyz"], 0x1)) {
                    var _0xbb60c9 = url().split('/')[0x4];
                    var _0x412701 = url() + '?do=getVideo';
                    var _0x5dd2b2 = "hash=" + _0xbb60c9 + '&r=' + baseUrl(_0xd123bc) + '&s=';
                    url(_0x412701);
                    headers("content-type", "application/x-www-form-urlencoded; charset=UTF-8");
                    headers("x-requested-with", 'XMLHttpRequest');
                    _0x78755 = fetchPost(_0x5dd2b2);
                    try {
                        var _0x20c2fd = JSON.parse(_0x78755);
                        _0x412701 = _0x20c2fd.videoSources[0x0].file;
                        url(_0x412701);
                        if (_0x412701.includes("fcdn")) {
                            _0x78755 = fetch();
                            url('');
                            try {
                                var _0x3b6403 = matchAll(_0x78755, /sticon-film"><\/span><b>(.*?)</g);
                                for (let _0x3d2195 = 0x0; _0x3d2195 < alts_raw.length; _0x3d2195++) {
                                    if (url() == '') {
                                        url(_0x3b6403[_0x3d2195][0x1]);
                                    } else {
                                        if (_0x3b6403[_0x3d2195][0x1].includes("1080p/playlist")) {
                                            url(_0x3b6403[_0x3d2195][0x1]);
                                        } else {
                                            if (_0x3b6403[_0x3d2195][0x1].includes("720p/playlist") && !url.includes("1080p/playlist")) {
                                                url(_0x3b6403[_0x3d2195][0x1]);
                                            } else {
                                                if (_0x3b6403[_0x3d2195][0x1].includes("480p/playlist") && !url.includes("1080p/playlist") && !url.includes("720p/playlist")) {
                                                    url(_0x3b6403[_0x3d2195][0x1]);
                                                } else if (_0x3b6403[_0x3d2195][0x1].includes("360p/playlist") && !url.includes("1080p/playlist") && !url.includes("720p/playlist") && !url.includes('480p/playlist')) {
                                                    url(_0x3b6403[_0x3d2195][0x1]);
                                                }
                                            }
                                        }
                                    }
                                }
                            } catch (_0x2f2b93) {}
                        }
                        g.deleteHeader("content-type");
                        g.deleteHeader("x-requested-with");
                        headers('Referer', "https://yandex.ru");
                    } catch (_0x440464) {
                        error(_0x440464.message);
                    }
                } else if (url(['ondembed.xyz'], 0x1)) {
                    url("ondembed.xyz", "fembed.com");
                }
            }
        }
        parser();
    }
}

function onlineradiobox() {
    url(fetch().match(/stream="(.*?)"/)[0x1]);
    g.setMediaType('mp3');
    parser();
}

function parsatv() {
    var _0x2ee723 = fetch();
    try {
        url(_0x2ee723.match(/file:\s*"(.*?)"/)[0x1]);
    } catch (_0x50368c) {
        url(_0x2ee723.match(/<iframe.*src="(.*embed.*)"/)[0x1]);
    }
    if (url(["youtube"], 0x1)) {
        url(url().match(/youtube-nocookie.com\/embed\/(.*?)\?/)[0x1]);
        url("https://m.youtube.com/watch?v=" + url());
    }
    parser();
}

function pokitv() {
    var _0x1eeb87 = url();
    var _0x127731 = fetch();
    url(_0x127731.match(/<iframe.*?data-litespeed-src="(.*?)"/)[0x1]);
    var _0x5f277e = url().split('/')[0x5];
    headers("X-Requested-With", 'XMLHttpRequest');
    headers("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    _0x127731 = fetchPost('hash=' + _0x5f277e + "&r=" + _0x1eeb87 + '&s=', url() + "?do=getVideo");
    var _0x340a43 = JSON.parse(_0x127731);
    if (_0x340a43.hasOwnProperty('videoSources')) {
        url(_0x340a43.videoSources[0x0].file);
    } else {
        url(_0x340a43.videoSrc);
        _0x127731 = fetch();
        url(_0x127731.match(/source.*?src=\"(.*?)\"/)[0x1]);
    }
    parser();
}

function pornhub() {
    var _0x4adf3b = matchAll(fetch(), /var flashvars_.*?=\s*(\{.*?});/g);
    var _0x46a7ad = {};
    for (let _0x39e710 = 0x0; _0x39e710 < _0x4adf3b.length; _0x39e710++) {
        try {
            var _0xfd6000 = JSON.parse(_0x4adf3b[_0x39e710][0x1]);
            var _0x29ff55 = _0xfd6000.defaultQuality;
            for (let _0x278c61 = 0x0; _0x278c61 < _0x29ff55.length; _0x278c61++) {
                var _0x54a739 = _0xfd6000.mediaDefinitions;
                for (let _0xd8b434 = 0x0; _0xd8b434 < _0x54a739.length; _0xd8b434++) {
                    if (_0x29ff55[_0x278c61] == _0x54a739[_0xd8b434].quality) {
                        _0x46a7ad[_0x29ff55[_0x278c61]] = _0x54a739[_0xd8b434].videoUrl;
                    }
                }
            }
        } catch (_0x5743aa) {}
    }
    var _0x1421bf = ['240', '360', '480', "720", '1080', "Alone"];
    var _0x2d8c23 = -0x1;
    var _0x48f1bd = -0x1;
    for (let _0x2d14f6 = 0x0; _0x2d14f6 < Object.keys(_0x46a7ad).length; _0x2d14f6++) {
        try {
            var _0x5818cc = Object.keys(_0x46a7ad)[_0x2d14f6];
            var _0x17507d = _0x1421bf.indexOf(_0x5818cc);
            if (_0x2d8c23 < _0x17507d) {
                _0x2d8c23 = _0x17507d;
                _0x48f1bd = _0x5818cc;
            }
        } catch (_0x3ae8f9) {}
    }
    if (_0x2d8c23 != -0x1) {
        url(fixUrl(_0x46a7ad[_0x48f1bd].replace(/\\/g, '')));
    }
    parser();
}

function pornpics() {
    var _0x5a46e2 = fetch();
    var _0x581a52 = _0x5a46e2.match(/var\s*P_LINK\s*=\s*\'\w{2,6}\/(.*?)\'/)[0x1];
    _0x581a52 = atob(_0x581a52);
    url(_0x581a52);
    parser();
}

function puhutv() {
    url(fixUrl(url()));
    var _0x528059 = fetch().match(/movieAssets".*?"video_id":"(PUHU_.*?)"/)[0x1];
    url('https://dygvideo.dygdigital.com/api/video_info?akamai=true&PublisherId=29&ReferenceId=' + _0x528059 + "&SecretKey=NtvApiSecret2014");
    _0x528059 = fetch();
    var _0x45c301 = JSON.parse(_0x528059);
    try {
        url(_0x45c301.data.flavors['0'].file_url_1);
    } catch (_0x452fd9) {
        url(_0x45c301.data.flavors.hls);
    }
    parser();
}

function radyodelisi() {
    var _0x16f1bd = fetch();
    url(_0x16f1bd.match(/source src=\"(.*?)\"/)[0x1]);
    parser();
}

function radyohome() {
    var _0x29c80d = matchAll(fetch(), /"hls","url":"(.*?)"/g);
    consolelog(_0x29c80d.length, "Test");
    url(_0x29c80d[_0x29c80d.length - 0x1][0x1].replace(/\\/g, ''));
    parser();
}

function realfilmizle() {
    var _0x48f41d = fetch().toLowerCase();
    var _0x177c3c = _0x48f41d.match(/iframe.*?src="(https.*?)"/)[0x1];
    g.deleteHeader("Referer");
    _0x48f41d = fetch(_0x177c3c);
    var _0x58161c = _0x48f41d.match(/bePlayer\('(.*?)',\s*'(.*?)'\);/)[0x1];
    var _0x3eb0f3 = _0x48f41d.match(/bePlayer\('(.*?)',\s*'(.*?)'\);/)[0x2];
    consolelog(_0x3eb0f3);
    _0x48f41d = getAes(_0x58161c, _0x3eb0f3).split("video_location] => ")[0x1].split('==')[0x0] + '==';
    url(_0x48f41d);
    headers("Referer", _0x177c3c);
    headers("Accept", "*/*");
    parser();
}

function setfilmizle() {
    url('boncuk45', '');
    var _0x47b974 = url();
    if (url(['#'], 0x1)) {
        url(url().split('#')[0x0]);
    }
    var _0x263ffe = fetch();
    var _0x9b4493 = _0x263ffe.match("data-post-id=\"(.*?)\"")[0x1];
    var _0x523a25 = {};
    try {
        var _0x5cde40 = matchAll(_0x263ffe, /icon_film">.*?<b>(.*?)<\/b>/g);
        if (!url(["setfilm"], 0x1)) {
            _0x5cde40 = matchAll(_0x263ffe, /sticon-film"><\/span><b>(.*?)</g);
        }
        for (let _0x33791d = 0x0; _0x33791d < _0x5cde40.length; _0x33791d++) {
            if (_0x5cde40[_0x33791d][0x1] != 'Raca') {
                _0x523a25[_0x5cde40[_0x33791d][0x1]] = _0x5cde40[_0x33791d][0x1];
            }
        }
    } catch (_0x100654) {}
    var _0x4e8d95 = _0x5cde40.length == _0x523a25.length;
    if (!url(['setfilm'], 0x1)) {
        _0x4e8d95 = !_0x263ffe.includes("tercihimturkcealtyazi");
    }
    if (!_0x47b974.includes('#')) {
        Core.showAlternatesJS(JSON.stringify(_0x523a25));
    } else {
        try {
            var _0x9566ed = _0x523a25[_0x47b974.split('#')[0x1]];
            var _0x3e7772 = baseUrl(url()) + '/wp-admin/admin-ajax.php';
            var _0x235859 = '';
            if (url(["setfilm"], 0x1)) {
                var _0x521f37 = _0x263ffe.match(/"nonce":\s*"(.*?)"/)[0x1];
                var _0x48e0f3 = {
                    'action': "get_video_url",
                    'post_id': _0x9b4493,
                    'player_name': _0x9566ed,
                    'nonce': _0x521f37,
                    'part_key': ''
                };
                if (!_0x4e8d95) {
                    if (lang == 0x1) {
                        _0x48e0f3.part_key = "turkcedublaj";
                    } else {
                        _0x48e0f3.part_key = "turkcealtyazi";
                    }
                }
                var _0x1d2eb2 = generateBoundary();
                var _0x331212 = buildMultipartData(_0x1d2eb2, _0x48e0f3);
                headers("Content-Type", "multipart/form-data; boundary=" + _0x1d2eb2);
                headers("Content-Length", '');
                _0x235859 = fetchPost(_0x331212, _0x3e7772);
            } else {
                var _0x521f37 = _0x263ffe.match(/ajaxurl:.*?nonce:\s*'(.*?)'/)[0x1];
                var _0x48e0f3 = "action=get_video_url&nonce=" + _0x521f37 + "&post_id=" + _0x9b4493 + '&player_name=' + _0x9566ed + "&part_key=";
                if (!_0x4e8d95) {
                    if (lang == 0x1) {
                        _0x48e0f3 += 'turkcedublaj';
                    } else {
                        _0x48e0f3 += "turkcealtyazi";
                    }
                }
                _0x235859 = fetchPost(_0x48e0f3, _0x3e7772);
            }
            url(_0x235859.match(/url":"(.*?)"/)[0x1].replace(/\\/g, ''));
            if (url(["setplay", "player"], 0x1)) {
                headers("Referer", url());
                headers("Accept", "*/*");
                g.deleteHeader('Content-Type');
                g.deleteHeader("Content-Length");
                _0x263ffe = fetch(url());
                var _0x2984dd = _0x263ffe.match(/"videoServer":"(.*?)"/)[0x1];
                var _0x3c7d67 = baseUrl(url()).replace(/\\/g, '');
                var _0x5581ec = _0x263ffe.match(/"videoUrl":"(.*?)"/)[0x1].replace(/\\/g, '');
                url(_0x3c7d67 + '' + _0x5581ec + "?s=" + _0x2984dd);
                consolelog(url());
            } else if (url(["vctplay"], 0x1)) {
                headers("Referer", url());
                g.deleteHeader("Content-Type");
                g.deleteHeader('Content-Length');
                _0x3c7d67 = baseUrl(url());
                _0x263ffe = fetch(url());
                _0x3c7d67 = _0x3c7d67 + _0x263ffe.match(/streamUrl\s*=\s*"(.*?)"/)[0x1];
                url(_0x3c7d67);
                consolelog(url());
            }
            parser();
        } catch (_0x4acde3) {
            error(_0x4acde3.message);
        }
    }
}

function showtv() {
    if (url(["canli-yayin", "canliyayin"], 0x1)) {
        var _0x5c4daa = fetch();
        var _0x580036 = /var\s*videoUrl\s*=\s*"(.*?)"/;
        if (url(['turk', "max"], 0x1)) {
            _0x580036 = /"ht_stream_m3u8":"(https.*?playlist.m3u8.*?)"/;
        }
        url(_0x5c4daa.match(_0x580036)[0x1]);
        parser();
    } else {
        var _0x5c4daa = fetch().match(/"Standart","src":"(.*?)"/)[0x1];
        _0x5c4daa = _0x5c4daa.replace("\\", '');
        url(_0x5c4daa);
        parser();
    }
}

function sezonlukdizi() {
    var _0x6e6eef = url();
    var _0x41ceb5 = fetch();
    _0x41ceb5 = _0x41ceb5.match(/<div\s*bid="(\d*)"\s*did=/)[0x1];
    headers("User-Agent", "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36");
    headers("X-Requested-With", "XMLHttpRequest");
    _0x41ceb5 = fetchPost("bid=" + _0x41ceb5 + '&dil=' + g.getLang(), baseUrl(url()) + "/ajax/dataAlternatif22.asp");
    if (_0x41ceb5.includes("eklenmedi")) {
        error("Sezonlukdizi 1544");
    }
    var _0x5f06e8 = JSON.parse(_0x41ceb5);
    var _0x17a264 = {};
    for (var _0x20e850 = 0x0; _0x20e850 < _0x5f06e8.data.length; _0x20e850++) {
        if (!_0x5f06e8.data[_0x20e850].baslik.toLowerCase().includes("netu") && !_0x5f06e8.data[_0x20e850].baslik.toLowerCase().includes("upto") && !_0x5f06e8.data[_0x20e850].baslik.toLowerCase().includes("multi") && !_0x5f06e8.data[_0x20e850].baslik.toLowerCase().includes("upstream") && !_0x5f06e8.data[_0x20e850].baslik.toLowerCase().includes("videoseyred")) {
            var _0xa375cb = _0x5f06e8.data[_0x20e850].id + '';
            var _0x3bd0bb = _0x5f06e8.data[_0x20e850].baslik;
            _0x17a264[_0x3bd0bb] = _0xa375cb;
        }
    }
    if (_0x17a264.length == 0x0) {
        error("Sezonlukdizi 1560");
    }
    if (!_0x6e6eef.includes('#')) {
        Core.showAlternatesJS(JSON.stringify(_0x17a264));
    } else {
        url(_0x6e6eef.split('#')[0x1]);
        _0x41ceb5 = fetchPost("id=" + url(), baseUrl(_0x6e6eef) + '/ajax/dataEmbed22.asp');
        _0x41ceb5 = _0x41ceb5.match(/(?:SRC|src)="(.*?)"/)[0x1];
        if (_0x41ceb5.startsWith('//')) {
            _0x41ceb5 = "https:" + _0x41ceb5;
        }
        if (_0x41ceb5.includes('/player/fembed.asp')) {
            url("https://dutrag.com/v/" + _0x41ceb5.split("\\?v=")[0x1]);
        } else {
            if (_0x41ceb5.includes("sbembed")) {
                var _0x486d13 = _0x41ceb5.split('/')[0x4].replace(".html", '');
                var _0x1fd4d2 = Core.makeID(0xc) + '||' + _0x486d13 + '||' + Core.makeID(0xc) + "||streamsb";
                var _0x38f2e2 = Core.bytesToHex(_0x1fd4d2);
                var _0x1844e2 = decodeURIComponent(_0x38f2e2);
                _0x1fd4d2 = Core.makeID(0xc) + '||' + Core.makeID(0xc) + '||' + Core.makeID(0xc) + "||streamsb";
                _0x38f2e2 = Core.bytesToHex(_0x1fd4d2);
                var _0x100c42 = decodeURIComponent(_0x38f2e2);
                _0x1fd4d2 = Core.makeID(0xc) + '||' + _0x100c42 + '||' + Core.makeID(0xc) + "||streamsb";
                _0x38f2e2 = Core.bytesToHex(_0x1fd4d2);
                var _0x49c0fb = decodeURIComponent(_0x38f2e2);
                url(baseUrl(url()) + "/sourcesx38/" + _0x1844e2 + '/' + _0x49c0fb);
                _0x41ceb5 = fetch();
                try {
                    url(JSON.parse(_0x41ceb5).stream_data.file);
                } catch (_0x48cc4f) {
                    url(JSON.parse(_0x41ceb5).stream_data.backup);
                }
            } else {
                if (_0x41ceb5.includes("playerjs")) {
                    var _0x486d13 = _0x41ceb5.split('/')[0x4].split("&v=")[0x1];
                    url(hexToString(_0x486d13));
                } else {
                    url(_0x41ceb5);
                }
            }
        }
        g.deleteHeader("X-Requested-With");
        g.deleteHeader('Content-Length');
        parser();
    }
}

function sibnet() {
    data = fetch();
    headers("Referer", url());
    data = (data + '').match(/src:\s*"(.*?)",/)[0x1];
    url(baseUrl(url()) + data);
    parser();
}

function sinefy() {
    var _0x119bb0 = url();
    headers("User-Agent", "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36");
    var _0x33af3f = fetch();
    var _0x3f57a2 = {};
    try {
        var _0x567c90 = matchAll(_0x33af3f, /data-querytype=".*?">\s*<a href="(.*?)"\s*data-navigo.*?>(.*?)</g);
        for (let _0x2574ac = 0x0; _0x2574ac < _0x567c90.length; _0x2574ac++) {
            var _0x1ba019 = _0x567c90[_0x2574ac][0x1];
            var _0xbee8d4 = _0x567c90[_0x2574ac][0x2];
            _0x3f57a2[_0xbee8d4] = _0x1ba019;
        }
    } catch (_0x5467b5) {
        error(_0x5467b5.message);
    }
    if (!_0x119bb0.includes('#')) {
        if (g.getLang() == 0x0) {
            Core.setLang(0x1);
        } else {
            Core.setLang(0x0);
        }
    }
    if (!_0x119bb0.includes('#') && JSON.stringify(_0x3f57a2) != '{}') {
        Core.showAlternatesJS(JSON.stringify(_0x3f57a2));
    } else {
        url(_0x119bb0.split('#')[0x1]);
        headers("Accept", '*/*');
        _0x33af3f = fetch();
        if (url(['rapid'], 0x1)) {
            url(_0x33af3f.match(/file:"(.*?)"/)[0x1]);
        } else {
            try {
                var _0x567c90 = matchAll(_0x33af3f, /iframe.*?src="(.*?)"/g);
                for (let _0x2de31a = 0x0; _0x2de31a < _0x567c90.length; _0x2de31a++) {
                    var _0x1ba019 = _0x567c90[_0x2de31a][0x1];
                    if (!_0x1ba019.includes("finema")) {
                        url(_0x1ba019);
                        break;
                    }
                }
                url(fixUrl(url()));
            } catch (_0x2a1cfd) {
                error(_0x2a1cfd.message);
            }
        }
        parser();
    }
}

function sinemacx() {
    var _0x44ae32 = url();
    url("?l=2", '');
    var _0x2d278d = fetch();
    _0x2d278d = _0x2d278d.match(/iframe.*?data-vsrc="(.*?)"/)[0x1];
    var _0x5a9384 = _0x2d278d.split('/')[0x4];
    url(_0x2d278d);
    url(fixUrl(url()));
    _0x2d278d = fetch();
    var _0x38d0c1 = '';
    try {
        _0x38d0c1 = _0x2d278d.match(/playerjsSubtitle.*?(http.*?vtt)"/)[0x1];
    } catch (_0x3d4d7b) {
        _0x38d0c1 = '';
    }
    headers('content-type', "application/x-www-form-urlencoded; charset=UTF-8");
    headers('x-requested-with', "XMLHttpRequest");
    url("video/", 'player/index.php?data=');
    url(url() + "&do=getVideo");
    _0x2d278d = fetchPost("hash=" + _0x5a9384 + "&r=" + baseUrl(_0x44ae32), url());
    var _0x217884 = JSON.parse(_0x2d278d);
    url(_0x217884.securedLink);
    g.deleteHeader("content-type");
    g.deleteHeader('x-requested-with');
    parser();
}

function sinemadelisi() {
    error("Sinemadelisi isimli kaynak site kapalÄ± olduÄŸundan oynatÄ±lamÄ±yor.");
    var _0x45dc2c = url();
    var _0x41b18b = fetch();
    _0x41b18b = _0x41b18b.match(/inepisode">(.*?)"butonlar">/)[0x1];
    var _0x37fa44 = {
        _0x305041: url()
    };
    try {
        var _0x267290 = matchAll(_0x41b18b, /<a\s*href="(.*?)"\s*class="post.*?dil="undefined">(.*?)</g);
        for (let _0x13d799 = 0x0; _0x13d799 < _0x267290.length; _0x13d799++) {
            _0x37fa44[_0x267290[_0x13d799][0x2] + '-' + _0x13d799] = _0x267290[_0x13d799][0x1];
        }
    } catch (_0xd4c145) {}
    if (!_0x45dc2c.includes('#')) {
        Core.showAlternatesJS(JSON.stringify(_0x37fa44));
    } else {
        url(_0x45dc2c.split('#')[0x1]);
        url('?l=2', '');
        _0x41b18b = fetch();
        url(_0x41b18b.match(/fitvidscompatible"\s*data-lazy-src="(.*?)"/)[0x1]);
        url(fixUrl(url()));
        parser();
    }
}

function sinemafilmizle() {
    var _0x2502a9 = url();
    headers("Referer", url());
    var _0x2e1e1f = fetch();
    var _0x3c5729 = [];
    var _0x13283c = [];
    var _0xba26a = [];
    var _0x2bfcab = {};
    var _0x6aec46 = "tra";
    if (g.getLang() == 0x0) {
        _0x6aec46 = "trd";
    }
    try {
        var _0x2dd280 = matchAll(_0x2e1e1f, /dil="(.*?)">.*?<\/span>/g);
        for (let _0x4d0b66 = 0x0; _0x4d0b66 < _0x2dd280.length; _0x4d0b66++) {
            _0x3c5729.push(_0x2dd280[_0x4d0b66][0x1]);
        }
        _0x2dd280 = matchAll(_0x2e1e1f, /dil=".*?">(.*?)<\/span>/g);
        for (let _0x3895db = 0x0; _0x3895db < _0x2dd280.length; _0x3895db++) {
            _0x13283c.push(_0x2dd280[_0x3895db][0x1]);
        }
        _0x2dd280 = matchAll(_0x2e1e1f, /html\('.*?<iframe.*?src="(.*?)"/g);
        for (let _0x458263 = 0x0; _0x458263 < _0x2dd280.length; _0x458263++) {
            _0xba26a.push(_0x2dd280[_0x458263][0x1]);
        }
    } catch (_0x36399c) {
        error(_0x36399c.message);
    }
    for (var _0x30cac3 = 0x0; _0x30cac3 < _0x3c5729.length; _0x30cac3++) {
        if (_0x3c5729[_0x30cac3] == _0x6aec46) {
            try {
                _0x2bfcab[_0x13283c[_0x30cac3]] = _0xba26a[_0x30cac3];
            } catch (_0x2397c8) {}
        }
    }
    if (!_0x2502a9.includes('#') && JSON.stringify(_0x2bfcab) != '{}') {
        Core.showAlternatesJS(JSON.stringify(_0x2bfcab));
    } else {
        url(_0x2502a9.split('#')[0x1]);
        var _0x28adcd = _0xba26a.indexOf(url());
        var _0x5a9956 = '';
        if (_0x28adcd != null) {
            _0x5a9956 = _0x13283c[_0x28adcd];
        }
        if (_0x5a9956.toLowerCase().includes("sine")) {
            if (!g.isWebView()) {
                error("No Webview");
            } else {
                getWebViewOwnContentJS(_0x2502a9, "popcornvakti", "I AM NOT LOOKING", "playSheilaBtn", '', 0x0, false, g.getHeadersJSON() + '', 0x1);
            }
        } else {
            if (url(['my.mail.ru', "vidmoly"], 0x1)) {
                if (url(['vidmoly'], 0x1)) {
                    url(url().split('vid=')[0x1]);
                }
            } else {
                headers('Referer', _0x2502a9);
                _0x2e1e1f = fetch();
                url(_0x2e1e1f.match(/player"><iframe.*?src=["\'](.*?)["\']/)[0x1]);
                if (!url(["odno"], 0x1) && !url(['ok.ru'], 0x1)) {
                    _0x2e1e1f = fetch();
                    url(_0x2e1e1f.match(/<iframe.*?src="(.*?)"/)[0x1]);
                }
            }
            parser();
        }
    }
}

function siyahfilmizle() {
    var _0x4c786f = url();
    headers("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36");
    headers('Cookie', "reklamlar=1; footerreklam=1; _ga=GA1.1.630178980.1748966407; cf_clearance=TbDtWgimRBuNHyQdJqmyELXQTo42tL_yPB5PpNifRb4-1748970923-1.2.1.1-gYA63kMcNnBseNGc32R47J8EzmV1dtkttjuyp5sKxKCetrTo1Yt1nHVmWmYhbwdW5ZxATcSsdwH7FWbKfWssR_Gye0g0Y0IIfWd7TQ2U53UfvZ0GkssilTraYwECIG3iyf_7.0EE_qcqTuzAykL9KRV4GDtI4hyZnh5mm3JVtflUm2GD6.nS4tAlKwADqWDap04KRHnZ1XrdjQdMevPnFANtsJkhwWCt8suZHscBrCMT0xTQPhEh4ddgI.Q5NJQ6iVo8SOI0N0pCUVOBfFkr46ogJn6HIIXj0GUI08mmI.KAI0uiLuM0soXZrKhsO6Ts8_ntT2Yftn0uG6fxU0NcPu7cRf9uxeldK99oLwK2c7TE4Aog4ZyKLJVC0nBEezdO; _ga_H37YEWQ148=GS2.1.s1748970902$o2$g1$t1748970922$j40$l0$h0");
    var _0x3d1554 = fetch();
    var _0x17e786 = {};
    try {
        var _0x2ba16c = matchAll(_0x3d1554, /<li>.*?<a href="(.*?)".*?<\/i>.*?(Film.*?)<.*?<\/li>/g);
        for (let _0x55c2a4 = 0x0; _0x55c2a4 < _0x2ba16c.length; _0x55c2a4++) {
            var _0x55e766 = _0x2ba16c[_0x55c2a4][0x2];
            var _0x5d43b4 = _0x2ba16c[_0x55c2a4][0x1];
            var _0x42d891 = _0x2ba16c[_0x55c2a4][0x3];
            if (_0x42d891 == '') {
                _0x42d891 = 'FilmPlatin';
                _0x17e786[_0x42d891] = _0x5d43b4;
            }
            if (_0x55e766 != null) {
                if (_0x55e766.includes('en') && g.getLang() == 0x1 || _0x55e766.includes('tr') && g.getLang() == 0x0) {
                    _0x17e786[_0x42d891] = _0x5d43b4;
                }
            }
        }
    } catch (_0x907ba0) {
        error(_0x907ba0.message);
    }
    if (!_0x4c786f.includes('#') && JSON.stringify(_0x17e786) != '{}') {
        Core.showAlternatesJS(JSON.stringify(_0x17e786));
    } else {
        if (_0x4c786f.includes('#')) {
            url(_0x4c786f.split('#')[0x1]);
        }
        _0x3d1554 = fetch();
        url(_0x3d1554.match(/iframe.*?src=["\'](.*?)["\']/)[0x1].replace("#038;", ''));
        url(fixUrl(url()));
        parser();
    }
}

function startv() {
    if (url(["canli-yayin"], 0x0)) {
        var _0x84729a = fetch("https://dyg-ads-cdn.s3.eu-west-1.amazonaws.com/live-broadcast-player/v1/bundle.js");
        var _0x1aca52 = /Ntv.*?development":"(.*?)"/;
        if (url(["startv"], 0x0)) {
            _0x1aca52 = /Startv.*?development":"(.*?)"/;
        }
        url(_0x84729a.match(_0x1aca52)[0x1]);
        parser();
    } else {
        var _0x84729a = fetch();
        refId = _0x84729a.match(/<meta property="dyg:tags" content="(.*?)"\/>/)[0x1].split(',')[0x2];
        var _0x3d0cf4 = JSON.parse(fetch('https://dygvideo.dygdigital.com/api/video_info?akamai=true&PublisherId=1&ReferenceId=StarTv_' + refId + "&SecretKey=NtvApiSecret2014*"));
        url(fixUrl(_0x3d0cf4.data.flavors['0'].file_url_1));
        parser();
    }
}

function sto() {
    var _0x131436 = url();
    var _0xb48b4a = fetch();
    var _0x4fc1f2 = baseUrl(url());
    var _0x5dafb1 = {};
    try {
        var _0x50e203 = matchAll(_0xb48b4a, /data-lang-key="(\d)"\s*data-link-id="\d+"\s*data-link-target="(.*?)".*?Hoster\s(.*?)"/g);
        for (let _0x4bcc3b = 0x0; _0x4bcc3b < _0x50e203.length; _0x4bcc3b++) {
            var _0x4be333 = _0x50e203[_0x4bcc3b][0x1];
            var _0x5a9f98 = _0x50e203[_0x4bcc3b][0x2];
            var _0x53bbd5 = _0x50e203[_0x4bcc3b][0x3];
            if (_0x4be333 != null) {
                if (_0x4be333 == '2' && g.getLang() == 0x0 || _0x4be333 == '1' && g.getLang() == 0x2) {
                    _0x5dafb1[_0x53bbd5] = _0x4fc1f2 + _0x5a9f98;
                }
            }
        }
    } catch (_0x5b05aa) {
        error(_0x5b05aa.message);
    }
    if (!_0x131436.includes('#') && JSON.stringify(_0x5dafb1) != '{}') {
        Core.showAlternatesJS(JSON.stringify(_0x5dafb1));
    } else {
        url(_0x131436.split('#')[0x1]);
        url(Core.getRedirectUrlJS(url()));
        if (url(["vidoza", "videzz"], 0x1)) {
            _0xb48b4a = fetch();
            url(_0xb48b4a.match(/source\s*src="(.*?)"/)[0x1]);
        }
        parser();
    }
}

function streamplayer() {
    headers("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    headers("x-requested-with", "XMLHttpRequest");
    var _0x5066c5 = fetch();
    url(_0x5066c5.match(/sources\s*:\s* \[\{file:"(.*?)"/)[0x1]);
    headers('Referer', 'https://vidmoly.to/');
    parser();
}

function streamruby() {
    headers("User-Agent", "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36");
    data = fetch();
    url((data + '').match(/file:"(.*?m3u8.*?)"/)[0x1]);
    headers("Referer", "https://streamruby.com/");
    parser();
}

function streamtheworld() {
    var _0x18f9ac = fetch().split("<transports>");
    var _0x503ba6 = '';
    for (let _0x1328cd = 0x0; _0x1328cd < _0x18f9ac.length; _0x1328cd++) {
        if (_0x18f9ac[_0x1328cd].includes("AAC")) {
            _0x503ba6 = _0x18f9ac[_0x1328cd];
            break;
        }
    }
    var _0x5e34ce = _0x503ba6.match(/<ip>(.*?)<\/ip>/)[0x1];
    var _0x897ccd = _0x503ba6.match(/<mount>(.*?)<\/mount>/)[0x1];
    g.setMediaType("mp5");
    url('https://' + _0x5e34ce + '/' + _0x897ccd + '.aac');
    headers("Connection", "keep-alive");
    parser();
}

function streamoupload() {
    var _0x19cbc2 = fetch();
    _0x19cbc2 = _0x19cbc2.match(/<script\s*type=".*?text\/javascript">\s*(eval[\s\S]*?)\s*<\/script>/)[0x1];
    _0x19cbc2 = unPack(_0x19cbc2);
    url(_0x19cbc2.match(/file\s*:\s*"(.*?streamoupload.*?)"/)[0x1].replace(/\\\\\//g, '/'));
    g.deleteHeader("Referer");
    g.deleteHeader("Base");
    parser();
}

function streamtape() {
    url(fixUrl(url()));
    headers('Referer', 'https://streamtape.com/');
    var _0x6b83a4 = fetch();
    _0x6b83a4 = matchAll(_0x6b83a4, /ById\('.+?=\s*(["']\/\/[^;<]+)/g);
    _0x6b83a4 = _0x6b83a4[_0x6b83a4.length - 0x1][0x1];
    var _0x3f4d14 = _0x6b83a4.split('+');
    var _0x2ad021 = '';
    for (let _0x2593bc = 0x0; _0x2593bc < _0x3f4d14.length; _0x2593bc++) {
        var _0x5cf9a6 = _0x3f4d14[_0x2593bc].split("'").join("\"");
        try {
            var _0x1ce66d = _0x5cf9a6.match(/"([^"]*)/)[0x1];
            var _0x48aa78 = 0x0;
            if (_0x5cf9a6.includes("substring")) {
                var _0x21ffb8 = matchAll(_0x5cf9a6, /substring\((\d+)/g);
                for (let _0x30d60a = 0x0; _0x30d60a < _0x21ffb8.length; _0x30d60a++) {
                    _0x48aa78 = _0x48aa78 + parseInt(_0x21ffb8[_0x30d60a][0x1]);
                }
            }
            _0x2ad021 = _0x2ad021 + _0x1ce66d.substring(_0x48aa78);
        } catch (_0x29d8c8) {}
    }
    _0x2ad021 = _0x2ad021 + "&stream=1";
    url(fixUrl(_0x2ad021));
    parser();
}

function superfilmgeldi() {
    var _0x36fb0b = url();
    var _0x479f7a = fetch(url().replace("?l=1", '').replace("?l=0", ''));
    _0x479f7a = _0x479f7a.match(/iframe\s*src="(.*?)"/)[0x1];
    if (_0x479f7a.startsWith('/')) {
        _0x479f7a = "https:" + _0x479f7a;
    }
    if (_0x479f7a.includes("vidmoly") || _0x479f7a.includes("ok.ru") || _0x479f7a.includes("odnoklas")) {
        url(_0x479f7a);
        parser();
    } else {
        if (_0x479f7a.includes("mixlion")) {
            _0x479f7a = fetch(_0x479f7a);
            var _0x19576f = _0x479f7a.match(/"videoServer":"(.*?)"/)[0x1];
            var _0x4677c2 = "https://mixlion.com" + _0x479f7a.match(/"videoUrl":"(.*?)"/)[0x1].replace(/\\/g, '');
            _0x4677c2 = _0x4677c2 + '?s=' + _0x19576f + "&d=";
            headers("Referer", _0x4677c2);
            headers("Accept", "*/*");
            _0x479f7a = fetch(_0x4677c2);
            url(_0x479f7a.match(/(htt.*?)$/)[0x1]);
        } else {
            if (_0x479f7a.includes("mixtiger")) {
                headers('content-type', "application/x-www-form-urlencoded; charset=UTF-8");
                headers('x-requested-with', "XMLHttpRequest");
                var _0x31cdd3 = _0x479f7a.split('/')[0x5];
                fetch(_0x479f7a);
                _0x479f7a = fetchPost("hash=" + _0x31cdd3 + '&r=' + baseUrl(_0x36fb0b) + "&s=", _0x479f7a + "?do=getVideo");
                var _0x54cea5 = JSON.parse(_0x479f7a);
                if (_0x54cea5.hasOwnProperty("videoSrc")) {
                    _0x479f7a = _0x54cea5.videoSrc;
                } else {
                    _0x479f7a = _0x54cea5.videoSources[0x0].file;
                }
                url(_0x479f7a);
            } else {
                if (_0x479f7a.includes("mixeagle")) {
                    headers('Referer', baseUrl(_0x479f7a));
                    headers("Accept", '*/*');
                    var _0x4cd717 = baseUrl(_0x479f7a);
                    var _0x479f7a = fetch(_0x479f7a);
                    var _0x6ca64f = _0x479f7a.match(/"videoServer":"(.*?)"/)[0x1];
                    _0x479f7a = _0x4cd717 + _0x479f7a.match(/videoUrl":"(.*?)"/)[0x1].split("\\").join('') + '?s=' + _0x6ca64f + "&d=";
                    url(_0x479f7a);
                }
            }
        }
    }
    parser();
}

function supervideo() {
    url(fixUrl(url()));
    var _0x578beb = fetch();
    try {
        _0x578beb = unPack(_0x578beb.match(/(eval\(function.*?)<\/script>/)[0x1]);
        try {
            url(_0x578beb.match(/file:"(.*?)"/)[0x1]);
        } catch (_0x44c214) {
            url(_0x578beb.match(/src:"(.*?)"/)[0x1]);
        }
    } catch (_0x5c3288) {
        url(_0x578beb.match(/\[\{file:"(.*?)"/)[0x1]);
    }
    parser();
}

function tafdi() {
    headers("X-requested-with", "XMLHttpRequest");
    headers("Content-Type", "Application/x-wwww-form-urlencoded; charset=UTF-8");
    var _0x15b275 = fetch();
    var _0x19b656 = _0x15b275.match(/<iframe\s*src=[\'"](.*?)[\'"]/)[0x1];
    url(_0x19b656);
    headers("Referer", url());
    _0x15b275 = fetch();
    var _0x5a1b41 = matchAll(_0x15b275, /"file":\s*"((?:(?!thumbs).)*?)"/g);
    var _0x253996 = '';
    var _0x40c673 = '';
    try {
        _0x253996 = _0x5a1b41[0x1][0x1].replace(/\\/g, '');
    } catch (_0x28b532) {}
    try {
        _0x40c673 = _0x5a1b41[0x2][0x1].replace(/\\/g, '');
    } catch (_0x8476cf) {}
    var _0x1df70d = _0x253996;
    if (_0x40c673.includes("tur") || _0x40c673.includes('tr')) {
        _0x1df70d = _0x40c673;
    }
    link = _0x5a1b41[0x0][0x1];
    link = unescape(link.replace(/\\x/g, '%'));
    sub(_0x1df70d.replace(".vtt", '.srt'));
    url(link);
    parser();
}

function tele1() {
    url(fetch().match(/iframe.*?src="(https:\/\/www.youtube.*?)"/)[0x1].replace("https://www", "https://m").replace("/embed/", "/watch?v="));
    parser(url(), 0x1, '', '', false);
}

function teve2() {
    if (url(["canli-yayin"], 0x0)) {
        var _0x29dcea = fetch();
        try {
            url(_0x29dcea.match(/file:'(.*?)'/)[0x1]);
        } catch (_0x32d250) {
            url(_0x29dcea.match(/contentUrl"\s*:\s*"(.*?)"/)[0x1]);
        }
        parser();
    } else {
        var _0x29dcea = fetch().match(/itemprop="embedURL" href="(.*?)"/)[0x1].replace("video", "action/media");
        _0x29dcea = fetch(_0x29dcea);
        var _0x5b8842 = JSON.parse(_0x29dcea);
        url(_0x5b8842.Media.Link.ServiceUrl + '/' + _0x5b8842.Media.Link.SecurePath);
        parser();
    }
}

function thehun() {
    url(fixUrl(fetch().match(/source src="(.*?)"/)[0x1]));
    parser();
}

function tjk() {
    url(fetch().match(/hls\s*:\s*'(.*?)'/)[0x1]);
    parser();
}

function tlc() {
    if (url(["canli-izle"], 0x0)) {
        var _0x29e7b8 = fetch();
        url(_0x29e7b8.match(/(?:daionUrl|liveUrl)\s*(?:=|\:)\s*(?:\'|")(.*?)(?:\'|")/)[0x1]);
        parser();
    } else {
        var _0x2eeeb3 = '';
        var _0x5cf3e6 = '20';
        if (url(["dmax"], 0x1)) {
            _0x5cf3e6 = '27';
        }
        _0x2eeeb3 = fetch().match(/referenceId\s*:\s*'(.*?)'/)[0x1];
        url("https://dygvideo.dygdigital.com/api/redirect?PublisherId=" + _0x5cf3e6 + '&ReferenceId=' + _0x2eeeb3 + '&SecretKey=NtvApiSecret2014*');
        parser();
    }
}

function trstx() {
    var _0x4d1b6a = fetch().match(/playerConfigs\s*=\s*(.*?);/)[0x1];
    var _0x53c71d = JSON.parse(_0x4d1b6a).href + '' + JSON.parse(_0x4d1b6a).file;
    url(fixUrl(_0x53c71d));
    _0x4d1b6a = matchAll(fetch(), /title":\s*"(.*?)".*?file":\s*"(.*?)"/g);
    var _0x4d12ac = '';
    var _0x3660d4 = {};
    for (var _0x5bc161 = 0x0; _0x5bc161 < _0x4d1b6a.length; _0x5bc161++) {
        if (g.getLang() == 0x1 && _0x4d1b6a[_0x5bc161][0x1].includes("Altyaz")) {
            _0x4d12ac = _0x4d1b6a[_0x5bc161][0x2];
        } else {
            if (g.getLang() == 0x0 && _0x4d1b6a[_0x5bc161][0x1].includes('Dublaj')) {
                _0x4d12ac = _0x4d1b6a[_0x5bc161][0x2];
            } else {
                _0x3660d4[_0x4d1b6a[_0x5bc161][0x1]] = _0x4d1b6a[_0x5bc161][0x1];
                if (g.getLang() == 0x2) {
                    _0x4d12ac = _0x4d1b6a[_0x5bc161][0x2];
                }
            }
        }
    }
    if (Object.keys(_0x3660d4).length > 0x1) {
        Core.showAlternatesJS(JSON.stringify(_0x3660d4));
    } else {
        var _0x316a9e = url().split("playlist");
        url(_0x316a9e[0x0] + "playlist/" + _0x4d12ac + "!!.txt");
        url(fetch());
        parser();
    }
}

function tv360() {
    var _0x1a632f = fetch();
    url(_0x1a632f.match(/source\s*src="(.*?)"/)[0x1]);
    parser();
}

function tv8() {
    if (url(["canli-yayin"], 0x0)) {
        var _0x46bf61 = fetch();
        url(_0x46bf61.match(/var videoUrl = "(.*?)"/)[0x1]);
        parser();
    } else {
        url(fetch().match(/hls\s*:\s*"(.*?)"/)[0x1].replace(/ /g, '').replace(/\"/g, ''));
        parser();
    }
}

function tvem() {
    var _0x11a2f0 = fetch();
    url(fetch(fixUrl(_0x11a2f0.match(/<div class="live-area">\s*.*?<script src="(.*?)"><\/script>/)[0x1])).match(/yayincomtr4="(.*?)"/)[0x1]);
    parser();
}

function tvnet() {
    url(fetch().match(/live-image"\s*href="(.*?)"/)[0x1]);
    parser();
}

function ucankus() {
    url(fetch().match(/<source\s*src="(.*?)"/)[0x1]);
    parser();
}

function ugurfilm() {
    var _0x335137 = url();
    var _0x49bc8e = fetch();
    var _0x71f792 = _0x49bc8e;
    var _0x5a4765 = {};
    if (!url(['#'], 0x1)) {
        try {
            _0x49bc8e = _0x49bc8e.match("<iframe.*?src=\"https://" + url().split('/')[0x2] + "/player(.*?)\"")[0x1];
            url("https://" + url().split('/')[0x2] + "/player" + _0x49bc8e);
            if (url([url().split('/')[0x2] + '/player/play.php'], 0x1)) {
                var _0x4f5170 = url().replace('https://' + url().split('/')[0x2] + "/player/play.php?vid=", '');
                _0x49bc8e = matchAll(fetch(), /class="c-dropdown__item"\s*data-dropdown-value="(.*?)" data-order-value="(\d+)"/g);
                var _0x395a65 = "https://" + url().split('/')[0x2] + "/player/ajax_sources.php";
                for (var _0x48a46e = 0x0; _0x48a46e < _0x49bc8e.length; _0x48a46e++) {
                    var _0x2a3775 = "vid=" + _0x4f5170 + '&alternative=' + _0x49bc8e[_0x48a46e][0x1] + '&ord=' + _0x49bc8e[_0x48a46e][0x2];
                    try {
                        headers("X-Requested-With", "XMLHttpRequest");
                        var _0x2ce67f = JSON.parse(fetchPost(_0x2a3775, _0x395a65)).iframe + '';
                        _0x2ce67f = fixUrl(_0x2ce67f) + '';
                        if (_0x2ce67f.includes("mail")) {
                            _0x5a4765.Mailru = _0x2ce67f;
                        } else {
                            if (_0x2ce67f.includes("fembed")) {
                                _0x5a4765.Fembed = _0x2ce67f;
                            } else {
                                if (_0x2ce67f.includes("ok.ru")) {
                                    _0x5a4765['Ok.ru'] = _0x2ce67f;
                                } else {
                                    if (_0x2ce67f.includes("odnoklassniki")) {
                                        _0x5a4765['Ok.ru'] = _0x2ce67f;
                                    } else {
                                        if (_0x2ce67f.includes("youtube")) {
                                            _0x5a4765.Youtube = _0x2ce67f;
                                        } else {
                                            if (_0x2ce67f.includes("vidmoly")) {
                                                _0x5a4765.Vidmoly = _0x2ce67f;
                                            } else if (_0x2ce67f.includes('1x')) {
                                                _0x5a4765['1x'] = _0x2ce67f;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } catch (_0xede477) {}
                }
            } else {
                try {
                    _0x49bc8e = _0x71f792.match(/parttab tab-aktif(.*?)<\/iframe>/)[0x1].match(/href="(.*?)"/)[0x1];
                    var _0x2ce67f = fetch(_0x49bc8e).match(/iframe.*?src=(?:'|")(.*?)(?:'|")/)[0x1];
                    if (_0x2ce67f.includes("mail")) {
                        _0x5a4765.Mailru = _0x2ce67f;
                    } else {
                        if (_0x2ce67f.includes('fembed')) {
                            _0x5a4765.Fembed = _0x2ce67f;
                        } else {
                            if (_0x2ce67f.includes("ok.ru")) {
                                _0x5a4765["Ok.ru"] = _0x2ce67f;
                            } else {
                                if (_0x2ce67f.includes("odnoklassniki")) {
                                    _0x5a4765["Ok.ru"] = _0x2ce67f;
                                } else {
                                    if (_0x2ce67f.includes("youtube")) {
                                        _0x5a4765.Youtube = _0x2ce67f;
                                    } else {
                                        if (_0x2ce67f.includes("vidmoly")) {
                                            _0x5a4765.Vidmoly = _0x2ce67f;
                                        } else if (_0x2ce67f.includes('1x')) {
                                            _0x5a4765['1x'] = _0x2ce67f;
                                        }
                                    }
                                }
                            }
                        }
                    }
                } catch (_0x383980) {
                    try {
                        _0x49bc8e = _0x71f792.match(/iframe.*?src="(.*?)"/)[0x1];
                        _0x5a4765.Youtube = _0x49bc8e;
                    } catch (_0xc83619) {}
                }
            }
        } catch (_0x4d2e25) {
            var _0xee6c51 = '';
            try {
                _0xee6c51 = _0x49bc8e.match(/<iframe.*?src="(.*?)"/)[0x2];
            } catch (_0x5a626a) {
                _0xee6c51 = _0x49bc8e.match(/<iframe.*?src="(.*?)"/)[0x1];
            }
            var _0x452751 = _0x49bc8e.match(/movie\/(.*?)\/iframe/)[0x1];
            if (_0xee6c51.includes("trstx") || _0xee6c51.includes("sobreatsesuyp")) {
                url(_0xee6c51);
            } else {
                _0x5a4765["AltyazÄ±lÄ±"] = "https:" + fetch(_0xee6c51 + "?t=" + _0x452751).match(/"hls":"(.*?)"/)[0x1].replace(/\//g, '');
                _0x5a4765.Dublaj = "https:" + fetch(_0xee6c51).match(/"hls":"(.*?)"/)[0x1].replace(/\//g, '');
            }
        }
    }
    if (!_0x335137.includes('#') && Object.keys(_0x5a4765).length > 0x1) {
        Core.showAlternatesJS(JSON.stringify(_0x5a4765));
    } else {
        if (url(['#'], 0x1)) {
            url(url().split('#')[0x1].replace(/\\/g, ''));
            url(fixUrl(url()));
        } else {
            url(_0x5a4765[Object.keys(_0x5a4765)[0x0]]);
        }
        parser();
    }
}

function unutulmaz() {
    var _0x3ba8b7 = url();
    var _0x5f243e = fetch();
    var _0xe058b8 = _0x5f243e.match(/<iframe.*?src=(.*?)\s/)[0x1];
    _0xe058b8 = _0xe058b8.replace(/"/g, '');
    if (!_0xe058b8.startsWith("http")) {
        _0xe058b8 = 'https:' + _0xe058b8;
    }
    var _0x32239 = {
        _0x3f90ee: _0xe058b8
    };
    try {
        var _0x370c3b = matchAll(_0x5f243e, /<li class="part">\s*<a href="(.*?)"/g);
        for (let _0x304d62 = 0x0; _0x304d62 < _0x370c3b.length; _0x304d62++) {
            var _0x275840 = fetch(_0x370c3b[_0x304d62][0x1]);
            var _0x46d2a4 = _0x275840.match(/<iframe.*?src=(.*?)\s/)[0x1];
            if (!_0x46d2a4.startsWith("http")) {
                _0x46d2a4 = "https:" + _0x46d2a4;
            }
            var _0x2cd451 = _0x46d2a4.match(/(?:\/\/www|\/\/)(.*?)\./);
            _0x32239[_0x2cd451] = _0x46d2a4;
        }
    } catch (_0x20ce9f) {
        error(_0x20ce9f.message);
    }
    if (!_0x3ba8b7.includes('#') && JSON.stringify(_0x32239) != '{}' && Object.keys(_0x32239).length > 0x1) {
        Core.showAlternatesJS(JSON.stringify(_0x32239));
    } else {
        if (_0x3ba8b7.includes('#')) {
            url(_0x3ba8b7.split('#')[0x1]);
        }
        if (Object.keys(_0x32239).length == 0x1) {
            url(_0xe058b8);
        }
        if (g.getLang() == 0x1) {
            Core.setLang(0x0);
        } else {
            Core.setLang(0x1);
        }
        headers("Referer", _0x3ba8b7);
        parser();
    }
}

function vectorx() {
    headers("Referer", baseUrl(url()));
    var _0x3172a3 = fetch() + '';
    var _0x11f9d4 = _0x3172a3.match(/Klauios = '(.*?)'/)[0x1];
    _0x3172a3 = getVectorx(_0x11f9d4);
    consolelog(_0x3172a3);
    url(_0x3172a3.match(/file:\s*"(.*?)",/)[0x1]);
    try {
        sub(_0x3172a3.match(/subtitle:\s*"\[Turkish\](.*?)",/)[0x1]);
    } catch (_0x4cd235) {}
    parser();
}

function videoseyred() {
    url(fixUrl(url()));
    headers('Referer', baseUrl(url()));
    url("https://videoseyred.in" + fetch().match(/playlistUrl='(.*?)'/)[0x1]);
    var _0x1c5de5 = JSON.parse(fetch());
    url(_0x1c5de5[0x0].sources[0x0].file);
    var _0x5a8079 = _0x1c5de5[0x0].tracks;
    for (let _0x54f8d6 = 0x0; _0x54f8d6 < _0x5a8079.length; _0x54f8d6++) {
        if (_0x5a8079[_0x54f8d6].hasOwnProperty("label")) {
            if (_0x5a8079[_0x54f8d6].label.includes('T')) {
                sub(_0x5a8079[_0x54f8d6].file);
                break;
            }
        }
    }
    parser();
}

function vidload() {
    url(fixUrl(url()));
    var _0x32f654 = url();
    var _0x46cd42 = new Date().getTime();
    url(baseUrl(url()) + '/video.js?' + _0x46cd42);
    var _0x3fefab = fetch();
    var _0x469dba = _0x3fefab.match(/window,["\'](.*?)["\'],["\'].*?["\']/)[0x1];
    var _0x3101e4 = _0x3fefab.match(/window,["\'].*?["\'],["\'](.*?)["\']/)[0x1];
    headers(_0x469dba, _0x3101e4);
    headers("Referer", _0x32f654);
    var _0x29c06b = _0x32f654.split('iframe/');
    var _0x5856b6 = _0x29c06b[_0x29c06b.length - 0x1];
    url(baseUrl(_0x32f654) + "/ajax/" + _0x5856b6 + '?' + _0x46cd42);
    _0x3fefab = fetch();
    var _0x4e0389 = JSON.parse(_0x3fefab);
    url(_0x4e0389.file + '?' + _0x4e0389.hash);
    parser();
}

function vidlop() {
    var _0x55e63f = url().split('/');
    _0x55e63f = _0x55e63f[_0x55e63f.length - 0x1];
    headers("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    headers("x-requested-with", 'XMLHttpRequest');
    var _0x3e19c8 = fetchPost("hash=" + _0x55e63f + "&r=" + baseUrl(url()), "https://vidlop.com/player/index.php?data=" + _0x55e63f + "&do=getVideo");
    _0x3e19c8 = JSON.parse(_0x3e19c8);
    url(_0x3e19c8.securedLink);
    var _0x574c04 = fetch();
    try {
        var _0x258d09 = matchAll(_0x574c04, /URI="(.*?\.vtt)"/g);
        for (let _0x4d3506 = 0x0; _0x4d3506 < _0x258d09.length; _0x4d3506++) {
            if (_0x258d09[_0x4d3506][0x1].includes("tur") && _0x258d09[_0x4d3506][0x1].includes(".vtt")) {
                sub(_0x258d09[_0x4d3506][0x1]);
            }
        }
    } catch (_0x414f48) {}
    parser();
}

function vidmoly() {
    url(fixUrl(url()));
    url(".to", ".me");
    url.fasturl;
    url["document has moved"];
    headers("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    headers("Accept", "text/html");
    headers('charset', 'utf-8');
    headers("sec-fetch-dest", 'iframe');
    headers('Referer', baseUrl(url()));
    g.logHeader();
    var _0xc8e3d7 = fetch();
    url(_0xc8e3d7.match(/sources:\s*.*?(https.*?m3u8).*?\],/)[0x1]);
    try {
        sub(_0xc8e3d7.match(/file\\s*:\\s*"(\/srt.*?)"/)[0x1]);
    } catch (_0xe0c656) {}
    parser();
}

function vidmoxy() {
    var _0x200958 = fetch();
    try {
        var _0x589683 = matchAll(_0x200958, /file":"(.*?)"/g);
        for (let _0x5a3a53 = 0x0; _0x5a3a53 < _0x589683.length; _0x5a3a53++) {
            if (_0x589683[_0x5a3a53][0x1].includes('Tur')) {
                sub(_0x589683[_0x5a3a53][0x1].split("\\").join(''));
            }
        }
    } catch (_0x2be615) {}
    try {
        _0x200958 = _0x200958.match(/EE\.dd\("(.*?)"\)/)[0x1];
        eval(function(_0x42dcef, _0xd3f17c, _0x196428, _0x38f62b, _0x3e1d99, _0x29af5c) {
            _0x3e1d99 = function(_0x191c1f) {
                return _0x191c1f.toString(_0xd3f17c);
            };
            if (!''.replace(/^/, String)) {
                while (_0x196428--) {
                    _0x29af5c[_0x3e1d99(_0x196428)] = _0x38f62b[_0x196428] || _0x3e1d99(_0x196428);
                }
                _0x38f62b = [function(_0x20a178) {
                    return _0x29af5c[_0x20a178];
                }];
                _0x3e1d99 = function() {
                    return "\\w+";
                };
                _0x196428 = 0x1;
            };
            while (_0x196428--) {
                if (_0x38f62b[_0x196428]) {
                    _0x42dcef = _0x42dcef.replace(new RegExp("\\b" + _0x3e1d99(_0x196428) + "\\b", 'g'), _0x38f62b[_0x196428]);
                }
            }
            return _0x42dcef;
        }("1 e={7:3(s){5 s.f('').h().i('')},8:3(s){5 s.2(/[a-j-9]/g,3(c){5 k.l((c<='9'?m:n)>=(c=c.o(0)+p)?c:c-q)})},t:3(s){1 r=6.7(s);1 a=6.8(r);1 b=u(a);5 b.2(/\\+/g,'-').2(/\\//g,'d').2(/=+$/,'')},v:3(s){s=s.2(/-/g,'+').2(/d/g,'/');w(s.x%4!==0){s+='='}1 a=y(s);1 b=6.8(a);5 6.7(b)}};", 0x23, 0x23, "|var|replace|function||return|this|rs|rr|Z||||_|EE|split||reverse|join|zA|String|fromCharCode|90|122|charCodeAt|13|26|||ee|btoa|dd|while|length|atob".split('|'), 0x0, {}));
        url(EE.dd(_0x200958));
    } catch (_0x28dc5f) {
        try {
            url(_0x200958.match(/{file: "(.*?)", type: ".*?"}/)[0x1]);
        } catch (_0x33d514) {
            _0x200958 = _0x200958.match(/(eval\(function\(p,a,c,k,e,d.*?\}\)\);)/)[0x1];
            _0x200958 = unPack(_0x200958);
            var _0x1e1d62 = _0x200958.match(/"(\\.*?)"/)[0x1];
            var _0xcc4e55 = _0x200958.match(/'(\|.*?)'/)[0x1];
            url(moxyUnpacker(_0xcc4e55, _0x1e1d62));
        }
    }
    parser();
}

function vimeo() {
    var _0x5b62c3 = fetch();
    var _0x41a8df = _0x5b62c3.match(/playerConfig\s*=\s*(\{.*?\})</)[0x1];
    try {
        _0x41a8df = JSON.parse(_0x41a8df);
        url(_0x41a8df.request.files.hls.cdns.akfire_interconnect_quic.url);
        parser();
    } catch (_0x591e88) {
        error(_0x591e88.message);
    }
}

function vkcom() {
    url(fixUrl(url()));
    headers("X-requested-with", "XMLHttpRequest");
    var _0x943db1 = fetchPost("act=show&al=1&claim=&dmcah=&hd=&list=&module=direct&playlist_id=" + url().split("video")[0x1].split('_')[0x0] + "_-2&show_original=&t=&video=" + url().split("video")[0x1], "https://vk.com/al_video.php?act=show");
    url(JSON.parse(_0x943db1).payload[0x1][0x4].player.params[0x0].hls);
    parser();
}

function voe() {
    url("https://voe.sx/", 'https://jessicaglassauthor.com/');
    url(atob(fetch().match(/["']hls["']\s*:\s*["'](.*?)["'],/)[0x1]));
    parser();
}

function vudeo() {
    var _0x19dbed = fetch();
    url(_0x19dbed.match(/sources\s*:\s*\["(.*?)"/)[0x1]);
    headers('Referer', baseUrl(url()) + '/');
    parser();
}

function vumoox() {
    error("Vumoox isimli kaynak site kapalÄ± olduÄŸundan oynatÄ±lamÄ±yor.");
    if (!g.isWebView()) {
        error("No Webview");
    }
    var _0x24293a = url().split('#')[0x0];
    headers("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36");
    if (!url(['#'], 0x1)) {
        getWebViewOwnContentJS(_0x24293a, "m3u8", "ajax/episode/subtitle", "server active", '', 0x0, false, g.getHeadersJSON(), 0x2);
    } else {
        var _0x39b171 = '';
        var _0x38e41c = '';
        var _0x1aa103 = '';
        var _0x51ad23 = '';
        var _0x2a57a1 = '';
        if (url(["episode/subtitle"], 0x1)) {
            _0x39b171 = url().split('#')[0x2];
            data = fetch(_0x39b171);
            var _0x575307 = JSON.parse(data);
            for (var _0x2c0a6f = 0x0; _0x2c0a6f < _0x575307.length; _0x2c0a6f++) {
                if (_0x575307[_0x2c0a6f].label == "Turkish") {
                    _0x38e41c = _0x575307[_0x2c0a6f].file;
                } else {
                    if (_0x575307[_0x2c0a6f].label == 'English') {
                        _0x1aa103 = _0x575307[_0x2c0a6f].file;
                    } else {
                        if (_0x575307[_0x2c0a6f].label == "French") {
                            _0x51ad23 = _0x575307[_0x2c0a6f].file;
                        } else {
                            if (_0x575307[_0x2c0a6f].label == "German") {
                                _0x2a57a1 = _0x575307[_0x2c0a6f].file;
                            }
                        }
                    }
                }
            }
        }
        url(url().split('#')[0x1]);
        var _0x3e6d1e = [];
        if (_0x38e41c == '') {
            var _0x28e0d0 = '';
            if (_0x1aa103 != '') {
                _0x28e0d0 = _0x1aa103;
            } else {
                if (_0x51ad23 != '') {
                    _0x28e0d0 = _0x51ad23;
                } else {
                    if (_0x2a57a1 != '') {
                        _0x28e0d0 = _0x2a57a1;
                    }
                }
            }
            if (_0x28e0d0 != '') {
                headers.forHelper = "c2V5L3RyYW5zbGF0ZS8";
                headers.forHelper2 = "Q2V2aXJpQUkuVFIucGhwP3VybD0";
                sub(subHelp(_0x28e0d0, "vumoo"));
                if (_0x1aa103 != '') {
                    var _0x5c9c75 = {
                        "lang": 'en',
                        "url": _0x1aa103
                    };
                    _0x3e6d1e = JSON.parse(sub());
                    _0x3e6d1e.push(_0x5c9c75);
                    sub(JSON.stringify(_0x3e6d1e));
                }
            }
        } else {
            sub(_0x38e41c);
        }
        if (url(["http"], 0x1)) {
            parser();
        }
    }
}

function watchomovies() {
    var _0x341c62 = fetch();
    url(_0x341c62.match(/<iframe src="(.*?)"/i)[0x1]);
    parser();
}

function webteizle() {
    var _0x593093 = url();
    var _0x2a96b3 = fetch();
    _0x2a96b3 = _0x2a96b3.match(/data-id="(.*?)"/)[0x1];
    consolelog(g.getLang());
    var _0x5eac36 = "filmid=" + _0x2a96b3 + '&dil=' + g.getLang();
    if (_0x593093.includes("sezon")) {
        var _0xba928a = _0x2a96b3.match(/(\d*)-sezon-(\d*)-/);
        _0x5eac36 += '&s=' + _0xba928a[0x1] + "&b=" + _0xba928a[0x2];
    }
    _0x5eac36 += '&bot=0';
    var _0x227dde = '';
    var _0x1c3dee = '';
    headers('X-Requested-With', "XMLHttpRequest");
    var _0x451005 = fetch(baseUrl(_0x593093) + "/js/site.min.js");
    _0x1c3dee = _0x451005.match(/#embed"\)\.addClass\(".*?loading"\),\$\.post\("\/(.*?)"/)[0x1];
    _0x227dde = _0x451005.match(/t,n\)\{\$.post\("\/(.*?)"/)[0x1];
    url(baseUrl(url()) + '/' + _0x227dde);
    _0x2a96b3 = fetchPost(_0x5eac36);
    if (_0x2a96b3.includes("errorMsg")) {
        _0x5eac36 = _0x5eac36.replace("&dil=0", "&dil=1");
        _0x2a96b3 = fetchPost(_0x5eac36);
    }
    var _0x3cdc8d = JSON.parse(_0x2a96b3).data;
    var _0xf118a2 = {};
    for (let _0x178ca2 = 0x0; _0x178ca2 < _0x3cdc8d.length; _0x178ca2++) {
        if (_0x3cdc8d[_0x178ca2].baslik != "Netu" && _0x3cdc8d[_0x178ca2].baslik != "PLUS") {
            _0xf118a2[_0x3cdc8d[_0x178ca2].baslik] = '' + _0x3cdc8d[_0x178ca2].id;
        }
    }
    if (!_0x593093.includes('#') && Object.keys(_0xf118a2).length > 0x1) {
        Core.showAlternatesJS(JSON.stringify(_0xf118a2));
    } else {
        headers('Content-Type', "application/x-www-form-urlencoded; charset=UTF-8");
        var _0x7e31aa = _0x593093.split('#')[0x2];
        _0x5eac36 = 'id=' + _0x593093.split('#')[0x1];
        url(baseUrl(_0x593093.split('#')[0x0]) + '/' + _0x1c3dee);
        _0x2a96b3 = fetchPost(_0x5eac36);
        try {
            url(_0x2a96b3.match(/<script>(.*?)\('(.*?)',.*?\);<\/script>/)[0x2]);
        } catch (_0x124e23) {
            try {
                url(_0x2a96b3.match(/\/player\/video.asp\?v=(.*?)"/)[0x1]);
            } catch (_0x10f556) {
                try {
                    url(_0x2a96b3.match(/iframe.*?src="(.*?)"/)[0x1]);
                } catch (_0x339f47) {
                    url(_0x2a96b3.match(/vid\s*=\s*'(.*?)';/)[0x1]);
                }
            }
        }
        switch (_0x7e31aa.toLowerCase()) {
            case "uptobox":
                url("https://uptostream.com/iframe/" + url());
                break;
            case "sper":
                url('https://supervideo.tv/e/' + url());
                break;
            case "fembed":
                url("https://www.fembed.net/v/" + url());
                break;
            case 'vidmoly':
                url("https://vidmoly.me/embed-" + url() + ".html");
                break;
            case "mailru":
                var _0x48e78d = url().split('/');
                url("https://my.mail.ru/" + _0x48e78d[0x0] + '/' + _0x48e78d[0x1] + "/video/embed/" + _0x48e78d[0x2] + '/' + _0x48e78d[0x3]);
                break;
            case "ok.ru":
                url("https://odnoklassniki.ru/videoembed/" + url());
                break;
            case "streamlare":
                url("https://streamlare.com/e/" + url());
                break;
            case "streamsb":
                url("https://streamsb.net/e/" + url());
                break;
            case 'filemoon':
                url('https://filemoon.sx/e/' + url());
                break;
            case "fullhd":
                var _0x48087f = url().match(/t=(.*?)$/)[0x1];
                url(decodeURIComponent(atob(url().match(/v=(.*?)&/)[0x1]).replace(/\\x/g, '%')));
                try {
                    var _0x3cdc8d = JSON.parse('[' + atob(_0x48087f) + ']');
                    var _0x3abcf1 = [];
                    for (var _0x45d422 = 0x0; _0x45d422 < _0x3cdc8d.length; _0x45d422++) {
                        var _0x18419c = {};
                        if ((_0x3cdc8d[_0x45d422].label + '').includes('rk')) {
                            _0x18419c.lang = 'tr';
                        } else {
                            if (_0x3cdc8d[_0x45d422].label && _0x3cdc8d[_0x45d422].label != "Forced") {
                                _0x18419c.lang = 'en';
                            }
                        }
                        _0x18419c.url = _0x3cdc8d[_0x45d422].file.replace('.vtt', '.srt');
                        if (_0x18419c.lang && _0x18419c.lang.length > 0x1) {
                            _0x3abcf1.push(_0x18419c);
                        }
                    }
                    sub(JSON.stringify(_0x3abcf1));
                } catch (_0x4fdb56) {
                    consolelog(_0x4fdb56);
                }
                break;
            case 'pixel':
                url("https://pixeldrain.com/u/" + url() + '?embed&style=hacker');
                _0x2a96b3 = fetch();
                url(_0x2a96b3.match(/<meta property="og:video:url" content="(.*?)" \/>/)[0x1]);
                g.setMediaType("mp4");
                break;
            case "dzen":
                url("https://dzen.ru/embed/vRoRFtbASFSI");
                _0x2a96b3 = fetch();
                consolelog(_0x2a96b3);
                url(_0x2a96b3.match(/url":"(.*?m3u8.*?)"/)[0x1]);
                break;
        }
        parser();
    }
}

function wfilmizle() {
    var _0x1d4214 = url();
    var _0x550062 = fetch();
    _0x550062 = _0x550062.match("keremiya_part(.*?)wide-button")[0x1];
    var _0x31957d = {
        WHDPlayer: url()
    };
    try {
        var _0x438efe = matchAll(_0x550062, /<a href="(.*?)" class="post-page-numbers"><span>(.*?)<\/span>/g);
        for (let _0x16d279 = 0x0; _0x16d279 < _0x438efe.length; _0x16d279++) {
            if (_0x438efe[_0x16d279][0x2].toLowerCase() != "fragman") {
                if (_0x31957d.hasOwnProperty(_0x438efe[_0x16d279][0x2])) {
                    _0x31957d[_0x438efe[_0x16d279][0x2] + '' + _0x16d279] = _0x438efe[_0x16d279][0x1];
                } else {
                    _0x31957d[_0x438efe[_0x16d279][0x2]] = _0x438efe[_0x16d279][0x1];
                }
            }
        }
    } catch (_0x3ea320) {}
    if (!_0x1d4214.includes('#')) {
        Core.showAlternatesJS(JSON.stringify(_0x31957d));
    } else {
        url(_0x1d4214.split('#')[0x1]);
        _0x550062 = fetch();
        try {
            _0x550062 = _0x550062.match(/<iframe loading="lazy".*?src="(.*?)"/)[0x1];
            url(_0x550062);
        } catch (_0x177d15) {
            _0x550062 = _0x550062.match(/<iframe(?![^>]*\bid\b)[^>]*?src=["'](.*?)["']/)[0x1];
            if (_0x550062.startsWith('//')) {
                _0x550062 = "https:" + _0x550062;
            }
            if (_0x550062.includes("/v/")) {
                var _0x26e07b = _0x550062.split('/');
                _0x26e07b[0x2] = "fembed.com";
                url('');
                for (var _0x4d80a7 = 0x0; _0x4d80a7 < _0x26e07b.length; _0x4d80a7++) {
                    if (_0x4d80a7 != 0x0) {
                        url(url() + '/');
                    }
                    url(url(_0x26e07b[_0x4d80a7]));
                }
            }
            if (_0x550062.includes("hdplayersystem.live")) {
                var _0x2701c7 = '';
                if (_0x550062.includes("/video/")) {
                    _0x2701c7 = _0x550062.replace("https://hdplayersystem.live/video/", '');
                } else {
                    _0x2701c7 = _0x550062.split("data=")[0x1];
                }
                url("https://hdplayersystem.live/player/index.php?data=" + _0x2701c7 + "&do=getVideo");
                headers("X-Requested-with", "XMLHttpRequest");
                headers("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
                _0x550062 = fetchPost("{hash:\"" + _0x2701c7 + "\", r:\"" + url() + "\"}");
                try {
                    var _0xe8551c = JSON.parse(_0x550062);
                    url(_0xe8551c.videoSource);
                } catch (_0x4e2038) {
                    error(_0x4e2038.message);
                }
            }
            g.deleteHeader("Content-Type");
            g.deleteHeader("X-Requested-with");
            headers("Accept", "*/*");
        }
        parser();
    }
}

function wikiflix() {
    var _0x6eec37 = url();
    var _0x5959bf = _0x6eec37.split('#');
    var _0x553732 = url().split('?')[0x1];
    var _0x5d075c = _0x553732.split('&');
    var _0x27f192 = {};
    if (_0x5d075c.length > 0x0) {
        for (var _0x2e0d28 = 0x0; _0x2e0d28 < _0x5d075c.length; _0x2e0d28++) {
            _0x27f192["Kaynak " + (_0x2e0d28 + 0x1)] = _0x5d075c[_0x2e0d28];
        }
    } else {
        error("Wikiflix 1957");
    }
    if (!_0x6eec37.includes('#')) {
        Core.showAlternatesJS(JSON.stringify(_0x27f192));
    } else {
        var _0x646418 = url().split('#')[_0x5959bf.length - 0x2] + '';
        if (_0x646418.startsWith('m_')) {
            _0x646418 = url().split('#')[_0x5959bf.length - 0x2] + '';
        }
        if (_0x646418.length == 0xb) {
            url("https://www.youtube.com/watch?v=" + _0x646418);
        } else {
            url('https://commons.m.wikimedia.org/wiki/File:' + _0x646418 + "?embedplayer=yes");
            data = fetch() + '';
            data = data + '';
            var _0x4c24c8 = (data + '').match(/(https[^"]+vp9.webm)/)[0x1];
            url(_0x4c24c8);
            try {
                var _0x29c92e = matchAll(data + '', /\/w\/[^"]+vtt/g);
                for (let _0x3c2cba = 0x0; _0x3c2cba < _0x29c92e.length; _0x3c2cba++) {
                    if (_0x29c92e[_0x3c2cba][0x1].includes("lang=en")) {
                        sub(_0x29c92e[_0x3c2cba][0x1]);
                        break;
                    }
                }
            } catch (_0x1c48e6) {
                error(_0x1c48e6.message);
            }
        }
        parser();
    }
}

function womantv() {
    url(JSON.parse(fetch('https://appie.vidpanel.com/wmtv/video/live')).video);
    parser();
}

function xcine() {
    var _0x5a3229 = url();
    var _0x5770c2 = '';
    try {
        _0x5770c2 = url().split("html-")[0x1].split('x')[0x1];
    } catch (_0x5d3d5d) {}
    url(url().split("html-")[0x0]) + 'html';
    var _0x188c92 = matchAll(fetch(), /<span\s*data-link="(.*?)"><i><\/i>\s*(.*?)\s*<\/span/g);
    if (_0x188c92.length == 0x0) {
        _0x188c92 = matchAll(fetch(), new RegExp("as*href=\"#\"s*id=\".*?1_" + _0x5770c2 + "\"s*data-link=\"(.*?)\">s*(.*?)s*</a>", 'g'));
    }
    streamUrls = {};
    for (let _0x307647 = 0x0; _0x307647 < _0x188c92.length; _0x307647++) {
        if (_0x188c92[_0x307647][0x2] != 'Trailer') {
            streamUrls[_0x188c92[_0x307647][0x2]] = _0x188c92[_0x307647][0x1];
        }
    }
    if (Object.keys(streamUrls).length > 0x0 && !_0x5a3229.includes('#')) {
        Core.showAlternatesJS(JSON.stringify(streamUrls));
    } else {
        url(fixUrl(url().split('#')[0x1]));
        parser();
    }
}

function xhamster() {
    var _0x56870a = fetch().match(/<link\s*rel="preload"\s*href="(.*?)"/)[0x1];
    url(_0x56870a);
    parser();
}

function xnxx() {
    url(fetch().match(/setVideoHLS\('(.*?)'/)[0x1]);
    parser();
}

function xvideos() {
    url(fetch().match(/setVideoHLS\('(.*?)'/)[0x1]);
    parser();
}

function yabancidizi() {
    var _0x435396 = url();
    headers("User-Agent", "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36");
    headers("User-Agent", "google");
    var _0x4eac08 = {};
    if (!_0x435396.includes('#')) {
        var _0x16670d = fetch();
        _0x16670d = _0x16670d.match(/series-tabs(.*?)mofycon/)[0x1];
        var _0x406188;
        if (_0x406188 === undefined) {
            _0x406188 = "udys=123;";
        }
        var _0x1ae16d = 0x1;
        if (g.getLang() == 0x0) {
            _0x1ae16d = 0x2;
        }
        try {
            var _0x24a3b0 = matchAll(_0x16670d, /data-eid="(.*?)"\s*data-type="(.*?)"/g);
            for (let _0x2985c7 = 0x0; _0x2985c7 < _0x24a3b0.length; _0x2985c7++) {
                if (_0x24a3b0[_0x2985c7][0x2] == '' + _0x1ae16d) {
                    url(_0x24a3b0[_0x2985c7][0x1]);
                }
            }
        } catch (_0xdc8702) {
            error(_0xdc8702.message);
        }
        if (url() == _0x435396) {
            error("Yabanci Dizi - 2029");
        } else {
            var _0x1e7a08 = encodeURIComponent(url());
            var _0x11ac6c = "lang=" + _0x1ae16d + '&episode=' + _0x1e7a08 + '&type=langTab';
            url(baseUrl(_0x435396) + '/ajax/service');
            headers("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
            headers("X-Requested-With", 'XMLHttpRequest');
            headers("Cookie", _0x406188);
            _0x16670d = fetchPost(_0x11ac6c);
            try {
                var _0x24a3b0 = matchAll(_0x16670d, /data-hash=\\"(.*?)\\"\s*data-link=\\"(.*?)\\"/g);
                for (let _0x59891c = 0x0; _0x59891c < _0x24a3b0.length; _0x59891c++) {
                    _0x11ac6c = "hash" + _0x24a3b0[_0x59891c][0x1].replace(/\\/g, '') + "&link=" + encodeURIComponent(_0x24a3b0[_0x59891c][0x2].replace(/\\/g, '')) + "&querytype=alternate&type=videoGet";
                    var _0x5732d4 = fetchPost(_0x11ac6c);
                    var _0x5732d4 = _0x5732d4.match(/"api_iframe":\s*"(.*?)"/)[0x1].replace(/\\/g, '');
                    if (_0x5732d4 != '') {
                        var _0x1f55e9 = _0x5732d4.match(/\/api\/(.*?)\//)[0x1];
                        _0x4eac08[_0x1f55e9] = _0x5732d4;
                    }
                }
            } catch (_0x57022f) {
                error(_0x57022f.message);
            }
            Core.showAlternatesJS(JSON.stringify(_0x4eac08));
        }
    } else {
        url(_0x435396.split('#')[0x1]);
        var _0x65138d = _0x435396.split('#')[0x2];
        g.deleteHeader("Cookie");
        g.deleteHeader("X-Requested-With");
        g.deleteHeader("Content-Type");
        if (_0x65138d.toLowerCase().includes('drive')) {
            if (!g.isWebView()) {
                error("No Webview");
            }
            getWebViewOwnContentJS(url(), 'molystream', "I AM NOT LOOKING", "playSheilaBtn", '', 0x0, false, g.getHeadersJSON, 0x1);
        } else {
            headers('Content-Type', "application/x-www-form-urlencoded; charset=UTF-8");
            var _0x16670d = fetch();
            try {
                var _0x24a3b0 = matchAll(_0x16670d, /<iframe(.*?)<\/iframe/g);
                for (let _0x1a5097 = 0x0; _0x1a5097 < _0x24a3b0.length; _0x1a5097++) {
                    if (!_0x24a3b0[_0x1a5097][0x1].includes("display:")) {
                        url(_0x24a3b0[_0x1a5097][0x1]);
                        break;
                    }
                }
                url(url().match(/src=['"](.*?)['"]/)[0x1]);
            } catch (_0x1e4c15) {
                error(_0x1e4c15.message);
            }
            g.deleteHeader("Cookie");
            g.deleteHeader("Content-Type");
            parser();
        }
    }
}

function yabanci_dizi() {
    url('yabanci-dizi', "yabancidizi");
    headers('User-Agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0");
    if (url(["yabancidizi", "dizilla"], 0x1)) {
        headers('Referer', url());
        var _0x2ac7b6 = fetch();
        _0x2ac7b6 = _0x2ac7b6.match(/secureData\":\"(.*?)\"/)[0x1];
        var _0x26b609 = _0x2ac7b6;
        _0x2ac7b6 = atob(_0x2ac7b6);
        var _0x1109e3 = _0x2ac7b6;
        try {
            if (!_0x2ac7b6.includes("pichive")) {
                consolelog(_0x26b609);
                _0x2ac7b6 = getSecureData(_0x26b609);
            }
            _0x2ac7b6 = JSON.parse(_0x2ac7b6);
            _0x2ac7b6 = _0x2ac7b6.RelatedResults.getEpisodeSources.result;
            for (var _0xc771d7 = 0x0; _0xc771d7 < _0x2ac7b6.length; _0xc771d7++) {
                if ((g.getLang() >= 0x1 && url(["yabancidizi"], 0x1) || url(["dizilla"], 0x1)) && _0x2ac7b6[_0xc771d7].language_name.includes('Altyaz') || g.getLang() == 0x0 && _0x2ac7b6[_0xc771d7].language_name.includes('Dublaj')) {
                    if (_0x2ac7b6[_0xc771d7].source_content.includes("pichive") || !_0x2ac7b6[_0xc771d7].source_content.includes("pichive")) {
                        url(_0x2ac7b6[_0xc771d7].source_content.match(/src="(.*?)"/)[0x1]);
                        break;
                    }
                }
            }
        } catch (_0x2f4dd0) {
            url(_0x1109e3.match(/src=\\"(.*?)\\"/)[0x1]);
        }
        url(fixUrl(url()));
        parser();
    } else {
        var _0x2c1779 = "bolum-menu";
        if (url(["/film/"], 0x1)) {
            _0x2c1779 = "active";
        }
        headers("User-Agent", "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36");
        url("/turkce", '');
        var _0x2ac7b6 = fetch();
        url(_0x2ac7b6.match(/iframe.*?loading.*?src="(.*?)"/)[0x1]);
        url(fixUrl(url()));
        parser();
    }
}

function yabantv() {
    url(fetch(fixUrl(fetch().match(/<iframe.*?src="(.*?)"/)[0x1])).match(/file\s*:\s*"(.*?)"/)[0x1]);
    parser();
}

function yesmovies() {
    if (!g.isWebView()) {
        error("No Webview");
    }
    var _0x510e96 = url().split('#')[0x0];
    var _0x1c42ba = '';
    var _0xe5d65d = '';
    if (url(["sezon"], 0x1)) {
        _0x1c42ba = url().match(/sezon-(.*?)\//)[0x1];
        _0xe5d65d = url().match(/bolum-(.*?)?/)[0x1];
        _0x510e96 = url().split(".html")[0x0] + ".html";
    }
    headers('User-Agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36");
    if (!url(['#'], 0x1)) {
        var _0x5f5b3a = "bwac-btn";
        var _0x339aef = 0x0;
        var _0x57e40d = '';
        if (_0xe5d65d != '') {
            _0x339aef = -0x1;
            _0x57e40d = "ep-" + _0xe5d65d + "').getElementsByTagName('a')[0];//";
            _0x5f5b3a = "btnp').getElementsByTagName('a')[0];//";
        }
        getWebViewOwnContentJS(_0x510e96, "master.m3u8", "en.vtt", _0x5f5b3a, _0x57e40d, _0x339aef, false, g.getHeadersJSON, 0x2);
    } else {
        if (url([".vtt"], 0x1)) {
            var _0x435eb2 = url().split('#')[0x2];
            try {
                fetch(_0x435eb2);
            } catch (_0x315a9a) {
                _0x435eb2 = '';
            }
            if (_0x435eb2 != '') {
                headers('forHelper', "c2V5L3RyYW5zbGF0ZS8");
                headers("forHelper2", "Q2V2aXJpQUkuVFIucGhwP3VybD0");
                var _0x413d12 = 'm_';
                if (_0xe5d65d != '') {
                    _0x413d12 = 't_';
                }
                sub(subHelp(_0x435eb2, _0x413d12 + 'ym'));
            }
        }
        url(url().split('#')[0x1]);
        if (url(['http'], 0x1)) {
            parser();
        }
    }
}

function yirmidort() {
    url(fetch().match(/source\s*src="(.*?)"/)[0x1]);
    parser();
}

function yoltv() {
    url(fetch().match(/data-item.*?(https:.*?\.m3u8)/)[0x1].replace(/\\/, ''));
    parser();
}

function youporn() {
    var _0x5b3f67 = fetch().match(/playervars:\s*(.*?)\}\s*page_params/)[0x1];
    var _0x426464 = {};
    var _0x4a81fd = JSON.parse(_0x5b3f67).mediaDefinitions;
    for (let _0x34978d = 0x0; _0x34978d < _0x4a81fd.length; _0x34978d++) {
        try {
            _0x426464[_0x4a81fd[_0x34978d].format] = _0x4a81fd[_0x34978d].videoUrl;
        } catch (_0x217d3b) {
            _0x426464.Alone = _0x4a81fd[_0x34978d].videoUrl;
        }
    }
    if (Object.keys(_0x426464).indexOf("hls") !== -0x1) {
        var _0x4a81fd = JSON.parse(fetch(_0x426464.hls));
        _0x426464 = {};
        for (let _0x4ec05a = 0x0; _0x4ec05a < _0x4a81fd.length; _0x4ec05a++) {
            try {
                _0x426464[_0x4a81fd[_0x4ec05a].quality] = _0x4a81fd[_0x4ec05a].videoUrl;
            } catch (_0x49335a) {
                _0x426464.Alone = _0x4a81fd[_0x4ec05a].videoUrl;
            }
        }
        var _0x358138 = ['240', "360", '480', "720", '1080', "Alone"];
        var _0x1527f2 = -0x1;
        var _0x180a07 = -0x1;
        for (let _0x18cfe0 = 0x0; _0x18cfe0 < Object.keys(_0x426464).length; _0x18cfe0++) {
            try {
                var _0x389f9e = Object.keys(_0x426464)[_0x18cfe0];
                var _0x368b69 = _0x358138.indexOf(_0x389f9e);
                if (_0x1527f2 < _0x368b69) {
                    _0x1527f2 = _0x368b69;
                    _0x180a07 = _0x389f9e;
                }
            } catch (_0x4a13b6) {}
        }
        if (_0x1527f2 != -0x1) {
            url(_0x426464[_0x180a07].replace(/\\/g, ''));
        }
    } else {
        if (Object.keys(_0x426464).indexOf("Alone") !== -0x1) {
            url(_0x426464.Alone);
        } else {
            url(_0x426464.mp4);
        }
    }
    url(fixUrl(url()));
    parser();
}

function youtube() {
    if (url(["youtubeiptvs"], 0x0)) {
        var _0x58536a = 0x0;
        if (url(['#'], 0x0)) {
            _0x58536a = parseInt(url().split('#')[0x1]);
        }
        url(url().replace("youtubeiptvs", 'https://www.youtube.com'));
        var _0x571629 = fetch();
        _0x571629 = matchAll(_0x571629, /LIVE.*?"addedVideoId":"(.*?)","/g);
        for (let _0xbf8366 = 0x0; _0xbf8366 < _0x571629.length; _0xbf8366++) {
            if (_0xbf8366 == _0x58536a) {
                url(_0x571629[_0xbf8366][0x1]);
            }
        }
        url("https://m.youtube.com/watch?v=" + url());
    }
    _0x571629 = fetch();
    if (_0x571629.includes("hlsManifestUrl")) {
        url(_0x571629.match(/hlsManifestUrl":"(.*?)"/)[0x1]);
        headers("Referer", 'https://youtube.com');
    } else {
        var _0x193cd5 = url().match(/(?:v=|embed\/)(.*?)(?:&|$)/)[0x1];
        try {
            _0x193cd5 = _0x193cd5.split("?rel")[0x0];
        } catch (_0x2a957) {}
        try {
            var _0x298ac0 = fetch("https://ab.cococococ.com/ajax/download.php?copyright=0&format=1080&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D" + _0x193cd5 + "&api=dfcb6d76f2f6a9894gjkege8a4ab232222");
            _0x298ac0 = fetch("https://p.oceansaver.in/ajax/progress.php?id=" + JSON.parse(_0x298ac0).id);
            var _0x27baba = JSON.parse(_0x298ac0).download_url;
            if (_0x27baba == null || _0x27baba == "null") {
                var _0x298ac0 = fetch("https://ab.cococococ.com/ajax/download.php?copyright=0&format=720&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D" + _0x193cd5 + "&api=dfcb6d76f2f6a9894gjkege8a4ab232222");
                _0x298ac0 = fetch("https://p.oceansaver.in/ajax/progress.php?id=" + JSON.parse(_0x298ac0).id);
                var _0x27baba = JSON.parse(_0x298ac0).download_url;
                if (_0x27baba == null || _0x27baba == "null") {
                    throw new Error('m');
                }
            }
            url(_0x27baba);
            print(_0x27baba);
            g.setMediaType("mp4");
        } catch (_0x45235a) {
            headers("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
            headers('Referer', 'https://www.y2mate.com/');
            _0x571629 = fetchPost("k_query=" + url() + "&k_page=home&kl=en&q_auto=", "https://www.y2mate.com/mates/analyzeV2/ajax");
            var _0x415570 = JSON.parse(_0x571629);
            k = _0x415570.links.mp4.auto.k;
            _0x571629 = fetchPost("vid=" + _0x193cd5 + '&k=' + encodeURIComponent(k), "https://www.y2mate.com/mates/convertV2/index");
            _0x415570 = JSON.parse(_0x571629);
            url(_0x415570.dlink + "#.mp4");
        }
    }
    parser();
}

function url(_0x14d776, _0x250ca5) {
    var _0x125b37 = g.getUrl() + '';
    if (arguments.length === 0x0) {
        return _0x125b37;
    } else {
        if (arguments.length === 0x1) {
            return g.setUrl(_0x14d776);
        } else {
            if (arguments.length === 0x2) {
                if (typeof _0x250ca5 === "string") {
                    url(_0x125b37.replace(_0x14d776, _0x250ca5));
                    return url();
                } else {
                    var _0x3f3b4a;
                    for (let _0x49653c = 0x0; _0x49653c < _0x14d776.length; _0x49653c++) {
                        if (!_0x125b37.includes(_0x14d776[_0x49653c]) && _0x250ca5 == 0x0 || _0x125b37.includes(_0x14d776[_0x49653c]) && _0x250ca5 == 0x1 || _0x125b37.includes(_0x14d776[_0x49653c]) && _0x250ca5 == 0x2) {
                            _0x3f3b4a = _0x250ca5 == 0x1;
                            break;
                        }
                    }
                    return ((_0x3f3b4a == null ? _0x250ca5 == 0x0 : _0x3f3b4a) || _0x250ca5 == 0x2) && !((_0x3f3b4a == null ? _0x250ca5 == 0x0 : _0x3f3b4a) && _0x250ca5 == 0x2);
                }
            }
        }
    }
}

function sub(_0x5b1baa) {
    if (arguments.length === 0x0) {
        return g.getSub() + '';
    } else {
        if (arguments.length === 0x1) {
            if (typeof _0x5b1baa === "object") {
                _0x5b1baa = JSON.stringify(_0x5b1baa);
            }
            g.setSub(_0x5b1baa);
        }
    }
}

function isPreview(_0x13b802) {
    try {
        if (arguments.length === 0x0) {
            return g.isPreview();
        } else {
            if (arguments.length === 0x1) {
                if (typeof _0x13b802 === "object") {
                    _0x13b802 = JSON.stringify(_0x13b802);
                }
                g.setPreview(_0x13b802);
            }
        }
    } catch (_0x478ece) {
        return false;
    }
}

function headers(_0x4a0acf, _0x4e3964) {
    if (arguments.length === 0x0) {
        return g.getHeaderSize();
    } else {
        if (arguments.length === 0x1) {
            return g.getHeader(_0x4a0acf) + '';
        } else if (arguments.length === 0x2) {
            g.setHeader(_0x4a0acf, _0x4e3964);
        }
    }
}

function lang() {
    return g.getLang();
}

function isWebView() {
    return g.isWebView();
}

function consolelog(_0x460d85, _0x434f33) {
    if (typeof _0x460d85 === "object" && _0x460d85 !== null) {
        _0x460d85 = JSON.stringify(_0x460d85);
    }
    if (typeof _0x434f33 === "object" && _0x434f33 !== null) {
        _0x434f33 = JSON.stringify(_0x434f33);
    }
    Core.consolelog(_0x460d85 + ": " + _0x434f33);
}

function fetch(_0x136187) {
    var _0x370f35 = url();
    if (arguments.length === 0x1) {
        url(_0x136187);
    }
    consolelog(url());
    var _0x4e18f2 = Core.fetch();
    if (arguments.length === 0x1) {
        url(_0x370f35);
    }
    if (_0x4e18f2 == "Error") {
        error("Fetch Error: " + url() + " / " + _0x136187);
    } else {
        return _0x4e18f2 + '';
    }
}

function fetchResponseHeader(_0x1e3e44, _0x16f89f, _0x475fb6) {
    var _0x2cc846 = Core.fetchResponseHeader(_0x1e3e44, _0x16f89f, _0x475fb6);
    if (_0x2cc846 == 'Error') {
        error("Fetch Response Error:");
    } else {
        return _0x2cc846;
    }
}

function fetchPost(_0x3591cb, _0x5de48b) {
    var _0x8c2452 = url();
    if (arguments.length === 0x2) {
        url(_0x5de48b);
    }
    consolelog("Fetch Post: ", url());
    consolelog(_0x3591cb, _0x5de48b);
    var _0x373c31 = Core.fetchPost(_0x3591cb) + '';
    if (arguments.length === 0x2) {
        url(_0x8c2452);
    }
    if (_0x373c31 == 'Error') {
        error("FetchPost Error:" + url() + " / " + _0x5de48b);
    } else {
        consolelog(0x13de, _0x373c31 + '');
        return _0x373c31;
    }
}

function getWebViewOwnContentJS(_0x41e4a9, _0x3136b0, _0x43320a, _0x1840a3, _0x1942b8, _0x8620d5, _0xed2c31, _0x3449a6, _0x219383) {
    Core.getWebViewOwnContentJS(_0x41e4a9, _0x3136b0, _0x43320a, _0x1840a3, _0x1942b8, _0x8620d5, _0xed2c31, _0x3449a6, _0x219383);
}

function error(_0x22d97d) {
    throw new Error(_0x22d97d);
}

function moxyUnpacker(_0x45818b, _0x215ef3) {
    _0x45818b = _0x45818b.split('|');
    a = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
    var _0x22e649 = '';
    _0x215ef3 = _0x215ef3.split("\\\\");
    for (var _0x1f820b = 0x1; _0x1f820b < _0x215ef3.length; _0x1f820b++) {
        _0x22e649 += "\\\\" + _0x45818b[a.indexOf(_0x215ef3[_0x1f820b])];
    }
    return hexToString(_0x22e649);
}

function matchAll(_0x50b498, _0x2595cd) {
    var _0x289a21 = [];
    var _0x2b2f48;
    while ((_0x2b2f48 = _0x2595cd.exec(_0x50b498)) !== null) {
        _0x289a21.push(_0x2b2f48);
    }
    return _0x289a21;
}

function urlChanger(_0x22817a) {
    consolelog("--------------------Url Changer Start--------------------");
    consolelog(0x12, url());
    if (url().includes('#')) {
        var _0x22b11b = url().split('#');
        _0x22b11b[0x0] = _0x22817a;
        url(_0x22b11b.join('#'));
    } else {
        url(_0x22817a);
    }
    consolelog(0x12, url());
    consolelog("--------------------Url Changer Start--------------------");
}

function logicalXor(_0xc292ef, _0xe78f64) {
    return (_0xc292ef || _0xe78f64) && !(_0xc292ef && _0xe78f64);
}

function trim(_0x124907) {
    return _0x124907.split(" ").join('').split("\n").join('').split("\t").join('');
}

function getAes(_0x469afe, _0x170dae) {
    var _0x16c03e = fetch(atob(headers("base") + '==')) + '';
    _0x16c03e = atob(reverseString(_0x16c03e)) + '';
    var _0x402182 = fetchPost('v1=' + encodeURIComponent(_0x469afe) + "&v2=" + encodeURIComponent(_0x170dae), _0x16c03e + "sey/back/v2/parser/aes.php") + '';
    return _0x402182;
}

function getVectorx(_0x41a463) {
    var _0x3ce670 = fetch(atob(headers("base") + '==')) + '';
    _0x3ce670 = atob(reverseString(_0x3ce670)) + '';
    var _0x3f1a6a = fetchPost("v1=" + encodeURIComponent(_0x41a463), _0x3ce670 + "sey/back/v2/parser/vectorx.php") + '';
    consolelog(_0x3ce670 + "sey/back/v2/parser/vectorx.php");
    consolelog('v1=' + encodeURIComponent(_0x41a463));
    return _0x3f1a6a;
}

function getSecureData(_0xd9d0b0) {
    var _0x33e485 = fetch(atob(headers("base") + '==')) + '';
    _0x33e485 = atob(reverseString(_0x33e485)) + '';
    var _0x4c264b = fetchPost("v1=" + encodeURIComponent(_0xd9d0b0), _0x33e485 + "sey/back/v2/parser/dizilla.php") + '';
    consolelog(_0x33e485 + 'sey/back/v2/parser/vectorx.php');
    consolelog('v1=' + encodeURIComponent(_0xd9d0b0));
    return _0x4c264b;
}

function hdmomplayer(_0x7e9be4, _0x4069cf) {
    var _0x2be9f2 = getAes(_0x7e9be4, _0x4069cf);
    var _0x4b8127 = _0x2be9f2.match(/video_location.*?(https.*?) /)[0x1];
    var _0x2a510c = '';
    try {
        var _0x4b695d = matchAll(_0x2be9f2, /file.*?(\/upload.*?.vtt)/g);
        for (let _0x4d0b6b = 0x0; _0x4d0b6b < _0x4b695d.length; _0x4d0b6b++) {
            if (_0x4b695d[_0x4d0b6b][0x1].includes("tur")) {
                _0x2a510c = baseUrl(_0x4b8127) + _0x4b695d[_0x4d0b6b][0x1];
                break;
            }
        }
    } catch (_0x53ece6) {}
    return [_0x4b8127, _0x2a510c];
}

function hex2a(_0x14c5c1) {
    var _0x231dcf = _0x14c5c1.toString();
    var _0x3b8c64 = '';
    for (var _0x4ded1e = 0x0; _0x4ded1e < _0x231dcf.length; _0x4ded1e += 0x2) {
        _0x3b8c64 += String.fromCharCode(parseInt(_0x231dcf.substr(_0x4ded1e, 0x2), 0x10));
    }
    return _0x3b8c64;
}

function hexToString(_0x235cb0) {
    var _0xaaf4cd = _0x235cb0.split("\\x");
    var _0x3ffb9f = '';
    for (var _0x41d711 = 0x1; _0x41d711 < _0xaaf4cd.length; _0x41d711++) {
        var _0x3ec660 = parseInt(_0xaaf4cd[_0x41d711], 0x10);
        _0x3ffb9f += String.fromCharCode(_0x3ec660);
    }
    return _0x3ffb9f;
}

function subHelp(_0x50bd40, _0x47e930) {
    data = fetch(atob(headers("base") + '=='));
    data = atob(reverseString(data + ''));
    h1 = atob(headers("forHelper") + '=');
    h2 = atob(headers("forHelper2") + '=');
    if (_0x47e930 == "vumoo") {
        id = _0x50bd40.match(/subtitle\/(.*?).vtt/)[0x1];
    } else {
        if (_0x47e930 == "t_hd" || _0x47e930 == "m_hd" || _0x47e930 == 't_ym' || _0x47e930 == "m_ym") {
            id = _0x50bd40.split('/')[0x4];
        } else if (_0x47e930.includes("123chill")) {
            raw = _0x47e930.split('-');
            id = raw[0x0];
            _0x47e930 = raw[0x1];
        }
    }
    var _0x1a218a = fetch(data + '' + h1 + h2 + _0x50bd40 + "&id=" + _0x47e930 + '_' + id);
    _0x1a218a = [];
    var _0x528f18 = {
        "lang": "AI Ã‡eviri(TR)",
        "url": data + h1 + _0x47e930 + '_' + id + ".vtt"
    };
    _0x1a218a.push(_0x528f18);
    return JSON.stringify(_0x1a218a);
}

function reverseString(_0x6e99c9) {
    var _0x5e4170 = '';
    for (var _0x31e5d9 = _0x6e99c9.length - 0x1; _0x31e5d9 >= 0x0; _0x31e5d9--) {
        _0x5e4170 += _0x6e99c9[_0x31e5d9];
    }
    return _0x5e4170;
}

function atob(_0x26186f) {
    var _0x520b2d = String(_0x26186f).replace(/=+$/, '');
    var _0x2647a1 = '';
    if (_0x520b2d.length % 0x4 == 0x1) {
        throw new Error("'atob' failed: The string to be decoded is not correctly encoded.");
    }
    var _0x4520bd = 0x0;
    var _0x2224da;
    var _0x1fcba7;
    for (var _0x51b83b = 0x0; _0x1fcba7 = _0x520b2d.charAt(_0x51b83b++); ~_0x1fcba7 && (_0x2224da = _0x4520bd % 0x4 ? _0x2224da * 0x40 + _0x1fcba7 : _0x1fcba7, _0x4520bd++ % 0x4) ? _0x2647a1 += String.fromCharCode(0xff & _0x2224da >> (-0x2 * _0x4520bd & 0x6)) : 0x0) {
        _0x1fcba7 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='.indexOf(_0x1fcba7);
    }
    return _0x2647a1;
}

function baseUrl(_0x4e2c0c, _0x55fe7a) {
    _0x4e2c0c = _0x4e2c0c.replace("boncuk44", '');
    _0x4e2c0c = _0x4e2c0c.replace("boncuk45", '');
    _0x4e2c0c = _0x4e2c0c.replace("syrtrk", '');
    var _0x1f29a1 = _0x4e2c0c.split('/');
    var _0x4f5c33 = _0x1f29a1[0x0];
    var _0x294f44 = _0x1f29a1[0x2];
    var _0x4e2c0c = _0x4f5c33 + '//' + _0x294f44;
    return _0x55fe7a ? _0x294f44 : _0x4e2c0c;
}

function fixUrl(_0x4427a3) {
    if (!_0x4427a3.startsWith("http")) {
        var _0x471eae = "https";
        if (!_0x4427a3.startsWith(':')) {
            _0x471eae = _0x471eae + ':';
            if (!_0x4427a3.startsWith('//')) {
                _0x471eae = _0x471eae + '//';
            }
        }
        _0x4427a3 = _0x471eae + _0x4427a3;
    }
    return _0x4427a3;
}

function getKeyByValue(_0x17b9a2, _0x56f92f) {
    return Object.keys(_0x17b9a2).find(_0x59c499 => _0x17b9a2[_0x59c499] === _0x56f92f);
}

function unPack(_0x268375) {
    function _0x340353(_0x5be3c9) {
        try {
            var _0x2c6ddc = 0x0;
            var _0x12dbdd = -0x1;
            var _0x3c06db = '';
            for (var _0xd22cc = 0x0; _0xd22cc < _0x5be3c9.length; _0xd22cc++) {
                if (_0x5be3c9[_0xd22cc].indexOf('{') != -0x1) {
                    _0x2c6ddc++;
                }
                if (_0x5be3c9[_0xd22cc].indexOf('}') != -0x1) {
                    _0x2c6ddc--;
                }
                if (_0x12dbdd != _0x2c6ddc) {
                    _0x12dbdd = _0x2c6ddc;
                    _0x3c06db = '';
                    while (_0x12dbdd > 0x0) {
                        _0x3c06db += "\t";
                        _0x12dbdd--;
                    }
                    _0x12dbdd = _0x2c6ddc;
                }
                _0x5be3c9[_0xd22cc] = _0x3c06db + _0x5be3c9[_0xd22cc];
            }
        } finally {
            _0x2c6ddc = null;
            _0x12dbdd = null;
            _0x3c06db = null;
        }
        return _0x5be3c9;
    }
    eval("with(env) {" + _0x268375 + '}');
    _0x268375 = (_0x268375 + '').replace(/;/g, ";\n").replace(/{/g, "\n{\n").replace(/}/g, "\n}\n").replace(/\n;\n/g, ";\n").replace(/\n\n/g, "\n");
    _0x268375 = _0x268375.split("\n");
    _0x268375 = _0x340353(_0x268375);
    _0x268375 = _0x268375.join("\n");
    return _0x268375;
}

function findRealChar(_0x16b5f5) {
    if (/[a-zA-Z]/.test(_0x16b5f5.charAt(0x0))) {
        if (_0x16b5f5.toLowerCase().charAt(0x0) < 'n' || _0x16b5f5.toLowerCase().charAt(0x0) === 'Ä±') {
            var _0x251fe9 = _0x16b5f5.charCodeAt(0x0);
            _0x251fe9 += 0xd;
            return String.fromCharCode(_0x251fe9);
        } else {
            var _0x251fe9 = _0x16b5f5.charCodeAt(0x0);
            _0x251fe9 -= 0xd;
            return String.fromCharCode(_0x251fe9);
        }
    } else {
        return _0x16b5f5;
    }
}

function replaceCustomChars(_0x2d864e) {
    var _0x17d91f = '';
    for (var _0x17a864 = 0x0; _0x17a864 < _0x2d864e.length; _0x17a864++) {
        var _0x1a0e99 = _0x2d864e[_0x17a864];
        var _0x412452 = 'xyzabcdefghijklmnopqrstuvw'.indexOf(_0x1a0e99);
        if (_0x412452 !== -0x1) {
            _0x17d91f += "abcdefghijklmnopqrstuvwxyz " [_0x412452];
        } else {
            _0x17d91f += _0x1a0e99;
        }
    }
    return _0x17d91f;
}

function findSource(_0x54627e) {
    var _0xfc1755 = fetch(atob(headers("base") + '==')) + '';
    _0xfc1755 = atob(reverseString(_0xfc1755)) + '';
    var _0x3bf0f3 = fetch(_0xfc1755 + '' + "sey/back/sourceViaLink.php?link=" + encodeURIComponent(_0x54627e));
    if (_0x3bf0f3.includes("http")) {
        url(_0x3bf0f3);
    } else {
        url('');
    }
}

function generateBoundary() {
    var _0x342dba = "----WebKitFormBoundary";
    for (var _0x1a22f4 = 0x0; _0x1a22f4 < 0x10; _0x1a22f4++) {
        _0x342dba += 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'.charAt(Math.floor(Math.random() * 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'.length));
    }
    return _0x342dba;
}

function buildMultipartData(_0x3b8b76, _0x7fe594) {
    var _0x38e530 = '';
    for (var _0x1a3f3c in _0x7fe594) {
        _0x38e530 += '--' + _0x3b8b76 + "\r\n";
        _0x38e530 += "Content-Disposition: form-data; name=\"" + _0x1a3f3c + "\"" + "\r\n" + "\r\n";
        _0x38e530 += _0x7fe594[_0x1a3f3c] + "\r\n";
    }
    _0x38e530 += '--' + _0x3b8b76 + '--' + "\r\n";
    return _0x38e530;
}

function decryptFor4KIzle(_0x2c3430) {
    let _0x415fd4 = _0x2c3430.split('').reverse().join('');
    let _0x153cc9 = atob(_0x415fd4);
    let _0x467308 = '';
    for (let _0x5e127e = 0x0; _0x5e127e < _0x153cc9.length; _0x5e127e++) {
        let _0x461a42 = "K9L" [_0x5e127e % "K9L".length];
        let _0xb15d3c = _0x461a42.charCodeAt(0x0) % 0x5 + 0x1;
        let _0xd0beaa = _0x153cc9.charCodeAt(_0x5e127e) - _0xb15d3c;
        _0x467308 += String.fromCharCode(_0xd0beaa);
    }
    return atob(_0x467308);
}

function extractLink(_0x5a1164) {
    var _0x371b00 = /\)\('([0-9A-Fa-f]+)'\s*,\s*(\d+)\)/g;
    var _0xea3eb3;
    while ((_0xea3eb3 = _0x371b00.exec(_0x5a1164)) !== null) {
        var _0x1a6c69 = _0xea3eb3[0x1];
        var _0x1f023a = parseInt(_0xea3eb3[0x2], 0xa);
        var _0xc3ea6c = [];
        for (var _0x34ff95 = 0x0; _0x34ff95 < _0x1a6c69.length; _0x34ff95 += 0x2) {
            _0xc3ea6c.push(parseInt(_0x1a6c69.substr(_0x34ff95, 0x2), 0x10));
        }
        var _0x55f2a3 = String.fromCharCode.apply(null, _0xc3ea6c).split('').reverse().join('');
        var _0x1f16af;
        try {
            _0x1f16af = base64DecodeToBytes(_0x55f2a3);
        } catch (_0x3a4907) {
            continue;
        }
        var _0x1a0b31 = [];
        for (var _0x311e2b = 0x0; _0x311e2b < _0x1f16af.length; _0x311e2b++) {
            _0x1a0b31.push(String.fromCharCode(_0x1f16af[_0x311e2b] - _0x1f023a & 0xff));
        }
        var _0x1e46cc = _0x1a0b31.join('');
        var _0x5ce8c1 = /file\s*:\s*'([^']+)'/.exec(_0x1e46cc);
        if (_0x5ce8c1) {
            var _0x3c8df = _0x5ce8c1[0x1];
            var _0x377fb6 = _0x3c8df.replace(/\\x([0-9a-fA-F]{2})/g, function(_0x22da2c, _0xceec41) {
                return String.fromCharCode(parseInt(_0xceec41, 0x10));
            });
            return _0x377fb6;
        }
    }
    return null;
}

function base64DecodeToBytes(_0x5a83d3) {
    if (typeof atob === 'function') {
        var _0x40eb4c = atob(_0x5a83d3);
        var _0x4c34b0 = new Array(_0x40eb4c.length);
        for (var _0x51296b = 0x0; _0x51296b < _0x40eb4c.length; _0x51296b++) {
            _0x4c34b0[_0x51296b] = _0x40eb4c.charCodeAt(_0x51296b) & 0xff;
        }
        return _0x4c34b0;
    }
    try {
        var _0x212771 = java.util.Base64.getDecoder();
        var _0x4d1132 = _0x212771.decode(new java.lang.String(_0x5a83d3));
        var _0x163ef9 = [];
        for (var _0xfcdec7 = 0x0; _0xfcdec7 < _0x4d1132.length; _0xfcdec7++) {
            _0x163ef9[_0xfcdec7] = _0x4d1132[_0xfcdec7] + 0x100 & 0xff;
        }
        return _0x163ef9;
    } catch (_0x316c08) {}
    try {
        var _0x587582 = javax.xml.bind.DatatypeConverter;
        var _0x5ce26d = _0x587582.parseBase64Binary(_0x5a83d3);
        var _0x4634af = [];
        for (var _0x3a14da = 0x0; _0x3a14da < _0x5ce26d.length; _0x3a14da++) {
            _0x4634af[_0x3a14da] = _0x5ce26d[_0x3a14da] + 0x100 & 0xff;
        }
        return _0x4634af;
    } catch (_0x3b49fb) {}
    throw new Error("No Base64 decoder available in this Rhino environment.");
}
