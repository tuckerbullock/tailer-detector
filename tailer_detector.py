import random, uuid
import pandas as pd
from datetime import datetime, timedelta, UTC
import matplotlib.pyplot as plt

# ---------------------------
# CONFIGURATION
# ---------------------------
NUM_USERS = 300
NUM_SHARPS = 8
NUM_PROPS = 120
NUM_GROUPS = 5
TAILERS_PER_GROUP = 10
TAIL_PROBABILITY = 0.8        # less than perfect tailing for realism
TAIL_LAG_MEAN = 8
TAIL_LAG_STD = 3
NOISE_PROB = 0.05
random.seed(42)

# ---------------------------
# STEP 1: Generate sharp picks
# ---------------------------
def gen_sharp_posts(n_sharps=NUM_SHARPS, n_props=NUM_PROPS, start_time=None):
    posts = []
    start_time = start_time or datetime.now(UTC)  # ✅ no warning anymore
    for i in range(n_props):
        t = start_time + timedelta(seconds=i * 30)
        sharp = f"sharp_{random.randint(1, n_sharps)}"
        posts.append({
            'prop_id': f"prop_{i}",
            'sharp_id': sharp,
            'post_time': t
        })
    return pd.DataFrame(posts)

# ---------------------------
# STEP 2: Create user groups
# ---------------------------
def create_user_groups(num_users=NUM_USERS, num_groups=NUM_GROUPS, tailers_per_group=TAILERS_PER_GROUP):
    users = [f"user_{i}" for i in range(num_users)]
    tailer_groups = []
    used_users = set()

    for _ in range(num_groups):
        group_members = random.sample([u for u in users if u not in used_users], tailers_per_group)
        used_users.update(group_members)
        tailer_groups.append(group_members)

    normal_users = [u for u in users if u not in used_users]
    return tailer_groups, normal_users

# ---------------------------
# STEP 3: Generate bets
# ---------------------------
def gen_bets(posts_df, tailer_groups, normal_users):
    bets = []
    sharps = posts_df['sharp_id'].unique()
    group_sharp_map = {i: random.choice(sharps) for i in range(len(tailer_groups))}

    for _, post in posts_df.iterrows():
        prop = post['prop_id']
        sharp = post['sharp_id']

        # Tailers follow their assigned sharp ~80% of the time with slight randomness
        for group_id, group in enumerate(tailer_groups):
            if group_sharp_map[group_id] == sharp:
                for user in group:
                    if random.random() < TAIL_PROBABILITY + random.uniform(-0.1, 0.1):
                        lag = max(0, random.gauss(TAIL_LAG_MEAN, TAIL_LAG_STD))
                        t = post['post_time'] + timedelta(seconds=lag)
                        bets.append({
                            'bet_id': str(uuid.uuid4()),
                            'timestamp': t,
                            'user_id': user,
                            'prop_id': prop,
                            'sharp_followed': sharp
                        })

        # Normal users randomly place bets
        for user in normal_users:
            if random.random() < NOISE_PROB:
                t = post['post_time'] + timedelta(seconds=random.randint(30, 3600))
                bets.append({
                    'bet_id': str(uuid.uuid4()),
                    'timestamp': t,
                    'user_id': user,
                    'prop_id': prop,
                    'sharp_followed': None
                })
    return pd.DataFrame(bets)

# ---------------------------
# STEP 4: Detection logic
# ---------------------------
def detect_tailers(bets, posts, lag_threshold=30, min_count=5, tail_score_threshold=0.6):
    merged = bets.merge(posts, on='prop_id', how='left')
    merged['lag'] = (merged['timestamp'] - merged['post_time']).dt.total_seconds()
    cand = merged[merged['lag'].between(0, lag_threshold)]
    grouped = cand.groupby('user_id').agg(
        tail_count=('bet_id', 'count'),
        total_shared_bets=('prop_id', 'nunique')
    ).reset_index()
    grouped['tail_score'] = grouped['tail_count'] / (grouped['total_shared_bets'] + 1e-6)
    flagged = grouped[
        (grouped['tail_count'] >= min_count) &
        (grouped['tail_score'] >= tail_score_threshold)
    ].sort_values(by='tail_score', ascending=False)

    sharp_summary = cand.groupby('sharp_id').agg(
        tailers_detected=('user_id', 'nunique'),
        total_tail_bets=('bet_id', 'count')
    ).reset_index().sort_values(by='tailers_detected', ascending=False)

    return flagged, sharp_summary

# ---------------------------
# STEP 5: Visualization
# ---------------------------
def visualize(flagged_users, sharp_summary):
    # Top tailers
    top_tailers = flagged_users.head(15)
    plt.figure(figsize=(12, 6))
    plt.bar(top_tailers['user_id'], top_tailers['tail_count'], color='royalblue')
    plt.xticks(rotation=45, ha='right')
    plt.title('Top Detected Tailers')
    plt.xlabel('User ID')
    plt.ylabel('Tail Count')
    plt.tight_layout()
    plt.savefig('top_tailers_chart.png')
    plt.close()

    # Most tailed sharps
    plt.figure(figsize=(8, 5))
    plt.bar(sharp_summary['sharp_id'], sharp_summary['total_tail_bets'], color='orange')
    plt.title('Most Tailed Sharps')
    plt.xlabel('Sharp ID')
    plt.ylabel('Total Tail Bets')
    plt.tight_layout()
    plt.savefig('most_tailed_sharps_chart.png')
    plt.close()

    print("📊 Charts saved as top_tailers_chart.png and most_tailed_sharps_chart.png")

# ---------------------------
# RUN EVERYTHING
# ---------------------------
if __name__ == "__main__":
    print("⏳ Generating fake data...")
    posts_df = gen_sharp_posts()
    tailer_groups, normal_users = create_user_groups()
    bets_df = gen_bets(posts_df, tailer_groups, normal_users)

    print(f"✅ Generated {len(posts_df)} sharp picks")
    print(f"✅ {len(tailer_groups)} tailing groups, {len(normal_users)} normal users")
    print(f"✅ {len(bets_df)} total bets generated")

    print("\n🚨 Running detection...")
    flagged_users, sharp_summary = detect_tailers(bets_df, posts_df)

    print("\n🏁 Flagged Tailers:")
    print(flagged_users.head(20))

    print("\n📊 Most Tailed Sharps:")
    print(sharp_summary)

    # Export results to CSV
    flagged_users.to_csv("flagged_tailers.csv", index=False)
    sharp_summary.to_csv("sharp_summary.csv", index=False)
    print("💾 Results saved to flagged_tailers.csv and sharp_summary.csv")

    # Generate charts
    visualize(flagged_users, sharp_summary)
