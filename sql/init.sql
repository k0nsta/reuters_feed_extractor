CREATE TABLE IF NOT EXISTS reuters(
    id serial primary key,
    "url" text not null,
    "title" text,
    "description" text,
    "content" text,
    "datetime" timestamp,
    constraint url_unique unique("url")
);
