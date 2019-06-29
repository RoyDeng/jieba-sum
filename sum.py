import sys
import os
import csv
import time
import jieba
from jieba import analyse
from collections import defaultdict
from json import dumps
import time

try:
    amb_list = ['相信', '認為', '不確定', '突然', '推測']
    risk_list = ['預期', '大約', '可能', '變化', '預計']

    for (root, dirs, files) in os.walk('./articles'):
        for name in files:
            start_time = time.time()
            year = os.path.splitext(name)[0]
            row_count = 0
            data_list = []

            with open('./articles/%s.csv' % (year), 'r', newline='', encoding = 'gb18030') as csvfile:
                row_count = sum(1 for row in csvfile) - 1

            with open('./articles/%s.csv' % (year), 'r', newline='', errors='ignore') as csvfile:
                rows = csv.reader(csvfile)
                next(rows)

                for row in rows:
                    amb = 0
                    risk = 0
                    word_list = list(analyse.textrank(row[5].strip()))

                    print(word_list)

                    for word in word_list:
                        if any(word in amb_word for amb_word in amb_list):
                            amb += 1
                        if any(word in risk_word for risk_word in risk_list):
                            risk += 1

                    data_list.append({
                        'code': row[0].strip(),
                        'amb': amb,
                        'risk': risk
                    })

                    process = 100 * float(len(data_list)) / float(row_count)

                    if int(process) == float(process):
                        decimals = 0
                    else:
                        decimals = 2

                    print('jieba process of %s: %s%%' % (year, '{0:.{1}f}'.format(process, decimals)))

            data_dict = {}

            for data in data_list:
                code = data['code']
                if code in data_dict:
                    data_dict[code]['amb'] = data_dict[code]['amb'] + data['amb']
                    data_dict[code]['risk'] = data_dict[code]['risk'] + data['risk']
                else:
                    data_dict[code] = data

            result_list = list(data_dict.values())

            print('start dumping %s result into data...' % (year))

            with open('./data/data%s.csv' % (year), 'w', newline='', encoding = 'cp950') as csvfile:
                fieldnames = ['Code', 'Year', 'AMB', 'Risk']
                rows = csv.DictWriter(csvfile, fieldnames = fieldnames)
                rows.writeheader()

                for row in result_list:
                    rows.writerow({'Code': row.get('code'), 'Year': year, 'AMB': str(row.get('amb')), 'Risk': str(row.get('risk'))})

            print('end dumping %s result into data...' % (year))
            print('execution time: %.2f s' % (round(time.time() - start_time, 1)))

except:
    print(sys.exc_info())