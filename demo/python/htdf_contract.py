#!/usr/bin/env python
#!coding:utf8

#author:taoist_ma
#date:2019/9/19 



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

data = "6060604052341561000f57600080fd5b336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555061042d8061005e6000396000f300606060405260043610610062576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063075461721461006757806327e235e3146100bc57806340c10f1914610109578063d0679d341461014b575b600080fd5b341561007257600080fd5b61007a61018d565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34156100c757600080fd5b6100f3600480803573ffffffffffffffffffffffffffffffffffffffff169060200190919050506101b2565b6040518082815260200191505060405180910390f35b341561011457600080fd5b610149600480803573ffffffffffffffffffffffffffffffffffffffff169060200190919080359060200190919050506101ca565b005b341561015657600080fd5b61018b600480803573ffffffffffffffffffffffffffffffffffffffff16906020019091908035906020019091905050610277565b005b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60016020528060005260406000206000915090505481565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614151561022557610273565b80600160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825401925050819055505b5050565b80600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205410156102c3576103fd565b80600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828254039250508190555080600160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825401925050819055507f3990db2d31862302a685e8086b5755072a6e2b5b780af1ee81ece35ee3cd3345338383604051808473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020018373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001828152602001935050505060405180910390a15b50505600a165627a7a72305820f3c54d8cf0c62d5295ef69e3fc795fa1886b4de4d3d58f50f83c70ed26b99d890029"
node_ip_port = '127.0.0.1:1317'   #节点ip和端口

contract_From = 'htdf1rgsfxav0af8a79cmtq6rnjtjkqngl9qcj8k9l7'
g_PrivKey = '2b1dcef7e7732fb381e23be54ee018329af6761901738b7add98867b8454e958'
g_PubKey = '03fb9a9da661d3de30f8faae99358c6638df03296d27322c3f99f5e3b821bbee05'


g_gaslimit = 12345678  #默认即可
g_gasprice =  100  #默认即可

def CreateAndSendContract():
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
            "To": ""\
        }],\
        "sequence": "%d"\
    }""" % (nAccountNumber, g_gasprice, g_gaslimit, data,contract_From, nSequence)

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
    print(hexlify( shaData) )
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
                "To": "",
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
}""" %(contract_From, data , g_gaslimit, g_gasprice , b64PubKey, b64Data)
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
    CreateAndSendContract()
        # break
