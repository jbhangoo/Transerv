from dateutil.parser import parse
import pytz


def convert_date_string(date_string):
    """
    Converts a user input date string to a format compatible with SQLAlchemy Date column.
    Returns a tuple (converted_date, is_valid) where:
    - converted_date: datetime.date object if valid, Error message if invalid
    - is_valid: True if the date was valid, False otherwise

    Example usage:
        date, valid = convert_date_string("2023-05-15")
        if valid:
            model.date_column = date
            db.session.add(model)
            db.session.commit()
        else:
            # Handle invalid date
    """
    if not date_string or not isinstance(date_string, str):
        return "No date found", False

    try:
        # Try to parse the date string using dateutil.parser
        # This handles various date formats like "2023-05-15", "05/15/2023", "May 15, 2023", etc.
        parsed_date = parse(date_string, fuzzy=False)

        # Convert to date object (removes time component)
        date_only = parsed_date.date()

        # Validate reasonable date range (e.g., between 1900 and 2100)
        if date_only.year < 1900 or date_only.year > 2100:
            return "Date out of range", False

        return date_only, True

    except (ValueError, OverflowError, TypeError):
        # Handle parsing errors
        return "Could not process date", False


def convert_time_string(time_string):
    """
    Converts a user input time string to a UTC time format compatible with SQLAlchemy Time column.

    Args:
        time_string (str): The time string to convert (e.g., "14:30", "2:30 PM", "14:30:15")
        timezone (str, optional): User's timezone name (e.g., "America/New_York").
                                 If None, assumes time is already in UTC.

    Returns:
        tuple: (converted_time, is_valid) where:
            - converted_time: datetime.time object in UTC if valid, error message if invalid
            - is_valid: True if the time was valid, False otherwise

    Example usage:
        time_obj, valid = convert_time_string("2:30 PM", "America/New_York")
        if valid:
            model.time_column = time_obj
            db.session.add(model)
            db.session.commit()
        else:
            # Handle invalid time
    """
    if not time_string or not isinstance(time_string, str):
        return "No time found", False

    try:
        # Try to parse the time string - add a dummy date to make dateutil.parser happy
        dummy_date = "2000-01-01 "
        parsed_datetime = parse(dummy_date + time_string)
        utc_time = parsed_datetime.time()

        return utc_time, True

    except (ValueError, OverflowError, TypeError):
        # Handle parsing errors
        return "Could not process time", False