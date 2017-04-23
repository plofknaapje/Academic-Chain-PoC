import hashlib


class Blockchain:

    def __init__(self):
        self.length = -1
        self.total_papers = 0
        self.blocks = []
        self.papers = dict()
        self.users = []

    def add_paper(self, paper, paper_name):
        """
        Adds paper with name = paper_name to the blockchain. Checks if the name is unused before executing.
        Creates a new block with the changes
        :param paper: Paper object
        :param paper_name: str
        :return: error messages.
        """

        if paper.name in self.papers:
            return "Error, this name is already in use."
        else:
            self.total_papers += 1
            self.papers[paper_name] = paper

            paper_authors = ""
            paper_reviewers = ""

            for author in paper.authors:
                paper_authors += " " + author.name + ","

            for reviewer in paper.reviewers:
                paper_reviewers += " " + reviewer.name + ","

            changes = "New paper: '{0}' by {1} reviewed by {2}.".format(paper_name, paper_authors, paper_reviewers)

            self.new_block(changes)

    def publish_paper(self, paper_name):
        """
        Publishes a paper to the blockchain and creates a new block to note the changes
        :param paper_name: str
        :return: nothing
        """
        self.papers[paper_name].status = "published"
        changes = "Status of paper " + paper_name + " has been changed from draft to published."

        if self.papers[paper_name].paper_type == "confirming":
            confirming_paper = self.papers[paper_name].confirming_paper
            self.papers[confirming_paper].confirmed_by.append(paper_name)
            changes += "\n'{0}' is a published paper confirming '{1}' and has been added as such. " \
                       "It will receive 20 % of the C of '{2}'.".format(paper_name, confirming_paper, confirming_paper)

        if self.papers[paper_name].paper_type == "disproving":
            disproving_paper = self.papers[paper_name].disproving_paper
            self.papers[disproving_paper].disproven_by.append(disproving_paper)
            self.papers[disproving_paper].paper_disproven()
            changes += "\n'{0}' is a published paper disproving '{1}' and has been added as such. " \
                       "The authors of '{2}' will lose all the C they gained from it.".format(paper_name,
                                                                                              disproving_paper,
                                                                                              disproving_paper)

        self.new_block(changes)

    def review_paper(self, reviewer_name, paper_name, go_no_go, feedback="None"):
        """
        Changes the go_no_go value of a paper by the reviewer and creates a new block to note the changes.
        :param reviewer_name: str
        :param paper_name: str
        :param go_no_go: Bool, True if reviewer thinks paper can be published
        :param feedback: str, feedback from reviewer (default = "None")
        :return: nothing
        """

        self.papers[paper_name].go.append(go_no_go)
        self.papers[paper_name].feedback.append(feedback)
        if go_no_go:
            content = reviewer_name + " has given '{0}' a go for publishing and " \
                                      "the following feedback: '{1}'".format(paper_name, feedback)
        else:
            content = reviewer_name + " has given '{0}' a No go for publishing and " \
                                      "the following feedback: '{1}'".format(paper_name, feedback)

        self.new_block(content)

    def citations_ok(self, papers):
        """
        Checks to see if all the citated papers are papers with status = "published"
        :param papers: list
        :return: Bool, if all papers are "published" -> True
        """
        for paper in papers:
            try:
                if not self.papers[paper].status == "published":
                    return False
            except KeyError:
                return False
        return True

    def print_block_num(self, number):
        """
        Prints the block from the blockchain at number
        :param number: int
        :return: str with content of the block at number
        """
        string = "Block {0} \n{1} \nHash of the previous block: {2} \n".format(self.blocks[number].number,
                                                                               self.blocks[number].changes,
                                                                               self.blocks[number].hash_prev_block)
        return string

    def print_all_blocks(self):
        """
        Prints all the blocks in the blockchain starting from the first block (Block 0).
        :return: All the blocks in the chain.
        """
        for block in self.blocks:
            string = "Block {0} \n{1} \nHash of the previous block: {2} \n".format(block.number, block.changes,
                                                                                   block.hash_prev_block)
            print string

    def new_block(self, content):
        """
        Creates a new Block object from the given content and the hash of the previous block.
        :param content: str with all the information the block should contain
        :return: nothing
        """
        self.length += 1
        try:
            hash_prev_block = hashlib.sha256()
            hash_prev_block.update(self.blocks[-1].changes)
            hash_prev_block = hash_prev_block.digest()
        except IndexError:
            hash_prev_block = "Genesisblock, wohoo"

        self.blocks.append(Block(content, hash_prev_block, self.length))


class Block:

    def __init__(self, content, hash_prev_block, number):
        """

        :param content: str, the content of the block
        :param hash_prev_block: str, the hash of the previous block
        :param number: int, the number of the block
        """
        self.changes = content
        self.hash_prev_block = hash_prev_block
        self.number = number
