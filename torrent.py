import os
import shutil

from storjtorrent import StorjTorrent as storrent

from paper import Paper


class Torrent:
    def __init__(self, file_path, paper):
        self.torrent_manager = storrent()
        self.torrent_file = ''
        assert isinstance(paper, Paper)
        self.paper = paper
        self.file = file_path

    @staticmethod
    def getMagnet(torrent_file):
        return "magnet:?xt=urn:btih:%s" % storrent.get_hash([], torrent_path=torrent_file)

    def seed(self, torrent_file):
        self.torrent_manager.add_torrent(torrent_file, True)
        print self.torrent_manager.get_status()

    def initialize(self):
        """
        Starts seeding the torrent from the local computer
        :return: Returns the magnet link for downloading
        """
        print self.paper.authors
        print self.paper.reviewers
        comment = "Authors: {0} - Reviewers: {1}".format(', '.join([author.name for author in self.paper.authors]),
                                                         ', '.join(
                                                             [reviewer.name for reviewer in self.paper.reviewers]))

        shared_directory = 'data/%s' % self.paper.file_hash
        new_file_path = os.path.join(shared_directory, self.paper.name + ".pdf")
        save_path = 'data/torrents/%s.torrent' % self.paper.file_hash

        # Create the sharing directory
        if not os.path.exists(shared_directory):
            os.mkdir(shared_directory)

        # Copy the files to the shared directory
        shutil.copyfile(self.file, new_file_path)

        # Create the torrent
        created_torrent = storrent.generate_torrent([],
                                                    shard_directory=shared_directory,
                                                    torrent_name=save_path,
                                                    comment=comment)
        self.torrent_file = save_path

        return Torrent.getMagnet(save_path)
