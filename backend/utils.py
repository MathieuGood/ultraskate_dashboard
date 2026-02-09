import re


class Utils:
    """
    A utility class containing various helper methods.
    """

    @classmethod
    def is_hhmmss_format(cls, str_time):
        """
        Checks whether a string matches the HH:MM:SS time format.

        Args:
            str_time (str): The string to check.

        Returns:
            bool: True if the string matches the HH:MM:SS format, False otherwise.
        """
        return re.match(r"^\d{2}:\d{2}:\d{2}$", str_time)

    @classmethod
    def convert_time_str_to_seconds(cls, str_time) -> int | None:
        """
        Converts a time string in HH:MM:SS format to seconds.

        Args:
            str_time (str): A time string in HH:MM:SS format.

        Returns:
            int: The equivalent time in seconds.
        """
        try:
            h, m, s = str_time.split(":")
            return int(h) * 3600 + int(m) * 60 + int(s)
        except ValueError:
            return None

    @classmethod
    # In a '00:08:26 (00:08:26)' string, extract only the time that is not
    # between the parentheses using a regex.
    def extract_time(cls, str_time) -> str | None:
        """
        Extracts the first HH:MM:SS time string found in a given string.

        Args:
            str_time (str): The string containing a time value.

        Returns:
            str | None: The extracted time string if found, otherwise None.
        """
        match = re.search(r"(\d{2}:\d{2}:\d{2})", str_time)
        if match:
            return match.group(0)
        return None

    @classmethod
    def seconds_to_hhmmss(cls, total_seconds: int) -> str:
        """
        Converts a total number of seconds to a HH:MM:SS formatted string.

        Args:
            total_seconds (int): The total number of seconds.

        Returns:
            str: The time in HH:MM:SS format.
        """
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    @classmethod
    def check_url_format(cls, url) -> bool:
        """
        Checks whether a URL is in a valid HTTP or HTTPS format.

        Args:
            url (str): The URL to validate.

        Returns:
            bool: True if the URL format is valid, False otherwise.
        """
        match = re.match(r"^https?://(?:www\.)?[^/]+/", url)
        return bool(match)

    @classmethod
    def extract_base_url(cls, url) -> str | None:
        """
        Extracts the base URL from a full URL.

        Args:
            url (str): The URL to extract the base URL from.

        Returns:
            str | None: The base URL if parsing succeeds, otherwise None.
        """
        if not Utils.check_url_format(url):
            return None

        match = re.search(r"^https?://(?:www\.)?[^/]+/", url)
        if match:
            return match.group(0)
        return None
