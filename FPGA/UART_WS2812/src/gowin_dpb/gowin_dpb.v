//Copyright (C)2014-2024 Gowin Semiconductor Corporation.
//All rights reserved.
//File Title: IP file
//Tool Version: V1.9.9.03 (64-bit)
//Part Number: GW1NZ-LV1QN48C6/I5
//Device: GW1NZ-1
//Created Time: Thu Dec 26 01:24:30 2024

module Gowin_DPB (douta, doutb, clka, ocea, cea, reseta, wrea, clkb, oceb, ceb, resetb, wreb, ada, dina, adb, dinb);

output [15:0] douta;
output [15:0] doutb;
input clka;
input ocea;
input cea;
input reseta;
input wrea;
input clkb;
input oceb;
input ceb;
input resetb;
input wreb;
input [11:0] ada;
input [15:0] dina;
input [11:0] adb;
input [15:0] dinb;

wire [15:0] dpb_inst_0_douta;
wire [15:0] dpb_inst_0_doutb;
wire [15:0] dpb_inst_1_douta;
wire [15:0] dpb_inst_1_doutb;
wire [15:0] dpb_inst_2_douta;
wire [15:0] dpb_inst_2_doutb;
wire [15:0] dpb_inst_3_douta;
wire [15:0] dpb_inst_3_doutb;
wire dff_q_0;
wire dff_q_1;
wire dff_q_2;
wire dff_q_3;
wire mux_o_0;
wire mux_o_1;
wire mux_o_3;
wire mux_o_4;
wire mux_o_6;
wire mux_o_7;
wire mux_o_9;
wire mux_o_10;
wire mux_o_12;
wire mux_o_13;
wire mux_o_15;
wire mux_o_16;
wire mux_o_18;
wire mux_o_19;
wire mux_o_21;
wire mux_o_22;
wire mux_o_24;
wire mux_o_25;
wire mux_o_27;
wire mux_o_28;
wire mux_o_30;
wire mux_o_31;
wire mux_o_33;
wire mux_o_34;
wire mux_o_36;
wire mux_o_37;
wire mux_o_39;
wire mux_o_40;
wire mux_o_42;
wire mux_o_43;
wire mux_o_45;
wire mux_o_46;
wire mux_o_48;
wire mux_o_49;
wire mux_o_51;
wire mux_o_52;
wire mux_o_54;
wire mux_o_55;
wire mux_o_57;
wire mux_o_58;
wire mux_o_60;
wire mux_o_61;
wire mux_o_63;
wire mux_o_64;
wire mux_o_66;
wire mux_o_67;
wire mux_o_69;
wire mux_o_70;
wire mux_o_72;
wire mux_o_73;
wire mux_o_75;
wire mux_o_76;
wire mux_o_78;
wire mux_o_79;
wire mux_o_81;
wire mux_o_82;
wire mux_o_84;
wire mux_o_85;
wire mux_o_87;
wire mux_o_88;
wire mux_o_90;
wire mux_o_91;
wire mux_o_93;
wire mux_o_94;
wire cea_w;
wire ceb_w;
wire gw_vcc;
wire gw_gnd;

assign cea_w = ~wrea & cea;
assign ceb_w = ~wreb & ceb;
assign gw_vcc = 1'b1;
assign gw_gnd = 1'b0;

DPB dpb_inst_0 (
    .DOA(dpb_inst_0_douta[15:0]),
    .DOB(dpb_inst_0_doutb[15:0]),
    .CLKA(clka),
    .OCEA(ocea),
    .CEA(cea),
    .RESETA(reseta),
    .WREA(wrea),
    .CLKB(clkb),
    .OCEB(oceb),
    .CEB(ceb),
    .RESETB(resetb),
    .WREB(wreb),
    .BLKSELA({gw_gnd,ada[11],ada[10]}),
    .BLKSELB({gw_gnd,adb[11],adb[10]}),
    .ADA({ada[9:0],gw_gnd,gw_gnd,gw_vcc,gw_vcc}),
    .DIA(dina[15:0]),
    .ADB({adb[9:0],gw_gnd,gw_gnd,gw_vcc,gw_vcc}),
    .DIB(dinb[15:0])
);

defparam dpb_inst_0.READ_MODE0 = 1'b0;
defparam dpb_inst_0.READ_MODE1 = 1'b0;
defparam dpb_inst_0.WRITE_MODE0 = 2'b00;
defparam dpb_inst_0.WRITE_MODE1 = 2'b00;
defparam dpb_inst_0.BIT_WIDTH_0 = 16;
defparam dpb_inst_0.BIT_WIDTH_1 = 16;
defparam dpb_inst_0.BLK_SEL_0 = 3'b000;
defparam dpb_inst_0.BLK_SEL_1 = 3'b000;
defparam dpb_inst_0.RESET_MODE = "SYNC";

DPB dpb_inst_1 (
    .DOA(dpb_inst_1_douta[15:0]),
    .DOB(dpb_inst_1_doutb[15:0]),
    .CLKA(clka),
    .OCEA(ocea),
    .CEA(cea),
    .RESETA(reseta),
    .WREA(wrea),
    .CLKB(clkb),
    .OCEB(oceb),
    .CEB(ceb),
    .RESETB(resetb),
    .WREB(wreb),
    .BLKSELA({gw_gnd,ada[11],ada[10]}),
    .BLKSELB({gw_gnd,adb[11],adb[10]}),
    .ADA({ada[9:0],gw_gnd,gw_gnd,gw_vcc,gw_vcc}),
    .DIA(dina[15:0]),
    .ADB({adb[9:0],gw_gnd,gw_gnd,gw_vcc,gw_vcc}),
    .DIB(dinb[15:0])
);

defparam dpb_inst_1.READ_MODE0 = 1'b0;
defparam dpb_inst_1.READ_MODE1 = 1'b0;
defparam dpb_inst_1.WRITE_MODE0 = 2'b00;
defparam dpb_inst_1.WRITE_MODE1 = 2'b00;
defparam dpb_inst_1.BIT_WIDTH_0 = 16;
defparam dpb_inst_1.BIT_WIDTH_1 = 16;
defparam dpb_inst_1.BLK_SEL_0 = 3'b001;
defparam dpb_inst_1.BLK_SEL_1 = 3'b001;
defparam dpb_inst_1.RESET_MODE = "SYNC";

DPB dpb_inst_2 (
    .DOA(dpb_inst_2_douta[15:0]),
    .DOB(dpb_inst_2_doutb[15:0]),
    .CLKA(clka),
    .OCEA(ocea),
    .CEA(cea),
    .RESETA(reseta),
    .WREA(wrea),
    .CLKB(clkb),
    .OCEB(oceb),
    .CEB(ceb),
    .RESETB(resetb),
    .WREB(wreb),
    .BLKSELA({gw_gnd,ada[11],ada[10]}),
    .BLKSELB({gw_gnd,adb[11],adb[10]}),
    .ADA({ada[9:0],gw_gnd,gw_gnd,gw_vcc,gw_vcc}),
    .DIA(dina[15:0]),
    .ADB({adb[9:0],gw_gnd,gw_gnd,gw_vcc,gw_vcc}),
    .DIB(dinb[15:0])
);

defparam dpb_inst_2.READ_MODE0 = 1'b0;
defparam dpb_inst_2.READ_MODE1 = 1'b0;
defparam dpb_inst_2.WRITE_MODE0 = 2'b00;
defparam dpb_inst_2.WRITE_MODE1 = 2'b00;
defparam dpb_inst_2.BIT_WIDTH_0 = 16;
defparam dpb_inst_2.BIT_WIDTH_1 = 16;
defparam dpb_inst_2.BLK_SEL_0 = 3'b010;
defparam dpb_inst_2.BLK_SEL_1 = 3'b010;
defparam dpb_inst_2.RESET_MODE = "SYNC";

DPB dpb_inst_3 (
    .DOA(dpb_inst_3_douta[15:0]),
    .DOB(dpb_inst_3_doutb[15:0]),
    .CLKA(clka),
    .OCEA(ocea),
    .CEA(cea),
    .RESETA(reseta),
    .WREA(wrea),
    .CLKB(clkb),
    .OCEB(oceb),
    .CEB(ceb),
    .RESETB(resetb),
    .WREB(wreb),
    .BLKSELA({gw_gnd,ada[11],ada[10]}),
    .BLKSELB({gw_gnd,adb[11],adb[10]}),
    .ADA({ada[9:0],gw_gnd,gw_gnd,gw_vcc,gw_vcc}),
    .DIA(dina[15:0]),
    .ADB({adb[9:0],gw_gnd,gw_gnd,gw_vcc,gw_vcc}),
    .DIB(dinb[15:0])
);

defparam dpb_inst_3.READ_MODE0 = 1'b0;
defparam dpb_inst_3.READ_MODE1 = 1'b0;
defparam dpb_inst_3.WRITE_MODE0 = 2'b00;
defparam dpb_inst_3.WRITE_MODE1 = 2'b00;
defparam dpb_inst_3.BIT_WIDTH_0 = 16;
defparam dpb_inst_3.BIT_WIDTH_1 = 16;
defparam dpb_inst_3.BLK_SEL_0 = 3'b011;
defparam dpb_inst_3.BLK_SEL_1 = 3'b011;
defparam dpb_inst_3.RESET_MODE = "SYNC";

DFFE dff_inst_0 (
  .Q(dff_q_0),
  .D(ada[11]),
  .CLK(clka),
  .CE(cea_w)
);
DFFE dff_inst_1 (
  .Q(dff_q_1),
  .D(ada[10]),
  .CLK(clka),
  .CE(cea_w)
);
DFFE dff_inst_2 (
  .Q(dff_q_2),
  .D(adb[11]),
  .CLK(clkb),
  .CE(ceb_w)
);
DFFE dff_inst_3 (
  .Q(dff_q_3),
  .D(adb[10]),
  .CLK(clkb),
  .CE(ceb_w)
);
MUX2 mux_inst_0 (
  .O(mux_o_0),
  .I0(dpb_inst_0_douta[0]),
  .I1(dpb_inst_1_douta[0]),
  .S0(dff_q_1)
);
MUX2 mux_inst_1 (
  .O(mux_o_1),
  .I0(dpb_inst_2_douta[0]),
  .I1(dpb_inst_3_douta[0]),
  .S0(dff_q_1)
);
MUX2 mux_inst_2 (
  .O(douta[0]),
  .I0(mux_o_0),
  .I1(mux_o_1),
  .S0(dff_q_0)
);
MUX2 mux_inst_3 (
  .O(mux_o_3),
  .I0(dpb_inst_0_douta[1]),
  .I1(dpb_inst_1_douta[1]),
  .S0(dff_q_1)
);
MUX2 mux_inst_4 (
  .O(mux_o_4),
  .I0(dpb_inst_2_douta[1]),
  .I1(dpb_inst_3_douta[1]),
  .S0(dff_q_1)
);
MUX2 mux_inst_5 (
  .O(douta[1]),
  .I0(mux_o_3),
  .I1(mux_o_4),
  .S0(dff_q_0)
);
MUX2 mux_inst_6 (
  .O(mux_o_6),
  .I0(dpb_inst_0_douta[2]),
  .I1(dpb_inst_1_douta[2]),
  .S0(dff_q_1)
);
MUX2 mux_inst_7 (
  .O(mux_o_7),
  .I0(dpb_inst_2_douta[2]),
  .I1(dpb_inst_3_douta[2]),
  .S0(dff_q_1)
);
MUX2 mux_inst_8 (
  .O(douta[2]),
  .I0(mux_o_6),
  .I1(mux_o_7),
  .S0(dff_q_0)
);
MUX2 mux_inst_9 (
  .O(mux_o_9),
  .I0(dpb_inst_0_douta[3]),
  .I1(dpb_inst_1_douta[3]),
  .S0(dff_q_1)
);
MUX2 mux_inst_10 (
  .O(mux_o_10),
  .I0(dpb_inst_2_douta[3]),
  .I1(dpb_inst_3_douta[3]),
  .S0(dff_q_1)
);
MUX2 mux_inst_11 (
  .O(douta[3]),
  .I0(mux_o_9),
  .I1(mux_o_10),
  .S0(dff_q_0)
);
MUX2 mux_inst_12 (
  .O(mux_o_12),
  .I0(dpb_inst_0_douta[4]),
  .I1(dpb_inst_1_douta[4]),
  .S0(dff_q_1)
);
MUX2 mux_inst_13 (
  .O(mux_o_13),
  .I0(dpb_inst_2_douta[4]),
  .I1(dpb_inst_3_douta[4]),
  .S0(dff_q_1)
);
MUX2 mux_inst_14 (
  .O(douta[4]),
  .I0(mux_o_12),
  .I1(mux_o_13),
  .S0(dff_q_0)
);
MUX2 mux_inst_15 (
  .O(mux_o_15),
  .I0(dpb_inst_0_douta[5]),
  .I1(dpb_inst_1_douta[5]),
  .S0(dff_q_1)
);
MUX2 mux_inst_16 (
  .O(mux_o_16),
  .I0(dpb_inst_2_douta[5]),
  .I1(dpb_inst_3_douta[5]),
  .S0(dff_q_1)
);
MUX2 mux_inst_17 (
  .O(douta[5]),
  .I0(mux_o_15),
  .I1(mux_o_16),
  .S0(dff_q_0)
);
MUX2 mux_inst_18 (
  .O(mux_o_18),
  .I0(dpb_inst_0_douta[6]),
  .I1(dpb_inst_1_douta[6]),
  .S0(dff_q_1)
);
MUX2 mux_inst_19 (
  .O(mux_o_19),
  .I0(dpb_inst_2_douta[6]),
  .I1(dpb_inst_3_douta[6]),
  .S0(dff_q_1)
);
MUX2 mux_inst_20 (
  .O(douta[6]),
  .I0(mux_o_18),
  .I1(mux_o_19),
  .S0(dff_q_0)
);
MUX2 mux_inst_21 (
  .O(mux_o_21),
  .I0(dpb_inst_0_douta[7]),
  .I1(dpb_inst_1_douta[7]),
  .S0(dff_q_1)
);
MUX2 mux_inst_22 (
  .O(mux_o_22),
  .I0(dpb_inst_2_douta[7]),
  .I1(dpb_inst_3_douta[7]),
  .S0(dff_q_1)
);
MUX2 mux_inst_23 (
  .O(douta[7]),
  .I0(mux_o_21),
  .I1(mux_o_22),
  .S0(dff_q_0)
);
MUX2 mux_inst_24 (
  .O(mux_o_24),
  .I0(dpb_inst_0_douta[8]),
  .I1(dpb_inst_1_douta[8]),
  .S0(dff_q_1)
);
MUX2 mux_inst_25 (
  .O(mux_o_25),
  .I0(dpb_inst_2_douta[8]),
  .I1(dpb_inst_3_douta[8]),
  .S0(dff_q_1)
);
MUX2 mux_inst_26 (
  .O(douta[8]),
  .I0(mux_o_24),
  .I1(mux_o_25),
  .S0(dff_q_0)
);
MUX2 mux_inst_27 (
  .O(mux_o_27),
  .I0(dpb_inst_0_douta[9]),
  .I1(dpb_inst_1_douta[9]),
  .S0(dff_q_1)
);
MUX2 mux_inst_28 (
  .O(mux_o_28),
  .I0(dpb_inst_2_douta[9]),
  .I1(dpb_inst_3_douta[9]),
  .S0(dff_q_1)
);
MUX2 mux_inst_29 (
  .O(douta[9]),
  .I0(mux_o_27),
  .I1(mux_o_28),
  .S0(dff_q_0)
);
MUX2 mux_inst_30 (
  .O(mux_o_30),
  .I0(dpb_inst_0_douta[10]),
  .I1(dpb_inst_1_douta[10]),
  .S0(dff_q_1)
);
MUX2 mux_inst_31 (
  .O(mux_o_31),
  .I0(dpb_inst_2_douta[10]),
  .I1(dpb_inst_3_douta[10]),
  .S0(dff_q_1)
);
MUX2 mux_inst_32 (
  .O(douta[10]),
  .I0(mux_o_30),
  .I1(mux_o_31),
  .S0(dff_q_0)
);
MUX2 mux_inst_33 (
  .O(mux_o_33),
  .I0(dpb_inst_0_douta[11]),
  .I1(dpb_inst_1_douta[11]),
  .S0(dff_q_1)
);
MUX2 mux_inst_34 (
  .O(mux_o_34),
  .I0(dpb_inst_2_douta[11]),
  .I1(dpb_inst_3_douta[11]),
  .S0(dff_q_1)
);
MUX2 mux_inst_35 (
  .O(douta[11]),
  .I0(mux_o_33),
  .I1(mux_o_34),
  .S0(dff_q_0)
);
MUX2 mux_inst_36 (
  .O(mux_o_36),
  .I0(dpb_inst_0_douta[12]),
  .I1(dpb_inst_1_douta[12]),
  .S0(dff_q_1)
);
MUX2 mux_inst_37 (
  .O(mux_o_37),
  .I0(dpb_inst_2_douta[12]),
  .I1(dpb_inst_3_douta[12]),
  .S0(dff_q_1)
);
MUX2 mux_inst_38 (
  .O(douta[12]),
  .I0(mux_o_36),
  .I1(mux_o_37),
  .S0(dff_q_0)
);
MUX2 mux_inst_39 (
  .O(mux_o_39),
  .I0(dpb_inst_0_douta[13]),
  .I1(dpb_inst_1_douta[13]),
  .S0(dff_q_1)
);
MUX2 mux_inst_40 (
  .O(mux_o_40),
  .I0(dpb_inst_2_douta[13]),
  .I1(dpb_inst_3_douta[13]),
  .S0(dff_q_1)
);
MUX2 mux_inst_41 (
  .O(douta[13]),
  .I0(mux_o_39),
  .I1(mux_o_40),
  .S0(dff_q_0)
);
MUX2 mux_inst_42 (
  .O(mux_o_42),
  .I0(dpb_inst_0_douta[14]),
  .I1(dpb_inst_1_douta[14]),
  .S0(dff_q_1)
);
MUX2 mux_inst_43 (
  .O(mux_o_43),
  .I0(dpb_inst_2_douta[14]),
  .I1(dpb_inst_3_douta[14]),
  .S0(dff_q_1)
);
MUX2 mux_inst_44 (
  .O(douta[14]),
  .I0(mux_o_42),
  .I1(mux_o_43),
  .S0(dff_q_0)
);
MUX2 mux_inst_45 (
  .O(mux_o_45),
  .I0(dpb_inst_0_douta[15]),
  .I1(dpb_inst_1_douta[15]),
  .S0(dff_q_1)
);
MUX2 mux_inst_46 (
  .O(mux_o_46),
  .I0(dpb_inst_2_douta[15]),
  .I1(dpb_inst_3_douta[15]),
  .S0(dff_q_1)
);
MUX2 mux_inst_47 (
  .O(douta[15]),
  .I0(mux_o_45),
  .I1(mux_o_46),
  .S0(dff_q_0)
);
MUX2 mux_inst_48 (
  .O(mux_o_48),
  .I0(dpb_inst_0_doutb[0]),
  .I1(dpb_inst_1_doutb[0]),
  .S0(dff_q_3)
);
MUX2 mux_inst_49 (
  .O(mux_o_49),
  .I0(dpb_inst_2_doutb[0]),
  .I1(dpb_inst_3_doutb[0]),
  .S0(dff_q_3)
);
MUX2 mux_inst_50 (
  .O(doutb[0]),
  .I0(mux_o_48),
  .I1(mux_o_49),
  .S0(dff_q_2)
);
MUX2 mux_inst_51 (
  .O(mux_o_51),
  .I0(dpb_inst_0_doutb[1]),
  .I1(dpb_inst_1_doutb[1]),
  .S0(dff_q_3)
);
MUX2 mux_inst_52 (
  .O(mux_o_52),
  .I0(dpb_inst_2_doutb[1]),
  .I1(dpb_inst_3_doutb[1]),
  .S0(dff_q_3)
);
MUX2 mux_inst_53 (
  .O(doutb[1]),
  .I0(mux_o_51),
  .I1(mux_o_52),
  .S0(dff_q_2)
);
MUX2 mux_inst_54 (
  .O(mux_o_54),
  .I0(dpb_inst_0_doutb[2]),
  .I1(dpb_inst_1_doutb[2]),
  .S0(dff_q_3)
);
MUX2 mux_inst_55 (
  .O(mux_o_55),
  .I0(dpb_inst_2_doutb[2]),
  .I1(dpb_inst_3_doutb[2]),
  .S0(dff_q_3)
);
MUX2 mux_inst_56 (
  .O(doutb[2]),
  .I0(mux_o_54),
  .I1(mux_o_55),
  .S0(dff_q_2)
);
MUX2 mux_inst_57 (
  .O(mux_o_57),
  .I0(dpb_inst_0_doutb[3]),
  .I1(dpb_inst_1_doutb[3]),
  .S0(dff_q_3)
);
MUX2 mux_inst_58 (
  .O(mux_o_58),
  .I0(dpb_inst_2_doutb[3]),
  .I1(dpb_inst_3_doutb[3]),
  .S0(dff_q_3)
);
MUX2 mux_inst_59 (
  .O(doutb[3]),
  .I0(mux_o_57),
  .I1(mux_o_58),
  .S0(dff_q_2)
);
MUX2 mux_inst_60 (
  .O(mux_o_60),
  .I0(dpb_inst_0_doutb[4]),
  .I1(dpb_inst_1_doutb[4]),
  .S0(dff_q_3)
);
MUX2 mux_inst_61 (
  .O(mux_o_61),
  .I0(dpb_inst_2_doutb[4]),
  .I1(dpb_inst_3_doutb[4]),
  .S0(dff_q_3)
);
MUX2 mux_inst_62 (
  .O(doutb[4]),
  .I0(mux_o_60),
  .I1(mux_o_61),
  .S0(dff_q_2)
);
MUX2 mux_inst_63 (
  .O(mux_o_63),
  .I0(dpb_inst_0_doutb[5]),
  .I1(dpb_inst_1_doutb[5]),
  .S0(dff_q_3)
);
MUX2 mux_inst_64 (
  .O(mux_o_64),
  .I0(dpb_inst_2_doutb[5]),
  .I1(dpb_inst_3_doutb[5]),
  .S0(dff_q_3)
);
MUX2 mux_inst_65 (
  .O(doutb[5]),
  .I0(mux_o_63),
  .I1(mux_o_64),
  .S0(dff_q_2)
);
MUX2 mux_inst_66 (
  .O(mux_o_66),
  .I0(dpb_inst_0_doutb[6]),
  .I1(dpb_inst_1_doutb[6]),
  .S0(dff_q_3)
);
MUX2 mux_inst_67 (
  .O(mux_o_67),
  .I0(dpb_inst_2_doutb[6]),
  .I1(dpb_inst_3_doutb[6]),
  .S0(dff_q_3)
);
MUX2 mux_inst_68 (
  .O(doutb[6]),
  .I0(mux_o_66),
  .I1(mux_o_67),
  .S0(dff_q_2)
);
MUX2 mux_inst_69 (
  .O(mux_o_69),
  .I0(dpb_inst_0_doutb[7]),
  .I1(dpb_inst_1_doutb[7]),
  .S0(dff_q_3)
);
MUX2 mux_inst_70 (
  .O(mux_o_70),
  .I0(dpb_inst_2_doutb[7]),
  .I1(dpb_inst_3_doutb[7]),
  .S0(dff_q_3)
);
MUX2 mux_inst_71 (
  .O(doutb[7]),
  .I0(mux_o_69),
  .I1(mux_o_70),
  .S0(dff_q_2)
);
MUX2 mux_inst_72 (
  .O(mux_o_72),
  .I0(dpb_inst_0_doutb[8]),
  .I1(dpb_inst_1_doutb[8]),
  .S0(dff_q_3)
);
MUX2 mux_inst_73 (
  .O(mux_o_73),
  .I0(dpb_inst_2_doutb[8]),
  .I1(dpb_inst_3_doutb[8]),
  .S0(dff_q_3)
);
MUX2 mux_inst_74 (
  .O(doutb[8]),
  .I0(mux_o_72),
  .I1(mux_o_73),
  .S0(dff_q_2)
);
MUX2 mux_inst_75 (
  .O(mux_o_75),
  .I0(dpb_inst_0_doutb[9]),
  .I1(dpb_inst_1_doutb[9]),
  .S0(dff_q_3)
);
MUX2 mux_inst_76 (
  .O(mux_o_76),
  .I0(dpb_inst_2_doutb[9]),
  .I1(dpb_inst_3_doutb[9]),
  .S0(dff_q_3)
);
MUX2 mux_inst_77 (
  .O(doutb[9]),
  .I0(mux_o_75),
  .I1(mux_o_76),
  .S0(dff_q_2)
);
MUX2 mux_inst_78 (
  .O(mux_o_78),
  .I0(dpb_inst_0_doutb[10]),
  .I1(dpb_inst_1_doutb[10]),
  .S0(dff_q_3)
);
MUX2 mux_inst_79 (
  .O(mux_o_79),
  .I0(dpb_inst_2_doutb[10]),
  .I1(dpb_inst_3_doutb[10]),
  .S0(dff_q_3)
);
MUX2 mux_inst_80 (
  .O(doutb[10]),
  .I0(mux_o_78),
  .I1(mux_o_79),
  .S0(dff_q_2)
);
MUX2 mux_inst_81 (
  .O(mux_o_81),
  .I0(dpb_inst_0_doutb[11]),
  .I1(dpb_inst_1_doutb[11]),
  .S0(dff_q_3)
);
MUX2 mux_inst_82 (
  .O(mux_o_82),
  .I0(dpb_inst_2_doutb[11]),
  .I1(dpb_inst_3_doutb[11]),
  .S0(dff_q_3)
);
MUX2 mux_inst_83 (
  .O(doutb[11]),
  .I0(mux_o_81),
  .I1(mux_o_82),
  .S0(dff_q_2)
);
MUX2 mux_inst_84 (
  .O(mux_o_84),
  .I0(dpb_inst_0_doutb[12]),
  .I1(dpb_inst_1_doutb[12]),
  .S0(dff_q_3)
);
MUX2 mux_inst_85 (
  .O(mux_o_85),
  .I0(dpb_inst_2_doutb[12]),
  .I1(dpb_inst_3_doutb[12]),
  .S0(dff_q_3)
);
MUX2 mux_inst_86 (
  .O(doutb[12]),
  .I0(mux_o_84),
  .I1(mux_o_85),
  .S0(dff_q_2)
);
MUX2 mux_inst_87 (
  .O(mux_o_87),
  .I0(dpb_inst_0_doutb[13]),
  .I1(dpb_inst_1_doutb[13]),
  .S0(dff_q_3)
);
MUX2 mux_inst_88 (
  .O(mux_o_88),
  .I0(dpb_inst_2_doutb[13]),
  .I1(dpb_inst_3_doutb[13]),
  .S0(dff_q_3)
);
MUX2 mux_inst_89 (
  .O(doutb[13]),
  .I0(mux_o_87),
  .I1(mux_o_88),
  .S0(dff_q_2)
);
MUX2 mux_inst_90 (
  .O(mux_o_90),
  .I0(dpb_inst_0_doutb[14]),
  .I1(dpb_inst_1_doutb[14]),
  .S0(dff_q_3)
);
MUX2 mux_inst_91 (
  .O(mux_o_91),
  .I0(dpb_inst_2_doutb[14]),
  .I1(dpb_inst_3_doutb[14]),
  .S0(dff_q_3)
);
MUX2 mux_inst_92 (
  .O(doutb[14]),
  .I0(mux_o_90),
  .I1(mux_o_91),
  .S0(dff_q_2)
);
MUX2 mux_inst_93 (
  .O(mux_o_93),
  .I0(dpb_inst_0_doutb[15]),
  .I1(dpb_inst_1_doutb[15]),
  .S0(dff_q_3)
);
MUX2 mux_inst_94 (
  .O(mux_o_94),
  .I0(dpb_inst_2_doutb[15]),
  .I1(dpb_inst_3_doutb[15]),
  .S0(dff_q_3)
);
MUX2 mux_inst_95 (
  .O(doutb[15]),
  .I0(mux_o_93),
  .I1(mux_o_94),
  .S0(dff_q_2)
);
endmodule //Gowin_DPB
