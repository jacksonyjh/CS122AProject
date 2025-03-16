# lowk might hard code these create table queries (source: homework 2 solutions)
create_table_query_map = dict()
create_table_query_map["users"] = """CREATE TABLE users (
    uid INT,
    email TEXT NOT NULL,
    joined_date DATE NOT NULL,
    nickname TEXT NOT NULL,
    street TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    genres TEXT,
    PRIMARY KEY (uid)
);
"""

create_table_query_map["producers"] = """CREATE TABLE producers (
    uid INT,
    bio TEXT,
    company TEXT,
    PRIMARY KEY (uid),
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE
);
"""


create_table_query_map["viewers"] = """CREATE TABLE viewers (
    uid INT,
    subscription ENUM('free', 'monthly', 'yearly'),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    PRIMARY KEY (uid),
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE
);
"""
create_table_query_map["releases"] = """CREATE TABLE releases (
    rid INT,
    producer_uid INT NOT NULL,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    release_date DATE NOT NULL,
    PRIMARY KEY (rid),
    FOREIGN KEY (producer_uid) REFERENCES producers(uid) ON DELETE CASCADE
);
"""

create_table_query_map["movies"] = """CREATE TABLE movies (
    rid INT,
    website_url TEXT,
    PRIMARY KEY (rid),
    FOREIGN KEY (rid) REFERENCES releases(rid) ON DELETE CASCADE
);
"""

create_table_query_map["series"] = """CREATE TABLE series (
    rid INT,
    introduction TEXT,
    PRIMARY KEY (rid),
    FOREIGN KEY (rid) REFERENCES releases(rid) ON DELETE CASCADE
);
"""
create_table_query_map["videos"] = """CREATE TABLE videos (
    rid INT,
    ep_num INT NOT NULL,
    title TEXT NOT NULL,
    length INT NOT NULL,
    PRIMARY KEY (rid, ep_num),
    FOREIGN KEY (rid) REFERENCES releases(rid) ON DELETE CASCADE
);
"""
create_table_query_map["sessions"] = """CREATE TABLE sessions (
    sid INT,
    uid INT NOT NULL,
    rid INT NOT NULL,
    ep_num INT NOT NULL,
    initiate_at DATETIME NOT NULL,
    leave_at DATETIME NOT NULL,
    quality ENUM('480p', '720p', '1080p'),
    device ENUM('mobile', 'desktop'),
    PRIMARY KEY (sid),
    FOREIGN KEY (uid) REFERENCES viewers(uid) ON DELETE CASCADE,
    FOREIGN KEY (rid, ep_num) REFERENCES videos(rid, ep_num) ON DELETE CASCADE
);
"""

create_table_query_map["reviews"] = """CREATE TABLE reviews (
    rvid INT,
    uid INT NOT NULL,
    rid INT NOT NULL,
    rating DECIMAL(2, 1) NOT NULL CHECK (rating BETWEEN 0 AND 5),
    body TEXT,
    posted_at DATETIME NOT NULL,
    PRIMARY KEY (rvid),
    FOREIGN KEY (uid) REFERENCES viewers(uid) ON DELETE CASCADE,
    FOREIGN KEY (rid) REFERENCES releases(rid) ON DELETE CASCADE
);
"""
