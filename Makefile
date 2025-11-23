file = cluster1.txt

test:
	python3 correlation.py $(file) -s VL.SLBO..HHZ -w P/0.2/0.72 -lp 10 -hp 2 -F http://10.110.0.135:18003/ -c -cs 0.05
