drop table if exists Festival;
create table Festival (
  id integer primary key autoincrement,
  title text not null,
  festival_date date not null,
  location text,
  price text,
  camping text,
  description text
);

drop table if exists Artist;
create table Artist (
  id integer primary key autoincrement,
  title text not null
);

drop table if exists Playing;
create table Playing (
  id integer primary key autoincrement,
  festival_id int,
  artist_id int
);