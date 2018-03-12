/*------- CREATE SQL---------*/
CREATE TABLE `testsimulation` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `IP` varchar(50) NOT NULL COMMENT 'IP地址',
  `STATU` decimal(10,0) DEFAULT '0' COMMENT '状态\n0：可用\n1：不可用',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8 COMMENT='用于测试模拟浏览的表'
