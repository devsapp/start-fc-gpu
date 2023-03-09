import tablestore
import os

ots_endpoint = os.environ['OTS_ENDPOINT']
ots_ak_id = os.environ['OTS_AK_ID']
ots_ak_secret = os.environ['OTS_AK_SECRET']
ots_instance = os.environ['OTS_INSTANCE']
ots_table_products = "mall_products_mock"
ots_table_comments = "mall_comments_mock"

# purpose: 
#      init ots client
ots_client = tablestore.OTSClient(ots_endpoint, ots_ak_id, ots_ak_secret, ots_instance, logger_name = 'table_store.log')

# purpose: 
#      create table-1 mall_products_mock: store product meta
try:
    ots_client.delete_table(ots_table_products)
except Exception:
    print("the ots_table_products is not exist.")

try:
    schema_of_primary_key = [('product_id', 'INTEGER')]
    table_meta = tablestore.TableMeta(ots_table_products, schema_of_primary_key)
    table_options = tablestore.TableOptions(-1, 1, 86400)
    reserved_throughput = tablestore.ReservedThroughput(tablestore.CapacityUnit(0, 0))
    ots_client.create_table(table_meta, table_options, reserved_throughput)
    print("create ots_table_products succeeded")
except Exception:
    print("create ots_table_products failed.")

# purpose:    
#     create table-2 mall_comments_mock: store user comments
try:
    ots_client.delete_table(ots_table_comments)
except Exception:
    print("the ots_table_comments is not exist.")

try:
    schema_of_primary_key = [('product_id', 'INTEGER'), ('user_id', 'INTEGER')]
    table_meta = tablestore.TableMeta(ots_table_comments, schema_of_primary_key)
    table_options = tablestore.TableOptions(-1, 1, 86400)
    reserved_throughput = tablestore.ReservedThroughput(tablestore.CapacityUnit(0, 0))
    ots_client.create_table(table_meta, table_options, reserved_throughput)
    print("create ots_table_comments succeeded")
except Exception:
    print("create ots_table_comments failed.")

# purpose:
#     prepare data for mall_comments_mock: product_id, user_id, comment_content
data = [
    # 500001
    [500001, 1001, "The newbie must, anyway, I followed the recipe above, did the cake and cookies, the cake although not 100% successful, a little shrinkage and cracking, but the taste is good, fluffy ~ this book is still good, no powdered sugar at home, told you to use the cooking machine to break the sugar on it, do not deliberately buy more than one material ~ perfect for newcomers."],
    [500001, 1002, "Just received, 2 days I dizzy, the fastest general courier to our here to 3 days, praise a!   The packaging table is simple, the instructions can not read. The bottle is translucent.   I asked the official, said excellence is also their partner, authentic peace of mind."],
    [500001, 1003, "It is a very good book, but this book does not give away any vouchers. It does not reflect the characteristics of the previous genuine books sent to the site learning vouchers."],
    [500001, 1004, "The content of this book is very good, is not the CD sent. This time, I reordered a set, expecting the CDs sent to work"],
    [500001, 1005, "A very practical book, very much like!"],
    [500001, 1006, "The book itself is not a problem, but the packaging of the goods is really not complimentary. I do not know for what reason, the previous carton packaging is now replaced by a plastic bag, shot two hardcover books to hand actually rolled the edge, super depressed. In this way to reduce costs, is not enough. Save only three dates, the loss is the trust of the people."],
    [500001, 1007, "Packaging is very good, the content is also good"],
    [500001, 1008, "Cheap best, hope to be cheaper soon!"],
    [500001, 1009, "I thought the content of this book has depth, I did not expect to open and look at a page of a few words, say things are also very shallow, sorry for the price, the quality and quantity of content with 5 dollars journal almost"],
    [500001, 1010, "Outsiders see the fun, insiders see the doorway.  No clinical experience of the family members every day everywhere talking nonsense."],

    # 500002
    [500002, 1011, "The first CD simply can not be put, the second content has not yet begun to learn, the book also has problems, the piano teacher said that there is a problem with the layout, because the number of fingering should not be written into the five lines."],
    [500002, 1012, "The main thing is that this version does not work, it costs me money. In fact, other versions, I like this book."],
    [500002, 1013, "Originally I wanted to rate three stars, look above so many TO, but also this cover design is very good? Turned a few sections, the general bar, from the content of the value of three stars. Maybe the author is a design bull, but the writing is not good to say"],
    [500002, 1014, "Dont buy, garbage than my laptop built-in pixel is worse than the 800w"],
    [500002, 1015, "The paper inside is damaged, the paper quality is very poor and yellowish, the cover is still damaged, a little disappointed."],
    [500002, 1016, "When you receive the goods, the packaging is very complete and not damaged, and the content of the book is very comprehensive, very much like"],
    [500002, 1017, "OK, the quality of the book is really good can not bear to write on it almost is the content feels a little less"],
    [500002, 1018, "A very good book, many things actually have their own personal experience and experience, for the sales staff to do a lot of help."],
    [500002, 1019, "Have not seen the content inside, but the previous buy New Oriental feel good, I guess this is also good"],
    [500002, 1020, "This book is about the wild flowers of Great Britain and Northwest Europe. It is not recommended if you want to use it as a reference for identifying European garden flowers.   The illustrations and binding are impeccable."],

    # 500003
    [500003, 1021, "Three words, it sucks."],
    [500003, 1022, "Bought three books on breakfast at one time, this book is the most homely, but also the baby's favorite, according to do a lot more, very good, recommended to buy"],
    [500003, 1023, "The story is very heartwarming, my daughter is 2 weeks old, very much like I read to her, read many, many times, although I do not know if she can understand"],
    [500003, 1024, "The content is not good. But the paper quality is not good. A touch and try out. It seems to be a pirated version"],
    [500003, 1025, "Bought for my little niece, the cover of the book she liked. When she got it in her hand, she started reading it inside and really enjoyed reading it. She is in the third grade."],
    [500003, 1026, "I bought his book because I was dizzy."],
    [500003, 1027, "Hope to be cheaper, the price is not competitive"],
    [500003, 1028, "This book is really good, very suitable for me!"],
    [500003, 1029, "Doesn't match my Samsung i929"],
    [500003, 1030, "The glass is quite thick, no bubbles or anything found, good. Special thanks to the courier, and fast attitude and good. Always like shopping at Amazon"],

    # 500004
    [500004, 1031, "Good very much like the content packaging are very good"],
    [500004, 1032, "The speed of delivery of the excellent really must praise a, yesterday placed two orders, this morning arrived, the home of the help received a single, this book is received in the company, super like, full color pages, although the introduction of the kind of not a lot, but suitable for just beginning to learn. Like"],
    [500004, 1033, "Great book! The translation is very accurate and informative, and it feels like a domestic Chinese translation that can't be beat!"],
    [500004, 1034, "For the price, that's it"],
    [500004, 1035, "The youngest grandson is about to be born, for his sister to see, I hope it will help."],
    [500004, 1036, "Very good book, no wonder it is popular around the world. The book is better than the movie, there are many details that are not shown in the movie. Worth buying"],
    [500004, 1037, "I thought it was a restoration of the real history, but the result was"],
    [500004, 1038, "The brew out of Nestle is fragrant, and the brew out of Nestle's original flavor is a little sweeter, but it suits my taste, very good."],
    [500004, 1039, "After flipping through the book is indeed depending on how you look at the smart people find a way not read with care just read a meaningless reading like marketing"],
    [500004, 1040, "Quite can inspire people to struggle a book, especially for students to see, very good book"],

    # 500005
    [500005, 1041, "Good quality, should be worth the money."],
    [500005, 1042, "Nice content! Love the style of hand-drawn illustrations."],
    [500005, 1043, "Size is suitable, feel the quality can be"],
    [500005, 1044, "The merchandise is good, the handwriting is clear and looks like the original!"],
    [500005, 1045, "Satisfied, there is no problem, depending on how long it can be used"],
    [500005, 1046, "The content is still good, very rich"],
    [500005, 1047, "This book is too thick, nothing important, regret"],
    [500005, 1048, "It's a very good book, but the price is expensive for the book itself."],
    [500005, 1049, "It is the best work of the author, which is true and vivid to life."],
    [500005, 1050, "The content is very good beauty to cry winging! But the quality is generally la ~ and the calendar card although on the small side but still very good-looking it! Super value oh!!! Especially recommended!"],

    # 500006
    [500006, 1051, "Bought for Dad, he personally think it's okay. The only dissatisfaction is the delivery process, 2 hours to the distance, but it took 7 days"],
    [500006, 1052, "I bought all the books in this set and both my son and I have read them. It is the best way to promote a boring history book in the form of comics. I have always lamented that Korean comics cover all aspects and our comics are too backward, but after reading this set of books, I think I have changed my opinion. I hope that there will be better works in the near future, and that the publicity of the works will be strengthened, and that the good works will be publicized more."],
    [500006, 1053, "This book is a collection of many of Huine's masterpieces and is worth a closer look if you want to understand her writing talent and some of her inner thoughts."],
    [500006, 1054, "I feel that the author did not have the first volume of heart, it is really to see the face of the Beijing Opera to buy."],
    [500006, 1055, "Flat head to listen to good, but the bell-shaped earpiece can not hear the fetal heartbeat, the other nothing, I think the overall good, very good, the family medicine necessary."],
    [500006, 1056, "Color and style as shown in the picture. The fabric is soft, wear feel very comfortable, I am slightly fat, so the effect of linen bean top loose wood. 163, 117 pounds, chose L, for reference"],
    [500006, 1057, "I may not have the goods, I buy this book, but I was sent another book of structural design principles, the same replacement, alas!"],
    [500006, 1058, "Professional books, study advertising can look at"],
    [500006, 1059, "I love it, and the quality of the product itself is good!"],
    [500006, 1060, "The first half is not bad, the back is not too much like. Quality is not bad"],

    # 500007
    [500007, 1061, "The book is very good, worth the price, unlike other books so dumb, but very difficult to read, to read slowly."],
    [500007, 1062, "Such a good recording, such a high level of production, such a low price, do not buy will regret"],
    [500007, 1063, "Too fine, very soft, the quality is not very good, the only advantage is to effectively prevent wet clothes from slipping"],
    [500007, 1064, "One of the feet how to install a little bit of slanting it, not much money too lazy to replace it."],
    [500007, 1065, "General, now the battery quality is not so ah? Almost use a three-day bar 。。。。。 Where are all the good quality batteries."],
    [500007, 1066, "If you can find it online, it's better not to spend so much money."],
    [500007, 1067, "Easy to understand, less content, packaging is not good, the book is damaged"],
    [500007, 1068, "The dictionary is the same size as the Xinhua Dictionary, and the dictionary is the same thickness, it is very beneficial to read Yadasmi's works."],
    [500007, 1069, "Very general, it is completely stacked"],
    [500007, 1070, "The content is rich, the viewpoint is excellent, and it is good to read after dinner. Book quality is average"],

    # 500008
    [500008, 1071, "The design and printing of the book are very beautiful, the content has not finished reading, in general, very thorough, detailed"],
    [500008, 1072, "The book is very light, pocket book. I like it very much. But there are a few pages printing quality is a bit problematic, there are ghosting. Fortunately, just a few pages. The main thing is cheap ah."],
    [500008, 1073, "The quality can be, more feel, the audio is okay, but some of the audio in the middle of the end is not the end of the words."],
    [500008, 1074, "The top and bottom are frosted metal, but the surrounding plastic, thicker than expected"],
    [500008, 1075, "It is disappointing that some of the verses are not explained."],
    [500008, 1076, "The quality is good, but the idiom is not complete, some basic idioms will not be found."],
    [500008, 1077, "Very cute book, postcards are also very cute, do not want to send, paper, printing is also great."],
    [500008, 1078, "If you only want to see the contents of the map, it is also done in detail. If you want to see a detailed introduction to the city, you should look for a book. In the book, each county is only about two or three important cities, but as a map is still relatively detailed."],
    [500008, 1079, "Affordable machine, very suitable for men who live a simple life"],
    [500008, 1080, "worth buying, the content is good, children like, is the video explanation is just a little, need to pay"],

    # 500009
    [500009, 1081, "The focus is not on preconception!"],
    [500009, 1082, "I do not know whether the logistics in the middle of the tampering, or the original excellent / Amazon out of the dictionary is so bad, or the original dictionary is also divided into three, six, nine, etc.. "],
    [500009, 1083, "Brewing coffee and tea are good, the filter is dense stainless steel. Coffee beans into particles are not very fine powder is not run out of the filter. Price is not cheap."],
    [500009, 1084, "Did not see the production date, but should be authentic This taste is good, grandma likes it very much"],
    [500009, 1085, "Keeping up with current events and learning"],
    [500009, 1086, "The book is good beyond my expectation, really good, good quality, good content, which can find what I want, comments are also there, notes are also there, good book ah."],
    [500009, 1087, "To support, such books can be recommended."],
    [500009, 1088, "General fiction reading, leisure time can read"],
    [500009, 1089, "Do not like, propaganda than the actual content!"],
    [500009, 1090, "This book is great for both learning and reading. My kids were excited to read a part of it and learn some historical allusions. I've been buying the bound version and using it for my own reading and study, it's very useful."],

    # 500010
    [500010, 1091, "The overall security performance is okay, but unfortunately the fingerprint recognition is sometimes not so in place! To identify 3 to 4 times!"],
    [500010, 1092, "The book arrived after a period of time to read, the content is very attractive, even after the translation of the text is not so difficult to read difficult to understand."],
    [500010, 1093, "The book has not yet seen, logistics is very powerful, the book is smaller than expected size I thought it was a magazine book so big turned out to be half of the magazine book, the content to see and then comment!"],
    [500010, 1094, "The first half is a brief introduction to the cheese making process and various classifications, and the second half is an index and introduction to cheeses from various regions of the world, but the translation is sometimes a bit forced, but it is quite satisfying to buy."],
    [500010, 1095, "Newly bought computer, for people who do not know anything press the boot how to enter the settings do not know, even a mouse and bag are not so expensive it is better to go to the physical store to buy, but also film"],
    [500010, 1096, "It is very comfortable to wear, not because of a long time to wear the meat pain... The sound is very clear, with good full range performance and semi-open sound reproduction."],
    [500010, 1097, "I've been paying attention to Mr. Fan's book and microblogging, buy this book has a healthy recipe, after the good to do to the family to eat ~ ~ good, the activity full 200 minus 55, but also package delivery, buy 7 big book only 16 * too good deal."],
    [500010, 1098, "This book is not a master's work, but it is a notebook compiled by his students. It is in both vernacular and Mandarin, and I can understand it. I had read the original work of the master, but I had a hard time reading it because of my limited level."],
    [500010, 1099, "The whole book uses countless examples to prove a habitual pattern, interested in going to the bookstore to read the last few pages on the line, saving time, effort and money."],
    [500010, 1100, "It was sent over very quickly, and took less than 11 hours. Outside the wind is very large did not check the goods, the result after opening the book to see a large crease behind the book, not in the general sense of the crease. The book's cover is hard cardboard, the whole back was rolled up and crushed, very bad! The warehouse is not even look at the time of delivery! If you do not want to start reading the book immediately, you will definitely return it!"]
]

# purpose: 
#     insert data
for item in data:
    primary_key = [('product_id', item[0]), ('user_id', item[1])]
    attribute_columns = [('comment_content', item[2]), ('comment_rating_positive', 0), ('comment_rating_neutral', 0), ('comment_rating_negative', 0)]
    row = tablestore.Row(primary_key, attribute_columns)
    try :
        consumed, return_row = ots_client.put_row(ots_table_comments, row)
        print ('[%d %d] put row succeed, consume %s write cu.' % (item[0], item[1], consumed.write))
    except tablestore.OTSClientError as e:
        print("[%d %d] put row failed, http_status:%d, error_message:%s" % (item[0], item[1], e.get_http_status(), e.get_error_message()))
    except tablestore.OTSServiceError as e:
        print("[%d %d] put row failed, http_status:%d, error_code:%s, error_message:%s, request_id:%s" % (item[0], item[1], e.get_http_status(), e.get_error_code(), e.get_error_message(), e.get_request_id()))
