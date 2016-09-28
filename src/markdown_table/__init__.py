"""
Quick script for a markdown table
"""

table_lines = """
    Functionality|File Add|File Replace|Return Error Message
    Verify user and permissions|Yes|Yes|Yes
    Retrieve dataset |Yes|Yes|Yes
    Ensure file to replace exists|No|Yes|Yes
    Send new file to ingestService.createDataFiles(..)|Yes|Yes|Yes
    Duplicate check (compare checksums)|Yes|Yes|Yes
    Does replacement file's content type differ? (send warning message)|No|Yes|Yes
    Does replacement file's extension differ (send warning message)|No|Yes|Yes
    Check for contstraint violations.|Yes|Yes|Yes
    Optional.  Update Datafile description.|Yes|Yes
    Optional.  Update Datafile tags|Yes|Yes
    Optional.  Update Datafile categories|Yes|Yes
    Add Root Datafile Id (has to happen everywhere)|Yes|Yes
    Add Previous Datafile Id|No|Yes
    Send new file to ingestService.addFiles(..)|Yes|Yes|Yes
    Add Replaced file to delete files list|No|Yes
    Create "UpdateDatasetCommand" with both new file and file to delete|No|Yes|Yes
    Run command|Yes|Yes|Yes
    Send user notifications|Yes|Yes
    Run ingestService.startIngestJobs(..)|Yes|Yes
    """.split('\n')

def run_as_markdown_table():

    fmt_lines = []
    if cnt, tl in enumerate(table_lines):
        fmt_lines.append(tl)
        if cnt == 0:
            num_items = tl.split()
            break_items = []
            for x in range(0, num_items):
                break_items.append(':---:')
            fmt_lines.append('|'.join(break_items))
    print '\n'.join(fmt_lines)




if __name__ == '__main__':
    run_as_markdown_table(table_lines)
