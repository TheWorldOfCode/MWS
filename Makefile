.POSIX:

install: mws
	cd ./packages; python3 -m pip install .
	cp ./mws ~/.local/bin/ 
	chmod 755 ~/.local/bin/mws

uninstall:
	python3 -m pip uninstall mws
	rm ~/.local/bin/mws

