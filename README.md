# telegram_bot_chef_helper
asynchrony telegram bot  ~~ helping the chef find meal cooking instructions.
Deploy process:
```/Users/andriiosypenko/.fly/bin/flyctl``` == flyctl
1)Install installation ```brew install flyctl | curl -L https://fly.io/install.sh | sh```
2)Login ```/Users/andriiosypenko/.fly/bin/flyctl  auth login```
3) Lounch app ```/Users/andriiosypenko/.fly/bin/flyctl launch```
4)Ship Docker image ```/Users/andriiosypenko/.fly/bin/flyctl deploy```