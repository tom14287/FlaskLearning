use tymt;

select * from designer;
select * from designscheme;
select * from competitivebid;
select * from decorationform;
select * from orderform;
select * from orderitem;
select CreateTime,FurnitureImage,Furniture.FurnitureID,FurniturePrice,FurnitureName,
			OrderItemNum
			from OrderForm, OrderItem, Furniture where 
			OrderForm.OrderFormID=OrderItem.OrderFormID and OrderItem.FurnitureID=
			Furniture.FurnitureID and OrderFormState='Success' and OrderForm.UserID=1 and OrderForm.OrderFormID  in (
			select OrderFormID from Comments);

update designer set CompanyID=3 where DesignerID=2;
update orderform set OrderFormState='Success' where OrderFormID = 2;
insert into decorationform(ConsumerID, DcFormDESC, DcFormState, DcFormCreatetime) value (1, 'ddddd2222', 'Success', now());
insert into competitivebid value(2, 2, 'qqqwwwsssaaa', now(), 'Accept', 111);
insert into orderform value();