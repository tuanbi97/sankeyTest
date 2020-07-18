import os
import csv

def normalize_url(url):
    url = url.split('/')[-1]
    url = url.split('?')[0]
    if (url == ''): return 'Home'
    return url

def getDate(item):
    return item['Date']

def journey_aggregate(csv_file, first_item_contain_str, max_step = 5, main_id = 'IP Address'):
    records = []
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        cnt = 0
        for row in reader:
            if (cnt == 0):
                headers = []
                for header in row:
                    headers.append(header)
            else:
                record = {}
                for idx, value in enumerate(row):
                    record[headers[idx]] = value
                records.append(record)
            cnt = 1

    person_journey = {}
    for record in records:
        if (record[main_id] not in person_journey):
            person_journey[record[main_id]] = []
        
        n_url = normalize_url(record['MA URL'])
        length = len(person_journey[record[main_id]])
        
        if (length == 0) :
            if (first_item_contain_str in n_url):
                person_journey[record[main_id]].append(n_url)
        else:
            if (n_url != person_journey[record[main_id]][length - 1]):
                person_journey[record[main_id]].append(n_url)
            
    #solution 2
    link_dict = {}
    for step in range(0, max_step):
        for key in person_journey:
            if step >= len(person_journey[key]): 
                continue
            current_page = person_journey[key][step] + '#' + str(step)
            if step > 0:
                link_edge = person_journey[key][step - 1] + '|' + current_page
                if link_edge not in link_dict: 
                    link_dict[link_edge] = 0
                link_dict[link_edge] += 1
            person_journey[key][step] = current_page
            
    source = []
    target = []
    value = []
    label = []
    label_pos = {}
    for key in link_dict:
        s = key.split('|')[0]
        t = key.split('|')[1]
        if s not in label_pos:
            label.append(s)
            label_pos[s] = len(label) - 1
        if t not in label_pos:
            label.append(t)
            label_pos[t] = len(label) - 1
        v = link_dict[key]
        source.append(label_pos[s])
        target.append(label_pos[t])
        value.append(v)

    return source, target, value, label
