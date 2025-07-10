---
date: 2025-02-13 01:49:19.419329
---

With the power of PostgreSQL, Python, and claude, I:

- Transposed some blog analytics by year from our company analytics service (exported to csv)
- Uploaded that raw data into Postgres
- Created a function that looked at each month and found the top three posts
- Moved those results into a temp_table that can use to get more information and do more analysis

Genuinely the most helpful AI has been and it still took about 2 hours of feeding the errors back in and explaining what it did wrong... Now I will have it explain each line of that gnarly function to me so I can write a new blog post...

![God and Anime on my side meme but with the power of Python SQL and AI](https://jmblogstorrage.blob.core.windows.net/media/power-of-python-sql-ai.jpg)
