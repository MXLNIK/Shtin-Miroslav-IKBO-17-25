# Задача 1
```bash
grep "" /etc/passwd | cut -d: -f1 | sort
```

# Задача 2
```bash
awk '!/^#/ {print $2, $1}' /etc/protocols | sort -n -r | head -n 5
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
```bash
#!/bin/bash

FILE=$1
grep -oP '[a-zA-Z_][a-zA-Z0-9_]*' "$FILE" | sort -u | tr '\n' ' '
echo ""
```

# Задача 5
```bash
#!/usr/bin/env bash

SCRIPT_NAME="$1"
TARGET_DIR="/usr/local/bin"
chmod 755 "$SCRIPT_NAME"
sudo cp "$SCRIPT_NAME" "$TARGET_DIR/"
```

# Задача 6
```bash
#!/bin/bash

FILE="$1"
FIRST_LINE=$(head -n 1 "$FILE" | sed 's/^[[:space:]]*//')
if [[ "$FIRST_LINE" =~ ^// ]] || [[ "$FIRST_LINE" =~ ^/\* ]] || [[ "$FIRST_LINE" =~ ^# ]]; then
    echo "Comments found"
else
    echo "Comments not found"
fi
```

# Задача 7
```bash

```

# Задача 8
```bash

```

# Задача 9
```bash

```

# Задача 10
```bash

```
