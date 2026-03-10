import json
from datetime import datetime
from shlex import join

def generate_report(target: str, results: dict) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # this function generates a report in markdown format, it takes the target and results as input and formats into a readable report
    lines = [
        f"OSINT Report for: {target}",
        f"**Generated:** {timestamp}",
        "---",
        
    ]
    
    ip_data = results.get("ip_info", {})
    # this adds the IP information section to the report, it checks if there is any errors in ip_data
    if "error" not in ip_data:
        lines += [
            "## IP Intelligence",
            f"- **IP:** {ip_data.get('ip', 'N/A')}",
            f"- **Organization:** {ip_data.get('org', 'N/A')}",
            f"- **Location:** {ip_data.get('city', '')}, {ip_data.get('country', '')}",
        ]
        # this formats the IP information in a readable way in the report
    else: 
        lines.append("## IP Intelligence\n- Not available for this target")
        # this adds a message to the report if the IP information is not available
        
    #News
    articles = results.get("news", [])
    if articles:
        lines.append("\n## News Mentions")
        for article in articles[:5]:
            lines.append(f"- [{article.get('title')}]({article.get('url')})") 
        # this adds the news mentions section to the report, it formats the news articles as a list of links with the title and URL
    
    #Shodan
    shodan_data = results.get("shodan", {})
    if "error" not in shodan_data and shodan_data:
        lines.append("\n## Exposed Infrastructure (Shodan)")
        lines.append(f"- **Total results:** {shodan_data.get('total', 0)}")
        for match in shodan_data.get("matches", []):
            lines.append(f"- {match['ip']} — Port {match['port']} — {match.get('org', 'Unknown')}")
    # this adds the Shodan section to the report, it checks if there are any errors in the Shodan data and formats the results to be readable
    
    #Whois
    whois_data = results.get("whois", {})
    if whois_data and "error" not in whois_data:
        record = whois_data.get("WhoisRecord", {})
        lines += [
            "\n## WHOIS Registration",
            f"- **Registrar:** {record.get('registrarName', 'N/A')}",
            f"- **Created:** {record.get('createdDate', 'N/A')}",
            f"- **Expires:** {record.get('expiresDate', 'N/A')}",
        ]
    # this adds the Whois section to the report, it checks if there are any errors in the Whois data and formats the registration information in a readable way
    
    report = "\n".join(lines)
    # this joins all the lines together into a single string to create the final report 
    
    filename = f"report_{target.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"           
    # this creates a filename for the report based on the target and timestamp
    with open(filename, "w") as f:
        f.write(report)
        # this writes the report to a markdown file
        
    print(f"\nReport Saved: {filename}")
    return report
