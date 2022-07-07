from mysql.connector import connection


class NeuraDB():

    def __init__(self, host: str, user: str, password: str, database: str):

        self.conn = connection.MySQLConnection(
            host=host,
            user=user,
            password=password,
            database=database
        )

        self.cursor = self.conn.cursor()
        
    def execute_query(self, query: str):

        try:
            self.cursor.execute(query)

            self.conn.commit()

            return True

        except:
            
            return False

    def close_connection(self):

        self.conn.close()

    def clear_table(self, table: str):
        
        try:
            self.cursor.execute(
                "truncate table {}".format(table)
            )

            self.conn.commit()

            return True

        except:
            
            return False
        
    def get_row_data(self, table: str, column: str, value: str):

        try:
            self.cursor.execute(
                "select * from {} where {} = '{}'".format(table, column, value)
            )

            return self.cursor.fetchone()

        except:

            return None
        
    def get_column_data(self, table, column: str):

        try:

            self.cursor.execute(
                "select {} from {}".format(column, table)
            )

            return [value[0] for value in self.cursor.fetchall()]

        except:

            return None
        
    def update_holder(self, nft: str, new_pubkey=None, new_hwid=None):

        try:
            query = "update holders set "
            
            if new_pubkey: query += "pubkey = '{}',".format(new_pubkey)
            if new_hwid: query += "hwid = '{}',".format(new_hwid)
            
            query = query[:-1] + " where nft = '{}'".format(nft)

            self.cursor.execute(str(query))

            self.conn.commit()

            return True
        
        except:
            
            return False
        
    def update_beta(self, beta: str, hwid: str):
        
        try:

            self.cursor.execute(
                """
                update betas set
                hwid = %s
                where code = %s
                """,
                [hwid, beta]
            )

            self.conn.commit()

            return True
        
        except:
            
            return False
        
    def add_nfts(self, nfts: list):

        new_nfts = [[nft] for nft in nfts]

        try:
            self.cursor.executemany(
                """
                insert into holders (nft)
                values (%s)
                """,
                new_nfts
            )

            self.conn.commit()

            return True

        except:

            return False

    def add_betas(self, betas: list):

        new_betas = [[beta] for beta in betas]

        try:
            self.cursor.executemany(
                """
                insert into betas (code)
                values (%s)
                """,
                new_betas
            )

            self.conn.commit()

            return True

        except:

            return False
    
    def check_holder_access(self, nft: str, pubkey: str, hwid: str) -> bool:

        try:

            hold_info = self.get_row_data("holders", "nft", nft)

            db_pubkey = hold_info[0]
            db_hwid = hold_info[2]

            if not db_pubkey:

                self.update_holder(nft, pubkey, hwid)

                return True

            else:

                if pubkey == db_pubkey and hwid == db_hwid:

                    return True

                if pubkey != db_pubkey and hwid == db_hwid:

                    self.update_holder(nft, pubkey, hwid)

                    return True

                if pubkey == db_pubkey and hwid != db_hwid:

                    return False

        except:
            
            return False
    
    def check_beta_access(self, beta: str, hwid: str):
        
        beta_data = self.get_row_data("betas", "code", beta)

        if beta_data:
            
            db_hwid = beta_data[1]

            if db_hwid is None:
                
                self.update_beta(beta, hwid)
                
                return True
            
            elif db_hwid == hwid:
                
                return True
              
        return False
     

    def clear_specific_hold(self, nft: str):

        try:
            self.cursor.execute(
                """
                update holders
                set pubkey = null, hwid = null
                where nft = %s
                """,
                [nft]
            )

            self.conn.commit()

            return True

        except:

            return None

    def get_total_count(self, table: str, column: str):

        try:
            self.cursor.execute(
                """
                select count(*) {} from {}
                """.format(column, table)
            )

            return int(self.cursor.fetchone()[0])

        except:

            return None
        

if __name__ == "__main__":

    NeuraDB()
