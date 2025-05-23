import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
import click
from rich.console import Console
from rich.table import Table
import requests

class DcCityCast:
    """
    A class to extract event data from the DC City Cast website.
    """

    def __init__(self):
        """
        Initializes the DcCityCast object.
        """
        self.soup = None

    def fetch_html(self, url: str) -> str:
        """Fetches the HTML content from a URL.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The HTML content.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
            return None

    def load_html(self, html_content: str):
        """Loads the html content"""
        self.html_content = html_content
        self.soup = BeautifulSoup(self.html_content, 'html.parser')

    def fetch_events(self) -> list[dict]:
        """
        Extracts event data (date and events) from HTML content and returns it in JSON format.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents a date and its events.
        """
        if not self.soup:
            return [{"error": "HTML content not loaded"}]

        event_list = self.soup.find(id='event-list')
        if not event_list:
            return [{"error": "Event list not found"}]

        events_by_date = []
        for day_div in event_list.find_all('div', class_='grid'):
            date_header = day_div.find('h3')
            if not date_header:
                continue
            date = date_header.text.strip()

            event_items = []
            ul = day_div.find('ul')
            if ul:
                for li in ul.find_all('li'):
                    a_tag = li.find('a')
                    event_name = a_tag.text.strip() if a_tag else "No Name"
                    event_url = a_tag['href'] if a_tag and 'href' in a_tag.attrs else None

                    # Extract time, price, and location
                    text = li.text.strip()
                    parts = text.split('|')
                    time_str = parts[1].strip() if len(parts) > 1 else None
                    price = parts[2].strip() if len(parts) > 2 else None
                    location = parts[3].strip() if len(parts) > 3 else None

                    # Sanitize time string
                    import re
                    from datetime import datetime
                    time = None
                    if time_str:
                        time_str = re.sub(r"^[.\s]+|[.\s]+$", "", time_str)  # Remove leading/trailing spaces and periods
                        try:
                            # Attempt to parse as a single time
                            time = datetime.strptime(time_str, "%I:%M %p").isoformat()
                        except ValueError as e:
                            time = None
                    try:
                        # Attempt to parse as a time range
                        time_parts = time_str.split(' - ')
                        if len(time_parts) == 2:
                            start_time = datetime.strptime(time_parts[0], "%I:%M %p").isoformat()
                            end_time = datetime.strptime(time_parts[1], "%I:%M %p").isoformat()
                            time = f"{start_time} - {end_time}"
                        else:
                            time = time_str  # If it's not a range, keep the original string
                    except ValueError:
                        time = None  # If parsing fails, keep the original string

                    event_items.append({
                        "name": event_name,
                        "url": event_url,
                        "time": time,
                        "location": location,
                        "price": price
                    })

            events_by_date.append({
                "date": date,
                "events": event_items
            })

        return events_by_date

@click.command()
@click.option('--test', is_flag=True, help='Run in test mode using sample.html')
def main(test):
    """
    Extracts event data from DC City Cast website and prints it in JSON format.
    """
    console = Console()
    dc_city_cast = DcCityCast()

    if test:
        console.print("[bold blue]Running in test mode using sample.html[/]")
        with open('sample.html', 'r') as f:
            html_content = f.read()
        dc_city_cast.load_html(html_content)
    else:
        url = "https://dc.citycast.fm/events"
        console.print(f"[bold blue]Fetching events from URL: {url}[/]")
        html_content = dc_city_cast.fetch_html(url)
        if html_content:
            dc_city_cast.load_html(html_content)
        else:
            console.print("[bold red]Failed to fetch HTML content from URL[/]")
            return

    events = dc_city_cast.fetch_events()

    console.print(json.dumps(events, indent=4))

if __name__ == '__main__':
    main()
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
import click
from rich.console import Console
from rich.table import Table

class DcCityCast:
    """
    A class to extract event data from the DC City Cast website.
    """

    def __init__(self, html_content: str = None):
        """
        Initializes the DcCityCast object.

        Args:
            html_content (str, optional): The HTML content to parse. Defaults to None.
        """
        self.html_content = html_content
        self.soup = None

    def load_html(self, html_content: str):
        """Loads the html content"""
        self.html_content = html_content
        self.soup = BeautifulSoup(self.html_content, 'html.parser')

    def fetch_events(self) -> list[dict]:
        """
        Extracts event data (date and events) from HTML content and returns it in JSON format.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents a date and its events.
        """
        if not self.soup:
            return [{"error": "HTML content not loaded"}]

        event_list = self.soup.find(id='event-list')
        if not event_list:
            return [{"error": "Event list not found"}]

        events_by_date = []
        for day_div in event_list.find_all('div', class_='grid'):
            date_header = day_div.find('h3')
            if not date_header:
                continue
            date = date_header.text.strip()

            event_items = []
            ul = day_div.find('ul')
            if ul:
                for li in ul.find_all('li'):
                    a_tag = li.find('a')
                    event_name = a_tag.text.strip() if a_tag else "No Name"
                    event_url = a_tag['href'] if a_tag and 'href' in a_tag.attrs else None

                    # Extract time, price, and location
                    text = li.text.strip()
                    parts = text.split('|')
                    time_str = parts[1].strip() if len(parts) > 1 else None
                    price = parts[2].strip() if len(parts) > 2 else None
                    location = parts[3].strip() if len(parts) > 3 else None

                    # Sanitize time string
                    time = None
                    if time_str:
                        time_str = re.sub(r"^[.\s]+|[.\s]+$", "", time_str)  # Remove leading/trailing spaces and periods
                    try:
                        # Attempt to parse as a single time
                        time = datetime.strptime(time_str, "%I:%M %p").isoformat()
                    except ValueError as e:
                        time = None
                    try:
                        # Attempt to parse as a time range
                        time_parts = time_str.split(' - ')
                        if len(time_parts) == 2:
                            start_time = datetime.strptime(time_parts[0], "%I:%M %p").isoformat()
                            end_time = datetime.strptime(time_parts[1], "%I:%M %p").isoformat()
                            time = f"{start_time} - {end_time}"
                        else:
                            time = time_str  # If it's not a range, keep the original string
                    except ValueError:
                        time = None  # If parsing fails, keep the original string

                    event_items.append({
                        "name": event_name,
                        "url": event_url,
                        "time": time,
                        "location": location,
                        "price": price
                    })

            events_by_date.append({
                "date": date,
                "events": event_items
            })

        return events_by_date

@click.command()
@click.option('--test', is_flag=True, help='Run in test mode using sample.html')
def main(test):
    """
    Extracts event data from DC City Cast website and prints it in JSON format.
    """
    console = Console()

    if test:
        console.print("[bold blue]Running in test mode using sample.html[/]")
        with open('sample.html', 'r') as f:
            html_content = f.read()
    else:
        console.print("[bold red]Fetching from website is not yet implemented[/]")
        return

    dc_city_cast = DcCityCast()
    dc_city_cast.load_html(html_content)
    events = dc_city_cast.fetch_events()

    console.print(json.dumps(events, indent=4))

if __name__ == '__main__':
    main()
