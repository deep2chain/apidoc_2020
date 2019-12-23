#!coding:utf8

#!coding:utf8
#author:yqq
#date:2019/5/6 0006 18:07
#description:

#author:yqq
#date:2019/9/29 0029 11:03
#description:  Python2.7  -->  Python3.7
#            迁移至 python3


import json
import hashlib
import coincurve
import base64
from binascii import  hexlify, unhexlify
import requests


ismainnet = False

if ismainnet:  #主网
    g_node_ip_port = '39.108.219.50:1317'   #主网节点ip和端口
    g_chainid = 'mainchain'
else: #测试网
    g_node_ip_port = '127.0.0.1:1317'   #测试节点
    g_chainid = 'testchain'

g_strFrom = 'htdf1rgsfxav0af8a79cmtq6rnjtjkqngl9qcj8k9l7'
g_PrivKey = '2b1dcef7e7732fb381e23be54ee018329af6761901738b7add98867b8454e958'
g_PubKey = '03fb9a9da661d3de30f8faae99358c6638df03296d27322c3f99f5e3b821bbee05'
g_gaslimit = 200000  #默认即可
g_gasprice =  100  #默认即可


def ecsign(rawhash, key):
    if coincurve and hasattr(coincurve, 'PrivateKey'):
        pk = coincurve.PrivateKey(key)
        signature = pk.sign_recoverable(rawhash, hasher=None)
        # v = safe_ord(signature[64]) + 27
        r = signature[0:32]
        s = signature[32:64]
        return r, s

def Transfer(strFrom, strTo, nAmount) -> None:
    '''
    转账
    :param strFrom:  源地址
    :param strTo:  目的地址
    :param nAmount:  数量(以satoshi为单位)  换算关系  1HTDF = 10^8 satoshi
    :return: 无
    '''

    try:
        rsp =  requests.get('http://%s/auth/accounts/%s' % (g_node_ip_port.strip(), strFrom.strip()))
        rspJson = rsp.json()
        nAccountNumber = int(rspJson['value']['account_number'], 10)
        nSequence = int(rspJson['value']['sequence'], 10)

    except Exception as e:
        print (e)
        return

    print('account_number : %d' % nAccountNumber)
    print('sequence: %d' % nSequence)


    print('\n-----------------------------------\n')


    jUnTxStr = """{\
    "account_number": "%d",\
	"chain_id": "%s",\
	"fee": {\
			"gas_price": "%d",\
			"gas_wanted": "%d"\
	},\
    "memo": "yqq",\
	"msgs": [{\
		"Amount": [{\
			"amount": "%d",\
            "denom": "satoshi"\
		}],\
        "Data": "",\
        "From": "%s",\
        "GasPrice": %s,\
        "GasWanted": %s,\
		"To": "%s"\
	}],\
    "sequence": "%d"\
    }"""  % (nAccountNumber, g_chainid, g_gasprice, g_gaslimit, nAmount, strFrom, g_gasprice, g_gaslimit, strTo , nSequence)

    # jUnTxStr = json.dumps(jUnTx , sort_keys=False)
    jUnTxStr = jUnTxStr.replace(' ', '')
    jUnTxStr = jUnTxStr.replace('\t', '')
    jUnTxStr = jUnTxStr.replace('\n', '')
    print(jUnTxStr)



    # return

    print("json字符转为byteArray: ")
    for  i in bytearray(jUnTxStr, encoding='utf-8'):
        print('{0}({1}),'.format(i, chr(i)), end=''),


    shaData =  hashlib.sha256( bytearray(jUnTxStr, encoding='utf-8') ).digest()
    print('\n-----------------------------------\n')
    print("Json的sha256结果:")
    print(hexlify( shaData) )
    # privKey = g_PrivKey.decode('hex')
    privKey = unhexlify( g_PrivKey )

    print('\n--------------------------------------\n')
    print("strPrivKey:", hexlify( privKey) )
    r, s = ecsign(shaData,  privKey)
    print('r:' +  hexlify(r).decode(encoding='utf8'))
    print('s:' + hexlify(s).decode(encoding='utf8'))

    print('\n--------------------------------------\n')
    b64Data = base64.b64encode(r + s).decode(encoding='utf8')
    print(type(b64Data))
    print(b64Data)

    print('--------------------------------------')
    pubKey = g_PubKey
    b64PubKey = base64.b64encode(unhexlify( pubKey)).decode(encoding='utf8')
    print("公钥的base64编码:" + b64PubKey)



    #---------------------------------------------------------

    jSigTx = """{
        "type": "auth/StdTx",
        "value":{
            "msg": [{
                "type": "htdfservice/send",  
                "value":{
                    "From": "%s",
                    "To": "%s",
                    "Amount": [{
                        "denom": "satoshi",
                        "amount": "%d"
                    }],
                    "Data": "",
                    "GasPrice": "%d",
                    "GasWanted": "%d"
                }
            }],
            "fee": {
                "gas_wanted": "%d",
                "gas_price": "%d"
            },
            "signatures": [{
                "pub_key": {
                    "type": "tendermint/PubKeySecp256k1",
                    "value": "%s"
                },
                "signature": "%s"
            }],
            "memo": "yqq"
        }
    }""" %(strFrom, strTo , nAmount, g_gasprice, g_gaslimit, g_gaslimit, g_gasprice, b64PubKey, b64Data)

    jSigTxStr = jSigTx
    jSigTxStr = jSigTxStr.replace(' ', '')
    jSigTxStr = jSigTxStr.replace('\t', '')
    jSigTxStr = jSigTxStr.replace('\n', '')
    bcastData = hexlify( bytes( jSigTxStr, encoding='utf8')).decode(encoding='utf8')
    print("签名的json:" + jSigTxStr)
    print("签名后的交易:"+ bcastData)


    # return

    #------------------------进行广播-----------------------------------
    bcastData = {'tx' :  bcastData }
    postData = json.dumps(bcastData)
    rsp = requests.post('http://%s/hs/broadcast' % (g_node_ip_port),  postData)

    try:
        if rsp.status_code == 200:
            rspJson = rsp.json()
            txid = str(rspJson['txhash'])
            print("%s 转给 %s 金额: %d  的交易广播成功, txid:%s" % (strFrom, strTo , nAmount, txid))
        else:
            print("%s 转给 %s 金额: %d  的交易广播广播失败: %s" % (strFrom, strTo , nAmount, rsp.text))
    except Exception as e:
        print(e)
        return



if __name__ == '__main__':

    # Transfer(g_strFrom, "htdf12hnuqw25j9kflduzgjflnm88gfyq9sxuwn49d2", 0.0001 * (10 ** 8))
    Transfer(g_strFrom, "htdf15qz307gtgme7xrq69ygjejfrhaumwlrlnz5ps9", 100 )

