from csv import DictReader
from datetime import datetime
import requests
import os


class IpfsBlogs:
    def __init__(self, file_in_csv, file_out_adoc_tpl, file_out_adoc, file_out_html) -> None:
        self.file_in_csv = file_in_csv
        self.file_out_adoc_tpl = file_out_adoc_tpl
        self.file_out_adoc = file_out_adoc
        self.file_out_html = file_out_html
        self.set_csv()
        # self.get_adoc_table()
        self.write_adoc_table()
        self.write_html()

    def set_csv(self):
        self.blogs = DictReader(open(self.file_in_csv))

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
            link = f'link:{url}[{domain}, window="_blank"]'
            online = self.is_online(url)
            adoc_rows += f'|{name}|{link}|{online}\n'
        today = datetime.today().strftime('%Y-%m-%d')
        return adoc_table % (today, adoc_rows)

    def write_adoc_table(self):
        with open(self.file_out_adoc_tpl, 'r') as f:
            tpl = f.read()
        with open(self.file_out_adoc, 'w') as f:
            f.write(tpl % self.get_adoc_table())

    def write_html(self):
        os.system(f'asciidoctor -o {self.file_out_html} {self.file_out_adoc}')


ipfs_blogs = IpfsBlogs(
    file_in_csv='ipfs-blogs.csv',
    file_out_adoc_tpl='README.tpl.adoc',
    file_out_adoc='README.adoc',
    file_out_html='index.html',
)
