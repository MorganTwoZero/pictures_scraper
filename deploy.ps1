ssh root@vpn "cd pictures_scraper && docker compose stop && git pull"
ssh root@vpn "docker compose up --build"
#clean deploy
#ssh root@vpn "cd pictures_scraper && docker compose stop && cd .. && rm -rf pictures_scraper && git clone https://github.com/MorganTwoZero/pictures_scraper"
#ssh root@vpn "mkdir ./pictures_scraper/certs" 
#ssh root@vpn "cp /etc/letsencrypt/live/honkai-pictures.ru/fullchain.pem /etc/letsencrypt/live/honkai-pictures.ru/privkey.pem /root/pictures_scraper/certs -rL"
#cat .env | ssh root@vpn "cat >> pictures_scraper/.env  && cd pictures_scraper && docker compose up --build"