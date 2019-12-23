# HTDF 代码例子（python）

# IDE环境和命令行 python版本 3
## vscode
python.python 设置为python3

## pycharm
Settings --> Project Interpreter 用python3

## 命令行
需要是python3
```
$ python --version
Python 3.5.2

```

# 用python3 重装 pip

```
$ wget https://bootstrap.pypa.io/get-pip.py
$ sudo python3 get-pip.py
```

# 依赖的安装
指定用 pip3（pytho3） 安装；

```
sudo pip3 install -r requirements
```

pip3 有异常的话，参考以下 `pip异常`进行处理

# 特殊的 env_python2 目录
## 该目录里的源码，是python2 写的；
为避免混淆，不要用 IDE（vscode、pycharm） 去调用， 而是使用命令行，指定用python2 执行

```
$pwd
.../env_python2

$python2 htdf_addr_gen.py
```
## 其他程序不要直接调用 env_python2 目录里的函数
因为本项目整体(包括htdf_transfer.py)是python3环境，env_python2目录里面是python2的代码，两者不兼容，不能相互调用；

例如，htdf_transfer.py 给定 g_PrivKey 生成对应 g_PubKey ，不能直接调用env_python2里的代码，即如下代码是错误的；

```
##htdf_transfer.py

##调用 env_python2 目录里的函数
g_PubKey = env_python2.htdf_addr_gen. (g_PrivKey)
```

# 从g_PrivKey 生成对应的 g_PubKey
以上提到：`其他程序不要直接调用 env_python2 目录里的函数` 

g_PrivKey 生成对应的 g_PubKey，只能在 env_python2/htdf_addr_gen.py 里面调

```
$ cat htdf_addr_gen.py
def main():    
    g_PrivKey = '3d559fbdfea9c06bfa549b3424b0147121575e8071c9e98f10a435cf6081f72d'
    print(g_PrivKey)
    pubKey = PrivKeyToPubKeyCompress(g_PrivKey)
    print(pubKey)

    pass


$ python2 htdf_addr_gen.py 
3d559fbdfea9c06bfa549b3424b0147121575e8071c9e98f10a435cf6081f72d
035d18f7e54f063679b09473066d1e6d9c3b16a2b66b02f8d156ea3645623adee0

```


# 例子

```
##私钥、公钥、地址生成
htdf_addr_gen.py

##转账
htdf_transfer.py
```



# 常见问题
## pip异常
pip 或者 pip3 有如下异常问题，需要重装 pip（详见以上  `用python3 重装 pip`）
```
$ pip3 --version
Traceback (most recent call last):
  File "/usr/local/bin/pip", line 6, in <module>
    from pip._internal.main import main
  ...
  File "build/bdist.linux-x86_64/egg/OpenSSL/__init__.py", line 8, in <module>
  File "build/bdist.linux-x86_64/egg/OpenSSL/crypto.py", line 15, in <module>
  File "build/bdist.linux-x86_64/egg/OpenSSL/_util.py", line 152, in <module>
TypeError: from_buffer() cannot return the address of the raw string within a str or unicode or bytearray object

```

## 依赖库不存在

依赖库不存在，手工安装指定依赖库 
```
$pip install coincurve
...
$pip install requests
...
```


 


