-- auto-generated definition
create table document
(
    id        INTEGER not null
        primary key,
    name      TEXT    not null,
    type      TEXT    not null,
    number    TEXT    not null,
    authority varchar(255),
    date      varchar(255),
    text      varchar(2047)
);


-- auto-generated definition
create table links
(
    id          INTEGER not null
        primary key,
    parent_id   INTEGER not null
        references document,
    child_id    INTEGER not null
        references document,
    start_index int,
    end_index   int
);

create index link_child_id
    on links (child_id);

create index link_parent_id
    on links (parent_id);