import blockchain
from person import Person

# Create blockchain
test_blockchain = blockchain.Blockchain()

# Creating persons

# Test author
robin = Person("Robin Verhoef", test_blockchain)
jochem = Person("Jochem Raat", test_blockchain)
marien = Person("Marien Raat", test_blockchain)

# Test reviewers
leendert = Person("Leendert Verhoef", test_blockchain)
ad = Person("Ad van Wijk", test_blockchain)
philipe = Person("Philipe Geubels", test_blockchain)


# Paper 1 test values
paper_name = "Academic blockchain system"
paper_type = "new"
authors = [robin]
citated = []
reviewers = [leendert, ad, philipe]
paper_file = "paper1.pdf"

# First paper !!!!
robin.release_paper(paper_name, paper_type, authors, citated, reviewers, paper_file)

# Tests for first paper
# print robin.find_paper("Academic blockchain system", "released")
# print ad.reviewed_papers
# print test_blockchain.print_block_num(0)

# Review of paper
ad.review_paper("Academic blockchain system", True, "None")
leendert.review_paper("Academic blockchain system", True, "None")
philipe.review_paper("Academic blockchain system", True, "None")

robin.publish_paper("Academic blockchain system")
input()
if(False):
    # Paper 2 test values
    paper_name = "Academic blockchain mining"
    paper_type = "confirming"
    authors = [robin]
    citated = ["Academic blockchain system"]
    reviewers = [leendert, ad, philipe]
    paper_file = "paper2.pdf"

    robin.release_paper(paper_name, paper_type, authors, citated, reviewers, paper_file, "Academic blockchain system")

    # Tests for second paper
    # print test_blockchain.print_block_num(1)

    # Test to publish paper
    # print robin.publish_paper("Academic blockchain mining")

    # Reviewing second paper
    ad.review_paper("Academic blockchain mining", True, "None")
    leendert.review_paper("Academic blockchain mining", True, "None")
    philipe.review_paper("Academic blockchain mining", True, "None")

    # Retry publishing
    robin.publish_paper("Academic blockchain mining")

    # New papers

    marien.release_paper("Stupidity of tech support tickets", "new", [marien], ["Academic blockchain system"],
                         [leendert, ad, philipe], "supid.openpdf")
    ad.review_paper("Stupidity of tech support tickets", True, "None")
    leendert.review_paper("Stupidity of tech support tickets", True, "None")
    philipe.review_paper("Stupidity of tech support tickets", True, "None")
    marien.publish_paper("Stupidity of tech support tickets")

    jochem.release_paper("Intelligence of tech support tickets", "disproving",
                         [jochem], ["Stupidity of tech support tickets"], [leendert, ad, philipe],
                         "smart.pdf", "Stupidity of tech support tickets")
    ad.review_paper("Intelligence of tech support tickets", True, "None")
    leendert.review_paper("Intelligence of tech support tickets", True, "None")
    philipe.review_paper("Intelligence of tech support tickets", True, "None")
    jochem.publish_paper("Intelligence of tech support tickets")

    print jochem.c_score
    print marien.c_score

# Test C-Score
print "C-Score robin = %f, philipe = %f, ad = %f and leendert = %f" % (robin.c_score, philipe.c_score, ad.c_score,
                                                                       leendert.c_score)
# Print all blocks
test_blockchain.print_all_blocks()

print test_blockchain.papers["Academic blockchain system"].confirmed_by
