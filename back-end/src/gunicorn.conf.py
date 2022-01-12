import os

# The socket to bind.
bind = f"0.0.0.0:{os.environ['BACK_END_PORT']}"

# The number of worker processes for handling requests.
workers = 4

# The type of workers to use.
worker_class = "sync"

# The maximum number of requests a worker will process before restarting.
max_requests = 100

# Front-end’s IPs from which allowed to handle set secure headers (comma separate).
forwarded_allow_ips = "*"
