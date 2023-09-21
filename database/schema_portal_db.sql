CREATE TABLE
    IF NOT EXISTS Organization (
        OrganizationId INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        WebSite TEXT NOT NULL UNIQUE,
        Country TEXT,
        FederationUnity TEXT,
        ShortDescription TEXT
    );

CREATE TABLE
    IF NOT EXISTS Tab (
        TabId INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL UNIQUE
    );

CREATE TABLE
    IF NOT EXISTS Type (
        TypeId INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL UNIQUE,
        TabId INTEGER NOT NULL,
        FOREIGN KEY (TabId) REFERENCES Tab(TabId)
    );

CREATE TABLE
    IF NOT EXISTS OrganizationType (
        OrganizationId INTEGER,
        TypeId INTEGER,
        PRIMARY KEY(OrganizationId, TypeId),
        FOREIGN KEY (OrganizationId) REFERENCES Organization(OrganizationId),
        FOREIGN KEY (TypeId) REFERENCES Type(TypeId)
    );