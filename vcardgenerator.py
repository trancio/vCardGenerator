# vCard genartor class with minimal functionality
#
# public methods:
#   add_name(last, first=None, middle=None, title=None, easter_order=False)
#       add FN and N properties
#   add_birthday(bday)
#       birthday with isoformat date string
#   add_anniversary(date)
#       anniversary with isoformat date string
#   add_nameday(namedate)
#       anniversary with mm-dd format date
#   add_categories(tag)
#       information about the vCard
#   add_note(note)
#       comment, supplemental information
#   add_other(property, value)
#       for non supported properties
#   add_email(email, email_type='home')
#       add home/work/... type email after validity check
#   add_emails(emails)
#       add emails from the list
#   add_phone(phone, mobile_operators=None, phone_type='home')
#       add home/work/cell/... type phone number after possibility check
#   add_phones(phones, mobile_operators=None)
#       add phone numbers from the list
#   save(filename, append=True)
#       close and save the vCard append or overwrite mode
#   view():
#       close and pretty print the vCard

import phonenumbers
from phonenumbers import carrier
from pyisemail import is_email
from datetime import datetime


class VCardGenerator:
    def __init__(self, version='4.0'):
        '''Init a vCard object.
           Set version for check property availability.'''
        self.version = version
        self.vcard = []
        self.vcard.append('BEGIN:VCARD')
        self.vcard.append(f'VERSION:{version}')
        self.end = 'END:VCARD'
        self.closed = False

    def add_name(self,
                 last,
                 first=None,
                 middle=None,
                 title=None,
                 eastern_order=False):
        '''Add FN and N properties.'''
        fn = 'FN:'
        if title:
            fn = f'{fn}{title} '
        if eastern_order:
            fn = f'{fn}{last}'
            if first:
                fn = f'{fn} {first}'
                if middle:
                    fn = f'{fn} {middle}'
        else:
            if first:
                fn = f'{fn}{first} '
                if middle:
                    fn = f'{fn}{middle} '
            fn = f'{fn}{last}'
        self.vcard.append(fn)

        n = f'N:{last};'
        if first:
            n = f'{n}{first}'
        n = f'{n};'
        if middle:
            n = f'{n}{middle}'
        n = f'{n};'
        if title:
            n = f'{n}{title}'
        self.vcard.append(n)

    def add_birthday(self, bday):
        '''Add birthday with isoformat date string.'''
        self.vcard.append(f'BDAY:{self._check_date(bday)}')

    def add_anniversary(self, date):
        '''Add anniversary with isoformate date string.'''
        self._check_version()
        self.vcard.append(f'ANNIVERSARY:{self._check_date(date)}')

    def add_nameday(self, date):
        '''Add month - day format anniversary.
           Valid date format: "mm-dd".'''
        self._check_version()
        year = datetime.now().year  # for validity check
        self._check_date(f'{year}-{date}')
        self.vcard.append(f'ANNIVERSARY:--{date[:2]}{date[3:]}')

    def add_categories(self, tag):
        '''Add CATEGORIES property.'''
        self.vcard.append(f'CATEGORIES:{tag}')

    def add_note(self, note):
        '''Add NOTE property.'''
        self.vcard.append(f'NOTE:{note}')

    def add_other(self, prop, value):
        '''To adding not supported property.'''
        self.vcard.append(f'{prop}:{value}')

    def add_email(self, email, e_type='home'):
        '''After validity check add email address.'''
        if is_email(email, check_dns=True):
            self.vcard.append(f'EMAIL;TYPE={e_type}:{email}')
        else:
            print(f'Warning: {email} is not a valid email address.')

    def add_emails(self, emails):
        '''Add email adresses from a list.'''
        if isinstance(emails, list):
            for email in emails:
                self.add_email(email)
        else:
            self.add_email(emails)

    def add_phone(self, phone, mobile_operators=None, p_type='home'):
        '''Add phone number. If the mobile operator is provided,
           TYPE parameter is set to "cell".
        '''
        try:
            p_number = phonenumbers.parse(phone)
            if phonenumbers.is_possible_number(p_number):
                if mobile_operators:
                    provider = carrier.name_for_number(p_number, 'en')
                    if provider in mobile_operators:
                        p_type = f'cell,{p_type}'
                self.vcard.append(f'TEL;VALUE=uri;TYPE={p_type}:tel:{phone}')
            else:
                print(f'Warning: {phone} is not a possible phone number')
        except phonenumbers.NumberParseException as e:
            print(f'Warning: {phone} is not a valid phone number. {e}')

    def add_phones(self, phones, mobile_operators=None):
        '''Add phone numbers from a list.'''
        if isinstance(phones, list):
            for phone in phones:
                self.add_phone(phone, mobile_operators)
        else:
            self.add_phone(phone, mobile_operators)

    def save(self, filename):
        '''Save vCard to file.'''
        if not self.closed:
            self._close_vcard()
        filename = f'{filename}.vcf'
        with open(filename, 'a+') as vcf:
            vcf.writelines([f'{line}\r\n' for line in self.vcard])

    def view(self):
        '''Pretty print the vCard.'''
        if not self.closed:
            self._close_vcard()
        for line in self.vcard:
            print(line)

    def _check_date(self, date):
        '''Check and convert date / datetime string.'''
        if date[-1] == 'Z':
            date = date[:-1]
        d = datetime.fromisoformat(date)
        return d.strftime('%Y-%m-%d')

    def _check_version(self):
        if self.version < '4.0':
            print(
                'Error: Versions lower than 4.0 do not support anniversaries')
            exit(1)

    def _close_vcard(self):
        '''Close vCard definition.'''
        self.vcard.append(self.end)
        self.closed = True
