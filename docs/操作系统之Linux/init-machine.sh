

touch ~/.inputrc

echo "\e[A": history-search-backward >> ~/.inputrc

"\e[B": history-search-forward

"\e[5~": history-search-backward
"\e[6~": history-search-forward

bind -f ~/.inputrc
