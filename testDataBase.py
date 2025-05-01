import sqlite3 
conn = sqlite3.connect('insurance_data.db')
c = conn.cursor()
recommended_policy = ['HealthGain Policy', 'ReAssure 2.0', 'Activ Health Platinum', 'Complete Health Insurance', 'ReAssure 2.0', 'ProHealth Prime', 'Optima Restore', 'Arogya Supreme', 'Activ Health Platinum', 'Activ Health Platinum', 'ReAssure 2.0', 'Arogya Supreme', 'Arogya Supreme', 'HealthGain Policy', 'Complete Health Insurance', 'Activ Health Platinum', 'Family Health Optima', 'ProHealth Prime', 'Activ Health Platinum', 'Optima Restore', 'Family Health Optima', 'Care Freedom', 'ProHealth Prime', 'ReAssure 2.0', 'Arogya Supreme', 'ReAssure 2.0', 'Care Freedom', 'Arogya Supreme', 'Family Health Optima', 'Medicare Premier', 'HealthGain Policy', 'Family Health Optima', 'ProHealth Prime', 'ReAssure 2.0', 'Activ Health Platinum', 'Care Freedom', 'Complete Health Insurance', 'Activ Health Platinum', 'Activ Health Platinum', 'Complete Health Insurance', 'Family Health Optima', 'Family Health Optima', 'HealthGain Policy', 'Care Freedom', 'Optima Restore', 'Medicare Premier', 'ProHealth Prime', 'Optima Restore', 'Arogya Supreme', 'Activ Health Platinum', 'Activ Health Platinum', 'Activ Health Platinum', 'Optima Restore', 'Activ Health Platinum', 'ReAssure 2.0', 'Family Health Optima', 'ProHealth Prime', 'Activ Health Platinum', 'Optima Restore', 'Medicare Premier', 'HealthGain Policy', 'Optima Restore', 'Family Health Optima', 'Activ Health Platinum', 'ReAssure 2.0', 'ReAssure 2.0', 'ReAssure 2.0', 'Arogya Supreme', 'Family Health Optima', 'ReAssure 2.0', 'Arogya Supreme', 'Arogya Supreme', 'ProHealth Prime', 'Optima Restore', 'Family Health Optima', 'ProHealth Prime', 'ReAssure 2.0', 'Family Health Optima', 'Medicare Premier', 'HealthGain Policy', 'ReAssure 2.0', 'Complete Health Insurance', 'Arogya Supreme', 'HealthGain Policy', 'Family Health Optima']

recommended_provider =['Niva Bupa', 'Care Health', 'Reliance General', 'Star Health', 'Tata AIG', 'ManipalCigna', 'ManipalCigna', 'SBI General', 'Star Health', 'HDFC ERGO', 'ICICI Lombard', 'ICICI Lombard', 'HDFC ERGO', 'Reliance General', 'SBI General', 'ICICI Lombard', 'HDFC ERGO', 'SBI General', 'Niva Bupa', 'HDFC ERGO', 'Niva Bupa', 'Reliance General', 'Aditya Birla', 'HDFC ERGO', 'Reliance General', 'Tata AIG', 'ICICI Lombard', 'Tata AIG', 'ManipalCigna', 'SBI General', 'Reliance General', 'Care Health', 'SBI General', 'HDFC ERGO', 'Star Health', 'Reliance General', 'Reliance General', 'SBI General', 'ManipalCigna', 'SBI General', 'Star Health', 'Tata AIG', 'ICICI Lombard', 'ICICI Lombard', 'Reliance General', 'SBI General', 'Reliance General', 'Reliance General', 'Reliance General', 'ICICI Lombard', 'Tata AIG', 'Tata AIG', 'ICICI Lombard', 'Reliance General', 'HDFC ERGO', 'Reliance General', 'SBI General', 'Niva Bupa', 'HDFC ERGO', 'Tata AIG', 'Reliance General', 'ICICI Lombard', 'HDFC ERGO', 'Aditya Birla', 'HDFC ERGO', 'Care Health', 'Niva Bupa', 'Care Health', 'HDFC ERGO', 'Reliance General', 'HDFC ERGO', 'ICICI Lombard', 'Reliance General', 'Niva Bupa', 'Reliance General', 'HDFC ERGO', 'Reliance General', 'Reliance General', 'Reliance General', 'Niva Bupa', 'SBI General', 'ICICI Lombard', 'ICICI Lombard', 'Aditya Birla', 'Care Health', 'Aditya Birla', 'ICICI Lombard', 'Reliance General', 'SBI General', 'SBI General', 'HDFC ERGO']

# c.execute('''
#     CREATE TABLE IF NOT EXISTS login_details (
#         name TEXT NOT NULL,
#         password TEXT NOT NULL
#     )
# ''')

# Commit the changes and close the connection
# conn.commit()
# conn.close()
# c.execute('''
#     CREATE TABLE IF NOT EXISTS policy_list (
#         provider TEXT,
#         policy_name TEXT
#     )
# ''')
conn = sqlite3.connect("insurance_data.db")
cur = conn.cursor()
cur.execute("SELECT  * FROM policy_list")
rows = cur.fetchall()
conn.close()
for d in rows:
    print(d)
# c.execute("SELECT name FROM sqlite_master WHERE type='table';")
# tables = c.fetchall()

# # Display the table names
# print("Tables in the database:")
# for table in tables:
#     print(table[0])

# c.execute("ALTER TABLE predictions ADD COLUMN role TEXT")
# c.execute("update  login_details set password = ? where name=?",("0310","admin"))
# c.execute("PRAGMA table_info(policy_list)" )
# c.execute("select * from policy_list")
# row=c.fetchall()
# c.execute("SELECT policy_name, provider FROM policy_list")
# rows = c.fetchall()
# for d in rows:
#     print(d)

# # c.execute("DROP TABLE IF EXISTS users")
# conn.commit()
conn.close()




# list of all the tables
('predictions',)
('policy_list',)
('login_details',)
