# Go-Festival
A website to recommend music festivals based on your favourite Spotify artists

This project has been shelved because Spotify now recommends festivals and concerts inside its client, rendering this much less useful!

The planned app would:

- Scrape data on upcoming festivals from and their lineups https://www.musicfestivalwizard.com/ using Scrapy
- Run this as a cron job on a Raspberry Pi
- Build a SQLite database from this festival data
- Use Flask to create a website in which users could log in with their Spotify account, and have the festivals which their favourite artists were playing at recommended to them
