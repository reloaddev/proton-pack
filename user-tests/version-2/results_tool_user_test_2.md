# User Test 2
## Allowed to use Proton Pack

### Requirement 1
- creates index to speed up reads, however, entries are already ordered
- does not drop old data
- 1/2

### Requirement 2
- handles setting email for rows where value is NULL
- 2/2

### Requirement 3
- duplicate values considered
- unique constraint
- no index created
- 1/2

### Requirement 4
- Creates a new table by joining to ensure fast reads
- Problems: data duplication, slower inserts, added complexity
- 1/2


### Requirement 5
- Decreases data type size
- Does not consider type narrowing
- 1/2

6/10