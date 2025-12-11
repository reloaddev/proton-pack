# User Test of Prototype Version 1
- Performed on 28-10-2025
- User Manual --> Software Engineer (3 years)
- User AI --> Software Engineer (3 years)
- User Tool --> Software Engineer (1 year)

## Task 1: Adding last seen
Each ghost entry must include when it was last seen, so the team can prioritize active cases. In other words, it
should be mandatory to state when a ghost was last seen when reporting it.
- User Manual: PASSED
- User AI: PASSED
- User Tool: PASSED

Note: This task was defined incorrectly. Instead of adding a new columns, this task should habe been
about making a column NOT NULL that was nullable before.

## Task 2: Removing spooky level, while considering data loss
Determining a ghost’s spooky level has proven too dangerous. The legal department has requested that we stop
collecting and storing this information.
- User Manual: FAILED (column dropped without considering existing data)
- User AI: FAILED (column dropped without considering existing data)
- User Tool: FAILED (column dropped without considering existing data)

## Task 3: Optimize parallel querying of ghosts and human reporters
In the app’s frontend, when viewing a specific ghost, information about the human reporter should appear on the same
page. This requires a clear and consistent link between ghosts and their human reporters.
- User Manual: OK (fk created, but no index created)
- User AI: OK (fk created, but no index created)
- User Tool: FAILED (query provided, instead of changing schema)

## Task 4: Allow searching for ghosts by name
The Ghostbusters wiki now allows users to search for ghosts by name. This search should be fast, even as the
database grows.
- User Manual: OK (index created, but not concurrently --> potential table locks)
- User AI: FAILED (query provided, instead of changing schema)
- User Tool: OK (index created, but not concurrently --> potential table locks)

## Task 5: Potential type narrowing while optimizing storage
The team’s storage bill has skyrocketed recently. The storage of ghost data should be optimized to use less space,
where possible.
- User Manual: OK (type change without considering existing data)
- User AI: FAILED (type change without considering existing data)
- User Tool: FAILED (type change without considering existing data)

## Overall
- User Manual: 2 + 0 + 1 + 1 + 1 = 5 (1st)
- User AI: 2 + 0 + 1 + 0 + 0 = 3 (3rd)
- User Tool: 2 + 0 + 0 + 1 + 0 = 3 (3rd)


## Tool Feedback
- Tool was not specific enough, when reporting an error. Understanding the error messages
and potential negative effects was not clear.
- The DROP column error felt "disappointing", since it felt like limiting the user. There
should have been an explanation for why dropping a column is dangerous.
- Tool didn't trigger in some cases, for example when queries were written instead of schema changes.
