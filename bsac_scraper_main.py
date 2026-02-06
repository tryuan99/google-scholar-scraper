from pathlib import Path

import pandas as pd
from absl import app, flags, logging
from scholarly import scholarly

FLAGS = flags.FLAGS

# Map from BSAC co-director to Google Scholar ID.
# See https://bsac.berkeley.edu/about-bsac/people/faculty-co-directors for the complete list.
GOOGLE_SCHOLAR_IDS = {
    "chien": "Yxr6-_IAAAAJ",
    "javey": "1gqyKqcAAAAJ",
    "liepmann": "JEF1Yk4AAAAJ",
    "lin": "FTe6HDoAAAAJ",
    "maboudian": "Qogwc7QAAAAJ",
    "pister": "mnAk4HIAAAAJ",
    "sipahigil": "0X-KuJAAAAAJ",
    "wu": "Yr2yu_sAAAAJ",
    "zheng": "Wi25oKoAAAAJ",
}


def scrape_publication_data(
    id: str,
    output_file: str,
    year: int = None,
) -> None:
    """Scrapes the publication data for the given Google Scholar ID.

    Args:
        id: Google Scholar ID.
        output_file: Output CSV file.
        year: Publication year.
    """
    # Search for the author.
    author = scholarly.search_author_id(id)
    logging.info("Found author: %s.", author.get("name"))

    # Fetch the publications.
    author = scholarly.fill(author, sections=["publications"])
    publications = author.get("publications", [])

    # Fetch the details of each publication.
    all_publications = []
    for publication in publications:
        publication_year = int(publication.get("bib", {}).get("pub_year", -1))
        if year is None or publication_year == year:
            full_publication = scholarly.fill(publication)
            bibliography = full_publication.get("bib", {})
            entry = {
                "Title": bibliography.get("title"),
                "Author": bibliography.get("author"),
                "Year": int(bibliography.get("pub_year", -1)),
                "Citation": bibliography.get("citation"),
                "Conference": bibliography.get("conference"),
                "Journal": bibliography.get("journal"),
            }
            all_publications.append(entry)
    logging.info("Found %d publication(s).", len(all_publications))

    # Save the publication to the output CSV file.
    df = pd.DataFrame(all_publications)
    df.to_csv(output_file, index=False)


def main(argv):
    assert len(argv) == 1, argv

    output_dir = Path(FLAGS.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for author in FLAGS.author:
        id = GOOGLE_SCHOLAR_IDS.get(author.lower(), None)
        if id is None:
            logging.error("Failed to find author ID for %s.", author)
            continue
        logging.info("Scraping publications for %s.", author)
        scrape_publication_data(id, f"{output_dir}/{author.lower()}.csv",
                                FLAGS.year)


if __name__ == "__main__":
    flags.DEFINE_multi_enum("author", None, GOOGLE_SCHOLAR_IDS.keys(),
                            "BSAC co-director.")
    flags.DEFINE_integer("year", None, "Publication year.")
    flags.DEFINE_string("output_dir", None, "Output directory.")
    flags.mark_flags_as_required(["author", "output_dir"])

    app.run(main)
