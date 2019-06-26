data d2006 ;
infile' C:\Users\user\Desktop\data\data2006.csv' delimiter=','  firstobs=3 Missover ;
input code year amb risk;


data d2007 ;
infile' C:\Users\user\Desktop\data\data2007.csv' delimiter=','  firstobs=3 Missover ;
input code year amb risk;


data d2008 ;
infile' C:\Users\user\Desktop\data\data2008.csv' delimiter=','  firstobs=3 Missover ;
input code year amb risk;


data d2009 ;
infile' C:\Users\user\Desktop\data\data2009.csv' delimiter=','  firstobs=3 Missover ;
input code year amb risk;


data d2010 ;
infile' C:\Users\user\Desktop\data\data2010.csv' delimiter=','  firstobs=3 Missover ;
input code year amb risk;

data dataall ;
merge d2006 d2007 d2008 d2009 d2010;
by code year;
proc print;
run;


data reg2;
infile' C:\Users\user\Desktop\data\reg2.csv' delimiter=','  firstobs=3 Missover ;
input code name$ year cash asset derivp derivn deriv ;
proc sort reg2;
by code year;
proc print;
run;


data reg1;
infile' C:\Users\user\Desktop\data\reg.csv' delimiter=','  firstobs=3 Missover ;
input code name$ year dividend	ca cl asset fasset iasset oasset cf leverage rnd mv lia;
proc sort reg1;
by code year;
proc print;
run;

data all1;
merge dataall reg2;
by code ;
proc sort data=all1; by year; 
proc print; 
run;

data all2;
merge all1 reg1;
by code ;
proc sort data=all2; by year; 
proc print; 
run;

data reg;
set all2;
nwc=ca-cl;
lasset=log(asset);
capex=fasset+iasset+oasset;
casha=cash/asset;
bv=asset-lia;
mb=mv/bv;
deriva=deriv/asset;
proc print;
run;
ods rtf file='d:name.doc';
proc reg;
model casha=amb risk mb lasset cf nwc capex  leverage rnd dividend;
run;
RUN;QUIT;
ods rtf close;


