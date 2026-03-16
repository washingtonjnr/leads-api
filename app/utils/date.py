from datetime import datetime

def format_date(date_str: str) -> str:
    """
    Convert data in the format 'yyyy-m-d' or 'yyyy-mm-dd' to 'dd/mm/yyyy'.

    Arguments:

    date_str: string containing the date from DummyJSON

    Returns:
    string without formatting 'dd/mm/yyyy' or None if input is None
    """

    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return date_str