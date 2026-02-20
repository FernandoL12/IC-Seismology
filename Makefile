# file = cluster1.txt
#
# Example:
# make test_ids ids="usp2026doac usp2026dmwl usp2026dmvw"
# make test_file file=cluster1.txt
# make check_fdsn


# ============================
#  Default configurations (seisarc tunnel on localhost)
# ============================
station = BL.RVDE..HHZ
window  = P/0.2/0.72
lp      = 10
hp      = 2
fdsn    = http://127.0.0.1:28080/
cs      = 0.05
script  = correlation.py

# ============================
#  FDSN connectivity check
# ============================
check_fdsn:
	curl -sS $(fdsn)fdsnws/event/1/application.wadl | head -n 20

# ============================
#  TEST 1 — pass IDs directly
# ============================
# Example:
# make test_ids ids="usp2026doac usp2026dmwl usp2026dmvw"
# ============================
test_ids:
	@if [ -z "$(ids)" ]; then \
		echo "ERROR: you must pass ids=\"id1 id2 id3\""; \
		echo "OR you can use a file with: make test_file file=cluster1.txt"; \
		exit 1; \
	fi
	python3 $(script) $(ids) \
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
	python3 $(script) $(shell cat $(file)) \
		-s $(station) -w $(window) -lp $(lp) -hp $(hp) \
		-F $(fdsn) -c -cs $(cs)

