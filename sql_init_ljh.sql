use tymt;

select * from designer;
select * from designscheme;
select * from competitivebid;
select * from decorationform;
update designer set CompanyID=3 where DesignerID=2;

insert into decorationform(ConsumerID, DcFormDESC, DcFormState, DcFormCreatetime) value (1, 'ddddd2222', 'Success', now());
insert into competitivebid value(2, 2, 'qqqwwwsssaaa', now(), 'Accept', 111)
