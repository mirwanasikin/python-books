import json
import sys
import os

from datetime import datetime

progress_path = os.path.join(os.path.dirname(__file__), '..', 'progress', 'progress.json')

with open(progress_path) as f:
    data = json.load(f)

print(json.dumps(data, indent=2))

def mark_completed(day):
    with open(progress_path, 'r') as f:
        data = json.load(f)

    if day not in data['completed_days']:
        data['completed_days'].append(day)
        data['current_day'] = max(data['current_day'], day)
        data['updated_at'] = datetime.now().strftime('%Y-%m-%d')

        with open(progress_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f'Day {day} marked completed')
    else:
        print(f'Day {day} already completed')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        mark_completed(int(sys.argv[1]))
    else:
        print('Usage: python scripts/check_progress.py [day_number]')