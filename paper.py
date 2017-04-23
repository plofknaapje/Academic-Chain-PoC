

class Paper:

    def __init__(self, name, paper_type, authors, cited, reviewers, paper_file, file_hash, paper_interaction):
        """
        Initiates new paper object which stores all the information about a paper
        :param name: str
        :param paper_type: str from [new, confirming, disproving]
        :param authors: list
        :param cited: list, contains names of citated papers
        :param reviewers: list
        :param paper_file: str, file_path to file.
        :param file_hash: str, currently hash of the name value.
        :param paper_interaction: str, paper to whom the type applies. Stored in confirming_paper or disproving_paper
        """

        # Basic data of the Paper object
        self.name = name
        self.status = "draft"
        self.authors = authors
        self.reviewers = reviewers
        self.paper_type = paper_type
        self.file = paper_file
        self.file_hash = file_hash
        self.disproven = False

        # C reward for different actors
        self.c_authors = 0.0
        self.c_reviewers = 0.0
        self.c_confirming = 0.0

        # C constants for fractal rewards
        self.review_constant = 0.2
        self.confirming_constant = 0.2

        self.feedback = []
        self.go = []

        # Variables for interaction with other papers
        self.confirming_paper = ''
        self.disproving_paper = ''
        self.confirmed_by = []
        self.disproven_by = []
        self.citated_by = 0
        self.citated_by_list = []
        self.cited = cited

        if paper_type == "confirming":
            self.confirming_paper = paper_interaction
        elif paper_type == "disproving":
            self.disproving_paper = paper_interaction

    def add_citation(self, amount):
        """
        Adds a citations of another paper to this paper and updates the c-score
        :param amount: int, amount of citations to add.
        :return: Nothing
        """
        if self.disproven:
            self.c_authors = 0
            self.c_reviewers = 0
            self.c_confirming = 0
        else:
            self.citated_by += amount
            self.c_authors += (amount - amount * self.review_constant)

            if len(self.confirmed_by) > 0:
                self.c_authors -= amount * self.confirming_constant
                self.c_confirming += amount * self.confirming_constant

            self.c_reviewers += amount * self.review_constant / (len(self.reviewers))

            if len(self.disproven_by) > 0:
                self.c_authors = 0
                self.c_reviewers = 0
                self.c_confirming = 0
                print "Disproven!"

        persons = self.authors + self.reviewers
        for person in persons:
            person.calculate_c()

    def paper_disproven(self):
        self.disproven = True
        print "Disproven"
