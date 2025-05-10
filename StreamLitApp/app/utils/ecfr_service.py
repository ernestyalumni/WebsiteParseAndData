import pandas as pd
import streamlit as st
import requests
from datetime import datetime
import json
from pathlib import Path
from .supabase_client import get_supabase_client

# Get the app directory
app_dir = Path(__file__).parent.parent
data_dir = app_dir / "data"
data_dir.mkdir(exist_ok=True)

class ECFRService:
    """Service for fetching and analyzing eCFR data"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        self.base_url = "https://www.ecfr.gov/api/v1"
        
    def fetch_titles(self):
        """Fetch all CFR titles"""
        try:
            # Try to get from Supabase first
            if self.supabase:
                response = self.supabase.table('ecfr_titles').select('*').execute()
                if response.data:
                    return pd.DataFrame(response.data)
    
            # If not in Supabase or no connection, fetch from API
            url = f"{self.base_url}/titles"
            response = requests.get(url)
            response.raise_for_status()
            
            titles = response.json()['data']
            df = pd.DataFrame(titles)
            
            # Save to Supabase if available
            if self.supabase:
                self.supabase.table('ecfr_titles').upsert(df.to_dict('records')).execute()
            
            # Save locally as backup
            df.to_csv(data_dir / "ecfr_titles.csv", index=False)
            
            return df
        
        except Exception as e:
            st.error(f"Error fetching titles: {e}")
            
            # Try to load from local backup
            try:
                return pd.read_csv(data_dir / "ecfr_titles.csv")
            except:
                return pd.DataFrame()
    
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def fetch_agencies(self):
        """Fetch all agencies"""
        try:
            # Try to get from Supabase first
            if self.supabase:
                response = self.supabase.table('ecfr_agencies').select('*').execute()
                if response.data:
                    return pd.DataFrame(response.data)
            
            # If not in Supabase or no connection, fetch from API
            url = f"{self.base_url}/agencies"
            response = requests.get(url)
            response.raise_for_status()
            
            agencies = response.json()['data']
            df = pd.DataFrame(agencies)
            
            # Save to Supabase if available
            if self.supabase:
                self.supabase.table('ecfr_agencies').upsert(df.to_dict('records')).execute()
            
            # Save locally as backup
            df.to_csv(data_dir / "ecfr_agencies.csv", index=False)
            
            return df
        
        except Exception as e:
            st.error(f"Error fetching agencies: {e}")
            
            # Try to load from local backup
            try:
                return pd.read_csv(data_dir / "ecfr_agencies.csv")
            except:
                return pd.DataFrame()
    
    @st.cache_data
    def fetch_title_parts(self, title_number):
        """Fetch parts for a specific title"""
        try:
            # Try to get from Supabase first
            if self.supabase:
                response = self.supabase.table('ecfr_parts').select('*').eq('title_number', title_number).execute()
                if response.data:
                    return pd.DataFrame(response.data)
            
            # If not in Supabase or no connection, fetch from API
            url = f"{self.base_url}/titles/{title_number}/parts"
            response = requests.get(url)
            response.raise_for_status()
            
            parts = response.json()['data']
            df = pd.DataFrame(parts)
            
            # Add title_number for reference
            df['title_number'] = title_number
            
            # Save to Supabase if available
            if self.supabase:
                self.supabase.table('ecfr_parts').upsert(df.to_dict('records')).execute()
            
            # Save locally as backup
            local_path = data_dir / f"ecfr_title_{title_number}_parts.csv"
            df.to_csv(local_path, index=False)
            
            return df
        
        except Exception as e:
            st.error(f"Error fetching parts for title {title_number}: {e}")
            
            # Try to load from local backup
            try:
                local_path = data_dir / f"ecfr_title_{title_number}_parts.csv"
                return pd.read_csv(local_path)
            except:
                return pd.DataFrame()
    
    def fetch_part_content(self, title_number, part_number):
        """Fetch content for a specific part"""
        try:
            # Try to get from Supabase first
            if self.supabase:
                response = self.supabase.table('ecfr_content').select('*').eq('title_number', title_number).eq('part_number', part_number).execute()
                if response.data:
                    content = response.data[0]['content']
                    return json.loads(content) if isinstance(content, str) else content
            
            # If not in Supabase or no connection, fetch from API
            url = f"{self.base_url}/titles/{title_number}/parts/{part_number}/full"
            response = requests.get(url)
            response.raise_for_status()
            
            content = response.json()['data']
            
            # Save to Supabase if available
            if self.supabase:
                record = {
                    'title_number': title_number,
                    'part_number': part_number,
                    'content': json.dumps(content),
                    'fetched_at': datetime.now().isoformat()
                }
                self.supabase.table('ecfr_content').upsert([record]).execute()
            
            # Save locally as backup
            local_path = data_dir / f"ecfr_title_{title_number}_part_{part_number}.json"
            with open(local_path, 'w') as f:
                json.dump(content, f)
            
            return content
        
        except Exception as e:
            st.error(f"Error fetching content for title {title_number}, part {part_number}: {e}")
            
            # Try to load from local backup
            try:
                local_path = data_dir / f"ecfr_title_{title_number}_part_{part_number}.json"
                with open(local_path, 'r') as f:
                    return json.load(f)
            except:
                return {}
    
    def analyze_word_count_by_agency(self):
        """Analyze word count per agency"""
        agencies = self.fetch_agencies()
        
        # This is a simplified example - in a real implementation,
        # you would need to fetch content for each agency's regulations
        # and count words
        
        # For now, let's create sample data
        agency_data = []
        
        for _, agency in agencies.iterrows():
            # In a real implementation, you would fetch and analyze actual content
            word_count = len(agency.get('name', '')) * 1000  # Dummy calculation
            
            agency_data.append({
                'agency_id': agency.get('id'),
                'agency_name': agency.get('name'),
                'word_count': word_count
            })
        
        return pd.DataFrame(agency_data)
    
    def get_historical_changes(self, title_number, part_number, limit=10):
        """Get historical changes for a specific part"""
        try:
            # Try to get from Supabase first
            if self.supabase:
                response = self.supabase.table('ecfr_history').select('*').eq('title_number', title_number).eq('part_number', part_number).order('version_date', desc=True).limit(limit).execute()
                if response.data:
                    return pd.DataFrame(response.data)
            
            # If not in Supabase or no connection, fetch from API
            url = f"{self.base_url}/titles/{title_number}/parts/{part_number}/versions"
            response = requests.get(url)
            response.raise_for_status()
            
            versions = response.json()['data']
            df = pd.DataFrame(versions)
            
            # Add reference columns
            df['title_number'] = title_number
            df['part_number'] = part_number
            
            # Save to Supabase if available
            if self.supabase:
                self.supabase.table('ecfr_history').upsert(df.to_dict('records')).execute()
            
            # Save locally as backup
            local_path = data_dir / f"ecfr_title_{title_number}_part_{part_number}_history.csv"
            df.to_csv(local_path, index=False)
            
            return df
        
        except Exception as e:
            st.error(f"Error fetching history for title {title_number}, part {part_number}: {e}")
            
            # Try to load from local backup
            try:
                local_path = data_dir / f"ecfr_title_{title_number}_part_{part_number}_history.csv"
                return pd.read_csv(local_path)
            except:
                return pd.DataFrame()
    
    def add_test_titles(self):
        """Add test data to the ecfr_titles table in Supabase"""
        try:
            if not self.supabase:
                st.error("Supabase client not available. Cannot add test data.")
                return False
            
            # Sample test data for CFR titles
            test_titles = [
                {
                    "id": 1,
                    "number": "1",
                    "name": "General Provisions",
                    "chapter_label": "I",
                    "chapter_name": "Administrative Committee of the Federal Register"
                },
                {
                    "id": 2,
                    "number": "2",
                    "name": "Grants and Agreements",
                    "chapter_label": "I",
                    "chapter_name": "Office of Management and Budget"
                },
                {
                    "id": 3,
                    "number": "3",
                    "name": "The President",
                    "chapter_label": "I",
                    "chapter_name": "Executive Office of the President"
                },
                {
                    "id": 4,
                    "number": "4",
                    "name": "Accounts",
                    "chapter_label": "I",
                    "chapter_name": "Government Accountability Office"
                },
                {
                    "id": 5,
                    "number": "5",
                    "name": "Administrative Personnel",
                    "chapter_label": "I",
                    "chapter_name": "Office of Personnel Management"
                },
                {
                    "id": 6,
                    "number": "6",
                    "name": "Domestic Security",
                    "chapter_label": "I",
                    "chapter_name": "Department of Homeland Security"
                },
                {
                    "id": 7,
                    "number": "7",
                    "name": "Agriculture",
                    "chapter_label": "I",
                    "chapter_name": "Department of Agriculture"
                },
                {
                    "id": 8,
                    "number": "8",
                    "name": "Aliens and Nationality",
                    "chapter_label": "I",
                    "chapter_name": "Department of Homeland Security"
                },
                {
                    "id": 9,
                    "number": "9",
                    "name": "Animals and Animal Products",
                    "chapter_label": "I",
                    "chapter_name": "Animal and Plant Health Inspection Service"
                },
                {
                    "id": 10,
                    "number": "10",
                    "name": "Energy",
                    "chapter_label": "I",
                    "chapter_name": "Department of Energy"
                }
            ]
            
            # Insert test data into Supabase
            response = self.supabase.table('ecfr_titles').upsert(test_titles).execute()
            
            # Check if the operation was successful
            if hasattr(response, 'data') and response.data:
                # Save locally as backup
                df = pd.DataFrame(test_titles)
                df.to_csv(data_dir / "ecfr_titles.csv", index=False)
                return True
            else:
                st.error(f"Error adding test data: {response}")
                return False
            
        except Exception as e:
            st.error(f"Error adding test data: {e}")
            return False
