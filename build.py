from csv import DictReader


class IpfsBlogs:
    def __init__(self, file_in, file_out_tpl, file_out) -> None:
        self.file_in = file_in
        self.file_out_tpl = file_out_tpl
        self.file_out = file_out
        self.set_csv()
        # self.get_adoc_table()
        self.write_adoc_table()

    def set_csv(self):
        self.blogs = DictReader(open(self.file_in))

    def get_adoc_table(self):
        adoc_table = ('|===\n'
        '|Name |Domain\n\n'
        '%s'
        '|===')
        print(adoc_table)
        adoc_rows = ''
        for blog in self.blogs:
            name = blog['Name']
            domain = blog['Domain']
            link = f'link:https://ipfs.io/ipns/{domain}[{domain}]'
            adoc_rows += f'|{name}|{link}\n'
        return adoc_table % adoc_rows

    def write_adoc_table(self):
        with open(self.file_out_tpl, 'r') as f:
            tpl = f.read()
        with open(self.file_out, 'w') as f:
            f.write(tpl % self.get_adoc_table())


ipfs_blogs = IpfsBlogs(
    file_in='ipfs-blogs.csv',
    file_out_tpl='README.tpl.adoc',
    file_out='README.adoc',
)
