source ./venv/bin/activate
pip install -r requirements.txt
alembic upgrade 8e92f8ba245c
alembic upgrade 906256cfcd17
alembic upgrade e8e3d57b7e99
alembic upgrade b94deee9cf68
alembic upgrade bc63ec4350c7
alembic upgrade bd0bbe82d721
alembic upgrade 1b32dd2b77f8
python app.py
