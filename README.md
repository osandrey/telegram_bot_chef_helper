# telegram_bot_chef_helper
asynchrony telegram bot  ~~ helping the chef find meal cooking instructions.
Deploy process:
```/Users/andriiosypenko/.fly/bin/flyctl``` == flyctl
1)Install installation ```brew install flyctl | curl -L https://fly.io/install.sh | sh```
2)Login ```/Users/andriiosypenko/.fly/bin/flyctl  auth login```
3) Lounch app ```/Users/andriiosypenko/.fly/bin/flyctl launch```
4)Ship Docker image ```/Users/andriiosypenko/.fly/bin/flyctl deploy```

5)Build image ```docker build . --platform=linux/amd64 -t osandreyman/chef_helper:0.0.1```

Docker push on DockerHub ```docker push osandreyman/chef_helper:0.0.1```


Run container on server
```docker run --name cheif_helper_bot -v /home/kiraparcer/data:/data osandreyman/chef_helper:0.0.1```