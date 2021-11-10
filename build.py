from csv import DictReader
from datetime import datetime
import requests
import os


class IpfsBlogs:
    def __init__(self, file_in, file_out_tpl, file_out) -> None:
        self.file_in = file_in
        self.file_out_tpl = file_out_tpl
        self.file_out = file_out
        self.set_csv()
        # self.get_adoc_table()
        self.write_adoc_table()
        self.write_html()

    def set_csv(self):
        self.blogs = DictReader(open(self.file_in))

    def is_online(self, url):
        try:
            requests.get(url)
            return '✅'
        except:
            return '❌'

    def get_adoc_table(self):
        adoc_table = ('.Online statuses as of %s\n'
                      '|===\n'
                      '|Name |Domain |Online?\n\n'
                      '%s'
                      '|===')
        # print(adoc_table)
        adoc_rows = ''
        for blog in self.blogs:
            name = blog['Name']
            domain = blog['Domain']
            url = f'https://ipfs.io/ipns/{domain}'
            link = f'link:{url}[{domain}]'
            online = self.is_online(url)
            adoc_rows += f'|{name}|{link}|{online}\n'
        today = datetime.today().strftime('%Y-%m-%d')
        return adoc_table % (today, adoc_rows)

    def write_adoc_table(self):
        with open(self.file_out_tpl, 'r') as f:
            tpl = f.read()
        with open(self.file_out, 'w') as f:
            f.write(tpl % self.get_adoc_table())

    def write_html(self):
        os.system(f'asciidoctor -o index.html {self.file_out}')


ipfs_blogs = IpfsBlogs(
    file_in='ipfs-blogs.csv',
    file_out_tpl='README.tpl.adoc',
    file_out='README.adoc',
)
