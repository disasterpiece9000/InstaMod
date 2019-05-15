from datetime import datetime
from configparser import ConfigParser


class Subreddit:
    def __init__(self, sub_name, r):
        self.r = r
        self.sub_name = sub_name
        self.sub = r.subreddit(sub_name)
        self.start_interval = datetime.now()
        
        # Read config file from wiki page
        config = ConfigParser(allow_no_value=True)
        config.read_string(self.sub.wiki["InstaModTest"].content_md)
        self.main_config = config["MAIN CONFIG"]
        print(self.main_config)
        self.flair_config = config["FLAIR"]
        print(self.flair_config)
        self.qc_config = config["QUALITY COMMENTS"]
        print(self.qc_config)
        self.progression_tiers = self.load_nested_config("PROGRESSION TIER", config)
        print(self.progression_tiers)
        self.sub_activity = self.load_nested_config("SUB ACTIVITY", config)
        print(self.sub_activity)
        self.sub_groups = self.load_nested_config("SUB GROUP", config)
        print(self.sub_groups)
    
    @staticmethod
    def load_nested_config(main_name, config):
        hold_config = {}
        tier_count = 1
        
        while True:
            tier_name = main_name + " " + str(tier_count)
            tier_count += 1
            
            if tier_name in config:
                hold_config[tier_name] = config[tier_name]
                
                # Check for and/or rules
                tier_name_and = tier_name + " - AND"
                if tier_name_and in config:
                    hold_config[tier_name_and] = config[tier_name_and]
                
                tier_name_or = tier_name + " - OR"
                if tier_name_or in config:
                    hold_config[tier_name_or] = config[tier_name_or]
            
            # Last tier was discovered
            else:
                break
        
        return hold_config
