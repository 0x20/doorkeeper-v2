
Table structure for table `cards` in db doorkeeper.db (sqlite3)
---

CREATE TABLE `cards` (
  `card_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `card_uid` text NOT NULL,
  `card_owner` text DEFAULT unknown NOT NULL,
  `card_added` int(30) DEFAULT 0 NOT NULL,
  `card_deleted` int(30) DEFAULT 0 NOT NULL);
  
Dependencies:
---
* platformio
* screen
* sqlite3
