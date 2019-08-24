# Установка Docker для Ubuntu 18.04

## 1. Устанавливаем зависимости
```bash
sudo apt-get update
sudo apt-get install apt-transport-https
sudo apt-get install ca-certificates
sudo apt-get install curl
sudo apt-get install software-properties-common
sudo apt-get install gnupg-agent  # ubuntu
sudo apt-get install gnupg2  # debian
```

## 2. Добавляем официальный ключ докера
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -  # ubuntu
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -  # debian
# проверяем что ключ установился
sudo apt-key fingerprint 0EBFCD88
```
## 3. Добавляем репозиторий докера
```bash
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"  # ubuntu
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"  # debian
```

## 4. Устанавливаем докер
```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
# проверка работоспособности
sudo docker run hello-world
```
## 5. Добавляем пользователя в группу docker
```bash
sudo usermod -aG docker ${USER}
su - ${USER}
id -nG  # проверяем что добавились
```

# Установка Docker-Compose

> зависимости py-pip, python-dev, libffi-dev, openssl-dev, gcc, libc-dev, and make
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```
