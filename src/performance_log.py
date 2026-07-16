import json
from pathlib import Path

import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = REPO_ROOT / "docs" / "performance_log.json"

# load the logged data
with open(LOG_FILE, "r") as f:
    log_data = json.load(f)

# convert seconds to milliseconds
log_data_ms = {method: [time * 1000 for time in times] for method, times in log_data.items()}

# average of each method
averages = {method: sum(times) / len(times) for method, times in log_data_ms.items()}

# sort data for plotting
methods = list(averages.keys())
avg_times = list(averages.values())

# plot the chart
plt.figure(figsize=(8, 6))  # narrower figure to reduce space between bars
bars = plt.bar(methods, avg_times, color=["lightblue", "lightgreen", "lightcoral"], width=1)
plt.xlabel("edge detection method")
plt.ylabel("average processing time (ms)")
plt.title("edge detection method performance comparison")
plt.xticks(rotation=10)
plt.tight_layout()

# add the exact value on top of each bar
for bar, avg_time in zip(bars, avg_times):
    plt.text(
        bar.get_x() + bar.get_width() / 2,  # x position of the text
        bar.get_height(),                   # y position of the text (bar height)
        f"{avg_time:.2f}",                  # text to display, 2 decimal places
        ha="center", va="bottom"            # horizontal and vertical alignment
    )

plt.show()
