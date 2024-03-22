
Inspired by [wybiral/noscript-chat](https://github.com/wybiral/noscript-chat), 
this is the python version of it.

### dev setup

```shell
virtualenv env
source env/bin/activate

pip install -r requirements.txt

python noscriptchat
```

And visit [localhost:8000](http://localhost:8000)

To run mockup chat users, in a separate shell:

```shell
python noscriptchat mock
```
