from ftplib import FTP
import time
import os


class Downloader(object):
    """
        Utility class that downloads the archive dumps from the DILA FTP server
        and extracts it
    """

    def __init__(self, download_dir="/tmp/kali_dump"):
        self.download_dir = download_dir

    def run(self):
        self.connect()
        self.get_last_dump_filename()
        self.download()
        self.extract()

    def connect(self):
        print("connecting to the FTP echanges.dila.gouv.fr ...")
        self.ftp = FTP("echanges.dila.gouv.fr")
        self.ftp.login()
        self.ftp.cwd('KALI')
        print("connected!")

    def get_last_dump_filename(self):
        print("trying to list files to find latest dump name ...")
        full_dump_files = [x for x in self.ftp.nlst() if x.startswith("Freemium_kali")]
        print("ok!")
        if len(full_dump_files) != 1:
            raise Exception("there should be a single Freemium file on the FTP, but found %s" % (len(full_dump_files)))
        self.dump_filename = full_dump_files[0]

    def download(self):
        dump_url = "ftp://echanges.dila.gouv.fr/KALI/%s" % self.dump_filename
        print("starting to download ...")
        # switched to wget, because python was too slow for the actual download
        # with open(full_dump_filename, "wb") as f:
        #     ftp.retrbinary('RETR %s' % full_dump_filename, f.write)
        os.system("wget %s -P %s" % (dump_url, self.download_dir))
        print("download done !")

    def extract(self):
        os.system("mkdir -p %s" % self.download_dir)
        print("extracting tar.gz archive to %s ..." % self.download_dir)
        os.system("pv %s | tar -zxf - -C %s" % (self.dump_filename, self.download_dir))
        print("extract done !")

if __name__ == "__main__":
    Downloader().run()
