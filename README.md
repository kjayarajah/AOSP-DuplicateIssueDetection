# AOSP-DuplicateIssueDetection

/*
*The crawlers are distributed for research purpose, but
*WITHOUT ANY WARRANTY; without even the implied warranty of
*MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
*We appreciate you citing our work if you use any part of the code or data:
*Kasthuri Jayarajah, Meeralakshmi Radhakrishnan, Camellia Zakaria, Duplicate Issue Detection for the Android Open Source
*Project, The 5th International Workshop on Software Mining co-located with ASE 2016 
*Feel free to contact the following people if you find any
*problems in the scraper. 
*kasthurij.2014@smu.edu.sg, meerakshm.2014@smu.edu.sg, ncamelliaz.2014@smu.edu.sg 
*/

Introduction:

The Android Open Source Project has seen tremendous traction
over the past decade, and as such, the bug repository is growing
in scale. With this growth, the effort required for project members
to triage incoming new reports to identify whether it is a duplicate
issue that has already been addressed, or receiving attention,
is also on the rise. Thsi project provides a set of crawlers to scrape issues and corresponding comments from
the Android issue tracker, and to scrape the Android API documentation for its packages and classes information.
In the orginal paper, we use a mix of IR techniques for detecting and validating issue redundancy in the Android Issue Tracker.

Code:

1. The Python files crawler.py, crawler_android.py and crawler_package.py crawl for data/metadata of the issues on the issue tracker, Android API documentation's packages and Android API Documentation's classes, respectively.
2. In the current form, crawler.py takes two issue IDs as inputs and write metadata to a CSV file (issues.csv) and stores the issues and related comments separately.
3. The format of the issues.csv file:
Issue id, Issue heading, status, Owner id (if exists) – to whom the issue is assigned to),<ignore>,Type of bug/issue,User who logged the issue,Time the issue was logged,Concatenated list of times of comments,Concatenated list of IDs of comments


Sample:

Sample data (roughly 3500 issues) and 47,000 comments are provided in the "data" folder.

