.PHONY: all

all:
	python3 setup.py sdist bdist_wheel

clean:
	sudo rm -rf ./build
	sudo rm -rf ./dist
	sudo rm -rf ./pyrtdb.egg-info
