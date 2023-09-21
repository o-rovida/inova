CREATE TABLE
    IF NOT EXISTS Article (
        ArticleDoi TEXT PRIMARY KEY,
        Title TEXT NOT NULL
    );

CREATE TABLE
    IF NOT EXISTS Video (
        EpisodeNumber INTEGER PRIMARY KEY AUTOINCREMENT,
        ArticleDoi TEXT NOT NULL,
        Title TEXT NOT NULL,
        URL TEXT NOT NULL,
        PublishedDate TEXT NOT NULL,
        FOREIGN KEY (ArticleDoi) REFERENCES Article(ArticleDoi)
    );

CREATE TABLE
    IF NOT EXISTS KeyWord (
        KeyWordId INTEGER PRIMARY KEY AUTOINCREMENT,
        Word TEXT NOT NULL UNIQUE
    );

CREATE TABLE
    IF NOT EXISTS videoKeyWord (
        EpisodeNumber INTEGER,
        KeyWordId INTEGER,
        PRIMARY KEY(EpisodeNumber, KeyWordId),
        FOREIGN KEY (EpisodeNumber) REFERENCES Video(EpisodeNumber),
        FOREIGN KEY (KeyWordId) REFERENCES KeyWord(KeyWordId)
    );