row:
user_id -> id
monitors: [monitor]

monitor:
id -> int
url -> string
sleep_time -> int
make_screenshots -> bool


To consider:
Keeping the data in a dictionary instead of a list would be probably better for performance of handlers
that operate based on single entries. Refactor only to be done server side then
