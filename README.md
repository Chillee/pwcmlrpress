# Usage
Just run it, and it'll spit out a json called mlrpress.json

It scrapes all volumes accessible from http://proceedings.mlr.press/ that have volume number >= 30.

# Format

```
{
    'conf_name': str,
    'date': str,
    'papers': [
        {
            'abstract': str?,
            'authors': [str],
            'code': str?,
            'pdf_link': str?,
            'title': str
        }
        ...
    ]
}
```

Note: the date formatting is typically provided as a string in the form "17-19 September 2019", although it can also be empty or "13 September 2019".