
-- Database: `facebook_data`
--

-- --------------------------------------------------------


--
-- Table structure for table `search_keyword`
--

CREATE TABLE `search_keyword` (
  `keyword_id` int(11) NOT NULL AUTO_INCREMENT,
  `keyword` varchar(255) NOT NULL,
  PRIMARY KEY (`keyword_id`),
  UNIQUE KEY `keyword` (`keyword`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



--
-- Table structure for table `post_comments`
--

CREATE TABLE `post_comments` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `FK_keyword_id` int(11) NOT NULL,
  `comment` text NOT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `FK_keyword_id` (`FK_keyword_id`),
  CONSTRAINT `post_comments_ibfk_1` FOREIGN KEY (`FK_keyword_id`) REFERENCES `search_keyword` (`keyword_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
