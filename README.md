# TESLA: TwittEr Spam LeArning - Docker Version

## CSCE 670 Spring 2018, Course Project

This is the dockerized version of [TESLA: TwittEr Spam LeArning](https://github.com/letheyue/TESLA-twitter-suspension-learning). Read below for more info about deploying the docker image on your local machine. Live web demo is available [here](https://tesla.roselin.me) (Heroku version no longer supported)

### Instruction

To deploy this app locally, please ensure that you have `Docker >= 19.03.8` installed already.

1. Clone the whole repo to your local drive.
2. While at the project folder, run: `docker-compose up -d`

Wait a bit, and if everything works you should be able to view the app at `localhost:4430`.

### Publish the app to the web

This part is designed for those who would like to publish the app to the web and prefer not to visit it through `IP:PORT`. Please make sure that your app is already up and running stably at `localhost:4430` before reading on.

**Method 1: Use Nginx**

This is what I'm using right now (since my VPS already has Nginx configured to serve other websites). Follow [this guide](https://www.digitalocean.com/community/questions/how-to-host-multiple-docker-containers-on-a-single-droplet-with-nginx-reverse-proxy?answer=57632) starting from step 2. It should allow basic HTTP traffic. To add SSL, a valid certificate is needed (I used `certbot` and `letsencrpyt` [guide](https://www.digitalocean.com/community/tutorials/how-to-use-certbot-standalone-mode-to-retrieve-let-s-encrypt-ssl-certificates-on-ubuntu-16-04)). Modify your Nginx configuration file to add a block similar to below:

```
server {
    listen 443 ssl;
    server_name `YOUR-DOMAIN-NAME-HERE`;

    location / {
        proxy_pass  http://localhost:4430;
    }

    ssl_certificate /etc/letsencrypt/live/`YOUR-DOMAIN-NAME-HERE`/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/`YOUR-DOMAIN-NAME-HERE`/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/`YOUR-DOMAIN-NAME-HERE`/chain.pem;
}

```

Restart the Nginx server and your app should display for incoming HTTPS traffic as well.

**Method 2: Use Traefik to manage docker network traffic**

Refer to the instruction [here](https://www.digitalocean.com/community/tutorials/how-to-use-traefik-as-a-reverse-proxy-for-docker-containers-on-ubuntu-16-04)

--> It's also possible to use Nginx-proxy as an alternative network policy. The setup is similar to Traefik.
