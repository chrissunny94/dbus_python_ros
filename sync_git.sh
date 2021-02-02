

git config --global credential.helper 'cache --timeout=3600'
# Set the cache to timeout after 1 hour (setting is in seconds)

#git pull
git add .
git add -A

git commit -m "$1"
git push 
