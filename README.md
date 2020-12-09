# Meaningful passwords

This tool generates passwords based on the meanings of a list of words

## Quickstart

Install dependencies and generate your first password, using the default dictionary

```shell
$ pip install -r requirements.txt
$ python password_generator.py
70-iNspire-unSelfish-Benefits
```

### Generating multiple passwords

To create multiple passwords use

```shell
$ python password_generator.py -p 10
```

## Advanced usage

### Creating a custom dictionary

#### How it works

In the file ``context.json`` there are a couple of lists:

- Each word in ``wordlist`` is combined with the words in ``similar`` and ``negative``. This creates an offset in the
  meaning of the generated words.
- Then for each word ``wordlist`` a given amount of similar words is found. This can be specified with the ``-a``
  argument

So each found 'synonym' will have an offset in meaning closer to ``similar`` and further from ``negative``. This means
that the words in ``similar`` and ``negative`` influence every entry of your dictionary.

The default dictionary is generated with 200 'synonyms' per word.

#### Let's generate the dictionary!

Adjust ``context.json`` to your liking, you will probably have to tune it a couple of times.

For testing purposes you can use a smaller dictionary and model and print 10 passwords:
```shell
$ python password_generator.py -a 30 -l minlength=3 -h maxlength=10 -m glove-wiki-gigaword-50 -p 10
```

When your passwords are starting to look nice, generate a larger dictionary with
```shell
$ python password_generator.py -g
```

Replace '10' with the desired amount of passwords

### Other options

To see all available options and their meanings run:
```shell
$ python password_generator.py -h
```
This prints the contents of the [help file](./help)
