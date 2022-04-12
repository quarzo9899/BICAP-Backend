# BICAP-backend
backend di BICAP che si basa su django e django rest framework.

## Debian
Rendiamo disponibile un disco di una macchina virtuale debian 10 creata usando kvm che include una versione del backand e tutte le dipendenze, consigliamo comunque di aggiornare all'ultima realese disponibile. [Download](https://drive.google.com/file/d/15QN-K7I9G_NVt0x-U296YSIfhLHXZT1I/view?usp=sharing)  
Nel caso si preferisse installare le dipendenze e il backand rendiamo disponibili i seguenti comandi:
```console
apt-get update
apt-get upgrade -y
apt-get install sudo -y
sudo apt-get install postgresql postgresql-contrib zlib1g-dev libjpeg-dev python3-pythonmagick inkscape xvfb poppler-utils libfile-mimeinfo-perl qpdf libimage-exiftool-perl ufraw-batch ffmpeg libreoffice supervisor nginx git python3-venv libpq-devapt python3-psycopg2 in -y
sudo adduser django
sudo usermod -aG sudo django
cd /tmp
sudo -u postgres createuser django
sudo -u postgres createdb BICAPwebDB
sudo -u postgres psql
ALTER USER django WITH PASSWORD 'LaPasswordCheVoleteDare';
```
Modificate **LaPasswordCheVoleteDare** con una password sicura

```console
exit
sudo su django
git clone https://github.com/SgozziCoders/BICAP-backend
mv BICAP-backend/DjangoBICAP/ /home/django/DjangoBICAP/
cd /home/django/
python3 -m venv django_env
pip install -r /home/django/DjangoBICAP/requirements.txt
mv DjangoBICAP/media/ /home/django/media-serve/
mkdir /home/django/static-serve/
```

Ora apriamo il file settings.py e modifichiamo la riga 91 inserendo la password del database
```console
nano DjangoBICAP/DjangoBICAP/settings.py
```

```console
python  manage.py collectstatic
python manage.py makemigrations BICAPweb
python manage.py migrate
python manage.py createsuperuser
mv /tmp/BICAP-backend/extras/gunicorn_start.bash /home/django/
chmod +x /home/django/gunicorn_start.bash
sudo mv /tmp/BICAP-backend/extras/DjangoBICAP.conf /etc/supervisor/conf.d/DjangoBICAP.conf
sudo mv /tmp/BICAP-backend/extras/nginx-default.conf /etc/nginx/sites-available/default
mkdir  /home/django/logs
touch /home/django/logs/gunicorn_supervisor.log
sudo systemctl restart supervisor
sudo systemctl enable supervisor
sudo  service nginx restart
```
