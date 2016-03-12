sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-pip git zsh wget

# Install zsh
wget --no-check-certificate https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh
echo "/bin/zsh" >> .bashrc

# Install django
sudo pip install Django==1.9.4
mkdir git && cd git
git clone https://github.com/a180285/django-learn.git

