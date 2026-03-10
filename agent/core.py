import logging 
# this I believe sets up logging
from agent.tasks import lookup_ip, lookup_news, lookup_shodan, lookup_whois
# this imports all the functions for each agenic tasks 

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
# this sets up the logging configuration to log messages to a specific format
logger = logging.getLogger(__name__)
#this creates the logger object which can be used to log messages

class OSINTAgent:
    def __init__(self, target: str):
        self.target = target
        self.results = {}
    # this is the constructor for the OSINTAgent class, it initializes the target and results attributes
    
    def run(self) -> dict:
        logger.info(f"Starting OSINT sweep on: {self.target}")
        # this is the main method that runs OSINT agent tasks and stores all the resultsin a dictionary 
        
        self._run_task("ip_info", lookup_ip, self.target)
        self._run_task("news", lookup_news, self.target)
        self._run_task("shodan", lookup_shodan, self.target)
        self._run_task("whois", lookup_whois, self.target)
        #this runs ip_info and news_task and stores the results
        
        logger.info("Sweep Complete.")
        return self.results
        #this logs in the the complettion message fo the tasks and returns the results dictionary
        
    def _run_task(self, name: str, func, *args):
        # this is a helper method to run a task and stores its results in the results dictionary, it also logs the start and completion of each task
        try:
            logger.info(f"Running task: {name}")
            self.results[name] = func(*args)
        except Exception as e:
            logger.warning(f"Task {name}' failed: {e}")
            self.results[name] = {"error": str(e)}
        # this runs the task and if it fails it logs a warning and stores the error message above
        
            
