LIB_DIR='Support/lib'
DEPS='flake8>=3.0,<4.0'

all: pip

pip:
	python -m pip install --target $(LIB_DIR) $(DEPS)

upgrade:
	python -m pip install --upgrade --target $(LIB_DIR) $(DEPS)

clean:
	find $(LIB_DIR) -not -name 'sitecustomize.py' -not -name 'flake8parser.py' -type f -print -delete
	find $(LIB_DIR) -type d -mindepth 1 -print -delete
