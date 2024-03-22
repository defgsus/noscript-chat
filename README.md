
Inspired by [wybiral/noscript-chat](https://github.com/wybiral/noscript-chat), 
this is the python version of it.


### run it locally

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

It's 3 users/threads posting on the `/mock` channel.


### deployment

Create a file called `.env` in the project root, or copy the
[`.env-example`](.env-example) file and adjust the settings.

It uses [python-decouple](https://github.com/HBNetwork/python-decouple)
so you can define environment variables as well.

