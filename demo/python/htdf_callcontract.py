#!/usr/bin/env python
#!coding:utf8

#author:yqq
#date:2019/5/6 0006 18:07
#description:



import json
import hashlib
import coincurve
import base64
from collections import OrderedDict
from binascii import  hexlify, unhexlify

def ecsign(rawhash, key):
    if coincurve and hasattr(coincurve, 'PrivateKey'):
        pk = coincurve.PrivateKey(key)
        signature = pk.sign_recoverable(rawhash, hasher=None)
        # v = safe_ord(signature[64]) + 27
        r = signature[0:32]
        s = signature[32:64]

        return r, s



    pass




import requests

data = "07546172"
node_ip_port = '127.0.0.1:1317'   #节点ip和端口

contract_From = 'htdf1rgsfxav0af8a79cmtq6rnjtjkqngl9qcj8k9l7'
g_PrivKey = '2b1dcef7e7732fb381e23be54ee018329af6761901738b7add98867b8454e958'
g_PubKey = '03fb9a9da661d3de30f8faae99358c6638df03296d27322c3f99f5e3b821bbee05'
contract_address='htdf14wexcec24kxgpf3rukktlnta5zyu9zav277qjc'




g_gaslimit = 12345678  #默认即可
g_gasprice =  100  #默认即可

def CallContract():
    rsp = requests.get('http://%s/auth/accounts/%s' % (node_ip_port.strip(), contract_From.strip()))
    rspJson = rsp.json()
    nAccountNumber = int(rspJson['value']['account_number'], 10)
    nSequence = int(rspJson['value']['sequence'], 10)
    print ("nAccountNumber:%d" %(nAccountNumber))
    print ("nSequence:%d" % (nSequence))
    print('\n-----------------------------------\n')
    rawStr = """{\
        "account_number": "%d",\
        "chain_id": "testchain",\
        "fee": {\
            "gas_price": "%d",\
            "gas_wanted": "%d"\
        },\
        "memo": "",\
        "msgs": [{\
        	"Amount": [{\
        		"amount": "0",\
                "denom": "satoshi"\
        	}],\
            "Data": "%s",\
            "From": "%s",\
            "GasPrice": 100,\
            "GasWanted": 1200000,\
            "To": "%s"\
        }],\
        "sequence": "%d"\
    }""" % (nAccountNumber, g_gasprice, g_gaslimit, data,contract_From, contract_address,nSequence)

    rawStr = rawStr.replace(' ', '')
    rawStr = rawStr.replace('\t', '')
    rawStr = rawStr.replace('\n', '')
    print ("rawStr:"+rawStr)

    print('\n-------------------------------\n')

    print("json字符转为byteArray: ")
    for  i in bytearray(rawStr, encoding='utf-8'):
        print('{0}({1}),'.format(i, chr(i))),
    shaData =  hashlib.sha256( bytearray(rawStr, encoding='utf-8') ).digest()
    print('\n-------------AAAAAAA------------------\n')
    print (bytearray(rawStr, encoding='utf-8'))
    print('\n-------------aaaaaaa------------------\n')
    print("Json的sha256结果:")
    print(hexlify( shaData))
    privKey = unhexlify( g_PrivKey )

    print('\n--------------------------------------\n')
    print("strPrivKey:", hexlify( privKey))
    r, s = ecsign(shaData,  privKey)
    print('r:' +  hexlify(r).decode(encoding='utf8'))
    print('s:' + hexlify(s).decode(encoding='utf8'))

    print('\n--------------------------------------\n')
    b64Data = base64.b64encode(r + s).decode(encoding='utf8')
    print("signdata :"+b64Data)

    print('--------------------------------------')
    pubKey = g_PubKey
    b64PubKey = base64.b64encode(unhexlify( pubKey)).decode(encoding='utf8')
    print("公钥的base64编码:" + b64PubKey)
    print('--------------------------------------')




    rawSignContract = """{
    "type": "auth/StdTx",
    "value":{
        "msg": [{
            "type": "htdfservice/send",
            "value":{
                "From": "%s",
                "To": "%s",
                "Amount": [{
                    "denom": "satoshi",
                    "amount": "0"
                }],
                "Data": "%s",
                "GasPrice": "100",
                "GasWanted": "1200000"
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
        "memo": ""
    }
}""" %(contract_From, contract_address,data , g_gaslimit , g_gasprice, b64PubKey, b64Data)
    SignContract = rawSignContract
    SignContract = SignContract.replace(' ', '')
    SignContract = SignContract.replace('\t', '')
    SignContract = SignContract.replace('\n', '')
    print ("SignContract :"+SignContract)



    bcastData = hexlify( bytes( SignContract, encoding='utf8')).decode(encoding='utf8')

    print('\n--------------------------------------\n')
    import json
    bcastData = {'tx' :  bcastData }
    postData = json.dumps(bcastData)
    print ("aaaaa :"+postData)
    rsp = requests.post('http://%s/hs/broadcast' % (node_ip_port),  postData)

    try:
        if rsp.status_code == 200:
            rspJson = rsp.json()
            txid = str(rspJson['txhash'])
            print(" txid:%s" % (txid))
        else:
            print(" 的交易广播广播失败: %s" % ( rsp.text))
    except Exception as e:
        print(e)
        return

if __name__ == '__main__':
    print('\n--------------------------------------\n')
    CallContract()
        # break
