import sys
import json
from agent.core import OSINTAgent
from agent.report import generate_report

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "8.8.8.8"
    
    agent = OSINTAgent(target)
    results = agent.run()
    
    generate_report(target, results) 
    # this generates the report using the target and results from the OSINTAgent
    
    
          