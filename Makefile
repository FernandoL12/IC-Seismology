#file = cluster1.txt

#test:
#	python3 correlation.py $(file) -s VL.SLBO..HHZ -w P/0.2/0.72 -lp 10 -hp 2 -F http://10.110.0.135:18003/ -c -cs 0.05


# ============================
#  Default configurations
# ============================
station = VL.SLBO..HHZ
window  = P/0.2/0.72
lp      = 10
hp      = 2
fdsn    = http://10.110.0.135:18003/
cs      = 0.05


# ============================
#  TEST 1 — pass IDs directly
# ============================
# Example:
# make test_ids ids="val2024abc val2024def val2025xyz"
# ============================
test_ids:
	@if [ -z "$(ids)" ]; then \
		echo "ERROR: you must pass ids=\"id1 id2 id3\""; \
		echo "OR you can use a file with: make test_file file=cluster1.txt"; \
		exit 1; \
	fi
	python3 correlation.py $(ids) \
		-s $(station) -w $(window) -lp $(lp) -hp $(hp) \
		-F $(fdsn) -c -cs $(cs)


# ============================
#  TEST 2 — pass a TXT file
# ============================
# Example:
# make test_file file=cluster1.txt
# ============================
test_file:
	@if [ -z "$(file)" ]; then \
		echo "ERROR: you must pass file=filename.txt"; \
		echo "OR you can pass IDs directly with: make test_ids ids=\"id1 id2\""; \
		exit 1; \
	fi
	python3 correlation.py $(shell cat $(file)) \
		-s $(station) -w $(window) -lp $(lp) -hp $(hp) \
		-F $(fdsn) -c -cs $(cs)


