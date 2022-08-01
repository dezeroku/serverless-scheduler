## Schedulers
The scope of this project is to react to item-level changes that are done to `Items` table (managed by
REST API that's defined in `items` module) and maintain easy to work with representation of jobs.
This representation would then be used to "cycle" between DynamoDB and SQS and trigger "real" checkers.

## Module Design
Data stored in `Items` table is meant to be easily manageable from a single-user perspective (so it's easy
to add, edit and remove entries).
Meanwhile the representation to be kept in `Schedulers` table is kept in a way that allows single-item monitoring
and modification.

In principle `Items` table keeps a list of items indexed by user, each of which has a list of monitoring jobs.
`Schedulers` table keeps a list of items indexed by the key of (job id (identifiable in user context) + user_id).

So an example `Items` content of:
| user_id | monitors |
|---------|----------|
| 1       | a, b     |
| 2       | b, g     |
| 3       | a, d     |

becomes (in `Schedulers`):
| key (user_id + monitor_id) |
|----------------------------|
| 1-a                        |
| 1-b                        |
| 2-b                        |
| 2-g                        |
| 3-a                        |
| 3-d                        |

Note that the monitor ids do not have to be unique globally (e.g. both user `1` and user `3` keep monitor jobs of id `1`).
However it's necessary that a concatenated string of `user_id` and `monitor_id` is unique in a global context.

With such a representation it's much easier to define the scheduling based on the DB itself and react to item-level changes that will be coming from `Items` service.

A single entry in `Schedulers` DB has to contain some kind of a "counter" that can be used to trigger next schedule.
For example
| key (user_id + monitor_id) | (monitor job details) | counter |
|----------------------------|-----------------------|---------|
| 1-a                        | ...                   | (int)   |

When a new entry is added to `Schedulers` table, it will cause an item-level change.
Based on it, a scheduled job will be added to an SQS (according to the details of monitor job, such as initial delay before processing etc).
The job's responsibility would be to:
1. Trigger the "real" monitoring job, by inserting an event to another SQS (this is controversial. Checking process could be already done at this stage, but let's try to keep responsibilities separate, at cost of adding another service and a queue)
2. Try to increment the counter of "seed job" in `Schedulers` DB

Because of this approach, scheduling would be fully scalable and "effortless" on the code's end.
There are few things to consider here:

### Possible paths
#### What if the details of an item changed in the `Schedulers` table?
As the triggering is done based on row-level changes, the schedulers should always run with most up-to-date monitor job details.
So no need to worry about manually checking that. TODO: Can we increment a counter in such a way that other fields are guaranteed to be not affected/overriden?

If an item is changed, it must be ensured that another scheduler is not created for the same monitor job.
If this is not ensured, there can be theoretically infinite number of schedulers running for the same job, which means a lot of wasted resources and annoyance.
An easy way to fix this issue is to only push an item to SQS, if the counter value has changed (which will happen during the initial insert as `None is not 0` and during a callback from SQS (as counter value will be simply incremented)).

#### What if the item will be removed from `Schedulers` table?
In this case there will be no counter to increment, so no callback from SQS will happen.
There is a risk of race condition here, same as in "item changed" case described above, so the same "TODO: Can we increment a counter in such a way that other fields are guaranteed to be not affected/overriden?" applies

#### What if a new item is inserted to `Schedulers` table?
Its initial counter value should be set to zero and it should be set to SQS.



## High-level overview
General idea at this point looks like so:

User <-> REST API (`Items`) -> DynamoDB (`Items`) -> (row level changes) -> DynamoDB (`Schedulers`) -> (row level changes) -> SQS -> (put an entry in outgoing SQS and edit an entry in `Schedulers` causing the cycle of scheduling)

So there is a whole scheduling mechanism already in place, but there's still nothing connected to the "outgoing SQS" mentioned above.
