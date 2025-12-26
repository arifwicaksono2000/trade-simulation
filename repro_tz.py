from datetime import datetime, timezone

# Arbitrary time: 2023-01-01 12:00:00
# If this is UTC, it refers to 12:00 UTC.
naive_dt = datetime(2023, 1, 1, 12, 0, 0)
print(f"Naive DT: {naive_dt}")

# Naive timestamp (treats as local time)
ts_naive = naive_dt.timestamp()
print(f"Naive Timestamp (system assumes local): {ts_naive}")

# Aware UTC timestamp
aware_dt = naive_dt.replace(tzinfo=timezone.utc)
print(f"Aware DT: {aware_dt}")
ts_aware = aware_dt.timestamp()
print(f"Aware Timestamp (UTC): {ts_aware}")

diff = ts_naive - ts_aware
print(f"Difference (seconds): {diff}")
print(f"Difference (hours): {diff / 3600}")
