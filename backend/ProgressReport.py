import sqlite3
from externalResource import pullNewReports

def main():
    updateReports()

def updateReports():
    databaseConnection = sqlite3.connect('ProgressReport.db')
    
    oldReport = getOldReports(databaseConnection)
    updateDatabase(databaseConnection, oldReport, pullNewReports())

    databaseConnection.commit()
    databaseConnection.close()

def getOldReports(conn):
    cursor = conn.cursor()
    
    try:  
        users = (cursor.execute('SELECT username FROM users')).fetchall()

        reports = {}

        for index in range(len(users)):
            username = users[index][0]

            reports[username] = []


            userReports = cursor.execute(f"SELECT progressName, report FROM progress WHERE username = '{username}';").fetchall()

            for report in userReports: 
                reports[username].append(report)
        
        cursor.close()
        return reports
                                
    except Exception: print("Error trying to pull data from database")

    cursor.close()

def updateDatabase(conn, oldReport, newReport): # fix <-------------------------
    cursor = conn.cursor()

    for reportKey in oldReport.keys():
        if not reportKey in newReport or oldReport[reportKey] == newReport[reportKey]: continue

        for value in newReport[reportKey]:
            reportName, reportValue = value[0], value[1]
            
            try: cursor.execute(f"UPDATE progress SET report = {reportValue} WHERE username = '{reportKey}' and progressName = '{reportName}';")
            except sqlite3.OperationalError as e:
                if "no such column" in str(e).lower(): cursor.execute(f"INSERT INTO progress (progressName, username, report) VALUES ('{reportName}', '{reportKey}', '{reportValue}');")
                else: print("Error attempting to change the database")


            # cursor.execute("""
            # INSERT INTO progress (progressName, username, report)
            # VALUES (?, ?, ?)
            # ON CONFLICT(progressName, username)
            # DO UPDATE SET report=excluded.report
            # """, (reportName, reportKey, reportValue))


    cursor.close()

if __name__ == "__main__": main()