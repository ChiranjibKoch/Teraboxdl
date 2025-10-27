from apify_client import ApifyClient
from config import Config


class TeraboxDownloader:
    def __init__(self):
        self.client = ApifyClient(Config.APIFY_API_TOKEN)
        self.actor_id = "vApnoJCJT5U1T74Vl"
    
    async def download(self, links: list):
        """
        Download files from Terabox using Apify Actor
        
        Args:
            links: List of Terabox URLs to download
            
        Returns:
            List of results from the Actor
        """
        # Prepare the Actor input
        run_input = {
            "links": links,
            "proxyConfiguration": {"useApifyProxy": False},
        }
        
        # Run the Actor and wait for it to finish
        run = self.client.actor(self.actor_id).call(run_input=run_input)
        
        # Fetch and collect Actor results from the run's dataset
        results = []
        for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
            results.append(item)
        
        return results
    
    def format_result(self, item: dict):
        """
        Format the download result for display
        
        Args:
            item: Result item from Apify Actor
            
        Returns:
            Formatted string with download information
        """
        formatted = "📥 **Download Information**\n\n"
        
        if "fileName" in item:
            formatted += f"📄 **File Name:** {item['fileName']}\n"
        
        if "fileSize" in item:
            formatted += f"💾 **Size:** {item['fileSize']}\n"
        
        if "downloadUrl" in item:
            formatted += f"🔗 **Download URL:** {item['downloadUrl']}\n"
        
        if "thumbnailUrl" in item:
            formatted += f"🖼 **Thumbnail:** {item['thumbnailUrl']}\n"
        
        return formatted
