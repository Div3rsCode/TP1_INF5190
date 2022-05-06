create table article(
    identifiant varchar(50) PRIMARY KEY,
    titre varchar(50) NOT NULL,
    auteur varchar(50) NOT NULL,
    date_publication datetime NOT NULL,
    paragraphe varchar(200) NOT NULL
);


insert into article values("wsdf35434tgvg","bouteille", "Wulleman","1990-12-23","rien a dire ici");
insert into article values("wsdf35wre4tgvg","bougie",   "Wulleman","1995-12-30","rien a dire ici");
insert into article values("wsdf35434tgrrvg","briquet", "Wulleman","2000-12-19","rien a dire ici");
insert into article values("wsdfeaswdrtgvg","brique",   "Wulleman","2005-12-19","rien a dire ici");
insert into article values("wsdf354ghjuvg","brouette",  "Wulleman","2025-12-19","rien a dire ici");