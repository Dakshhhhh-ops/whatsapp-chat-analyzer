# ChatLens 💬

A WhatsApp conversation analyzer that turns your exported chat into a clean, interactive dashboard — message stats, timelines, emoji breakdowns, activity heatmaps, and response time analysis.

[Live demo → https://whatsapp-chat-analyzer-a2z6kq6te6fgjmupz7hxak.streamlit.app/](https://whatsapp-chat-analyzer-a2z6kq6te6fgjmupz7hxak.streamlit.app/)

---

## What it does

Upload a WhatsApp chat export and get an instant breakdown across five tabs:

**Overview**
- Total messages, words, links, and media files
- Most active participants with message share percentages
- Word cloud of most used words (stopwords filtered)
- Top 10 emoji usage with counts
- Weekly activity heatmap by day and time period

**Timeline**
- Monthly and daily message volume charts
- Busiest months and days of the week

**Media & Links**
- Breakdown of images, videos, audio, stickers, GIFs, and links
- Media vs text ratio pie chart

**Response Time**
- Fastest and slowest responders with average and median times
- Response speed by hour of day — see when your group is most active
- Full reply matrix showing who replies to whom
- Highlights the single fastest pair: who replies to who the quickest

**Raw Data**
- Full parsed message table for manual exploration

---

## Getting started

**Export your chat from WhatsApp**

```
WhatsApp → Open any chat → ⋮ Menu → More → Export chat → Without media
```

This gives you a `.txt` file. Upload it to ChatLens and hit **Run analysis**.

---

## Run locally

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/chatlens.git
cd chatlens
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run**
```bash
streamlit run app.py
```

---

## Requirements

```
streamlit
pandas
matplotlib
wordcloud
emoji
urlextract
```

---

## Project structure

```
chatlens/
├── app.py              # Streamlit UI and all tab rendering
├── preprocessor.py     # Parses raw WhatsApp export into a DataFrame
├── helper.py           # All analysis functions
├── stopwords.txt       # Words filtered from the word cloud
└── requirements.txt
```

**`preprocessor.py`** handles the messy part — regex parsing of WhatsApp's export format into structured columns: `user`, `message`, `date`, `year`, `month`, `day`, `hour`, `minute`, `only_date`, `day_name`, `month_name`, `period`.

**`helper.py`** contains all the analysis logic:

| Function | What it does |
|---|---|
| `fetch_stats` | Message, word, media, and link counts |
| `busiest_users` | Top users by message count and share % |
| `create_wordcloud` | Generates word cloud image |
| `emoji_helper` | Counts emoji frequency |
| `monthly_timeline` | Messages grouped by month |
| `daily_timelime` | Messages grouped by day |
| `month_activity_map` | Messages by month name |
| `week_activity_map` | Messages by day of week |
| `activity_heatmap` | Pivot table of day × time period |
| `response_analysis` | Core response time computation (vectorised) |
| `avg_response_time` | Per-user mean, median, reply count |
| `response_time_by_hour` | Median response time for each hour 0–23 |
| `reply_matrix` | Pivot of who replied to whom |
| `fastest_pair` | Finds the user pair with the highest reply speed ratio |

---

## How response time is calculated

For each message, the time gap since the previous message from a **different user** is recorded. Gaps over 720 minutes (12 hours) are excluded — those are new conversations, not replies. The analysis uses vectorised pandas `shift()` for performance rather than row-by-row iteration.

The **fastest pair** insight compares each user's per-pair average response time against their overall average, requiring a minimum of 5 samples to filter out noise.

---

## Notes

- Works with both Android and iOS WhatsApp exports
- Group chats and one-on-one chats are both supported
- `group_notification` system messages are automatically filtered out
- All processing happens locally in your browser session — your chat data is never stored

---

## Upcoming

- Sentiment timeline — emotional tone of the chat over time
- PDF report export
- Conversation starter analysis — who initiates vs who only responds
