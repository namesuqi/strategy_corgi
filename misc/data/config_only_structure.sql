/*
Navicat MySQL Data Transfer

Source Server         : corgi
Source Server Version : 50638
Source Host           : 192.168.3.217:3306
Source Database       : config

Target Server Type    : MYSQL
Target Server Version : 50638
File Encoding         : 65001

Date: 2017-11-07 11:36:06
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for inits
-- ----------------------------
DROP TABLE IF EXISTS `inits`;
CREATE TABLE `inits` (
  `role` varchar(20) NOT NULL,
  `num` int(11) NOT NULL,
  PRIMARY KEY (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for online
-- ----------------------------
DROP TABLE IF EXISTS `online`;
CREATE TABLE `online` (
  `peer_id` char(32) NOT NULL DEFAULT '',
  `sdk_version` varchar(10) DEFAULT NULL,
  `public_ip` varchar(20) DEFAULT NULL,
  `public_port` int(5) DEFAULT NULL,
  `private_ip` varchar(20) DEFAULT NULL,
  `private_port` int(5) DEFAULT NULL,
  `nat_type` int(1) DEFAULT NULL,
  `timestamp` varchar(100) DEFAULT NULL,
  `stun_ip` varchar(20) DEFAULT NULL,
  `isp_id` varchar(20) DEFAULT NULL,
  `province_id` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`peer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for peer
-- ----------------------------
DROP TABLE IF EXISTS `peer`;
CREATE TABLE `peer` (
  `peer_id` char(32) NOT NULL DEFAULT '',
  `sdk_version` varchar(10) DEFAULT NULL,
  `public_ip` varchar(20) DEFAULT NULL,
  `public_port` int(5) DEFAULT NULL,
  `private_ip` varchar(20) DEFAULT NULL,
  `private_port` int(5) DEFAULT NULL,
  `timestamp` varchar(100) DEFAULT NULL,
  `nat_type` int(1) DEFAULT NULL,
  `file_id` varchar(50) DEFAULT NULL,
  `duration` varchar(5) DEFAULT NULL,
  `seeds_download` varchar(15) DEFAULT NULL,
  `seeds_upload` varchar(15) DEFAULT NULL,
  `cdn_download` varchar(10) DEFAULT NULL,
  `p2p_download` varchar(5) DEFAULT NULL,
  `operation` varchar(10) DEFAULT NULL,
  `stun_ip` varchar(20) DEFAULT NULL,
  `isp_id` varchar(10) DEFAULT NULL,
  `province_id` varchar(10) DEFAULT NULL,
  `play_type` varchar(5) DEFAULT NULL,
  `error_type` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`peer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for seed
-- ----------------------------
DROP TABLE IF EXISTS `seed`;
CREATE TABLE `seed` (
  `peer_id` char(32) NOT NULL DEFAULT '',
  `sdk_version` varchar(10) DEFAULT NULL,
  `timestamp` varchar(100) DEFAULT NULL,
  `file_id` varchar(50) DEFAULT NULL,
  `file_status` varchar(20) DEFAULT NULL,
  `lsm_free` varchar(10) DEFAULT NULL,
  `lsm_total` varchar(10) DEFAULT NULL,
  `private_ip` varchar(20) DEFAULT NULL,
  `private_port` int(5) DEFAULT NULL,
  `public_ip` varchar(20) DEFAULT NULL,
  `public_port` int(5) DEFAULT NULL,
  `nat_type` int(1) DEFAULT NULL,
  `disk_total` bigint(50) DEFAULT NULL,
  `stun_ip` varchar(20) DEFAULT NULL,
  `isp_id` varchar(10) DEFAULT NULL,
  `province_id` varchar(10) DEFAULT NULL,
  `disk_free` bigint(20) DEFAULT NULL,
  `duration` int(3) DEFAULT NULL,
  `seeds_download` int(10) DEFAULT NULL,
  `seeds_upload` int(10) DEFAULT NULL,
  `cdn_download` int(10) DEFAULT NULL,
  `p2p_download` int(10) DEFAULT NULL,
  `operation` varchar(10) DEFAULT NULL,
  `play_type` varchar(5) DEFAULT NULL,
  `error_type` varchar(10) DEFAULT NULL,
  `priority` int(10) DEFAULT NULL,
  PRIMARY KEY (`peer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for vod_heartbeat
-- ----------------------------
DROP TABLE IF EXISTS `vod_heartbeat`;
CREATE TABLE `vod_heartbeat` (
  `peer_id` varchar(32) NOT NULL,
  `sdk_version` varchar(10) DEFAULT NULL,
  `nat_type` varchar(1) DEFAULT NULL,
  `public_ip` varchar(15) DEFAULT NULL,
  `public_port` int(5) DEFAULT NULL,
  `private_ip` varchar(15) DEFAULT NULL,
  `private_port` int(5) DEFAULT NULL,
  `stun_ip` varchar(15) DEFAULT NULL,
  `isp_id` varchar(5) DEFAULT NULL,
  `province_id` varchar(5) DEFAULT NULL,
  `timestamp` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`peer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for vod_sdk_lsm
-- ----------------------------
DROP TABLE IF EXISTS `vod_sdk_lsm`;
CREATE TABLE `vod_sdk_lsm` (
  `peer_id` varchar(32) NOT NULL,
  `disk_total` varchar(15) DEFAULT NULL,
  `disk_free` varchar(15) DEFAULT NULL,
  `lsm_total` varchar(10) DEFAULT NULL,
  `lsm_free` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`peer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
