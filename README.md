# Sports Betting Tailer Detector

***Overview***
This project simulates how sharp bettors and tailing users interact with sports betting props — and builds a simple detection system that identifies **groups of tailers** who follow sharp picks too consistently.  
The simulation is designed to mimic real-world betting app behavior and can be extended into more advanced analysis later.

*First, let's start with the:*

Problem:

  There are large Discord (social platform) servers ran by extremely intelligent sports bettors (called sharps, in slang) that send out their picks on certain player props to a large number of users who tail them quickly. This allows many users to profit a lot off of these sports betting companies, using the picks of intelligent sports bettors. 
  In response, apps have become better and better at temporarily removing (called "pulling") and adjusting (called "bumping") props when they know that this is occurring, but they are not perfect. I've seen apps like "Chalkboard" and "Underdog Fantasy" pull and bump props incredibly quickly, and be very effective in limiting “sharp” groups of tailers...
So it is clear this is what apps want to do, but it seems they can’t quite find a consistent way to pull/bump every time.


*So, I thought...*

  Is there a way to more effectively identify successful users and groups that tail sharps, in order to more effectively apply limits to successful users?

Well, why is this imporant?

  This is an important topic for especially some of the biggest companies, like:

  Underdog Fantasy:
  This app includes a "Streaks" feature, where users can keep a "streak" of picks in a row, and if they get to 11 correct, they can cash their $10 entry out to typically $10,000. This means that small mistakes in props can lead to huge losses for UD, as sharps will identify this error and many tailers will add this pick to their streak. Minimizing pull times for these props would have serious savings.

  Dabble: 
  This app, despite being so popular, simply just has the lowest pull time I've seen, along with the slowest limits. These are huge losses for the company, but great for bettors.

  PrizePicks:
  This is possibly the Largest company, and has the most wide selection of niche props that sharps like to attack (eSports, Darts, etc.). A wider market allows sharps to exploit more errors, and they need to be quick to remove potential huge mistakes.

  Essentially, it would be greatly beneficial to come up with a faster/more consistent way to identify which props need to be removed to limit effects of inaccurate lines (according to proven sharp outside analysts)

*My Solution:*

  A project that builds a database on who is tailing communities for various sharps, and potentially companies could use this idea/framework to implement faster prop pull times by using this pattern identification (I understand this is simple code, I find the value to be in the framework) (Fake data is generated in the code, since of course I don't have access to the database of these companies.)
  

## Some Features
-  **Sharp bettor simulation:** Randomly generates prop bet picks and timestamps.  
-  **Tailer groups:** Simulates multiple groups of users tailing specific sharps.  
-  **Detection logic:** Flags suspicious users based on lag time and tailing frequency.  
-  **Data visualization:** Bar charts of top tailers and most-tailed sharps.  
-  **CSV export:** Saves `flagged_tailers.csv` and `sharp_summary.csv` automatically.

---

## Tech Stack
- **Language:** Python 3.13
- **Libraries:**  
  - `pandas` for data handling  
  - `matplotlib` for visualization  
  - `uuid` and `datetime` for event simulation


## File Structure
tailer-detector/
│
├─ tailer_detector.py # main simulation + detection script
├─ flagged_tailers.csv # saved tailer results
├─ sharp_summary.csv # summary of sharp activity
├─ top_tailers_chart.png # visualization of top tailers
├─ most_tailed_sharps_chart.png # visualization of most tailed sharps
└─ README.md # this file


## How It Works
1. The script creates fake sharp bettors and tailers.  
2. Each sharp posts prop picks at set intervals.  
3. Tailer groups mimic real-world behavior by placing bets shortly after sharps.  
4. The detection algorithm:  
   - Calculates **lag time**  
   - Flags users with consistently short lag times and high overlap with sharps  
5. Results are saved and visualized.


## Example Output
✅ Generated 120 sharp picks
✅ 5 tailing groups, 250 normal users
✅ 2192 total bets generated

🏁 Flagged Tailers:
user_id tail_count total_shared_bets tail_score
0 user_43 19 19 1.0
1 user_67 18 18 1.0
...

📊 Most Tailed Sharps:
sharp_id tailers_detected total_tail_bets
0 sharp_4 20 320
1 sharp_6 20 235
...


## Example Charts
- `top_tailers_chart.png` → Top flagged tailers.  
- `most_tailed_sharps_chart.png` → Most tailed sharps.


Future Improvements
-Add less predictable tailing behavior (noise, mistakes, random delays).
-Build a simple dashboard for visualizing tailing activity in real-time.
-Implement a scoring system to rank suspicious users.
-Add ML or statistical models for sharper detection.


This project was developed with the assistance of AI tools (ChatGPT) for code structuring and debugging.


Author:
Tucker Bullock
UT Austin • Statistics and Data Science Student• Aspiring Software Engineer/Data Analyst/Data Scientist
📬 [www.linkedin.com/in/tucker-bullock]
