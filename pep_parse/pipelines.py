import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).parents[1]
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'


class PepParsePipeline:

    def __init__(self):
        self.results_dir = BASE_DIR / 'results'
        self.results_dir.mkdir(exist_ok=True)
        self.count_of_statuses = defaultdict(int)

    def open_spider(self, spider):
        now_formatted = dt.datetime.now().strftime(DATETIME_FORMAT)
        file_name = f'status_summary__{now_formatted}.csv'
        file_path = self.results_dir / file_name
        self.file = csv.writer(open(file_path, 'w', encoding='utf-8'),
                               dialect='unix')
        self.file.writerow(['Статус', 'Количество'])

    def process_item(self, item, spider):
        self.count_of_statuses[item['status']] += 1
        return item

    def close_spider(self, spider):
        self.count_of_statuses['Total'] = sum(self.count_of_statuses.values())
        self.file.writerows(self.count_of_statuses.items())
