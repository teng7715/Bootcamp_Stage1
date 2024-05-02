## Task 2: Create database and table in your MySQL server
### 👉🏽 2-1 Create a new database named website.
```sql
create database website;
```
![image](https://teng7715.github.io/Week%205/screenshot/2-1.png)


### 👉🏽 2-2 Create a new table named member, in the website database, designed as below
```sql
create table member(
    id bigint primary key auto_increment,
    name varchar(255) not null,
    username varchar(255) not null,
    password varchar(255) not null,
    follower_count int unsigned not null default 0,
    time datetime not null default current_timestamp
);
```
![image](https://teng7715.github.io/Week%205/screenshot/2-2.1.png)
![image](https://teng7715.github.io/Week%205/screenshot/2-2.2.png)

## Task 3: SQL CRUD
### 👉🏽 3-1 INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data.
```sql
insert into member (name,username,password,follower_count) values ('test','test','test',200);
insert into member (name,username,password,follower_count) values ('麥當勞唯一信仰','mydondon','mydondon',1300);
insert into member (name,username,password,follower_count) values ('肯爺爺老當益壯','KFC_stillyoung','KFC_stillyoung',800);
insert into member (name,username,password,follower_count) values ('摩斯高質感代表','mosburger_love','mosburger_love',1500);
insert into member (name,username,password,follower_count) values ('漢堡王火烤美味','onfire_king','onfire_king',500);
```
![image](https://teng7715.github.io/Week%205/screenshot/3-1.png)



### 👉🏽 3-2
### 👉🏽 3-3
### 👉🏽 3-4
### 👉🏽 3-5
### 👉🏽 3-6
### 👉🏽 3-7
### 👉🏽 3-8
