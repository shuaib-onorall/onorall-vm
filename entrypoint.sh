if [ "$DATABASE" = "mongo" ]
then
    echo "Waiting for mongodb..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "mongodb started"
fi

python manage.py flush --no-input
python manage.py migrate

exec "$@"