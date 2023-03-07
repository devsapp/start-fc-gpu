create database mall_db;
use mall_db;
CREATE TABLE product_comment_tbl (
    id INT(4) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user_id INT(4) NOT NULL,
    product_id INT(4) NOT NULL,
    comment_timestamp TIMESTAMP,
    comment_content TEXT NOT NULL,
    comment_rating_positive INT(4) DEFAULT 0,
    comment_rating_neutral INT(4) DEFAULT 0,
    comment_rating_negative INT(4) DEFAULT 0
);

insert into product_comment_tbl(user_id, product_id, comment_timestamp, comment_content) VALUES(10010, 50000201, "1980-01-01 00:00:01", "The newbie must, anyway, I followed the recipe above, did the cake and cookies, the cake although not 100% successful, a little shrinkage and cracking, but the taste is good, fluffy ~ this book is still good, no powdered sugar at home, told you to use the cooking machine to break the sugar on it, do not deliberately buy more than one material ~ perfect for newcomers.");
insert into product_comment_tbl(user_id, product_id, comment_timestamp, comment_content) VALUES(10011, 50000201, "1980-01-01 00:00:01", "Just received, 2 days I dizzy, the fastest general courier to our here to 3 days, praise a!   The packaging table is simple, the instructions can not read. The bottle is translucent.   I asked the official, said excellence is also their partner, authentic peace of mind.");
insert into product_comment_tbl(user_id, product_id, comment_timestamp, comment_content) VALUES(10012, 50000201, "1980-01-01 00:00:01", "It is a very good book, but this book does not give away any vouchers. It does not reflect the characteristics of the previous genuine books sent to the site learning vouchers.");
insert into product_comment_tbl(user_id, product_id, comment_timestamp, comment_content) VALUES(10013, 50000201, "1980-01-01 00:00:01", "The content of this book is very good, is not the CD sent. This time, I reordered a set, expecting the CDs sent to work");
insert into product_comment_tbl(user_id, product_id, comment_timestamp, comment_content) VALUES(10014, 50000201, "1980-01-01 00:00:01", "A very practical book, very much like!");
insert into product_comment_tbl(user_id, product_id, comment_timestamp, comment_content) VALUES(10015, 50000201, "1980-01-01 00:00:01", "The book itself is not a problem, but the packaging of the goods is really not complimentary. I do not know for what reason, the previous carton packaging is now replaced by a plastic bag, shot two hardcover books to hand actually rolled the edge, super depressed. In this way to reduce costs, is not enough. Save only three dates, the loss is the trust of the people.");
insert into product_comment_tbl(user_id, product_id, comment_timestamp, comment_content) VALUES(10016, 50000201, "1980-01-01 00:00:01", "Packaging is very good, the content is also good");
insert into product_comment_tbl(user_id, product_id, comment_timestamp, comment_content) VALUES(10017, 50000201, "1980-01-01 00:00:01", "Cheap best, hope to be cheaper soon!");

insert into product_comment_tbl(user_id, product_id, comment_timestamp, comment_content) VALUES(10020, 50000301, "1980-01-01 00:00:01", "I thought the content of this book has depth, I did not expect to open and look at a page of a few words, say things are also very shallow, sorry for the price, the quality and quantity of content with 5 dollars journal almost");
insert into product_comment_tbl(user_id, product_id, comment_timestamp, comment_content) VALUES(10021, 50000301, "1980-01-01 00:00:01", "Outsiders see the fun, insiders see the doorway.  No clinical experience of the family members every day everywhere talking nonsense.");
insert into product_comment_tbl(user_id, product_id, comment_timestamp, comment_content) VALUES(10022, 50000301, "1980-01-01 00:00:01", "The first CD simply can not be put, the second content has not yet begun to learn, the book also has problems, the piano teacher said that there is a problem with the layout, because the number of fingering should not be written into the five lines.");
insert into product_comment_tbl(user_id, product_id, comment_timestamp, comment_content) VALUES(10023, 50000301, "1980-01-01 00:00:01", "The main thing is that this version does not work, it costs me money. In fact, other versions, I like this book.");
insert into product_comment_tbl(user_id, product_id, comment_timestamp, comment_content) VALUES(10024, 50000301, "1980-01-01 00:00:01", "Originally I wanted to rate three stars, look above so many TO, but also this cover design is very good? Turned a few sections, the general bar, from the content of the value of three stars. Maybe the author is a design bull, but the writing is not good to say");
insert into product_comment_tbl(user_id, product_id, comment_timestamp, comment_content) VALUES(10025, 50000301, "1980-01-01 00:00:01", "Dont buy, garbage than my laptop built-in pixel is worse than the 800w");
insert into product_comment_tbl(user_id, product_id, comment_timestamp, comment_content) VALUES(10026, 50000301, "1980-01-01 00:00:01", "The paper inside is damaged, the paper quality is very poor and yellowish, the cover is still damaged, a little disappointed.");


