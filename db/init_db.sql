create table document
(
    id        int auto_increment
        primary key,
    name      text          not null,
    type      text          not null,
    number    text          null,
    authority varchar(255)  null,
    date      date          null,
    text      varchar(2047) null,
    ont_id    text          null,
    constraint document_id_uindex
        unique (id)
);

create table links
(
    id          int auto_increment
        primary key,
    parent_id   int                  not null,
    child_id    int                  not null,
    start_index int                  null,
    end_index   int                  null,
    is_custom   tinyint(1) default 1 null,
    type        int                  null,
    constraint links_child_id_parent_id_uk
        unique (child_id, parent_id),
    constraint links_id_uindex
        unique (id)
);

create index link_child_id
    on links (child_id);

create index link_parent_id
    on links (parent_id);

