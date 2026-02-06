# Google Scholar Publication Scraper

### Setup

#### Requirements

To run the scraper, ensure that you have Python 3 installed on your system and that you have the following libraries in your current environment:
* `absl-py`
* `pandas`
* `scholarly`

### Scraping BSAC Publications

To scrape the publications for one or more BSAC faculty co-directors, run the `bsac_scraper_main.py` script:

```bash
python3 bsac_scraper_main.py \
    --author chien \
    --author pister \
    --output_dir path/to/output/directory \
    --year 2026
```

The full list of BSAC faculty co-directors can be found here: https://bsac.berkeley.edu/about-bsac/people/faculty-co-directors.

#### Flags

The `bsac_scraper_main.py` scripts supports the following commandline flags:
* `--author`: BSAC faculty co-director for which to scrape the publications. Can be specified multiple times.
* `--output_dir`: Output directory in which the output CSV files are stored.
* `--year` (optional): Publication year. If not specified, all publications are scraped.

#### Output

The `bsac_scraper_main.py` outputs one CSV file for each author with the following columns: `Title`, `Author`, `Year`, `Citation`, `Conference`, and `Journal`.
