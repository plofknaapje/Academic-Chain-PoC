import shutil

from storjtorrent import StorjTorrent as storrent
from paper import Paper
from person import Person

import os


class Torrent:
    def __init__(self, file_path, person, paper):
        assert isinstance(person, Person)
        assert isinstance(paper, Paper)
        self.paper = paper
        self.person = person
        self.file = file_path

    @staticmethod
    def getMagnet(torrent_file):
        return "magnet:?xt=urn:btih:%s" % storrent.get_hash([], torrent_path=torrent_file)

    def seed(self):
        """
        Starts seeding the torrent from the local computer
        :return: Returns the magnet link for downloading
        """
        comment = "Authors: %s - Reviewers: %s" % (self.paper.authors.join(', '), self.paper.reviewers.join(', '))
        shared_directory = 'data/%s' % self.paper.file_hash
        new_file_path = os.path.join(shared_directory, self.paper.name + ".pdf")
        save_path = 'data/torrents/temp.torrent'

        # Create the sharing directory
        os.mkdir(shared_directory)

        # Copy the files to the shared directory
        shutil.copyfile(self.file, new_file_path)

        # Create the torrent
        created_torrent = storrent.generate_torrent([],
                                                    shard_directory=shared_directory,
                                                    torrent_name=self.paper.name,
                                                    comment=comment, save_path=save_path)
        return Torrent.getMagnet(save_path)
