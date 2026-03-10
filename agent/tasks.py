import requests
from agent.utils import get_key
import shodan as shodan_lib


def lookup_ip(ip_address: str) -> dict:
    """
    Look up an IP address using the ipinfo.io API. Returns a dictionary of information about the IP.
    """
    token = get_key("IPINFO_TOKEN")
    url = f"https://ipinfo.io/{ip_address}?token={token}"
    
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    
    return response.json()
                                
def lookup_news(query : str) -> list:
    """
    Search for recent news articles mentioning specified target. Aquired
    """
    key = get_key("NEWS_API_KEY")
    url = "https://newsapi.org/v2/everything"
    
    params = {
        "q" : query,
        "apiKey" : key,
        "pageSize" : 5,
        "sortBy": "relevancy"
    }
    
    response = requests.get(url, params=params, timeout = 10)
    response.raise_for_status()
    
    data = response.json()
    return data.get("articles", [])

def lookup_shodan(query: str) -> dict:
    #this is a function to look up information in the Shodan Library, using the get_key fucntion getting the actual API key then creates the Shodan client searching for the query and returning the reuslts in the dictionary
    """
    Search Shodan for exposed services and open ports related to the target.
    """
    api = shodan_lib.Shodan(get_key("SHODAN_API_KEY"))
    # this creates the Shodan client using the API key
    try: 
        results = api.search(query)
        # this searches the Shodan database for the query and stores the results
        return {
            "total": results["total"],
            "matches": [
                {
                    "ip": match.get("ip_str"),
                    "port": match.get("port"),
                    "org": match.get("org"),
                    "hostnames": match.get("hostnames, []")
                    #this returns the relevant information about each match in the Shodan search results, with the IP Address, port, organization, and hostnames
                }
                for match in results.get("matches", [])[:5]
                #this limits the results to the top 5 matches
            ]
        }
    except shodan_lib.APIError as e:
        return {"error": str(e)}
    #this handles any API error that may occur during the search and returns an error message 
    
def lookup_whois(domain: str) -> dict:
    #this is the function to look up information in the Whois database using the get_key function with the API key given
    """
    Look up domain registration info — who owns it and when it was registered.
    """
    
    key = get_key("WHOIS_API_KEY")
    url = "https://www.whoisxmlapi.com/whoisserver/WhoisService"
    params = {
        "apiKey": key,
        "domainName": domain,
        "outputFormat": "JSON"
    }
    
    response = requests.get(url, params=params, timeout= 10)
    response.raise_for_status()
    return response.json()
    #this sends the get request function to the Whois API with the specified parameters and returns the response in JSON format
    
    