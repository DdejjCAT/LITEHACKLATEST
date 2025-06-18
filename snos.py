# DECODED BY HYPER X SQUAD >>> TOP 1 
# @decoded_softs
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from colored import cprint 
import os
from pystyle import Anime, Colors, Colorate, Center
sys.stdout.reconfigure(line_buffering=True)

senders = {
'k1839u@mail.ru':'1BjdCeGCNcdsXkSRZibA',
    'r2000m@mail.ru':'mK2CSfCcBYTpWznMUYCj',
    'u200o@mail.ru':'hpXzRhGZbuEmKC6YkkFb',
    'zxcforumgei@mail.ru':'zr8dDwC3wfJ2mf87WFBH',
    'hxjdjdhdhdhdhrhrh@mail.ru':'L79En4jttW74jMfPPmd2',
    'hdhdhdhdheje@mail.ru':'4t0L5F7e1bVbYYnfi0X8',
    'r200y@mail.ru':'wJec5CtZ6cGeM9iRtStY',
    'ristislavchernyagam@bk.ru':'iPsbVY4kBffEzraQUysm',
    'gi2000km@mail.ru':'00aZwUGJtp551XSCgJqg',
    'bh1963hj@mail.ru':'dNbDC9R52hnb9fwM2Pq2',
    'j123i@mail.ru':'ihfjY7TWNDL88JGHCeMK',
    '192hkk@mail.ru':'64NJ7uEUcMkJ7cHxzRp3',
    'f193hj@mail.ru':'r26UzK7GkNJQKYHqwYb7',
    'j183j@mail.ru':'2VndP5kNNnXJthvDF729',
    't183tj@mail.ru':'Z4K8BUiukka1j1WphtJ5',
    'j378j@mail.ru':'ZiW71BFPFEriUi4CENQJ',
    'ik278j@mail.ru':'ayygGXd0BT9bKRBNgtS1',
    'qstkennethadams388@gmail.com':'itpz jkrh mtwp escx',
'usppaullewis171@gmail.com':'lpiy xqwi apmc xzmv',
'ftkgeorgeanderson367@gmail.com':'okut ecjk hstl nucy',
'nieedwardbrown533@gmail.com':'wvig utku ovjk appd',
'h56400139@gmail.com':'byrl egno xguy ksvf',
'den.kotelnikov220@gmail.com':'xprw tftm lldy ranp',
'trevorzxasuniga214@gmail.com':'egnr eucw jvxg jatq',
'dellapreston50@gmail.com':'qoit huon rzsd eewo',
'neilfdhioley765@gmail.com':'rgco uwiy qrdc gvqh',
'hhzcharlesbaker201@gmail.com':'mcxq vzgm quxy smhh',
'samuelmnjassey32@gmail.com':'lgct cjiw nufr zxjg',
'allisonikse1922@gmail.com':'tozo xrzu qndn mwuq',
'corysnja1996@gmail.com':'pfjk ocbf augx cgiy',
'maddietrdk1999@gmail.com':'rhqb ssiz csar cvot',
'yaitskaya.alya@mail.ru':'CeiYHA6GNpvuCz584eCp',
'yelena.polikarpova.1987@mail.ru':'70Ktuvrs1iYbvSnbK8hG',
'yeva.zuyeva.85@mail.ru':'EBjgRqq73hue9dGhUA2R',
'zina.yagovenko.69@mail.ru':'QKBmpXnzFZVu9w4ewSrA',
'ilya.yaroslavov.72@mail.ru':'A2gNkb8n54i4T7XdPdH5',
'maryamna.moskvina.62@mail.ru':'dT7ftdX72cMsVemqRRqu',
'zina.zhvikova@mail.ru':'7CwRkjeL3a5viE9we3bt',
'boyarinova.fisa@mail.ru':'NnJfmSBzQ9Eew09xirpY',
'prokhor.sveshnikov.73@mail.ru':'Ybunrxdf95gkzm6A6ipp',
'azhikelyamov.yulian@mail.ru':'r7hanfr0tMqcBE4Edmg0',
'prokhor.siyantsev@mail.ru':'yubs6kvtfpWT4Tram26e',
'yablonev90@mail.ru':'42krThdaYbWCrCbH8UgK',
'mari.dvornikova.86@mail.ru':'qdEzYLWSTz6UEM2E4i0u',
'vika.tobolenko.96@mail.ru':'3WQ2wFTwge9m2C09QsfK',
'koporikov.yura@mail.ru':'nJtyfjqYi91j7tk0udNx',
'zina.podshivalova.92@mail.ru':'u4CL3YxVutmiuTvmTrbu',
'leha.novitskiy.71@mail.ru':'qQZd1gMqkU906Xk2hgJJ',
'rimma.aleksandrovicha.72@mail.ru':'biL4m6h0h4xQrDB3PnPp',
'polina.karaseva.1987@mail.ru':'mxZUqPPTrZHK99jUfPhB',
'prokhor.sablin.82@mail.ru':'vN7FjmmCmAD0JnQsANyc',
'kade.kostya@mail.ru':'U0hdXu7y3c1AVeT1Vpn9',
'yelizaveta.novokshonova.71@mail.ru':'aKPpgaPDuwaKbX1pbcq3',
'pozdovp@mail.ru':'EGDd20c7s82Z0s9LmrXc',
'siyasinovy@mail.ru':'z2ZdsRL04JvBYZrrjrvv',
'nina.gref.73@mail.ru':'sitw1XTxCVgji061iqj7',
'fil.golubkin.80@mail.ru':'PeaLrzjbn408DEeiqmQq',
'venedikt.babinov.71@mail.ru':'tBewA1HQm29c2Zkira96',
'den.verderevskiy.67@mail.ru':'fndp7qr67dpfXBAu0ePH',
'olga.viranovskaya.92@mail.ru':'50QSPrecgk5cMdk1YsBm',
'uyankilovich@mail.ru':'Muw9kX9vAhhKxbZXZ3sh',
'clqdxtqbfj@rambler.ru':'8278384a3L51C',
'qeuvkzwxao@rambler.ru':'72325556pMFol',
'mgiwwgbjqt@rambler.ru':'3180204jCoAdt',
'olwogjcicw@rambler.ru':'3993480P4Gyth',
'qjdmjszsnc@rambler.ru':'6545403StkbOh',
'yqoibpcoki@rambler.ru':'695328653f9Wp',
'vnlhjjkbxr@rambler.ru':'4609313egqV59',
'vpgcdkunar@rambler.ru':'9936120R4LYh3',
'agycsnogqq@rambler.ru':'0234025nWwX5j',
'ctmhzsngse@rambler.ru':'2480571s1sZvW',
'ryztzlttdn@rambler.ru':'9416368kTX5jI',
'hqxybovebw@rambler.ru':'8245145VhX704',
'rejrjswkwb@rambler.ru':'5114881xCYqsB',
'xkbecjvxnx@rambler.ru':'5670524FiFi39',
'xnlqkfvwzx@rambler.ru':'7911186rp8L9P',
'gvzzmqtuzy@rambler.ru':'5133370ZstXEx',
'eijxsbjyfy@rambler.ru':'36196124YQZeI',
'bizdlfuahq@rambler.ru':'8374903tkk2gA',
'dhehumtsef@rambler.ru':'9126453AkhK0Z',
'zsotxpaxvi@rambler.ru':'46227528QryxI',
'ktsgdygeuc@rambler.ru':'1853586bnCyzK',
'uiacgqvgpe@rambler.ru':'65280104FvoJW',
'ynazuhytyd@rambler.ru':'1038469bD3PXc',
'ewmyymarvi@rambler.ru':'5023318Bh3tBg',
'wllhpdisuj@rambler.ru':'24856958LdTsS',
'ldqicaqxqo@rambler.ru':'3878601ZNDUtq',
'qnuumqoreq@rambler.ru':'97575207Is6tx',
'hlqhvdwpvn@rambler.ru':'6886684bPjiyd',
'mjjjxiuadq@rambler.ru':'0606032V81m1F',
'qmasujqfrk@rambler.ru':'277585511anUy',
'mfemvxqdcq@rambler.ru':'8831015UwqwWD',
'jauvxszfam@rambler.ru':'0711044gqzrVR',
'lkmujuagfk@rambler.ru':'08781007DLS8k',
'kcamwmzxjo@rambler.ru':'9812873rVr1MY',
'czkklwifon@rambler.ru':'74278883h9FP8',
'tsjsbqyrfk@rambler.ru':'0150917jIseH2',
'pbetvcnhzh@rambler.ru':'9952234XaKDFu',
'bsahxcpwkw@rambler.ru':'2860163ch8Ido',
'xphyesgbtc@rambler.ru':'6594341ERehhX',
'egmpjoufeq@rambler.ru':'2613441hfDuWr',
'jyaolatwam@rambler.ru':'7668835xdjLbg',
'istooplcmf@rambler.ru':'6592403JR47Wm',
'vxesoednot@rambler.ru':'35885918QZw94',
'oywtklayaz@rambler.ru':'4434448KsCuTf',
'tazxrlpjil@rambler.ru':'8342862p9Wyst',
'aumiycpxid@rambler.ru':'4109383BuuNcN',
'lrrztbfuzy@rambler.ru':'3646406sDO8ay',
'ocggavguxr@rambler.ru':'6406050SL2mZG',
'imprdsrnmd@rambler.ru':'4869746vpxksJ',
'eidyoikavp@rambler.ru':'1243890yXPyix',
'jtbcabsapw@rambler.ru':'566339497yHv3',
'szokdvnzrw@rambler.ru':'5285567I3Bil1',
'jqflrccfjs@rambler.ru':'7239478VeLuf1',
'nhmxjawemh@rambler.ru':'22695409fkCex',
'uoolwvvwdc@rambler.ru':'1073090zX6ebM',
'bdnptczren@rambler.ru':'2684430DcPEuk',
'bfghzdkurg@rambler.ru':'3874335d5hDQy',
'ljlexsfcvo@rambler.ru':'4102671EIquGo',
'byzjhysyyg@rambler.ru':'4637736mzdEcT',
'tlrjbuzcyj@rambler.ru':'2437827AhPaGW',
'denjsbmggh@rambler.ru':'228014585ayVe',
'ekkjrcskzo@rambler.ru':'6609442MFPeDO',
'ptpjocqobw@rambler.ru':'6047270EXk7Hb',
'nekrxmcklm@rambler.ru':'3532718I3vV4C',
'ulgqeqvdqy@rambler.ru':'6764301Nx25yL',
'ezofozvhyn@rambler.ru':'43181265tC6FQ',
'hwklsnkqky@rambler.ru':'2399374mHyEUJ',
'elglaqexoj@rambler.ru':'9803014pMNF9p',
'rgmjfwhhjs@rambler.ru':'3268611cfC3aR',
'vcvwvkntgb@rambler.ru':'6536007UgTXg4',
'phkohtlitv@rambler.ru':'0238010TXt5aN',
'pqqqyejlqi@rambler.ru':'0429804UwSSi2',
'toxevermnd@rambler.ru':'1801000MqDm87',
'dicfdqgxad@rambler.ru':'2062460Tbvjlz',
'sktsnxhcxe@rambler.ru':'35185285Pon91',
'jpljjnrrla@rambler.ru':'0815671xPHjiw',
'rtqpiimiid@rambler.ru':'6534672URa1mI',
'ldygdlpizk@rambler.ru':'6686886YWhL05',
'fqxqadaxfy@rambler.ru':'3195621x5qYdU',
'chybzpsglw@rambler.ru':'8032931YTKllg',
'vkctzanare@rambler.ru':'1157997LGySqk',
'repjncygun@rambler.ru':'3300691BqYJVG',
'khrarivdow@rambler.ru':'7168350Cmqkmj',
'aqbeitoqdl@rambler.ru':'87552792499tS',
'vhauhgmbnc@rambler.ru':'9276444y9YzY1',
'cfoqabqkbi@rambler.ru':'4601718gc2Zji',
'kmqnowhvjp@rambler.ru':'6667003L1jZxc',
'djsdksvzhj@rambler.ru':'7523251yAKPjZ',
'uztbbbfqbp@rambler.ru':'8265517naN9fx',
'ljrbpfuicp@rambler.ru':'39793362TjZIk',
'jzzdyxicjo@rambler.ru':'8117494s6CZVB',
'gjnbtrflkc@rambler.ru':'8623171iqXOD9',
'jfjtwncyeb@rambler.ru':'7066987lMSG2Z',
'rfphqkyyrj@rambler.ru':'8800207M5Nj7Y',
'ilynipkqwx@rambler.ru':'83333032WQo83',
'ifzenleixs@rambler.ru':'69679436xM9U4',
'oevwtysoel@rambler.ru':'6918228UC47Zs',
'hpdkdwqvzx@rambler.ru':'0605431xMVexd',
'ekbkufxdxx@rambler.ru':'1918712uEOQ9t',
'zstxwfwiof@rambler.ru':'4043772UwRp5o',
'rjmrbybhnd@rambler.ru':'5203792lDmxvC',
'eukygnfzno@rambler.ru':'3520959hXs1Zw',
'ljrolbwlad@rambler.ru':'0394475pK0dYa',
'gozpezocmj@rambler.ru':'8282635Gkvuvq',
'asytoiumwt@rambler.ru':'42141199FgP3H',
'fbiooohghv@rambler.ru':'7338453zMbWhb',
'ajwlalfqqu@rambler.ru':'3360915x1XVgt',
'cvegntetwm@rambler.ru':'8091607CSuKMf',
'jnhjnmicbt@rambler.ru':'6375986dokrgG',
'fnaauasmjz@rambler.ru':'4160248ztCRsJ',
'qnwmlvfwct@rambler.ru':'8367630XGXmxW',
'lkycbhjcwp@rambler.ru':'5255980KedZTc',
'bkyojwrkxl@rambler.ru':'1286663uHl4WQ',
'lxddybklck@rambler.ru':'1077242JFSyQN',
'chzhdkoxnp@rambler.ru':'0533445SI0q7c',
'ofjxkwwomf@rambler.ru':'04956317DKrSX',
'jlirgtapbl@rambler.ru':'8728917NdMxgN',
'dgcceghlse@rambler.ru':'2986381aT5V36',
'rkwfhcvlem@rambler.ru':'10022063K5qmY',
'orgjvhbrxw@rambler.ru':'0652659TopL8Z',
'opynskpmzp@rambler.ru':'2881423L4qs6x',
'pbqzrueeko@rambler.ru':'44469262tOGeK',
'raxzhngqti@rambler.ru':'3078265mgWYjl',
'ztnxozwuuj@rambler.ru':'0637919utKekj',
'gtxjzwlgio@rambler.ru':'3737088WWddrY',
'sjbflcwjgn@rambler.ru':'9791667kVGllD',
'znggdpfxzu@rambler.ru':'0209083jdisUI',
'gnvhlocnro@rambler.ru':'4361239Vu3OCl',
'vqeijhgrmo@rambler.ru':'5560137M1oKk2',
'meefvzfwqb@rambler.ru':'9793015vJE0qF',
'sclsjzvugn@rambler.ru':'4631432OQjvWt',
'ybbtiosefy@rambler.ru':'3511505pL04S1',
'agwqdadpkb@rambler.ru':'0930298CUZdLp',
'kudgvibwao@rambler.ru':'5791834nlLQtU',
'qyonxjqbxi@rambler.ru':'9390829m2Edz3',
'jhetdlhlqk@rambler.ru':'5530162MiLHZe',
'bsjvczarsc@rambler.ru':'5747155KvNjcL',
'wlcilpvzqu@rambler.ru':'2757580jLlM9M',
'xxdgcixidw@rambler.ru':'2867562O7zGft',
'wekduwrnkp@rambler.ru':'2646367TlIskI',
'keakcnrorg@rambler.ru':'9223165cV1Jj8',
'nzuspyevwr@rambler.ru':'2212416npkUqe',
'mgjfbgitts@rambler.ru':'7368986roeLXD',
'smfxvrnhmu@rambler.ru':'6947298Kau5qA',
'yvkelubdzf@rambler.ru':'5913332lXWtlC',
'bwywtjxybd@rambler.ru':'2766021wTSkeU',
'dlvyzavolw@rambler.ru':'274983252lHyu',
'oaudcugulf@rambler.ru':'4543030UHFWaV',
'zvqexaokhf@rambler.ru':'1453114PCheCq',
'pjuafpzpoo@rambler.ru':'8474216vNFUG0',
'ckryhpqogh@rambler.ru':'4791674aJHW43',
'vlkqstbhpd@rambler.ru':'3021260kBI3KU',
'jwuupemjpm@rambler.ru':'7769235y719L9',
'bmxuqrzcnk@rambler.ru':'1345552ExHXyu',
'fqrkonqkjc@rambler.ru':'4104158bVEORa',
'gizwbhyrfd@rambler.ru':'3863359lgfpTv',
'onghqwbvnz@rambler.ru':'8249537XWqpPk',
'aeyeyvlnkl@rambler.ru':'6025219f5mGom',
'qcwweqcqbx@rambler.ru':'2503306kHzKPD',
'vefmynztzu@rambler.ru':'1134939bhRpJS',
'qlkhitdctp@rambler.ru':'31621358ZPx5F',
'xhgfgecvrn@rambler.ru':'4116759TRhERi',
'globizrzui@rambler.ru':'9679753mLkmMd',
'vvfcuoibrf@rambler.ru':'13558992CDkJj',
'enccmwktap@rambler.ru':'7631476Lzr9hd',
'njbnyghvdq@rambler.ru':'48585907Qh2NS',
'cobadewaxd@rambler.ru':'6433228NMX7a0',
'zzvsuoiqfx@rambler.ru':'5067380KtnMTb',
'lkdcjpcqxu@rambler.ru':'8319085aRHdoT',
'zcabeofgox@rambler.ru':'0059181TJSaJq',
'rswrifhmtf@rambler.ru':'2987108xzf1Uy',
'gebzgyscic@rambler.ru':'6981082UOD1sL',
'yhncgfwjom@rambler.ru':'7866073mRMAal',
'pvvlmjmiwe@rambler.ru':'2807349CLUZie',
'towqdsigmc@rambler.ru':'48481486UnoRg',
'eyzwvxphxz@rambler.ru':'5532563Bskght',
'aruhbkpsud@rambler.ru':'8022722dNUe59',
'kckwnnvmwf@rambler.ru':'77502899D6ygI',
'emicquwuxf@rambler.ru':'2982514obBgCJ',
'pnefqbonja@rambler.ru':'1443294ZY7BgB',
'wlnecrzvkb@rambler.ru':'2016456ke4QRw',
'lucufydobd@rambler.ru':'4188202gvlmuR',
'obcheovoqy@rambler.ru':'34012721sYlv3',
'fjxwhhlhxp@rambler.ru':'1621680a9CbS0',
'rjggfmhckx@rambler.ru':'4470958ocoPjD',
'oqixhlbhlh@rambler.ru':'4902150aD8Tkr',
'zmlfdygkce@rambler.ru':'4809956HgOdyu',
'zdjqfhdafp@rambler.ru':'9142498RW8Ynh',
'cjoyoxsdby@rambler.ru':'108516737An82',
'hfrcbbwzgb@rambler.ru':'1732107RUVvSu',
'crkbywjfzg@rambler.ru':'9616254qbUhAG',
'luygpfibra@rambler.ru':'9488606qXIvQZ',
'xepjtcrrzo@rambler.ru':'3774977dMOr4c',
'ayrbethwst@rambler.ru':'4658060glYVyA',
'czhjnqqgdd@rambler.ru':'89865789wXqfK',
'oltotetppj@rambler.ru':'0936665mJL9H0',
'eaoeqvygrv@rambler.ru':'5348316HcEpsm',
'dkfvwvkotb@rambler.ru':'3366454MTGiOR',
'wavsfqiarg@rambler.ru':'4220587wVJ8gU',
'gkwlbrhwix@rambler.ru':'6383580cCHutT',
'uachryyzde@rambler.ru':'0643369cWRWhr',
'nuyfldwirg@rambler.ru':'29709163eKxWc',
'fnorovxtvk@rambler.ru':'469173140zLer',
'qrmnfyxdqj@rambler.ru':'7609701E9XfBC',
'ncupywgysj@rambler.ru':'8506439mTgrb6',
'ehhuextqqm@rambler.ru':'4136418EqGa4N',
'utasiosnxd@rambler.ru':'6230428wOiMLm',
'ppizzpzqod@rambler.ru':'6217530deEIGb',
'mgzczmjjpo@rambler.ru':'5974114gf7VLz',
'ezugyxxfkx@rambler.ru':'6920685aZVulS',
'vnuwwwuhuj@rambler.ru':'20889562nRk1x',
'xqkicchcbc@rambler.ru':'4345126XoitUD',
'hykbjrvqsw@rambler.ru':'8281493mLUbNt',
'etyqikxlam@rambler.ru':'1096360Cvg5n7',
'blnpfilkdh@rambler.ru':'6208964Fhgy1O',
'azawxjcfeh@rambler.ru':'8923382Pqo1jI',
'dyumumpgus@rambler.ru':'3454195S5FQ7d',
'ryejfejmef@rambler.ru':'1474062Y49oZE',
'uqyfeqyumv@rambler.ru':'4305431o270vK',
'vardlzqzas@rambler.ru':'8158325VAjymq',
'wvqbwbpofd@rambler.ru':'2037592lvIWZI',
'agsnpvxscg@rambler.ru':'676450330Gmzj',
'ctiwtwpowk@rambler.ru':'7004605qQOK5O',
'vvluscokds@rambler.ru':'2351339uVtaUb',
'gqtipysiyk@rambler.ru':'4672575GMSkQq',
'vwtjzupcul@rambler.ru':'6978060SRfKxQ',
'klvdgsoczb@rambler.ru':'8504791kNehzf',
'lavpussyin@rambler.ru':'1183746FmKlfU',
'xvzoptqyhd@rambler.ru':'7635851M7gCQO',
'yzkgydxjlr@rambler.ru':'3889248nBv9xb',
'tkuscgummb@rambler.ru':'2646861vfBmjy',
'ytbfnnlvuc@rambler.ru':'8680715wXqNoY',
'qrmyueqrpk@rambler.ru':'48163158cQzn3',
'nulburzrsp@rambler.ru':'4628721fbFYDx',
'xpsncakaar@rambler.ru':'8050121QgZtLE',
'rsfyuinlhi@rambler.ru':'7789677doEl7X',
'lruwhkjpmm@rambler.ru':'2407934PCrhbt',
'zqlboekoph@rambler.ru':'4540547BXedBD',
'djrmgdvpxk@rambler.ru':'2516345lt4GhI',
'cdyagajvqt@rambler.ru':'0457036J8b9x1',
'csbmtfyogo@rambler.ru':'8578398RoY5Me',
'mtgjgvchbf@rambler.ru':'6273263XOh0fb',
'hjovrkraea@rambler.ru':'1756354e4T9PL',
'wuasdmqayg@rambler.ru':'8983467Njjbfc',
'dnzaquycrh@rambler.ru':'3047369gLtNHO',
'rdptnhimnz@rambler.ru':'92217639LcTX1',
'yklofyaekj@rambler.ru':'0018913JhfLfv',
'zqfzplzlwp@rambler.ru':'6550676M1gwNy',
'fzcveyejbh@rambler.ru':'9098104PB57ol',
'qcpwhpqape@rambler.ru':'3277585gafS4o',
'xfitvnzvez@rambler.ru':'0023433CgWWiW',
'tiansbolvj@rambler.ru':'0200419d6c8hD',
'ibwukvjyxn@rambler.ru':'6846348Go4rB7',
'tfclkifgjn@rambler.ru':'9973469KBqk2S',
'yscehsgepj@rambler.ru':'0258935Wptd0G',
'webznumpmf@rambler.ru':'4342482ZhTyVk',
'xadehtuxys@rambler.ru':'94129234ZK2kl',
'wsfmuqnmjp@rambler.ru':'7886187uCcru0',
'mhovkuzfnl@rambler.ru':'3632660bLpvSw',
'pppuvtsuxu@rambler.ru':'6227635FqgnGa',
'vvezjeryic@rambler.ru':'7595367ZgjYIn',
'oiukjktkhx@rambler.ru':'35863397YZBFb',
'qswbndmblj@rambler.ru':'3563325a93EZ6',
'ztyfnsdrqa@rambler.ru':'7748929ZbfDrw',
'lrjduagkcj@rambler.ru':'8783147DV4pJe',
'fhrzanukuh@rambler.ru':'169703230lEf6',
'pqnnzwuuku@rambler.ru':'6446752B0qw8H',
'ndctkqjnfc@rambler.ru':'1534939xHfafC',
'tlzuekovcn@rambler.ru':'9668644RKjMla',
'ermdcrjyhu@rambler.ru':'9838788xXiLRC',
'qbfymlhpwj@rambler.ru':'3278597BlWafL',
'uuuzmgapoy@rambler.ru':'2535811Vz3dxV',
'chjolhsihy@rambler.ru':'8253848P8B5cd',
'rrakdmtsdb@rambler.ru':'0459246V4tjHK',
'ngkrbvqvha@rambler.ru':'9835759JQxkal',
'caxeoztjpa@rambler.ru':'1297098SSweKM',
'molnxkchzu@rambler.ru':'3122920NIh3iE',
'murnslgulf@rambler.ru':'1045964Oppb9c',
'qcjyautxca@rambler.ru':'6358075LUbp6R',
'amhlnrxaue@rambler.ru':'3401580IiYPYn',
'wexnexkcct@rambler.ru':'2157766eLIiqP',
'oplwkvkrct@rambler.ru':'7136350vkGkaT',
'pmddwbvmwv@rambler.ru':'3066705M2aCUh',
'aqjcdxeuuh@rambler.ru':'2077271RlOJ0c',
'baiivnfrdy@rambler.ru':'1327519LJwKyi',
'apvskvwhsv@rambler.ru':'2995739T8pCNZ',
'xsejblkgit@rambler.ru':'6224118EhnkyG',
'rxihtsvdxg@rambler.ru':'3045787jhQxfI',
'dgtmxgrdsm@rambler.ru':'0342058YAff0O',
'wuxaurjkuu@rambler.ru':'6231160X8CsYl',
'erimfuxfdl@rambler.ru':'1956070yzlgSl',
'ncklilvfts@rambler.ru':'5077711XhCUzu',
'eerlpvniie@rambler.ru':'6769422kteVgK',
'mcrtyjkbdi@rambler.ru':'5281059WC9HfI',
'izjnzlavcu@rambler.ru':'4201974Gjdy1B',
'tkrywugfgq@rambler.ru':'1037112WpAZzl',
'hpxzczhgwe@rambler.ru':'4522788wYVDJk',
'rtfanictwt@rambler.ru':'9292445IxACdk',
'lhschktxka@rambler.ru':'0731083E0ItX4',
'zfqfwvmnms@rambler.ru':'82390631NIbOF',
'rzaviakxlb@rambler.ru':'2230383uFiVmA',
'rmmueooozx@rambler.ru':'1531525wyFFSm',
'weasmvistt@rambler.ru':'7079364RGZCBs',
'qikszesoqz@rambler.ru':'6739326h2Wy4j',
'gosgrmonmh@rambler.ru':'7425012zw2LXl',
'vuhlehwstc@rambler.ru':'6477750sVXsV3',
'wcbmulbsbk@rambler.ru':'9889803qVwaj6',
'aejerwwnft@rambler.ru':'4598847uygrUg',
'rtrkjygdey@rambler.ru':'4810312JrG4Ti',
'uywyrkhuue@rambler.ru':'6593801fMGH6b',
'flqyimskwk@rambler.ru':'7856809GVZfzT',
'mqjqttpyui@rambler.ru':'3633261lxxEPt',
'asagkqfygx@rambler.ru':'90629300zd5Xm',
'bupfcjoqrc@rambler.ru':'7806644uXzkZy',
'twicbfjgoz@rambler.ru':'0187832xjeOz1',
'kseniya.pavlova.9898@mail.ru': 'GRVDAjqvvx9xz00L2wUx',
        'annakrasnova.1994@mail.ru': 'jUFMXba6wLFcuQBkqht2',
 'sanya.dragonov@mail.ru': 'RakuzanSnos',
    'avyavya.vyaavy@mail.ru': 'zmARvx1MRvXppZV6xkXj',
    'gdfds98@mail.ru': '1CtFuHTaQxNda8X06CaQ',
    'dfsdfdsfdf51@mail.ru': 'SXxrCndCR59s5G9sGc6L',
'aria.therese.svensson@mail.com': 'Zorro1ab',
'taterbug@verizon.net': 'Holly1!',
'ejbrickner@comcast.net': 'Pass1178',
'teressapeart@cox.net': 'Quinton2329!',
'liznees@verizon.net': 'Dancer008',
'olajakubovich@mail.com': 'OlaKub2106OlaKub2106',
'kcdg@charter.net': 'Jennifer3*',
'bean_118@hotmail.com': 'Liverpool118!',
'dsdhjas@mail.com': 'LONGHACH123',
'robitwins@comcast.net': 'May241996',
'wasina@live.com': 'Marlas21',
'aruzhan.01@mail.com': '1234567!',
'rob.tackett@live.com': 'metallic',
'lindahallenbeck@verizon.net': 'Anakin@2014',
'hlaw82@mail.com': 'Snoopy37$$',
'paintmadman@comcast.net': 'mycat2200*',
'prideandjoy@verizon.net': 'Ihatejen12',
'sdgdfg56@mail.com': 'kenwood4201',
'garrett.danelz@comcast.net': 'N11golfer!',
'gillian_1211@hotmail.com': 'Gilloveu1211',
'sunpit16@hotmail.com': 'Putter34!',
'fdshelor@verizon.net': 'Masco123*',
'yeags1@cox.net': 'Zoomom1965!',
'amine002@usa.com': 'iScrRoXAei123',
'bbarcelo16@cox.net': 'Bsb161089$$',
'laliebert@hotmail.com': 'pirates2',
'vallen285@comcast.net': 'Delft285!1!',
'sierra12@email.com': 'tegen1111',
'luanne.zapevalova@mail.com': 'FqWtJdZ5iN@',
'kmay@windstream.net': 'Nascar98',
'redbrick1@mail.com': 'Redbrick11',
'ivv9ah7f@mail.com': 'K226nw8duwg',
'erkobir@live.com': 'floydLAWTON019',
'Misscarter@mail.com': 'ashtray19',
'carlieruby10@cox.net': 'Lollypop789$',
'blackops2013@mail.com': 'amason123566',
'caroline_cullum@comcast.net': 'carter14',
'dpb13@live.com': 'Ic&ynum13',
'heirhunter@usa.com': 'Noguys@714',
'sherri.edwards@verizon.net': 'Dreaming123','rami.rami1980@hotmail.com': 'ramirami1980',
'jmsingleton2@comcast.net': '151728Jn$$',
'aberancho@aol.com': '10diegguuss10',
'dgidel@iowatelecom.net': 'Buster48',
'gpopandopul@mail.com': 'GEORG62A',
'bolgodonsk@mail.com': '012345678!',
'colbycolb@cox.net': 'Signals@1',
'lyimbshsup@rambler.ru': '6463734rnAygg',
           'jdqukazixk@rambler.ru': '0225223ACFeq0',
           'baljufgcnc@rambler.ru': '4738678YMyCvO',
           'ruslanorlovimx4134@rambler.ru': 'Andersonnancy945',
           'vladislavkulikovxcr1902@rambler.ru': 'Allenkimberly021',
           'romasidorovdbj3700@rambler.ru': 'Clarkmargaret444',
           'lehabogdanovhdw1954@rambler.ru': 'Evanssandra913',
           'mihailtitovopr6182@rambler.ru': 'Younghelen407',
           'koljafedotovmqj2347@rambler.ru': 'Gonzalezsarah321',
           'genasemenovhvu9785@rambler.ru': 'Taylorlaura482',
           'vovafedorovmvu7067@rambler.ru': 'Collinsbetty976',
           'grishakulikovyyk8848@rambler.ru': 'Wilsonlaura931',
           'olegnikitinxwo3553@rambler.ru': 'Wrightkaren568',
           'gennadijkalininizb3132@rambler.ru': 'Turnerdorothy038',
           'bogdankarpovxad9304@rambler.ru': 'Carterlinda019',
           'koljakuznecovzfq8892@rambler.ru': 'Walkerhelen225',
           'vladdmitrievtpv8734@rambler.ru': 'Brownmary434',
           'arturkovalevdln7432@rambler.ru': 'Lewisnancy365',
           'konstantinbelovabq7348@rambler.ru': 'Allenmary923',
           'sashavorobevbml8362@rambler.ru': 'Hilllaura818',
           'ruslankozlovhji7240@rambler.ru': 'Hallnancy735',
           'olegzajcevepy8163@rambler.ru': 'Nelsonsharon117',
           'grigorijfominlxp0053@rambler.ru': 'Wrightpatricia686',
           'vitalijmaslovusv3737@rambler.ru': 'Garciabetty827',
           'olegbelovblx5518@rambler.ru': 'Phillipssharon437',
           'olegmaslovrde8926@rambler.ru': 'Mitchellbetty324',
           'vitalijdavydovtal6583@rambler.ru': 'Rodriguezmichelle351',
           'dmitrijmironovlaf9788@rambler.ru': 'Whitedeborah816',
           'vanjakulikovdpf6394@rambler.ru': 'Allencarol017',
           'andrejmaksimovwjw5202@rambler.ru': 'Cartersusan436',
           'zhenjaafanasevomj8876@rambler.ru': 'Harrislinda730',
           'sanjatimofeevxur1820@rambler.ru': 'Martinmichelle433',
           'grishabogdanovhqj9645@rambler.ru': 'Turnermargaret062',
           'viktorpavlovzlh2404@rambler.ru': 'Hilllaura917',
           'mihailkuznecovbuh2424@rambler.ru': 'Millerkaren783',
           'bogdanmironovkgf3690@rambler.ru': 'Greenjennifer095',
           'tolikkulikovnfv3662@rambler.ru': 'Perezelizabeth881',
           'sanjaabramovotb8410@rambler.ru': 'Hillpatricia526',
           'pashabykovzhy8581@rambler.ru': 'Scottdonna750',
           'jurijbogdanovwuc0744@rambler.ru': 'Harrisnancy027',
           'antongusevaws0670@rambler.ru': 'Collinsruth779',
           'maksimlebedevsxm5444@rambler.ru': 'Evanskaren499',
           'vladimirchernyshevfnt3789@rambler.ru': 'Halldonna541',
           'petjagusevrzl9637@rambler.ru': 'Taylorpatricia485',
           'vitaliklebedevhla3289@rambler.ru': 'Lewismichelle721',
           'aleksandrwerbakovsbg8385@rambler.ru': 'Gonzalezdeborah554',
           'pavelgrigorevjtz4407@rambler.ru': 'Campbellbetty034',
           'maksdenisovskv0461@rambler.ru': 'Smithmaria151',
           'gennadijtihonovqzc3691@rambler.ru': 'Clarksharon602',
           'ruslandmitrievvgr1236@rambler.ru': 'Kingdeborah697',
           'genamaslovfys4433@rambler.ru': 'Wrightsharon746',
           'borjamironovfrc3345@rambler.ru': 'Harrissusan337',
           'antonchernovown4062@rambler.ru': 'Thomaskimberly712',
           'vladimirgrigoreveqq9112@rambler.ru': 'Parkermichelle304',
           'sashawerbakoviet2953@rambler.ru': 'Clarksharon806',
           'mishaantonovcwv6881@rambler.ru': 'Kingmargaret388',
           'mihailmelnikovoyp1458@rambler.ru': 'Wilsonlisa429',
           'kostjakiselevhjw4194@rambler.ru': 'Evanshelen904',
           'kostjastepanovbes5317@rambler.ru': 'Carterlaura187',
           'toljadanilovcvh2967@rambler.ru': 'Martinezbarbara968',
           'leshakozlovspt3407@rambler.ru': 'Hernandezbetty901',
           'vanjakozlovbvy7090@rambler.ru': 'Jonescarol966',
           'leshafilippovfha9160@rambler.ru': 'Davislinda702',
           'olegjakovlevmkp6120@rambler.ru': 'Perezjennifer226',
           'igorisaevfen3865@rambler.ru': 'Allenpatricia615',
           'pashakonovalovgmf3693@rambler.ru': 'Garciamichelle737',
           'vladimirandreevqol3763@rambler.ru': 'Robinsonkimberly357',
           'jurijprohorovgnq3561@rambler.ru': 'Kinglaura374',
           'vladislavtarasovpqk4498@rambler.ru': 'Garciacarol344',
           'antonvorobevtxz5033@rambler.ru': 'Lopezlinda159',
           'romaandreevjvo1698@rambler.ru': 'Youngnancy376',
           'vladislavbeljaevvfa7045@rambler.ru': 'Robertsjennifer080',
           'vitaliknikolaevzoh1565@rambler.ru': 'Collinsdonna967',
           'koljamironovydt4703@rambler.ru': 'Wrightmichelle859',
           'gennadijsemenovmki9018@rambler.ru': 'Perezsusan734',
           'pashakarpovafr2420@rambler.ru': 'Wrightsarah462',
           'artemkomarovqqt3719@rambler.ru': 'Martinlinda992',
           'konstantinchernyshevneh8321@rambler.ru': 'Smithdonna021',
           'grigorijsidorovrpl5056@rambler.ru': 'Harrispatricia221',
           'petrsergeevmse2216@rambler.ru': 'Bakerjennifer796',
'brailsnos29s7yeu@gmail.com': 'brailsnos29s7yeu','shasa22872kos92ho@gmail.com':
'shasa22872kos92ho@','snoserbraila1@gmail.com':
'snoserbraila1    ','avyavya.vyaavy@mail.ru': 'zmARvx1MRvXppZV6xkXj','korlithiobtennick@mail.ru': 'feDLSiueGT89APb81v74',
    'avyavya.vyaavy@mail.ru': 'zmARvx1MRvXppZV6xkXj',
    'gdfds98@mail.ru': '1CtFuHTaQxNda8X06CaQ',
    'dfsdfdsfdf51@mail.ru': 'SXxrCndCR59s5G9sGc6L',
 'lovedel.anisss@mail.ru': 'cJkiz18MAWS0L85DGW8n',
           'love.efs@mail.ru': 'vzw5bwePbzeXhYhDeeA1',
           'fsadfsaf.sdfasdfas@mail.ru': 'KUN0wpJbViwpFXFPkHb4',
           'fkjvfmdsof@mail.ru': 'CxM2JUT0vx03aSyD53Ns',
           'sawage.dasha@mail.ru': 'SyfStmkgK29KUB0BQVAy',
           'opunm.sdaww@mail.ru': 'Y1BjSZCHeLTxmvaW49FH',
           'fall.gall@mail.ru': 'tFqTgMUqkidcBbw91hD7',
           'wzxcvd@mail.ru': 'vwPUnRUGW75MUKaFzhVc',
           'masha.mashala@mail.ru': 'rtM0rCSHZstDVQpxmEkh',
           'wwagege@mail.ru': 'ZZNkRLrZseLN57phVeEQ',
           'irigjfodjdkdkk@mail.ru': 'n8r0TKCygC5xqaWxStr1',
           'sdfghafdhg@mail.ru': 'Kag0fefn6mFWMzQ17PGb',
           'dasha.goat@mail.ru': '3bkf9iHyuFUfEfKzXYLm',
           'dasha.sasaas@mail.ru': 'UAVwCgpFXaD2zcQ9gVSE',
           'dasha.lovely.02@mail.ru': 'paUrCHANKWWxefzaQvQm',
           'dasha.butifull@mail.ru': '0bAbKQUfpVRDcrLtc0Ya',
           'firirotifigj@gmail.com': 'RQCgW8vb127AGRZ5Kvf1',
           'dasha.mdaaa@gmail.com': 'HXNg0M0bvyaEs1tbMjTB',
           'lfwgdg@mail.ru': 'h6hAUvp3KNPqqcmmduU3',
           'dasha.holle@mail.ru': '0g5g6kwEtkKw2hYCaSTj',
           'darya.holly@mail.ru': 'he02duEXu4iiDambB6ZG',
           'dasha.vonk@mail.ru': 'AayKrKyfEDyeubmRqKRm',
           'kloxc@mail.ru': 'FVUeii2MdbNcqEmZr','korlithiobtennick@mail.ru': 'feDLSiueGT89APb81v74',
    'avyavya.vyaavy@mail.ru': 'zmARvx1MRvXppZV6xkXj',
    'gdfds98@mail.ru': '1CtFuHTaQxNda8X06CaQ',
    'dfsdfdsfdf51@mail.ru': 'SXxrCndCR59s5G9sGc6L',
'aria.therese.svensson@mail.com': 'Zorro1ab',
'taterbug@verizon.net': 'Holly1!',
'ejbrickner@comcast.net': 'Pass1178',
'teressapeart@cox.net': 'Quinton2329!',
'liznees@verizon.net': 'Dancer008',
'olajakubovich@mail.com': 'OlaKub2106OlaKub2106',
'kcdg@charter.net': 'Jennifer3*',
'bean_118@hotmail.com': 'Liverpool118!',
'dsdhjas@mail.com': 'LONGHACH123',
'robitwins@comcast.net': 'May241996',
'wasina@live.com': 'Marlas21',
'aruzhan.01@mail.com': '1234567!',
'rob.tackett@live.com': 'metallic',
'lindahallenbeck@verizon.net': 'Anakin@2014',
'hlaw82@mail.com': 'Snoopy37$$',
'paintmadman@comcast.net': 'mycat2200*',
'prideandjoy@verizon.net': 'Ihatejen12',
'sdgdfg56@mail.com': 'kenwood4201',
'garrett.danelz@comcast.net': 'N11golfer!',
'gillian_1211@hotmail.com': 'Gilloveu1211',
'sunpit16@hotmail.com': 'Putter34!',
'fdshelor@verizon.net': 'Masco123*',
'yeags1@cox.net': 'Zoomom1965!',
'amine002@usa.com': 'iScrRoXAei123',
'bbarcelo16@cox.net': 'Bsb161089$$',
'laliebert@hotmail.com': 'pirates2',
'vallen285@comcast.net': 'Delft285!1!',
'sierra12@email.com': 'tegen1111',
'luanne.zapevalova@mail.com': 'FqWtJdZ5iN@',
'kmay@windstream.net': 'Nascar98',
'redbrick1@mail.com': 'Redbrick11',
'ivv9ah7f@mail.com': 'K226nw8duwg',
'erkobir@live.com': 'floydLAWTON019',
'Misscarter@mail.com': 'ashtray19',
'carlieruby10@cox.net': 'Lollypop789$',
'blackops2013@mail.com': 'amason123566',
'caroline_cullum@comcast.net': 'carter14',
'dpb13@live.com': 'Ic&ynum13',
'heirhunter@usa.com': 'Noguys@714',
'sherri.edwards@verizon.net': 'Dreaming123','rami.rami1980@hotmail.com': 'ramirami1980',
'jmsingleton2@comcast.net': '151728Jn$$',
'aberancho@aol.com': '10diegguuss10',
'dgidel@iowatelecom.net': 'Buster48',
'gpopandopul@mail.com': 'GEORG62A',
'bolgodonsk@mail.com': '012345678!',
'colbycolb@cox.net': 'Signals@1',
'nicrey4@comcast.net': 'Dabears54',
'mordechai@mail.com': 'Mordechai',
'inemrzoya@mail.com': 'rLS1elaUrLS1elaU',
'tarabedford@comcast.net': 'Money4me',
'mycockneedsit@mail.com': 'benjamin3',
'saralaine@mail.com': 'sarlaine12!1',
'jonb2006@verizon.net': '1969Camaro',
'rjhssa1@verizon.net': 'Donna613*',
'cameron.doug@charter.net': 'Jake2122$',
'bridget.shappell@comcast.net': 'Brennan1',
'rugs8@comcast.net': 'baseball46',
'averyjacobs3@mail.com': '1960682644!',
'lstefanick@hotmail.com': 'Luv2dance2',
'bchavez123@mail.com': 'aadrianachavez',
'lukejamesjones@mail.com': 'tinkerbell1',
'emahoney123@comcast.net': 'Shieknmme3','mandy10.mcevoy@btinternet.com': 'Tr1plets3',
'jet747@cox.net': 'Sadie@1234',
'landsgascareservices@mail.com': 'Alisha25@',
'samantha224@mail.com': 'Madden098!@',
'kbhamil@wowway.com': 'Carol1940',
'email@bjasper.com': 'Lhsnh4us123!',
'biggsbrian@cox.net': 'Trains@2247Trains@2247',
'dzzeblnd@aol.com': 'Geosgal@1',
'jtrego@indy.rr.com': 'Jackwill14!',
'chrisphonte.rj@comcast.net': 'Junior@3311',
'tvwifiguy@comcast.net': 'Bill','defenestrador@mail.com': 'm0rb1d8ss',
'glangley@gmx.com': 'ironhide',
'zmbuohbo@nietamail.com': 'bwhshijvS!7708',
'mzwdxmbr@vecinomail.com': 'yogovhrcS!9604',
'sdwljbvw@senoramail.com': 'fhfmqzwhS!3765',
'bvmqjvxg@menormail.com': 'obcyxskhX!5435',
'vpdsmckd@nietamail.com': 'soivmwqbA!4968',
'rtckyhny@vecinomail.com': 'xxtgawjxX!8484',
'etczzucr@senoramail.com': 'jlgflnfvS!9717',
'muztpwnl@menormail.com': 'xplstfvnA!4629',
'afbzgbqs@nietamail.com': 'hcthlbkkS!9664',
'vwnajvtb@vecinomail.com': 'qpaufpfdX!6846',
'ndnxnqst@senoramail.com': 'uamvwtvxY!4448',
'aehbzvtn@menormail.com': 'pdzabldbX!1586',
'yuofldqp@nietamail.com': 'uumnzcoqA!9950',
'iryxsvsg@vecinomail.com': 'hcnkpndqY!3869',
'adeppaas@senoramail.com': 'qdjmsbtrY!8595','vbrexarm@menormail.com': 'mpyxepysX!5838',
'uiwedngh@nietamail.com': 'xenlwbqqX!3150',
'kgwbdctw@vecinomail.com': 'vgnbhgclX!7983',
'yxjcdhet@senoramail.com': 'ykfdidaiY!2510',
'hfrtvmrz@menormail.com': 'cirrohtjY!3834',
'mpudwtru@nietamail.com': 'ofdhcbjqX!8197',
'eoulmbhe@vecinomail.com': 'wdcytnqaY!2858',
'diniduks@senoramail.com': 'qdatfzqaS!4552',
'acpidkkq@menormail.com': 'slownwabX!7663',
'nkpswjsb@nietamail.com': 'tjyaixxvY!7554',
'charlotte2850@hotmail.com': 'kelalu2850','korlithiobtennick@mail.ru': 'feDLSiueGT89APb81v74',
    'avyavya.vyaavy@mail.ru': 'zmARvx1MRvXppZV6xkXj',
    'gdfds98@mail.ru': '1CtFuHTaQxNda8X06CaQ',
    'dfsdfdsfdf51@mail.ru': 'SXxrCndCR59s5G9sGc6L',
'aria.therese.svensson@mail.com': 'Zorro1ab',
'taterbug@verizon.net': 'Holly1!',
'ejbrickner@comcast.net': 'Pass1178',
'teressapeart@cox.net': 'Quinton2329!',
'liznees@verizon.net': 'Dancer008',
'olajakubovich@mail.com': 'OlaKub2106OlaKub2106',
'kcdg@charter.net': 'Jennifer3*',
'bean_118@hotmail.com': 'Liverpool118!',
'dsdhjas@mail.com': 'LONGHACH123',
'robitwins@comcast.net': 'May241996',
'wasina@live.com': 'Marlas21',
'aruzhan.01@mail.com': '1234567!',
'rob.tackett@live.com': 'metallic',
'lindahallenbeck@verizon.net': 'Anakin@2014',
'hlaw82@mail.com': 'Snoopy37$$',
'paintmadman@comcast.net': 'mycat2200*',
'prideandjoy@verizon.net': 'Ihatejen12',
'sdgdfg56@mail.com': 'kenwood4201',
'garrett.danelz@comcast.net': 'N11golfer!',
'gillian_1211@hotmail.com': 'Gilloveu1211',
'sunpit16@hotmail.com': 'Putter34!',
'fdshelor@verizon.net': 'Masco123*',
'yeags1@cox.net': 'Zoomom1965!',
'amine002@usa.com': 'iScrRoXAei123',
'bbarcelo16@cox.net': 'Bsb161089$$',
'laliebert@hotmail.com': 'pirates2',
'vallen285@comcast.net': 'Delft285!1!',
'sierra12@email.com': 'tegen1111',
'luanne.zapevalova@mail.com': 'FqWtJdZ5iN@',
'kmay@windstream.net': 'Nascar98',
'redbrick1@mail.com': 'Redbrick11',
'ivv9ah7f@mail.com': 'K226nw8duwg',
'erkobir@live.com': 'floydLAWTON019',
'Misscarter@mail.com': 'ashtray19',
'carlieruby10@cox.net': 'Lollypop789$',
'blackops2013@mail.com': 'amason123566',
'caroline_cullum@comcast.net': 'carter14',
'dpb13@live.com': 'Ic&ynum13',
'heirhunter@usa.com': 'Noguys@714',
'sherri.edwards@verizon.net': 'Dreaming123','rami.rami1980@hotmail.com': 'ramirami1980',
'jmsingleton2@comcast.net': '151728Jn$$',
'aberancho@aol.com': '10diegguuss10',
'dgidel@iowatelecom.net': 'Buster48',
'gpopandopul@mail.com': 'GEORG62A',
'bolgodonsk@mail.com': '012345678!',
'colbycolb@cox.net': 'Signals@1',
'nicrey4@comcast.net': 'Dabears54',
'mordechai@mail.com': 'Mordechai',
'inemrzoya@mail.com': 'rLS1elaUrLS1elaU',
'tarabedford@comcast.net': 'Money4me',
'mycockneedsit@mail.com': 'benjamin3',
'saralaine@mail.com': 'sarlaine12!1',
'jonb2006@verizon.net': '1969Camaro',
'rjhssa1@verizon.net': 'Donna613*',
'cameron.doug@charter.net': 'Jake2122$',
'bridget.shappell@comcast.net': 'Brennan1',
'rugs8@comcast.net': 'baseball46',
'averyjacobs3@mail.com': '1960682644!',
'lstefanick@hotmail.com': 'Luv2dance2',
'bchavez123@mail.com': 'aadrianachavez',
'lukejamesjones@mail.com': 'tinkerbell1',
'emahoney123@comcast.net': 'Shieknmme3','mandy10.mcevoy@btinternet.com': 'Tr1plets3',
'jet747@cox.net': 'Sadie@1234',
'landsgascareservices@mail.com': 'Alisha25@',
'samantha224@mail.com': 'Madden098!@',
'kbhamil@wowway.com': 'Carol1940',
'email@bjasper.com': 'Lhsnh4us123!',
'biggsbrian@cox.net': 'Trains@2247Trains@2247',
'dzzeblnd@aol.com': 'Geosgal@1',
'jtrego@indy.rr.com': 'Jackwill14!',
'chrisphonte.rj@comcast.net': 'Junior@3311',
'tvwifiguy@comcast.net': 'Bill','defenestrador@mail.com': 'm0rb1d8ss',
'glangley@gmx.com': 'ironhide',
'zmbuohbo@nietamail.com': 'bwhshijvS!7708',
'mzwdxmbr@vecinomail.com': 'yogovhrcS!9604',
'sdwljbvw@senoramail.com': 'fhfmqzwhS!3765',
'bvmqjvxg@menormail.com': 'obcyxskhX!5435',
'vpdsmckd@nietamail.com': 'soivmwqbA!4968',
'rtckyhny@vecinomail.com': 'xxtgawjxX!8484',
'etczzucr@senoramail.com': 'jlgflnfvS!9717',
'muztpwnl@menormail.com': 'xplstfvnA!4629',
'afbzgbqs@nietamail.com': 'hcthlbkkS!9664',
'vwnajvtb@vecinomail.com': 'qpaufpfdX!6846',
'ndnxnqst@senoramail.com': 'uamvwtvxY!4448',
'aehbzvtn@menormail.com': 'pdzabldbX!1586',
'yuofldqp@nietamail.com': 'uumnzcoqA!9950',
'iryxsvsg@vecinomail.com': 'hcnkpndqY!3869',
'adeppaas@senoramail.com': 'qdjmsbtrY!8595','vbrexarm@menormail.com': 'mpyxepysX!5838',
'uiwedngh@nietamail.com': 'xenlwbqqX!3150',
'kgwbdctw@vecinomail.com': 'vgnbhgclX!7983',
'yxjcdhet@senoramail.com': 'ykfdidaiY!2510',
'hfrtvmrz@menormail.com': 'cirrohtjY!3834',
'mpudwtru@nietamail.com': 'ofdhcbjqX!8197',
'eoulmbhe@vecinomail.com': 'wdcytnqaY!2858',
'diniduks@senoramail.com': 'qdatfzqaS!4552',
'acpidkkq@menormail.com': 'slownwabX!7663',
'nkpswjsb@nietamail.com': 'tjyaixxvY!7554',
'charlotte2850@hotmail.com': 'kelalu2850',
    'gdfds98@mail.ru': '1CtFuHTaQxNda8X06CaQ',
    'dfsdfdsfdf51@mail.ru': 'SXxrCndCR59s5G9sGc6L',
'aria.therese.svensson@mail.com': 'Zorro1ab',
'taterbug@verizon.net': 'Holly1!',
'ejbrickner@comcast.net': 'Pass1178',
'teressapeart@cox.net': 'Quinton2329!',
'liznees@verizon.net': 'Dancer008',
'olajakubovich@mail.com': 'OlaKub2106OlaKub2106',
'kcdg@charter.net': 'Jennifer3*',
'bean_118@hotmail.com': 'Liverpool118!',
'dsdhjas@mail.com': 'LONGHACH123',
'robitwins@comcast.net': 'May241996',
'wasina@live.com': 'Marlas21',
'aruzhan.01@mail.com': '1234567!',
'rob.tackett@live.com': 'metallic',
'lindahallenbeck@verizon.net': 'Anakin@2014',
'hlaw82@mail.com': 'Snoopy37$$',
'paintmadman@comcast.net': 'mycat2200*',
'prideandjoy@verizon.net': 'Ihatejen12',
'sdgdfg56@mail.com': 'kenwood4201',
'garrett.danelz@comcast.net': 'N11golfer!',
'gillian_1211@hotmail.com': 'Gilloveu1211',
'sunpit16@hotmail.com': 'Putter34!',
'fdshelor@verizon.net': 'Masco123*',
'yeags1@cox.net': 'Zoomom1965!',
'amine002@usa.com': 'iScrRoXAei123',
'bbarcelo16@cox.net': 'Bsb161089$$',
'laliebert@hotmail.com': 'pirates2',
'vallen285@comcast.net': 'Delft285!1!',
'sierra12@email.com': 'tegen1111',
'luanne.zapevalova@mail.com': 'FqWtJdZ5iN@',
'kmay@windstream.net': 'Nascar98',
'redbrick1@mail.com': 'Redbrick11',
'ivv9ah7f@mail.com': 'K226nw8duwg',
'erkobir@live.com': 'floydLAWTON019',
'Misscarter@mail.com': 'ashtray19',
'carlieruby10@cox.net': 'Lollypop789$',
'blackops2013@mail.com': 'amason123566',
'caroline_cullum@comcast.net': 'carter14',
'dpb13@live.com': 'Ic&ynum13',
'heirhunter@usa.com': 'Noguys@714','koladad357@gmail.com': 'Denia020121',
'sherri.edwards@verizon.net': 'Dreaming123','rami.rami1980@hotmail.com': 'ramirami1980',
'jmsingleton2@comcast.net': '151728Jn$$',
'aberancho@aol.com': '10diegguuss10',
'dgidel@iowatelecom.net': 'Buster48',
'gpopandopul@mail.com': 'GEORG62A',
'bolgodonsk@mail.com': '012345678!',
'colbycolb@cox.net': 'Signals@1','bepenisha@hotmail.com':
'Mereherg',
'Mishanuhka@hotmail.com':
'MishaBeregin',
'bemjaelde@outlook.com':
'Merenken',
'Emadeleber@hotmail.com':
'hasmen11',
'vfuttriwd@outlook.con':
'Amerin77',
'keshder@hotmail.com':
'Berman99',
'beshkefa@hotmail.con':
'Erkamen33',
'r33tgfgheefg@hotmail.com':
'beshurwqw44',
'fufhuhihpgr@hotmail.com':
'urhirehhrp66',
'reggrfgfu@outlook.com':
'reggrfgfu55',
'uregurg@outlook.com':
'irqggrigr54',
'ffvrrwgwe@outlook.com':
'uewgeuigyi65',
'bfrireieu@outlook.com':
'uuhhqrigh65',
'Ehhsjsgwbwh@outlook.com':
'jshwjwjwh5',
'Jegwjwhwh@outlook.com':
'hsjsnajsgsbjs55',
'ehhsjsgwbwh@outlook.com':
'uegsjshshsh56',
'Idgwnwgv@outlook.com':
'hssbjsgsbshsg56',
'Hejsjshdjh@outlook.com':
'jehdjsjwhbsjshs57',
'Jdjsksjsbsjjs@outlook.com':
'Shgwjshsvsh56',
'Hsyevsjshsh@outlook.com':
'eugehwhsgshs58',
'Shsjsfvs@outlook.com':
'sjgewjhwbeheh56',
'Jrhenejhebe@outlook.com':
'jdgsbshdgdh56',
'Ushsjshdhdj@outlook.com':
'jsgssjjshwjwj52',
'Rjgsjajshsjs@outlook.com':
'hsvsjehsbsjdhd67',
'Hdbdjshsbwbsh@outlook.com':
'jshsnshsgsbshwgg5',
'Nshbdndhdg@outlook.com':
'djhdbdjsjshsbsj65',
'Diegbnwhwbwh@outlook.com':
'kdgsj4shsgsbs5',
'Firuebejwgb@outlook.com':
'djshebjshsbe56',
'Irhehejsgwbhw@outlook.com':
'shhwvejsjsbsj56',
'Jrhsjwiegeje@outlook.com':
'rkrjhenejeh6',
'Urhehejeheh@outlook.com':
'ekjsbwsjhs5',
'Idhhshegdbwh@outlook.com':
'jdhebwnehbeje56',
'Jdhsbekehve@outlook.com':
'3jjevwbwheg',
'Jrhbenehsgshs@outlook.com':
'jfhdbej5',
'Iwhwbwhsgbw@outlook.com':
'jdhsvsbshe34',
'Jfhdbejehev@outlook.com':
'djgsbwhegebe5',
'Gehehdgdhjh@outlook.com':
'orhebwjsgev56',
'imbalik14@gmail.comimbalik':
'imbalik756',
'qwartsydtuyfug@outlook.com':
'estrdfigoihopnm',
'dfwvjhkjblin2387@outlook.com':
'dsftuyieiwv7',
'tegvrvirfviollflbg@outlook.com':
'fewhuoihon;ggg',
'tgyhukilgfgfgbkfkbj@outlook': 'com-ftrueyviuaewbilc',
'rgjvrebflgrthggoutlook.com':
'vhjkbhbff7',
'dfsekyuvlu@outlook.com':
'fhkfduvdfbu3u8',
'kfduylgi@outlook.com':
'jyU4?nS?Cv4mMdF',
'cdghdvdvhdhv@outlook.com':
'hjk/l;Dfgfg','raumonatuhadi@mail.ru': 'a7r6U9J6KHDaguAsidDH',
    'floworadpewoodvi@mail.ru': 'ZcyUg5MUq8jMr9i8aST1',
    'letzegebquirdisnui@mail.ru': 'abniAcbrCjRskpysMc75',
    'millveramontmoni@mail.ru': 'bLd8Zg4tqfxmUq7KW5jW',
    'letkixipromnussi@mail.ru': 'bNraxddiagE9Sx23SxYt',
    'hotriosmartraverba@mail.ru': 'cALqh0bjnPefyiu7WL0v',
    'pillgemisscritcomsa@mail.ru': 'dHBUrMg6aqXhvx0m1cVf',
    'leigedeamvebig@mail.ru': 'dVTsGqDbZYbjse9iHNR2',
    'knocrufridunringgent@mail.ru': 'dn333DbbuEfGnqw08Rxm',
    'tworensodiapansaa@mail.ru': 'dsGajJE1TtiAGgZsgyvQ',
    'korlithiobtennick@mail.ru': 'feDLSiueGT89APb81v74',
    'terbgebuoviror@mail.ru': 'gaqaKs06xg22kkXXW2LU',
    'tioreibunthandvahear@mail.ru': 'ggKygTjxSLzwm4tWd43B','korlithiobtennick@mail.ru': 'feDLSiueGT89APb81v74',
    'avyavya.vyaavy@mail.ru': 'zmARvx1MRvXppZV6xkXj',
    'gdfds98@mail.ru': '1CtFuHTaQxNda8X06CaQ',
    'dfsdfdsfdf51@mail.ru': 'SXxrCndCR59s5G9sGc6L',
 'lovedel.anisss@mail.ru': 'cJkiz18MAWS0L85DGW8n',
           'love.efs@mail.ru': 'vzw5bwePbzeXhYhDeeA1',
           'fsadfsaf.sdfasdfas@mail.ru': 'KUN0wpJbViwpFXFPkHb4',
           'fkjvfmdsof@mail.ru': 'CxM2JUT0vx03aSyD53Ns',
           'sawage.dasha@mail.ru': 'SyfStmkgK29KUB0BQVAy',
           'opunm.sdaww@mail.ru': 'Y1BjSZCHeLTxmvaW49FH',
           'fall.gall@mail.ru': 'tFqTgMUqkidcBbw91hD7',
           'wzxcvd@mail.ru': 'vwPUnRUGW75MUKaFzhVc',
           'masha.mashala@mail.ru': 'rtM0rCSHZstDVQpxmEkh',
           'wwagege@mail.ru': 'ZZNkRLrZseLN57phVeEQ',
           'irigjfodjdkdkk@mail.ru': 'n8r0TKCygC5xqaWxStr1',
           'sdfghafdhg@mail.ru': 'Kag0fefn6mFWMzQ17PGb',
           'dasha.goat@mail.ru': '3bkf9iHyuFUfEfKzXYLm',
           'dasha.sasaas@mail.ru': 'UAVwCgpFXaD2zcQ9gVSE',
           'dasha.lovely.02@mail.ru': 'paUrCHANKWWxefzaQvQm',
           'dasha.butifull@mail.ru': '0bAbKQUfpVRDcrLtc0Ya',
           'firirotifigj@gmail.com': 'RQCgW8vb127AGRZ5Kvf1',
           'dasha.mdaaa@gmail.com': 'HXNg0M0bvyaEs1tbMjTB',
           'lfwgdg@mail.ru': 'h6hAUvp3KNPqqcmmduU3',
           'dasha.holle@mail.ru': '0g5g6kwEtkKw2hYCaSTj',
           'darya.holly@mail.ru': 'he02duEXu4iiDambB6ZG',
           'dasha.vonk@mail.ru': 'AayKrKyfEDyeubmRqKRm',
           'kloxc@mail.ru': 'FVUeii2MdbNcqEmZr','lovedel.anisss@mail.ru': 'cJkiz18MAWS0L85DGW8n',
           'love.efs@mail.ru': 'vzw5bwePbzeXhYhDeeA1',
           'fsadfsaf.sdfasdfas@mail.ru': 'KUN0wpJbViwpFXFPkHb4',
           'fkjvfmdsof@mail.ru': 'CxM2JUT0vx03aSyD53Ns',
           'sawage.dasha@mail.ru': 'SyfStmkgK29KUB0BQVAy',
           'opunm.sdaww@mail.ru': 'Y1BjSZCHeLTxmvaW49FH',
           'fall.gall@mail.ru': 'tFqTgMUqkidcBbw91hD7',
           'wzxcvd@mail.ru': 'vwPUnRUGW75MUKaFzhVc',
           'masha.mashala@mail.ru': 'rtM0rCSHZstDVQpxmEkh',
           'wwagege@mail.ru': 'ZZNkRLrZseLN57phVeEQ',
           'irigjfodjdkdkk@mail.ru': 'n8r0TKCygC5xqaWxStr1',
           'sdfghafdhg@mail.ru': 'Kag0fefn6mFWMzQ17PGb',
           'dasha.goat@mail.ru': '3bkf9iHyuFUfEfKzXYLm',
           'dasha.sasaas@mail.ru': 'UAVwCgpFXaD2zcQ9gVSE',
           'dasha.lovely.02@mail.ru': 'paUrCHANKWWxefzaQvQm',
           'dasha.butifull@mail.ru': '0bAbKQUfpVRDcrLtc0Ya',
           'firirotifigj@gmail.com': 'RQCgW8vb127AGRZ5Kvf1',
           'dasha.mdaaa@gmail.com': 'HXNg0M0bvyaEs1tbMjTB',
           'lfwgdg@mail.ru': 'h6hAUvp3KNPqqcmmduU3',
           'dasha.holle@mail.ru': '0g5g6kwEtkKw2hYCaSTj',
           'darya.holly@mail.ru': 'he02duEXu4iiDambB6ZG',
           'dasha.vonk@mail.ru': 'AayKrKyfEDyeubmRqKRm',
           'kloxc@mail.ru': 'FVUeii2MdbNcqEmZrq7N',
           'proto.dasha@mail.ru': 'LqJt4xXtqaAxUsd4D1HD',
           'dportq@mail.ru': 'CRUJZ7gi37VFn6a9mmYx',
           'dasha.port.06@mail.ru': 'Cnsy43cXqbAGVUswWdig',
           'portuyeye@mail.ru': 'y2jPgBkCxLuDBiHU2cAV',
           'dlegoyy@mail.ru': 'NtX9FmVJDi8fsBusv16Z',
           'portee05@mail.ru': '2eiDAier2n1MBrf1MZiX',
           'flipov.vlad@mail.ru': 'yePH6i1Sxw7XiYjR3E5K',
           'msolhov@mail.ru': 'RzQcdrRwYaJqycuxHzxM',
           'aslocv@mail.ru': 'i7n8zk8Dy0E9v7Sx2wLX',
           'kagbxz@mail.ru': 'vYkY8mrbqxGzpz8NqXe7',
           'mardjela@mail.ru': 'Cug2mXZ5d4c8aLNfnwCR',
           'egsdfdg@mail.ru': 'kCYudJg4P1KYF7iLkgcK',
           'ejofree@mail.ru': 'YKxiqwNwA87DEf8VftHF',
           'lina.fdfsfg@mail.ru': 'ts4JsHZhPf2vZ8rqxhmr',
           'abfdgs@mail.ru': 'vqdEDLtXpTU784KqLcvF',
           'pgkksdg@mail.ru': 'qfs6Nrg2zG2Zfudt8idz',
           'vadgadg@mail.ru': 'VkM3a1GpPaABr84PCztb',
           'jake.nod@mail.ru': '39uS26JTgKrBWJFdC16h',
           'noah.soli@mail.ru': 'xXvHn9usximafHmt4Rup',
           'jdlodd@mail.ru': 'rcAxee0FtnzL0wf4qUuX',
           'mmardjela@mail.ru': '3fhUwHBWipHasch29fv0',
           'andrea.aalto@mail.ru': 'XJrFhNwPamYaz6mjJ6yT',
           'luca.velde@mail.ru': 'cEeCv1mtP8Y2fsL4F1Xf',
           'esolhov@mail.ru': 'HB3zF1mz1H7EDEfinhdi',
           'fdfsfg04@mail.ru': 'hSrWxzjRWBLDYuPAB60F',
           'amardjela@mail.ru': 'rmyndAbyj7e5gjg3queN',
           'mrashni@mail.ru': 'Gukjw4sbwCrgAgFaZzx1','ugtnddpzej@rambler.ru':'9506681adi6MU',
'cisvzeeuyg@rambler.ru':'6301453fJo4s9',
'ggflngvlih@rambler.ru':'22408953S2gby',
'nvynpxnkkd@rambler.ru':'2510571xHHdgR',
'fjzoyuouuz@rambler.ru':'59097784rDPPd',
'bzgqlptwhl@rambler.ru':'0816705Tr1FYG',
'vigzkazhat@rambler.ru':'31932120MtFlm',
'afgunihnfe@rambler.ru':'9061194g5B45C',
'ngvxtwpesz@rambler.ru':'2011142rqGxFR',
'egvwsdlkyr@rambler.ru':'9037151L6w49u',
'tfdmxqejns@rambler.ru':'7787340bbA3sL',
'thrcxqfhxt@rambler.ru':'4033354R50aaM',
'gzbsslvpgb@rambler.ru':'8608390st77PG',
'vgwkozobgf@rambler.ru':'0713430AUe0Jj',
'xthokzcxta@rambler.ru':'0362278TxeHl1',
'ulgtgyesux@rambler.ru':'4621758slMQ2q',
'mekpwikznr@rambler.ru':'3416279IFmuKQ',
'clgplzxnqw@rambler.ru':'6412121gc7Dcu',
'azfingoovg@rambler.ru':'6148697BuRbwO',
'xfjhvzmnac@rambler.ru':'9670930pBIR7W',
'thgwrxhltj@rambler.ru':'2369423cUvLuf',
'agpjaemyqm@rambler.ru':'6572399A8cFh6',
'wvicwdopps@rambler.ru':'7661495MeRn88',
'kpuaeogels@rambler.ru':'02848019U4yxH',
'dzdhnhsfia@rambler.ru':'6976310gzYoE2',
'vlldcxigrj@rambler.ru':'9022806maOtUs',
'hlfczgnfrr@rambler.ru':'9916462168Ypp',
'jtmtruwscg@rambler.ru':'9923365hkHeN6',
'aozzmmsvvi@rambler.ru':'0399945jLmU7B',
'nglqkjipix@rambler.ru':'0058167GPjOZR',
'dxldwtdips@rambler.ru':'4221180vuJqsB',
'fnymojqdux@rambler.ru':'4820302GP03Ru',
'elvyorfunb@rambler.ru':'9023694jkXJV4',
'yiredoekax@rambler.ru':'3543487Cm2P2a',
'hpobxpntkg@rambler.ru':'9360288IzyHkP',
'owbsixedjj@rambler.ru':'6443042VnSBeS',
'hgwptrmpwz@rambler.ru':'9923510OpfY1W',
'cyblanwvop@rambler.ru':'5825453FKm1ZE',
'uwtjezecrs@rambler.ru':'6411755QBcF7p',
'ybjbggdruu@rambler.ru':'4065298o86MLm',
'uckmapemvh@rambler.ru':'9531228JLg96F',
'jkjportalx@rambler.ru':'2401077inLnJj',
'kolnanjvkw@rambler.ru':'86294929rsQvg',
'rhzlhaagsc@rambler.ru':'03837749f9qvW',
'fdroghhuoy@rambler.ru':'13627259IrATl',
'jhripippie@rambler.ru':'8596550xkdTvR',
'ghjullwyxo@rambler.ru':'7784503Dl60Kl',
'srdicexvfo@rambler.ru':'8943491TEOSke',
'jgxvvtcsvi@rambler.ru':'2851226DI6zY5',
'krihsllwpz@rambler.ru':'4272238ts9X3z',
'jolonbfrbl@rambler.ru':'2637507DppJyT',
'uqblakalnx@rambler.ru':'3735373NSS8lz',
'owiwwvgrrx@rambler.ru':'0592924zRhm4W',
'qtjwomftjv@rambler.ru':'6049164OqDaxz',
'aiosomfxks@rambler.ru':'6919172lA1N45',
'xmqrrmybdl@rambler.ru':'5597456YOjL0c',
'lkawwbtmaj@rambler.ru':'0796449gknSFs',
'lomxgjndyr@rambler.ru':'2467557Ib1ZVu',
'jqwcsddyrg@rambler.ru':'1102645xGeLhj',
'kacftekdeq@rambler.ru':'0261527ivGs1S',
'alazchgdiv@rambler.ru':'9751444kT01fm',
'vgymcieuft@rambler.ru':'3312197YSGrOc',
'cogyjubzkl@rambler.ru':'0174602bkNHod',
'weinejwyir@rambler.ru':'0637170gHYLdN',
'uxsoazzpwb@rambler.ru':'4936893zRSsTC',
'sbbzmlvdgo@rambler.ru':'2224249cGnGIv',
'ymycqoegto@rambler.ru':'4818009OHorIl',
'vqueaeveat@rambler.ru':'50476661392iV',
'vunvhfkbks@rambler.ru':'6880622LYLbfc',
'xjetfnzjhi@rambler.ru':'0518737rzBvTd',
'liekddtuws@rambler.ru':'5819586i6eSoS',
'ycencrfdxd@rambler.ru':'1051144aZoHRP',
'bpkishuvbc@rambler.ru':'5154664Vwi6Ua',
'wsnypwafbt@rambler.ru':'9707576JDK9Fw',
'oytrjytdpr@rambler.ru':'0906843MAu7RU',
'smeaipdrpu@rambler.ru':'5648933ztPS6u',
'fmyzcbctri@rambler.ru':'3308444zi68By',
'iurqgpxynb@rambler.ru':'8366202xmgCYS',
'wqhcmaknrv@rambler.ru':'0502120gdP9zL',
'fbnkspvdjz@rambler.ru':'7945888mcrStg',
'hpbpeeptcc@rambler.ru':'3788419Pc252T',
'xksxdxwdze@rambler.ru':'7078149cqEy4T',
'wdpuletfdl@rambler.ru':'5322696L0N9l9',
'bziqrktkhy@rambler.ru':'3246091kgTTaZ',
'saelakwdmc@rambler.ru':'0563798ptrtSN',
'anitjpnnos@rambler.ru':'7990575MCToVl',
'ixvpbrsnyd@rambler.ru':'95615495uwOsN',
'ifrxkefqxo@rambler.ru':'1264966unxLRo',
'mhqgjgjxvv@rambler.ru':'2226251mpDJ9n',
'uowohxbqei@rambler.ru':'3504468bIHRWV',
'cvdkpcwdmq@rambler.ru':'6488683AEsgdG',
'qxnrsosnwp@rambler.ru':'0370763iQaWfn',
'opnvudfwap@rambler.ru':'1873848oOgVLA','pswrzpjlnj@rambler.ru':'4119723UWtRMq',
'lvhqxrbyjx@rambler.ru':'9096999IwuiNK',
'iiuphvfjck@rambler.ru':'6800251g3qPxP',
'szlbpfqfnu@rambler.ru':'57915343pGk9Z',
'kmnsazmofd@rambler.ru':'9881154UFzUnz',
'xlngvgdfyy@rambler.ru':'8503734lIaDOq',
'toksegumgm@rambler.ru':'1206136M2pgxK',
'lzxweynvmk@rambler.ru':'0656844M8Ua7r',
'piltwbqahv@rambler.ru':'1571843HwjOy5',
'rwbqxcjhij@rambler.ru':'2627820ygMv0p',
'ybxdyezeaw@rambler.ru':'8683132Fm75um',
'rhlumlbqxc@rambler.ru':'0502630CYEngx',
'qstvhreejj@rambler.ru':'2436299apZbqS',
'cpldnzlqgs@rambler.ru':'7520506dxK7nW',
'eumghdgkgm@rambler.ru':'5129031GzG03Z',
'qwfahkwfjh@rambler.ru':'7088021Myistn',
'twhvlnbtvt@rambler.ru':'9399429GaJJa4',
'jhddwfikgw@rambler.ru':'1393287IB0PZo',
'pzvrccwdbm@rambler.ru':'7758769ekQe1f',
'shwrdzijmf@rambler.ru':'3873842XH3bgL',
'vbuigzynnm@rambler.ru':'3856920aHzE4A',
'ztwiwilejq@rambler.ru':'8616981WYFTCk',
'vuszmpdppy@rambler.ru':'7726003c24PVz',
'dacoapnvnt@rambler.ru':'81066143Zm1fp',
'apkjscfntk@rambler.ru':'3546871Y7Bk0w',
'oainbrnnrp@rambler.ru':'84346062U6MFe',
'pidhhlesak@rambler.ru':'5135415L1Dnqt',
'ehwulsfufl@rambler.ru':'5801265ubPOzK',
'irzgfdicah@rambler.ru':'3719696WyxpXh',
'yzjduaakxc@rambler.ru':'2438994ACJaub',
'hodqdiuklo@rambler.ru':'767841344A1tF',
'nzlqpjwpot@rambler.ru':'6915997SUqN84',
'xhvhvjqvrt@rambler.ru':'17843148GoORZ',
'opbghlryyi@rambler.ru':'6187779N2tt8r',
'vbzayzmnnz@rambler.ru':'2765133rIsG4W',
'wnmuqoxgvg@rambler.ru':'4030133AjIHEa',
'fwczlkjeqx@rambler.ru':'6138606ClwDQY',
'mdmspcvyaw@rambler.ru':'0098146Yud02L',
'hrdswjzgqw@rambler.ru':'0856046puV88r',
'xyqgrjswfr@rambler.ru':'81996872YvIq7',
'entkfoopcd@rambler.ru':'5336523l9K1n2',
'djtueljvss@rambler.ru':'9936980wtNXfX',
'dzmctubwws@rambler.ru':'4622840Q7HZyO',
'wzuwzzgnvl@rambler.ru':'6153631PNMlBx',
'rmtcqdgvnd@rambler.ru':'9338592pDQDSq',
'cmueytlsbc@rambler.ru':'5897484z7lKrY',
'prpsvvroci@rambler.ru':'2722168RHYhcx',
'juyhlrlzvt@rambler.ru':'1838830ziEfOH',
'ofuggpdykx@rambler.ru':'8520503CZNHjV',
'qfjwtjbhpo@rambler.ru':'4156828Jf4enw',
'rwrwswudhv@rambler.ru':'8266122J4AqLc',
'xxyxszaaqr@rambler.ru':'11798633kGF38',
'zlhlyybkbp@rambler.ru':'5168039gkHAkf',
'zrajbxewkt@rambler.ru':'01285925IinUA',
'lybjgnaaqg@rambler.ru':'6251735AhBL0N',
'twivzuqoth@rambler.ru':'8953852Squ69v',
'ifachrohjq@rambler.ru':'6493652wiEikB',
'myjhbsfeen@rambler.ru':'627375988utRh',
'mgitqvmqpn@rambler.ru':'0551846dwPIRy',
'wihhibhnzt@rambler.ru':'6339855JrieYb',
'wqyqfejfde@rambler.ru':'8320490aKnTOl',
'ppnzdnsaex@rambler.ru':'5946797PCCQbt',
'xgfwhtiodv@rambler.ru':'1076982D2fVan',
'jtbkavwonp@rambler.ru':'2167743FHBnvK',
'jhgnpipwzi@rambler.ru':'0213954Bb6HLN',
'jfnbeyfmap@rambler.ru':'1833567Xfs3Zz',
'jzpvhqpeou@rambler.ru':'2582828Fqk74i',
'zkoyaouflp@rambler.ru':'0837359dfuJlw',
'xjlijveaic@rambler.ru':'0433010ACosxN',
'fgqkunnxuf@rambler.ru':'7050015TdukKM',
'wjujeqszmu@rambler.ru':'6801665tMQsNw',
'myfdfokpcq@rambler.ru':'9580174PIIaDB',
'dbwzzwreaw@rambler.ru':'4503607jKRRxg',
'kzjffhsqzm@rambler.ru':'7541663G4h8ff',
'ogwwxhodgp@rambler.ru':'9026462cBffsb',
'orbqllwfic@rambler.ru':'7731849gMxIRX',
'lkjryvlrkk@rambler.ru':'4584518olcMQd',
'kcwzjfymsg@rambler.ru':'2697206gH7N2j',
'mpidmygqpw@rambler.ru':'8743805dkRTHf',
'upuvifnpgv@rambler.ru':'8995521oep4fI',
'daktrhbkhx@rambler.ru':'7299608dROBrL',
'hsgcdmawhg@rambler.ru':'9049438FM4AwM',
'izyqvsqgyb@rambler.ru':'5061241OrRQvL',
'jmakpgklid@rambler.ru':'6306172L1vo7F',
'vojzlsygaw@rambler.ru':'68760161Y5Qc1',
'xissuvpdsw@rambler.ru':'8463274QCOysy',
'bfrqorylrl@rambler.ru':'7007968e6zR4D',
'ussakdyclz@rambler.ru':'9126092iyxMtf',
'dlvnuoywwi@rambler.ru':'6650255RQm6PZ',
'kwhypobcqy@rambler.ru':'6753512Zu3QqH',
'ijzhqfpxfd@rambler.ru':'9982131JljUpU',
'onjukiabwr@rambler.ru':'9999847KmBCcq',
'axwoyxhehh@rambler.ru':'5593617efqURG','ktcbvgmedu@rambler.ru':'6584452BrQ969',
'oeljddjwqv@rambler.ru':'7386064fCZMlz',
'mddougbwlb@rambler.ru':'6873332TIeG8F',
'tpocbfvyre@rambler.ru':'9675226LFKwRO',
'pqmsonwrrx@rambler.ru':'2415353VkimGL',
'lzpvenpnur@rambler.ru':'4494046oos6kD',
'evsrczefvq@rambler.ru':'1981259DsjrsG',
'dkebyytjrl@rambler.ru':'5720478lk3u9X',
'bdmxcbyjgt@rambler.ru':'7240932V5fVZR',
'tpzaoqtayx@rambler.ru':'9676101I3Af84',
'kcujemkfnl@rambler.ru':'6632444LCeeuA',
'cpkaqjxlaq@rambler.ru':'8158799QlPzh8',
'omlllacuhf@rambler.ru':'1984022BFd4qb',
'kashdhmtvv@rambler.ru':'390755782Rn04',
'imqqmtuggk@rambler.ru':'9357633G6MyYn',
'uaiodcrerw@rambler.ru':'2461236zuhlDx',
'oqputgndap@rambler.ru':'20692247SGS8a',
'gbqlutzdca@rambler.ru':'9768268oRiSSw',
'ktesatgssv@rambler.ru':'0684725Mf7VKP',
'jiynakjgyd@rambler.ru':'3637610o5Kl4P',
'pmqkykszvg@rambler.ru':'5466953jvGECw',
'sxpqnbxfgt@rambler.ru':'4265394mLYBoX',
'owlatdcvap@rambler.ru':'68425495iJVl4',
'zivdifdmja@rambler.ru':'5017633pews8P',
'iigbhtwffd@rambler.ru':'0158311HUDci2',
'iqolabntmj@rambler.ru':'3696752WtpCBQ',
'udxkikhenc@rambler.ru':'5230944pVpJa1',
'tdainafogs@rambler.ru':'1479817xdFEa3',
'ddhavbgovc@rambler.ru':'35963964uL6Zx',
'dyxxnlddri@rambler.ru':'9835924OFo82U',
'szqhbtahdj@rambler.ru':'9732972Pf7YVX',
'pheilxtzdp@rambler.ru':'3798892ibIhLo',
'guruesnrny@rambler.ru':'1127416a5kN1S',
'canlrwmbtz@rambler.ru':'4495454pfHMxR',
'bviylhwmpg@rambler.ru':'06152842r2KmG',
'tjqmzvvflj@rambler.ru':'63963647Gl8FG',
'ktqwcmuazg@rambler.ru':'69655371OYt77',
'mbyinljbwq@rambler.ru':'5072263iMw2V4',
'lmyjnbydqx@rambler.ru':'34786225dlQ55',
'lxsfwyruiy@rambler.ru':'9489974ssFXqn',
'wzwgcufsoo@rambler.ru':'5826393KfInE7',
'vvbuqwqied@rambler.ru':'4249236pewtC9',
'gqwirofmjf@rambler.ru':'9283282nbQ5GK',
'vqevacjnsv@rambler.ru':'4899725kM8rKT',
'effhddiqal@rambler.ru':'1512943nrY5TN',
'qrznkghzmx@rambler.ru':'1741706Kwrx4H',
'ogusnctnhf@rambler.ru':'2394265lm1Hc9',
'kqvlzvqazc@rambler.ru':'1717008paBOnL',
'daowvtpzek@rambler.ru':'2346534Jp8NHl',
'wbbipzhzyw@rambler.ru':'0543120bJl0Ly',
'rgpbonfqhj@rambler.ru':'3976206M39T8v',
'bmoouqbpxl@rambler.ru':'0961594LTt87j',
'iruxmqpkpo@rambler.ru':'6742659p9KCnW',
'xjzaxqyscz@rambler.ru':'1813628QLnV8k',
'cxzguplstz@rambler.ru':'0472468DITsU2',
'zmutrpskzc@rambler.ru':'9061032Q8XkOc',
'lihtyubtis@rambler.ru':'9067530mwE2Z4',
'uquacqlvrh@rambler.ru':'4995515zgvYk2',
'dxdcwfjkwr@rambler.ru':'0997427IdH9If',
'mylkzncdqz@rambler.ru':'0554174SF6hxH',
'xozdfwxdge@rambler.ru':'1594107UC4cgp',
'qxlskakyrw@rambler.ru':'8329586GRn1yg',
'sqjmzkqplu@rambler.ru':'7977820Rg4Cug',
'kiowipszrh@rambler.ru':'7440327xnshaY',
'yvcrwkrqkt@rambler.ru':'2188228LqV5iL',
'konxlfvxck@rambler.ru':'8001466E1E0pt',
'eeucoepqwx@rambler.ru':'4221996BHGqkQ',
'rbwnajwssb@rambler.ru':'4418291q0pO9Q',
'itdgtxpyeb@rambler.ru':'0510139bJgNxi',
'bavuuusibh@rambler.ru':'2133928qDHF3K',
'cssgkgwhqa@rambler.ru':'959014174qXG3',
'grczehsbgy@rambler.ru':'1833927GccUgh',
'tyqpgkrbna@rambler.ru':'3223661odePym',
'qezgkdoceq@rambler.ru':'1749341rGotmB',
'erdbokiyrq@rambler.ru':'1240186YA1lCN',
'mfyosvypfx@rambler.ru':'1529362HjySLq',
'vkeobbnpfh@rambler.ru':'57391160fYOkj',
'jqfzgmsoke@rambler.ru':'1665323tNhxlq',
'jrfckizumd@rambler.ru':'30295639Cn7jn',
'tdtofzbxyc@rambler.ru':'9432737zEA3Rb',
'tlolhafizf@rambler.ru':'8187560T7iX8Z',
'fbgtygfvbo@rambler.ru':'4817024n9Yryi',
'kbfcsxpand@rambler.ru':'4797454CkXl1P',
'fcyihdhjzp@rambler.ru':'7845590y1Zuno',
'uvjdqhnpyy@rambler.ru':'2131196Dt7lht',
'jwfckuaxnu@rambler.ru':'8383081Q2nlnM',
'oofbwmgsvu@rambler.ru':'4079597yfVFqq',
'wiwortjxrd@rambler.ru':'8492478BXG5Of',
'acydvhsizp@rambler.ru':'6810797R0lapH',
'exhizlkrsq@rambler.ru':'0349949mrAsUY',
'cqawqlpwuf@rambler.ru':'8359817P9sAAi',
'ypdcseqdes@rambler.ru':'2980191OengK3',
'hhatkdcenx@rambler.ru':'1871876PG0TbF',

}
receivers = ['abuse@telegram.org',
    'dmca@telegram.org',
    'recover@telegram.org',
    'security@telegram.org',
    'sms@telegram.org',
    'sticker@telegram.org',
    'support@telegram.org']

banner = '''
Основной код снocера: XASANOV
Официальный порт на LiteHack: @error_kill

[1] СНОС АКК0В         [2] СНОС КАНАЛ0В
[3] СНОС Б0Т0В         [4] СНОС ЧАТОВ

'''

color_code = {
    "reset": "\033[0m",  
    "underline": "\033[04m", 
    "green": "\033[32m",     
    "yellow": "\033[93m",    
    "red": "\033[31m",       
    "cyan": "\033[36m",     
    "bold": "\033[01m",        
    "pink": "\033[95m",
    "url_l": "\033[36m",       
    "li_g": "\033[92m",      
    "f_cl": "\033[0m",
    "dark": "\033[90m",     
}   

alignment = "{:>50}".format(banner)
banner = Colorate.Horizontal(Colors.green_to_black, alignment)
print(banner)

def send_email(receiver, sender_email, sender_password, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        if 'gmail.com' in sender_email:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
        elif 'rambler.ru' in sender_email:
            smtp_server = 'smtp.rambler.ru'
            smtp_port = 587
        elif 'hotmail.com' in sender_email:
            smtp_server = 'smtp.office365.com'
            smtp_port = 587
        elif 'mail.ru' in sender_email:
            smtp_server = 'smtp.mail.ru'
            smtp_port = 587
        else:
            raise ValueError("Unsupported email provider")
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver, msg.as_string())
        server.quit()
        
        return True
    except Exception as e:
        return False

def main():
    sent_emails = 0
    print(f'{color_code["red"]}[:D]{color_code["bold"]} выбирай >{color_code["yellow"]} ')
    choice = input()

    if choice == '1':
        print("1. ЗА СПАМ, РЕКЛАМУ")
        print("2. ЗА ДОКСUНГ")
        print("3. ЗА ТРОЛЛUНГ(ОСК)")
        print("4. ПР0ДАЖА/РЕКЛАМА НАРК0ТЫ")
        print("5. КУРАТ0РСТВО В НАРК0ШОПЕ")
        print("6. ПРОДАЖА ЦП")
        print("7. ВbIМ0ГАНUЕ UНТUМНЫХ ФОТО У НЕСОВЕРШЕННОЛЕТНUХ")
        print("8. УГНЕТАНUЕ НАЦИИ")
        print("9. УГНЕТАНUЕ РЕЛUГUU")
        print("10. РАСПР0СТР0НЯЕТ РАСЧЛЕНЕНКУ")
        print("11. РАСПР0СТР0НЯЕТ ЖUВОДЕРКУ")
        print("12. РАСПР0СТР0НЯЕТ ПОРНУХУ")
        print("13. СУТЕНЕР(ШЛЮХ ПРОДАЕТ)")
        print("14. ПРUЗЫВ К САМ0ВbIПUЛУ")
        print("15. ПРUЗbIВ К ТЕРР0РУ")
        print("16. УГРОЗbI СВАТА U ТП")
        print("17. УГРОЗbI РАСПРАВbI")
        print("18. СНОС СЕССИЙ")
        print("19. С ВUРТ Н0МЕРОМ")
        print("20. С ПРEМКОЙ")
        print("21. ПР0СТ0 СН0С (НЕ ЭФФЕКТUВЕН)")
        print("[:D] выбирай > ")
        comp_choice = input()
        
        if comp_choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17" ]:
            print("СЛЕДУЙ УКАЗАНUЯМ")
            print("USERNAME: ")
            username = input()
            print("TG ID: ")
            id = input()
            print("CCbIЛКА НА ЧАТ: ")
            chat_link = input()
            print("ССbIЛКА НА НАРУШЕНUЕ В ЧАТЕ: ")
            violation_link = input()
            cprint("----------------------------------" , "black")
            cprint("АТАКА НАЧАЛАСb" , "red")
            cprint("----------------------------------" , "black")
            comp_texts = {
                "1": f"Здравствуйте, уважаемая поддержка. На вашей платформе я нашел пользователя который отправляет много ненужных сообщений - СПАМ. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушения - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю.",
                "2": f"Здравствуйте, уважаемая поддержка, на вашей платформе я нашел пользователя, который распространяет чужие данные без их согласия. его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение/нарушения - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его акккаунта.",
                "3": f"Здравствуйте, уважаемая поддержка телеграм. Я нашел пользователя который открыто выражается нецензурной лексикой и спамит в чатах. его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение/нарушения - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его акккаунта.",
                "4": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который продает и рекламирует наркотические вещества. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользоателю путем блокировки его аккаунта.",
                "5": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который привлекает людей в сферу нарко-бизнеса. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировни его аккаунта.",
                "6": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который продает порнографические материалы с участием несовешеннолетних. Его юзернейм - {username}, его айди {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
                "7": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который вымогает фото интимного характера у несовершенно летних, его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры к данному пользователю путем блокировки его аккаунта.",
                "8": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который угнетает нацию и разжигает конфликты. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователб=ю путем блокировки его аккаунта.",
                "9": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который угнетает религию и разжигает конфликты. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользоателю путем блокировки его аккаунта.",
                "10": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который распростроняет видео и фото шокирущего контента с убийством людей. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
                "11": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который распростроняет видео и фото шокирующего контента с убийством животных. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
                "12": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который распростроняет фото и видео порнографического типа. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
                "13": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который продает услуги проституции. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
                "14": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который отправляет сообщения которые приводят людей к суициду. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примине меры по отношению к данному пользователю путем блокировки его аккаунта.",
                "15": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который отправляет сообщения с призывом к террризму. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
                "16": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который угрожает людям распростронением личной информации. Его юзернейи - {username}, его айди {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
                "17": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который угрожает людям расправой. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта."
            }
            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[comp_choice]
                    comp_body = comp_text.format(username=username.strip(), id=id.strip(), chat_link=chat_link.strip(),
                                                 violation_link=violation_link.strip())
                    send_email(receiver, sender_email, sender_password, 'Жалоба на аккаунт телеграм', comp_body)
                    cprint(f"ОТПРАВЛЕНО НА {receiver} 0Т {sender_email}", "green")
                    sent_emails += 14888
                    time.sleep(5)

        elif comp_choice in ["18", "21"]:
            print("СЛЕДУЙ УКАЗАНUЯМ")
            print("USERNAME: ")
            username = input()
            print("TG ID: ")
            id = input("")
            cprint("АТАКА НАЧАЛАСb" , "red")
            comp_texts = {
                "18": f"Здравствуйте, уважаемая поддержка. Я случайно перешел по фишинговой ссылке и утерял доступ к своему аккаунту. Его юзернейм - {username}, его айди - {id}. Пожалуйста удалите аккаунт или обнулите сессии",
                "21": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя с подозрительной активностью на аккаунте. Его юзернейм - {username}, его айди - {id}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки аккаунта."
            }

            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[comp_choice]
                    comp_body = comp_text.format(username=username.strip(), id=id.strip())
                    send_email(receiver, sender_email, sender_password, 'Я утерял свой аккаунт в телеграм', comp_body)
                    cprint(f"ОТПРАВЛЕНО НА {receiver} 0Т {sender_email}", "green")
                    sent_emails += 14888
                    time.sleep(5)

        elif comp_choice in ["19", "20"]:
            print("СЛЕДУЙ УКАЗАНUЯМ")
            print("USERNAME: ")
            username = input()
            print("TG ID: ")
            id = input("")
            cprint("АТАКА НАЧАЛАСb" , "red")
            comp_texts = {
                "19": f"Добрый день поддержка Telegram!Аккаунт {username} , {id} использует виртуальный номер купленный на сайте по активации номеров. Отношения к номеру он не имеет, номер никак к нему не относиться.Прошу разберитесь с этим. Заранее спасибо!",
                "20": f"Добрый день поддержка Telegram! Аккаунт {username} {id} приобрёл премиум в вашем мессенджере чтобы рассылать спам-сообщения и обходить ограничения Telegram.Прошу проверить данную жалобу и принять меры!"
            }

            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[comp_choice]
                    comp_body = comp_text.format(username=username.strip(), id=id.strip())
                    send_email(receiver, sender_email, sender_password, 'Жалоба на пользователя телеграм', comp_body)
                    cprint(f"ОТПРАВЛЕНО НА {receiver} 0Т {sender_email}", "green")
                    sent_emails += 14888
                    time.sleep(5)


    elif choice == "2":
        
        print("1. С ЛUЧНЫМU ДАННЫМU")
        print("2. С ЖUВОДЕРСТВ0М ")
        print("3. С ДЕТСКUМ П0РНО")
        print("4. ДЛЯ КАНАЛ0В ТИПА ПРАЙСОВ")
        print("5. С РАСЧЛЕНЕНК0Й")
        print("6. РУЛЕТКU (КАЗUК)")
        print("7. НАРК0-Ш0П")
        print("8. ПРUЗbIВ К ТЕРРОРУ")
        print("9. ПРUЗbIВ К САМ0ВbIПUЛУ")
        print("10. РАЗЖUГАНUE НЕНАВUCTU")
        print("11. ПРОПОГАНДА НАСUЛUЯ")
        print("12. ПРОДАЖА ДЕТСКUХ UНТUМ0К")
        print("13. УГНЕТЕНUЕ НАЦUU")
        print("14. УГНЕТЕНUЕ РЕЛUГUU")
        print("15. С П0РНУХОЙ")
        print("ВbIБUРАЙ: ")
        ch_choice = input()

        if ch_choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]:
            print("ССbIЛКА НА КАНАЛ: ")
            channel_link = input()
            print("ССbIЛКА НА НАРУШЕНUЕ В КАНАЛЕ: ")
            channel_violation = input("")
            cprint("АТАКА НАЧАЛАСb" , "red")
            comp_texts = {
                "1": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал, который распространяет личные данные невинных людей. Ссылка на канал - {channel_link}, ссылки на нарушения - {channel_violation}. Пожалуйста заблокируйте данный канал.",
                "2": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который распространяет жестокое обращение с животными. Ссылка на канал - {channel_link}, сслыки на нарушения - {channel_violation}. Пожалуйста заблокируйте данный канал.",
                "3": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который распространяет порнографию с участием несовершеннолетних. Ссылка на канал - {channel_link}, сслыки на нарушения - {channel_violation}. Пожалуйста заблокируйте данный канал.",
                "4": f"Здравствуйте, уважаемый модератор телеграмма. хочу пожаловаться вам на канал,который продает услуги доксинга, сваттинга. Ссылка на телеграмм канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "5": f"Здравствуйте, уважаемая поддержка Телеграмма. На вашей платформе я нашел канал который распространяет шокирующие кадры убийства людей. Ссылка на телеграмм канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "6": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который распростроняет рулетки или же казино, которые запрещены на территории РФ статьей 171 УКРФ. Ссылка на телеграмм канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "5": f"Здравствуйте, уважаемая поддержка Телеграмма. На вашей платформе я нашел канал который распространяет шокирующие кадры убийства людей. Ссылка на телеграмм канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "7": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который пропогондирует продажу наркотических веществ, которые запрещены на территории РФ статьей 228.1 УКРФ. Ссылка на телеграмм канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "8": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который призывает людей к террору что запрещено на территории РФ статьей 205.2 УКРФ. Ссылка на телеграмм канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "9": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который призывает людей к суициду что запрещено на территории РФ статьей 110.1 УКРФ. Ссылка на телеграмм канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "10": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который разжигает ненависть в сторону определенных людей или же групп лиц. Ссылка на канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "11": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который пропогандирует насилие что запрещено на территории РФ статьей 282 УКРФ. Ссылка на канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "12": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который занимается продажей детских интимных фото что запрещено на территории РФ статьей 242.1 УКРФ. Ссылка на канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "13": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который пропогондирует угнетение нации что запрещено на территории РФ статьей 282 УКРФ. Ссылка на канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "14": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который пропогондирует угнетение религии что запрещено на территории РФ статьей 148 УКРФ. Ссылка на канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "15": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который пропогонирует порнографические материалы. Ссыока на канал - {channel_link}, Ссылка на нарушение - {channel_violation}. Просьба заблокировать данный канал."
            }
            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[ch_choice]
                    comp_body = comp_text.format(channel_link=channel_link.strip(), channel_violation=channel_violation.strip)
                    send_email(receiver, sender_email, sender_password, 'Жалоба на телеграм канал', comp_body)
                    cprint(f"ОТПРАВЛЕНО НА {receiver} 0Т {sender_email}", "green")
                    sent_emails += 100000
                    time.sleep(5)


    elif choice == "3":
        print("1. ГЛА3 Б0ГА ")
        print("2. ТUПА СUНЕГ0 КUТА")
        print("3. ПР0ДАЖА ЦП")
        print("4. М0ШЕННИЧЕСКUЕ СХЕМЫ")
        print("5. СПАМ, РЕКЛАМА")
        print("6. ШАНТАЖ")
        print("7. UЗВРАЩЕНUЯ(СНАФФ,ЦП U ТП)")
        print("ВbIБUРАЙ: ")
        bot_ch = input()
        if bot_ch in ["1", "2", "3", "4", "5", "6", "7"]:
            print("USERNAME BOTA: ")
            bot_user = input()
            cprint("АТАКА НАЧАЛАСb" , "red")
            comp_texts = {
                "1": f"Здравствуйте, уважаемая поддержка телеграм. На вашей платформе я нашел бота, который осуществляет поиск по личным данным ваших пользователей. Ссылка на бота - {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота.",
                "2": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел бота который путем заданий приводит людей к суициду что запрещено на территории РФ статьей 110.1 УКРФ. Ссылка на бота {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота.",
                "3": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел бота который продает порнографические материалы с участием лиц не достигших совершеннолетия, что запрещено на территории РФ статьей 242.1 УКРФ. Ссылка на бота {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота.",
                "4": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел бота который занимается мошенническими схемами и обманывает людей на деньги что запрещено на территории РФ статьей 159 УКРФ. Ссылка на бота {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота.",
                "5": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел бота который рассылает навязчивую рекламу и спамит ей в чатах. Ссылка на бота {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота.",
                "6": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел бота который путем шантажа вымогает из людей деньги, личные данные и другие вещи. Ссылка на бота {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота.",
                "7": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел бота который распростроняет видео шокируещего контента по типу детского порно и расчленения людей. Ссылка на бота {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота."
             }
            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[bot_ch]
                    comp_body = comp_text.format(bot_user=bot_user.strip())
                    send_email(receiver, sender_email, sender_password, 'Жалоба на бота телеграм', comp_body)
                    cprint(f"ОТПРАВЛЕНО НА {receiver} 0Т {sender_email}", "green")
                    sent_emails += 10000
                    time.sleep(5)
        
    elif choice == "4":
        print("1. ПРОСТО СНОС(НЕ ЭФФЕКТUВЕН)")
        print("2. СПАМ/РЕКЛАМА")
        print("3. ЗА АВУ UЛU НАЗВАНUЕ")
        print("4. ПР0П0ГАНДА НАСИЛИЯ U ТП")
        print("5. НАКРУТКА")
        print("6. ОСКU В ЧАТЕ")
        print("ВbIБUРАЙ: ")
        bottik = input()
        if bottik in ["1", "2", "3", "4", "5"]:
            print("ССbIЛКА НА ЧАТ: ")
            user_chat = input()
            print("TG ID ЧАТА: ")
            id_chat = input()
            cprint("АТАКА НАЧАЛАСb" , "red")
            comp_texts = {
                "1": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел группу с подозрительной активностью. Ссылка на группу - {user_chat}, Айди группы - {id_chat}. Пожалуйста примите меры в сторону данной группы и заблокируйте ее.",
                "2": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел группу в которой проходят спам-рассылки. Ссылка на группу - {user_chat}, Айди группы - {id_chat}. Пожалуйста примите меры в сторону этой группы и заблокируйте ее как можно скорее.",
                "3": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел группу в которой стоит вызывающая аватарка и имя, разжигающее конфликты. Ссылка на группу - {user_chat}, Айди группы - {id_chat}. Пожалуйста примите меры в сторону этой группы и заблокируйте ее как можно скорее.",
                "4": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел группу в которой пропогондируется насилие и другие подобные жестокости. Ссылка на группу - {user_chat}, Айди группы - {id_chat}. Пожалуйста примите меры в сторону этой группы и заблокируйте ее как можно скорее",
                "5": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел группу в которой происходит накрутка подписчиков. Ссылка на группу - {user_chat}, Айди группы - {id_chat}. Пожалуйста примите меры в сторону этой группы и заблокируйте ее как можно скорее"
            }
            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[bottik]
                    comp_body = comp_text.format(user_chat=user_chat.strip(), id_chat=id_chat.strip())
                    send_email(receiver, sender_email, sender_password, 'Жалоба на группу телеграм', comp_body)
                    cprint(f"ОТПРАВЛЕНО НА {receiver} 0Т {sender_email}", "green")
                    sent_emails += 10000
                    time.sleep(5)     

        elif bottik == "6":
            print("ССbIЛКА НА ЧАТ: ")
            username_chat = input()
            print("TG ID CHATA: ")
            idtg_chata = input()
            print("ССbIЛКА НА НАРУШЕНUЕ: ")
            ssilka = input()
            cprint("ATAKA НАЧАЛАСb" , "red")
            comp_texts = {
                "6": f"Здравствуйте, уважаемая поддержка телеграмма. Я нашел группу с которой оскорбляют людей и используют ненормативную лексику в их сторону. Ссылка на группу - {username_chat}, Айди группы - {idtg_chata}, Ссылка на нарушение - {ssilka}. Пожалуйста примите меры в сторону этой группы и заблокируйте ее как можно скорее"
            }
            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[bottik]
                    comp_body = comp_text.format(username_chat=username_chat.strip(), idtg_chata=idtg_chata.strip(), ssilka=ssilka.strip())
                    send_email(receiver, sender_email, sender_password, 'Жалоба на группу телеграм', comp_body)
                    cprint(f"ОТПРАВЛЕНО НА {receiver} 0Т {sender_email}", "green")
                    sent_emails += 10000
                    time.sleep(5)     

  
if __name__ == "__main__":
    main()
    

