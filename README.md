# CaesarAIHub

## 📌 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## 🚀 About the Project

There are 4 CaesarAIHub,CaesarAIJackett,CaesarAIStreamYT,CaesarAIMovieStream 


---

## ✨ Features

- ✅ Feature 1 (e.g., "Fast and scalable API")
- ✅ Feature 2 (e.g., "Secure authentication with JWT")
- ✅ Feature 3 (e.g., "Supports multiple database backends")
- ✅ Feature 4 (e.g., "Extensive unit tests")

---

## 📥 Installation


### Clone the repository

```
git clone --recurse-submodules git@github.com:CaesarCloudSync/CaesarAIHub.git.git

```
### Build the project
```
docker compose build

```
Run the containers up. 
```
docker compose up
```
### Get JACKETT_API_KEY and REALDEBRID_API_KEY API Keys
Below is the Jackett, go to it and add the indexers for example nyaasi,torlock,torrentgalaxy etc.
```
http://127.0.0.1:9117/UI/Dashboard

```
Copy the API Key and store it in the CaesarAIMovieStream .env file as:
```
JACKETT_API_KEY
```
If this is the first time running, the containers may be need to be run again with a new API key.

Store the REALDEBRID_API_KEY in the CaesarAIMovieStream .env as well. You can get it from this page.
```
https://real-debrid.com/devices
```
### Set Jackett Architecture Environment variable.
In the root .env set AMD_OR_AARCH as depending on what device you are building on:
```
AMD or AARCH
```
### Setting up the VPN for Jacket
You need a wg*.conf file, go to the url below and login, scroll down to the wireguard, configurations. 
Getting Wireguard wg0.conf file
```
https://account.protonvpn.com/downloads
```

Click Create and this will create your wg0 file. Rename the file to wg0.conf and add it to this directory.
```CaesarAIJackett/config/wireguard```
 
THIS IS IMPORTANT OR THE VPN WON'T RUN.

### Test the VPN
To see if the VPN is working 
```
docker ps
```
Find the jackett docker container and exec into it:
```
docker exec -it <container name> sh
```
Update the container and install curl
```
apt update && apt install curl

```
Run the below command and it will give you the ip address of the jackett container
```
curl ifconfig.me
```
Go to https://whatismyipaddress.com/ and check if it is at the protonvpn's country. If so it is working.

### Setup Cloudflare tunnel to have access to all services.
Go to this link below it will create the tunnel that connects to the hostname.
```
https://one.dash.cloudflare.com/15f7bc7d5f9c21072f16f2abe3070143/networks/tunnels
```
Use this video to understand how the cloudflare tunnel works
```
https://www.youtube.com/watch?v=SivE_EfUNd8
```
Once the tunnel domain and subdomain is setup. Go to this link below and it will show the healthcheck. Showing that it is work.
```
https://hub.caesaraihub.org/

```

### Setup Prowlerr
https://hotio.dev/containers/prowlarr/#__tabbed_2_2
Take Both docker-compose files and put it all in one service. Make sure wg0.conf file exists in root directory for the vpn.
Make sure the wg0.conf is from two different accounts and different servers ideally.
```
config/wireguard/wg0.conf
```
Then docker compose up.

#### Setup Cloudflare proxy on prowlerr (Deprecated for now)
If you recieve "Unable to access anidex.info, blocked by CloudFlare Protection." when adding an indexer on prowlerr
https://trash-guides.info/Prowlarr/prowlarr-setup-flaresolverr/

### Extra Notes
This is the code that manually creates the Jackett instance and includes it with wireguard.
https://github.com/DyonR/docker-Jackettvpn

Installing wireguard manually, could be done in a docker container solely but errors with resolv.conf due to docker using it for the engine.
https://protonvpn.com/support/wireguard-linux#cli

Official Jackett Documentation
https://github.com/Jackett/Jackett