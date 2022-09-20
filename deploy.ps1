ssh root@vpn "cd pictures_scraper && docker compose stop && git pull"
cat .env | ssh root@vpn "cat > pictures_scraper/.env  && cd pictures_scraper && docker compose up --build"
#clean deploy
#ssh root@vpn "cd pictures_scraper && docker compose stop && cd .. && rm -rf pictures_scraper && git clone https://github.com/MorganTwoZero/pictures_scraper"
#ssh root@vpn "mkdir ./pictures_scraper/certs" 
#ssh root@vpn "cp /etc/letsencrypt/live/pixiv.sbs/fullchain.pem /etc/letsencrypt/live/pixiv.sbs/privkey.pem /root/pictures_scraper/certs -rL"