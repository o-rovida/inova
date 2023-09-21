CREATE TABLE
    IF NOT EXISTS Article (
        ArticleDoi TEXT PRIMARY KEY,
        Title TEXT NOT NULL
    );

CREATE TABLE
    IF NOT EXISTS Video (
        EpisodeNumber INTEGER PRIMARY KEY AUTOINCREMENT,
        ArticleDoi TEXT NOT NULL,
        FOREIGN KEY (ArticleDoi) REFERENCES Article(ArticleDoi),
        Title TEXT NOT NULL,
        URL TEXT NOT NULL,
        PublishedDate DATE NOT NULL
    );

CREATE TABLE
    IF NOT EXISTS KeyWord (
        KeyWordId INTEGER AUTOINCREMENT PRIMARY KEY,
        Word TEXT NOT NULL UNIQUE
    );

CREATE TABLE
    IF NOT EXISTS videoKeyWord (
        EpisodeNumber INTEGER NOT NULL,
        KeyWordId INTEGER NOT NULL,
        PRIMARY KEY(EpisodeNumber, KeyWordId),
        FOREIGN KEY (EpisodeNumber) REFERENCES Video(EpisodeNumber),
        FOREIGN KEY (KeyWordId) REFERENCES KeyWord(KeyWordId)
    );