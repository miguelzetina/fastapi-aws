poetry run coverage run -m pytest -v tests && poetry run coverage report -m --omit="*/test*,config/*.conf"
