cp -r ../code/dashboard .
cp -r ../code/helpers .
cp -r ../code/siman .
cp -r ../code/Procfile .
cp -r ../code/conda-requirements.txt .


git add -A
dt=`date +"%Y-%m-%d_%H-%M"`
git commit -m "$dt"

git push heroku master

heroku open