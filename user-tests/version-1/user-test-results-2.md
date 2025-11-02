# User Test of Prototype Version 1
- Performed on 02-11-2025
- User AI --> Software Engineer (Student)
- User Tool --> Software Engineer (Student)

## Task 1: Adding last seen
Each ghost entry must include when it was last seen, so the team can prioritize active cases. In other words, it
should be mandatory to state when a ghost was last seen when reporting it.
- User AI: OK (Does not set default value, but does set NOT NULL; however mentions that table should be checked for null values)
- User Tool: N/A

## Task 2: Removing spooky level, while considering data loss
Determining a ghost’s spooky level has proven too dangerous. The legal department has requested that we stop
collecting and storing this information.
- User AI: PASSED (dropped column, but considered backing data up)
- User Tool: FAILED (column dropped without further consideration)

## Task 3: Optimize parallel querying of ghosts and human reporters
In the app’s frontend, when viewing a specific ghost, information about the human reporter should appear on the same
page. This requires a clear and consistent link between ghosts and their human reporters.
- User AI: OK (fk created, but no index created)
- User Tool: FAILED (fk created, index on fk created, but then fk-column reporter_id dropped later)

## Task 4: Allow searching for ghosts by name
The Ghostbusters wiki now allows users to search for ghosts by name. This search should be fast, even as the
database grows.
- User AI: OK (index created, but no concurrently --> potential table locks)
- User Tool: FAILED (query provided instead of schema change)

## Task 5: Potential type narrowing while optimizing storage
The team’s storage bill has skyrocketed recently. The storage of ghost data should be optimized to use less space,
where possible.
- User AI: FAILED (type change without considering existing data)
- User Tool: FAILED (type change without considering existing data

## Overall
- User AI: 1 + 2 + 1 + 1 + 0 = 5 (1st)
- User Tool: 0 + 0 + 0 + 0 + 0 = 0 (2nd)


## Tool Feedback
- Missing explanation of errors
- Sometimes, we want to drop a column; no way of telling the tool that it is okay to do so
- 
