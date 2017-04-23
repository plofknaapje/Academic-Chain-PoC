import hashlib
from paper import Paper
from torrent import Torrent

class Person:
    def __init__(self, name, blockchain):
        """
        Initiates a new Person who can interact with the blockchain.
        :param name: str
        :param blockchain: Blockchain object, A person can only act on one Blockchain
        """
        self.name = name
        self.published_papers = []
        self.reviewed_papers = []
        self.c_score = 0.0
        self.blockchain = blockchain

    def release_paper(self, paper_name, paper_type, authors, citated, reviewers, paper_file, paper_interaction=""):
        # type: (str, ste, list, list, list, str, str) -> object
        """
        Initiates the release of a paper into the blockchain with status: draft
        :param paper_name: str
        :param paper_type: str from [new, confirming, disproving]
        :param authors: list
        :param citated: list
        :param reviewers: list
        :param paper_file: str, file_path
        :param paper_interaction: str, paper_name of paper which it disproves or confirms
        :return: str, feedback on parameters
        """
        file_hash = hashlib.sha256()
        file_hash.update(paper_file)
        file_hash = file_hash.hexdigest()

        if len(reviewers) + 1 >= 3:
            if self.blockchain.citations_ok(citated):
                if ((paper_type == "disproving" or paper_type == "confirming") and not paper_interaction == "") \
                        or paper_type == "new":
                    new_paper = Paper(paper_name, paper_type, authors, citated, reviewers,
                                      paper_file, file_hash, paper_interaction)

                    torrent = Torrent(paper_file, new_paper)
                    new_paper.magnet = torrent.initialize()
                    print "Magnet link: %s" % new_paper.magnet
                    torrent.seed(torrent.torrent_file)

                    for author in authors:
                        author.published_papers.append(paper_name)

                    for reviewer in reviewers:
                        reviewer.reviewed_papers.append(paper_name)

                    self.blockchain.add_paper(new_paper, paper_name)

                    return "Paper released successfully"
                else:
                    return "Paper-interaction variable is required to release a paper that is not new"
            else:
                return "One or more of your citations seem to be unpublished papers. These can't be used as citations"
        else:
            return "%i reviewers is not enough, a minimum of 3 is required" % len(reviewers)

    def publish_paper(self, paper_name):
        """
        Checks for go from reviewers and manages citations. Changes status to published
        :param paper_name: str
        :return: str, error if problem with approval
        """
        if False not in self.blockchain.papers[paper_name].go and len(self.blockchain.papers[paper_name].go) > 1:
            self.blockchain.publish_paper(paper_name)
            for citation in self.blockchain.papers[paper_name].cited:
                self.blockchain.papers[citation].citated_by_list.append(citation)
                self.blockchain.papers[citation].add_citation(1)
        else:
            return "Error, this paper has not yet been approved by it's reviewers"

    def find_paper(self, paper_name, paper_status):
        """
        Looks for paper of this person
        :param paper_name: str
        :param paper_status: str from [draft, published, reviewed]
        :return: Paper object or str error.
        """
        if paper_status == "draft":
            if paper_name in self.published_papers and paper_name in self.blockchain.papers and \
                            self.blockchain.papers[paper_name].status == paper_status:
                return self.blockchain.papers[paper_name]
            else:
                return "Draft paper could not be found"
        elif paper_status == "published":
            if paper_name in self.published_papers and paper_name in self.blockchain.papers and \
                            self.blockchain.papers[paper_name].status == paper_status:
                return self.blockchain.papers[paper_name]
            else:
                return "Published paper could not be found"
        elif paper_status == "reviewed":
            if paper_name in self.reviewed_papers and paper_name in self.blockchain.papers:
                return self.blockchain.papers[paper_name]
            else:
                return "Reviewed paper could not be found"
        else:
            return paper_status + " is not valid, valid statuses are: draft | published | reviewed "

    def review_paper(self, paper_name, go_no_go, feedback):
        """
        Lets Person review a paper
        :param paper_name: str
        :param go_no_go: Bool
        :param feedback: str
        :return:
        """
        if paper_name in self.reviewed_papers:
            self.blockchain.review_paper(self.name, paper_name, go_no_go, feedback)
        else:
            return "You are not a reviewer of this paper!"

    def calculate_c(self):
        """
        Recalculates the C-Score of a person
        :return: int
        """
        self.c_score = 0.0
        for paper in self.published_papers:
            if self.blockchain.papers[paper].status == "published":
                self.c_score += self.blockchain.papers[paper].c_authors
                if self.blockchain.papers[paper].paper_type == "confirming":
                    confirming_paper = self.blockchain.papers[paper].confirming_paper
                    self.c_score += self.blockchain.papers[confirming_paper].c_confirming
            else:
                print "This paper ({0}) has the draft status and will not be counted as a citation.".format(
                    self.blockchain.papers[paper].name)
        for paper in self.reviewed_papers:
            self.c_score += self.blockchain.papers[paper].c_reviewers

        return self.c_score
