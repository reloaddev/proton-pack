# User Test 2
## Not allowed to use Proton Pack

### Requirement 1
- Considers data loss
- Provides index solution
- 2/2

### Requirement 2
- Considers that setting email to NOT NULL will break, in case there is NULL values
- Getting their emails should be ensure, before setting it to NOT NULL
- 2/2

### Requirement 3
- Considers duplicate names
- Considers adding an index
- Does not consider concurrent building
- 1/2

### Requirement 4
- Creates a new table by joining to ensure fast reads
- Problems: data duplication, slower inserts, added complexity
- 1/2

### Requirement 5
- Considers deduplicates
- Considers datatypes
- Does not explicitly consider type narrowing
- 1/2

7/10