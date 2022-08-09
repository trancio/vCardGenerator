#!/usr/bin/env python3

import os
import csv
from vcardgenerator import VCardGenerator

FILENAME = 'example3'

vcard_name = f'{FILENAME}.vcf'
csv_name = f'{FILENAME}.csv'


def read_csv(filename):
    with open(filename, 'r') as csv_data:
        csv_reader = csv.DictReader(csv_data,
                                    delimiter=';',
                                    skipinitialspace=True)
        data = list(csv_reader)
    return data


def make_vcard(data):
    # iniitialize a vcard version 4.0
    # anniversary is not supported in version 3.0
    vcard = VCardGenerator()
    last = data['last_name']
    first = data['first_name']
    middle = data['middle_name']
    title = data['title']
    if last == '':
        last = None
    if first == '':
        first = None
    if middle == '':
        middle = None
    if title == '':
        title = None
    vcard.add_name(last, first, middle, title)
    if data['birthday'] != '':
        vcard.add_birthday(data['birthday'])
    if data['nameday'] != '':
        vcard.add_nameday(data['nameday'])
    if data['tel_home'] != '':
        vcard.add_phone(data['tel_home'], p_type='home')
    if data['tel_cell'] != '':
        vcard.add_phone(data['tel_cell'], p_type='cell')
    if data['tel_work'] != '':
        vcard.add_phone(data['tel_work'], p_type='work')
    if data['email_home'] != '':
        vcard.add_email(data['email_home'], 'home')
    if data['email_work'] != '':
        vcard.add_email(data['email_work'], 'work')
    if data['relationship'] != '':
        vcard.add_categories(data['relationship'])
    if data['comment'] != '':
        vcard.add_note(data['comment'])
    return vcard


def make_vcards(data):
    vcards = []
    for row in data:
        vcard = make_vcard(row)
        vcards.append(vcard)
    for vcard in vcards:
        vcard.save(FILENAME)


def main():
    csv_data = read_csv(csv_name)
    if os.path.exists(vcard_name):
        os.remove(vcard_name)
    make_vcards(csv_data)


if __name__ == '__main__':
    main()
