# EasySaaS

This project will be attempted to make a great starting point for your next big business as easy and efficient as possible.
This project will create an easy way to build a SaaS application using Python、Dash and feffery-xxx-components.
This project also show you how to use Dash effectively and efficiently.

### Run mysql And redis By Docker

```
curl -fsSL https://get.docker.com | bash -s docker
docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD={password} -d mysql
docker run --name redis -p 6379:6379 -d redis --requirepass "{redis-password}"
docker inspect mysql/redis | grep IPAddress
```

### Update System Environs

```
vim .bash_profile / .zshrc
# export {PRE}_APP_DOMAIN=http://127.0.0.1:8000

# export {PRE}_MAIL_SERVER=smtp.exmail.xx.com
# export {PRE}_MAIL_PORT=465
# export {PRE}_MAIL_USERNAME=noreply@easysaas.com
# export {PRE}_MAIL_PASSWORD=xxxxxxxxxxxxxxxxxxxxx

# export {PRE}_REDIS_URI=redis://:password@host:port
# export {PRE}_DATABASE_URI=sqlite:///{DIR}/main.db
# mysql+pymysql://user:password@host:port/dbname
source .bash_profile / .zshrc
```

### Install venv And requirements.txt

```
# Python3.8 required
cd {DIR} && python3.8 -m venv .venv
source .venv/bin/activate / deactivate
pip3 install -r requirements.txt
```

### Run Application With uwsgi / gunicorn / uvicorn

```
.venv/bin/uwsgi --http :8000 --module index:server --pidfile index.pid 
                --master --enable-threads --daemonize index.log
.venv/bin/uwsig --stop / --reload index.pid

.venv/bin/uvicorn main:app --port 8000 --reload
```

### Frontend

- Bootstrap: https://getbootstrap.com/docs/5.1/utilities/api/
- CheatSheet: https://dashcheatsheet.pythonanywhere.com/
- Front4.0: https://htmlstream.com/front-v4.0/index.html
- Echarts: https://echarts.apache.org/examples/zh/index.html
- Antd: https://ant-design.gitee.io/index-cn
- Fac: https://fac.feffery.tech/what-is-fac
- Fuc: https://fuc.feffery.tech/what-is-fuc
- FastAPI: https://fastapi.tiangolo.com
- Pydantic: https://pydantic-docs.helpmanual.io
