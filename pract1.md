# Задача 1
```bash
grep "" /etc/passwd | cut -d: -f1 | sort
```

# Задача 2
```bash
awk '!/^#/ && NF>=2 {print $2, $1}' /etc/protocols | sort -n -r | head -n 5
```

# Задача 3
```bash
#!/bin/bash

TEXT="$1"
LENGTH=${#TEXT}
BORDER="+"
for ((i=0; i<LENGTH+2; i++)); do
    BORDER="${BORDER}-"
done
BORDER="${BORDER}+"

echo "$BORDER"
echo "| $TEXT |"
echo "$BORDER"
```

# Задача 4

# Задача 5

# Задача 6

# Задача 7

# Задача 8

# Задача 9

# Задача 10
