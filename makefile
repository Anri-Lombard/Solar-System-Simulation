install: 
	python3 -m venv venv
	. venv/bin/activate && \
		pip3 install -Ur requirements.txt && \
		pip3 install --no-cache-dir -Ur post_requirements.txt

venv :
	test -d venv || python3 -m venv venv

clean:
	rm -rf venv

run:
	python3 ./src/main.py