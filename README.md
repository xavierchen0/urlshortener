# URL Shortener

> Short URLs are like a box of chocolates... you never know where they’re gonna
> redirect.

# Usage

Use the web app via this [link](https://urlshortener-74dy.onrender.com/).

# Approach

**Functional Requirements:**

1. Able to convert a long URL to a short URL,
2. Short URL should redirect user to the long URL.

For (1), the challenge is creating a one-to-one map between the short URL and
long URL. With an infinitely many long URLs, I must therefore create infinitely
many short URLs, but this isn't feasible.

I initially tried to use a random string generator to create the short URL but
soon realised that given sufficient time, there will be a chance that there will
be two of the same short URLs.

I then considered using a hashing algorithm, like SHA, but I quickly realised
that even the smallest output of the SHA algorithm is too long to be suitable
for use as a short URL. Taking a substring of the output simply increases the
risk of duplicated short URLs.

With the original intention to create a database, I realised that I can use the
unique row id provided by my database as the primary key for each long URL. To
reduce the number of characters, I can change the integer row id from base-10 to
base-62, where 62 comes from the number of characters in `[0-9a-zA-Z]` and these
are the only characters I am using for my short URL. This methodology underlies
how the short url is generated.

For (2), with the short url generated, I can query the database for rows with
that short URL. Since there is a one-to-one mapping between the short and long
URL, there will only be either one or zero row for that short URL. If the short
URL exists in the database, I redirect the user to the long URL, otherwise, I
return a HTTP `404` status code to the user.

# Tech Stack

Goal: Make a simple web app that is easy to build and with minimal dependencies.

`Python` - For the backend server logic and request routing.

`HTMX` - For dynamic frontend interaction directly from HTML without needing
JavaScript frameworks.

`Tailwind CSS` - For easy and quick UI styling.

`SQLAlchemy` - For managing database interactions between PostgreSQL and SQLite.

# Development

## Installation

**Via `uv`**

```bash
uv sync
```

**Via `pip`**

```bash
pip install -r requirements.txt
```

## Execution

**Via `uv`**

```bash
uv run flask run
```

**Via `pip`**

```bash
flask run
```
