fastcat
=======

fastcat is a little Python library for quickly looking up broader/narrower 
relations in Wikipedia categories locally. It relies on redis, and a 
[SKOS](http://downloads.dbpedia.org/current/en/skos_categories_en.nt.bz2) 
file that dbpedia make available based on the Wikipedia MySQL dumps.


Usage
-----

When you first `import fastcat` the SKOS file will be downloaded and loaded 
into your redis instance. After that you'll be able to:

```python
>>> import fastcat
>>> print fastcat.broader("Computer programming")
['Software engineering', 'Computing']
>>> print fastcat.narrower("Computer programming")
['Programming idioms', 'Programming languages', 'Concurrent computing', 'Source code', 'Refactoring', 'Data structures', 'Programming games', 'Computer programmers', 'Version control', 'Anti-patterns', 'Programming constructs', 'Algorithms', 'Web Services tools', 'Programming paradigms', 'Software optimization', 'Debugging', 'Computer programming tools', 'Computer libraries', 'Programming contests', 'Archive networks', 'Self-hosting software', 'Educational abstract machines', 'Software design patterns', 'Computer arithmetic']
```

License
-------

[Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/)
