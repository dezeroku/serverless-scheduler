row:
user_id -> id
monitors: [monitor]

monitor:
id -> int
url -> string
sleepTime -> int
makeScreenshots -> bool


To consider:
Keeping the data in a dictionary instead of a list would be probably better for performance of handlers
that operate based on single entries. Refactor only to be done server side then
