# Installation

### 1. Get Docker ready

To build Tutti environment, you first need to install **Docker** and **Docker Compose** in your host server.  
Since their installation steps may depend on your local environment, please follow their latest official installation procedures.

- [Install Docker](https://docs.docker.com/get-docker/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

### 2. Clone Tutti repository

```bash
git clone https://github.com/iflb/tutti
```

!> You need an **access permission** to the Github private repository. If you haven't requested it, contact someone at ifLab.

### 3. Activate Tutti

#### [Optional] Automatic SSL configuration by using Let's Encrypt

If you already have your web domain name ready, Tutti can automatically request/renew SSL certification via [Let's Encrypt](https://letsencrypt.org) at each time you start Tutti service, so that all web pages can be served with `https://`.
This is especially necessary when you are planning to use some crowdsourcing platforms like [Amazon Mechanical Turk](https://mturk.com). 

To enable this feature, you first need to edit an environment configuration file `tutti/.env` as follows:

```bash
<!-- tutti/.env -->

DOMAIN_NAME=<Your domain name here (e.g., yourdomain.com)>
EMAIL=<Your email address here>
...
ENABLE_SSL=1
...
```

Also note that you need to have the port numbers 80 and 443 of your host server open.

#### Build

Run the command below (this may take at least a few minutes)

```bash
sudo docker-compose build
```

#### Start

Run the command below (this may take another few minutes)

```bash
sudo docker-compose up
```

Then wait while output logs keep printing, until you see the similar message as shown below (this means Vue CLI successfully started the frontend server.)

<img src="/_media/vue-ready-output.png" />

### 4. Check Tutti Console

Access `https://yourdomain.com/vue/console/` (Web hosting w/ SSL) or `http://localhost/vue/console/` (local host machine) via a web browser (Google Chrome is recommended).
Make sure that the console is displayed with the green sign "Websocket connected", which means DUCTS backend server is successfully booted.

<img src="/_media/console-ready-screenshot.png" width="700" />

**That's it!** You are now ready to start developing your annotation project with Tutti.
