#!/usr/bin/env python3

import os
from vcard_gen import VCardGenerator

mobile_operators = ['Magyar Telekom', 'Vodafone', 'Telenor', 'Digi']

vcard = VCardGenerator()

vcard.add_name('Doe', 'John', 'Jimmy', 'Dr.')
vcard.add_birthday('1979-03-28')
vcard.add_anniversary('2005-07-12T08:30:00Z')
vcard.add_anniversary('2015-09-06')
vcard.add_nameday('06-27')
vcard.add_categories('family,tester')
vcard.add_note('Uncle')
vcard.add_other('NICKNAME', 'Johnny, Jim')
vcard.add_emails(['jdoe@gmail.com', 'jimdoe@gmail.com'])
vcard.add_email('jjdoe@gmail.com', 'work')
vcard.add_phone('+3620-9123-455', mobile_operators, 'work')
vcard.add_phone('+3614346047', mobile_operators, 'work')
vcard.add_phones(['+3612451654', '+3630-8025-365'], mobile_operators)

filename = 'example2'
if os.path.exists(f'{filename}.vcf'):
    os.remove(f'{filename}.vcf')
vcard.save(filename)
