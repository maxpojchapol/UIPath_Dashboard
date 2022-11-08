# Uipathdashboard


## for developing
create a new db.sqlite3 file if you want a clean database
delete all 000. 001. files in the dashboard/migrations folder

```
python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser
```





## sample data 
the folder fixtures in the dashboard app will contain files to fill the db with initial data
data should be altered (the dates to match the current date)

```
py manage.py loaddata sampledata.json
```


