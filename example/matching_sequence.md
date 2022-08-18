# Matching sequences

Your main loop will need to get input from the user and split it into words, let’s say a list of strings like this:

```py
command = input("What are you doing next? ")
# analyze the result of command.split()
```

The next step is to interpret the words. Most of our commands will have two words: an action and an object. So you may be tempted to do the following:

```py
[action, obj] = command.split()
...  # interpret action, obj
```

The problem with that line of code is that it’s missing something: what if the user types more or fewer than 2 words? To prevent this problem you can either check the length of the list of words, or capture the `ValueError` that the statement above would raise.

You can use a matching statement instead:

```py
match command.split():
    case [action, obj]:
        ...  # interpret action, obj
```

[source]: https://peps.python.org/pep-0636/
